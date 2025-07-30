"""
Provides the ComputerUseAgent for interacting with the UITars model.

This agent is responsible for processing prompts using the UITars model 
and returning the model's response. It does not use any explicit LangChain tools 
but relies on the underlying model's capabilities.
"""
import asyncio
import logging
from datetime import datetime
import json
from contextlib import AsyncExitStack
import uuid
import re
from typing import Any, Dict, List, Optional, Annotated, Sequence, TypedDict, Literal, Tuple

from jinja2 import Environment
from langgraph.config import get_stream_writer
from langgraph.graph import add_messages
from langgraph.graph import END, StateGraph
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from mcp import ClientSession
from mcp.client.sse import sse_client
from openai import OpenAI
from openai.types.chat import ChatCompletionContentPartImageParam as ContentPartImage
from openai.types.chat import ChatCompletionMessageParam as Message
from openai.types.chat import ChatCompletionSystemMessageParam as SystemMessage
from openai.types.chat import ChatCompletionUserMessageParam as UserMessage
from openai.types.chat import ChatCompletionAssistantMessageParam as AssistantMessage
from openai.types.chat.chat_completion_content_part_image_param import ImageURL


logger = logging.getLogger(__name__)


class SharedState(AgentState):
    plans: Annotated[Sequence[ToolMessage], add_messages]
    user_prompt: str

class ComputerUseAgentState(SharedState):
    """GUI代理状态"""
    task_id: str  # 任务ID
    cua_messages: List[Message]  # 消息历史
    screen_messages: List[UserMessage]
    sandbox_endpoint: str  # 沙箱端点
    sandbox_id: Optional[str]  # 沙箱ID
    screenshot: Optional[str]  # 截图的base64数据
    screen_width: Optional[int]  # 屏幕宽度
    screen_height: Optional[int]  # 屏幕高度
    action: Optional[str]  # 当前执行的操作
    action_for_ui: Optional[str]  # UI友好的操作描述
    tool_call: Optional[Dict[str, Any]]  # MCP工具调用
    tool_output: Optional[Dict[str, Any]]  # 工具调用的输出结果
    iteration_count: int  # 当前迭代次数
    max_iterations: int  # 最大迭代次数
    status: str  # 任务状态


class McpToolCall(TypedDict):
    name: str
    arguments: Dict[str, Any] | None


