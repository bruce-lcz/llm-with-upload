# 🤖 AI 聊天助手

一個基於 Streamlit 和 Azure OpenAI GPT-4o 的智能聊天機器人應用，支援文件上傳和多模態對話。

## 功能特色

- 💬 即時聊天界面
- 📁 **文件上傳支援** - 圖片、PDF、Word文檔、文字文件
- 🤖 **GPT-4o 模型**（Azure OpenAI）- 支援文字和圖片分析
- ⚙️ 可調整的模型參數 (溫度、最大token數)
- 📱 響應式設計
- 🔄 流式回應顯示
- 🗑️ 清除聊天記錄功能
- 🖼️ 圖片分析能力

## 支援的文件格式

### 圖片文件
- JPG, JPEG, PNG, GIF, BMP, WebP
- 支援圖片內容分析

### 文檔文件
- PDF - 自動提取文字內容
- Word文檔 (.docx, .doc) - 提取段落文字
- 文字文件 (.txt, .md, .csv)

## 安裝步驟

### 1. 安裝依賴包

```bash
pip install -r requirements.txt
```

### 2. 設置 Azure OpenAI 參數

請在 `config.py` 中填入你的 Azure OpenAI 相關資訊，或於 `.env` 設定下列參數：

```env
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

> 你也可以直接在 `config.py` 編輯這些參數。

### 3. 運行應用

```bash
streamlit run app.py --server.port 8566
```

應用將在 `http://localhost:8566` 啟動。

## 使用說明

### 基本對話
1. 在輸入框中輸入你的問題
2. 按 Enter 或點擊發送按鈕
3. AI 會根據你的問題提供回答

### 文件分析
1. **上傳文件**：在文件上傳區域選擇要分析的文件
2. **等待處理**：系統會自動處理並顯示文件信息
3. **提問**：在聊天框中輸入關於文件的問題
4. **獲得回答**：AI 會根據文件內容回答你的問題

### 調整設置
在側邊欄可以：
- 調整創意度 (Temperature)
- 設置最大回應長度
- 清除聊天記錄

## GPT-4o (Azure OpenAI) 模型特色

- **多模態能力**：同時支援文字和圖片分析
- **強大推理**：更準確的邏輯推理和問題解決
- **快速回應**：優化的回應速度
- **智能理解**：更好的上下文理解能力

## 環境變數

| 變數名 | 說明 | 必需 | 範例 |
|--------|------|------|------|
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API Key | ✅ | `xxxxxxx` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI 端點 | ✅ | `https://your-resource-name.openai.azure.com/` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Azure OpenAI 部署名稱 | ✅ | `gpt-4o` |
| `AZURE_OPENAI_API_VERSION` | API 版本 | ✅ | `2024-02-15-preview` |

## 使用範例

### 圖片分析
1. 上傳一張圖片
2. 問：「這張圖片裡有什麼？」
3. AI 會描述圖片內容

### 文檔分析
1. 上傳 PDF 或 Word 文檔
2. 問：「這份文檔的主要內容是什麼？」
3. AI 會總結文檔重點

### 多文件分析
1. 上傳多個相關文件
2. 問：「這些文件之間有什麼關聯？」
3. AI 會分析文件間的關係

## 注意事項

- 請確保你有有效的 Azure OpenAI API Key 與正確的 Endpoint、Deployment Name
- API 調用會產生費用，請注意使用量
- 大文件處理可能需要較長時間
- 建議在生產環境中設置適當的速率限制
- GPT-4o 支援圖片分析，無需額外設置

## 故障排除

### 常見問題

1. **API Key 或 Endpoint 錯誤**
   - 檢查 `config.py` 或 `.env` 中的參數是否正確
   - 確保 API Key 有足夠的權限

2. **文件上傳失敗**
   - 檢查文件格式是否支援
   - 確認文件大小是否過大
   - 檢查文件是否損壞

3. **圖片分析失敗**
   - 檢查圖片格式是否支援
   - 確認 Azure OpenAI 部署支援多模態

4. **連接錯誤**
   - 檢查網路連接
   - 確認 Azure OpenAI 服務狀態

## 技術架構

- **前端**: Streamlit
- **後端**: Python
- **AI 服務**: Azure OpenAI GPT-4o
- **文件處理**: PIL, PyPDF2, python-docx
- **配置管理**: python-dotenv

## 授權

MIT License