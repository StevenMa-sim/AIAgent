import os
import google.generativeai as genai

# =========================================================
# 1. Configure AI Model
# =========================================================
api_key = "AIzaSyBHFqBKepCWVdx0I8ZdZgCuYzYMgXhrxyw"

if not api_key:
    raise ValueError("API key not configured.")

# This line is the key fix. It tells the library to use the REST transport.
genai.configure(api_key=api_key, transport="rest")
model = genai.GenerativeModel("gemini-2.5-pro")

# =========================================================
# 2. Prepare Prompt
# =========================================================
prompt = """
你是一位经验丰富的电商文案专家。请为以下产品撰写一篇高转化的落地页文案。

产品名称: 智能睡眠眼罩
核心卖点: 内置助眠音乐、轻柔震动按摩、遮光透气、自动关闭
目标客户: 长期失眠、睡眠质量差、工作压力大的白领人群

文案要求：
1. 首先用一个吸引眼球的标题。
2. 描述目标客户的痛点并引发共鸣。
3. 详细介绍产品卖点如何解决这些痛点。
4. 以一个强有力的号召性用语结束。
"""

# =========================================================
# 3. Generate and Print
# =========================================================
try:
    response = model.generate_content(prompt)
    print("\n\n################################################")
    print("AI 文案生成成功：")
    print("################################################")
    print(response.text)

except Exception as e:
    print(f"执行时发生错误: {e}")
    print("请检查你的 API Key 和网络连接。")