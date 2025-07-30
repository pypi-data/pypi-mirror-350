import React from "react";
import { createRoot } from "react-dom/client";
import Sidebar from "./components/Sidebar";
import ChatPage from "./components/ChatPage";
import LoadingModal from "./components/LoadingModal";
import { useBackendStatus } from "./utils/useBackendStatus";
// 導入 AG Grid 樣式
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:8000";

function App() {
  const { isLoading, isError, retryCount } = useBackendStatus(apiUrl);

  /**
   * Handles retry action when backend connection fails
   * This function simply reloads the page which will:
   * 1. Reset the retry counter
   * 2. Attempt to reconnect to the backend
   * 3. Display a fresh loading state to the user
   */
  const handleRetry = () => {
    // Force reload the page to start the process over
    window.location.reload();
  };

  return (
    <>
      <LoadingModal
        isVisible={isLoading || isError}
        isError={isError}
        retryCount={retryCount}
        onRetry={handleRetry}
      />

      <div style={{
        display: "flex",
        visibility: isLoading || isError ? 'hidden' : 'visible'
      }}>
        <Sidebar title="輿論雷達站" apiUrl={apiUrl} />
        <ChatPage apiUrl={apiUrl} />
      </div>
    </>
  );
}

const root = createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
