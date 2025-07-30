// import { useState, useCallback } from 'react';
// import { SavedSearch, SearchResult } from '../types';

// export const useSearchProcessing = (apiUrl: string) => {
//   const [isProcessing, setIsProcessing] = useState(false);
//   const [processingError, setProcessingError] = useState<string | null>(null);

//   const executeSearch = useCallback(async (title: string, sessionId: string): Promise<SearchResult> => {
//     console.debug('[useSearchProcessing] 開始執行搜索', title);
//     setIsProcessing(true);
//     setProcessingError(null);

//     try {
//       const response = await fetch(`${apiUrl}/api/search/execute?session_id=${sessionId}`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ title }),
//       });

//       if (!response.ok) {
//         const errorText = await response.text();
//         throw new Error(`Search execution failed: ${response.status} ${errorText}`);
//       }

//       const result = await response.json();
//       console.debug('[useSearchProcessing] 搜索執行成功', result);
//       return result;
//     } catch (error) {
//       console.error('[useSearchProcessing] 執行搜索失敗:', error);
//       setProcessingError(error instanceof Error ? error.message : 'Unknown error');
//       throw error;
//     } finally {
//       setIsProcessing(false);
//     }
//   }, [apiUrl]);

//   const cancelProcessing = useCallback(() => {
//     console.debug('[useSearchProcessing] 取消搜索處理');
//     setIsProcessing(false);
//     setProcessingError(null);
//   }, []);

//   return {
//     isProcessing,
//     processingError,
//     executeSearch,
//     cancelProcessing,
//   };
// };

export {};
