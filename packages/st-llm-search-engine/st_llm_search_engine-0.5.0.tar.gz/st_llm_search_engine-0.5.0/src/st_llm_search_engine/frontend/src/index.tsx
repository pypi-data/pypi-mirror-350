// frontend/src/index.tsx

import React from "react";
import ReactDOM from "react-dom";
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";
import Sidebar from "./components/Sidebar";
import ChatPage from "./components/ChatPage";
import LoadingModal from "./components/LoadingModal";
import { useBackendStatus } from "./utils/useBackendStatus";
// 導入 AG Grid 樣式
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

// 包裝 StLLMSearchEngine 組件，添加 LoadingModal
function AppWrapper(props: any) {
  const apiUrl = props.args?.api_url || "http://localhost:8000";
  const { isLoading, isError, retryCount } = useBackendStatus(apiUrl);

  const handleRetry = () => {
    // 強制重新載入頁面以重置計數器並重新嘗試連接
    window.location.reload();
  };

  // 設定 iframe 高度（只需呼叫一次即可）
  Streamlit.setFrameHeight();

  return (
    <>
      <LoadingModal
        isVisible={isLoading || isError}
        isError={isError}
        retryCount={retryCount}
        onRetry={handleRetry}
      />

      <div style={{
        width: "100%",
        height: "100vh",
        background: "#111",
        color: "white",
        fontFamily: "'Inter', 'PingFang TC', 'Microsoft JhengHei', Arial, sans-serif",
        display: "flex",
        position: "relative",
        margin: 0,
        padding: 0,
        visibility: isLoading || isError ? 'hidden' : 'visible'
      }}>
        <Sidebar title="輿論雷達站" apiUrl={apiUrl} />
        <ChatPage apiUrl={apiUrl} />
      </div>
    </>
  );
}

class StLLMSearchEngine extends StreamlitComponentBase<any> {
  public render() {
    return <AppWrapper {...this.props} />;
  }
}

const ConnectedComponent = withStreamlitConnection(StLLMSearchEngine);

ReactDOM.render(
  <React.StrictMode>
    <ConnectedComponent />
  </React.StrictMode>,
  document.getElementById("root")
);

