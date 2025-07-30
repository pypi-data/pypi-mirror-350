import React from "react";

export default function ConfirmModal({
  open,
  onConfirm,
  onCancel,
  message,
}: {
  open: boolean;
  onConfirm: () => void;
  onCancel: () => void;
  message: string;
}) {
  if (!open) return null;
  return (
    <div style={{
      position: "fixed",
      top: 0, left: 0, right: 0, bottom: 0,
      background: "rgba(0,0,0,0.6)",
      zIndex: 9999,
      display: "flex",
      alignItems: "center",
      justifyContent: "center"
    }}>
      <div style={{
        background: "#222",
        color: "#fff",
        borderRadius: 12,
        padding: "32px 24px",
        minWidth: 320,
        boxShadow: "0 4px 32px #000a"
      }}>
        <div style={{ fontSize: 18, marginBottom: 24, textAlign: "center" }}>
          {message}
        </div>
        <div style={{ display: "flex", gap: 16, justifyContent: "center" }}>
          <button
            onClick={onCancel}
            style={{
              background: "#444",
              color: "#fff",
              border: "none",
              borderRadius: 8,
              padding: "8px 24px",
              fontSize: 16,
              cursor: "pointer"
            }}
          >取消</button>
          <button
            onClick={onConfirm}
            style={{
              background: "#28c8c8",
              color: "#fff",
              border: "none",
              borderRadius: 8,
              padding: "8px 24px",
              fontSize: 16,
              cursor: "pointer"
            }}
          >刪除</button>
        </div>
      </div>
    </div>
  );
}
