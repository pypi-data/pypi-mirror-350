import React from 'react';
import { ErrorMessageProps } from '../types';

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onClear, isVisible }) => {
  if (!isVisible) return null;

  return (
    <div style={{
      color: '#ff4d4f',
      textAlign: 'center',
      margin: '16px 0',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: 8
    }}>
      <span>{message}</span>
      <button
        onClick={onClear}
        style={{
          background: 'none',
          border: 'none',
          color: '#28c8c8',
          cursor: 'pointer',
          fontSize: 14,
          padding: '4px 8px',
          borderRadius: 4,
        }}
      >
        重試
      </button>
    </div>
  );
};

export default ErrorMessage;
