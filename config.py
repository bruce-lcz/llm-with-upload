import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# Azure OpenAI 設定
AZURE_OPENAI_API_KEY = "your-azure-openai-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT_NAME = "your-deployment-name"
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"

# Streamlit 配置
STREAMLIT_TITLE = "AI 聊天助手"
STREAMLIT_DESCRIPTION = "與AI助手進行對話，獲得智能回答" 