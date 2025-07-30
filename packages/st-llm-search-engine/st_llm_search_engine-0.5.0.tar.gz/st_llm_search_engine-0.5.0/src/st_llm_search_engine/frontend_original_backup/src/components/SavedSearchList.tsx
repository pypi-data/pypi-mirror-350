// src/components/SavedSearchList.tsx
import React, { useState } from "react";
import SearchListResult from "./SearchListResult";
import Modal from "./Modal";

export type SavedSearchListProps = {
  items: string[];
  onSelect: (name: string) => void;
};

export default function SavedSearchList({
  items,
  onSelect
}: SavedSearchListProps) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{ width: "100%" }}>
      <div style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 20,     // 與清單距離拉大
        color: "#777777",
        width: "100%"
      }}>
        <span style={{
          textAlign: "left",
          color: "#777777",
          fontSize: 12,
          paddingLeft: 8
        }}>Saved Search</span>
        <button onClick={() => setOpen(true)} style={{
          background: "none",
          border: "none",
          color: "#28c8c8",
          cursor: "pointer",
          fontSize: 12,
          lineHeight: 1,
          padding: 0,
          paddingRight: 8,
          margin: 0
        }}>＋</button>
      </div>
      <SearchListResult items={items} onSelect={onSelect} />
      <Modal open={open} onClose={() => setOpen(false)} />
    </div>
  );
}
