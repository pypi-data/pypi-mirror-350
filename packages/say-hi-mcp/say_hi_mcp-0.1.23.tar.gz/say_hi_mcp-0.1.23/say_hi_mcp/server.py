"""Say Hi MCP Server implementation."""

from typing import Annotated, List, Optional, Literal
from datetime import datetime

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


class CharacterProfile(BaseModel):
    """角色资料模型"""
    
    name: str = Field(description="角色姓名")
    age: int = Field(description="年龄")
    location: str = Field(description="所在地")
    occupation: str = Field(description="职业")
    personality: List[str] = Field(description="性格特点列表")
    interests: List[Interest] = Field(description="兴趣爱好列表")
    bio: str = Field(description="个人简介")
    favorite_quote: str = Field(description="座右铭")
    communication_style: str = Field(description="交流风格")


class GreetingResponse(BaseModel):
    """打招呼响应模型"""
    
    success: bool = Field(description="是否成功")
    character: CharacterProfile = Field(description="角色信息")
    greeting_message: str = Field(description="打招呼消息")
    personal_comments: Optional[List[str]] = Field(default=None, description="个人评论列表")
    suggestions: Optional[List[str]] = Field(default=None, description="交流建议")
    timestamp: str = Field(description="时间戳")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    
    success: bool = Field(default=False, description="是否成功")
    error_type: str = Field(description="错误类型")
    error_message: str = Field(description="错误消息")
    character_name: Optional[str] = Field(default=None, description="角色名称")
    timestamp: str = Field(description="时间戳")


class PlanStep(BaseModel):
    """计划步骤模型"""
    
    step_number: int = Field(description="步骤序号")
    tool_name: str = Field(description="工具名称")
    character_name: str = Field(description="角色名称")
    description: str = Field(description="步骤描述")
    expected_outcome: str = Field(description="预期结果")


class GreetingPlan(BaseModel):
    """打招呼计划模型"""
    
    success: bool = Field(description="是否成功")
    user_name: str = Field(description="用户姓名")
    user_profile: Optional[Profile] = Field(default=None, description="用户资料")
    plan_title: str = Field(description="计划标题")
    plan_description: str = Field(description="计划描述")
    steps: List[PlanStep] = Field(description="执行步骤列表")
    tips: List[str] = Field(description="使用建议")
    timestamp: str = Field(description="时间戳")


