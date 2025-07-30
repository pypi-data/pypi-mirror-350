export interface SearchQuery {
  title: string;
  time: number;
  source: number;
  tags: string[];
  query: string;
  n?: string;
  range: null | any;
}

export interface SavedSearch {
  id: number;
  title: string;
  account: string;
  order?: number;
  query: SearchQuery;
  createdAt: string;
}

export interface SearchFormData {
  timeOption: number;
  startDate?: string;
  endDate?: string;
  source?: string[];
  kol?: string[];
}

export interface SearchResult {
  records: any[];
  total: number;
  timeRange: {
    start: string;
    end: string;
  };
  source?: string;
  kol?: string;
}

export interface CacheData {
  searches: SavedSearch[];
  timestamp: number;
}

export interface SearchListHeaderProps {
  onAdd: () => void;
  onRefresh: () => void;
  onClear: () => void;
  isRefreshing: boolean;
}

export interface SearchListContentProps {
  searches: SavedSearch[];
  onEdit: (search: SavedSearch) => void;
  onDelete: (id: number) => void;
  onExecute: (search: SavedSearch) => void;
  onReorder: (fromIndex: number, toIndex: number) => void;
  isProcessing: boolean;
  processingTitle: string | null;
}

export interface SearchProcessingOverlayProps {
  isVisible: boolean;
  title: string;
  onCancel: () => void;
}

export interface SearchItemProps {
  search: SavedSearch;
  onEdit: (search: SavedSearch) => void;
  onDelete: (id: number) => void;
  onExecute: (search: SavedSearch) => void;
  isSystem: boolean;
}
