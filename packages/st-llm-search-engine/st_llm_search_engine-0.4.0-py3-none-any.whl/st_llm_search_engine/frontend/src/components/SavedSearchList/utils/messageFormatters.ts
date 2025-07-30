import { SearchResult } from '../types';
import { formatTime, getTimeOptionText } from './timeFormatters';

export const formatSearchResultMessage = (title: string, result: SearchResult, formData: any) => {
  const timeRange = formData.time === 3
    ? `${formData.range ? formData.range[0]?.format('YYYY/M/D HH:mm:ss') : ''} ~ ${formData.range ? formData.range[1]?.format('YYYY/M/D HH:mm:ss') : ''}`
    : getTimeOptionText(formData.time, formData.n);

  return [
    `嗨！我找到了「${title}」的搜索資料啦！🎯✨`,
    `這批資料的時間範圍是 ${timeRange} 📅`,
    `我已經幫你整理好了：💁 資料來源：${result.source || '全部'} 📊 涵蓋KOL：${result.kol || 'All'} ⭐`,
    `總共有 ${result.records.length} 筆資料等著你來探索！👀`,
    `有什麼想過濾的嗎？我很樂意幫你找出這段時間的趨勢喔！`
  ].join('\n');
};

export const formatSearchResultJson = (result: SearchResult) => {
  return `\`\`\`json\n${JSON.stringify(result.records, null, 2)}\n\`\`\``;
};
