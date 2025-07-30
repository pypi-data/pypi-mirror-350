"""Lumi Computer Use Agent SDK"""

import logging

from .client import LumiCuaClient, create_computer_use_agent
from .sandbox import Sandbox
from .agent.tools import ComputerTool, BashTool, FileTool
from .models.common import (
    Action,
    ScreenshotResult,
    ComputerActionArgs,
    SandboxDetails,
    SandboxStatus,
    SandboxOsType,
)
from .services.ecs_manager_client import ECSManagerClient
from .services.tool_server_client import ToolServerClient

# Configure logging for the SDK
# Basic configuration, users can override this.
logger = logging.getLogger(__name__) # Use __name__ which will be 'lumi_cua_sdk'
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Set default logging level for the SDK. Can be configured by the user.
logger.setLevel(logging.INFO) 

__all__ = [
    "LumiCuaClient",
    "Sandbox",
    "ComputerTool",
    "BashTool",
    "FileTool",
    "Action",
    "ScreenshotResult",
    "ComputerActionArgs",
    "SandboxDetails",
    "SandboxStatus",
    "ECSManagerClient",
    "ToolServerClient",
    "create_computer_use_agent"
    "logger"
]