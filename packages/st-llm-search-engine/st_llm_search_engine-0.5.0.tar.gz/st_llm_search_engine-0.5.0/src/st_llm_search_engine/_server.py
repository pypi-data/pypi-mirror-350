from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import traceback
from fastapi.middleware.cors import CORSMiddleware
from st_llm_search_engine.gemini import get_gemini_api_key
from st_llm_search_engine.sheet import (
    get_kol_sheet_config as get_sheet_config,
    get_saved_search_config,
    get_kol_data_config
)
import gspread
import socket
import subprocess
import time
import json
from datetime import datetime, timezone, timedelta
from functools import lru_cache
import threading
import os
import logging
import sys
import pandas as pd
from pathlib import Path
import google.generativeai as genai
from google.generativeai import GenerativeModel  # 明確導入 GenerativeModel
from google.api_core.exceptions import InvalidArgument
from typing import List, Dict, Any, Optional

# 設置日誌文件路徑
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug.log")

# 確保日誌文件存在，並清空它
with open(LOG_FILE, "w") as f:
    f.write(f"API 服務器調試日誌 - 啟動時間: {datetime.now()}\n")
    f.write("="*50 + "\n\n")

def write_log(message):
    """直接將消息寫入日誌文件"""
    try:
        with open(LOG_FILE, "a") as f:
            timestamp = datetime.now().strftime("%H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
            f.flush()
    except Exception as e:
        print(f"寫入日誌出錯: {e}")

# 記錄啟動信息
write_log("API 服務器已啟動")

# 配置日誌系統，同時輸出到控制台和文件
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger("st_llm_search_engine.server")

# 初始日誌
logger.info("="*50)
logger.info("API 服務器啟動")
logger.info("="*50)

# 添加緩存鎖，防止並發更新緩存
_cache_lock = threading.Lock()

# 緩存的保存查詢數據
_saved_searches_cache = None
_cache_timestamp = 0

# KOL 數據緩存
_kol_data_cache = None
_kol_data_cache_timestamp = 0

# API URL 相關變量和函數
_api_url = "http://localhost:8000"  # 默認API URL

# 用於存儲消息的全局變量
_messages = {}  # 改為字典，鍵為session_id，值為該session的消息列表
_message_lock = threading.RLock()
_message_id_counter = 0  # 添加消息ID計數器初始化


def set_api_url(url):
    """設定API URL"""
    global _api_url
    _api_url = url


def get_api_url():
    """獲取API URL"""
    return _api_url


load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源，包括Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_MODEL = "gemini-2.0-flash"


def gemini_chat(messages, api_key):
    # messages: [{"role": "user"/"bot", "content": "..."}]
    # 如果 API key 為空，直接返回錯誤信息
    if not api_key:
        # 尝试从环境变量直接获取 API key
        env_api_key = os.environ.get("GEMINI_API_KEY", "")
        if env_api_key:
            print("从环境变量获取 Gemini API 密钥")
            api_key = env_api_key
        else:
            print("錯誤：未設置 Gemini API 密鑰")
            return "錯誤：未設置 Gemini API 密鑰，無法使用聊天功能。請在環境變數中設置 GEMINI_API_KEY。"

    contents = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        # 確保不修改原始內容，保留所有換行符
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{GEMINI_MODEL}:generateContent")
    headers = {"Content-Type": "application/json"}
    payload = {"contents": contents}
    params = {"key": api_key}
    resp = requests.post(
        url, headers=headers, params=params, json=payload, timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


@app.post("/api/chat")
async def chat(request: Request):
    """
    處理聊天請求，生成回應。

    期望的請求格式：
    {
        "messages": [
            {"role": "user", "content": "你好"},
            {"role": "bot", "content": "您好，有什麼我能幫忙的嗎？"},
            ...
        ],
        "session_id": "用戶的會話ID，可選" // 新增
    }
    """
    global _messages, _message_id_counter

    try:
        req_data = await request.json()
        messages = req_data.get("messages", [])
        session_id = req_data.get("session_id", "default")  # 獲取session_id，默認為"default"

        write_log("="*50)
        write_log(f"聊天請求 (session_id: {session_id})")
        write_log(f"收到 {len(messages)} 條消息")

        # 確保有消息可處理
        if not messages:
            write_log("錯誤: 消息列表為空")
            return JSONResponse({"error": "消息列表不能為空"}, status_code=400)

        # 獲取最新的用戶消息
        last_msg = messages[-1]
        if last_msg.get("role") != "user":
            write_log("錯誤: 最後一條消息不是用戶消息")
            return JSONResponse({"error": "最後一條消息必須是用戶消息"}, status_code=400)

        # 獲取用戶輸入內容
        user_input = last_msg.get("content", "").strip()
        if not user_input:
            write_log("錯誤: 用戶輸入為空")
            return JSONResponse({"error": "用戶輸入不能為空"}, status_code=400)

        write_log(f"用戶輸入: {user_input[:50]}...")

        # 處理用戶輸入並生成回應
        try:
            # 檢查是否為模擬回應模式
            if os.environ.get('MOCK_REPLY') == 'true':
                write_log("使用模擬回應模式")
                bot_reply = f"這是對 '{user_input}' 的模擬回應。時間戳: {datetime.now().isoformat()}"
            else:
                # 使用實際的 LLM 處理
                gemini_key = get_gemini_api_key()
                if not gemini_key:
                    write_log("錯誤: Google API key 未設置")
                    return JSONResponse({"error": "Google API key 未設置，無法使用 AI 功能"}, status_code=503)

                # 配置API密鑰
                genai.configure(api_key=gemini_key)
                model = GenerativeModel(GEMINI_MODEL)

                # 準備聊天歷史，排除最新的用戶消息（稍後單獨添加）
                chat_history = []
                for msg in messages[:-1]:  # 只使用歷史消息
                    role = msg.get("role")
                    content = msg.get("content", "")
                    # 將前端的 "user"/"bot" 角色映射為 Gemini 的 "user"/"model"
                    gemini_role = "user" if role == "user" else "model"
                    chat_history.append({"role": gemini_role, "parts": [content]})

                # 創建聊天會話
                chat = model.start_chat(history=chat_history if chat_history else None)

                # 發送最新的用戶消息並獲取回應
                response = chat.send_message(user_input)
                bot_reply = response.text

            # 創建新的消息 ID
            with _message_lock:
                _message_id_counter += 1
                msg_id = f"{int(time.time() * 1000)}_{_message_id_counter}"

            # 創建用戶消息對象
            user_message = {
                "id": f"{msg_id}_user",
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().strftime("%H:%M")
            }

            # 創建機器人回應消息對象
            bot_message = {
                "id": f"{msg_id}_bot",
                "role": "bot",
                "content": bot_reply,
                "timestamp": datetime.now().strftime("%H:%M")
            }

            # 將新消息添加到會話歷史
            with _message_lock:
                # 確保該session_id的消息列表存在
                if session_id not in _messages:
                    _messages[session_id] = []

                # 添加消息
                _messages[session_id].append(user_message)
                _messages[session_id].append(bot_message)
                write_log(f"已添加用戶消息和機器人回應到會話 {session_id}")
                write_log(f"當前消息總數: {len(_messages[session_id])}")

            # 返回機器人回應
            return JSONResponse({"reply": bot_reply})

        except Exception as e:
            write_log(f"處理聊天請求時出錯: {str(e)}")
            traceback.print_exc()
            return JSONResponse({"error": f"處理請求時出錯: {str(e)}"}, status_code=500)

    except Exception as e:
        write_log(f"解析聊天請求時出錯: {str(e)}")
        traceback.print_exc()
        return JSONResponse({"error": f"解析請求時出錯: {str(e)}"}, status_code=400)

@app.post("/api/chat_direct")
async def chat_direct(request: Request):
    """
    直接添加一條訊息到聊天界面，不通過 LLM。

    期望的請求格式：
    {
        "role": "user" | "bot",
        "content": "訊息內容",
        "metadata": { "query": "查詢字串" }, // 可選
        "session_id": "用戶的會話ID，可選" // 新增
    }
    """
    global _messages, _message_id_counter

    try:
        data = await request.json()
        write_log("="*50)
        session_id = data.get("session_id", "default")  # 獲取session_id，默認為"default"
        write_log(f"直接添加消息 (session_id: {session_id})")

        if not isinstance(data, dict):
            write_log("錯誤: 請求格式不正確")
            return JSONResponse({"error": "請求格式不正確"}, status_code=400)

        role = data.get("role")
        if role not in ["user", "bot"]:
            write_log(f"錯誤: 角色無效 {role}")
            return JSONResponse({"error": "角色必須為 'user' 或 'bot'"}, status_code=400)

        content = data.get("content")
        if content is None:
            write_log("錯誤: 消息內容為空")
            return JSONResponse({"error": "消息內容不能為空"}, status_code=400)

        metadata = data.get("metadata", {})

        # 創建新的消息 ID
        with _message_lock:
            _message_id_counter += 1
            msg_id = f"{int(time.time() * 1000)}_{_message_id_counter}"

        # 創建消息對象
        message = {
            "id": msg_id,
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%H:%M"),
            "metadata": metadata
        }

        # 添加消息到歷史
        with _message_lock:
            # 確保該session_id的消息列表存在
            if session_id not in _messages:
                _messages[session_id] = []

            _messages[session_id].append(message)
            message_count = len(_messages[session_id])

        write_log(f"消息已添加，ID: {msg_id}")
        write_log(f"當前消息總數: {message_count}")
        write_log("="*50)

        return JSONResponse({"id": msg_id, "status": "success"})

    except Exception as e:
        write_log("="*50)
        write_log(f"添加直接消息時出錯: {str(e)}")
        traceback.print_exc()
        write_log("="*50)
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/chat_direct_batch")
async def chat_direct_batch(request: Request):
    """
    批量添加訊息到聊天界面，不通過 LLM。
    用於一次性添加多個消息，減少API請求次數。

    期望的請求格式：
    {
        "messages": [
            {
                "role": "user" | "bot",
                "content": "訊息內容1",
                "metadata": { "query": "查詢字串" } // 可選
            },
            {
                "role": "user" | "bot",
                "content": "訊息內容2",
                "metadata": { "query": "查詢字串" } // 可選
            },
            ...
        ],
        "session_id": "用戶的會話ID，可選" // 新增
    }
    """
    global _messages, _message_id_counter

    try:
        req_data = await request.json()
        messages = req_data.get("messages", [])
        session_id = req_data.get("session_id", "default")  # 獲取session_id，默認為"default"

        write_log("="*50)
        write_log(f"批量添加消息 (session_id: {session_id}): {len(messages)} 條")

        if not isinstance(messages, list):
            write_log("錯誤: 請求格式不正確，應為消息數組")
            return JSONResponse({"error": "請求格式不正確，應為消息數組"}, status_code=400)

        if len(messages) == 0:
            write_log("錯誤: 消息數組為空")
            return JSONResponse({"error": "消息數組不能為空"}, status_code=400)

        added_messages = []

        # 添加每條消息
        for msg_data in messages:
            if not isinstance(msg_data, dict):
                continue

            role = msg_data.get("role")
            if role not in ["user", "bot"]:
                continue

            content = msg_data.get("content")
            if content is None:
                continue

            metadata = msg_data.get("metadata", {})

            # 創建新的消息 ID
            with _message_lock:
                _message_id_counter += 1
                msg_id = f"{int(time.time() * 1000)}_{_message_id_counter}"

            # 創建消息對象
            message = {
                "id": msg_id,
                "role": role,
                "content": content,
                "timestamp": datetime.now().strftime("%H:%M"),
                "metadata": metadata
            }

            added_messages.append(message)

        # 批量添加所有有效消息
        with _message_lock:
            # 確保該session_id的消息列表存在
            if session_id not in _messages:
                _messages[session_id] = []

            _messages[session_id].extend(added_messages)
            message_count = len(_messages[session_id])

        write_log(f"已添加 {len(added_messages)} 條有效消息")
        write_log(f"當前消息總數: {message_count}")
        write_log("="*50)

        return JSONResponse({
            "status": "success",
            "count": len(added_messages),
            "ids": [msg["id"] for msg in added_messages]
        })

    except Exception as e:
        write_log("="*50)
        write_log(f"批量添加消息時出錯: {str(e)}")
        traceback.print_exc()
        write_log("="*50)
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/gemini_analysis")
async def analyze_data_with_gemini(request: Request):
    """分析表格數據並提供見解"""
    try:
        req_data = await request.json()
        records = req_data.get("data", req_data.get("records"))  # 嘗試從 data 或 records 字段獲取數據
        query = req_data.get("query", "")
        session_id = req_data.get("session_id", "default")  # 獲取session_id，默認為"default"

        if not records:
            return JSONResponse({"error": "未提供記錄數據"}, status_code=400)

        # 獲取API密鑰
        gemini_key = get_gemini_api_key()
        if not gemini_key:
            return JSONResponse({
                "error": f"未設置Google API密鑰，無法使用 {GEMINI_MODEL} 進行分析。請檢查環境變量。"
            }, status_code=503)

        try:
            # 配置API密鑰
            genai.configure(api_key=gemini_key)
            model = GenerativeModel(GEMINI_MODEL)

            # 創建聊天會話
            chat = model.start_chat(history=[])

            # 準備提示詞
            system_prompt = """你是一個專業的數據分析師，擅長分析網路社群數據。
當用戶提供數據時，請分析這些數據並提供專業見解。當用戶提出特定問題時，直接回答他們的問題。

請注意以下要點：
1. 回答應該簡潔但有洞察力
2. 識別數據中的關鍵趨勢和模式
3. 不要重複用戶已經知道的信息
4. 如果數據不足以得出結論，請誠實說明
5. 使用繁體中文回答

如果用戶沒有提出特定問題，請分析並突出表格數據中最重要的洞察。
"""
            # 將查詢與數據結合
            prompt_parts = []
            prompt_parts.append(system_prompt)

            # 添加查詢(如果有)
            if query:
                prompt_parts.append(f"\n用戶問題: {query}\n")
            else:
                prompt_parts.append("\n請分析以下數據並提供最重要的洞察:\n")

            # 添加數據
            data_str = json.dumps(records, ensure_ascii=False, indent=2)
            prompt_parts.append(f"數據 (JSON格式):\n{data_str}")

            # 發送系統提示
            full_prompt = "\n".join(prompt_parts)
            response = chat.send_message(full_prompt)

            # 創建消息對象
            with _message_lock:
                _message_id_counter += 1
                msg_id = f"{int(time.time() * 1000)}_{_message_id_counter}"

            # 創建分析結果消息
            analysis_message = {
                "id": msg_id,
                "role": "bot",
                "content": response.text,
                "timestamp": datetime.now().strftime("%H:%M"),
                "metadata": {"query": query}
            }

            # 添加消息到會話歷史
            with _message_lock:
                # 確保該session_id的消息列表存在
                if session_id not in _messages:
                    _messages[session_id] = []

                _messages[session_id].append(analysis_message)

            return JSONResponse({"response": response.text, "message_id": msg_id})
        except Exception as e:
            error_message = f"處理 {GEMINI_MODEL} 分析時出錯: {str(e)}。可能是API配額限制或格式異常。"
            write_log(error_message)
            return JSONResponse({"error": error_message}, status_code=500)
    except Exception as e:
        error_message = str(e)
        write_log(f"分析數據時出錯: {error_message}")
        return JSONResponse({"error": error_message}, status_code=500)

@app.get("/api/sheet/kol")
async def get_kol_tags(col: str):
    print(f"收到獲取標籤請求，列名: {col}")
    # 檢查配置
    cfg = get_sheet_config()
    print(f"Sheet配置: {cfg}")

    # Mock data for testing
    if not cfg["sheet_id"]:
        print("未設置sheet_id，返回測試數據")
        return JSONResponse(["學校", "政治", "媒體", "科技", "娛樂"])

    if not (cfg["sheet_id"] and cfg["tab_name"] and
            cfg["service_account_path"]):
        print("Sheet配置不完整")
        return JSONResponse({"error": "Sheet config not set"}, status_code=400)

    try:
        print(f"嘗試連接Google Sheet: ID={cfg['sheet_id']}, Tab={cfg['tab_name']}")
        gc = gspread.service_account(filename=cfg["service_account_path"])
        sh = gc.open_by_key(cfg["sheet_id"])
        ws = sh.worksheet(cfg["tab_name"])

        print(f"嘗試查找列: {col}")
        col_cell = ws.find(col)
        if not col_cell:
            print(f"未找到列: {col}")
            return JSONResponse(
                {"error": f"Column '{col}' not found"},
                status_code=404
            )

        print(f"找到列 {col} 在位置: {col_cell.col}")
        col_values = ws.col_values(col_cell.col)[1:]  # skip header

        # 去重並排序
        unique_values = sorted(list(set(col_values)))
        print(f"獲取到 {len(unique_values)} 個唯一標籤值")

        return JSONResponse(unique_values)
    except Exception as e:
        print(f"獲取標籤時出錯: {str(e)}")
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


def normalize_order_for_account(ws, account='系統'):
    """重新調整指定帳號的所有清單順序，確保順序連續"""
    try:
        # 獲取標題行
        headers = ws.row_values(1)

        # 檢查必要欄位
        title_col_idx = None
        order_col_idx = None
        account_col_idx = None

        if '標題' in headers:
            title_col_idx = headers.index('標題') + 1
        elif 'title' in headers:
            title_col_idx = headers.index('title') + 1

        if '順序' in headers:
            order_col_idx = headers.index('順序') + 1

        if '帳號' in headers:
            account_col_idx = headers.index('帳號') + 1

        if not (title_col_idx and order_col_idx):
            print("無法調整順序：缺少必要欄位")
            return False

        # 獲取所有數據
        all_data = ws.get_all_records()

        # 篩選出指定帳號的數據
        account_items = []
        for idx, row in enumerate(all_data):
            row_account = row.get('帳號', '系統')
            if row_account == account:
                # 記錄行號（+2 是因為索引從0開始且有標題行）
                account_items.append({
                    'title': row.get('標題', ''),
                    'order': int(row.get('順序', 9999)) if row.get('順序', '') else 9999,
                    'row': idx + 2
                })

        # 按現有順序排序
        account_items.sort(key=lambda x: x['order'])

        # 重新分配順序，確保從1開始連續
        batch_updates = []
        for i, item in enumerate(account_items, 1):
            row_num = item['row']
            new_order = i

            # 添加到批量更新列表
            batch_updates.append({
                'range': f'{ws.title}!{chr(64 + order_col_idx)}{row_num}',
                'values': [[str(new_order)]]
            })

        # 執行批量更新
        if batch_updates:
            ws.spreadsheet.values_batch_update(
                {
                    'data': batch_updates,
                    'valueInputOption': 'USER_ENTERED'
                }
            )
            print(f"已重新調整 {account} 帳號的順序，共更新 {len(batch_updates)} 個項目")
            return True

        return False
    except Exception as e:
        print(f"重新調整順序時出錯: {str(e)}")
        traceback.print_exc()
        return False

def get_cached_saved_searches(force_refresh=False):
    """獲取緩存的保存查詢數據，如果需要則強制刷新"""
    global _saved_searches_cache, _cache_timestamp

    current_time = time.time()
    cache_age = current_time - _cache_timestamp

    # 將緩存時間從10分鐘改為2分鐘，這樣更頻繁地檢查數據更新
    if _saved_searches_cache is None or cache_age > 120 or force_refresh:
        with _cache_lock:
            # 再次檢查，避免其他線程已經更新了緩存
            if _saved_searches_cache is None or cache_age > 120 or force_refresh:
                try:
                    # 檢查配置
                    cfg = get_saved_search_config()

                    if not (cfg["sheet_id"] and cfg["tab_name"] and
                            cfg["service_account_path"]):
                        print("Saved Search Sheet配置不完整")
                        return None

                    # 連接 Google Sheet
                    gc = gspread.service_account(filename=cfg["service_account_path"])
                    sh = gc.open_by_key(cfg["sheet_id"])

                    try:
                        ws = sh.worksheet(cfg["tab_name"])
                    except gspread.exceptions.WorksheetNotFound:
                        print(f"工作表 {cfg['tab_name']} 不存在")
                        return None

                    # 獲取所有記錄
                    records = ws.get_all_records()

                    # 按帳號分組處理數據
                    processed_data = {}

                    for record in records:
                        # 獲取帳號，默認為「系統」
                        account = record.get('帳號', '系統')

                        # 獲取標題和數據
                        title = record.get('標題', record.get('title', ''))
                        data = record.get('查詢值', record.get('data', ''))
                        order = record.get('順序', 9999)

                        # 嘗試解析數據
                        try:
                            if isinstance(data, str):
                                # 使用與寫入時相同的參數，不需要 ensure_ascii=False，因為讀取時不涉及 ASCII 轉換
                                parsed_data = json.loads(data)
                            else:
                                parsed_data = data
                        except (json.JSONDecodeError, TypeError):
                            print(f"無法解析數據: {data[:100]}...")  # 添加更多日誌信息
                            parsed_data = {"title": title}

                        # 如果帳號不在字典中，初始化
                        if account not in processed_data:
                            processed_data[account] = []

                        # 添加記錄
                        processed_data[account].append({
                            "title": title,
                            "data": parsed_data,
                            "order": int(order) if order and str(order).isdigit() else 9999
                        })

                    # 對每個帳號的數據按順序排序
                    for account in processed_data:
                        processed_data[account].sort(key=lambda x: x["order"])

                    # 更新緩存
                    _saved_searches_cache = processed_data
                    _cache_timestamp = current_time

                    print(f"已更新保存查詢緩存，包含 {len(processed_data)} 個帳號")

                except Exception as e:
                    print(f"更新緩存時出錯: {str(e)}")
                    traceback.print_exc()
                    # 如果出錯且緩存不存在，返回空字典
                    if _saved_searches_cache is None:
                        _saved_searches_cache = {}

    return _saved_searches_cache

def get_cached_kol_data(force_refresh=False):
    """獲取緩存的KOL數據，如果需要則強制刷新（每30分鐘更新一次）"""
    global _kol_data_cache, _kol_data_cache_timestamp

    current_time = time.time()
    cache_age = current_time - _kol_data_cache_timestamp

    # 如果緩存不存在、過期（30分鐘）或強制刷新
    if _kol_data_cache is None or cache_age > 1800 or force_refresh:
        with _cache_lock:
            # 再次檢查，避免其他線程已經更新了緩存
            if _kol_data_cache is None or cache_age > 1800 or force_refresh:
                try:
                    # 檢查配置
                    cfg = get_kol_data_config()

                    if not (cfg["sheet_id"] and cfg["tab_name"] and
                            cfg["service_account_path"]):
                        print("KOL Data Sheet配置不完整")
                        return None

                    # 連接 Google Sheet
                    gc = gspread.service_account(filename=cfg["service_account_path"])
                    sh = gc.open_by_key(cfg["sheet_id"])

                    try:
                        ws = sh.worksheet(cfg["tab_name"])
                    except gspread.exceptions.WorksheetNotFound:
                        print(f"工作表 {cfg['tab_name']} 不存在")
                        return None

                    # 獲取所有記錄
                    records = ws.get_all_records()

                    # 更新緩存
                    _kol_data_cache = records
                    _kol_data_cache_timestamp = current_time

                    print(f"已更新KOL數據緩存，包含 {len(records)} 條記錄")

                except Exception as e:
                    print(f"更新KOL數據緩存時出錯: {str(e)}")
                    traceback.print_exc()
                    # 如果出錯且緩存不存在，返回空列表
                    if _kol_data_cache is None:
                        _kol_data_cache = []

    return _kol_data_cache

def get_kol_mapping_records():
    """獲取KOL ID到名稱的映射記錄"""
    try:
        # 獲取KOL工作表配置
        kol_cfg = get_sheet_config()
        if not (kol_cfg["sheet_id"] and kol_cfg["tab_name"] and kol_cfg["service_account_path"]):
            print("KOL工作表配置不完整")
            return []

        # 連接Google Sheet
        gc = gspread.service_account(filename=kol_cfg["service_account_path"])
        sh = gc.open_by_key(kol_cfg["sheet_id"])
        kol_ws = sh.worksheet(kol_cfg["tab_name"])
        kol_records = kol_ws.get_all_records()

        print(f"獲取到 {len(kol_records)} 筆KOL映射記錄")
        return kol_records
    except Exception as e:
        print(f"獲取KOL映射記錄時出錯: {str(e)}")
        traceback.print_exc()
        return []

@app.post("/api/saved_search")
async def save_search(request: Request):
    """保存查詢條件"""
    try:
        # 獲取請求數據
        data = await request.json()
        print(f"接收到的數據: {data}")
        print(f"數據類型: {type(data)}")

        # 檢查是否有標題
        if "title" not in data or not data["title"]:
            print("缺少必要的標題字段")
            return JSONResponse(
                {"error": "Missing required field: title"},
                status_code=400
            )

        # 檢查配置
        cfg = get_saved_search_config()
        print(f"Saved Search Sheet配置: {cfg}")

        if not (cfg["sheet_id"] and cfg["tab_name"] and
                cfg["service_account_path"]):
            print("Saved Search Sheet配置不完整")
            return JSONResponse(
                {"error": "Saved Search Sheet config not set"},
                status_code=400
            )

        try:
            # 連接 Google Sheet
            print(f"嘗試連接 Google Sheet: {cfg['sheet_id']}")
            gc = gspread.service_account(filename=cfg["service_account_path"])
            sh = gc.open_by_key(cfg["sheet_id"])
            print(f"成功連接 Google Sheet")

            # 檢查工作表是否存在，如果不存在則創建
            try:
                ws = sh.worksheet(cfg["tab_name"])
                print(f"找到工作表: {cfg['tab_name']}")

                # 檢查工作表是否有標題行，如果沒有則添加
                headers = ws.row_values(1)
                if not headers or len(headers) < 6:
                    print("工作表缺少標題行，添加標題行")
                    ws.update('A1:F1', [['id', '標題', '帳號', '順序', '查詢值', '新增時間']])
                    print("已添加標題行")
            except gspread.exceptions.WorksheetNotFound:
                print(f"工作表 {cfg['tab_name']} 不存在，創建新工作表")
                ws = sh.add_worksheet(title=cfg["tab_name"], rows=1000, cols=20)
                # 添加標題行
                ws.update('A1:F1', [['id', '標題', '帳號', '順序', '查詢值', '新增時間']])
                print("已創建工作表並添加標題行")

            # 將數據轉換為JSON字符串
            data_json = json.dumps(data, ensure_ascii=False)
            print(f"數據已序列化為JSON: {data_json[:100]}...")

            # 檢查是否已存在相同標題的查詢條件
            try:
                print(f"查找標題: '{data['title']}'")
                cell = None
                try:
                    cell = ws.find(data["title"])
                except Exception as e:
                    print(f"查找標題時出錯: {str(e)}")
                    # 如果是 CellNotFound 或其他錯誤，cell 將保持為 None

                now = datetime.now().isoformat()

                if cell is None:
                    # 如果找不到，則添加新記錄
                    print(f"未找到已存在的查詢條件，添加新記錄")

                    # 獲取最後一行的ID並增加1
                    all_values = ws.get_all_values()
                    next_id = 1  # 默認從1開始

                    if len(all_values) > 1:  # 如果有數據行（不只是標題行）
                        try:
                            last_id = all_values[-1][0]  # 最後一行的第一列是ID
                            if last_id and last_id.isdigit():
                                next_id = int(last_id) + 1
                        except (IndexError, ValueError) as e:
                            print(f"獲取最後ID時出錯: {str(e)}，使用默認ID: {next_id}")

                    print(f"添加新記錄，ID: {next_id}，時間戳: {now}")

                    # 計算順序值（根據同一帳號的記錄數量）
                    # 獲取同一帳號的所有記錄
                    account = "暫存"  # 默認帳號
                    account_records = []

                    for record in all_values[1:]:  # 跳過標題行
                        if len(record) >= 3 and record[2] == account:  # index 2 是帳號列
                            account_records.append(record)

                    # 新記錄的順序設為帳號記錄數 + 1
                    order = len(account_records) + 1
                    print(f"同一帳號 '{account}' 已有 {len(account_records)} 條記錄，新記錄順序為: {order}")

                    ws.append_row([
                        str(next_id),          # id
                        data["title"],         # 標題
                        "暫存",                # 帳號 (改為"暫存"而不是"系統")
                        str(order),            # 順序
                        data_json,             # 查詢值 (JSON字符串)
                        now                     # 新增時間
                    ])
                    print(f"已添加新記錄")

                    # 重新調整順序
                    normalize_order_for_account(ws, "暫存")

                    # 強制刷新緩存
                    get_cached_saved_searches(force_refresh=True)

                    return JSONResponse({"status": "created", "title": data["title"]})
                else:
                    # 更新現有記錄
                    row_num = cell.row
                    print(f"找到已存在的查詢條件，行號: {row_num}")

                    # 更新現有記錄
                    print(f"更新記錄，時間戳: {now}")
                    ws.update_cell(row_num, 5, data_json)  # 查詢值
                    print(f"已更新記錄")

                    # 強制刷新緩存
                    get_cached_saved_searches(force_refresh=True)

                    return JSONResponse({"status": "updated", "title": data["title"]})
            except Exception as e:
                print(f"查找或更新記錄時出錯: {str(e)}")
                traceback.print_exc()
                return JSONResponse({"error": str(e)}, status_code=500)
        except Exception as e:
            print(f"保存查詢條件時出錯: {str(e)}")
            traceback.print_exc()
            return JSONResponse({"error": str(e)}, status_code=500)
    except Exception as e:
        print(f"處理請求時出錯: {str(e)}")
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/api/saved_search")
async def get_saved_search(title: str = None, account: str = None, force_refresh: bool = False):
    """
    獲取保存的搜索條件

    如果指定了 title 參數，則僅返回該標題的搜索條件
    """
    try:
        # 獲取緩存數據
        cached_data = get_cached_saved_searches(force_refresh=force_refresh)

        if cached_data is None:
            logger.error("無法獲取保存的搜索條件數據")
            return JSONResponse({"error": "Failed to retrieve saved searches"}, status_code=500)

        # 如果傳入了 title 參數，則只返回該標題的搜索條件
        if title:
            logger.info(f"獲取特定搜索條件: {title}")

            # 遍歷所有帳號和項目，查找匹配的標題
            for account_items in cached_data.values():
                for item in account_items:
                    if item["title"] == title:
                        # 只返回該記錄的 data 字段
                        return JSONResponse(item["data"])

            # 如果找不到對應標題的記錄，返回空對象
            return JSONResponse({}, status_code=404)

        # 如果傳入了 account 參數，則過濾該帳號的記錄
        if account:
            logger.info(f"過濾帳號 {account} 的搜索條件")
            if account in cached_data:
                # 從帳號分組數據中提取記錄
                records = cached_data[account]
                # 提取標題列表
                items = [record["title"] for record in records]
                return JSONResponse({
                    "items": items,
                    "records": records,
                    "account": account
                })
            else:
                # 如果沒有該帳號的數據，返回空列表
                return JSONResponse({
                    "items": [],
                    "records": [],
                    "account": account
                })

        # 返回所有記錄，轉換格式以兼容前端
        all_items = []
        all_records = []

        for account, items in cached_data.items():
            for item in items:
                all_items.append(item["title"])
                # 複製項目並添加帳號字段
                record = item.copy()
                record["account"] = account
                all_records.append(record)

        # 按帳號和順序值排序
        all_records.sort(key=lambda x: (0 if x.get("account") == "系統" else 1, x.get("order", 9999)))
        # 重新排列 items，與 records 順序一致
        all_items = [record["title"] for record in all_records]

        return JSONResponse({
            "items": all_items,
            "records": all_records
        })
    except Exception as e:
        logger.error(f"獲取保存的搜索條件時出錯: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/saved_search/reorder")
async def reorder_saved_searches(request: Request):
    """重新排序保存的查詢條件"""
    try:
        # 獲取請求數據
        data = await request.json()
        logger.info(f"接收到的重排序數據: {data}")

        if not isinstance(data, dict) or "items" not in data or not isinstance(data["items"], list):
            logger.error("無效的數據格式，期望 {items: [{title: string, order: number}, ...]}")
            return JSONResponse(
                {"error": "Invalid data format. Expected {items: [{title: string, order: number}, ...]}"},
                status_code=400
            )

        # 檢查配置
        cfg = get_saved_search_config()
        logger.info(f"Saved Search Sheet配置: {cfg}")

        if not (cfg["sheet_id"] and cfg["tab_name"] and cfg["service_account_path"]):
            logger.error("Saved Search Sheet配置不完整")
            return JSONResponse(
                {"error": "Saved Search Sheet config not set"},
                status_code=400
            )

        # 連接 Google Sheet
        gc = gspread.service_account(filename=cfg["service_account_path"])
        sh = gc.open_by_key(cfg["sheet_id"])

        try:
            ws = sh.worksheet(cfg["tab_name"])
        except gspread.exceptions.WorksheetNotFound:
            logger.error(f"工作表 {cfg['tab_name']} 不存在")
            return JSONResponse({"error": "Worksheet not found"}, status_code=404)

        # 獲取標題行
        headers = ws.row_values(1)

        # 檢查是否有順序欄位
        order_col_idx = None
        if '順序' in headers:
            order_col_idx = headers.index('順序') + 1  # gspread 列索引從1開始
        elif 'order' in headers:
            order_col_idx = headers.index('order') + 1  # gspread 列索引從1開始
        else:
            logger.error("工作表中沒有順序欄位")
            return JSONResponse({"error": "Order column not found in worksheet"}, status_code=400)

        # 檢查是否有標題欄位
        title_col_idx = None
        if '標題' in headers:
            title_col_idx = headers.index('標題') + 1  # gspread 列索引從1開始
        elif 'title' in headers:
            title_col_idx = headers.index('title') + 1
        else:
            logger.error("工作表中沒有標題欄位")
            return JSONResponse({"error": "Title column not found in worksheet"}, status_code=400)

        # 檢查是否有帳號欄位
        account_col_idx = None
        if '帳號' in headers:
            account_col_idx = headers.index('帳號') + 1  # gspread 列索引從1開始
        elif 'account' in headers:
            account_col_idx = headers.index('account') + 1

        # 獲取所有數據，包括帳號和標題
        all_data = ws.get_all_records()

        # 獲取前端請求中指定的帳號，如果沒有則處理所有非系統帳號的項目
        request_account = data.get("account", "暫存")  # 默認處理暫存帳號

        # 重新排序前端傳來的項目
        frontend_items = {item["title"]: item["order"] for item in data["items"]}

        # 尋找每個項目所屬的帳號
        item_accounts = {}
        for row in all_data:
            title = row.get('標題', row.get('title', ''))
            if title in frontend_items:
                account = row.get('帳號', row.get('account', '系統'))
                item_accounts[title] = account

        # 按帳號分組
        account_groups = {}
        for row in all_data:
            account = row.get('帳號', row.get('account', '系統'))  # 默認帳號為「系統」
            if account not in account_groups:
                account_groups[account] = []
            account_groups[account].append(row)

        # 更新每個項目的順序
        updated_items = []
        batch_updates = []  # 收集所有更新操作

        # 對每個帳號組處理
        for account, group_items in account_groups.items():
            # 跳過系統帳號，系統帳號項目不應被重排序
            if account == "系統":
                continue

            # 找出屬於當前組且在前端傳來的項目列表中的項目
            current_group_frontend_items = []
            for item in group_items:
                title = item.get('標題', item.get('title', ''))
                if title in frontend_items:
                    current_group_frontend_items.append({
                        'title': title,
                        'order': frontend_items[title],
                        'row': all_data.index(item) + 2  # +2 因為索引從0開始且有標題行
                    })

            # 如果當前帳號組有需要更新的項目
            if current_group_frontend_items:
                # 按前端傳來的順序排序
                current_group_frontend_items.sort(key=lambda x: x['order'])

                # 重新分配順序，確保從1開始連續
                for i, item in enumerate(current_group_frontend_items, 1):
                    row_num = item['row']
                    new_order = i
                    logger.info(f"更新 '{item['title']}' 的順序為 {new_order}（行號: {row_num}）")

                    # 添加到批量更新列表
                    batch_updates.append({
                        'range': f'{ws.title}!{chr(64 + order_col_idx)}{row_num}',
                        'values': [[str(new_order)]]
                    })

                    updated_items.append({
                        "title": item['title'],
                        "order": new_order
                    })

        # 執行批量更新
        if batch_updates:
            ws.spreadsheet.values_batch_update(
                {
                    'data': batch_updates,
                    'valueInputOption': 'USER_ENTERED'
                }
            )
            logger.info(f"批量更新完成，共更新 {len(batch_updates)} 個項目")

            # 重新調整所有帳號的順序
            for account in account_groups:
                normalize_order_for_account(ws, account)

            # 強制刷新緩存
            get_cached_saved_searches(force_refresh=True)

        return JSONResponse({
            "status": "success",
            "updated_items": updated_items
        })

    except Exception as e:
        logger.error(f"重排序查詢條件時出錯: {str(e)}")
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/api/saved_search/{title}")
async def get_saved_search_by_title(title: str):
    """獲取指定標題的查詢條件"""
    try:
        # 獲取緩存數據
        cached_data = get_cached_saved_searches()

        if cached_data is None:
            return JSONResponse(
                {"error": "Failed to retrieve saved searches"},
                status_code=500
            )

        # 檢查緩存格式並相應處理
        if isinstance(cached_data, dict):
            # 如果是按帳號分組的格式 {account1: [...items], account2: [...items]}
            for account_items in cached_data.values():
                for item in account_items:
                    if item["title"] == title:
                        return JSONResponse(item["data"])
        elif isinstance(cached_data, dict) and "records" in cached_data:
            # 如果是扁平格式 {"items": [...], "records": [...]}
            for record in cached_data.get("records", []):
                if record["title"] == title:
                    return JSONResponse(record["data"])

        # 如果未找到
        return JSONResponse(
            {"error": f"Search with title '{title}' not found"},
            status_code=404
        )
    except Exception as e:
        print(f"獲取查詢條件時出錯: {str(e)}")
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


@app.delete("/api/saved_search/{title}")
async def delete_saved_search(title: str):
    """刪除指定標題的查詢條件"""
    # 提前聲明全局變量
    global _saved_searches_cache, _cache_timestamp

    try:
        # 檢查配置
        cfg = get_saved_search_config()
        print(f"Saved Search Sheet配置: {cfg}")

        if not (cfg["sheet_id"] and cfg["tab_name"] and
                cfg["service_account_path"]):
            print("Saved Search Sheet配置不完整")
            return JSONResponse(
                {"error": "Saved Search Sheet config not set"},
                status_code=400
            )

        try:
            # 連接 Google Sheet
            gc = gspread.service_account(filename=cfg["service_account_path"])
            sh = gc.open_by_key(cfg["sheet_id"])

            try:
                ws = sh.worksheet(cfg["tab_name"])
            except gspread.exceptions.WorksheetNotFound:
                print(f"工作表 {cfg['tab_name']} 不存在")
                return JSONResponse({"error": "Worksheet not found"}, status_code=404)

            # 獲取標題行
            headers = ws.row_values(1)

            # 檢查是否有標題欄位
            title_col_idx = None
            if '標題' in headers:
                title_col_idx = headers.index('標題') + 1
            elif 'title' in headers:
                title_col_idx = headers.index('title') + 1
            else:
                print("工作表中沒有標題欄位")
                return JSONResponse({"error": "Title column not found"}, status_code=400)

            # 檢查是否有帳號欄位
            account_col_idx = None
            if '帳號' in headers:
                account_col_idx = headers.index('帳號') + 1

            # 查找要刪除的記錄
            try:
                # 獲取所有數據以避免 findall 可能的問題
                all_data = ws.get_all_values()
                target_row = None

                # 從第二行開始搜索 (跳過標題行)
                for row_idx, row in enumerate(all_data[1:], start=2):
                    # 檢查標題是否匹配 (注意 title_col_idx 從 1 開始，而 row 索引從 0 開始)
                    if row[title_col_idx-1] == title:
                        target_row = row_idx
                        break

                if not target_row:
                    print(f"未找到標題為 '{title}' 的記錄")
                    return JSONResponse({"error": "Record not found"}, status_code=404)

                # 刪除記錄
                ws.delete_rows(target_row)
                print(f"已刪除標題為 '{title}' 的記錄 (行號: {target_row})")

                # 重新調整順序 (不依賴帳號，優先調整「暫存」帳號的順序)
                try:
                    normalize_order_for_account(ws, "暫存")
                    print("已重新調整「暫存」帳號的順序")
                except Exception as e:
                    print(f"重新調整「暫存」帳號順序時出錯: {str(e)}")

                # 無論如何，強制刷新緩存
                _saved_searches_cache = None
                _cache_timestamp = 0
                get_cached_saved_searches(force_refresh=True)

                return JSONResponse({"status": "success", "deleted": title})

            except Exception as e:
                print(f"刪除記錄時出錯: {str(e)}")
                traceback.print_exc()

                # 即使出錯，也強制刷新緩存
                _saved_searches_cache = None
                _cache_timestamp = 0

                return JSONResponse({"error": str(e)}, status_code=500)

        except Exception as e:
            print(f"刪除查詢條件時出錯: {str(e)}")
            traceback.print_exc()
            return JSONResponse({"error": str(e)}, status_code=500)
    except Exception as e:
        print(f"處理刪除請求時出錯: {str(e)}")
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        # 在任何情況下都強制刷新緩存
        try:
            _saved_searches_cache = None
            _cache_timestamp = 0
        except:
            pass


@app.get("/api/kol-data")
async def get_kol_data(force_refresh: bool = False):
    """獲取KOL數據列表"""
    try:
        # 獲取緩存的KOL數據
        data = get_cached_kol_data(force_refresh)

        if data is None:
            return JSONResponse(
                {"error": "無法獲取KOL數據，配置可能不完整"},
                status_code=500
            )

        return JSONResponse(data)
    except Exception as e:
        print(f"獲取KOL數據時出錯: {str(e)}")
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


def is_port_in_use(port):
    """檢查端口是否被佔用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def find_available_port(start_port=8000, max_attempts=10):
    """尋找可用端口"""
    port = start_port
    for _ in range(max_attempts):
        if not is_port_in_use(port):
            return port
        port += 1
    return None


def run_api_server(host="localhost", start_port=8000, sheet_config=None, saved_search_config=None, kol_data_config=None, return_pid=False, workers=4):
    """
    啟動 API 服務器

    參數:
    - host: 主機名，默認為 localhost
    - start_port: 起始端口號，默認為 8000
    - sheet_config: Sheet 配置字典，可選
    - saved_search_config: Saved Search Sheet 配置字典，可選
    - kol_data_config: KOL Data Sheet 配置字典，可選
    - return_pid: 是否返回進程 ID，默認為 False
    - workers: 工作進程數，默認為 4

    返回:
    - 如果 return_pid 為 True，返回 (API URL, 進程 ID)
    - 否則僅返回 API URL
    """
    # 查找可用端口
    port = find_available_port(start_port)
    api_url = f"http://{host}:{port}"

    # 設置 Sheet 環境變數
    if sheet_config and isinstance(sheet_config, dict):
        os.environ["SHEET_ID"] = sheet_config.get("sheet_id", "")
        os.environ["SHEET_TAB"] = sheet_config.get("tab_name", "")
        os.environ["SHEET_CREDENTIALS"] = sheet_config.get("service_account_path", "")

    # 設置 Saved Search Sheet 環境變數
    if saved_search_config and isinstance(saved_search_config, dict):
        os.environ["SAVED_SEARCH_SHEET_ID"] = saved_search_config.get("sheet_id", "")
        os.environ["SAVED_SEARCH_TAB"] = saved_search_config.get("tab_name", "")
        os.environ["SAVED_SEARCH_CREDENTIALS"] = saved_search_config.get(
            "service_account_path", ""
        )

    # 設置 KOL Data Sheet 環境變數
    if kol_data_config and isinstance(kol_data_config, dict):
        os.environ["KOL_DATA_SHEET_ID"] = kol_data_config.get("sheet_id", "")
        os.environ["KOL_DATA_TAB"] = kol_data_config.get("tab_name", "")
        os.environ["KOL_DATA_CREDENTIALS"] = kol_data_config.get(
            "service_account_path", ""
        )

    # 啟動 API 服務器
    cmd = [
        "uvicorn",
        "st_llm_search_engine.server:app",
        "--host", host,
        "--port", str(port),
        "--workers", str(workers),  # 設置工作進程數
        "--reload"
    ]

    # 在子進程中運行服務器
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    # 設置 API URL
    set_api_url(api_url)
    print(f"API 服務器已啟動: {api_url}")

    if return_pid:
        return api_url, process.pid
    else:
        return api_url


# 保留原來的 run_server 函數名稱作為別名，以兼容現有代碼
run_server = run_api_server

@app.post("/api/filtered-kol-data")
async def get_filtered_kol_data(request: Request):
    """根據時間範圍和KOL ID列表篩選KOL數據"""
    try:
        data = await request.json()

        # 獲取請求參數
        time_range = data.get("time_range", {})
        kol_ids = data.get("kol_ids", ["All"])
        query = data.get("query", "")

        # 檢查時間範圍
        start_time = time_range.get("start_time")
        end_time = time_range.get("end_time")
        if start_time is None or end_time is None:
            return JSONResponse({"error": "缺少時間範圍參數"}, status_code=400)

        # 記錄篩選條件日誌 (直接使用時間戳記錄)
        print(f"篩選條件: 時間={start_time}~{end_time}, KOL={kol_ids}")

        # 獲取KOL數據
        kol_data = get_cached_kol_data(force_refresh=False)
        if kol_data is None:
            return JSONResponse({"error": "無法獲取KOL數據"}, status_code=500)
        print(f"原始數據: {len(kol_data)}筆")

        # 獲取KOL映射數據
        kol_records = get_kol_mapping_records()

        # 使用pandas處理數據
        import pandas as pd

        # 將數據轉為DataFrame
        data_df = pd.DataFrame(kol_data)
        if data_df.empty:
            # 轉換時間範圍為可讀格式用於響應
            start_dt_utc8 = datetime.fromtimestamp(start_time, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))
            end_dt_utc8 = datetime.fromtimestamp(end_time, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))

            return JSONResponse({
                "records": [],
                "total_count": 0,
                "filter_info": {
                    "time_range": {
                        "start_time": start_time,
                        "end_time": end_time,
                        "start_time_utc8": start_dt_utc8.strftime("%Y-%m-%d %H:%M:%S"),
                        "end_time_utc8": end_dt_utc8.strftime("%Y-%m-%d %H:%M:%S")
                    },
                    "kol_ids": kol_ids,
                    "query": query
                }
            })

        # 確保時間戳為數值型
        if 'timestamp' in data_df.columns:
            data_df['timestamp'] = pd.to_numeric(data_df['timestamp'], errors='coerce')
            data_df = data_df.dropna(subset=['timestamp'])
            print(f"有效時間戳數據: {len(data_df)}筆")

        # 1. 先進行KOL篩選
        if "All" not in kol_ids and 'kol_id' in data_df.columns:
            before_count = len(data_df)
            data_df = data_df[data_df['kol_id'].isin(kol_ids)]
            print(f"KOL篩選: {before_count} -> {len(data_df)}筆")

        # 2. 再進行時間戳篩選
        if 'timestamp' in data_df.columns:
            before_count = len(data_df)
            data_df = data_df[(data_df['timestamp'] >= start_time) & (data_df['timestamp'] <= end_time)]
            print(f"時間篩選: {before_count} -> {len(data_df)}筆")

        # 注意：根據用戶要求，移除了關鍵詞篩選的代碼段

        # KOL名稱映射
        kol_df = pd.DataFrame(kol_records)
        if not kol_df.empty:
            # 嘗試各種欄位名稱組合
            mapping_success = False
            for col_pair in [("KOL_ID", "KOL"), ("kol_id", "kol"), ("id", "name")]:
                if col_pair[0] in kol_df.columns and col_pair[1] in kol_df.columns:
                    kol_mapping_df = kol_df[[col_pair[0], col_pair[1]]].rename(
                        columns={col_pair[0]: "kol_id", col_pair[1]: "kol_name"}
                    )
                    if 'kol_id' in data_df.columns:
                        data_df = data_df.merge(kol_mapping_df, on="kol_id", how="left")
                        data_df["kol_name"] = data_df["kol_name"].fillna(data_df["kol_id"])
                        mapping_success = True
                        print(f"使用 {col_pair[0]}/{col_pair[1]} 列進行KOL映射")
                        break

            if not mapping_success:
                print("未找到匹配的KOL映射欄位")

        # 如果沒有kol_name列，則從kol_id創建
        if 'kol_id' in data_df.columns and 'kol_name' not in data_df.columns:
            data_df["kol_name"] = data_df["kol_id"]
            print("使用kol_id作為kol_name的替代")

        # 3. 篩選完成後，最後才格式化時間
        if 'timestamp' in data_df.columns:
            def format_timestamp(ts):
                if pd.isna(ts):
                    return ""
                try:
                    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                    dt = dt.astimezone(timezone(timedelta(hours=8)))
                    return dt.strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    return str(ts)

            data_df["created_time"] = data_df["timestamp"].apply(format_timestamp)

        # 處理缺失值並按時間戳降序排序
        data_df = data_df.fillna("")
        if 'timestamp' in data_df.columns:
            data_df = data_df.sort_values("timestamp", ascending=False)

        # 選擇需要的列
        columns = ["doc_id", "kol_name", "created_time", "post_url", "content", "reaction_count", "share_count"]
        for col in columns:
            if col not in data_df.columns:
                data_df[col] = ""

        # 轉換為字典列表
        filtered_data = data_df[columns].to_dict(orient="records")
        print(f"篩選後: {len(filtered_data)}筆記錄")

        # 轉換時間範圍為可讀格式用於響應
        start_dt_utc8 = datetime.fromtimestamp(start_time, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))
        end_dt_utc8 = datetime.fromtimestamp(end_time, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))

        # 構建響應數據
        response_data = {
            "records": filtered_data,
            "filter_info": {
                "time_range": {
                    "start_time": start_time,
                    "end_time": end_time,
                    "start_time_utc8": start_dt_utc8.strftime("%Y-%m-%d %H:%M:%S"),
                    "end_time_utc8": end_dt_utc8.strftime("%Y-%m-%d %H:%M:%S")
                },
                "kol_ids": kol_ids,
                "query": query
            },
            "total_count": len(filtered_data)
        }

        return JSONResponse(response_data)

    except Exception as e:
        print(f"篩選KOL數據時出錯: {str(e)}")
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/api/messages")
async def get_messages(since: str = None, session_id: str = "default"):
    """
    獲取消息歷史，可選指定自特定ID之後的消息。
    用於前端輪詢新消息。

    參數:
    - since: 指定從哪個消息ID之後開始獲取
    - session_id: 會話ID，默認為"default"
    """
    global _messages

    write_log("="*50)
    write_log(f"獲取消息請求 (session_id: {session_id})")

    # 確保該session_id的消息列表存在
    with _message_lock:
        if session_id not in _messages:
            _messages[session_id] = []

        user_messages = _messages[session_id]
        write_log(f"當前session消息總數: {len(user_messages)}")
        write_log(f"since參數: {since}")

        if not since:
            # 如果沒有指定 since，返回最後 10 條消息
            result = user_messages[-10:] if user_messages else []
            write_log(f"未指定since，返回最後 {len(result)} 條消息")
        else:
            # 找到 since 對應的消息的索引
            since_index = -1
            for i, msg in enumerate(user_messages):
                if msg["id"] == since:
                    since_index = i
                    break

            # 返回 since 之後的消息
            if since_index != -1:
                result = user_messages[since_index + 1:]
                write_log(f"找到 since 索引 {since_index}，返回後續 {len(result)} 條消息")
            else:
                # 如果找不到指定的 ID，返回最後 10 條消息
                result = user_messages[-10:] if user_messages else []
                write_log(f"未找到 since ID，返回最後 {len(result)} 條消息")

    write_log("獲取消息請求完成")
    write_log("="*50)
    return JSONResponse({"messages": result})

# 修改清空消息函數
@app.post("/api/clear_messages")
async def clear_messages(session_id: str = "default"):
    """清空指定會話的所有聊天消息，開始新會話

    參數:
    - session_id: 會話ID，默認為"default"
    """
    global _messages

    try:
        write_log("="*50)
        write_log(f"清空消息請求開始處理 (session_id: {session_id})")

        # 使用鎖來確保線程安全
        with _message_lock:
            # 確認該session_id存在
            if session_id in _messages:
                write_log(f"清空前消息數量: {len(_messages[session_id])}")
                if len(_messages[session_id]) > 0:
                    write_log(f"第一條消息: {_messages[session_id][0]['content'][:50]}...")
                    write_log(f"最後一條消息: {_messages[session_id][-1]['content'][:50]}...")

                # 清空該session的消息
                _messages[session_id] = []
                write_log(f"Session {session_id} 的消息列表已完全清空")
            else:
                # 如果session不存在，創建空列表
                _messages[session_id] = []
                write_log(f"創建了新的session: {session_id}")

        write_log("清空消息操作已成功完成")
        write_log("="*50)

        # 返回清晰的成功響應
        return JSONResponse({
            "status": "success",
            "message": f"All messages cleared for session {session_id}",
            "count": 0
        })
    except Exception as e:
        write_log("="*50)
        write_log(f"清空聊天消息時出錯: {str(e)}")
        traceback.print_exc()
        write_log("="*50)
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/chat_direct_batch")
async def chat_direct_batch(request: Request):
    """
    批量添加訊息到聊天界面，不通過 LLM。
    用於一次性添加多個消息，減少API請求次數。

    期望的請求格式：
    {
        "messages": [
            {
                "role": "user" | "bot",
                "content": "訊息內容1",
                "metadata": { "query": "查詢字串" } // 可選
            },
            {
                "role": "user" | "bot",
                "content": "訊息內容2",
                "metadata": { "query": "查詢字串" } // 可選
            },
            ...
        ],
        "session_id": "用戶的會話ID，可選" // 新增
    }
    """
    global _messages, _message_id_counter

    try:
        req_data = await request.json()
        messages = req_data.get("messages", [])
        session_id = req_data.get("session_id", "default")  # 獲取session_id，默認為"default"

        write_log("="*50)
        write_log(f"批量添加消息 (session_id: {session_id}): {len(messages)} 條")

        if not isinstance(messages, list):
            write_log("錯誤: 請求格式不正確，應為消息數組")
            return JSONResponse({"error": "請求格式不正確，應為消息數組"}, status_code=400)

        if len(messages) == 0:
            write_log("錯誤: 消息數組為空")
            return JSONResponse({"error": "消息數組不能為空"}, status_code=400)

        added_messages = []

        # 添加每條消息
        for msg_data in messages:
            if not isinstance(msg_data, dict):
                continue

            role = msg_data.get("role")
            if role not in ["user", "bot"]:
                continue

            content = msg_data.get("content")
            if content is None:
                continue

            metadata = msg_data.get("metadata", {})

            # 創建新的消息 ID
            with _message_lock:
                _message_id_counter += 1
                msg_id = f"{int(time.time() * 1000)}_{_message_id_counter}"

            # 創建消息對象
            message = {
                "id": msg_id,
                "role": role,
                "content": content,
                "timestamp": datetime.now().strftime("%H:%M"),
                "metadata": metadata
            }

            added_messages.append(message)

        # 批量添加所有有效消息
        with _message_lock:
            # 確保該session_id的消息列表存在
            if session_id not in _messages:
                _messages[session_id] = []

            _messages[session_id].extend(added_messages)
            message_count = len(_messages[session_id])

        write_log(f"已添加 {len(added_messages)} 條有效消息")
        write_log(f"當前消息總數: {message_count}")
        write_log("="*50)

        return JSONResponse({
            "status": "success",
            "count": len(added_messages),
            "ids": [msg["id"] for msg in added_messages]
        })

    except Exception as e:
        write_log("="*50)
        write_log(f"批量添加消息時出錯: {str(e)}")
        traceback.print_exc()
        write_log("="*50)
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/gemini_analysis")
async def analyze_data_with_gemini(request: Request):
    """分析表格數據並提供見解"""
    try:
        req_data = await request.json()
        records = req_data.get("data", req_data.get("records"))  # 嘗試從 data 或 records 字段獲取數據
        query = req_data.get("query", "")
        session_id = req_data.get("session_id", "default")  # 獲取session_id，默認為"default"

        if not records:
            return JSONResponse({"error": "未提供記錄數據"}, status_code=400)

        # 獲取API密鑰
        gemini_key = get_gemini_api_key()
        if not gemini_key:
            return JSONResponse({
                "error": f"未設置Google API密鑰，無法使用 {GEMINI_MODEL} 進行分析。請檢查環境變量。"
            }, status_code=503)

        try:
            # 配置API密鑰
            genai.configure(api_key=gemini_key)
            model = GenerativeModel(GEMINI_MODEL)

            # 創建聊天會話
            chat = model.start_chat(history=[])

            # 準備提示詞
            system_prompt = """你是一個專業的數據分析師，擅長分析網路社群數據。
當用戶提供數據時，請分析這些數據並提供專業見解。當用戶提出特定問題時，直接回答他們的問題。

請注意以下要點：
1. 回答應該簡潔但有洞察力
2. 識別數據中的關鍵趨勢和模式
3. 不要重複用戶已經知道的信息
4. 如果數據不足以得出結論，請誠實說明
5. 使用繁體中文回答

如果用戶沒有提出特定問題，請分析並突出表格數據中最重要的洞察。
"""
            # 將查詢與數據結合
            prompt_parts = []
            prompt_parts.append(system_prompt)

            # 添加查詢(如果有)
            if query:
                prompt_parts.append(f"\n用戶問題: {query}\n")
            else:
                prompt_parts.append("\n請分析以下數據並提供最重要的洞察:\n")

            # 添加數據
            data_str = json.dumps(records, ensure_ascii=False, indent=2)
            prompt_parts.append(f"數據 (JSON格式):\n{data_str}")

            # 發送系統提示
            full_prompt = "\n".join(prompt_parts)
            response = chat.send_message(full_prompt)

            # 創建消息對象
            with _message_lock:
                _message_id_counter += 1
                msg_id = f"{int(time.time() * 1000)}_{_message_id_counter}"

            # 創建分析結果消息
            analysis_message = {
                "id": msg_id,
                "role": "bot",
                "content": response.text,
                "timestamp": datetime.now().strftime("%H:%M"),
                "metadata": {"query": query}
            }

            # 添加消息到會話歷史
            with _message_lock:
                # 確保該session_id的消息列表存在
                if session_id not in _messages:
                    _messages[session_id] = []

                _messages[session_id].append(analysis_message)

            return JSONResponse({"response": response.text, "message_id": msg_id})
        except Exception as e:
            error_message = f"處理 {GEMINI_MODEL} 分析時出錯: {str(e)}。可能是API配額限制或格式異常。"
            write_log(error_message)
            return JSONResponse({"error": error_message}, status_code=500)
    except Exception as e:
        error_message = str(e)
        write_log(f"分析數據時出錯: {error_message}")
        return JSONResponse({"error": error_message}, status_code=500)
