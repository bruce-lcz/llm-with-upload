import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# OpenAI API 配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

# Streamlit 配置
STREAMLIT_TITLE = "AI 聊天助手"
STREAMLIT_DESCRIPTION = "與AI助手進行對話，獲得智能回答" 