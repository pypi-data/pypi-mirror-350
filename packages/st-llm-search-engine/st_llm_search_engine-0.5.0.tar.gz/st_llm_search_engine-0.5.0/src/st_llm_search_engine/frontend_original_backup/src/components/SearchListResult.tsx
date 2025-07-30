import React from "react";

export type SearchListResultProps = {
  items: string[];
  onSelect: (name: string) => void;
};

export default function SearchListResult({ items, onSelect }: SearchListResultProps) {
  return (
    <ul style={{ listStyle: "none", padding: 0, margin: 0, width: "100%" }}>
      {items.map(name => (
        <li key={name} style={{
          width: "100%",
          background: "#333333",
          borderRadius: 4,
          padding: "8px 16px",
          marginBottom: 8,
          cursor: "pointer",
          color: "#FFFFFF"
        }}
        onClick={() => onSelect(name)}
        >
          {name}
        </li>
      ))}
    </ul>
  );
}
