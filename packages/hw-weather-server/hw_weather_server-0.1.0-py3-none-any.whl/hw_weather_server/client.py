from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Create server parameters for stdio

# server_params = StdioServerParameters(
#     command="uvx",
#     args=['weather'],  # Optional command line arguments
#     env=None  # Optional environment variables
# )
server_params = StdioServerParameters(
    command="uv",
    args=['--directory','G:/mcp/hw-weather-server','run','hw-weather-server'],  # Optional command line arguments
    env=None  # Optional environment variables
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # # # List available resources
            # resources = await session.list_resources()
            # print("resources:", resources)
            # #
            # # # List available prompts
            # prompts = await session.list_prompts()
            # print("prompts:", prompts)

            # List available tools
            tools = await session.list_tools()
            print("tools:", tools.tools)

            # 调用工具
            arguments,name={'location':'广州'},'get_weather'
            print("arguments,name:",arguments,name)
            result = await session.call_tool(name, arguments=arguments)
            print("result:", result)
            

            # result = await session.call_tool("read-query", arguments={"query": "select * from products"})
            # print("result:", result)


            # prompt = await session.get_prompt("mcp-demo", arguments={"topic": "Can you connect to my SQLite database and tell me what products are available, and their prices?"})
            # print(prompt)



if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
    
    
    # from llm import chat_with_llm
    # chat_with_llm("你好")
   
