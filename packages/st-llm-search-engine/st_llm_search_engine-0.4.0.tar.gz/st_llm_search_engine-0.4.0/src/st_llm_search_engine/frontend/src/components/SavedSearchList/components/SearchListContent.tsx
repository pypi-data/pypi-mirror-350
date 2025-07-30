import React, { useState, useRef, useEffect } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { SavedSearch } from '../types';

interface SearchListContentProps {
  searches: SavedSearch[];
  onEdit: (search: SavedSearch) => void;
  onDelete: (id: number) => void;
  onExecute: (search: SavedSearch) => void;
  onView: (search: SavedSearch) => void;
  onReorder: (startIndex: number, endIndex: number) => void;
  isProcessing?: boolean;
  processingTitle?: string | null;
}

// 右鍵菜單元件
interface ContextMenuProps {
  visible: boolean;
  x: number;
  y: number;
  item: SavedSearch;
  onEdit: (search: SavedSearch) => void;
  onDelete: (id: number) => void;
  onExecute: (search: SavedSearch) => void;
  onView: (search: SavedSearch) => void;
  isSystemItem: boolean;
  onClose: () => void;
}

const ContextMenu: React.FC<ContextMenuProps> = ({
  visible,
  x,
  y,
  item,
  onEdit,
  onDelete,
  onExecute,
  onView,
  isSystemItem,
  onClose
}) => {
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [onClose]);

  if (!visible) return null;

  return (
    <div
      ref={menuRef}
      style={{
        position: 'fixed',
        top: y,
        left: x,
        background: '#222',
        border: '1px solid #444',
        borderRadius: 4,
        padding: 4,
        zIndex: 1000
      }}
    >
      {/* 檢視選項 - 所有項目都可見 */}
      <button
        style={{
          background: 'transparent',
          border: 'none',
          color: '#fff',
          padding: '8px 16px',
          cursor: 'pointer',
          width: '100%',
          textAlign: 'left',
          borderRadius: 4
        }}
        onClick={() => {
          onView(item);
          onClose();
        }}
        onMouseOver={(e) => {
          e.currentTarget.style.background = '#444';
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.background = 'transparent';
        }}
      >
        檢視
      </button>

      {/* 系統項目不可編輯或刪除 */}
      {!isSystemItem && (
        <>
          <button
            style={{
              background: 'transparent',
              border: 'none',
              color: '#fff',
              padding: '8px 16px',
              cursor: 'pointer',
              width: '100%',
              textAlign: 'left',
              borderRadius: 4
            }}
            onClick={() => {
              onEdit(item);
              onClose();
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.background = '#444';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.background = 'transparent';
            }}
          >
            編輯
          </button>

          <button
            style={{
              background: 'transparent',
              border: 'none',
              color: '#ff4d4f',
              padding: '8px 16px',
              cursor: 'pointer',
              width: '100%',
              textAlign: 'left',
              borderRadius: 4
            }}
            onClick={() => {
              // 直接調用 onDelete，確認視窗應該在父組件處理
              onDelete(item.id);
              onClose();
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.background = '#444';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.background = 'transparent';
            }}
          >
            刪除
          </button>
        </>
      )}
      {isSystemItem && (
        <div style={{
          color: '#777',
          padding: '8px 16px',
          fontSize: '14px'
        }}>
          系統項目不可編輯或刪除
        </div>
      )}
    </div>
  );
};

interface SearchItemProps {
  search: SavedSearch;
  index: number;
  onEdit: (search: SavedSearch) => void;
  onDelete: (id: number) => void;
  onExecute: (search: SavedSearch) => void;
  onView: (search: SavedSearch) => void;
  onReorder: (startIndex: number, endIndex: number) => void;
  isSelected: boolean;
  isProcessing: boolean;
  isProcessingThis: boolean;
}

