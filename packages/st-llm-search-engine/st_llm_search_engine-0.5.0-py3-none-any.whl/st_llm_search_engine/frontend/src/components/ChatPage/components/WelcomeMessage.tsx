import React from 'react';
import { WelcomeMessageProps } from '../types';

const WelcomeMessage: React.FC<WelcomeMessageProps> = ({ isVisible }) => {
  if (!isVisible) return null;

  return (
    <div style={{
      color: '#aaa',
      position: 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      width: '80%',
      textAlign: 'center',
      zIndex: 10
    }}>
      <div style={{ fontSize: 24, fontWeight: 600, color: '#28c8c8', marginBottom: 80 }}>
        歡迎使用 AI 雷達站！
      </div>
      <div style={{ fontSize: 16, marginBottom: 30 }}>
        您可以透過以下方式開始使用：
      </div>
      <div style={{ marginBottom: 12 }}>
        <span style={{ color: '#28c8c8', fontWeight: 600}}>1.</span>
        <span>在下方和我聊天</span>
      </div>
      <div style={{ marginBottom: 12 }}>
        <span style={{ color: '#28c8c8', fontWeight: 600}}>2.</span>
        <span>從左側選擇一個你想看的報告，我將替你篩選&分析資料</span>
      </div>
      <div style={{ marginBottom: 12 }}>
        <span style={{ color: '#28c8c8', fontWeight: 600}}>3.</span>
        <span>客製化你想看的報告，去點擊左側的「+」吧！！</span>
      </div>
    </div>
  );
};

export default WelcomeMessage;
