export const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

/**
 * 帶有自動添加 API Key 的 fetch 函數
 *
 * @param url API 端點 URL
 * @param options fetch 選項
 * @returns fetch response
 */
export async function fetchWithKey(url: string, options: RequestInit = {}) {
  // 嘗試從多個位置獲取 API Key
  // 1. 從 localStorage
  // 2. 從 window 對象
  // 3. 從 .env 文件 (通過 process.env)
  const apiKey = (typeof window !== 'undefined' && window.localStorage.getItem("API_KEY"))
    || (typeof window !== 'undefined' && (window as any).REACT_APP_API_KEY)
    || process.env.REACT_APP_API_KEY
    || "";

  console.debug(`[fetchWithKey] 請求 URL: ${url.split('?')[0]}, 方法: ${options.method || 'GET'}`);

  if (!apiKey) {
    console.warn(`[fetchWithKey] 警告: 未找到 API Key，請求可能會失敗`);
  } else {
    console.debug(`[fetchWithKey] API Key 可用`);
  }

  const headers = {
    ...(options.headers || {}),
    "x-api-key": apiKey,
  };

  // 預設 30 秒超時，除非有明確的信號
  const controller = new AbortController();
  // 使用自定义超时而不是 AbortSignal.timeout
  const timeoutSignal = options.signal || controller.signal;

  const timeoutId = setTimeout(() => {
    console.warn(`[fetchWithKey] 請求超時: ${url}`);
    controller.abort();
  }, 30000);

  try {
    console.debug(`[fetchWithKey] 發送請求...`);
    const response = await fetch(url, {
      ...options,
      headers,
      signal: timeoutSignal
    });

    console.debug(`[fetchWithKey] 收到響應, 狀態: ${response.status}`);
    return response;
  } catch (error) {
    // 檢查是否為 AbortError
    if (error instanceof Error && error.name === 'AbortError') {
      console.error(`[fetchWithKey] 請求被中止 (可能超時): ${url}`);
    } else {
      console.error(`[fetchWithKey] 請求錯誤 (${url}):`, error);
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}
