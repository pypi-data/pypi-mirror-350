import React, { useMemo, useRef } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { ModuleRegistry } from 'ag-grid-community';
import { AllCommunityModule } from 'ag-grid-community';

ModuleRegistry.registerModules([AllCommunityModule]);

interface TableRendererProps {
  tableData: string;
}

const TableRenderer: React.FC<TableRendererProps> = ({ tableData }) => {
  const gridRef = useRef<any>(null);

  // Parse table data
  const { rowData, columnDefs, parseError } = useMemo(() => {
    try {
      if (!tableData) {
        return { rowData: [], columnDefs: [], parseError: null };
      }

      // Determine table format and parse accordingly
      if (tableData.includes('|')) {
        return parseMarkdownTable(tableData);
      } else if (tableData.includes(',') || tableData.includes('\t')) {
        return parseCSVTable(tableData, tableData.includes('\t') ? '\t' : ',');
      } else {
        return { rowData: [], columnDefs: [], parseError: '無法識別的表格格式' };
      }
    } catch (error) {
      return {
        rowData: [],
        columnDefs: [],
        parseError: `解析錯誤: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }, [tableData]);

  // Export functions with proper quote handling
  const exportCSV = () => {
    if (gridRef.current?.api) {
      gridRef.current.api.exportDataAsCsv({
        fileName: `表格數據_${new Date().toISOString().split('T')[0]}.csv`,
        processCellCallback: (params: any) => {
          // Handle special characters for CSV export
          if (params.value === null || params.value === undefined) {
            return '';
          }
          const valueString = String(params.value);
          // Escape quotes and wrap in quotes if contains comma, quote or newline
          if (valueString.includes(',') || valueString.includes('"') || valueString.includes('\n')) {
            return `"${valueString.replace(/"/g, '""')}"`;
          }
          return valueString;
        }
      });
    }
  };

  // 匯出 JSON 功能
  const exportJSON = () => {
    if (gridRef.current?.api) {
      // 獲取所有行數據
      const allData = [];
      gridRef.current.api.forEachNode((node: any) => {
        if (node.data) {
          allData.push(node.data);
        }
      });

      // 創建 JSON 字符串
      const jsonString = JSON.stringify(allData, null, 2);

      // 創建 Blob 對象
      const blob = new Blob([jsonString], { type: 'application/json' });

      // 創建下載連結
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `表格數據_${new Date().toISOString().split('T')[0]}.json`;

      // 觸發下載
      document.body.appendChild(link);
      link.click();

      // 清理
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
  };

  // If there's a parse error, show error message
  if (parseError) {
    return (
      <div style={{
        padding: '12px',
        background: '#333',
        color: '#ff4d4f',
        borderRadius: '8px',
        marginTop: '16px',
        marginBottom: '16px'
      }}>
        <p>表格解析錯誤: {parseError}</p>
      </div>
    );
  }

  // 自定義樣式，確保表格內容和分頁控制項正確顯示
  const customStyles = `
    .ag-theme-alpine {
      --ag-header-background-color: #f5f5f5;
      --ag-odd-row-background-color: #fff;
      --ag-row-border-color: #ddd;
      --ag-header-column-separator-color: #ddd;
    }

    .ag-theme-alpine .ag-paging-panel {
      border-top: 1px solid #ddd;
      background-color: #f5f5f5;
      padding: 8px;
      color: #333;
    }

    .ag-theme-alpine .ag-paging-button {
      color: #1e88e5;
    }

    .ag-theme-alpine .ag-cell {
      color: #333;
    }

    .ag-theme-alpine .ag-header-cell-label {
      font-weight: bold;
    }
  `;

  return (
    <div
      className="ag-theme-alpine"
      style={{
        width: '100%',
        maxWidth: '100%',
        margin: '16px auto',
        border: '1px solid #1e88e5',
        borderRadius: 8,
        background: '#fff',
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column'
      }}
    >
      <style>{customStyles}</style>

      {/* 表格主體 */}
      <div style={{ height: '430px', overflow: 'hidden' }}>
        <AgGridReact
          ref={gridRef}
          rowData={rowData}
          columnDefs={columnDefs}
          pagination={true}
          paginationPageSize={10}
          paginationPageSizeSelector={[10, 20, 50, 100]}
          domLayout="normal"
          headerHeight={38}
          rowHeight={36}
          defaultColDef={{
            flex: 1,
            minWidth: 120,
            filter: true,
            sortable: true,
            resizable: true,
            cellStyle: { fontSize: 15, padding: "6px 12px" }
          }}
          suppressNoRowsOverlay={false}
          overlayNoRowsTemplate="<span style='color: #666; padding: 10px;'>無數據</span>"
        />
      </div>

      {/* 下載按鈕固定在底部 */}
      <div style={{
        display: 'flex',
        justifyContent: 'flex-end',
        padding: '8px 12px',
        backgroundColor: '#f5f5f5',
        borderTop: '1px solid #ddd'
      }}>
        <button
          onClick={exportCSV}
          style={{
            backgroundColor: '#1e88e5',
            color: 'white',
            border: 'none',
            padding: '6px 12px',
            borderRadius: '4px',
            marginRight: '8px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: 'bold'
          }}
        >
          下載 CSV
        </button>
        <button
          onClick={exportJSON}
          style={{
            backgroundColor: '#1e88e5',
            color: 'white',
            border: 'none',
            padding: '6px 12px',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: 'bold'
          }}
        >
          下載 JSON
        </button>
      </div>
    </div>
  );
};

