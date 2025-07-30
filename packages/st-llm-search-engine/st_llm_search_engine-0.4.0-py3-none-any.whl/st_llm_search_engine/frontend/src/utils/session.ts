/**
 * 取得 sessionId，優先用傳入值，其次 sessionStorage，最後自動 call API 拿（需外部補上）。
 * @param sessionIdProp 可選，外部傳入 sessionId
 * @returns sessionId string
 */
export function getSessionId(sessionIdProp?: string): string {
    if (sessionIdProp) {
      console.debug('[getSessionId] 用 sessionIdProp:', sessionIdProp);
      return sessionIdProp;
    }
    if (typeof window !== 'undefined' && window.sessionStorage) {
      let id = window.sessionStorage.getItem('session_id');
      if (id) {
        console.debug('[getSessionId] 用 sessionStorage:', id);
        return id;
      }
      console.debug('[getSessionId] sessionStorage 沒有 session_id');
    }
    console.debug('[getSessionId] 回傳空字串');
    return '';
  }
