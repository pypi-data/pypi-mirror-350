import React from 'react';
import { MessageItemProps } from '../types';
import TableRenderer from './TableRenderer';

const MessageItem: React.FC<MessageItemProps> = ({ message, isUser }) => {
  // 格式化時間 - 處理多種時間格式並使用本地時區
  const formatTime = (timestamp: string | number) => {
    try {
      let date: Date;

      // 根據不同格式處理時間戳
      if (typeof timestamp === 'number' || /^\d+$/.test(timestamp.toString())) {
        // 數字格式或純數字字符串，視為 Unix 時間戳（秒）
        const timestampNum = typeof timestamp === 'number' ? timestamp : parseInt(timestamp.toString(), 10);

        // 檢查是秒還是毫秒 (簡單判斷：如果數值小於 10^12，認為是秒)
        const isSeconds = timestampNum < 10000000000;
        date = new Date(isSeconds ? timestampNum * 1000 : timestampNum);
      } else {
        // 其他格式，假設是 ISO 字符串
        date = new Date(timestamp);
      }

      // 檢查日期是否有效
      if (isNaN(date.getTime())) {
        console.error('無效的時間戳記:', timestamp);
        return '';
      }

      // 使用本地化格式，顯示時:分
      const options: Intl.DateTimeFormatOptions = {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false // 使用24小時制
      };

      return date.toLocaleTimeString(undefined, options);
    } catch (error) {
      console.error('時間格式化錯誤:', error, timestamp);
      return '';
    }
  };

  // 檢測並解析消息中的表格
  const parseContent = (content: string) => {
    if (isUser) {
      // 用戶消息直接返回原始內容
      return <div>{content}</div>;
    }

    // 檢查是否包含代碼塊
    if (!content.includes('```')) {
      return <div>{content}</div>;
    }

    console.debug('MessageItem: 檢測到代碼塊，開始解析', content.substring(0, 100) + '...');

    try {
      // 尋找所有可能的表格（代碼塊中的內容）
      const parts: React.ReactNode[] = [];
      let lastIndex = 0;
      let hasTable = false;

      // 更嚴謹的正則表達式，處理各種可能的代碼塊格式
      // 1. ```language\n content \n```
      // 2. ``` content ```
      const regex = /```(?:(csv|markdown|md|table)?)\n?([\s\S]*?)\n?```/g;

      let match;
      let matchCount = 0;

      while ((match = regex.exec(content)) !== null) {
        matchCount++;
        const [fullMatch, codeType, codeContent] = match;

        console.debug(`MessageItem: 找到第 ${matchCount} 個代碼塊，類型: ${codeType || '未指定'}`);

        // 添加表格前的文本
        if (match.index > lastIndex) {
          const textBeforeBlock = content.substring(lastIndex, match.index);
          if (textBeforeBlock.trim()) {
            parts.push(<div key={`text-${parts.length}`}>{textBeforeBlock}</div>);
          }
        }

        // 判斷是否為表格
        const isTable =
          // 明確標記為表格格式
          codeType === 'csv' ||
          codeType === 'markdown' ||
          codeType === 'md' ||
          codeType === 'table' ||
          // 或者內容符合表格特徵
          (codeContent.includes('|') &&
           codeContent.split('\n').length >= 3 &&
           codeContent.split('\n')[0].includes('|') &&
           codeContent.split('\n')[1].includes('-')) ||
          // CSV 格式特徵
          (codeContent.includes(',') &&
           codeContent.split('\n').length >= 2 &&
           codeContent.split('\n')[0].includes(','));

        if (isTable) {
          console.debug('MessageItem: 識別為表格，將使用 TableRenderer 渲染');
          hasTable = true;

          // 清理一下表格內容，確保沒有多餘的空行
          const cleanTableContent = codeContent.trim();

          // 渲染表格，注意這裡不再需要額外的容器限制寬度
          parts.push(
            <div key={`table-container-${parts.length}`} style={{ width: '100%' }}>
              <TableRenderer key={`table-${parts.length}`} tableData={cleanTableContent} />
            </div>
          );
        } else {
          console.debug('MessageItem: 識別為普通代碼塊');
          // 不是表格，保留原始代碼塊
          parts.push(
            <pre key={`code-${parts.length}`} style={{
              background: '#333',
              padding: '12px',
              borderRadius: '8px',
              overflowX: 'auto',
              fontSize: '14px',
              margin: '16px 0'
            }}>
              <code>{codeContent}</code>
            </pre>
          );
        }

        lastIndex = match.index + fullMatch.length;
      }

      // 添加最後一部分文本
      if (lastIndex < content.length) {
        const remainingText = content.substring(lastIndex);
        if (remainingText.trim()) {
          parts.push(<div key={`text-${parts.length}`}>{remainingText}</div>);
        }
      }

      console.debug(`MessageItem: 解析完成，共 ${parts.length} 個部分，${matchCount} 個代碼塊`);

      if (parts.length > 0) {
        return <>{parts}</>;
      }
    } catch (error) {
      console.error('解析消息內容時出錯:', error);
    }

    // 如果解析失敗或沒有找到任何內容，直接返回原始內容
    return <div>{content}</div>;
  };

  const formattedTime = formatTime(message.created_at);

  // 檢測消息是否包含表格
  const hasTable = !isUser && message.content.includes('```') &&
    (message.content.includes('```csv') ||
     message.content.includes('```markdown') ||
     message.content.includes('```md') ||
     message.content.includes('```table') ||
     (message.content.includes('|') && message.content.includes('-')));

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: isUser ? 'row-reverse' : 'row',
        alignItems: 'flex-end',
        marginBottom: 16,
        width: '100%'
      }}
    >
      <div
        style={{
          background: isUser ? '#222' : 'none',
          color: '#fff',
          borderRadius: 12,
          padding: '12px 16px',
          maxWidth: isUser ? '66%' : (hasTable ? '95%' : '70%'), // 包含表格時增加寬度
          width: hasTable ? '95%' : 'auto', // 包含表格時設定固定寬度
          wordBreak: 'break-word',
          fontSize: 16,
          marginLeft: isUser ? 0 : 12,
          marginRight: isUser ? 12 : 0,
          alignSelf: isUser ? 'flex-end' : 'flex-start',
        }}
      >
        {parseContent(message.content)}
        <div style={{
          fontSize: 12,
          color: '#aaa',
          marginTop: 4,
          textAlign: isUser ? 'right' : 'left'
        }}>
          {formattedTime}
        </div>
      </div>
    </div>
  );
};

export default MessageItem;
