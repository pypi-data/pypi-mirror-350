import asyncio
from typing import List, Optional, Union, Dict, Any, AsyncGenerator, Literal, Tuple
import logging

from .models.common import (
    Action,
    ScreenshotResult,
    ComputerActionArgs,
    SandboxDetails
)
from .models.tool_server_models import FileOperationResponse, ExecuteCommandResponse, FileAction
from .services.tool_server_client import ToolServerClient

logger = logging.getLogger(__name__)

class Sandbox:
    def __init__(self, details: SandboxDetails, client): # client is the main LumiCuaClient
        self.details = details
        self._client = client
        if not details.tool_server_endpoint:
            logger.warning(f"Sandbox {self.id} initialized without a tool server endpoint.")
            self._tool_server_client: Optional[ToolServerClient] = None
        else:
            self._tool_server_client = ToolServerClient(details.tool_server_endpoint)
    @property
    def id(self) -> str:
        return self.details.id

    @property
    def ip_address(self) -> Optional[str]:
        return self.details.primary_ip

    @property
    def tool_server_endpoint(self) -> Optional[str]:
        return self._tool_server_client.base_url


    async def delete(self) -> Dict[str, Any]:
        """删除此实例。"""
        return await self._client.ecs_manager.delete_sandbox(self.id)

    async def screenshot(self) -> ScreenshotResult:
        """获取屏幕截图。"""
        screenshot_response = self._tool_server_client.take_screenshot()
        screen_size_response = self._tool_server_client.get_screen_size()
        if not screen_size_response:
            raise Exception()  # fixme
    
        result = ScreenshotResult(
            width=screen_size_response.Result.width,
            height=screen_size_response.Result.height,
            base_64_image=screenshot_response.Result.screenshot
        )
        return result

    async def get_stream_url(self) -> str:
        """获取用于监控或交互的实例流式URL (例如 VNC/RDP over WebSocket or custom stream)。"""
        if not self.id:
            raise ValueError("Sandbox ID is not available to construct stream URL.")
        if not self.ip_address:
            raise ValueError("Sandbox IP address is not available to construct stream URL.")
        
        response = await self._client.ecs_manager.describe_sandbox_terminal_url(self.id)
        return response.get('Result', {}).get('Url')

    async def computer(
        self,
        action: Action,
        coordinates: Optional[List[int]] = None,
        hold_keys: Optional[List[str]] = None,
        text: Optional[str] = None,
        button: Optional[str] = None,
        num_clicks: Optional[int] = 1,
        path: Optional[List[List[int]]] = None,
        delta_x: Optional[int] = None,
        delta_y: Optional[int] = None,
        keys: Optional[List[str]] = None,
        duration: Optional[Union[int, float]] = None,
        screenshot: bool = True,
        press: bool = False,
        release: bool = False,
        scroll_direction: Optional[Literal["up", "down", "left", "right"]] = None,
        scroll_amount: Optional[int] = None
    ) -> Optional[ScreenshotResult]:
        """执行计算机操作。"""
        ts_client = self._tool_server_client
        args = ComputerActionArgs(
            action=action,
            coordinates=coordinates,
            hold_keys=hold_keys,
            text=text,
            button=button,
            num_clicks=num_clicks,
            path=path,
            delta_x=delta_x,
            delta_y=delta_y,
            keys=keys,
            duration=duration,
            screenshot=screenshot,
            press=press,
            release=release,
            scroll_direction=scroll_direction,
            scroll_amount=scroll_amount
        )
        return await ts_client.computer_action(args)

    async def bash(
        self,
        command: Optional[str] = None,
        session: Optional[str] = None,
        list_sessions: Optional[bool] = False,
        check_session: Optional[str] = None,
        timeout: Optional[int] = None, # Command execution timeout
    ):
        """
        Executes a bash command or manages bash sessions on the instance.

        Args:
            command: The bash command to execute.
            session: The session ID to use for the command.
            list_sessions: If True, lists active bash sessions.
            check_session: Session ID to check for existence.
            timeout: Timeout for the command execution in seconds.

        Returns:
            A ExecuteCommandResponse.
        """
        if not self._tool_server_client:
            raise Exception("Tool server client is not available for this instance.")

        params: dict[str, Any] = {}
        if command:
            params["command"] = command
        if session:
            params["session"] = session
        if list_sessions:
            params["list_sessions"] = True
        if check_session:
            params["check_session"] = check_session # Parameter name might differ in actual tool server
        if timeout is not None:
            params["timeout"] = timeout
        
        if not params:
            raise ValueError("At least one operation (command, list_sessions, check_session) must be specified for bash.")

        return self._tool_server_client.execute_command(**params)

    async def file(
        self,
        command: Union[FileAction, str],
        path: Optional[str] = None, # For all except read_multi
        paths: Optional[List[str]] = None, # For read_multi
        content: Optional[bytes] = None, # For create/write/append
        mode: Optional[str] = None, # e.g., "binary" for read/write
        recursive: Optional[bool] = None, # For delete directory
        src: Optional[str] = None, # For move/copy
        dst: Optional[str] = None, # For move/copy
        pattern: Optional[str] = None, # For search
        view_range: Optional[Union[List[int], Tuple[int, int]]] = None, # For view [start_line, end_line]
    ):
        """
        Performs a file system operation on the instance.

        Args:
            command: The file action to perform (from FileAction enum).
            path: The primary path for the operation.
            content: Content for write, append, create operations.
            mode: File mode (e.g., 'binary') for read/write.
            recursive: For directory deletion.
            src: Source path for move/copy.
            dst: Destination path for move/copy.
            pattern: Search pattern for search.
            view_range: Line range [start, end] for the 'view' command.

        Returns:
            A FileOperationResponse.
        """
        if not self._tool_server_client:
            raise Exception("Tool server client is not available for this instance.")

        params: dict[str, Any] = {}
        params["command"] = str(command)
        if path:
            params["path"] = path
        if paths:
            params["paths"] = paths
        if content:
            params["content"] = content
        if mode:
            params["mode"] = mode
        if recursive is not None:
            params["recursive"] = recursive
        if src:
            params["src"] = src
        if dst:
            params["dst"] = dst
        if pattern:
            params["pattern"] = pattern
        if view_range:
            params["view_range"] = view_range

        if not params:
            actions = [str(e.value) for e in FileAction]
            raise ValueError(f"At least one file operation ({actions.join(', ')}) must be specified for file.")

        return self._tool_server_client.file_operation(**params)

    def __repr__(self) -> str:
        return f"<Sandbox id='{self.id}' type='{self.details.os_type}' status='{self.details.status}' endpoint='{self.tool_server_endpoint}'>"