export interface SearchQuery {
  title: string;
  time?: number;
  source?: number;
  tags?: string[];
  query?: string;
  n?: string;
  range?: any;
}

export interface SearchModalProps {
  open: boolean;
  mode: 'create' | 'edit' | 'view';
  onClose: () => void;
  onSave?: (data: SearchQuery) => Promise<void>;
  initialData?: SearchQuery | null;
  isSaving?: boolean;
  apiUrl?: string;
}
