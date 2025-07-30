from mcp.server.fastmcp import FastMCP
import xlwings as xw  # type: ignore
from tabulate import tabulate
from pathlib import Path
import re

# Create an MCP server
mcp = FastMCP("Excel API")


@mcp.tool()
def get_sheet_names() -> list[str]:
    """Get all sheet names from the active Excel workbook."""
    app = xw.apps.active
    wb = app.books.active
    return [sheet.name for sheet in wb.sheets]


@mcp.tool()
def read(
    sheet_name: str,
    cell_address: str,
    is_expanded_range: bool = False,
    headers: bool = True,
    tablefmt: str = "plain",
) -> str:
    """Read cells from Excel and format as a table.

    Args:
        sheet_name: Name of the sheet
        cell_address: Cell address or range (e.g., 'A1' for expanded, 'A1:C10' for specific range)
        is_expanded_range: If True, expand from the cell to find full data region
        headers: Whether first row contains headers
        tablefmt: Table format (plain, simple, grid, pipe, etc.)
    """
    app = xw.apps.active
    wb = app.books.active
    sheet = wb.sheets[sheet_name]

    # Get values based on whether it's expanded or specific range
    if is_expanded_range:
        values = sheet.range(cell_address).expand().value
        # Parse start cell to get position
        col_letters = "".join(c for c in cell_address if c.isalpha())
        row_num = int("".join(c for c in cell_address if c.isdigit()))
    else:
        values = sheet.range(cell_address).value
        # Parse range to get start position
        start_cell = cell_address.split(":")[0]
        col_letters = "".join(c for c in start_cell if c.isalpha())
        row_num = int("".join(c for c in start_cell if c.isdigit()))

    # Handle single cell case
    if not isinstance(values, list):
        return str(values) if values is not None else ""

    # Handle single row case
    if not isinstance(values[0], list):
        values = [values]

    # Convert None values to empty strings
    clean_values = [
        [str(cell) if cell is not None else "" for cell in row] for row in values
    ]

    # Always add row numbers
    for i, row in enumerate(clean_values):
        row.insert(0, str(row_num + i))

    # Always generate column headers
    start_col = ord(col_letters[0]) - ord("A")
    col_headers = ["Row"]
    for i in range(len(clean_values[0]) - 1):
        col_headers.append(chr(ord("A") + start_col + i))

    if headers and clean_values:
        return tabulate(clean_values[1:], headers=col_headers, tablefmt=tablefmt)
    else:
        return tabulate(clean_values, headers=col_headers, tablefmt=tablefmt)


@mcp.tool()
def write(
    sheet_name: str,
    start_cell: str,
    values: list[list[str]],
    is_expanded_range: bool = False,
    save_on_min_cells_written: int = 0,
) -> str:
    """Write values to a range of cells in Excel.

    Args:
        sheet_name: Name of the sheet
        start_cell: Starting cell address like 'A1', 'B5', etc.
        values: 2D list of values to write
        is_expanded_range: If True, clear the expanded range before writing
        save_on_min_cells_written: If > 0, save the workbook if at least this many cells were written
    """
    app = xw.apps.active
    wb = app.books.active
    sheet = wb.sheets[sheet_name]

    if is_expanded_range:
        # Clear the expanded range first
        sheet.range(start_cell).expand().clear_contents()

    sheet.range(start_cell).value = values
    rows = len(values)
    cols = len(values[0]) if values else 0
    cells_written = rows * cols

    # Save if requested and we wrote at least the minimum cells
    if save_on_min_cells_written > 0 and cells_written >= save_on_min_cells_written:
        wb.save()
        return f"Written {rows}x{cols} range starting at {sheet_name}!{start_cell} and saved workbook"

    return f"Written {rows}x{cols} range starting at {sheet_name}!{start_cell}"


