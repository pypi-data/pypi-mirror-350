// src/components/SidebarHeader.tsx
import React, { useRef, useLayoutEffect, useState } from "react";

export default function SidebarHeader({ title }: { title: string }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [fontSize, setFontSize] = useState(24);

  useLayoutEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;
    const context = document.createElement("canvas").getContext("2d");
    if (!context) return;
    let size = 24;
    context.font = `700 ${size}px Inter, PingFang TC, Microsoft JhengHei, Arial, sans-serif`;
    let textWidth = context.measureText(title).width;
    const maxWidth = container.offsetWidth;
    while (textWidth > maxWidth && size > 12) {
      size -= 1;
      context.font = `700 ${size}px Inter, PingFang TC, Microsoft JhengHei, Arial, sans-serif`;
      textWidth = context.measureText(title).width;
    }
    setFontSize(size);
  }, [title]);

  return (
    <div
      ref={containerRef}
      style={{
        width: "100%",
        minHeight: 29,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
      }}
    >
      <h2
        style={{
          width: "100%",
          fontFamily: "'Inter', 'PingFang TC', 'Microsoft JhengHei', Arial, sans-serif",
          fontWeight: 700,
          fontSize,
          lineHeight: 1.2,
          color: "#FFFFFF",
          margin: 0,
          whiteSpace: "nowrap",
          textAlign: "center",
          overflow: "hidden",
          textOverflow: "ellipsis",
        }}
        title={title}
      >
        {title}
      </h2>
    </div>
  );
}
