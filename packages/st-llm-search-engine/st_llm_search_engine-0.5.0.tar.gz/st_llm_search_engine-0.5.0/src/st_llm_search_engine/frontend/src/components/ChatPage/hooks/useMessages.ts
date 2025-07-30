import { useState, useEffect, useCallback } from 'react';
import { Message, MessageCache } from '../types';
import { fetchWithKey } from '../../../utils/fetchWithKey';

// 在內存中存儲消息快取，而非使用 sessionStorage
// 這樣每個標籤頁都有自己的內存快取，不會相互影響
const messageCache: Record<string, MessageCache> = {};
const CACHE_EXPIRY = 24 * 60 * 60 * 1000; // 1 天過期

export const useMessages = (
  apiUrl: string,
  sessionId: string,
  searchId: string
) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isThinking, setIsThinking] = useState(false);

  // 生成快取鍵
  const getCacheKey = useCallback(() => {
    return `${sessionId}-${searchId}`;
  }, [sessionId, searchId]);

  // 加載消息
  const loadMessages = useCallback(async (forceRefresh = false) => {
    const cacheKey = getCacheKey();
    console.debug(`[useMessages] 嘗試加載消息，sessionId=${sessionId}, searchId=${searchId}, forceRefresh=${forceRefresh}`);

    // 嘗試從內存快取加載
    const loadFromCache = () => {
      if (forceRefresh) return false;

      const cachedData = messageCache[cacheKey];
      if (cachedData) {
        try {
          if (Date.now() - cachedData.timestamp < CACHE_EXPIRY) {
            console.debug(`[useMessages] 從內存快取加載 ${cachedData.messages.length} 條消息`);
            setMessages(cachedData.messages);
            return true;
          }
        } catch (e) {
          console.error("[useMessages] 快取解析錯誤:", e);
        }
      }
      return false;
    };

    // 如果無法從快取加載，則從 API 加載
    if (!loadFromCache()) {
      try {
        setIsLoading(true);
        setError('');

        console.debug(`[useMessages] 從 API 加載消息: ${apiUrl}/api/message?session_id=${sessionId}&search_id=${searchId}`);
        const response = await fetchWithKey(
          `${apiUrl}/api/message?session_id=${sessionId}&search_id=${searchId}`
        );

        console.debug(`[useMessages] API 響應狀態: ${response.status}`);

        if (response.ok) {
          const data = await response.json();
          console.debug(`[useMessages] API 返回數據:`, data);

          // 確保我們處理的是數組
          const messageArray = Array.isArray(data) ? data : [];

          const formattedMessages = messageArray.map((msg: any) => ({
            id: msg.id.toString(),
            role: msg.role as "user" | "bot",
            content: msg.content,
            created_at: msg.created_at
          }));

          console.debug(`[useMessages] 格式化後 ${formattedMessages.length} 條消息`);
          setMessages(formattedMessages);

          // 更新快取
          updateCache(formattedMessages);
        } else {
          console.error(`[useMessages] 加載消息失敗: ${response.status}`);
          setError("無法加載對話歷史");
        }
      } catch (e) {
        console.error("[useMessages] API 錯誤:", e);
        setError("連接失敗，請檢查網絡");
      } finally {
        setIsLoading(false);
      }
    }
  }, [apiUrl, sessionId, searchId, getCacheKey]);

  // 更新快取
  const updateCache = useCallback((messagesData: Message[]) => {
    const cacheKey = getCacheKey();
    console.debug(`[useMessages] 更新內存快取，${messagesData.length} 條消息`);

    // 更新內存快取
    messageCache[cacheKey] = {
      messages: messagesData,
      timestamp: Date.now()
    };
  }, [getCacheKey]);

  // 發送用戶消息
  const sendUserMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    try {
      setError('');
      // 先建立並顯示用戶消息 (樂觀 UI 更新)
      const newUserMsg: Message = {
        id: `temp-${Date.now()}`,
        role: "user",
        content,
        created_at: new Date().toISOString()
      };

      console.debug(`[useMessages] 準備發送用戶消息: ${content}`);

      // 使用函數式更新確保使用最新狀態
      setMessages(prevMessages => [...prevMessages, newUserMsg]);

      // 發送到 API，按照技術文件的要求
      console.debug(`[useMessages] 調用 API: ${apiUrl}/api/message?session_id=${sessionId}&search_id=${searchId}`);
      const response = await fetchWithKey(
        `${apiUrl}/api/message?session_id=${sessionId}&search_id=${searchId}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ role: 'user', content })
        }
      );

      console.debug(`[useMessages] API 響應狀態: ${response.status}`);

      if (response.ok) {
        const data = await response.json();
        console.debug(`[useMessages] API 返回數據:`, data);

        // 用 API 返回的真實消息替換臨時消息
        setMessages(prevMessages => {
          const updatedMessages = prevMessages.map(msg =>
            msg.id === newUserMsg.id ? {
              id: data.id.toString(),
              role: data.role as "user" | "bot",
              content: data.content,
              created_at: data.created_at
            } : msg
          );

          // 更新快取
          updateCache(updatedMessages);
          return updatedMessages;
        });

        // 獲取 AI 回應，符合技術文件 4.1 的要求
        await getLLMResponse(content);
      } else {
        console.error(`[useMessages] 發送消息失敗: ${response.status}`);
        setError("訊息發送失敗，請重新發送或通知開發人員");
        // 移除臨時消息
        setMessages(prevMessages => prevMessages.filter(msg => msg.id !== newUserMsg.id));
      }
    } catch (e) {
      console.error("[useMessages] 發送消息錯誤:", e);
      setError("網絡錯誤，請稍後再試");
    }
  }, [apiUrl, sessionId, searchId, updateCache]);

  // 獲取 AI 回應，新增 query 參數以符合技術文件
  const getLLMResponse = useCallback(async (query?: string) => {
    try {
      setIsThinking(true);

      // 獲取 LLM 回應，添加 query 參數如果存在
      const queryParam = query ? `&query=${encodeURIComponent(query)}` : '';
      const llmUrl = `${apiUrl}/api/message/llm?session_id=${sessionId}&search_id=${searchId}${queryParam}`;

      console.debug(`[useMessages] 獲取 LLM 回應: ${llmUrl}`);
      const llmResponse = await fetchWithKey(llmUrl);

      console.debug(`[useMessages] LLM 響應狀態: ${llmResponse.status}`);

      if (llmResponse.ok) {
        const llmData = await llmResponse.json();
        console.debug(`[useMessages] LLM 返回數據:`, llmData);

        const botContent = typeof llmData.content === 'string' ? llmData.content :
                           typeof llmData === 'string' ? llmData :
                           JSON.stringify(llmData);

        console.debug(`[useMessages] 處理後的 LLM 內容: ${botContent.substring(0, 50)}...`);

        // 將 LLM 回應保存為消息
        console.debug(`[useMessages] 保存 bot 消息: ${apiUrl}/api/message?session_id=${sessionId}&search_id=${searchId}`);
        const botResponse = await fetchWithKey(
          `${apiUrl}/api/message?session_id=${sessionId}&search_id=${searchId}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role: 'bot', content: botContent })
          }
        );

        console.debug(`[useMessages] 保存 bot 消息響應狀態: ${botResponse.status}`);

        if (botResponse.ok) {
          const botData = await botResponse.json();
          console.debug(`[useMessages] 保存 bot 消息返回數據:`, botData);

          // 添加 bot 消息到列表，使用函數式更新確保使用最新狀態
          setMessages(prevMessages => {
            const updatedMessages = [...prevMessages, {
              id: botData.id.toString(),
              role: "bot" as const,
              content: botData.content,
              created_at: botData.created_at
            }];

            // 更新快取
            updateCache(updatedMessages);
            return updatedMessages;
          });

        } else {
          console.error(`[useMessages] AI 回應處理失敗: ${botResponse.status}`);
          setError("AI 回應處理失敗");
        }
      } else {
        console.error(`[useMessages] AI 回應獲取失敗: ${llmResponse.status}`);
        setError("AI 回應獲取失敗");
      }
    } catch (e) {
      console.error("[useMessages] LLM 回應錯誤:", e);
      setError("AI 回應獲取失敗");
    } finally {
      setIsThinking(false);
    }
  }, [apiUrl, sessionId, searchId, updateCache]);

  // 清除錯誤
  const clearError = useCallback(() => {
    setError('');
  }, []);

  // 初始加載
  useEffect(() => {
    console.debug(`[useMessages] 初始化 hook，sessionId=${sessionId}, searchId=${searchId}`);
    loadMessages();
  }, [loadMessages]);

  // 檢測快取與後端數據一致性
  const validateCache = useCallback(() => {
    // 這個函數可以用來檢查快取數據結構是否與後端一致
    // 如果檢測到不一致，可以調用 loadMessages(true) 強制刷新
    console.debug(`[useMessages] 驗證快取，sessionId=${sessionId}, searchId=${searchId}`);
    loadMessages(true);
  }, [loadMessages]);

  // 當 sessionId 變更時強制刷新
  useEffect(() => {
    console.debug(`[useMessages] sessionId 變更，強制刷新`);
    loadMessages(true);
  }, [sessionId]);

  return {
    messages,
    isLoading,
    isThinking,
    error,
    sendUserMessage,
    clearError,
    refreshMessages: () => loadMessages(true),
    validateCache
  };
};
