import React, { useState, useRef, useEffect } from "react";
import { DatePicker } from 'antd';
import 'antd/dist/reset.css';
import TagSelector from "./TagSelector";
const { RangePicker } = DatePicker;

const fontFamily = "'Inter', 'Noto Sans TC', 'Microsoft JhengHei', Arial, sans-serif";
const timeOptions = ["昨日", "今日", "近N日", "自訂區間"];
const sourceOptions = ["全部", "Facebook", "Threads"];

export default function Modal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const [title, setTitle] = useState("");
  const [tag, setTag] = useState("");
  const [query, setQuery] = useState("");
  const [time, setTime] = useState(0);
  const [source, setSource] = useState(0);
  const [n, setN] = useState("");
  const [nError, setNError] = useState(false);
  const nInputRef = useRef<HTMLInputElement>(null);
  const [range, setRange] = useState<any>(null);
  const [popupOpen, setPopupOpen] = useState(false);
  const tagRef = useRef<HTMLTextAreaElement>(null);
  const queryRef = useRef<HTMLTextAreaElement>(null);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [tagsList, setTagsList] = useState<string[]>([]);

  const validateN = (val: string) => {
    const num = Number(val);
    return /^[1-9]$|^1[0-9]$|^2[0-9]$|^30$/.test(val) && num >= 1 && num <= 30;
  };

  // 自動長高
  useEffect(() => {
    if (tagRef.current) {
      tagRef.current.style.height = '40px';
      tagRef.current.style.height = tagRef.current.scrollHeight + 'px';
    }
  }, [tag]);
  useEffect(() => {
    if (queryRef.current) {
      queryRef.current.style.height = '40px';
      queryRef.current.style.height = queryRef.current.scrollHeight + 'px';
    }
  }, [query]);

  useEffect(() => {
    if (open) {
      setSelectedTags([]); // 每次打開 modal 都重置 chip 狀態
    }
  }, [open]);

  // 自動 fetch 標籤
  useEffect(() => {
    if (open) {
      fetch("/api/sheet/kol?col=KOL")
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) {
            setTagsList(data);
          }
        })
        .catch(err => console.error("Failed to fetch tags:", err));
    }
  }, [open]);

  if (!open) return null;
  return (
    <div
      className="modal-backdrop"
      style={{
        position: "fixed",
        top: 0, left: 0, right: 0, bottom: 0,
        background: "rgba(0,0,0,0.7)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily,
      }}
      onClick={e => {
        if (e.target === e.currentTarget) {
          // 檢查是否有 popup 並且點擊在 popup 上
          const dropdown = document.querySelector('.ant-picker-dropdown');
          if (dropdown && dropdown.contains(document.activeElement)) {
            // 點擊在 popup 上，不做事
            return;
          }
          if (popupOpen) {
            setPopupOpen(false);
            document.activeElement && (document.activeElement as HTMLElement).blur();
          } else {
            onClose();
          }
        }
      }}
    >
      <div
        className="modal-content"
        style={{
          width: 616,
          minHeight: 634,
          height: "auto",
          maxHeight: "90vh",
          background: "#161616",
          borderRadius: 20,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          boxSizing: "border-box",
          padding: 0,
          position: "relative",
          paddingBottom: 24,
        }}
        onClick={e => e.stopPropagation()}
      >
        {/* 標題 */}
        <div
          style={{
            width: "100%",
            fontWeight: 400,
            fontSize: 24,
            lineHeight: "29px",
            color: "#fff",
            textAlign: "center",
            fontFamily,
            marginTop: 28,
            marginBottom: 28,
          }}
        >
          新增查詢條件
        </div>

        {/* 主要內容區塊 */}
        <div
          style={{
            width: 552,
            flex: 1,
            display: "flex",
            flexDirection: "column",
            alignItems: "flex-start",
            gap: 28,
            fontFamily,
            overflowY: "auto",
          }}
        >
          {/* 標題 */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14, lineHeight: "17px" }}>標題</div>
            <input
              value={title}
              onChange={e => setTitle(e.target.value)}
              placeholder="請輸入查詢標題"
              style={{
                background: "#222",
                borderRadius: 12,
                border: "none",
                padding: 12,
                width: "100%",
                color: "#fff",
                fontSize: 14,
                outline: "none",
                fontFamily,
              }}
            />
          </div>
          {/* 時間 */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14 }}>
              時間
              {nError && (
                <span style={{ color: "#FF4C4C", marginLeft: 12 }}>請輸入1-30內的數字</span>
              )}
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              {timeOptions.map((label, i) => (
                <button
                  key={label}
                  onClick={() => { setTime(i); if (i !== 2) setNError(false); }}
                  style={{
                    background: i === time ? "#222" : "#222",
                    border: i === time ? "1px solid #28C8C8" : "none",
                    color: "#fff",
                    borderRadius: 12,
                    padding: "12px 20px",
                    fontSize: 14,
                    cursor: "pointer",
                    opacity: i === time ? 1 : 0.7,
                    fontFamily,
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  {label === "近N日"
                    ? (i === time
                      ? (
                        <>
                          近
                          <input
                            ref={nInputRef}
                            value={n}
                            onChange={e => {
                              setN(e.target.value);
                              setNError(false);
                            }}
                            onBlur={() => setNError(!validateN(n))}
                            style={{
                              width: 28,
                              margin: "0 2px",
                              background: "transparent",
                              border: "none",
                              color: "#fff",
                              fontSize: 14,
                              textAlign: "center",
                              outline: "none",
                              borderBottom: "1px solid #28C8C8",
                            }}
                            maxLength={2}
                            inputMode="numeric"
                            pattern="[0-9]*"
                            placeholder="N"
                          />
                          日
                        </>
                      )
                      : "近N日"
                    )
                    : label
                  }
                </button>
              ))}
            </div>
            {time === 3 && (
              <div style={{ display: "flex", justifyContent: "center", width: "100%", marginTop: 20 }}>
                <RangePicker
                  showTime
                  style={{ minWidth: 350, width: '70%' }}
                  getPopupContainer={trigger => document.body}
                  popupStyle={{ color: '#bbb', background: '#181818' }}
                  onChange={(val, strArr) => setRange(val)}
                  onOk={() => document.activeElement && (document.activeElement as HTMLElement).blur()}
                  open={popupOpen}
                  onOpenChange={setPopupOpen}
                />
              </div>
            )}
          </div>
          {/* 資料源 */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14 }}>資料源</div>
            <div style={{ display: "flex", gap: 8 }}>
              {sourceOptions.map((label, i) => (
                <button
                  key={label}
                  onClick={() => setSource(i)}
                  style={{
                    background: i === source ? "#222" : "#222",
                    border: i === source ? "1px solid #28C8C8" : "none",
                    color: "#fff",
                    borderRadius: 12,
                    padding: "12px 20px",
                    fontSize: 14,
                    cursor: "pointer",
                    opacity: i === source ? 1 : 0.7,
                    fontFamily,
                  }}
                >{label}</button>
              ))}
            </div>
          </div>
          {/* 標籤 */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14 }}>標籤</div>
            <TagSelector
              tagsList={tagsList}
              value={selectedTags}
              onChange={setSelectedTags}
            />
          </div>
          {/* 檢索口令 */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14 }}>檢索口令</div>
            <textarea
              ref={queryRef}
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="請輸入您想查詢的檢索口令"
              rows={1}
              style={{
                background: "#222",
                borderRadius: 12,
                border: "none",
                padding: 12,
                width: "100%",
                color: "#fff",
                fontSize: 14,
                outline: "none",
                fontFamily,
                wordBreak: "break-all",
                resize: "none",
                height: 40,
                minHeight: 40,
                lineHeight: 1.5,
              }}
            />
          </div>
        </div>
        {/* 底部按鈕區 */}
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            gap: 40,
            width: 232,
            height: 40,
            fontFamily,
            margin: "24px auto 0 auto",
            justifyContent: "center",
            paddingBottom: 40,
          }}
        >
          <button
            style={{
              flex: 1,
              background: "#333",
              borderRadius: 20,
              color: "#fff",
              fontWeight: 500,
              fontSize: 15,
              border: "none",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: 40,
              padding: 0,
              cursor: "pointer",
              fontFamily,
            }}
            onClick={onClose}
          >
            取消
          </button>
          <button
            style={{
              flex: 1,
              background: "#28D1D1",
              borderRadius: 20,
              color: "#222",
              fontWeight: 500,
              fontSize: 15,
              border: "none",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: 40,
              padding: 0,
              cursor: "pointer",
              fontFamily,
            }}
          >
            儲存
          </button>
        </div>
      </div>
    </div>
  );
}
