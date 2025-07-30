import React, { useState, useRef, useEffect } from "react";
import { DatePicker, Tooltip, Button } from 'antd';
import 'antd/dist/reset.css';
import { SearchQuery, SearchModalProps } from './types';
import TagSelector from './TagSelector';
// TODO: TagSelector 可獨立出來，先內嵌
const { RangePicker } = DatePicker;

const fontFamily = "'Inter', 'PingFang TC', 'Microsoft JhengHei', Arial, sans-serif";
const timeOptions = ["昨日", "今日", "近N日", "自訂區間"];
const sourceOptions = ["全部", "Facebook", "Threads"];

export default function SearchModal({
  open,
  mode,
  onClose,
  onSave,
  initialData,
  isSaving = false,
  apiUrl = window.REACT_APP_API_URL || "http://localhost:8000"
}: SearchModalProps) {
  const readOnly = mode === 'view';
  const [title, setTitle] = useState("");
  const [tag, setTag] = useState("");
  const [query, setQuery] = useState("");
  const [time, setTime] = useState(0);
  const [source, setSource] = useState(0);
  const [n, setN] = useState("");
  const [nError, setNError] = useState(false);
  const [titleError, setTitleError] = useState(false);
  const nInputRef = useRef<HTMLInputElement>(null);
  const [range, setRange] = useState<any>(null);
  const [popupOpen, setPopupOpen] = useState(false);
  const tagRef = useRef<HTMLTextAreaElement>(null);
  const queryRef = useRef<HTMLTextAreaElement>(null);
  const [selectedTags, setSelectedTags] = useState<string[]>(["All"]);
  const [tagsList, setTagsList] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const validateN = (val: string) => {
    const num = Number(val);
    return /^[1-9]$|^1[0-9]$|^2[0-9]$|^30$/.test(val) && num >= 1 && num <= 30;
  };

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
      if (initialData) {
        setTitle(initialData.title || "");
        setTime(initialData.time !== undefined ? initialData.time : 0);
        setSource(initialData.source !== undefined ? initialData.source : 0);
        setSelectedTags(initialData.tags || ["All"]);
        setQuery(initialData.query || "");
        setN(initialData.n || "");
        setRange(initialData.range || null);
      } else {
        setTitle("");
        setTime(0);
        setSource(0);
        setSelectedTags(["All"]);
        setQuery("");
        setN("");
        setRange(null);
      }
      fetchTags();
    }
  }, [open, initialData]);

  const fetchTags = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${apiUrl}/api/sheet/kol-list`);
      const data = await response.json();
      if (Array.isArray(data.kols)) {
        setTagsList(data.kols.map((k: any) => k.kol_name || k.kol_id));
      }
    } catch (error) {
      console.error("Error fetching tags:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = () => {
    if (!title.trim()) {
      setTitleError(true);
      return;
    }
    if (time === 2 && !validateN(n)) {
      setNError(true);
      return;
    }
    if (onSave) {
      const formData: SearchQuery = {
        title,
        time,
        source,
        tags: selectedTags,
        query,
        n,
        range
      };
      onSave(formData);
    }
  };

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
        zIndex: 9999
      }}
      onClick={e => {
        if (e.target === e.currentTarget) onClose();
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
          {mode === 'view' ? "閱覽查詢條件" : (mode === 'edit' ? "編輯查詢條件" : "新增查詢條件")}
        </div>
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
            <div style={{ color: "#fff", fontSize: 14, lineHeight: "17px" }}>
              標題 {!readOnly && <span style={{ color: "#FF4C4C" }}>*</span>}
              {titleError && !readOnly && (
                <span style={{ color: "#FF4C4C", marginLeft: 12 }}>此欄位為必填</span>
              )}
            </div>
            <input
              value={title}
              onChange={e => {
                if (!readOnly) {
                  setTitle(e.target.value);
                  if (e.target.value) setTitleError(false);
                }
              }}
              onBlur={() => !readOnly && setTitleError(!title.trim())}
              placeholder={readOnly ? "" : "請輸入查詢標題"}
              disabled={readOnly}
              style={{
                background: "#222",
                borderRadius: 12,
                border: titleError && !readOnly ? "1px solid #FF4C4C" : "none",
                padding: 12,
                width: "100%",
                color: "#fff",
                fontSize: 14,
                outline: "none",
                fontFamily,
                opacity: readOnly ? 0.7 : 1,
              }}
            />
          </div>
          {/* 時間 */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14 }}>
              時間
              {nError && !readOnly && (
                <span style={{ color: "#FF4C4C", marginLeft: 12 }}>請輸入1-30內的數字</span>
              )}
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              {timeOptions.slice(0, 3).map((label, i) => (
                <button
                  key={label}
                  onClick={() => { if (!readOnly) { setTime(i); if (i !== 2) setNError(false); } }}
                  disabled={readOnly}
                  style={{
                    background: i === time ? "#222" : "#222",
                    border: i === time ? "1px solid #28C8C8" : "none",
                    color: "#fff",
                    borderRadius: 12,
                    padding: "12px 20px",
                    fontSize: 14,
                    cursor: readOnly ? "default" : "pointer",
                    opacity: i === time ? 1 : (readOnly ? 0.5 : 0.7),
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
                              if (!readOnly) {
                                setN(e.target.value);
                                setNError(false);
                              }
                            }}
                            onBlur={() => !readOnly && setNError(!validateN(n))}
                            disabled={readOnly}
                            style={{
                              width: 28,
                              margin: "0 2px",
                              background: "transparent",
                              border: "none",
                              color: "#fff",
                              fontSize: 14,
                              textAlign: "center",
                              outline: "none",
                              borderBottom: readOnly ? "none" : "1px solid #28C8C8",
                              opacity: readOnly ? 0.7 : 1,
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
              <Tooltip title="功能還在開發中" placement="top">
                <button
                  disabled={true}
                  style={{
                    background: "#222",
                    border: "none",
                    color: "#fff",
                    borderRadius: 12,
                    padding: "12px 20px",
                    fontSize: 14,
                    cursor: "not-allowed",
                    opacity: 0.5,
                    fontFamily,
                  }}
                >
                  自訂區間
                </button>
              </Tooltip>
            </div>
          </div>
          {/* 資料源 */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14 }}>資料源</div>
            <div style={{ display: "flex", gap: 8 }}>
              {sourceOptions.map((label, i) => (
                <Tooltip key={label} title={i === 2 ? "功能還在開發中" : ""} placement="top">
                  <button
                    onClick={() => !readOnly && i !== 2 && setSource(i)}
                    disabled={readOnly || i === 2}
                    style={{
                      background: i === source ? "#222" : "#222",
                      border: i === source ? "1px solid #28C8C8" : "none",
                      color: "#fff",
                      borderRadius: 12,
                      padding: "12px 20px",
                      fontSize: 14,
                      cursor: readOnly || i === 2 ? "default" : "pointer",
                      opacity: i === source ? 1 : (readOnly || i === 2 ? 0.5 : 0.7),
                      fontFamily,
                    }}
                  >{label}</button>
                </Tooltip>
              ))}
            </div>
          </div>
          {/* KOL */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14 }}>KOL</div>
            <TagSelector
              tagsList={tagsList}
              value={selectedTags}
              onChange={!readOnly ? setSelectedTags : undefined}
              disabled={readOnly}
            />
          </div>
          {/* 檢索口令 */}
          <div style={{ display: "flex", flexDirection: "column", gap: 8, width: "100%" }}>
            <div style={{ color: "#fff", fontSize: 14 }}>檢索口令</div>
            <textarea
              ref={queryRef}
              value={query}
              onChange={e => !readOnly && setQuery(e.target.value)}
              placeholder={readOnly ? "" : "請輸入您想查詢的檢索口令"}
              disabled={readOnly}
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
                opacity: readOnly ? 0.7 : 1,
              }}
            />
          </div>
        </div>
        {/* 底部按鈕區 */}
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            gap: 8,
            width: "auto",
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
              padding: "0 15px",
              cursor: "pointer",
              fontFamily,
              minWidth: "120px",
              maxWidth: "150px",
            }}
            onClick={onClose}
          >
            {readOnly ? "關閉" : "取消"}
          </button>
          {!readOnly && (
            <button
              id="save-button"
              style={{
                flex: 1,
                background: "#28D1D1",
                borderRadius: 20,
                color: "#222",
                fontWeight: 500,
                fontSize: 15,
                border: "none",
                height: 40,
                padding: "0 15px",
                cursor: isSaving ? "not-allowed" : "pointer",
                opacity: isSaving ? 0.7 : 1,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                minWidth: "120px",
                maxWidth: "150px",
              }}
              onClick={(e) => {
                if (!isSaving) {
                  handleSave();
                }
              }}
              disabled={isSaving}
            >
              {isSaving ? "儲存中..." : "儲存"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
