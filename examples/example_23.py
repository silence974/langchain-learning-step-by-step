class HierarchicalMemory:
    """
    1. 静态事实层：用户画像、偏好、固定信息
    2. 提取事实层：从对话中提取的关键信息
    3. 动态对话层：原始历史对话
    """
    def __init__(self):
        self.static_facts = StaticMemoryLayer()
        self.extracted_facts = ExtractedMemoryLayer()
        self.conversation_history = DynamicMemoryLayer()
        
    def get_context(self, user_id, query):
        static = self.static_facts.get(user_id)
        extracted = self.extracted_facts.search(query)
        dynamic = self.conversation_history.get_recent(
            user_id,
            max_tokens=1000,
            max_messages=10,
            time_window="7d",
        )
        return self.merge_memories(static, extracted, dynamic)
    

@before_agent(can_jump_to=["end"])
def inject_hierarchical_memory(state: AgentState, runtime: Runtime):
    user_id = state.user_id
    last_message = state.messages[-1].content
    
    context = hierarchical_memory.get_context(user_id, last_message)
    
    return {
        "messages": [
            SystemMessage(content=f"""
            可用记忆结构：
            1. 用户画像： {context['static']}
            2. 提取事实： {context['extracted']}
            3. 动态对话： {context['dynamic']}
            """),
            *state["messages"]
        ]
    }