import os
import sys
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 确保你的 Google API Key 正确配置
os.environ["GOOGLE_API_KEY"] = "AIzaSyBHFqBKepCWVdx0I8ZdZgCuYzYMgXhrxyw"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", transport="rest")
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"), transport="rest")

# 从命令行参数中读取文件路径
if len(sys.argv) < 2:
    print("错误：请提供分析报告的文件路径作为参数。")
    sys.exit(1)
report_file_path = sys.argv[1]

# 读取分析报告
with open(report_file_path, "r", encoding="utf-8") as f:
    analysis_report = f.read()

# Prompt for Copywriting Agent
prompt = PromptTemplate.from_template(
    """你是一位顶级的营销专家。根据以下市场分析报告，为产品撰写一篇符合“小黑品”策略的落地页文案。
    分析报告：{analysis_report}
    文案必须包含：标题、痛点描述、解决方案、核心卖点和号召性用语。
    """
)

# Combine and run
chain = prompt | llm | StrOutputParser()
try:
    landing_page_copy = chain.invoke({"analysis_report": analysis_report})
    print("\n\n################################################")
    print("落地页文案已生成：")
    print("################################################")
    print(landing_page_copy)
except Exception as e:
    print(f"执行时发生错误: {e}")