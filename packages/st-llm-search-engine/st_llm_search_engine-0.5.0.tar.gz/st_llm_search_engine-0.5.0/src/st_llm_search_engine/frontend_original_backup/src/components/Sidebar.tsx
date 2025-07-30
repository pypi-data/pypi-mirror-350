// src/components/Sidebar.tsx
import React, { useState } from "react";
import SidebarHeader from "./SidebarHeader";
import ButtonGroup from "./ButtonGroup";
import SavedSearchList from "./SavedSearchList";
import SearchListResult from "./SearchListResult";

export default function Sidebar({ title }: { title: string }) {
  const [list, setList] = useState<string[]>(["Filter 01","Filter 02","Filter 03"]);
  const [activeTab, setActiveTab] = useState<'filter' | 'settings'>('filter');

  return (
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
      <SidebarHeader title={title} />
      <div style={{ marginTop: 20, width: "100%", display: "flex", justifyContent: "center" }}>
        <ButtonGroup activeTab={activeTab} setActiveTab={setActiveTab} />
      </div>
      <div
        style={{
          background: 'rgba(34,34,34,0.7)',
          borderRadius: 8,
          padding: '16px 0',
          width: '100%',
          marginTop: 50,
        }}
      >
        {activeTab === 'filter' ? (
          <>
            <SavedSearchList
              items={list}
              onSelect={name => alert(`選到 ${name}`)}
            />
            <SearchListResult items={list} onSelect={name => alert(`選到 ${name}`)} />
          </>
        ) : (
          <div
            style={{
              color: '#aaa',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: 120,
              width: '100%',
              fontSize: 16,
              fontWeight: 500,
            }}
          >
            此功能還在開發中
          </div>
        )}
      </div>
    </div>
  );
}
