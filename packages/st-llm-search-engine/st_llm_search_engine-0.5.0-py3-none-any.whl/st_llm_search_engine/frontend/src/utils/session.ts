/**
 * 生成一個唯一的 session ID
 * @returns 隨機生成的 UUID
 */
function generateUUID(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

/**
 * 取得 sessionId，使用 sessionStorage 確保同一個標籤頁重新載入時使用相同的 ID
 * @param sessionIdProp 可選，外部傳入 sessionId
 * @returns sessionId string
 */
export function getSessionId(sessionIdProp?: string): string {
  // 1. 如果有外部傳入的 sessionId，則優先使用
  if (sessionIdProp) {
    console.debug('[getSessionId] 用 sessionIdProp:', sessionIdProp);
    return sessionIdProp;
  }

  // 2. 從 sessionStorage 獲取，確保同一個分頁重新載入時使用相同的 ID
  const storedSessionId = sessionStorage.getItem('session_id');
  if (storedSessionId) {
    console.debug('[getSessionId] 用現有的 sessionId:', storedSessionId);
    return storedSessionId;
  }

  // 3. 生成新的 sessionId（只有在新開分頁或首次載入時）
  const newSessionId = generateUUID();
  console.debug('[getSessionId] 生成新的 sessionId:', newSessionId);
  sessionStorage.setItem('session_id', newSessionId);
  return newSessionId;
}