@mcp.tool()
def open_workbook(file_path: str, create_if_not_exists: bool = True) -> str:
    """Open an Excel file in a new workbook.

    Args:
        file_path: Path to the Excel file to open
        create_if_not_exists: If True, create the file if it doesn't exist
    """
    try:
        path = Path(file_path)

        # Check if the file is already open and activate it
        app = xw.apps.active
        for wb in app.books:
            if Path(wb.fullname).resolve() == path.resolve():
                wb.activate()
                return f"Activated already open workbook: {wb.name} with sheets: {[sheet.name for sheet in wb.sheets]}"

        if not path.exists() and create_if_not_exists:
            # Create a new workbook and save it
            # Ensure the directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            wb = xw.Book()
            wb.save(path)
            return f"Created and opened new workbook: {wb.name} with sheets: {[sheet.name for sheet in wb.sheets]}"
        elif not path.exists() and not create_if_not_exists:
            return f"Error: File {file_path} does not exist and create_if_not_exists is False"
        else:
            wb = xw.Book(file_path)
            return f"Opened workbook: {wb.name} with sheets: {[sheet.name for sheet in wb.sheets]}"
    except Exception as e:
        return f"Error opening file: {e}"


@mcp.tool()
def close_workbook(filename: str | None = None) -> str:
    """Close an Excel workbook.

    Args:
        filename: Name of the workbook to close. If None, closes the active workbook.
    """
    try:
        app = xw.apps.active
        if filename is None:
            wb = app.books.active
            wb_name = wb.name
            wb.close()
            return f"Closed active workbook: {wb_name}"
        else:
            for wb in app.books:
                if wb.name == filename:
                    wb_name = wb.name
                    wb.close()
                    return f"Closed workbook: {wb_name}"
            return f"Error: Workbook '{filename}' not found"
    except Exception as e:
        return f"Error closing workbook: {e}"


@mcp.tool()
def list_open_workbooks() -> list[str]:
    """List all currently open Excel workbooks."""
    try:
        app = xw.apps.active
        return [wb.fullname for wb in app.books]
    except Exception as e:
        return [f"Error listing workbooks: {e}"]


@mcp.tool()
def save_workbook(filename: str | None = None) -> str:
    """Save a workbook.

    Args:
        filename: Name of the workbook to save. If None, saves the active workbook.
    """
    try:
        app = xw.apps.active
        if filename is None:
            wb = app.books.active
            wb.save()
            return f"Saved active workbook: {wb.name}"
        else:
            # Find the workbook by name
            for wb in app.books:
                if wb.name == filename:
                    wb.save()
                    return f"Saved workbook: {wb.name}"
            return f"Error: Workbook '{filename}' not found"
    except Exception as e:
        return f"Error saving workbook: {e}"


@mcp.tool()
def get_workbook_names(filename: str | None = None) -> str:
    """Get all defined names from a workbook with their references.

    Args:
        filename: Name of the workbook to get names from. If None, uses the active workbook.
    """
    try:
        app = xw.apps.active
        if filename is None:
            wb = app.books.active
        else:
            # Find the workbook by name
            wb = None
            for book in app.books:
                if book.name == filename:
                    wb = book
                    break
            if wb is None:
                return f"Error: Workbook '{filename}' not found"

        names_info = []
        for name in wb.names:
            names_info.append([name.name, name.refers_to])

        if not names_info:
            return "No named ranges found in workbook"

        return tabulate(names_info, headers=["Name", "Refers To"], tablefmt="plain")
    except Exception as e:
        return f"Error getting workbook names: {e}"


