import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import type { CodeComponent } from "react-markdown/lib/ast-to-react";
import TablePanel from "./TablePanel";

type Message = {
  id: string;
  role: "user" | "bot";
  content: string;
  timestamp: string;
};

const CodeBlock: CodeComponent = ({ className, children }) => {
  const [copied, setCopied] = useState(false);
  const language = className ? className.replace("language-", "") : "";
  const code = String(children).replace(/\n$/, "");
  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1200);
  };
  return (
    <div style={{ position: "relative" }}>
      <button
        onClick={handleCopy}
        style={{
          position: "absolute",
          top: 8,
          right: 8,
          zIndex: 2,
          background: "#222",
          color: "#28c8c8",
          border: "none",
          borderRadius: 4,
          padding: "2px 8px",
          fontSize: 12,
          cursor: "pointer"
        }}
      >
        {copied ? "已複製" : "複製"}
      </button>
      <SyntaxHighlighter language={language} style={oneDark} customStyle={{ borderRadius: 8, fontSize: 14 }}>
        {code}
      </SyntaxHighlighter>
    </div>
  );
};

function renderMessage(msg: Message) {
  let content = msg.content.trim();
  if (content.startsWith('```json')) {
    content = content.replace(/^```json/, '').replace(/```$/, '').trim();
  } else if (content.startsWith('```')) {
    content = content.replace(/^```/, '').replace(/```$/, '').trim();
  }
  let parsed: any;
  try {
    parsed = JSON.parse(content);
  } catch {}
  const isTableData = Array.isArray(parsed) && parsed.length > 0 && typeof parsed[0] === "object";

  if (isTableData) {
    const columns = Object.keys(parsed[0]).map(key => ({
      field: key,
      headerName: key
    }));
    const rows = parsed;
    return <TablePanel columns={columns} rows={rows} />;
  }
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{ code: CodeBlock }}
    >
      {msg.content}
    </ReactMarkdown>
  );
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const [isComposing, setIsComposing] = useState(false);

  useEffect(() => {
    if (!chatContainerRef.current) return;
    const el = chatContainerRef.current;
    el.scrollTop = el.scrollHeight;
  }, [messages.length]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages([
      ...messages,
      {
        id: Date.now().toString(),
        role: "user",
        content: input,
        timestamp: new Date().toLocaleTimeString().slice(0, 5)
      }
    ]);
    setInput("");
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: [
          ...messages,
          { role: "user", content: input }
        ] })
      });
      if (!res.ok) throw new Error("API error");
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setMessages(msgs => [
        ...msgs,
        {
          id: Date.now().toString() + "-bot",
          role: "bot",
          content: String(data.reply),
          timestamp: new Date().toLocaleTimeString().slice(0, 5)
        }
      ]);
    } catch (e) {
      setError("發生錯誤，請稍後再試");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", width: "100vw", height: "100vh" }}>
      <div style={{ flex: "0 0 10%" }} />
      <div style={{ flex: "0 0 80%", display: "flex", flexDirection: "column", height: "100vh" }}>
        {/* 訊息串 */}
        <div
          ref={chatContainerRef}
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            overflowY: "auto",
            padding: "24px 0"
          }}
        >
          {messages.map(msg => (
            <div
              key={msg.id}
              style={{
                display: "flex",
                flexDirection: msg.role === "user" ? "row-reverse" : "row",
                alignItems: "flex-end",
                marginBottom: 16,
              }}
            >
              <div
                style={{
                  background: msg.role === "user" ? "#222" : "none",
                  color: "#fff",
                  borderRadius: 12,
                  padding: "12px 16px",
                  maxWidth: msg.role === "user" ? "42%" : "70%",
                  wordBreak: "break-word",
                  fontSize: 16,
                  marginLeft: msg.role === "user" ? 0 : 12,
                  marginRight: msg.role === "user" ? 12 : 0,
                  alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
                }}
              >
                {renderMessage(msg)}
                <div style={{
                  fontSize: 12,
                  color: "#aaa",
                  marginTop: 4,
                  textAlign: msg.role === "user" ? "right" : "left"
                }}>{msg.timestamp}</div>
              </div>
            </div>
          ))}
          {loading && (
            <div style={{ color: "#aaa", textAlign: "center", margin: "16px 0" }}>
              機器人思考中...
            </div>
          )}
          {error && (
            <div style={{ color: "#ff4d4f", textAlign: "center", margin: "16px 0" }}>
              {error}
            </div>
          )}
        </div>
        {/* 輸入框 */}
        <div style={{
          width: "100%",
          background: "transparent",
          padding: "16px 32px",
          borderTop: "1px solid #222",
          display: "flex",
          alignItems: "center"
        }}>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onCompositionStart={() => setIsComposing(true)}
            onCompositionEnd={() => setIsComposing(false)}
            onKeyDown={e => { if (e.key === "Enter" && !isComposing) handleSend(); }}
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
            onClick={handleSend}
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
      <div style={{ flex: "0 0 10%" }} />
    </div>
  );
}