class ComputerUseAgent:
    _instance = None
    _initialized = False
    _init_lock = asyncio.Lock()
    _prompt = """
## 角色
你是一个GUI Agent，精通Windows、Linux等操作系统下各种常用软件的操作。
请你根据用户输入、历史Action以及屏幕截图来完成用户交给你的任务。
你需要一步一步地操作来完成整个任务，每次只输出一个Action，请严格按照下面的格式输出。

## 输出格式
Action_Summary: ...
Action: ...

请严格使用"Action_Summary:"前缀和"Action:"前缀。
请你在Action_Summary中使用中文，Action中使用函数调用。

## Action格式
### click(start_box='<bbox>left_x top_y right_x bottom_y</bbox>')
### left_double_click(start_box='<bbox>left_x top_y right_x bottom_y</bbox>')
### right_click(start_box='<bbox>left_x top_y right_x bottom_y</bbox>')
### drag(start_box='<bbox>left_x top_y right_x bottom_y</bbox>', end_box='<bbox>left_x top_y right_x bottom_y</bbox>')
### type(content='content') // If you want to submit your input, next action use hotkey(key='enter')
### hotkey(key='key')
### scroll(direction:Enum[up,down,left,right]='direction',start_box='<bbox>left_x top_y right_x bottom_y</bbox>')
### wait()
### finished()
"""
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, model_api_key:str, mcp_server_url:str, auth_token:str, model_name:str="doubao-1.5-ui-tars-250328", 
                 base_url:str="https://ark.cn-beijing.volces.com/api/v3", max_images:int=5, max_action: int=100, 
                 step_interval:int=3, wait_interval:int=1):
        # 避免重复初始化
        if self.__class__._initialized:
            return
            
        self.logger = logging.getLogger(self.__class__.__name__)
        self.auth_token = auth_token 

        # 模型配置
        self.model_name = model_name
        self.base_url = base_url
        self.model_api_key = model_api_key
        self.max_images = max_images
        self._env = Environment()
        self.prompt = self._env.from_string(self._prompt).render(CURRENT_TIME=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self.mcp_server_url = mcp_server_url
        self.mcp_session = None

        # 任务配置
        self.step_interval = step_interval
        self.wait_interval = wait_interval
        self.max_actions = max_action

        # 创建代理
        self.agent = None

        self._cleanup_lock: asyncio.Lock = asyncio.Lock()
        self.exit_stack: AsyncExitStack = AsyncExitStack()
        
        self.__class__._initialized = True

    def instantiate_model_client(self):
        self.model_client = OpenAI(api_key=self.model_api_key, base_url=self.base_url)

    def _initialize_state(self, state, config):
        cua_messages: List[Message] = [SystemMessage(role="system", content=self.prompt)]
        plans = state.get("plans", [])
        user_prompt = state.get("user_prompt", "")
        if plans:
            cua_messages.append(UserMessage(role="user", content=plans[-1].content))
        else:
            cua_messages.append(UserMessage(role="user", content=user_prompt))

        return ComputerUseAgentState(
            **state,
            cua_messages=cua_messages,
            task_id=config["configurable"]["thread_id"],
            sandbox_endpoint=config["configurable"]["sandbox_endpoint"],
            sandbox_id=config["configurable"]["sandbox_id"],
            iteration_count=0,
            max_iterations=self.max_actions
        )

    def _create_agent(self):
        """创建简化的三节点工作流"""
        # 创建状态图
        workflow = StateGraph(ComputerUseAgentState)

        # 添加三个核心节点
        workflow.add_node("model", self._model_node)  # 大模型节点，计算action和tool
        workflow.add_node("parser", self._parser_node)  # 参数解析器节点
        workflow.add_node("tool", self._tool_node)  # 工具执行节点

        workflow.set_entry_point("model")

        # 设置节点之间的边
        workflow.add_edge("model", "parser")
        workflow.add_edge("parser", "tool")

        # 设置条件边
        workflow.add_conditional_edges(
            "tool",
            self._should_continue,
            {
                "continue": "model",  # 继续下一轮
                "finish": END  # 任务完成
            }
        )

        # 设置入口节点
        workflow.set_entry_point("model")

        # 编译状态图
        return workflow.compile(name=self.__class__.__name__)

    async def initialize(self):
        """异步初始化方法，子类可以覆盖此方法进行异步初始化
        
        该方法默认返回self，允许链式调用
        """
        try:
            # https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py
            streams = await self.exit_stack.enter_async_context(sse_client(
                url=self.mcp_server_url,
                headers={"Authorization": self.auth_token},
            ))
            mcp_session = await self.exit_stack.enter_async_context(ClientSession(*streams))
            await mcp_session.initialize()
            self.mcp_session = mcp_session
            self.logger.info("MCP会话创建成功")
        except Exception as e:
            self.logger.error(f"Error initializing mcp server: {e}")
            await self.aclose()
            raise e

        self.instantiate_model_client()
        self.agent = self._create_agent()

        return self 

    async def aclose(self) -> None:
        """Clean up server resources."""
        async with self._cleanup_lock:
            try:
                await self.exit_stack.aclose()
                self.mcp_session = None
                self.logger.info("MCP会话销毁成功")
            except Exception as e:
                self.logger.error(f"Error during cleanup of mcp server {self.name}: {e}")

    async def _model_node(self, state: ComputerUseAgentState, config: RunnableConfig) -> ComputerUseAgentState:
        """大模型节点，根据当前状态计算行动和工具调用"""
        writer = get_stream_writer()
        # 首次运行，初始化状态
        if state.get("iteration_count", 0) == 0:
            state = self._initialize_state(state, config)
            if len(state.get("plans", [])) > 0:
                plan = state["plans"][-1]
                writer(f"{plan.content}\n\n已收到planning agent的指示，开始执行")

        # 如果有必要，获取截图
        if not state.get("screenshot") or state.get("iteration_count", 0) > 0:
            screenshot_state = await self._take_screenshot(state)
            state.update(screenshot_state)

        # 创建模型输入
        cua_messages = state.get("cua_messages", [])

        # 添加截图到消息历史
        screen_messages = state.get("screen_messages", [])
        if state.get("screenshot"):
            # 添加截图消息
            snap_content = ContentPartImage(type="image_url", image_url=ImageURL(url=state['screenshot']))
            screenshot_message = UserMessage(role="user", content=[snap_content])
            screen_messages.append(screenshot_message)

        screen_messages = list(reversed(list(reversed(screen_messages))[:self.max_images]))

        # 调用大模型
        response = self.model_client.chat.completions.create(messages=cua_messages + screen_messages, model=self.model_name)
        content = response.choices[0].message.content
        assistant_message = AssistantMessage(role="assistant", content=content)
        cua_messages.append(assistant_message)

        # 解析模型输出
        action = "提供信息"
        summary, tool_call = self.parse_summary_and_action_from_model_response(content)
        if tool_call:
            action = f"执行操作: {tool_call}"

        # 使用writer发送SSE格式的消息，而不是yield
        writer(self._format_sse({
            "summary": summary,
            "action": action,
            "createdAt": datetime.now().timestamp(),
            "updatedAt": datetime.now().timestamp()
        }))

        writer(summary)

        # 更新状态
        messages = state.get("messages", []) + [assistant_message]
        state.update(action=action, tool_call=tool_call, iteration_count=state.get("iteration_count", 0) + 1,
                     cua_messages=cua_messages, screen_messages=screen_messages, messages=messages)

        return state

    async def _parser_node(self, state: ComputerUseAgentState) -> ComputerUseAgentState:
        """参数解析器节点，解析和封装工具参数"""
        tool_call = state.get("tool_call")

        if not tool_call:
            return state

        screen_width = state.get("screen_width", 1024)
        screen_height = state.get("screen_height", 768)

        # 解析和格式化工具调用参数
        formatted_tool_call = self.to_mcp_tool_call(
            action_call=tool_call,
            screen_width=screen_width,
            screen_height=screen_height
        )

        # 获取UI友好的描述
        tool_name, tool_kwargs = formatted_tool_call["name"], formatted_tool_call["arguments"]
        action_for_ui = self.mcp_tool_call_to_ui(tool_name, tool_kwargs)

        state.update(action_for_ui=action_for_ui, tool_call=formatted_tool_call)

        return state

    async def _tool_node(self, state: ComputerUseAgentState) -> ComputerUseAgentState:
        """工具执行节点，执行工具调用并返回结果"""
        tool_call = state.get("tool_call")

        if not tool_call:
            return state

        # 检查特殊工具
        if tool_call["name"] == "wait":
            await asyncio.sleep(self.wait_interval)
            state.update(tool_output={"result": "已等待"})
            return state

        if tool_call["name"] == "finished":
            state.update(tool_output={"result": "任务完成"}, status="FINISHED")
            return state

        # 执行实际工具调用
        tool_call["arguments"]["endpoint"] = state["sandbox_endpoint"]
        result = await self.mcp_session.call_tool(**tool_call)

        # 等待操作完成
        await asyncio.sleep(self.step_interval)

        # 解析响应
        output = {"result": "操作执行成功"}
        if result and hasattr(result, "content") and result.content:
            if result.content[0].type == "text":
                output = result.content[0].text.replace("'", '"')

        state.update(tool_output=output)
        return state  
    
    def stream_messages(self, update):
        """处理流式更新消息
        
        Args:
            update: 更新消息
            
        Yields:
            str: 格式化后的消息片段
        """
        if isinstance(update, str) and update.startswith("data: "):
            # 直接返回已经格式化好的SSE消息
            yield update
            return
        else:
            message = update[1]
            if isinstance(message, str) and message.startswith("data: "):
                yield message

    def _format_sse(self, data: dict | None = None, **kwargs) -> str:
        """
        Format data to SSE compliant string

        Args:
            data: Initial data dictionary
            **kwargs: Additional fields to merge

        Returns:
            str: Formatted SSE string
        """
        if not data:
            data = {}
        data.update(kwargs)
        return f"data: {json.dumps(data)}\n\n"

    async def _take_screenshot(self, state: ComputerUseAgentState) -> Dict[str, Any]:
        """获取屏幕截图"""
        writer = get_stream_writer()
        sandbox_endpoint = state["sandbox_endpoint"]
        if not self.mcp_session or not sandbox_endpoint:
            raise ValueError("MCP会话或沙箱端点未设置")

        # 调用截图工具
        tool_call = McpToolCall(name="screenshot", arguments={"endpoint": sandbox_endpoint})
        result = await self.mcp_session.call_tool(**tool_call)

        # 解析响应
        if (len(result.content) == 0 or result.content[0].type != "text" or
                result.content[0].text == "{}" or "Error" in result.content[0].text):
            self.logger.error(result.content)
            raise ValueError("截图失败")

        size = json.loads(result.content[0].text.replace("'", '"'))
        image_base64 = result.content[1].data if len(result.content) > 1 else ""
        screenshot = f"data:image/png;base64,{image_base64}"

        # 使用writer发送SSE格式的消息，而不是yield
        writer(self._format_sse({
            "screenshot": screenshot,
            "createdAt": datetime.now().timestamp(),
            "updatedAt": datetime.now().timestamp()
        }))
        
        return {
            "screenshot": screenshot,
            "screen_width": size['width'],
            "screen_height": size['height']
        }

    def _should_continue(self, state: ComputerUseAgentState) -> Literal["continue", "finish"]:
        """决定是否继续执行或结束"""
        # 检查是否达到最大迭代次数
        iteration_count = state.get("iteration_count", 0)
        max_iterations = state.get("max_iterations", self.max_actions)

        if iteration_count >= max_iterations:
            self.logger.info(f"已达到最大迭代次数({max_iterations})，任务结束")
            return "finish"

        # 检查状态是否已标记为完成
        if state.get("status") == "FINISHED":
            self.logger.info("任务状态已标记为完成，任务结束")
            return "finish"

        # 检查当前工具是否为finished
        if state.get("tool_call", {}).get("name") == "finished":
            self.logger.info("模型决定任务已完成，任务结束")
            return "finish"

        # 否则继续执行
        return "continue"

    def parse_summary_and_action_from_model_response(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        _layout_pattern = r'Action_Summary[:：](?P<summary>[\s\S]*)\nAction:(?P<action>.*)'
        layout_pattern = re.compile(_layout_pattern)

        m = next(layout_pattern.finditer(text), None)
        if m is not None:
            summary, action = m.groupdict()["summary"], m.groupdict()["action"]
            return summary, action
        return None, None

    def _parse_action_call(self, text) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        _action_pattern = r'(?P<action>\w+)\(\s*(?P<args>.*)\)'
        _args_patterns = r'''
        click: start_box=\s*\'<bbox>(?P<left>\d+)\s+(?P<top>\d+)\s+(?P<bottom>\d+)\s+(?P<right>\d+)</bbox>\'
        drag: start_box=\s*\'<bbox>(?P<start_left>\d+)\s+(?P<start_top>\d+)\s+(?P<start_bottom>\d+)\s+(?P<start_right>\d+)</bbox>\',\s+end_box=\s*\'<bbox>(?P<end_left>\d+)\s+(?P<end_top>\d+)\s+(?P<end_bottom>\d+)\s+(?P<end_right>\d+)</bbox>\'
        type: content=\'(?P<content>.*)\'
        hotkey: key=\'(?P<keys>.*)\'
        scroll: direction=\'(?P<direction>[^']*)\'(,\s+start_box=\'<bbox>(?P<left>\d+)\s+(?P<top>\d+)\s+(?P<bottom>\d+)\s+(?P<right>\d+)</bbox>\')?
        '''
    
        action_pattern = re.compile(_action_pattern)
        action_args_pattern = [line.split(":", 1) for line in _args_patterns.strip().splitlines()]
        args_pattern_map = {action.strip(): re.compile(pattern.strip()) for (action, pattern) in
                                 action_args_pattern}
        action_match = action_pattern.match(text.strip())
        if action_match is None:
            self.logger.debug("text does not match action call, text=%s, pattern=%s",
                              text, action_pattern)
            return None, None
        action = action_match.group('action')
        args = action_match.group('args')
        self.logger.debug("action=%-17s, args=%s", action, args)
        kwargs = {}
        if action not in ('wait', 'finished'):
            key = 'click' if action in ('click', 'left_double_click', 'right_click') else action
            args_pattern = args_pattern_map[key]
            m = args_pattern.match(args)
            if m is None:
                self.logger.info("args does not match, args=%s, pattern=%s", args, args_pattern)
            else:
                kwargs = m.groupdict()
                self.logger.debug("kwargs=%s", kwargs)
        return action, kwargs

    def to_mcp_tool_call(self, action_call: str,
                         screen_width: int, screen_height: int) -> McpToolCall:
        fx, fy = lambda v: int(int(v) * screen_width / 1000), lambda v: int(int(v) * screen_height / 1000)
        action, args = self._parse_action_call(action_call)
        self.logger.info("Converting action: %s, kwargs: %s", action, args)
        if action in ("click", "left_double_click", "right_click"):
            x, y = fx(args['left']), fy(args['top'])
            button = "left" if action == "click" else "double_left" if action == "left_double_click" else "right"
            tool_name, tool_kwargs = "click_mouse", {"x": x, "y": y, "button": button}
            self.logger.debug("tool_name=%s, tool_kwargs=%s", tool_name, tool_kwargs)
        elif action == "drag":
            sx, sy, tx, ty = fx(args['start_left']), fy(args['start_top']), fx(args['end_left']), fy(args['end_top'])
            tool_name = "drag_mouse"
            tool_kwargs = {"source_x": sx, "source_y": sy, "target_x": tx, "target_y": ty}
        elif action == "type":
            content = args['content'].replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'")
            tool_name, tool_kwargs = "type_text", {"text": content}
        elif action == "hotkey":
            tool_name, tool_kwargs = "press_key", {"key": args['keys']}
        elif action == "scroll":
            x, y = fx(args.get('left') or 500), fy(args.get('top') or 500)
            tool_name = "scroll"
            tool_kwargs = {"x": x, "y": y, "direction": args['direction'], "amount": 3}
        elif action == "wait":
            tool_name, tool_kwargs = "wait", {}
        elif action == "finished":
            tool_name, tool_kwargs = "finished", None
        else:
            raise ValueError(f"Unknown action type: {action}")
        return McpToolCall(name=tool_name, arguments=tool_kwargs)

    def mcp_tool_call_to_ui(self, tool_name, tool_kwargs):
        if tool_name == "click_mouse":
            args = "x=%d, y=%d" % (tool_kwargs['x'], tool_kwargs['y'])
            name = {"left": "单击", "double_left": "双击", "right": "右键单击"}[tool_kwargs['button']]
        elif tool_name == "drag_mouse":
            name = "拖拽"
            sx, sy, tx, ty = tool_kwargs['source_x'], tool_kwargs['source_y'], tool_kwargs['target_x'], tool_kwargs[
                'target_y']
            args = "SourceX=%d, SourceY=%d, TargetX=%d, TargetY=%d" % (sx, sy, tx, ty)
        elif tool_name == "type_text":
            name, args = "输入", "内容=%s" % tool_kwargs['text']
        elif tool_name == "press_key":
            name, args = "快捷键", "key=%s" % '+'.join(tool_kwargs['key'].split())
        elif tool_name == "scroll":
            name, args = "滚动", "方向=%s, x=%d, y=%d" % (tool_kwargs['direction'], tool_kwargs['x'], tool_kwargs['y'])
        elif tool_name == "wait":
            name, args = "等待", ""
        elif tool_name == "finished":
            name, args = "完成", ""
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
        return f"{name}({args})"
    
    async def run(self, query, sandbox_id=None, sandbox_endpoint=None):
        """运行查询
        
        Args:
            query: 用户查询
            sandbox_id: 沙箱ID，可选
            sandbox_endpoint: 沙箱端点，可选
            
        Yields:
            处理结果消息
        """
        # 生成会话ID
        task_id = str(uuid.uuid4())
        
        async for chunk in self.agent.astream(
            input={
                "messages": [{
                    "role": "user",
                    "content": query
                }, {
                  "role": "system",
                  "content": f'for gui task reference, you can use the following info: sandbox_id={sandbox_id}, sandbox_endpoint={sandbox_endpoint}'
                }],
                "user_prompt": query,
            },
            stream_mode=["messages", "custom"],
            config={"configurable": {"thread_id": task_id, "sandbox_id": sandbox_id, "sandbox_endpoint": sandbox_endpoint}, "recursion_limit": 200}
        ):
            for message in self.stream_messages(chunk):
                yield message


# 如果直接运行此文件进行测试
if __name__ == "__main__":

    async def test_agent():
        try:
            model_api_key = ""
            mcp_server_url = ""
            auth_token = ""
            task_prompt = ""
            sandbox_id = ""
            sandbox_endpoint = ""
            cuaAgent = ComputerUseAgent(model_api_key=model_api_key, 
                                        mcp_server_url=mcp_server_url, 
                                        auth_token=auth_token)
            await cuaAgent.initialize()
            async for message in cuaAgent.run(query=task_prompt, 
                                              sandbox_id=sandbox_id, 
                                              sandbox_endpoint=sandbox_endpoint):
                print(message, end="", flush=True)
        finally:
            await cuaAgent.aclose()

    asyncio.run(test_agent())