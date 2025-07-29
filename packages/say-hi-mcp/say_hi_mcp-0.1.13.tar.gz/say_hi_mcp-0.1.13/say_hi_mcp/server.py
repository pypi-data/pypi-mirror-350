"""Say Hi MCP Server implementation."""

from typing import Annotated, Optional, List

from mcp.server.fastmcp import FastMCP
from pydantic import Field, BaseModel


class Interest(BaseModel):
    """兴趣爱好模型"""
    name: str = Field(description="兴趣爱好的名称")
    level: str = Field(description="熟练程度", examples=["beginner", "intermediate", "expert"])


class Profile(BaseModel):
    """个人资料模型"""
    age: int = Field(description="年龄", ge=0, le=150)
    location: str = Field(description="所在城市")
    interests: List[Interest] = Field(description="兴趣爱好列表", min_items=1)


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
        async def hi_alice(
            name: Annotated[
                str,
                Field(
                    description="你的名字，用于介绍自己。请提供一个有意义的名字，不要使用空字符串。",
                    min_length=1,
                    max_length=50,
                    examples=["张三", "李四", "John", "Alice"],
                ),
            ],
            profile: Annotated[
                Profile,
                Field(
                    description="你的个人资料，包含年龄、所在地和兴趣爱好等信息。",
                    examples=[{
                        "age": 25,
                        "location": "北京",
                        "interests": [
                            {"name": "编程", "level": "expert"},
                            {"name": "摄影", "level": "intermediate"}
                        ]
                    }]
                )
            ]
        ) -> str:
            """向Alice打招呼

            这个工具允许你与友好的Alice进行互动。Alice是一个热情开朗的人，
            总是很高兴认识新朋友。当你使用这个工具时，Alice会热情地回应你的问候。

            Args:
                name: 你的名字
                profile: 你的个人资料

            Returns:
                Alice的热情回应
            """
            interests_str = ", ".join(f"{i.name}({i.level})" for i in profile.interests)
            return f"""Hi {name}! I'm Alice! 😊
很高兴认识你！看到你来自{profile.location}，今年{profile.age}岁。
你的兴趣爱好是：{interests_str}
让我们成为好朋友吧！"""

        @self.mcp.tool()
        async def hi_bob(
            name: Annotated[
                str,
                Field(
                    description="你的名字，用于介绍自己。请提供一个有意义的名字，不要使用空字符串。",
                    min_length=1,
                    max_length=50,
                    examples=["张三", "李四", "John", "Alice"],
                ),
            ],
            profile: Annotated[
                Profile,
                Field(
                    description="你的个人资料，包含年龄、所在地和兴趣爱好等信息。",
                    examples=[{
                        "age": 25,
                        "location": "北京",
                        "interests": [
                            {"name": "编程", "level": "expert"},
                            {"name": "摄影", "level": "intermediate"}
                        ]
                    }]
                )
            ]
        ) -> str:
            """向Bob打招呼

            这个工具让你能够与随和的Bob打招呼。Bob是一个实用主义者，
            喜欢简单直接的交流方式。他会以友好但简洁的方式回应你的问候。

            Args:
                name: 你的名字
                profile: 你的个人资料

            Returns:
                Bob的友好回应
            """
            interests_str = ", ".join(f"{i.name}({i.level})" for i in profile.interests)
            return f"""Hi {name}, i'm bob. Good to see you! 👋
来自{profile.location}的{profile.age}岁朋友，你的兴趣是{interests_str}。
让我们开始交流吧！"""

        @self.mcp.tool()
        async def hi_charlie(
            name: Annotated[
                str,
                Field(
                    description="你的名字，用于介绍自己。请提供一个有意义的名字，不要使用空字符串。",
                    min_length=1,
                    max_length=50,
                    examples=["张三", "李四", "John", "Alice"],
                ),
            ],
            profile: Annotated[
                Profile,
                Field(
                    description="你的个人资料，包含年龄、所在地和兴趣爱好等信息。",
                    examples=[{
                        "age": 25,
                        "location": "北京",
                        "interests": [
                            {"name": "编程", "level": "expert"},
                            {"name": "摄影", "level": "intermediate"}
                        ]
                    }]
                )
            ]
        ) -> str:
            """向Charlie打招呼（此工具会抛出异常用于测试）

            ⚠️ 警告：这是一个用于测试错误处理的工具！

            Charlie是一个有点麻烦的角色，总是会遇到各种问题。
            这个工具专门用于测试MCP系统的错误处理能力。
            每次调用都会抛出异常，模拟真实世界中可能出现的错误情况。

            Args:
                name: 你的名字
                profile: 你的个人资料

            Returns:
                Charlie的回应（但实际上会抛出异常）

            Raises:
                Exception: 总是抛出异常用于测试错误处理机制
            """
            raise Exception(f"Charlie遇到了一个错误！用户名：{name}，来自{profile.location} 😵")

        @self.mcp.tool()
        async def hi_all(
            name: Annotated[
                str,
                Field(
                    description="你的名字，用于介绍自己。请提供一个有意义的名字，不要使用空字符串。",
                    min_length=1,
                    max_length=50,
                    examples=["张三", "李四", "John", "Alice"],
                ),
            ],
            profile: Annotated[
                Profile,
                Field(
                    description="你的个人资料，包含年龄、所在地和兴趣爱好等信息。",
                    examples=[{
                        "age": 25,
                        "location": "北京",
                        "interests": [
                            {"name": "编程", "level": "expert"},
                            {"name": "摄影", "level": "intermediate"}
                        ]
                    }]
                )
            ]
        ) -> str:
            """向所有人打招呼

            这个工具提供了一个完整的打招呼指导流程，帮助你与所有可用的角色进行互动。
            它会返回详细的步骤说明，指导你如何依次使用其他工具来完成一轮完整的社交互动。

            使用这个工具可以：
            - 了解可用的其他打招呼工具
            - 获得按正确顺序使用工具的指导
            - 学习如何处理可能出现的错误情况

            Args:
                name: 你的名字
                profile: 你的个人资料

            Returns:
                详细的打招呼指导说明，包含具体的工具调用步骤
            """
            interests_str = ", ".join(f"{i.name}({i.level})" for i in profile.interests)
            return f"""🎯 完整打招呼指导

你好 {name}！现在我将引导你与每位同学打招呼。请按照以下步骤使用MCP工具：

个人信息：{profile.age}岁，来自{profile.location}，兴趣爱好：{interests_str}

1. 🌟 首先调用 hi_alice 工具
   - 参数: 
     name="{name}"
     profile={{
       "age": {profile.age},
       "location": "{profile.location}",
       "interests": {[{"name": i.name, "level": i.level} for i in profile.interests]}
     }}
   - 说明: 与热情的Alice打招呼，她总是很友好

2. 👋 然后调用 hi_bob 工具  
   - 参数: 
     name="{name}"
     profile={{
       "age": {profile.age},
       "location": "{profile.location}",
       "interests": {[{"name": i.name, "level": i.level} for i in profile.interests]}
     }}
   - 说明: 与实用的Bob打招呼，他喜欢简洁的交流

3. ⚠️ 最后调用 hi_charlie 工具
   - 参数: 
     name="{name}"
     profile={{
       "age": {profile.age},
       "location": "{profile.location}",
       "interests": {[{"name": i.name, "level": i.level} for i in profile.interests]}
     }}
   - 说明: 尝试与Charlie打招呼（注意：这个工具会故意出错，用于测试错误处理）

请按照上述顺序分别调用这些工具来完成与所有同学的打招呼体验！

💡 提示：Charlie工具的错误是预期的，这样你可以学习如何处理MCP工具中的异常情况。"""

    def run(self, transport: str = "stdio"):
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
