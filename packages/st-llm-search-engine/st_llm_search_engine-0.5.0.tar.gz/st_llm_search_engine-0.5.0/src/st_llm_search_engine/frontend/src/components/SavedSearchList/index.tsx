import React, { useState, useCallback, useEffect, forwardRef, useImperativeHandle } from 'react';
import { SavedSearch, SearchResult, SearchQuery } from './types';
import { useSavedSearches } from './hooks/useSavedSearches';
// import { useSearchProcessing } from './hooks/useSearchProcessing';
// import { useMessageHandling } from './hooks/useMessageHandling';
import { SearchListHeader } from './components/SearchListHeader';
import { SearchListContent } from './components/SearchListContent';
import { SearchProcessingOverlay } from './components/SearchProcessingOverlay';
import ConfirmModal from '../../components/ConfirmModal';

interface SavedSearchListProps {
  apiUrl: string;
  sessionId: string;
  onEdit: (search: SavedSearch | null, mode: 'edit' | 'view' | 'create') => void;
  onSaveSearch?: (search: Omit<SavedSearch, 'id' | 'createdAt'>) => Promise<void>;
}

// 定義 ref 暴露的方法
export interface SavedSearchListRef {
  handleSaveSearch: (search: Omit<SavedSearch, 'id' | 'createdAt'>) => Promise<SavedSearch | null>;
  handleUpdateSearch: (id: number, updatedData: Partial<SavedSearch>) => Promise<void>;
  handleRefresh: () => Promise<void>;
}

