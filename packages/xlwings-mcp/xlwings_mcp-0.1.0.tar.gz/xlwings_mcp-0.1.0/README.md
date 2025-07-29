# xlwings-mcp

MCP server for Excel automation via xlwings.

## Features

- Read and write Excel cells and ranges
- Manage Excel workbooks (open, close, save)
- List sheets and workbooks
- Format data as tables

## Installation

```bash
pip install xlwings-mcp
```

## Usage

Run the MCP server:

```bash
xlwings-mcp
```

## Requirements

- Python 3.12+
- xlwings
- Excel application (Windows/macOS)

## MCP Tools

- `get_sheet_names`: Get all sheet names from active workbook
- `read`: Read cells from Excel and format as table
- `write`: Write values to Excel cells
- `open_workbook`: Open Excel file
- `close_workbook`: Close Excel workbook
- `list_open_workbooks`: List all open workbooks
- `save_workbook`: Save workbook
