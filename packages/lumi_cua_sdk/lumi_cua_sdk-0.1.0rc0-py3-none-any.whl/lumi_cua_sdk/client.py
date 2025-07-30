from typing import List, Optional, Dict, Any, AsyncGenerator

from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from .sandbox import Sandbox
from .agent.tools import ComputerTool, BashTool, FileTool
from .services.ecs_manager_client import ECSManagerClient
from .services.cua_uitars_agent import ComputerUseAgent
from .models.common import SandboxOsType
from .models.cua_uitars_agent_models import AgentStreamMessage
import json

import logging
logger = logging.getLogger(__name__)

class LumiCuaClient:
    """Client for interacting with the Lumi Computer Use Agent services."""

    def __init__(self, ecs_manager_endpoint: str, auth_token: Optional[str] = None):
        """
        Initializes the LumiCuaClient.

        Args:
            ecs_manager_endpoint: The endpoint for the ECS manager service.
            self.auth_token: Optional API key for authenticating with backend services.
        """
        self.auth_token = auth_token
        self.ecs_manager = ECSManagerClient(ecs_manager_endpoint=ecs_manager_endpoint, api_key=auth_token)
        logger.info(f"LumiCuaClient initialized. ECS Manager: {ecs_manager_endpoint}")

    async def list_sandboxes(self) -> List[Sandbox]:
        """
        Lists available CUA sandboxes by calling the ECS manager.

        Returns:
            A list of Sandbox objects.
        """
        logger.info("Listing sandboxes via ECS manager.")
        sandboxes_detail_list = await self.ecs_manager.describe_sandboxes()
        return [Sandbox(details=details, client=self) for details in sandboxes_detail_list]


    async def start_linux(self, wait_for_ip: bool = True, wait_timeout: int = 300) -> Sandbox:
        """
        Starts a new Linux CUA sandbox using the ECS manager.

        Args:
            wait_for_ip: If True, waits until the sandbox has a private IP.
            wait_timeout: Timeout in seconds for waiting for the IP.

        Returns:
            An Sandbox object representing the started Linux sandbox.
        """
        logger.info(f"Attempting to start a Linux sandbox (wait_for_ip={wait_for_ip}).")
        sandbox_details = await self.ecs_manager.create_sandbox(
            os_type=SandboxOsType.LINUX, 
            wait_for_ip=wait_for_ip,
            wait_timeout=wait_timeout
        )
        logger.info(f"Linux sandbox started via ECS manager: id={sandbox_details.id}, ip={sandbox_details.primary_ip}")
        return Sandbox(details=sandbox_details, client=self)

    async def start_window(self, wait_for_ip: bool = True, wait_timeout: int = 300) -> Sandbox:
        """
        Starts a new Windows CUA sandbox using the ECS manager.

        Args:
            wait_for_ip: If True, waits until the sandbox has a private IP.
            wait_timeout: Timeout in seconds for waiting for the IP.

        Returns:
            An Sandbox object representing the started Windows sandbox.
        """
        logger.info(f"Attempting to start a Windows sandbox (wait_for_ip={wait_for_ip}).")
        sandbox_details = await self.ecs_manager.start_sandbox(
            os_type=SandboxOsType.WINDOWS, 
            wait_for_ip=wait_for_ip,
            wait_timeout=wait_timeout
        )
        logger.info(f"Windows sandbox started via ECS manager: id={sandbox_details.id}, ip={sandbox_details.private_ip}")
        return Sandbox(details=sandbox_details, client=self)

    async def agent_stream(
        self,
        model_api_key: str,
        mcp_server_url: str,
        task_prompt: str,
        sandbox: Sandbox,
        model_name: str = "doubao-1.5-ui-tars-250328",
        base_url: str = "https://ark.cn-beijing.volces.com/api/v3",
        max_images: int = 5,
        max_action: int = 100,
        step_interval: int = 3,
        wait_interval: int = 1
    ) -> AsyncGenerator[AgentStreamMessage, None]:
        """
        Creates, initializes, and runs the ComputerUseAgent, yielding parsed stream messages.

        Args:
            model_api_key: API key for the model service.
            mcp_server_url: URL for the MCP server.
            task_prompt: The task prompt for the agent.
            sandbox: The sandbox to use.
            model_name: Name of the model to use.
            base_url: Base URL for the model API.
            max_images: Maximum number of images to use in prompts.
            max_action: Maximum number of actions the agent can take.
            step_interval: Interval in seconds to wait after an action.
            wait_interval: Interval in seconds for the 'wait' action.

        Yields:
            AgentStreamMessage: Parsed messages from the agent's run stream.
        """
        cua_agent = None # Initialize to None for the finally block
        try:
            cua_agent = create_computer_use_agent(
                model_api_key=model_api_key,
                mcp_server_url=mcp_server_url,
                auth_token=self.auth_token,
                model_name=model_name,
                base_url=base_url,
                max_images=max_images,
                max_action=max_action,
                step_interval=step_interval,
                wait_interval=wait_interval
            )
            await cua_agent.initialize()
            logger.info("ComputerUseAgent initialized.")
            logger.info(f"Running agent with task: {task_prompt} in sandbox: {sandbox.id}")
            async for sse_event_str in cua_agent.run(query=task_prompt, sandbox_id=sandbox.id, sandbox_endpoint=sandbox.tool_server_endpoint):
                if isinstance(sse_event_str, str):
                    lines = sse_event_str.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith("data:"):
                            json_str = line[len("data:"):].strip()
                            if json_str:
                                try:
                                    json_data = json.loads(json_str)
                                    if isinstance(json_data, dict):
                                        # Assuming AgentStreamMessage is the correct model for the content of 'data'
                                        parsed_message = AgentStreamMessage(**json_data)
                                        yield parsed_message
                                    else:
                                        logger.warning(f"Parsed JSON data from SSE is not a dict: {json_data}")
                                except json.JSONDecodeError as jde:
                                    logger.error(f"JSON decoding failed for SSE data: {json_str}. Error: {jde}")
                                except Exception as e:
                                    logger.error(f"Error processing SSE data part: {json_str}, error: {e}")
                            # else: SSE data field was empty
                        # else: line is not an SSE data line (e.g. event, id, retry, or comment)
                else:
                    logger.warning(f"Received unexpected message type from agent.run: {type(sse_event_str)}, content: {sse_event_str}")
        finally:
            if cua_agent: # Ensure agent was initialized before trying to close
                await cua_agent.aclose()
                logger.info("ComputerUseAgent closed.")

