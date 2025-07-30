// import { useCallback } from 'react';
// import { SearchResult } from '../types';
// import { formatSearchResultMessage, formatSearchResultJson } from '../utils/messageFormatters';

// export const useMessageHandling = (apiUrl: string) => {
//   const sendSearchResultMessages = useCallback(async (title: string, result: SearchResult, formData: any, sessionId: string) => {
//     try {
//       const messages = [
//         {
//           role: "user",
//           content: `我想查看「${title}」的搜索結果`,
//           metadata: { query: "" }
//         },
//         {
//           role: "bot",
//           content: formatSearchResultMessage(title, result, formData),
//           metadata: { query: "" }
//         },
//         {
//           role: "bot",
//           content: formatSearchResultJson(result),
//           metadata: { query: "" }
//         }
//       ];

//       const response = await fetch(`${apiUrl}/api/chat_direct_batch`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({
//           messages,
//           session_id: sessionId
//         }),
//       });

//       if (!response.ok) {
//         throw new Error('Failed to send messages');
//       }

//       // 觸發搜索完成事件
//       window.dispatchEvent(new CustomEvent('searchProcessingCompleted', {
//         detail: {
//           title,
//           recordCount: result.records.length,
//           eventId: Date.now().toString()
//         }
//       }));

//       return true;
//     } catch (error) {
//       console.error("發送消息失敗:", error);
//       throw error;
//     }
//   }, [apiUrl]);

//   return {
//     sendSearchResultMessages
//   };
// };
