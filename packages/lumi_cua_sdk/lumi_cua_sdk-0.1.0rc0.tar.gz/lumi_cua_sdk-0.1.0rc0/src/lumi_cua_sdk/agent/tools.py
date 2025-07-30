from typing import Type, Optional, Any, List, Dict, Union
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
import logging
import asyncio

from ..sandbox import Sandbox
from ..models.common import Action, ScreenshotResult
from ..models.tool_server_models import FileOperationRequest, ExecuteCommandRequest, FileAction

logger = logging.getLogger(__name__)

class ComputerToolSchema(BaseModel):
    action: Action = Field(description="The computer action to perform.")
    coordinates: Optional[List[int]] = Field(None, description="Coordinates [x, y] for mouse actions like move, click, scroll.")
    hold_keys: Optional[List[str]] = Field(None, description="Keys to hold during a mouse move action.")
    text: Optional[str] = Field(None, description="Text to type for the type_text action.")
    button: Optional[str] = Field(None, description="Mouse button for click_mouse action (e.g., 'left', 'right', 'middle').")
    num_clicks: Optional[int] = Field(1, description="Number of clicks for click_mouse action.")
    path: Optional[List[List[int]]] = Field(None, description="Path as a list of [x, y] coordinates for drag_mouse action.")
    delta_x: Optional[int] = Field(None, description="Horizontal scroll amount for scroll action.")
    delta_y: Optional[int] = Field(None, description="Vertical scroll amount for scroll action.")
    keys: Optional[List[str]] = Field(None, description="Keys to press for press_key action (e.g., ['ctrl', 'c']).")
    duration: Optional[float] = Field(None, description="Duration for press_key (hold) or wait action in seconds.")
    screenshot: bool = Field(True, description="Whether to return a screenshot after the action.")

class ComputerTool(BaseTool):
    name: str = "computer_operation"
    description: str = (
        "Performs various computer operations like mouse movements, clicks, typing, key presses, scrolling, and taking screenshots. "
        "Returns a screenshot by default after most actions, unless 'screenshot' is set to False."
    )
    args_schema: Type[BaseModel] = ComputerToolSchema
    sandbox: Sandbox

    def _run(self, **kwargs: Any) -> Any:
        raise NotImplementedError("ComputerTool does not support synchronous execution.")

    async def _arun(self, **kwargs: Any) -> Optional[Dict[str, Any]]:
        logger.debug(f"ComputerTool executing with args: {kwargs}")
        action_args = ComputerToolSchema(**kwargs)
        result: Optional[ScreenshotResult] = await self.sandbox.computer(**action_args.model_dump())
        if result:
            return result.model_dump()
        return None

class BashTool(BaseTool):
    """Tool for executing bash commands on the instance."""
    args_schema: Type[BaseModel] = ExecuteCommandRequest
    sandbox: Sandbox
    name: str = "bash_shell"
    description: str = (
        "Executes bash commands on the remote instance. "
        "Use the 'command' parameter to specify the command string (e.g., 'ls -la'). "
        "Optional: 'session' to run in an existing session, 'list_sessions' (boolean) to list active sessions, "
        "'check_session' (session_id) to check if a session exists, 'timeout' (seconds) for command execution."
    )

    def _run(self,
        command: Optional[str] = None,
        session: Optional[int] = None,
        list_sessions: Optional[bool] = False,
        check_session: Optional[int] = None,
        timeout: Optional[int] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        return asyncio.run(self._arun(
            command=command,
            session=session,
            list_sessions=list_sessions,
            check_session=check_session,
            timeout=timeout,
            **kwargs
        ))

    async def _arun(
        self,
        command: Optional[str] = None,
        session: Optional[int] = None,
        list_sessions: Optional[bool] = False,
        check_session: Optional[int] = None,
        timeout: Optional[int] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        if not command and not list_sessions and check_session is None:
            return {"error": "BashTool requires 'command', 'list_sessions=True', or 'check_session=<id>'."}
        result = await self.sandbox.bash(
            command=command,
            session=session,
            list_sessions=list_sessions,
            check_session=check_session,
            timeout=timeout,
        )
        return result.model_dump(exclude_unset=True)

class FileTool(BaseTool):
    """Tool for performing file system operations on the instance."""
    args_schema: Type[BaseModel] = FileOperationRequest
    sandbox: Sandbox
    name: str = "file_system"
    description: str = (
        "Performs file system operations like read, read_multi, exists, write, list, delete, move, copy, etc. "
        "Specify the 'action' (from FileAction enum, e.g., 'read', 'write', 'list'). "
        "Other parameters depend on the command: "
        "'content' for write/append/create, 'mode' ('binary'), "
        "'path' (for all except read_muti)"
        "'paths' for read_multi"
        "'content' for write/append/create"
        "'pattern' for search"
        "'recursive' (for delete), 'src'/'dst' (for move/copy), 'view_range' (for view)."
    )

    def _run(
        self,
        command: str,
        path: Optional[str] = None,
        paths: Optional[List[str]] = None,
        content: Optional[Union[str, bytes]] = None,
        mode: Optional[str] = None,
        recursive: Optional[bool] = None,
        src: Optional[str] = None,
        dst: Optional[str] = None,
        pattern: Optional[str] = None,
        view_range: Optional[List[int]] = None,
        **kwargs: Any   
    ) -> Dict[str, Any]:
        return asyncio.run(self._arun(
            command=command,
            path=path,
            paths=paths,
            content=content,
            mode=mode,
            recursive=recursive,
            src=src,
            dst=dst,
            pattern=pattern,
            view_range=view_range,
            **kwargs
        ))

    async def _arun(
        self,
        command: str,
        path: Optional[str] = None,
        paths: Optional[List[str]] = None,
        content: Optional[Union[str, bytes]] = None,
        mode: Optional[str] = None,
        recursive: Optional[bool] = None,
        src: Optional[str] = None,
        dst: Optional[str] = None,
        pattern: Optional[str] = None,
        view_range: Optional[List[int]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        result = await self.sandbox.file(
            command=command,
            path=path,
            paths=paths,
            content=content,
            mode=mode,
            recursive=recursive,
            src=src,
            dst=dst,
            pattern=pattern,
            view_range=view_range,
        )
        return result.model_dump(exclude_unset=True)