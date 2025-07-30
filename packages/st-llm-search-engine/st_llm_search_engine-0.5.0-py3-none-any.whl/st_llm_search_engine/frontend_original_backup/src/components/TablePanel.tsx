import React, { useMemo } from "react";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { ModuleRegistry } from 'ag-grid-community';
import { AllCommunityModule } from 'ag-grid-community';

ModuleRegistry.registerModules([AllCommunityModule]);

export default function TablePanel({ columns, rows }: { columns: any[]; rows: any[] }) {
  // ag-grid columns 需要 field, headerName
  const agColumns = useMemo(() => columns.map(col => ({
    field: col.field,
    headerName: col.headerName || col.field,
    flex: 1,
    minWidth: 100,
    cellStyle: { fontSize: 15, padding: "6px 8px" },
    headerClass: 'ag-header-cell',
  })), [columns]);

  return (
    <div
      className="ag-theme-alpine"
      style={{
        height: 400,
        width: '100%',
        maxWidth: 900,
        margin: '32px auto',
        border: '3px solid #1e88e5',
        borderRadius: 12,
        boxShadow: '0 2px 16px #0004',
        background: '#fff',
      }}
    >
      <AgGridReact
        rowData={rows}
        columnDefs={agColumns}
        pagination={true}
        paginationPageSize={10}
        domLayout="autoHeight"
        suppressRowClickSelection
        suppressCellFocus
        headerHeight={38}
        rowHeight={36}
      />
    </div>
  );
}
