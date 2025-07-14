import streamlit as st
import openai
from config import *
from file_processor import FileProcessor
import base64


# 設置頁面配置
st.set_page_config(
    page_title=STREAMLIT_TITLE,
    page_icon="🤖",
    layout="wide"
)

# 初始化 Azure OpenAI 客戶端
if AZURE_OPENAI_API_KEY:
    try:
        client = openai.AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
    except Exception as e:
        st.error(f"⚠️ Azure OpenAI 初始化失敗: {str(e)}")
        st.stop()
else:
    st.error("⚠️ 請設置 AZURE_OPENAI_API_KEY 相關環境變數")
    st.stop()

# 初始化會話狀態
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# 頁面標題
st.title("🤖 AI 聊天助手")
st.markdown("---")

# 側邊欄配置
with st.sidebar:
    st.header("⚙️ 設置")
    
    # 溫度設置
    temperature = st.slider(
        "創意度 (Temperature)",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="較低的值會產生更一致的答案，較高的值會產生更創意的答案"
    )
    
    # 最大token數
    max_tokens = st.slider(
        "最大回應長度",
        min_value=100,
        max_value=2000,
        value=1000,
        step=100
    )
    
    # 清除聊天記錄
    if st.button("🗑️ 清除聊天記錄"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.uploaded_files = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 使用說明")
    st.markdown("""
    1. 上傳文件（支援圖片、PDF、Word文檔、文字文件）
    2. 在下方輸入框中輸入你的問題
    3. 按 Enter 或點擊發送按鈕
    4. AI 會根據你的問題和文件提供回答
    5. 可以在側邊欄調整創意度和回應長度
    """)
    
    st.markdown("---")
    st.markdown("### 🤖 模型信息")
    st.markdown("GPT-4o 支援文字和圖片分析")

# 文件上傳區域
st.header("📁 文件上傳")

uploaded_files = st.file_uploader(
    "選擇文件（支援多檔）",
    type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'pdf', 'docx', 'doc', 'txt', 'md', 'csv'],
    accept_multiple_files=True,
    help="支援圖片、PDF、Word文檔、文字文件等格式"
)

# 處理上傳的文件
if uploaded_files:
    st.session_state.uploaded_files = []
    
    for uploaded_file in uploaded_files:
        with st.spinner(f"正在處理 {uploaded_file.name}..."):
            result = FileProcessor.process_file(uploaded_file)
            
            if 'error' not in result:
                st.session_state.uploaded_files.append(result)
                
                # 顯示文件信息
                col1, col2 = st.columns([1, 3])
                with col1:
                    if result['type'] == 'image':
                        st.image(uploaded_file, width=100)
                    else:
                        st.write("📄")
                
                with col2:
                    st.write(f"**{result['filename']}**")
                    st.write(f"類型: {result['type']}")
                    st.write(f"信息: {result['info']}")
                
                st.success(f"✅ {uploaded_file.name} 處理完成")
            else:
                st.error(f"❌ {uploaded_file.name}: {result['error']}")

# 顯示所有圖片
all_images = [f for f in st.session_state.uploaded_files if f['type'] == 'image']
if all_images:
    st.header("📸 當前圖片")
    for i, img_info in enumerate(all_images):
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            img_data = base64.b64decode(img_info['content'])
            st.image(img_data, width=80)
        with col2:
            st.write(f"**{img_info['filename']}**")
            st.write(f"來源: 上傳")
            st.write(f"信息: {img_info['info']}")
        with col3:
            if st.button(f"❌ 移除", key=f"remove_{i}"):
                st.session_state.uploaded_files.remove(img_info)
                st.rerun()

# 顯示聊天記錄
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.info("👋 你好！我是你的AI助手，你可以上傳文件或直接輸入問題與我對話！")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message.get("type") == "image":
                st.image(message["content"], caption=message.get("filename", ""))
            else:
                st.markdown(message["content"])

# 用戶輸入
if prompt := st.chat_input("輸入你的問題..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 正在思考...")
        try:
            messages = []
            system_message = "你是一個有用的AI助手。"
            if st.session_state.uploaded_files:
                system_message += "用戶上傳了一些文件，請根據文件內容回答問題。"
            messages.append({"role": "system", "content": system_message})
            image_files = [f for f in st.session_state.uploaded_files if f['type'] == 'image']
            text_files = [f for f in st.session_state.uploaded_files if f['type'] != 'image']
            if image_files:
                if text_files:
                    file_content = "用戶上傳的文字文件內容：\n\n"
                    for file_info in text_files:
                        file_content += f"文件名: {file_info['filename']}\n"
                        file_content += f"文件類型: {file_info['type']}\n"
                        file_content += f"文件信息: {file_info['info']}\n"
                        file_content += f"文件內容:\n{file_info['content'][:2000]}...\n\n"
                    messages.append({"role": "user", "content": file_content})
                for image_file in image_files:
                    image_content = {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_file['content']}"
                        }
                    }
                    image_text = f"用戶上傳的圖片：{image_file['filename']}\n{image_file['info']}"
                    messages.append({
                        "role": "user",
                        "content": [
                            {"type": "text", "text": image_text},
                            image_content
                        ]
                    })
            else:
                if st.session_state.uploaded_files:
                    file_content = "用戶上傳的文件內容：\n\n"
                    for file_info in st.session_state.uploaded_files:
                        file_content += f"文件名: {file_info['filename']}\n"
                        file_content += f"文件類型: {file_info['type']}\n"
                        file_content += f"文件信息: {file_info['info']}\n"
                        file_content += f"文件內容:\n{file_info['content'][:2000]}...\n\n"
                    messages.append({"role": "user", "content": file_content})
            for msg in st.session_state.messages[-5:]:
                if msg["role"] != "system":
                    messages.append({"role": msg["role"], "content": msg["content"]})
            response = client.chat.completions.create(
                deployment_id=AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"❌ 發生錯誤: {str(e)}")
            message_placeholder.markdown("抱歉，發生了一些錯誤，請稍後再試。")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Powered by OpenAI GPT-4o & Streamlit</p>
        <p style='font-size:13px;color:#aaa;'>Copyright © Bruce Cheng 2025</p>
    </div>
    """,
    unsafe_allow_html=True
) 