@mcp.tool()
def search(
    pattern: str,
    filename: str | None = None,
    search_sheets: bool = True,
    search_names: bool = True,
    search_values: bool = True,
    search_formulas: bool = True,
    limit: int = 4,
) -> str:
    """Search for a regex pattern in sheet names, defined names, cell values, and formulas.

    Args:
        pattern: Regular expression pattern to search for
        filename: Name of the workbook to search. If None, uses the active workbook.
        search_sheets: If True, search in sheet names
        search_names: If True, search in defined names
        search_values: If True, search in cell values
        search_formulas: If True, search in cell formulas
        limit: Number of results to return per type (default 4)
    """
    try:
        app = xw.apps.active
        if filename is None:
            wb = app.books.active
        else:
            # Find the workbook by name
            wb = None
            for book in app.books:
                if book.name == filename:
                    wb = book
                    break
            if wb is None:
                return f"Error: Workbook '{filename}' not found"

        regex = re.compile(pattern, re.IGNORECASE)
        results = []
        sheet_count = 0
        names_count = 0
        sheet_total = 0
        names_total = 0

        # Search sheet names
        if search_sheets:
            for sheet in wb.sheets:
                if regex.search(sheet.name):
                    sheet_total += 1
                    if sheet_count < limit:
                        results.append(["Sheet Name", sheet.name, "", ""])
                        sheet_count += 1

        # Search defined names
        if search_names:
            for name in wb.names:
                if regex.search(name.name) or regex.search(name.refers_to):
                    names_total += 1
                    if names_count < limit:
                        results.append(["Named Range", name.name, name.refers_to, ""])
                        names_count += 1

        # Search cell values and formulas
        if search_values or search_formulas:
            values_count = 0
            formulas_count = 0
            values_total = 0
            formulas_total = 0

            for sheet in wb.sheets:
                used_range = sheet.used_range
                if used_range is None:
                    continue

                values = used_range.value
                formulas = used_range.formula

                # Handle single cell case
                if not isinstance(values, list):
                    values = [[values]]
                    formulas = [[formulas]]
                elif values and not isinstance(values[0], list):
                    values = [values]
                    formulas = [formulas]

                start_row = used_range.row
                start_col = used_range.column

                for row_idx, (value_row, formula_row) in enumerate(
                    zip(values, formulas)
                ):
                    for col_idx, (value, formula) in enumerate(
                        zip(value_row, formula_row)
                    ):
                        cell_address = f"{chr(ord('A') + start_col - 1 + col_idx)}{start_row + row_idx}"

                        # Search in cell value
                        if (
                            search_values
                            and value is not None
                            and regex.search(str(value))
                        ):
                            values_total += 1
                            if values_count < limit:
                                results.append(
                                    [
                                        "Cell Value",
                                        f"{sheet.name}!{cell_address}",
                                        str(value),
                                        "",
                                    ]
                                )
                                values_count += 1

                        # Search in formula (if different from value)
                        if (
                            search_formulas
                            and formula is not None
                            and formula != value
                            and regex.search(str(formula))
                        ):
                            formulas_total += 1
                            if formulas_count < limit:
                                results.append(
                                    [
                                        "Formula",
                                        f"{sheet.name}!{cell_address}",
                                        str(formula),
                                        "",
                                    ]
                                )
                                formulas_count += 1

        if not results:
            return f"No matches found for pattern: {pattern}"

        # Build summary of truncated results
        truncation_info = []
        if search_sheets and sheet_total > limit:
            truncation_info.append(
                f"Sheet Names: showing {sheet_count} of {sheet_total}"
            )
        if search_names and names_total > limit:
            truncation_info.append(
                f"Named Ranges: showing {names_count} of {names_total}"
            )
        if search_values and values_total > limit:
            truncation_info.append(
                f"Cell Values: showing {values_count} of {values_total}"
            )
        if search_formulas and formulas_total > limit:
            truncation_info.append(
                f"Formulas: showing {formulas_count} of {formulas_total}"
            )

        result_table = tabulate(
            results, headers=["Type", "Location", "Content", ""], tablefmt="plain"
        )

        if truncation_info:
            return result_table + "\n\nResults limited:\n" + "\n".join(truncation_info)
        else:
            return result_table
    except Exception as e:
        return f"Error searching: {e}"


def main() -> None:
    """Entry point for the xlwings-mcp CLI."""
    mcp.run()


if __name__ == "__main__":
    main()
