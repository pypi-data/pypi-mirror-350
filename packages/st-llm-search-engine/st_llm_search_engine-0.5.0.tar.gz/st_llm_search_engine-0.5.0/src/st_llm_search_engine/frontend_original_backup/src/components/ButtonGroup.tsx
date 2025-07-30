// src/components/ButtonGroup.tsx
import React from "react";
import IconButton from "./IconButton";
import FilterIcon from "../assets/filter-icon.svg";
import SettingsIcon from "../assets/setting-icon.svg";

export default function ButtonGroup({ activeTab, setActiveTab }: {
  activeTab: "filter" | "settings",
  setActiveTab: (tab: "filter" | "settings") => void
}) {
  return (
    <div style={{
      display: "flex",
      gap: 8,
      width: "100%",
    }}>
      <div style={{ flex: 1 }}>
        <IconButton
          Icon={FilterIcon}
          iconWidth={24}
          iconHeight={24}
          width="100%"
          height={50}
          bgColor="#222222"
          borderRadius={"1vw"}
          active={activeTab === "filter"}
          onClick={() => setActiveTab("filter")}
        />
      </div>
      <div style={{ flex: 1 }}>
        <IconButton
          Icon={SettingsIcon}
          iconWidth={24}
          iconHeight={24}
          width="100%"
          height={50}
          bgColor="#222222"
          borderRadius={"1vw"}
          active={activeTab === "settings"}
          onClick={() => setActiveTab("settings")}
        />
      </div>
    </div>
  );
}