// Helper function to parse Markdown tables
function parseMarkdownTable(markdownTable: string) {
  const rows = markdownTable.trim().split('\n');

  // Need at least header row, separator row, and one data row
  if (rows.length < 3) {
    return { rowData: [], columnDefs: [], parseError: 'Markdown 表格格式不正確: 行數不足' };
  }

  // Parse header row
  const headerRow = rows[0].trim();
  const headers = headerRow
    .split('|')
    .map(h => h.trim())
    .filter(h => h.length > 0);

  if (headers.length === 0) {
    return { rowData: [], columnDefs: [], parseError: 'Markdown 表格格式不正確: 無法解析標題' };
  }

  // Create column definitions
  const columnDefs = headers.map(header => ({
    field: header,
    headerName: header,
    flex: 1,
    minWidth: 120,
    filter: true,
    sortable: true,
    resizable: true
  }));

  // Skip separator row (second row), parse data from third row onwards
  const dataRows = rows.slice(2);
  const rowData = dataRows.map(row => {
    const cells = row
      .split('|')
      .map(cell => cell.trim())
      .filter((_, i) => i > 0 && i <= headers.length);

    const rowObj: Record<string, any> = {};
    headers.forEach((header, i) => {
      rowObj[header] = cells[i] || '';
    });

    return rowObj;
  });

  return { rowData, columnDefs, parseError: null };
}

// Helper function to parse CSV/TSV tables
function parseCSVTable(csvTable: string, delimiter: string = ',') {
  const rows = csvTable.trim().split('\n');

  if (rows.length < 2) {
    return { rowData: [], columnDefs: [], parseError: 'CSV 表格數據不足' };
  }

  // Parse header row
  const headerRow = rows[0];
  const headers = headerRow
    .split(delimiter)
    .map(h => h.trim().replace(/^"|"$/g, ''));

  if (headers.length === 0) {
    return { rowData: [], columnDefs: [], parseError: 'CSV 表格格式不正確: 無法解析標題' };
  }

  // Create column definitions
  const columnDefs = headers.map(header => ({
    field: header,
    headerName: header,
    flex: 1,
    minWidth: 120,
    filter: true,
    sortable: true,
    resizable: true
  }));

  // Parse data rows - properly handle quoted values with commas
  const dataRows = rows.slice(1);
  const rowData = dataRows.map(row => {
    // More robust CSV parsing that handles quotes
    const cells: string[] = [];
    let currentCell = '';
    let inQuotes = false;

    for (let i = 0; i < row.length; i++) {
      const char = row[i];

      if (char === '"') {
        if (inQuotes && i + 1 < row.length && row[i + 1] === '"') {
          // Double quotes inside quotes - add a single quote
          currentCell += '"';
          i++;
        } else {
          // Toggle quote mode
          inQuotes = !inQuotes;
        }
      } else if (char === delimiter && !inQuotes) {
        // End of cell
        cells.push(currentCell);
        currentCell = '';
      } else {
        // Regular character
        currentCell += char;
      }
    }

    // Add the last cell
    cells.push(currentCell);

    const rowObj: Record<string, any> = {};
    headers.forEach((header, i) => {
      rowObj[header] = cells[i] || '';
    });

    return rowObj;
  });

  return { rowData, columnDefs, parseError: null };
}

export default TableRenderer;
