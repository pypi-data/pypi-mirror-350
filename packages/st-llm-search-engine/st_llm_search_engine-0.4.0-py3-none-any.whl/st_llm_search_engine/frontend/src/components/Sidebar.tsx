// src/components/Sidebar.tsx
import React, { useState, useEffect, useCallback, useRef } from "react";
import SidebarHeader from "./SidebarHeader";
import ButtonGroup from "./ButtonGroup";
import { SavedSearchList, SavedSearchListRef } from "./SavedSearchList";
import { SavedSearch, SearchQuery } from "./SavedSearchList/types";
import SearchModal from "./SearchModal";
import { getSessionId } from '../utils/session';

interface SidebarProps {
  title: string;
  apiUrl: string;
}

export default function Sidebar({ title, apiUrl }: SidebarProps) {
  console.debug('[Sidebar] 渲染組件');
  const [activeTab, setActiveTab] = useState<'filter' | 'settings'>('filter');
  const [sessionId, setSessionId] = useState<string>(() => getSessionId());
  const [modalOpen, setModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState<'create' | 'edit' | 'view'>('create');
  const [currentSearch, setCurrentSearch] = useState<SavedSearch | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  // 新增狀態，追蹤保存搜索的結果
  const [saveResult, setSaveResult] = useState<{id: number, title: string} | null>(null);

  // 保存對 SavedSearchList 組件的引用
  const savedSearchListRef = useRef<SavedSearchListRef>(null);

  // 只在組件掛載時獲取 sessionId
  useEffect(() => {
    if (sessionId) return;
    (async () => {
      try {
        const response = await fetch(`${apiUrl}/api/session`);
        const data = await response.json();
        if (data.session_id) {
          sessionStorage.setItem('session_id', data.session_id);
          setSessionId(data.session_id);
        }
      } catch (error) {
        console.error("[Sidebar] 獲取 session ID 失敗:", error);
      }
    })();
  }, [apiUrl, sessionId]);

  const handleSearchAction = useCallback((search: SavedSearch | null, mode: 'edit' | 'view' | 'create') => {
    console.debug('[Sidebar] handleSearchAction 觸發，mode:', mode, 'search:', search?.title);
    setCurrentSearch(search);
    setModalMode(mode);
    setModalOpen(true);
  }, []);

  const handleModalClose = useCallback(() => {
    console.debug('[Sidebar] 關閉模態框');
    setModalOpen(false);
  }, []);

  const handleSaveSearch = useCallback(async (data: SearchQuery) => {
    console.debug('[Sidebar] 保存搜索:', data);
    setIsSaving(true);
    try {
      if (modalMode === 'create') {
        // 創建新搜索 - 直接使用 SavedSearchList 的方法
        const searchData = {
          title: data.title || "",
          account: "使用者", // 添加必要的 account 字段
          query: {
            title: data.title || "", // 確保 query 也包含 title
            time: data.time ?? 1,
            source: data.source ?? 0,
            tags: Array.isArray(data.tags) ? data.tags : ["All"],
            query: data.query || "",
            n: data.n ?? "",
            range: data.range ?? null
          }
        };

        console.debug('[Sidebar] 調用 handleSaveSearch:', searchData);
        const result = await savedSearchListRef.current.handleSaveSearch(searchData);

        if (result) {
          console.debug('[Sidebar] 保存成功, 結果:', result);
          setSaveResult(result);

          // 保存成功後關閉模態框
          setModalOpen(false);
          console.debug('[Sidebar] 新增搜尋後關閉模態框');
        }

        // 保存後立即刷新
        setTimeout(() => {
          if (savedSearchListRef.current) {
            console.debug('[Sidebar] 保存後延時強制刷新');
            savedSearchListRef.current.handleRefresh();
          }
        }, 500);

        // 第二次刷新，確保UI更新
        setTimeout(() => {
          if (savedSearchListRef.current) {
            console.debug('[Sidebar] 保存後第二次延時刷新');
            savedSearchListRef.current.handleRefresh();
          }
        }, 1000);
      } else if (modalMode === 'edit' && currentSearch) {
        // 編輯搜索 - 使用 SavedSearchList 的方法
        const updatedData = {
          title: data.title || "",
          query: {
            title: data.title || "", // 確保 query 也包含 title
            time: data.time ?? 1,
            source: data.source ?? 0,
            tags: Array.isArray(data.tags) ? data.tags : ["All"],
            query: data.query || "",
            n: data.n ?? "",
            range: data.range ?? null
          }
        };

        // 重要：先更新當前搜索的 UI 狀態，讓使用者立即看到變化
        setCurrentSearch(prev => {
          if (!prev) return null;
          return {
            ...prev,
            title: data.title || prev.title,
            query: {
              ...prev.query,
              title: data.title || prev.query.title,
              time: data.time ?? prev.query.time,
              source: data.source ?? prev.query.source,
              tags: Array.isArray(data.tags) ? data.tags : prev.query.tags,
              query: data.query || prev.query.query,
              n: data.n ?? prev.query.n,
              range: data.range ?? prev.query.range
            }
          };
        });

        // 立即關閉 modal，避免閃爍
        setModalOpen(false);
        console.debug('[Sidebar] 立即關閉模態框，避免閃爍');

        // 保存搜索結果到狀態，觸發刷新邏輯
        setSaveResult({
          id: currentSearch.id,
          title: data.title
        });

        // 然後在背景執行 API 請求
        console.debug('[Sidebar] 調用 handleUpdateSearch, ID:', currentSearch.id);
        savedSearchListRef.current.handleUpdateSearch(currentSearch.id, updatedData)
          .then(() => {
            console.debug('[Sidebar] API 更新成功');
            // 保存成功後靜默刷新列表數據
            setTimeout(() => {
              if (savedSearchListRef.current) {
                savedSearchListRef.current.handleRefresh();
              }
            }, 200);
          })
          .catch(error => {
            console.error("[Sidebar] API 更新失敗:", error);
            // 可以在這裡添加錯誤提示，但不影響已關閉的 modal
          });
      } else {
        // 其他情況直接關閉模態框
        setModalOpen(false);
        console.debug('[Sidebar] 保存完成，關閉模態框');
      }
    } catch (error) {
      console.error("[Sidebar] 保存搜索失敗:", error);
    } finally {
      setIsSaving(false);
    }
  }, [modalMode, currentSearch, sessionId]);

  // 監聽保存結果，確保 UI 狀態一致
  useEffect(() => {
    if (saveResult && savedSearchListRef.current) {
      console.debug('[Sidebar] 檢測到保存結果變化:', saveResult);

      // 強制刷新
      savedSearchListRef.current.handleRefresh();

      // 清空保存結果
      setTimeout(() => {
        setSaveResult(null);
      }, 1000);
    }
  }, [saveResult]);

  return (
    <div style={{
      width: 288,
      height: "100vh",
      minHeight: "100vh",
      background: "#161616",
      color: "#FFFFFF",
      padding: "40px 24px 0 24px",
      display: "flex",
      flexDirection: "column",
      alignItems: "flex-start",
      flexShrink: 0,
      boxSizing: "border-box",
      position: "fixed",
      left: 0,
      top: 0,
      bottom: 0,
      zIndex: 100,
    }}>
      <SidebarHeader title={title} />
      <div style={{ marginTop: 20, width: "100%", display: "flex", justifyContent: "center" }}>
        <ButtonGroup activeTab={activeTab} setActiveTab={setActiveTab} />
      </div>
      <div
        style={{
          background: 'rgba(34,34,34,0.7)',
          borderRadius: 8,
          padding: '16px 0',
          width: '100%',
          marginTop: 50,
          flex: 1,
          overflow: "auto",
          marginBottom: 0,
          paddingBottom: 24
        }}
      >
        {activeTab === 'filter' ? (
          sessionId && (
            <SavedSearchList
              ref={savedSearchListRef}
              apiUrl={apiUrl}
              sessionId={sessionId}
              onEdit={handleSearchAction}
            />
          )
        ) : (
          <div
            style={{
              color: '#aaa',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: 120,
              width: '100%',
              fontSize: 16,
              fontWeight: 500,
            }}
          >
            此功能還在開發中
          </div>
        )}
      </div>

      {modalOpen && (
        <SearchModal
          open={modalOpen}
          mode={modalMode}
          onClose={handleModalClose}
          onSave={handleSaveSearch}
          initialData={currentSearch ? {
            title: currentSearch.title,
            time: currentSearch.query.time,
            source: currentSearch.query.source,
            tags: currentSearch.query.tags,
            query: currentSearch.query.query,
            n: currentSearch.query.n,
            range: currentSearch.query.range
          } : null}
          isSaving={isSaving}
          apiUrl={apiUrl}
        />
      )}
    </div>
  );
}