def create_computer_use_agent(
    model_api_key: str,
    mcp_server_url: str,
    auth_token: str,
    model_name: str = "doubao-1.5-ui-tars-250328",
    base_url: str = "https://ark.cn-beijing.volces.com/api/v3",
    max_images: int = 5,
    max_action: int = 100,
    step_interval: int = 3,
    wait_interval: int = 1
) -> ComputerUseAgent:
    """
    Factory function to create and initialize a ComputerUseAgent instance.

    Args:
        model_api_key: API key for the model service.
        mcp_server_url: URL for the MCP server.
        auth_token: Authentication token for computer use environment's ECS Manager Server.
        model_name: Name of the model to use, doubao-1.5-ui-tars-250328 by default. 
        base_url: Base URL for the model API, https://ark.cn-beijing.volces.com/api/v3 by default.
        max_images: Maximum number of images to use in prompts, 5 by default.
        max_action: Maximum number of actions the agent can take, 100 by default.
        step_interval: Interval in seconds to wait after an action, 3 by default.
        wait_interval: Interval in seconds for the 'wait' action, 1 by default.

    Returns:
        An uninitialized ComputerUseAgent instance.
    """
    logger.info(f"Creating ComputerUseAgent with model: {model_name}, MCP URL: {mcp_server_url}")
    agent = ComputerUseAgent(
        model_api_key=model_api_key,
        mcp_server_url=mcp_server_url,
        auth_token=auth_token,
        model_name=model_name,
        base_url=base_url,
        max_images=max_images,
        max_action=max_action,
        step_interval=step_interval,
        wait_interval=wait_interval
    )
    return agent
