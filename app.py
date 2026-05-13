import streamlit as st
import os

# 1. 頁面基礎設定
st.set_page_config(
    page_title="Linux 終端機實戰手冊",
    page_icon="🐧",
    layout="wide"
)

# 2. 注入自定義 CSS：美化程式碼區塊與視覺字體
st.markdown("""
    <style>
    /* 程式碼區塊美化 */
    code {
        color: #e83e8c !important;
        background-color: #f8f9fa !important;
        padding: 2px 5px !important;
        border-radius: 5px !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    /* 整塊指令區塊美化 */
    pre code {
        color: #212529 !important;
        background-color: #f1f3f5 !important;
        display: block !important;
        padding: 1.2rem !important;
        line-height: 1.5 !important;
        border-left: 5px solid #007bff !important;
    }
    /* 側邊欄標題顏色 */
    .sidebar .sidebar-content {
        background-color: #fdfdfd;
    }
    </style>
""", unsafe_allow_html=True)

# --- 側邊欄設計 ---
st.sidebar.title("📖 Linux 工具書")
st.sidebar.markdown("---")

# 獲取當前目錄下所有的 .md 檔案（排除 README.md）
md_files = [f for f in os.listdir('.') if f.endswith('.md') and f != "README.md"]
md_files.sort()

if not md_files:
    st.sidebar.error("❌ 找不到 .md 檔案！")
    st.title("歡迎使用 Linux 實戰工具書")
    st.info("請上傳 Markdown 檔案至 GitHub 倉庫以開始內容。")
else:
    # 讓使用者選擇章節
    selected_file = st.sidebar.selectbox(
        "📂 選擇教學章節：",
        ["--- 請選擇 ---"] + md_files
    )

    st.sidebar.divider()
    
    # 重新整理按鈕：讓學生能一鍵同步 GitHub 最新內容
    if st.sidebar.button("🔄 刷新內容同步"):
        st.rerun()

    st.sidebar.info("講師：嚴 稑 臻\n網管開發助手：Gemini")

    # --- 主畫面邏輯 ---
    if selected_file == "--- 請選擇 ---":
        # 首頁歡迎畫面
        st.title("🐧 歡迎進入 Linux 指令實戰工具書")
        st.markdown("""
        這是一個專為 Linux 初學者與網管人員設計的互動式手冊。
        
        ### 💡 如何開始？
        1. 從左側 **「選擇教學章節」** 下拉選單中挑選單元。
        2. 閱讀說明，並利用指令區塊右上角的 **「複製按鈕」** 快速實作。
        3. 如果內容有更新，點擊左側的 **「刷新內容同步」**。
        
        ---
        *提示：建議搭配 Google Colab 或虛擬機進行實戰演練。*
        """)
    else:
        # 顯示所選的 Markdown 內容
        try:
            with open(selected_file, "r", encoding="utf-8") as f:
                content = f.read()
                # 取得檔名作為標題（去掉 .md）
                display_title = selected_file.replace(".md", "").replace("_", " ")
                st.title(f"📄 單元：{display_title}")
                st.markdown(content)
        except Exception as e:
            st.error(f"讀取檔案時出錯：{e}")

# --- 頁尾隱藏 Streamlit 標誌（選做） ---
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)