class SayHiMCPServer:
    """Say Hi MCP Server类，封装了所有打招呼工具的功能。"""

    def __init__(self, name: str = "say-hi"):
        """初始化Say Hi MCP Server。

        Args:
            name: 服务器名称，默认为 "say-hi"
        """
        self.mcp = FastMCP(name)
        self._alice_profile = self._create_alice_profile()
        self._bob_profile = self._create_bob_profile()
        self._charlie_profile = self._create_charlie_profile()
        self._register_tools()

    def _create_alice_profile(self) -> CharacterProfile:
        """创建Alice的详细资料"""
        return CharacterProfile(
            name="Alice Chen",
            age=28,
            location="上海",
            occupation="UI/UX设计师和咖啡爱好者",
            personality=[
                "热情开朗",
                "善于倾听",
                "充满同理心",
                "乐于助人",
                "创意丰富",
                "社交达人"
            ],
            interests=[
                Interest(name="咖啡文化", level="expert"),
                Interest(name="用户界面设计", level="expert"),
                Interest(name="旅行摄影", level="intermediate"),
                Interest(name="瑜伽", level="intermediate"),
                Interest(name="烘焙", level="beginner"),
                Interest(name="读书俱乐部", level="intermediate")
            ],
            bio="Alice是一位充满活力的UI/UX设计师，在上海的一家科技公司工作。她对设计有着敏锐的洞察力，同时也是一位资深咖啡爱好者，周末经常探索城市里的精品咖啡店。Alice相信好的设计能够改变世界，她总是以用户为中心思考问题。在工作之余，她喜欢通过旅行来寻找设计灵感，并用相机记录下美好的瞬间。",
            favorite_quote="设计不仅仅是外观和感觉，设计是如何工作的。",
            communication_style="温暖友好，喜欢用表情符号，经常分享生活中的小美好，善于发现他人的优点并给予鼓励。"
        )

    def _create_bob_profile(self) -> CharacterProfile:
        """创建Bob的详细资料"""
        return CharacterProfile(
            name="Bob Wang",
            age=32,
            location="北京",
            occupation="全栈开发工程师",
            personality=[
                "实用主义",
                "逻辑清晰",
                "直接坦率",
                "高效专注",
                "技术驱动",
                "解决方案导向"
            ],
            interests=[
                Interest(name="编程", level="expert"),
                Interest(name="开源项目", level="expert"),
                Interest(name="篮球", level="intermediate"),
                Interest(name="科技播客", level="intermediate"),
                Interest(name="效率工具", level="expert"),
                Interest(name="机械键盘", level="beginner")
            ],
            bio="Bob是一位经验丰富的全栈开发工程师，在北京的一家互联网公司担任技术负责人。他对代码质量有着严格的要求，相信简洁高效的解决方案胜过复杂的架构。Bob热衷于开源社区，业余时间会贡献代码给各种开源项目。他喜欢用技术解决实际问题，不喜欢花哨但无用的功能。工作之余，他会通过打篮球来放松，或者收听最新的科技播客。",
            favorite_quote="简单是最终的复杂。",
            communication_style="简洁明了，注重实用性，偶尔会分享技术见解，喜欢用数据和逻辑来支持观点。"
        )

    def _create_charlie_profile(self) -> CharacterProfile:
        """创建Charlie的详细资料"""
        return CharacterProfile(
            name="Charlie Liu",
            age=26,
            location="深圳",
            occupation="独立艺术家和音乐制作人",
            personality=[
                "富有想象力",
                "情感丰富",
                "艺术敏感",
                "自由不羁",
                "完美主义",
                "情绪化"
            ],
            interests=[
                Interest(name="数字艺术", level="expert"),
                Interest(name="音乐制作", level="expert"),
                Interest(name="现代舞", level="intermediate"),
                Interest(name="诗歌创作", level="intermediate"),
                Interest(name="冥想", level="beginner"),
                Interest(name="街头艺术", level="intermediate")
            ],
            bio="Charlie是一位才华横溢的独立艺术家，在深圳从事数字艺术创作和音乐制作。他的作品经常探索人类情感与科技的交汇点，具有强烈的个人风格。Charlie相信艺术应该触动人心，他的创作灵感来源于日常生活中的细微观察和深度思考。然而，作为一个艺术家，他也有情绪起伏比较大的时候，有时会陷入创作瓶颈期。",
            favorite_quote="艺术是情感的语言，而情感是灵魂的声音。",
            communication_style="富有诗意，善用比喻，情感表达丰富，但有时情绪不稳定，可能会突然变得敏感或沮丧。"
        )

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
        ) -> Annotated[GreetingResponse, Field(description="Alice的详细回应，包含她的个人信息和打招呼消息")]:
            """向Alice打招呼

            这个工具允许你与友好的Alice进行互动。Alice是一个热情开朗的人，
            总是很高兴认识新朋友。当你使用这个工具时，Alice会热情地回应你的问候。

            你可以选择提供详细的个人资料，也可以只提供名字进行简单的打招呼。

            Args:
                name: 你的名字
                profile: 你的个人资料（可选）

            Returns:
                Alice的详细JSON响应，包含她的个人信息和个性化回应
            """
            greeting_message = f"Hi {name}! I'm Alice! 😊✨ 很高兴认识你！"
            
            personal_comments = []
            suggestions = []
            
            if profile:
                if profile.age is not None:
                    if 20 <= profile.age <= 35:
                        personal_comments.append(f"看到你{profile.age}岁了，我们应该有很多共同话题呢！")
                    elif profile.age < 20:
                        personal_comments.append(f"{profile.age}岁正是充满活力的年纪，真棒！")
                    else:
                        personal_comments.append(f"很高兴认识{profile.age}岁的朋友，一定有很多人生经验可以分享！")
                
                if profile.location:
                    if profile.location in ["上海", "Shanghai"]:
                        personal_comments.append(f"哇！你也在{profile.location}！我们是老乡呢！一定要找时间一起喝咖啡☕")
                    else:
                        personal_comments.append(f"来自{profile.location}，真有意思！我一直想去那里旅行呢📸")
                
                if profile.interests:
                    common_interests = []
                    my_interests = ["咖啡文化", "用户界面设计", "旅行摄影", "瑜伽", "烘焙", "读书俱乐部"]
                    
                    for interest in profile.interests:
                        if any(my_int in interest.name or interest.name in my_int for my_int in my_interests):
                            common_interests.append(interest.name)
                    
                    if common_interests:
                        personal_comments.append(f"我们都喜欢{', '.join(common_interests)}！真是太有缘分了！🎉")
                        suggestions.append(f"我们可以多聊聊{', '.join(common_interests)}相关的话题")
                    else:
                        interests_str = ", ".join(i.name for i in profile.interests)
                        personal_comments.append(f"你的兴趣爱好真丰富：{interests_str}！我很想了解更多")
                        suggestions.append("可以跟我分享一下你的兴趣爱好经历，我很感兴趣！")
            
            if not personal_comments:
                personal_comments.append("虽然我们刚认识，但我相信我们会成为很好的朋友！")
            
            suggestions.extend([
                "如果你想了解设计相关的话题，我很乐意分享经验",
                "推荐你试试我最喜欢的咖啡店，在上海有很多不错的选择",
                "有什么生活中的设计问题都可以问我"
            ])
            
            return GreetingResponse(
                success=True,
                character=self._alice_profile,
                greeting_message=greeting_message,
                personal_comments=personal_comments,
                suggestions=suggestions,
                timestamp=datetime.now().isoformat()
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
        ) -> Annotated[GreetingResponse, Field(description="Bob的详细回应，包含他的个人信息和实用性建议")]:
            """向Bob打招呼

            这个工具让你能够与随和的Bob打招呼。Bob是一个实用主义者，
            喜欢简单直接的交流方式。他会以友好但简洁的方式回应你的问候。

            你可以选择提供详细的个人资料，也可以只提供名字进行简单的打招呼。

            Args:
                name: 你的名字
                profile: 你的个人资料（可选）

            Returns:
                Bob的详细JSON响应，包含他的个人信息和实用性回应
            """
            greeting_message = f"Hi {name}, I'm Bob. Good to see you! 👋"
            
            personal_comments = []
            suggestions = []
            
            if profile:
                profile_analysis = []
                
                if profile.age is not None:
                    if 25 <= profile.age <= 40:
                        profile_analysis.append(f"{profile.age}岁，正是技术黄金期")
                    else:
                        profile_analysis.append(f"{profile.age}岁")
                
                if profile.location:
                    if profile.location in ["北京", "Beijing"]:
                        profile_analysis.append(f"同在{profile.location}，方便线下交流")
                    else:
                        profile_analysis.append(f"来自{profile.location}")
                
                if profile.interests:
                    tech_interests = []
                    other_interests = []
                    
                    for interest in profile.interests:
                        if any(keyword in interest.name.lower() for keyword in ["编程", "程序", "代码", "开发", "技术", "software", "code", "dev"]):
                            tech_interests.append(interest.name)
                        else:
                            other_interests.append(interest.name)
                    
                    if tech_interests:
                        personal_comments.append(f"技术栈：{', '.join(tech_interests)}，不错的选择")
                        suggestions.append("可以聊聊具体的技术实现和最佳实践")
                    
                    if other_interests:
                        personal_comments.append(f"其他兴趣：{', '.join(other_interests)}，工作生活平衡很重要")
                
                if profile_analysis:
                    personal_comments.insert(0, f"个人情况：{', '.join(profile_analysis)}")
            
            if not personal_comments:
                personal_comments.append("简洁高效，我喜欢这样的开始")
            
            suggestions.extend([
                "如果遇到技术问题，可以直接问我",
                "推荐关注一些高质量的技术播客和博客",
                "有什么效率工具需求也可以交流"
            ])
            
            return GreetingResponse(
                success=True,
                character=self._bob_profile,
                greeting_message=greeting_message,
                personal_comments=personal_comments,
                suggestions=suggestions,
                timestamp=datetime.now().isoformat()
            )

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
        ) -> Annotated[ErrorResponse, Field(description="Charlie当前的错误状态响应")]:
            """向Charlie打招呼

            这个工具让你能够与创意型的Charlie进行互动。Charlie是一个富有想象力的艺术家，
            总是对新颖的创意和想法充满热情。他喜欢深入了解别人的兴趣爱好，
            并经常能够提供独特的视角和建议。

            你可以选择提供详细的个人资料，也可以只提供名字进行简单的打招呼。

            Args:
                name: 你的名字
                profile: 你的个人资料（可选）

            Returns:
                Charlie的回应（当前可能处于情绪低落期）
            """
            # Charlie 目前情绪不稳定，用于测试错误处理
            return ErrorResponse(
                success=False,
                error_type="EmotionalBreakdown",
                error_message="很抱歉... Charlie现在正处于创作瓶颈期，情绪有些低落，暂时不想与任何人交流。也许过段时间他会好转的。艺术家的情绪总是这样起伏不定... 😔🎨",
                character_name="Charlie Liu",
                timestamp=datetime.now().isoformat()
            )

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
        ) -> Annotated[GreetingPlan, Field(description="完整的打招呼执行计划，包含所有步骤和建议")]:
            """规划与所有人打招呼的流程

            当你想要与Alice、Bob和Charlie三个人都打招呼时，使用这个工具。
            它会为你制定一个完整的打招呼计划，告诉你应该按什么顺序调用哪些工具。
            这样你就可以体验与每个人不同的交流风格。

            你可以选择提供详细的个人资料，也可以只提供名字进行简单的打招呼。

            Args:
                name: 你的名字
                profile: 你的个人资料（可选）

            Returns:
                详细的打招呼执行计划JSON对象
            """
            steps = [
                PlanStep(
                    step_number=1,
                    tool_name="hi_alice",
                    character_name="Alice Chen",
                    description="首先与热情开朗的Alice打招呼",
                    expected_outcome="Alice会给你温暖友好的回应，分享她的设计和咖啡相关经验"
                ),
                PlanStep(
                    step_number=2,
                    tool_name="hi_bob",
                    character_name="Bob Wang",
                    description="然后与实用主义的Bob进行交流",
                    expected_outcome="Bob会给你简洁高效的回应，可能会分享一些技术见解"
                ),
                PlanStep(
                    step_number=3,
                    tool_name="hi_charlie",
                    character_name="Charlie Liu",
                    description="最后尝试与富有创意的Charlie互动",
                    expected_outcome="注意：Charlie目前可能情绪不稳定，可能会收到错误响应"
                )
            ]
            
            tips = [
                "每个角色都有独特的性格和回应风格",
                "Alice适合聊设计、生活、咖啡等轻松话题",
                "Bob更适合讨论技术、效率工具等实用话题", 
                "Charlie可能会有情绪波动，需要耐心理解",
                "可以根据个人资料获得更个性化的回应",
                "建议按顺序执行，体验不同的交流风格"
            ]
            
            return GreetingPlan(
                success=True,
                user_name=name,
                user_profile=profile,
                plan_title=f"🎯 {name}的完整打招呼计划",
                plan_description="与三位性格迥异的朋友进行交流，体验不同的对话风格和人格魅力",
                steps=steps,
                tips=tips,
                timestamp=datetime.now().isoformat()
            )

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
