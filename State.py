from langgraph.graph import StateGraph, END

# ---------- 定义 State ----------
class AppState(TypedDict):
    user_role: str
    preferences: dict
    emotion: dict
    diet_goals: dict
    menu_candidates: list
    shopping_list: list
    coaching_scripts: list
    conversation_history: list

# ---------- 定义节点 ----------
def user_input_node(state: AppState) -> AppState:
    # 接收父母/儿童输入
    return state

def info_gather_node(state: AppState) -> AppState:
    # 检查信息缺失 → chatbot追问
    return state

def task_classifier_node(state: AppState) -> str:
    # 输出 "emotion" | "menu" | "shopping" | "coaching"
    return "menu"

def emotion_analysis_node(state: AppState) -> AppState:
    # 调用情绪模型 → 更新 state["emotion"]
    return state

def menu_planner_node(state: AppState) -> AppState:
    # 调用 RAG + 食谱库 → 生成 state["menu_candidates"]
    return state

def coles_api_node(state: AppState) -> AppState:
    # 调用超市API → state["shopping_list"]
    return state

def parent_coaching_node(state: AppState) -> AppState:
    # 生成餐桌话术脚本
    return state

def safety_gateway_node(state: AppState) -> AppState:
    # 检测风险 → 返回警告 or 继续
    return state

# ---------- 构建 Graph ----------
graph = StateGraph(AppState)

graph.add_node("UserInput", user_input_node)
graph.add_node("InfoGather", info_gather_node)
graph.add_node("TaskClassifier", task_classifier_node)
graph.add_node("EmotionAnalysis", emotion_analysis_node)
graph.add_node("MenuPlanner", menu_planner_node)
graph.add_node("ColesAPI", coles_api_node)
graph.add_node("ParentCoaching", parent_coaching_node)
graph.add_node("SafetyGateway", safety_gateway_node)

# ---------- 边的定义 ----------
graph.add_edge("UserInput", "InfoGather")
graph.add_edge("InfoGather", "TaskClassifier")

graph.add_conditional_edges(
    "TaskClassifier",
    lambda state: state["task_type"],
    {
        "emotion": "EmotionAnalysis",
        "menu": "MenuPlanner",
        "shopping": "ColesAPI",
        "coaching": "ParentCoaching",
    }
)

# 风险检测放在末尾
graph.add_edge("MenuPlanner", "SafetyGateway")
graph.add_edge("ColesAPI", "SafetyGateway")
graph.add_edge("ParentCoaching", "SafetyGateway")
graph.add_edge("EmotionAnalysis", END)
graph.add_edge("SafetyGateway", END)

app = graph.compile()
