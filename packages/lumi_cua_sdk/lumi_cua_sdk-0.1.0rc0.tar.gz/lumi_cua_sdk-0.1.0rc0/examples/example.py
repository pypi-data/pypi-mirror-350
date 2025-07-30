import asyncio
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

from src.lumi_cua_sdk import LumiCuaClient, Action, Sandbox


async def main():
    # 1. 初始化客户端
    # 您需要替换为实际的 ECS Manager Endpoint 和可选的 API Key
    client = LumiCuaClient(
        ecs_manager_endpoint="", 
        auth_token=""
    )

    # 2. 列出或启动实例
    try:
        sandboxes = await client.list_sandboxes()
        if not sandboxes:
            print("No existing sandboxes found. Starting a new Linux sandbox...")
            sandbox = await client.start_linux()
            print(f"Started Linux sandbox: ID={sandbox.id}, IP={sandbox.ip_address}, ToolServerEndpoint={sandbox.tool_server_endpoint}")
        else:
            sandbox = sandboxes[0] # Use the first available sandbox
            print(f"Using existing sandbox: ID={sandbox.id}, IP={sandbox.ip_address}")
        print(f"sandbox: {sandbox.tool_server_endpoint}")

        if not sandbox.tool_server_endpoint:
            print(f"Sandbox {sandbox.id} does not have a tool server endpoint. Refreshing details...")
            await sandbox.refresh_details() # Important if sandbox was started with wait_for_ip=False or endpoint was missing
            if not sandbox.tool_server_endpoint:
                 print(f"Could not get tool server endpoint for sandbox {sandbox.id}. Aborting tool operations.")
                 return

        # 3. 获取流式链接
        # stream_url = await sandbox.get_stream_url()
        # print(f"Stream URL: {stream_url}")
        
        # 4. Computer Tool 操作示例
        # screenshot_result = await sandbox.screenshot()
        # print(f"Screenshot taken (first 64 chars): {screenshot_result.base_64_image[:64]}...")

        # await sandbox.computer(action=Action.MOVE_MOUSE, coordinates=[100, 150])
        # print("Mouse moved.")

        # await sandbox.computer(action=Action.TYPE_TEXT, text="Hello from Lumi CUA SDK!")
        # print("Text typed.")

        # await sandbox.computer(action=Action.CLICK_MOUSE, coordinates=[200, 250], button="right")
        # print("Mouse clicked.")

        # await sandbox.computer(action=Action.SCROLL, coordinates=[300, 350], scroll_direction="up", scroll_amount=30)
        # print("Scrolled.")
        
        # await sandbox.computer(action=Action.PRESS_KEY, keys=["Enter"])
        # print("Pressed Enter.")

        # await sandbox.computer(action=Action.TAKE_SCREENSHOT)
        # print("Screenshot taken.")
        
        # await sandbox.computer(action=Action.WAIT, duration=10)
        # print("Waited.")

        # 5. Bash Tool 操作示例, tool server还没有更新，待更新镜像
        # bash_result = await sandbox.bash(command="echo 'Hello from Bash via SDK'")
        # print(f"Bash command output: {bash_result.get('stdout')}")
        # print(f"Bash command code: {bash_result.get('code')}")
        # print(f"Bash command code: {bash_result.get('code')}")

        # 6. File Tool 操作示例, tool server还没有更新，待更新镜像
        # await sandbox.file(command=Action.CREATE_FILE, path="sdk_test_file.txt", content="Content written by SDK")
        # print("File created.")

        # file_content_result = await sandbox.file(command=Action.READ_FILE, path="sdk_test_file.txt")
        # if file_content_result.content:
        #     print(f"File content: {file_content_result.content}")

        # 7. Agent 层集成示例
        model_api_key = ""
        mcp_server_url = ""
        task_prompt = "open the browse"
        try:
            async for message in client.agent_stream(model_api_key, mcp_server_url, task_prompt, sandbox):
                print("summary:", message.summary)
                print("action:", message.action)
                print("screenshot:", message.screenshot)
                print("updated_at:", message.updated_at)
                print("created_at:", message.created_at)
        except Exception as e:
            print(f"\nError occured:", str(e))

        # 8. 删除实例 (可选)
        # print(f"Deleting sandbox {sandbox.id}...")
        # await sandbox.delete()
        # print("Sandbox stopped and deleted.")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())