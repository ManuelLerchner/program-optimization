from typing import Any, Sequence, List


class TableFormatter:
    @staticmethod
    def format_cell(value: Any, width: int, align: str = "^") -> str:
        """Format a single cell value with given width and alignment."""
        value_str = str(value)
        format_str = "{:" + align + str(width) + "}"
        return format_str.format(value_str)

    @staticmethod
    def get_column_widths(headers: Sequence[Any], rows: Sequence[Sequence[Any]],
                          min_width: int = 10, padding: int = 2) -> List[int]:
        """Calculate optimal column widths based on content."""
        widths = [min_width] * len(headers)

        # Check headers
        for i, header in enumerate(headers):
            widths[i] = max(widths[i], len(str(header)) + padding)

        # Check all rows
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)) + padding)

        return widths

    def print_table(self, headers: Sequence[Any], rows: Sequence[Sequence[Any]],
                    title: str = "", min_width: int = 10, padding: int = 2) -> None:
        """
        Print a formatted table with headers and rows.

        Args:
            headers: Sequence of column headers
            rows: Sequence of rows, where each row is a sequence of values
            title: Optional table title
            min_width: Minimum column width
            padding: Padding between columns
        """
        # Calculate column widths
        widths = self.get_column_widths(headers, rows, min_width, padding)
        total_width = sum(widths) + len(widths) + 1

        # Print title if provided
        if title:
            print("\n" + "=" * total_width)
            print(self.format_cell(title, total_width))
            print("=" * total_width)

        # Print headers
        print("┌" + "┬".join("─" * width for width in widths) + "┐")
        print("│" + "│".join(self.format_cell(header, width)
                             for header, width in zip(headers, widths)) + "│")
        print("├" + "┼".join("─" * width for width in widths) + "┤")

        # Print rows
        for row in rows:
            print("│" + "│".join(self.format_cell(cell, width)
                                 for cell, width in zip(row, widths)) + "│")

        # Print bottom border
        print("└" + "┴".join("─" * width for width in widths) + "┘")
