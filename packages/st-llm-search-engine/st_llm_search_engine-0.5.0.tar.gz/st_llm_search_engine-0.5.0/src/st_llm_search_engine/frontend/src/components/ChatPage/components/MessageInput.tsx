import React from 'react';
import { MessageInputProps } from '../types';

const MessageInput: React.FC<MessageInputProps> = ({
  value,
  onChange,
  onSend,
  isThinking
}) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // 對中文輸入法和 shift+enter 特殊處理
    if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div style={{
      position: 'fixed',
      bottom: 0,
      left: '288px', // 對齊 Sidebar 右側
      right: 0,
      background: '#161616',
      display: 'flex',
      alignItems: 'center',
      padding: '16px 32px',
      zIndex: 10
    }}>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        style={{
          flex: 1,
          background: '#222',
          color: '#fff',
          border: 'none',
          borderRadius: 12,
          padding: '12px 16px',
          fontSize: 16,
          outline: 'none',
          resize: 'none',
          minHeight: '40px',
          maxHeight: '100px',
          overflowY: 'auto'
        }}
        placeholder="請輸入訊息..."
        disabled={isThinking}
      />
      <button
        onClick={onSend}
        style={{
          marginLeft: 16,
          background: '#28c8c8',
          color: '#fff',
          border: 'none',
          borderRadius: 8,
          padding: '10px 20px',
          fontSize: 16,
          cursor: isThinking ? 'not-allowed' : 'pointer',
          opacity: isThinking ? 0.6 : 1
        }}
        disabled={isThinking}
      >
        送出
      </button>
    </div>
  );
};

export default MessageInput;
