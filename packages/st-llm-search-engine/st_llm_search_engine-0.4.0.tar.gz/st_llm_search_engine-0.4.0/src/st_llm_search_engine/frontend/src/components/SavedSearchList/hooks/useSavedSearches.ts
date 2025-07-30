import { useState, useCallback, useRef } from 'react';
import type { SavedSearch } from '../types';
import { getSessionId } from '../../../utils/session';
import { fetchWithKey, API_URL } from '../../../utils/fetchWithKey';

export const useSavedSearches = (sessionIdProp: string) => {
  const sessionId = getSessionId(sessionIdProp);
  console.debug('[useSavedSearches] hook called, sessionId:', sessionId);
  const [searches, setSearches] = useState<SavedSearch[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const requestSeq = useRef(0);

  // 直接追蹤當前的搜索列表，避免閉包問題
  const searchesRef = useRef<SavedSearch[]>([]);

  // 當 searches 發生變化時，更新 searchesRef
  const updateSearchesRef = (newSearches: SavedSearch[]) => {
    searchesRef.current = newSearches;
    setSearches(newSearches);
    console.debug('[updateSearchesRef] 更新引用，新搜索列表長度:', newSearches.length);
  };

  // 提取排序邏輯為單獨的函數
  const sortSearches = useCallback((searches: SavedSearch[]) => {
    const sorted = [...searches].sort((a, b) => {
      if (a.account === "系統" && b.account !== "系統") return -1;
      if (a.account !== "系統" && b.account === "系統") return 1;
      return a.order - b.order;
    });
    console.debug('[sortSearches] sorted:', sorted);
    return sorted;
  }, []);

  // fetchSavedSearches 改為普通 async function
  async function fetchSavedSearches(force = false) {
    if (isLoading && !force || !sessionId) {
      return;
    }
    const seq = ++requestSeq.current;
    try {
      setIsLoading(true);
      setError(null);
      const response = await fetchWithKey(`${API_URL}/api/saved_search?session_id=${sessionId}`);
      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }
      const data = await response.json();
      let arr: SavedSearch[] = Array.isArray(data) ? data : (Array.isArray(data.searches) ? data.searches : []);
      if (seq === requestSeq.current) {
        const sortedArr = sortSearches(arr);
        updateSearchesRef(sortedArr);
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to fetch saved searches');
    } finally {
      setIsLoading(false);
    }
  }

  // 改進的 saveSearch 函數，直接返回新的搜索數據
  const saveSearch = useCallback(async (search: Omit<SavedSearch, 'id' | 'createdAt'>): Promise<SavedSearch | null> => {
    if (isLoading) return null;
    if (!sessionId) return null;
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetchWithKey(`${API_URL}/api/saved_search?session_id=${sessionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: search.title || "",
          time: search.query.time ?? 1,
          source: search.query.source ?? 0,
          tags: Array.isArray(search.query.tags) ? search.query.tags : ["All"],
          query: search.query.query || "",
          n: search.query.n ?? "",
          range: search.query.range ?? null
        }),
      });
      if (!response.ok) throw new Error(`Failed to save search: ${response.status}`);
      const responseData = await response.json();
      let newSearch: SavedSearch | null = null;
      if (responseData && typeof responseData === 'object' && responseData.id) {
        newSearch = responseData as SavedSearch;
        // 直接 append 到 state
        const updated = sortSearches([...searchesRef.current, newSearch]);
        updateSearchesRef(updated);
        // 新增空訊息
        await fetchWithKey(`${API_URL}/api/message?session_id=${sessionId}&search_id=${newSearch.id}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ role: 'bot', content: '' }),
        });
      }
      return newSearch;
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to save search');
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, sortSearches, isLoading, updateSearchesRef, searchesRef]);

  const deleteSearch = useCallback(async (id: number) => {
    if (isLoading || !sessionId) return;
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetchWithKey(`${API_URL}/api/saved_search?session_id=${sessionId}&search_id=${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error(`Failed to delete search: ${response.status}`);
      const updatedSearches = sortSearches(searchesRef.current.filter(s => s.id !== id));
      updateSearchesRef(updatedSearches);
      setTimeout(() => { fetchSavedSearches(true); }, 100);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to delete search');
      await fetchSavedSearches(true);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, fetchSavedSearches, sortSearches, isLoading]);

  const reorderSearches = useCallback(async (startIndex: number, endIndex: number) => {
    if (isLoading || !sessionId) return;
    const newSearches = [...searchesRef.current];
    const [removed] = newSearches.splice(startIndex, 1);
    newSearches.splice(endIndex, 0, removed);
    const updatedSearches = newSearches.map((search, index) => ({ ...search, order: index }));
    const sortedSearches = sortSearches(updatedSearches);
    updateSearchesRef(sortedSearches);
    try {
      setIsLoading(true);
      await Promise.all(
        sortedSearches.map(search =>
          fetchWithKey(`${API_URL}/api/saved_search?session_id=${sessionId}&search_id=${search.id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ order: search.order })
          })
        )
      );
    } catch (err) {
      await fetchSavedSearches(true);
    } finally {
      setIsLoading(false);
    }
  }, [sortSearches, sessionId, fetchSavedSearches, isLoading]);

  const clearSearches = useCallback(async () => {
    console.log('[clearSearches] called');
    console.log('[clearSearches] isLoading:', isLoading, 'sessionId:', sessionId);
    console.log('[clearSearches] searchesRef.current:', searchesRef.current);
    const userSearchIds = searchesRef.current.filter(search => search.account !== '系統').map(search => search.id);
    console.log('[clearSearches] userSearchIds:', userSearchIds);
    if (isLoading || !sessionId) return;
    setIsLoading(true);
    setError(null);
    try {
      if (userSearchIds.length === 0) {
        console.log('[clearSearches] userSearchIds is empty, nothing to delete');
        return;
      }
      for (const id of userSearchIds) {
        console.log(`[clearSearches] DELETE /api/saved_search?session_id=${sessionId}&search_id=${id}`);
        await fetchWithKey(`${API_URL}/api/saved_search?session_id=${sessionId}&search_id=${id}`, {
          method: 'DELETE',
        });
      }
      const updatedSearches = sortSearches(searchesRef.current.filter(s => s.account === '系統'));
      updateSearchesRef(updatedSearches);
      await fetchSavedSearches(true);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to clear searches');
      await fetchSavedSearches(true);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, fetchSavedSearches, sortSearches, isLoading]);

  const updateSearch = useCallback(async (id: number, updatedData: Partial<SavedSearch>) => {
    if (isLoading || !sessionId) return;
    setIsLoading(true);
    setError(null);
    try {
      // 先發送 PATCH 請求
      const response = await fetchWithKey(`${API_URL}/api/saved_search?session_id=${sessionId}&search_id=${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedData),
      });

      if (!response.ok) {
        throw new Error(`Failed to update search: ${response.status}`);
      }

      // 從響應中獲取更新後的數據
      const updatedSearchData = await response.json();
      console.debug('[updateSearch] 後端返回的更新數據:', updatedSearchData);

      // 使用後端返回的數據更新前端狀態
      const updatedSearches = sortSearches(
        searchesRef.current.map(s => {
          if (s.id !== id) return s;

          // 直接用後端返回的完整數據替換
          if (updatedSearchData && typeof updatedSearchData === 'object') {
            return {
              ...s,
              ...updatedSearchData,
              // 如果 query 在回應中存在，則使用它，否則保持原樣
              query: updatedSearchData.query || s.query
            };
          }

          // 後備方案：手動合併數據
          // merge updatedData into s.query for query-related fields
          const newQuery = { ...s.query };
          if (updatedData.query) {
            Object.assign(newQuery, updatedData.query);
          } else {
            ['time', 'source', 'tags', 'query', 'n', 'range'].forEach(key => {
              if (key in updatedData) {
                newQuery[key] = (updatedData as any)[key];
              }
            });
          }

          return {
            ...s,
            title: updatedData.title ?? s.title,
            query: newQuery
          };
        })
      );

      updateSearchesRef(updatedSearches);
      console.debug('[updateSearch] 前端狀態已更新');
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to update search');
      await fetchSavedSearches(true);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, fetchSavedSearches, sortSearches, isLoading]);

  return {
    searches,
    isLoading,
    error,
    fetchSavedSearches,
    saveSearch,
    deleteSearch,
    reorderSearches,
    clearSearches,
    updateSearch,
  };
};
