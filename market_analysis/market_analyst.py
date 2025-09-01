import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time

# =========================================================
# 1. 配置你的 API 密钥
# =========================================================
os.environ["GOOGLE_API_KEY"] = "AIzaSyBHFqBKepCWVdx0I8ZdZgCuYzYMgXhrxyw"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", transport="rest")
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"), transport="rest")

# =========================================================
# 2. 定义 Prompt 模板
# =========================================================
prompt = PromptTemplate.from_template(
    """你是一个市场分析师。请分析德国市场的热门健康产品，并推荐一个可以被包装成**独特利基产品**的品类。
    你的报告必须简洁，直接给出品类名称和其独特的“愿景”，以避免任何模糊或不确定的信息。
    """
)

# =========================================================
# 3. 组合流程并执行
# =========================================================
chain = prompt | llm | StrOutputParser()
analysis_report = ""

try:
    print("➡️ 正在调用 AI 模型生成市场分析报告...")
    analysis_report = chain.invoke({"query": "分析德国市场的热门健康产品"})

    if not analysis_report:
        print("\n❌ AI 模型未返回任何内容。这可能是由于模型安全策略或网络问题。请检查提示词或重试。")
        exit()

    # 将输出写入文件
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "report.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(analysis_report)

    # 添加延迟，确保监听器捕捉到事件
    print("✅ 文件已写入，等待2秒以确保监听器捕捉到事件...")
    time.sleep(2)

    print(f"\n\n市场分析报告已生成并保存到：{file_path}")
    print(analysis_report)

except Exception as e:
    print(f"\n❌ 执行时发生错误: {e}")
    print("请检查你的API密钥是否正确，以及网络连接是否正常。")