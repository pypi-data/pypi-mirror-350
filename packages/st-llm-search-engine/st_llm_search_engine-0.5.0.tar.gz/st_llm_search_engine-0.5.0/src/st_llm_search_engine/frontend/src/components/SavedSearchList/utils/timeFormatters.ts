export const formatTime = (timestamp: string): string => {
  try {
    const date = new Date(timestamp);
    if (isNaN(date.getTime())) return timestamp;
    return date.toLocaleString('zh-TW', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    }).replace(/\//g, '/');
  } catch (error) {
    console.error('格式化時間錯誤:', error);
    return timestamp;
  }
};

export const getTimeOptionText = (time?: number, n?: string): string => {
  switch(time) {
    case 0: return "昨日";
    case 1: return "今日";
    case 2: return `近${n || "N"}日`;
    case 3: return "自訂區間";
    default: return "今日";
  }
};
