import React from 'react';

interface LoadingModalProps {
  isVisible: boolean;
  isError?: boolean;
  retryCount?: number;
  maxRetries?: number;
  onRetry?: () => void;
}

const LoadingModal: React.FC<LoadingModalProps> = ({
  isVisible,
  isError = false,
  retryCount = 0,
  maxRetries = 24,
  onRetry
}) => {
  if (!isVisible) return null;

  // Calculate estimated time remaining (rough estimate)
  const remainingRetries = Math.max(0, maxRetries - retryCount);
  const estimatedTimeSeconds = remainingRetries * 5; // assuming 5 seconds per retry
  const minutesRemaining = Math.floor(estimatedTimeSeconds / 60);
  const secondsRemaining = estimatedTimeSeconds % 60;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.75)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 10000,
        color: '#fff',
        fontFamily: "'Inter', 'PingFang TC', 'Microsoft JhengHei', Arial, sans-serif",
      }}
    >
      <div
        style={{
          background: '#222',
          borderRadius: '16px',
          padding: '32px',
          width: '320px',
          textAlign: 'center',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          boxShadow: '0 4px 24px rgba(0, 0, 0, 0.5)',
        }}
      >
        {!isError ? (
          <>
            <div
              style={{
                width: '64px',
                height: '64px',
                borderRadius: '50%',
                border: '4px solid rgba(40, 200, 200, 0.1)',
                borderTopColor: '#28c8c8',
                animation: 'spin 1.5s linear infinite',
                marginBottom: '24px',
              }}
            />

            <h3
              style={{
                fontSize: '18px',
                fontWeight: 600,
                marginBottom: '16px',
                color: '#fff',
              }}
            >
              正在啟動服務
            </h3>

            <p
              style={{
                fontSize: '14px',
                lineHeight: 1.5,
                color: '#aaa',
                marginBottom: '8px',
              }}
            >
              服務正在啟動中，這可能需要約 {minutesRemaining}:{secondsRemaining.toString().padStart(2, '0')} 分鐘。
            </p>
            <p
              style={{
                fontSize: '14px',
                lineHeight: 1.5,
                color: '#aaa',
                marginBottom: '16px',
              }}
            >
              請稍候，頁面將自動加載。
            </p>

            <div
              style={{
                fontSize: '12px',
                color: '#666',
              }}
            >
              嘗試次數: {retryCount} / {maxRetries}
            </div>
          </>
        ) : (
          <>
            <div
              style={{
                width: '64px',
                height: '64px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '24px',
                color: '#ff4d4f',
                fontSize: '40px',
              }}
            >
              ⚠️
            </div>

            <h3
              style={{
                fontSize: '18px',
                fontWeight: 600,
                marginBottom: '16px',
                color: '#ff4d4f',
              }}
            >
              服務啟動失敗
            </h3>

            <p
              style={{
                fontSize: '14px',
                lineHeight: 1.5,
                color: '#aaa',
                marginBottom: '24px',
              }}
            >
              無法連接到後端服務，請稍後再試或聯繫系統管理員。
            </p>

            {onRetry && (
              <button
                onClick={onRetry}
                style={{
                  background: '#28c8c8',
                  color: '#222',
                  border: 'none',
                  borderRadius: '20px',
                  padding: '8px 24px',
                  fontSize: '14px',
                  fontWeight: 500,
                  cursor: 'pointer',
                }}
              >
                重試
              </button>
            )}
          </>
        )}

        <style>
          {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
          `}
        </style>
      </div>
    </div>
  );
};

export default LoadingModal;
