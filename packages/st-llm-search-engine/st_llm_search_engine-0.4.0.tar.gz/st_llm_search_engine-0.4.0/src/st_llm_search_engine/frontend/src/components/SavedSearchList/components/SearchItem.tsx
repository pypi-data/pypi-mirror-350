import React from 'react';
import { SearchItemProps } from '../types';

export const SearchItem: React.FC<SearchItemProps> = ({
  search,
  onEdit,
  onDelete,
  onExecute,
  isSystem
}) => {
  return (
    <div className="flex items-center justify-between p-3 bg-white rounded-lg shadow-sm">
      <div className="flex-1">
        <h3 className="text-sm font-medium text-gray-900">{search.title}</h3>
        {isSystem && (
          <span className="inline-block px-2 py-1 text-xs text-gray-500 bg-gray-100 rounded">
            系統搜索
          </span>
        )}
      </div>
      <div className="flex items-center space-x-2">
        <button
          onClick={() => onExecute(search)}
          className="p-2 text-green-500"
          title="執行搜索"
        >
          <i className="fas fa-play"></i>
        </button>
        {!isSystem && (
          <>
            <button
              onClick={() => onEdit(search)}
              className="p-2 text-blue-500"
              title="編輯搜索"
            >
              <i className="fas fa-edit"></i>
            </button>
            <button
              onClick={() => onDelete(search.id)}
              className="p-2 text-red-500"
              title="刪除搜索"
            >
              <i className="fas fa-trash"></i>
            </button>
          </>
        )}
      </div>
    </div>
  );
};
