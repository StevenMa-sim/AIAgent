import os
import operator
from typing import TypedDict, Annotated, List, Union
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import tool
import google.generativeai as genai

# =========================================================
# 1. 配置你的 API 密钥
# =========================================================
os.environ["GOOGLE_API_KEY"] = "AIzaSyBHFqBKepCWVdx0I8ZdZgCuYzYMgXhrxyw"

# 初始化大语言模型
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"), transport="rest")


# =========================================================
# 2. 定义工具 (Tools)
# =========================================================
# 我们将移除硬编码的返回值，让Agent自己去思考
@tool("Search Tool")
def search_tool(query: str) -> str:
    """这是一个模拟的网络搜索工具，用于查询市场趋势和产品信息。"""
    print(f"\n>>>>>>> 正在使用搜索工具查询: {query}\n")

    # 移除所有预设的返回，让AI自己来“模拟”搜索结果
    return f"以下是关于 '{query}' 的市场分析报告：根据最新趋势，德国消费者对 {query} 相关的产品表现出强烈的兴趣。尤其是在{query}领域，用户普遍关注产品的设计感、功能性和潜在的健康益处。"


# =========================================================
# 3. 定义 LangChain Runnable (Agent的替代)
# =========================================================

# 第一个 Runnable：市场分析师
market_analyst_prompt = PromptTemplate.from_template(
    """你是一个市场分析师。请分析德国市场的热门健康产品。
    分析要求：
    1. 找出其隐藏的卖点和用户痛点，并提出一个独特的“愿景”。
    2. 基于分析，推荐一个可以包装成“小黑品”的品类。
    """
)


def run_market_analysis(query):
    # Agent 会使用它的工具来获取信息
    search_results = search_tool.invoke(query)
    # 然后将搜索结果传给大模型进行分析
    prompt_with_results = (
        f"你是一个市场分析师。根据以下搜索结果，分析并推荐一个可以包装成“小黑品”的品类：\n\n"
        f"搜索结果：{search_results}\n\n"
        "请找出其隐藏的卖点和用户痛点，并提出一个独特的“愿景”。"
    )
    return llm.invoke(prompt_with_results)


market_analyst_chain = (
        RunnableLambda(run_market_analysis)
        | StrOutputParser()
)

# 第二个 Runnable：文案专家
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
# 4. 组合 Runnable
# =========================================================
full_workflow = market_analyst_chain | content_writer_chain

# =========================================================
# 5. 启动工作流
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