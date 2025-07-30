import { useState, useEffect } from 'react';
import { fetchWithKey } from './fetchWithKey';

export const useBackendStatus = (apiUrl: string, checkInterval = 5000, maxRetries = 24) => {
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [retryCount, setRetryCount] = useState(0);

  useEffect(() => {
    let isMounted = true;
    let timerId: ReturnType<typeof setTimeout> | null = null;

    const checkBackendStatus = async () => {
      if (!isMounted) return;

      try {
        // 创建自定义超时控制器，替代 AbortSignal.timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 3000);

        const response = await fetchWithKey(`${apiUrl}/ping`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (response.ok) {
          setIsLoading(false);
          setIsError(false);
          setRetryCount(0);
        } else {
          if (retryCount < maxRetries) {
            setRetryCount(prev => prev + 1);
            timerId = setTimeout(checkBackendStatus, checkInterval);
          } else {
            setIsLoading(false);
            setIsError(true);
          }
        }
      } catch (error) {
        console.error('Backend status check failed:', error);
        if (retryCount < maxRetries && isMounted) {
          setRetryCount(prev => prev + 1);
          timerId = setTimeout(checkBackendStatus, checkInterval);
        } else if (isMounted) {
          setIsLoading(false);
          setIsError(true);
        }
      }
    };

    // Initial check
    checkBackendStatus();

    return () => {
      isMounted = false;
      if (timerId) clearTimeout(timerId);
    };
  }, [apiUrl, checkInterval, maxRetries, retryCount]);

  return { isLoading, isError, retryCount };
};
