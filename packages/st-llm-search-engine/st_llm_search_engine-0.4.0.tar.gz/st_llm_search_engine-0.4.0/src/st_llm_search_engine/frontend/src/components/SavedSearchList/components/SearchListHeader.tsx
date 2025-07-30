import React from 'react';
import { SearchListHeaderProps } from '../types';
import { FaSyncAlt, FaTrash, FaPlus } from 'react-icons/fa';

const BUTTON_STYLE = {
  background: 'none',
  border: 'none',
  color: '#28c8c8',
  cursor: 'pointer',
  fontSize: 16,
  lineHeight: 1,
  padding: 0,
  margin: 0,
  width: 20,
  height: 20,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
} as const;

const ICON_PROPS = { size: 16 };

export const SearchListHeader: React.FC<SearchListHeaderProps> = ({
  onAdd,
  onRefresh,
  onClear,
  isRefreshing
}) => {
  return (
    <div style={{
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      marginBottom: 20,
      color: "#777777",
      width: "100%",
      paddingRight: 16,
    }}>
      <div style={{ display: "flex", alignItems: "center" }}>
        <span style={{
          textAlign: "left",
          color: "#777777",
          fontSize: 14,
          fontWeight: 500,
          paddingLeft: 8
        }}>Saved Search</span>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        {/* 刷新按鈕 */}
        <button
          onClick={onRefresh}
          disabled={isRefreshing}
          style={BUTTON_STYLE}
          title="刷新列表"
        >
          <FaSyncAlt
            {...ICON_PROPS}
            style={isRefreshing ? { animation: "spin 1s linear infinite" } : {}}
          />
        </button>
        {/* 清空按鈕 */}
        <button
          onClick={onClear}
          style={BUTTON_STYLE}
          title="清空列表"
        >
          <FaTrash {...ICON_PROPS} />
        </button>
        {/* 新增按鈕 */}
        <button
          onClick={onAdd}
          style={BUTTON_STYLE}
          title="新增搜索"
        >
          <FaPlus {...ICON_PROPS} />
        </button>
      </div>
    </div>
  );
};