const SearchItem: React.FC<SearchItemProps> = ({
  search,
  index,
  onEdit,
  onDelete,
  onExecute,
  onView,
  onReorder,
  isSelected,
  isProcessing,
  isProcessingThis
}) => {
  const isSystemItem = search.account === '系統';
  const [contextMenu, setContextMenu] = useState({ visible: false, x: 0, y: 0 });

  // 直接使用ref對象，不再單獨創建額外引用
  const ref = useRef<HTMLDivElement>(null);

  const [{ isDragging }, drag] = useDrag({
    type: 'SEARCH_ITEM',
    item: { index },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
    canDrag: () => !isSystemItem && !isProcessing,
  });

  const [, drop] = useDrop({
    accept: 'SEARCH_ITEM',
    hover: (item: { index: number }, monitor) => {
      // 如果是系統項目或正在處理中，不允許拖曳
      if (isSystemItem || isProcessing) return;

      // 如果是同一個項目，不進行操作
      if (item.index === index) return;

      // 獲取拖曳元素的位置
      if (!ref.current) return;

      const hoverBoundingRect = ref.current.getBoundingClientRect();
      const hoverMiddleY = (hoverBoundingRect.bottom - hoverBoundingRect.top) / 2;
      const clientOffset = monitor.getClientOffset();
      const hoverClientY = clientOffset ? clientOffset.y - hoverBoundingRect.top : 0;

      // 只有當拖曳超過元素中間位置時才進行重排序
      if ((item.index < index && hoverClientY < hoverMiddleY) ||
          (item.index > index && hoverClientY > hoverMiddleY)) {
        return;
      }

      // 執行重排序操作
      console.debug('[SearchItem] 重排序: 從', item.index, '到', index);
      onReorder(item.index, index);
      item.index = index;
    },
  });

  // 設置複合引用
  drag(drop(ref));

  const handleContextMenu = (e: React.MouseEvent) => {
    e.preventDefault();
    setContextMenu({
      visible: true,
      x: e.clientX,
      y: e.clientY
    });
  };

  const closeContextMenu = () => {
    setContextMenu({ ...contextMenu, visible: false });
  };

  return (
    <>
      <div
        ref={ref}
        style={{
          width: "100%",
          background: isDragging ? "#444444" : isSelected ? "#444444" : isProcessingThis ? "rgba(25,118,210,0.08)" : "transparent",
          borderRadius: 4,
          padding: "8px 16px",
          marginBottom: 8,
          cursor: isSystemItem || isProcessing ? "default" : "grab",
          color: "#FFFFFF",
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
          display: "flex",
          alignItems: "center",
          opacity: isDragging ? 0.5 : isProcessingThis ? 0.8 : 1,
          boxShadow: isDragging ? "0 4px 8px rgba(0,0,0,0.3)" : "none",
          transition: "background-color 0.2s ease",
          border: isSelected ? "1px solid #666" : "1px solid transparent",
        }}
        onClick={() => onExecute(search)}
        onContextMenu={handleContextMenu}
      >
        <span style={{
          marginRight: '12px',
          cursor: isSystemItem || isProcessing ? 'not-allowed' : 'grab',
          color: '#888',
          fontSize: '20px',   // 增大這個圖示
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: '16px',
          height: '16px',
        }}>
          ≡
        </span>
        <span style={{
          overflow: 'hidden',
          textOverflow: 'ellipsis',
          flexGrow: 1,
          color: 'white',    // 統一白色文字
          fontWeight: isSystemItem ? 500 : 400,
        }}>
          {search.title}
          {isProcessingThis && (
            <span style={{
              marginLeft: 8,
              color: '#4caf50',
              fontSize: '12px',
            }}>
              處理中...
            </span>
          )}
        </span>
      </div>

      <ContextMenu
        visible={contextMenu.visible}
        x={contextMenu.x}
        y={contextMenu.y}
        item={search}
        onEdit={onEdit}
        onDelete={onDelete}
        onExecute={onExecute}
        onView={onView}
        isSystemItem={isSystemItem}
        onClose={closeContextMenu}
      />
    </>
  );
};

export const SearchListContent: React.FC<SearchListContentProps> = ({
  searches,
  onEdit,
  onDelete,
  onExecute,
  onView,
  onReorder,
  isProcessing,
  processingTitle
}) => {
  console.debug('[SearchListContent] function body');
  const [selectedItem, setSelectedItem] = useState<number | null>(null);

  console.debug('[SearchListContent] render, searches:', searches, 'length:', searches?.length);

  // 檢查searches是否為有效數組
  if (!searches || !Array.isArray(searches)) {
    console.warn('[SearchListContent] 搜索數據無效:', searches);
    return <div style={{ color: '#888', textAlign: 'center', padding: '20px' }}>無搜索數據</div>;
  }

  // 檢查searches數組長度
  if (searches.length === 0) {
    return <div style={{ color: '#888', textAlign: 'center', padding: '20px' }}>暫無保存的搜索</div>;
  }

  const handleExecute = (search: SavedSearch) => {
    console.debug('[SearchListContent] 執行搜索:', search?.title || 'unknown');
    setSelectedItem(search.id);
    onExecute(search);
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div style={{ width: "100%" }}>
        {searches.map((search, index) => {
          // 檢查每個 search 對象的有效性
          if (!search || typeof search.id !== 'number') {
            console.warn('[SearchListContent] 無效的搜索項目:', search);
            return null;
          }

          const isProcessingThis = isProcessing && processingTitle === search.title;

          return (
            <SearchItem
              key={search.id}
              search={search}
              index={index}
              onEdit={onEdit}
              onDelete={onDelete}
              onExecute={handleExecute}
              onView={onView}
              onReorder={onReorder}
              isSelected={selectedItem === search.id}
              isProcessing={isProcessing}
              isProcessingThis={isProcessingThis}
            />
          );
        })}
      </div>
    </DndProvider>
  );
};
