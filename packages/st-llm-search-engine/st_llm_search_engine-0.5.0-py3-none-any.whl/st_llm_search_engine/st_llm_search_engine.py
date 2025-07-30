import os
import streamlit as st
import streamlit.components.v1 as components

# 取得當前檔案所在目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
# 構建前端組件路徑
component_path = os.path.join(current_dir, "frontend/build")


# 宣告 Streamlit 組件
_component_func = components.declare_component(
    "render",
    path=component_path
)


def render(height="100vh", key=None, api_url=None, api_key=None):
    """
    渲染 React 組件

    參數:
    - height: 組件高度，預設為 "100vh"（視窗高度）
    - key: Streamlit 組件的唯一標識
    - api_url: API服務器的URL，如果為None則使用默認值
    - api_key: API服務器的驗證密鑰

    返回:
    - 組件的返回值，可能包含以下格式：
      - 如果是加載保存的查詢條件：{"type": "LOAD_SEARCH", "data": {...查詢條件...}}
      - 如果是保存新的查詢條件：{"type": "SAVE_SEARCH", "data": {...查詢條件...}}
      - 如果是篩選後的KOL數據：{"type": "FILTERED_DATA", "data": {formData, filterResult, messages}}
      - 如果是篩選數據出錯：{"type": "FILTERED_DATA_ERROR", "data": {message}}
    """

    #########################################################

    # 調試信息 (僅在控制台輸出，不顯示在UI上)
    print(f"組件路徑: {component_path}")
    print(f"組件路徑是否存在: {os.path.exists(component_path)}")
    if os.path.exists(component_path):
        print(f"組件目錄內容: {os.listdir(component_path)}")

    #########################################################

    # 添加CSS確保組件填滿整個視窗
    st.markdown("""
    <style>
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 用於存儲聊天訊息的 session_state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # 用於追踪數據更新的 session_state
    if "update_count" not in st.session_state:
        st.session_state.update_count = 0

    # 嘗試渲染組件
    try:
        component_value = _component_func(
            height=height,
            key=key,
            api_url=api_url,
            api_key=api_key
        )

        # 處理組件返回值
        if component_value and isinstance(component_value, dict):
            message_type = component_value.get('type')
            data = component_value.get('data')

            # 如果是加載保存的查詢條件
            if message_type == 'LOAD_SEARCH':
                print(f"加載查詢條件: {data}")
                # 可以在這裡添加額外的處理邏輯

            # 如果是保存新的查詢條件
            elif message_type == 'SAVE_SEARCH':
                print(f"保存查詢條件: {data}")
                # 可以在這裡添加額外的處理邏輯

            # 如果是篩選後的KOL數據
            elif message_type == 'FILTERED_DATA':
                print(f"收到篩選後的KOL數據")

                if data and isinstance(data, dict) and 'messages' in data:
                    # 清空之前的訊息以避免堆積
                    st.session_state.chat_messages = []

                    messages = data.get('messages', [])
                    print(f"接收到 {len(messages)} 條訊息")

                    # 將篩選結果訊息添加到聊天界面
                    for message in messages:
                        if message and isinstance(message, dict):
                            role = message.get('role', 'bot')
                            content = message.get('content', '')

                            # 檢查角色格式
                            if role not in ['user', 'bot']:
                                role = 'bot'  # 預設使用 bot

                            # 添加到聊天訊息中
                            st.session_state.chat_messages.append({
                                'role': role,
                                'content': content
                            })

                    # 增加更新計數以觸發重新渲染
                    st.session_state.update_count += 1
                    print(f"更新計數: {st.session_state.update_count}")

            # 如果是篩選數據出錯
            elif message_type == 'FILTERED_DATA_ERROR':
                print(f"篩選KOL數據出錯")

                error_message = data.get('message', '篩選數據時出錯，請稍後再試') if data else '篩選數據時出錯，請稍後再試'

                # 添加錯誤訊息到聊天界面
                st.session_state.chat_messages.append({
                    'role': 'bot',
                    'content': f"**錯誤**: {error_message}"
                })

                # 增加更新計數以觸發重新渲染
                st.session_state.update_count += 1

        # 創建一個容器來展示訊息，並顯示更新計數以確保重新渲染
        chat_container = st.container()

        # 顯示聊天訊息
        with chat_container:
            # 添加隱藏的計數器來強制更新
            st.empty().markdown(f'<div style="display:none">{st.session_state.update_count}</div>', unsafe_allow_html=True)

            if hasattr(st.session_state, 'chat_messages') and st.session_state.chat_messages:
                for message in st.session_state.chat_messages:
                    role = message.get('role', 'bot')
                    content = message.get('content', '')

                    if role == 'user':
                        st.markdown(f"**User**: {content}", unsafe_allow_html=True)
                    else:
                        # 使用 unsafe_allow_html=True 確保 Markdown 和 HTML 格式能正確顯示
                        st.markdown(f"{content}", unsafe_allow_html=True)

        return component_value
    except Exception as e:
        st.error(f"組件渲染失敗: {str(e)}")
        return None