export const SavedSearchList = forwardRef<SavedSearchListRef, SavedSearchListProps>(({
  apiUrl,
  sessionId,
  onEdit,
  onSaveSearch
}, ref) => {
  console.debug('[SavedSearchList] function body, sessionId=', sessionId);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [processingTitle, setProcessingTitle] = useState<string | null>(null);
  const [showClearModal, setShowClearModal] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [initialLoadDone, setInitialLoadDone] = useState(false);
  const [lastSavedSearch, setLastSavedSearch] = useState<SavedSearch | null>(null);
  const [savedSearchCount, setSavedSearchCount] = useState(0);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [searchToDelete, setSearchToDelete] = useState<number | null>(null);

  const {
    searches,
    error,
    fetchSavedSearches,
    saveSearch,
    deleteSearch,
    reorderSearches,
    clearSearches,
    updateSearch
  } = useSavedSearches(sessionId);

  // Debug: render 時印出 searches
  console.debug('[SavedSearchList] render, searches=', searches, 'length=', searches?.length, 'lastSavedSearch=', lastSavedSearch);

  // 檢查搜索數量是否與上次不同，如果不同，打印詳細信息
  useEffect(() => {
    if (searches && searches.length !== savedSearchCount) {
      console.debug('[SavedSearchList] 搜索數量變化! 從', savedSearchCount, '變為', searches.length);
      console.debug('[SavedSearchList] 搜索列表詳情:', JSON.stringify(searches, null, 2));
      setSavedSearchCount(searches.length);
    }
  }, [searches, savedSearchCount]);

  const handleRefresh = useCallback(async () => {
    console.debug('[handleRefresh] 開始強制刷新');
    setIsRefreshing(true);
    try {
      await fetchSavedSearches(true); // 強制刷新
      console.debug('[handleRefresh] 刷新完成');
    } catch (error) {
      console.error('[handleRefresh] 刷新失敗:', error);
    } finally {
      setIsRefreshing(false);
    }
  }, [fetchSavedSearches]);

  const handleSaveSearch = useCallback(
    async (search: Omit<SavedSearch, 'id' | 'createdAt'>) => {
      console.debug('[handleSaveSearch] 開始保存:', search.title);

      try {
        // 記錄操作前的列表長度
        const beforeCount = searches ? searches.length : 0;
        console.debug('[handleSaveSearch] 保存前搜索數量:', beforeCount);
        console.debug('[handleSaveSearch] 保存前搜索列表:', JSON.stringify(searches, null, 2));

        // 直接使用 saveSearch 並獲取結果
        const newSearch = await saveSearch(search);
        console.debug('[handleSaveSearch] saveSearch結果:', newSearch);

        // 保存最後一次保存的搜索，用於後續處理
        if (newSearch) {
          setLastSavedSearch(newSearch);
          console.debug('[handleSaveSearch] 已設置lastSavedSearch:', newSearch);
        }

        // 如果父組件提供了 onSaveSearch 回調，則調用它
        if (onSaveSearch) {
          console.debug('[handleSaveSearch] 調用父組件的 onSaveSearch');
          await onSaveSearch(search);
        }

        return newSearch;
      } catch (error) {
        console.error('[handleSaveSearch] 保存出錯:', error);
        return null;
      }
    },
    [saveSearch, onSaveSearch, searches]
  );

  const handleUpdateSearch = useCallback(
    async (id: number, updatedData: Partial<SavedSearch>) => {
      console.debug('[handleUpdateSearch] 開始更新搜索, ID:', id);
      await updateSearch(id, updatedData);
      console.debug('[handleUpdateSearch] 更新完成，強制刷新UI');
      await handleRefresh();
    },
    [updateSearch, handleRefresh]
  );

  // 暴露方法給父組件
  useImperativeHandle(ref, () => ({
    handleSaveSearch,
    handleUpdateSearch,
    handleRefresh
  }), [handleSaveSearch, handleUpdateSearch, handleRefresh]);

  const handleExecute = (search: SavedSearch) => {
    console.debug('[SavedSearchList] handleExecute search=', search);
    // 左鍵點擊不進行任何操作
    // onEdit(search, 'edit');
    // executeSearch(search);
  };

  const handleView = (search: SavedSearch) => {
    console.debug('[SavedSearchList] handleView search=', search);
    onEdit(search, 'view');
  };

  const handleReorder = useCallback((fromIndex: number, toIndex: number) => {
    reorderSearches(fromIndex, toIndex);
  }, [reorderSearches]);

  const handleDelete = useCallback(async (id: number) => {
    console.debug('[handleDelete] 開始刪除搜索, ID:', id);
    setSearchToDelete(id);
    setDeleteConfirmOpen(true);
    console.debug('[handleDelete] setSearchToDelete:', id, 'setDeleteConfirmOpen: true');
  }, []);

  const handleConfirmDelete = useCallback(async () => {
    console.debug('[handleConfirmDelete] searchToDelete:', searchToDelete, 'deleteConfirmOpen:', deleteConfirmOpen, 'isLoading:', isLoading);
    if (searchToDelete === null) {
      console.warn('[handleConfirmDelete] searchToDelete is null, abort');
      return;
    }

    console.debug('[handleConfirmDelete] 確認刪除, ID:', searchToDelete);
    setDeleteConfirmOpen(false);

    try {
      await deleteSearch(searchToDelete);
      console.debug('[handleConfirmDelete] 刪除成功');
      setTimeout(() => {
        handleRefresh();
      }, 100);
    } catch (error) {
      console.error('[handleConfirmDelete] 刪除失敗:', error);
    } finally {
      setSearchToDelete(null);
      console.debug('[handleConfirmDelete] setSearchToDelete: null');
    }
  }, [searchToDelete, deleteSearch, handleRefresh, deleteConfirmOpen, isLoading]);

  const handleCancelDelete = useCallback(() => {
    console.debug('[handleCancelDelete] 取消刪除');
    setDeleteConfirmOpen(false);
    setSearchToDelete(null);
    console.debug('[handleCancelDelete] setDeleteConfirmOpen: false, setSearchToDelete: null');
  }, []);

  const handleClear = useCallback(() => {
    setShowClearModal(true);
  }, []);

  const handleConfirmClear = useCallback(async () => {
    setShowClearModal(false);
    try {
      await clearSearches();
      setLastSavedSearch(null);
      console.debug('[handleConfirmClear] 清空完成');
    } catch (error) {
      console.error('清空搜索失敗:', error);
    }
  }, [clearSearches]);

  const handleCancelClear = useCallback(() => {
    setShowClearModal(false);
  }, []);

  // 只在組件掛載時加載一次數據
  useEffect(() => {
    console.debug('[SavedSearchList] useEffect初始加載, initialLoadDone=', initialLoadDone, 'sessionId=', sessionId);

    // 避免重複加載
    if (initialLoadDone || !sessionId) {
      console.debug('[SavedSearchList] 跳過初始加載');
      return;
    }

    const loadInitialData = async () => {
      setIsLoading(true);
      try {
        console.debug('[SavedSearchList] 執行初始加載');
        await fetchSavedSearches(true);
        setInitialLoadDone(true);
        console.debug('[SavedSearchList] 初始加載完成');
      } catch (error) {
        console.error("[SavedSearchList] 初始加載失敗:", error);
      } finally {
        setIsLoading(false);
      }
    };

    loadInitialData();
  }, [sessionId, fetchSavedSearches, initialLoadDone]);

  // 檢測searches變化
  useEffect(() => {
    console.debug('[SavedSearchList] searches變化，當前數量:', searches?.length);
  }, [searches]);

  // 組件挂載時執行一次刷新
  useEffect(() => {
    console.debug('[SavedSearchList] 組件挂載，執行一次刷新');
    if (sessionId) {
      handleRefresh();
    }
    // 只在組件挂載時執行一次
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 如果最後保存的搜索不在列表中，強制刷新
  useEffect(() => {
    if (lastSavedSearch && searches && searches.length > 0) {
      const savedSearchExists = searches.some(s => s.id === lastSavedSearch.id);
      if (!savedSearchExists) {
        console.debug('[SavedSearchList] 最後保存的搜索不在列表中，強制刷新');
        handleRefresh();
      }
    }
  }, [lastSavedSearch, searches, handleRefresh]);

  if (isLoading && !initialLoadDone) {
    console.debug('[SavedSearchList] 渲染加載中...');
    return <div className="text-center py-4">載入中...</div>;
  }

  if (error) {
    console.debug('[SavedSearchList] 渲染錯誤:', error);
    return <div className="text-center py-4 text-red-500">載入失敗: {error}</div>;
  }

  console.debug('[SavedSearchList] 渲染完整內容，searches數量:', searches?.length);
  return (
    <div className="p-4">
      <SearchListHeader
        onAdd={() => onEdit(null, 'create')}
        onRefresh={handleRefresh}
        onClear={handleClear}
        isRefreshing={isRefreshing}
      />
      <SearchListContent
        searches={searches || []}
        onEdit={(search) => onEdit(search, 'edit')}
        onDelete={handleDelete}
        onExecute={handleExecute}
        onView={handleView}
        onReorder={handleReorder}
      />
      <ConfirmModal
        open={showClearModal}
        onConfirm={handleConfirmClear}
        onCancel={handleCancelClear}
        message="確定要清空所有自訂搜尋？"
      />
      <ConfirmModal
        open={deleteConfirmOpen}
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
        message={`確定要刪除這個搜索嗎？`}
      />
    </div>
  );
});
