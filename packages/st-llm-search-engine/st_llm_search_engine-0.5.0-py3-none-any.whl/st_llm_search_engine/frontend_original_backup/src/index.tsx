// frontend/src/index.tsx

import React, { useEffect } from "react";
import ReactDOM from "react-dom";
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";

// 定義簡化版 React 元件
class StLLMSearchEngine extends StreamlitComponentBase {
  public componentDidMount() {
    // 通知 Streamlit 元件已準備好
    Streamlit.setFrameHeight(window.innerHeight);
    console.log("Component initialized and ready");

    // 設置視窗大小變化的監聽器
    window.addEventListener('resize', this.handleResize);
  }

  public componentWillUnmount() {
    // 移除監聽器
    window.removeEventListener('resize', this.handleResize);
  }

  // 處理視窗大小變化
  private handleResize = () => {
    Streamlit.setFrameHeight(window.innerHeight);
  }

  public render() {
    return (
      <div
        style={{
          display: "flex",
          width: "100vw",
          height: "100vh",
          background: "#111111",
          fontFamily: "'Inter', 'PingFang TC', 'Microsoft JhengHei', Arial, sans-serif",
          color: "white",
        }}
      >
        {/* 簡化版側邊欄 */}
        <div style={{
          width: 288,
          height: "100vh",
          background: "#161616",
          color: "#FFFFFF",
          padding: "40px 24px 0 24px",
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
        }}>
          <h2>AI 雷達站</h2>
          <div style={{ marginTop: 20, width: "100%", display: "flex", justifyContent: "center" }}>
            <button style={{
              background: "#222",
              color: "white",
              border: "none",
              padding: "8px 16px",
              borderRadius: "4px",
              cursor: "pointer"
            }}>
              篩選器
            </button>
            <button style={{
              background: "transparent",
              color: "#999",
              border: "none",
              padding: "8px 16px",
              borderRadius: "4px",
              cursor: "pointer",
              marginLeft: "8px"
            }}>
              設定
            </button>
          </div>
        </div>

        {/* 簡化版聊天頁面 */}
        <div style={{ flex: 1, display: "flex", flexDirection: "column", height: "100vh" }}>
          <div style={{ flex: 1, padding: "24px", overflowY: "auto" }}>
            <div style={{
              background: "#222",
              color: "white",
              borderRadius: "12px",
              padding: "16px",
              maxWidth: "70%",
              marginBottom: "16px"
            }}>
              歡迎使用 AI 雷達站！這是一個簡化版的 UI。
            </div>
            <div style={{
              background: "#222",
              color: "white",
              borderRadius: "12px",
              padding: "16px",
              maxWidth: "70%",
              marginBottom: "16px",
              alignSelf: "flex-end",
              marginLeft: "auto"
            }}>
              這個版本已經能夠與 Streamlit 正確通訊了。
            </div>
          </div>
          <div style={{
            padding: "16px 32px",
            borderTop: "1px solid #222",
            display: "flex",
            alignItems: "center"
          }}>
            <input
              style={{
                flex: 1,
                background: "#222",
                color: "#fff",
                border: "none",
                borderRadius: 8,
                padding: "12px 16px",
                fontSize: 16,
                outline: "none"
              }}
              placeholder="輸入訊息..."
            />
            <button
              style={{
                marginLeft: 16,
                background: "#28c8c8",
                color: "#fff",
                border: "none",
                borderRadius: 8,
                padding: "10px 20px",
                fontSize: 16,
                cursor: "pointer"
              }}
            >送出</button>
          </div>
        </div>
      </div>
    );
  }
}

// 使用官方的 withStreamlitConnection 高階元件
const ConnectedComponent = withStreamlitConnection(StLLMSearchEngine);

// 渲染元件到 DOM
ReactDOM.render(
  <React.StrictMode>
    <ConnectedComponent />
  </React.StrictMode>,
  document.getElementById("root")
);
