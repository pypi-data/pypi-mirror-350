import React from 'react';
import { SearchProcessingOverlayProps } from '../types';

export const SearchProcessingOverlay: React.FC<SearchProcessingOverlayProps> = ({
  isVisible,
  title,
  onCancel
}) => {
  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-xl max-w-md w-full">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          正在處理搜索: {title}
        </h3>
        <div className="flex justify-center mb-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
        <p className="text-gray-600 text-center mb-4">
          請稍候，正在處理您的搜索請求...
        </p>
        <div className="flex justify-center">
          <button
            onClick={onCancel}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
          >
            取消
          </button>
        </div>
      </div>
    </div>
  );
};
