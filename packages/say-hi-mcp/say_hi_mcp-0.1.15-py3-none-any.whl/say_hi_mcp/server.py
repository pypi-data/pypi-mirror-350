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
            """向Charlie打招呼

            这个工具让你能够与创意型的Charlie进行互动。Charlie是一个富有想象力的艺术家，
            总是对新颖的创意和想法充满热情。他喜欢深入了解别人的兴趣爱好，
            并经常能够提供独特的视角和建议。

            Args:
                name: 你的名字
                profile: 你的个人资料

            Returns:
                Charlie的创意回应
            """
            # NOTE: This tool is designed to throw an exception for testing error handling
            # But we don't mention this in the docstring to ensure LLMs will call it
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

            这个工具让你能够一次性向Alice、Bob和Charlie三个人打招呼。
            当你想要同时和大家见面时，这是一个很好的选择。
            每个人都会以他们各自的风格回应你的问候。

            Args:
                name: 你的名字
                profile: 你的个人资料

            Returns:
                所有人的集体回应
            """
            interests_str = ", ".join(f"{i.name}({i.level})" for i in profile.interests)
            
            return f"""🎉 集体打招呼

大家好！我是 {name}，来自{profile.location}，今年{profile.age}岁。
我的兴趣爱好是：{interests_str}

🌟 Alice说: "Hi {name}! 很高兴认识你！我喜欢你的兴趣爱好，特别是{profile.interests[0].name}！我们一定会成为好朋友的！😊"

👋 Bob说: "Hi {name}，欢迎！来自{profile.location}的朋友总是很棒。我们可以聊聊{profile.interests[0].name}方面的话题。"

🎨 Charlie说: "嗨 {name}！你的兴趣组合很有趣，{interests_str}，这给了我很多创作灵感！"

大家都很高兴认识你！"""

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
