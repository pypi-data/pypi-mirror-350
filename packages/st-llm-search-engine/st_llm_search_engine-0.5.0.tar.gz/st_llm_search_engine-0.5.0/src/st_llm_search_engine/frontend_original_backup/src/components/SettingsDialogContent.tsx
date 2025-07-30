import React from "react";

export default function SettingsDialogContent({ onClose }: { onClose: () => void }) {
  return (
    <div
      style={{
        width: 616,
        height: 634,
        background: "#161616",
        borderRadius: 20,
        position: "relative",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        boxSizing: "border-box",
        padding: 0,
      }}
    >
      {/* 關閉按鈕 */}
      <button
        onClick={onClose}
        style={{
          position: "absolute",
          right: 28,
          top: 28,
          width: 24,
          height: 24,
          background: "none",
          border: "none",
          cursor: "pointer",
          color: "#fff",
          fontSize: 24,
        }}
        aria-label="close"
      >×</button>

      {/* 標題 */}
      <div
        style={{
          position: "absolute",
          top: 28,
          left: "50%",
          transform: "translateX(-50%)",
          width: 144,
          height: 29,
          fontFamily: "Inter",
          fontWeight: 400,
          fontSize: 24,
          lineHeight: "29px",
          color: "#fff",
          textAlign: "center",
        }}
      >
        新增查詢條件
      </div>

      {/* 主要內容區塊 */}
      <div
        style={{
          position: "absolute",
          top: 77,
          left: "50%",
          transform: "translateX(-50%)",
          width: 552,
          height: 442,
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          gap: 28,
        }}
      >
        {/* 標題欄位 */}
        <div style={{ display: "flex", flexDirection: "column", gap: 8, width: 199 }}>
          <div style={{ color: "#fff", fontSize: 14, lineHeight: "17px" }}>標題</div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              background: "#222",
              borderRadius: 12,
              padding: 12,
              width: 199,
              height: 41,
            }}
          >
            <span style={{ color: "rgba(255,255,255,0.5)", fontSize: 14 }}>請輸入查詢標題</span>
          </div>
        </div>
        {/* 其餘區塊照 Figma 規格用 flex/gap 寫，可自行擴充 */}
      </div>

      {/* 底部按鈕區 */}
      <div
        style={{
          position: "absolute",
          left: "50%",
          transform: "translateX(-50%)",
          bottom: 28,
          display: "flex",
          flexDirection: "row",
          gap: 8,
          width: 232,
          height: 51,
        }}
      >
        <button
          style={{
            flex: 1,
            background: "#333",
            borderRadius: 99,
            color: "#fff",
            fontWeight: 500,
            fontSize: 16,
            border: "none",
            padding: "16px 40px",
            cursor: "pointer",
          }}
          onClick={onClose}
        >
          取消
        </button>
        <button
          style={{
            flex: 1,
            background: "#28D1D1",
            borderRadius: 99,
            color: "#222",
            fontWeight: 600,
            fontSize: 16,
            border: "none",
            padding: "16px 40px",
            cursor: "pointer",
          }}
        >
          儲存
        </button>
      </div>
    </div>
  );
}
