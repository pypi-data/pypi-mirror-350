import React, { useState, useEffect } from 'react';
import { getSessionId } from '../../utils/session';
import { ChatPageProps } from './types';
import MessageList from './components/MessageList';
import MessageInput from './components/MessageInput';
import { useMessages } from './hooks/useMessages';

const ChatPage: React.FC<ChatPageProps> = ({ apiUrl }) => {
  // 每次加載頁面都會獲取新的 sessionId，確保每個標籤頁有獨立的 session
  const [sessionId] = useState<string>(() => getSessionId());
  const [searchId, setSearchId] = useState<string>("999");
  const [input, setInput] = useState("");

  // 從 URL 獲取 searchId (如果有)
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const sid = urlParams.get('search_id');
    if (sid) setSearchId(sid);
    console.debug(`[ChatPage] 初始化頁面，sessionId=${sessionId}, searchId=${searchId || 'none'}`);
  }, []);

  // 記錄 sessionId 到控制台，幫助調試
  useEffect(() => {
    console.debug(`[ChatPage] 當前 sessionId: ${sessionId}`);
  }, [sessionId]);

  // 使用自定義 hook 處理消息
  const {
    messages,
    isLoading,
    isThinking,
    error,
    sendUserMessage,
    clearError,
    refreshMessages,
    validateCache
  } = useMessages(apiUrl, sessionId, searchId);

  // 處理發送消息
  const handleSend = () => {
    if (!input.trim()) return;
    console.debug(`[ChatPage] 發送消息: ${input.substring(0, 30)}...`);
    sendUserMessage(input);
    setInput("");
  };

  // 設置消息內容
  const handleInputChange = (value: string) => {
    setInput(value);
  };

  // 檢查快取數據結構與後端一致性
  useEffect(() => {
    // 每次 search_id 變更時驗證快取
    console.debug(`[ChatPage] searchId 變更，驗證快取: ${searchId}`);
    validateCache();
  }, [searchId, validateCache]);

  // 監聽消息變化
  useEffect(() => {
    console.debug(`[ChatPage] 消息列表更新，現有 ${messages.length} 條消息`);
  }, [messages]);

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      width: "calc(100% - 288px)", // 減去 Sidebar 的寬度
      marginLeft: "288px", // 從 Sidebar 右側開始
      height: "100vh",
      position: "relative",
      background: "#222",
      overflow: "hidden"
    }}>
      {/* 消息列表 */}
      <MessageList
        messages={messages}
        isThinking={isThinking}
        error={error}
        searchId={searchId}
        onErrorClear={clearError}
      />

      {/* 消息輸入框 */}
      <MessageInput
        value={input}
        onChange={handleInputChange}
        onSend={handleSend}
        isThinking={isThinking}
      />
    </div>
  );
};

export default ChatPage;
