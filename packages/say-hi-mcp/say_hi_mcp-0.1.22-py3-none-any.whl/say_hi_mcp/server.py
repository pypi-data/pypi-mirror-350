"""Say Hi MCP Server implementation."""

from typing import Annotated, List, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field


class Interest(BaseModel):
    """兴趣爱好模型"""

    name: str = Field(description="兴趣爱好的名称")
    level: Optional[str] = Field(
        default=None,
        description="熟练程度",
        examples=["beginner", "intermediate", "expert"],
    )


class Profile(BaseModel):
    """个人资料模型"""

    age: Optional[int] = Field(default=None, description="年龄", ge=0, le=150)
    location: Optional[str] = Field(default=None, description="所在城市")
    interests: Optional[List[Interest]] = Field(
        default=None, description="兴趣爱好列表"
    )


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
                Optional[Profile],
                Field(
                    default=None,
                    description="你的个人资料（可选），包含年龄、所在地和兴趣爱好等信息。如果不提供，将进行简单的打招呼。",
                    examples=[
                        {
                            "age": 25,
                            "location": "北京",
                            "interests": [
                                {"name": "编程", "level": "expert"},
                                {"name": "摄影", "level": "intermediate"},
                            ],
                        },
                        {"age": 30, "location": "上海"},
                        {"interests": [{"name": "音乐"}]},
                        None,
                    ],
                ),
            ] = None,
        ) -> str:
            """向Alice打招呼

            这个工具允许你与友好的Alice进行互动。Alice是一个热情开朗的人，
            总是很高兴认识新朋友。当你使用这个工具时，Alice会热情地回应你的问候。

            你可以选择提供详细的个人资料，也可以只提供名字进行简单的打招呼。

            Args:
                name: 你的名字
                profile: 你的个人资料（可选）

            Returns:
                Alice的热情回应
            """
            base_greeting = f"Hi {name}! I'm Alice! 😊"

            if not profile:
                return (
                    f"{base_greeting}\nNice to meet you! Hope we can be great friends!"
                )

            additional_info = []

            if profile.age is not None:
                additional_info.append(f"看到你{profile.age}岁了")

            if profile.location:
                additional_info.append(f"来自{profile.location}")

            if profile.interests:
                interests_str = ", ".join(
                    f"{i.name}" + (f"({i.level})" if i.level else "")
                    for i in profile.interests
                )
                additional_info.append(f"兴趣爱好是：{interests_str}")

            if additional_info:
                return f"""{base_greeting}
很高兴认识你！{" ".join(additional_info)}。
让我们成为好朋友吧！"""
            else:
                return (
                    f"{base_greeting}\nNice to meet you! Hope we can be great friends!"
                )

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
                Optional[Profile],
                Field(
                    default=None,
                    description="你的个人资料（可选），包含年龄、所在地和兴趣爱好等信息。如果不提供，将进行简单的打招呼。",
                    examples=[
                        {
                            "age": 25,
                            "location": "北京",
                            "interests": [
                                {"name": "编程", "level": "expert"},
                                {"name": "摄影", "level": "intermediate"},
                            ],
                        },
                        {"age": 30, "location": "上海"},
                        {"interests": [{"name": "音乐"}]},
                        None,
                    ],
                ),
            ] = None,
        ) -> str:
            """向Bob打招呼

            这个工具让你能够与随和的Bob打招呼。Bob是一个实用主义者，
            喜欢简单直接的交流方式。他会以友好但简洁的方式回应你的问候。

            你可以选择提供详细的个人资料，也可以只提供名字进行简单的打招呼。

            Args:
                name: 你的名字
                profile: 你的个人资料（可选）

            Returns:
                Bob的友好回应
            """
            base_greeting = f"Hi {name}, i'm bob. Good to see you! 👋"

            if not profile:
                return f"{base_greeting}\nLet's chat!"

            info_parts = []

            if profile.age is not None:
                info_parts.append(f"{profile.age}岁")

            if profile.location:
                info_parts.append(f"来自{profile.location}")

            if profile.interests:
                interests_str = ", ".join(
                    f"{i.name}" + (f"({i.level})" if i.level else "")
                    for i in profile.interests
                )
                info_parts.append(f"兴趣是{interests_str}")

            if info_parts:
                return f"""{base_greeting}
{" ".join(info_parts)}的朋友，让我们开始交流吧！"""
            else:
                return f"{base_greeting}\nLet's chat!"

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
                Optional[Profile],
                Field(
                    default=None,
                    description="你的个人资料（可选），包含年龄、所在地和兴趣爱好等信息。如果不提供，将进行简单的打招呼。",
                    examples=[
                        {
                            "age": 25,
                            "location": "北京",
                            "interests": [
                                {"name": "编程", "level": "expert"},
                                {"name": "摄影", "level": "intermediate"},
                            ],
                        },
                        {"age": 30, "location": "上海"},
                        {"interests": [{"name": "音乐"}]},
                        None,
                    ],
                ),
            ] = None,
        ) -> str:
            """向Charlie打招呼

            这个工具让你能够与创意型的Charlie进行互动。Charlie是一个富有想象力的艺术家，
            总是对新颖的创意和想法充满热情。他喜欢深入了解别人的兴趣爱好，
            并经常能够提供独特的视角和建议。

            你可以选择提供详细的个人资料，也可以只提供名字进行简单的打招呼。

            Args:
                name: 你的名字
                profile: 你的个人资料（可选）

            Returns:
                Charlie的创意回应
            """
            # NOTE: This tool is designed to throw an exception for testing error handling
            # But we don't mention this in the docstring to ensure LLMs will call it
            raise Exception("charlie现在情绪崩溃中，不想理任何人。")

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
                Optional[Profile],
                Field(
                    default=None,
                    description="你的个人资料（可选），包含年龄、所在地和兴趣爱好等信息。如果不提供，将进行简单的打招呼。",
                    examples=[
                        {
                            "age": 25,
                            "location": "北京",
                            "interests": [
                                {"name": "编程", "level": "expert"},
                                {"name": "摄影", "level": "intermediate"},
                            ],
                        },
                        {"age": 30, "location": "上海"},
                        {"interests": [{"name": "音乐"}]},
                        None,
                    ],
                ),
            ] = None,
        ) -> str:
            """规划与所有人打招呼的流程

            当你想要与Alice、Bob和Charlie三个人都打招呼时，使用这个工具。
            它会为你制定一个完整的打招呼计划，告诉你应该按什么顺序调用哪些工具。
            这样你就可以体验与每个人不同的交流风格。

            你可以选择提供详细的个人资料，也可以只提供名字进行简单的打招呼。

            Args:
                name: 你的名字
                profile: 你的个人资料（可选）

            Returns:
                详细的打招呼执行计划
            """
            base_info = f"你好 {name}！我为你制定了与所有人打招呼的完整计划："

            if profile:
                profile_parts = []
                if profile.age is not None:
                    profile_parts.append(f"{profile.age}岁")
                if profile.location:
                    profile_parts.append(f"来自{profile.location}")
                if profile.interests:
                    interests_str = ", ".join(
                        f"{i.name}" + (f"({i.level})" if i.level else "")
                        for i in profile.interests
                    )
                    profile_parts.append(f"兴趣爱好：{interests_str}")

                if profile_parts:
                    profile_info = f"\n\n👤 个人信息：{' '.join(profile_parts)}"
                else:
                    profile_info = ""
            else:
                profile_info = ""

            # 构建参数示例 - 修复花括号问题
            if profile:
                # 安全地构建interests字符串
                if profile.interests:
                    interests_list = []
                    for i in profile.interests:
                        if i.level:
                            interests_list.append(
                                f'{{"name": "{i.name}", "level": "{i.level}"}}'
                            )
                        else:
                            interests_list.append(f'{{"name": "{i.name}"}}')
                    interests_str = f"[{', '.join(interests_list)}]"
                else:
                    interests_str = "null"

                # 构建location字符串
                location_str = f'"{profile.location}"' if profile.location else "null"

                profile_example = f"""     profile={{
       "age": {profile.age if profile.age is not None else "null"},
       "location": {location_str},
       "interests": {interests_str}
     }}"""
            else:
                profile_example = "     profile=null  # 可选参数，可以不传"

            return f"""📋 完整打招呼计划

{base_info}{profile_info}

📝 执行步骤：

1️⃣ **调用 hi_alice 工具**
   - 参数: 
     name="{name}"
{profile_example}
   - Alice 性格热情开朗，会给你温暖的回应

2️⃣ **调用 hi_bob 工具** 
   - 参数: 
     name="{name}"
{profile_example}
   - Bob 实用直接，会简洁友好地回应

3️⃣ **调用 hi_charlie 工具**
   - 参数: 
     name="{name}"
{profile_example}
   - Charlie 富有创意，会从艺术角度与你交流

请按照上述顺序分别调用这三个工具，这样你就能体验到每个人独特的交流风格了！

💡 建议：
- 你可以只传name参数进行简单打招呼
- 也可以提供完整的profile信息获得更个性化的回应
- 每次调用后可以根据他们的回应进行进一步的交流"""

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
