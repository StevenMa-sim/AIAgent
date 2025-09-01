import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import tool

# =========================================================
# 1. 配置你的 API 密钥
# =========================================================
# 请直接将你的 API 密钥粘贴到这里，用作临时测试
api_key = "AIzaSyBHFqBKepCWVdx0I8ZdZgCuYzYMgXhrxyw"
if not api_key:
    raise ValueError("API 密钥未配置。")

os.environ["GOOGLE_API_KEY"] = api_key
genai.configure(api_key=api_key)

# =========================================================
# 2. 初始化大语言模型
# =========================================================
# 这是解决超时问题的关键行
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", transport="rest")

# =========================================================
# 3. 定义工具 (Tools)
# =========================================================
@tool("Search Tool")
def search_tool(query: str) -> str:
    """这是一个模拟的网络搜索工具，用于查询市场趋势和产品信息。"""
    print(f"\n>>>>>>> 正在使用搜索工具查询: {query}\n")
    if "德国市场热门健康产品" in query:
        return "最新的数据显示，德国市场对缓解压力、改善睡眠和提高效率的健康产品需求旺盛。其中，智能香薰机、头皮按摩器和便携式健身设备是热门品类。"
    return "未找到相关信息。"

# =========================================================
# 4. 定义 LangChain Runnable (Agent的替代)
# =========================================================
market_analyst_prompt = PromptTemplate.from_template(
    """你是一个市场分析师。根据以下搜索结果，分析并推荐一个可以包装成“小黑品”的品类：
    搜索结果：{search_results}
    分析要求：找出其隐藏的卖点和用户痛点，并提出一个独特的“愿景”。
    """
)
def run_search_tool(query):
    return search_tool.invoke(query)
market_analyst_chain = (
    {"search_results": RunnableLambda(run_search_tool)}
    | market_analyst_prompt
    | llm
    | StrOutputParser()
)
content_writer_prompt = PromptTemplate.from_template(
    """你是一个创意文案专家。根据以下市场分析报告，为产品撰写一篇符合“小黑品”策略的落地页文案。
    分析报告：{analysis_report}
    文案要求：文案必须包括：标题、痛点描述、解决方案、核心卖点和号召性用语。
    """
)
content_writer_chain = (
    {"analysis_report": RunnablePassthrough()}
    | content_writer_prompt
    | llm
    | StrOutputParser()
)

# =========================================================
# 5. 组合 Runnable
# =========================================================
full_workflow = market_analyst_chain | content_writer_chain

# =========================================================
# 6. 启动工作流
# =========================================================
inputs = "分析德国市场的热门健康产品。"
try:
    result = full_workflow.invoke(inputs)
    print("\n\n################################################")
    print("AI 落地页文案已生成：")
    print("################################################")
    print(result)
except Exception as e:
    print(f"执行时发生错误: {e}")