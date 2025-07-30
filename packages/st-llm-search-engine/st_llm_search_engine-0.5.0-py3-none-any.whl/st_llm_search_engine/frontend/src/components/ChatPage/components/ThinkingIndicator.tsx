import React from 'react';
import { ThinkingIndicatorProps } from '../types';

const ThinkingIndicator: React.FC<ThinkingIndicatorProps> = ({ isVisible }) => {
  if (!isVisible) return null;

  return (
    <div style={{
      color: '#aaa',
      marginTop: 8,
      marginLeft: 12,
      display: 'flex',
      alignItems: 'center',
    }}>
      <span>正在思考中</span>
      <span className="thinking-dots" style={{
        marginLeft: 4,
        animation: 'ellipsis 1.5s infinite',
      }}>...</span>

      <style>
        {`
          @keyframes ellipsis {
            0% { opacity: 0.3; }
            50% { opacity: 1; }
            100% { opacity: 0.3; }
          }

          .thinking-dots {
            animation: ellipsis 1.5s infinite;
          }
        `}
      </style>
    </div>
  );
};

export default ThinkingIndicator;
