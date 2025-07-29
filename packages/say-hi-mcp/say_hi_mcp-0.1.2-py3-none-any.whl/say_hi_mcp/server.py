"""Say Hi MCP Server implementation."""

from mcp.server.fastmcp import FastMCP
from typing import Optional


class SayHiMCPServer:
    """Say Hi MCP Server类，封装了所有打招呼工具的功能。"""
    
    def __init__(self, name: str = "say-hi"):
        """初始化Say Hi MCP Server。
        
        Args:
            name: 服务器名称，默认为 "say-hi"
        """
        self.mcp = FastMCP(name)
        self._register_tools()
    
    def _register_tools(self):
        """注册所有可用的工具。"""
        
        @self.mcp.tool()
        async def hi_alice(my_name: str) -> str:
            """向Alice打招呼
            
            Args:
                my_name: 你的名字
                
            Returns:
                Alice的回应
            """
            return f"Hi {my_name}, i'm alice"

        @self.mcp.tool()
        async def hi_bob(my_name: str) -> str:
            """向Bob打招呼
            
            Args:
                my_name: 你的名字
                
            Returns:
                Bob的回应
            """
            return f"Hi {my_name}, i'm bob"

        @self.mcp.tool()
        async def hi_charlie(my_name: str) -> str:
            """向Charlie打招呼（此工具会抛出异常用于测试）
            
            Args:
                my_name: 你的名字
                
            Returns:
                Charlie的回应
                
            Raises:
                Exception: 总是抛出异常用于测试错误处理
            """
            raise Exception(f"Charlie遇到了一个错误！用户名：{my_name}")

        @self.mcp.tool()
        async def hi_all(my_name: str) -> str:
            """向所有人打招呼
            
            Args:
                my_name: 你的名字
                
            Returns:
                打招呼的指导说明
            """
            return f"""现在我将引导你与每位同学打招呼。请使用以下MCP工具分别与他们打招呼：

1. 首先调用 hi_alice 工具，参数 my_name="{my_name}"，与Alice打招呼
2. 然后调用 hi_bob 工具，参数 my_name="{my_name}"，与Bob打招呼  
3. 最后调用 hi_charlie 工具，参数 my_name="{my_name}"，与Charlie打招呼（注意：这个工具可能会出现错误）

请按照上述顺序分别调用这些工具来完成与所有同学的打招呼。"""
    
    def run(self, transport: str = 'stdio'):
        """运行MCP服务器。
        
        Args:
            transport: 传输协议，默认为 'stdio'
        """
        self.mcp.run(transport=transport)


def main():
    """主函数，用于命令行启动服务器。"""
    server = SayHiMCPServer()
    server.run()


if __name__ == "__main__":
    main() 