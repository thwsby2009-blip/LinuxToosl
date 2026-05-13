import streamlit as st
import os

st.set_page_config(page_title="Linux 實戰工具書", page_icon="🐧")

# --- 側邊欄：自動讀取 .md 檔案清單 ---
st.sidebar.title("📚 Linux 指令選單")

# 獲取當前目錄下所有的 .md 檔案（排除 README.md）
md_files = [f for f in os.listdir('.') if f.endswith('.md') and f != "README.md"]
md_files.sort() # 排序，讓 01, 02 照順序排

if not md_files:
    st.error("找不到 .md 檔案！請確認檔案已上傳至 GitHub。")
else:
    selected_file = st.sidebar.selectbox("請選擇章節：", md_files)

    # --- 主畫面：讀取並顯示 Markdown 內容 ---
    st.title("📖 Linux 互動筆記")
    
    with open(selected_file, "r", encoding="utf-8") as f:
        content = f.read()
        st.markdown(content)

# --- 頁尾設計 ---
st.sidebar.divider()
st.sidebar.info("編輯：Harry.Tsai")
