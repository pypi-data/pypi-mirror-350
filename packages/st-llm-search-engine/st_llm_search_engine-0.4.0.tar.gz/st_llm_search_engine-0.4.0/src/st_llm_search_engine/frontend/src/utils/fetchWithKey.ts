export const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

/**
 * 帶有自動添加 API Key 的 fetch 函數
 *
 * @param url API 端點 URL
 * @param options fetch 選項
 * @returns fetch response
 */
export async function fetchWithKey(url: string, options: RequestInit = {}) {
  const apiKey = (typeof window !== 'undefined' && window.localStorage.getItem("API_KEY"))
    || (typeof window !== 'undefined' && (window as any).REACT_APP_API_KEY)
    || "";

  const headers = {
    ...(options.headers || {}),
    "x-api-key": apiKey,
  };

  // 預設 30 秒超時，除非有明確的信號
  const controller = new AbortController();
  // 使用自定义超时而不是 AbortSignal.timeout
  const timeoutSignal = options.signal || controller.signal;

  const timeoutId = setTimeout(() => controller.abort(), 30000);

  try {
    const response = await fetch(url, {
      ...options,
      headers,
      signal: timeoutSignal
    });
    return response;
  } catch (error) {
    console.error(`Fetch error for ${url}:`, error);
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}
