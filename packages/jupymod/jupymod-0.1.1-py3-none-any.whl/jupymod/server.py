# server.py
import json
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("jupyter-mcp")


def _process_cells_to_xml(
    cells: list, start_idx: int = 0, end_idx: int | None = None
) -> list[str]:
    """
    Process notebook cells into XML format.

    Args:
        cells: List of notebook cells
        start_idx: Starting index (inclusive)
        end_idx: Ending index (exclusive), None for all cells

    Returns:
        List of XML strings representing the cells
    """
    xml_parts = []

    for i, cell in enumerate(cells[start_idx:end_idx], start=start_idx):
        if end_idx and i >= end_idx:
            break
        cell_type = cell["cell_type"]

        # Join source lines into single content
        content = (
            "".join(cell["source"])
            if isinstance(cell["source"], list)
            else cell["source"]
        )

        xml_parts.append(f'<cell type="{cell_type}" id="{i}">')
        xml_parts.append(content)
        xml_parts.append("</cell>")

        if cell_type == "code":
            xml_parts.append("<outputs>")
            for output in cell["outputs"]:
                # Handle stdout output
                if "name" in output and output["name"] == "stdout":
                    xml_parts.append(f"{''.join(output['text'])}")
                # Handle execution results
                elif output["output_type"] == "execute_result":
                    xml_parts.append(f"{''.join(output['data']['text/plain'])}")

            xml_parts.append("</outputs>")
            xml_parts.append("")

    return xml_parts


@mcp.tool()
def get_markdown_representation(notebook_path: str) -> str:
    """
    Get a clean XML representation of a notebook file.

    Args:
        notebook_path: Path to the .ipynb file

    Returns:
        XML string representation of the notebook
    """
    try:
        with open(notebook_path, "r") as f:
            notebook = json.load(f)

        xml_parts = _process_cells_to_xml(notebook["cells"])
        return "\n".join(xml_parts)

    except Exception as e:
        return f"Error reading notebook: {str(e)}"


@mcp.tool()
def get_markdown_representation_subset(
    notebook_path: str, start_idx: int, end_idx: int
) -> str:
    """
    Get a clean XML representation of a subset of notebook cells.

    Args:
        notebook_path: Path to the .ipynb file
        start_idx: Starting cell index (inclusive, 0-based)
        end_idx: Ending cell index (exclusive, 0-based)

    Returns:
        XML string representation of the specified cell range
    """
    try:
        with open(notebook_path, "r") as f:
            notebook = json.load(f)

        num_cells = len(notebook["cells"])

        if start_idx < 0 or start_idx >= num_cells:
            return f"Start index {start_idx} is out of range. Must be between 0 and {num_cells - 1}"

        if end_idx < 0 or end_idx > num_cells:
            return f"End index {end_idx} is out of range. Must be between 0 and {num_cells}"

        if start_idx >= end_idx:
            return f"Start index {start_idx} must be less than end index {end_idx}"

        xml_parts = _process_cells_to_xml(notebook["cells"], start_idx, end_idx)
        return "\n".join(xml_parts)

    except Exception as e:
        return f"Error reading notebook: {str(e)}"


@mcp.tool()
def modify_cell(notebook_path: str, cell_idx: int, content: list[str]) -> str:
    """
    Modify a cell in a notebook file by position.

    Args:
        notebook_path: Path to the .ipynb file
        cell_idx: Index of the cell to modify (0-based)
        content: List of strings representing the cell content

    Returns:
        Success message or error description
    """
    try:
        with open(notebook_path, "r") as f:
            notebook = json.load(f)

        if cell_idx >= len(notebook["cells"]) or cell_idx < 0:
            return f"Cell index {cell_idx} is out of range"

        target_cell = notebook["cells"][cell_idx]

        # Assert cell type is markdown or code
        cell_type = target_cell["cell_type"]
        if cell_type not in ["markdown", "code"]:
            return f"Cell type '{cell_type}' is not supported. Only 'markdown' and 'code' cells can be modified."

        # Update cell content
        target_cell["source"] = content

        # Write back to file
        with open(notebook_path, "w") as f:
            json.dump(notebook, f, indent=2)

        return f"Successfully modified {cell_type} cell at index {cell_idx}"

    except Exception as e:
        return f"Error modifying notebook: {str(e)}"


@mcp.tool()
def add_cell(
    notebook_path: str, cell_idx: int, content: list[str], cell_type: str = "markdown"
) -> str:
    """
    Add a new cell to a notebook file at the specified position.

    Args:
        notebook_path: Path to the .ipynb file
        cell_idx: Index where to insert the new cell (0-based)
        content: List of strings representing the cell content
        cell_type: Type of cell to add ("markdown" or "code", defaults to "markdown")

    Returns:
        Success message or error description
    """
    try:
        with open(notebook_path, "r") as f:
            notebook = json.load(f)

        if cell_type not in ["markdown", "code"]:
            return f"Cell type '{cell_type}' is not supported. Only 'markdown' and 'code' cells can be added."

        if cell_idx < 0 or cell_idx > len(notebook["cells"]):
            return f"Cell index {cell_idx} is out of range. Must be between 0 and {len(notebook['cells'])} (inclusive)"

        # Create new cell
        new_cell = {"cell_type": cell_type, "metadata": {}, "source": content}

        # Add outputs field for code cells
        if cell_type == "code":
            new_cell["execution_count"] = None
            new_cell["outputs"] = []

        # Insert the new cell at the specified position
        notebook["cells"].insert(cell_idx, new_cell)

        # Write back to file
        with open(notebook_path, "w") as f:
            json.dump(notebook, f, indent=2)

        return f"Successfully added {cell_type} cell at index {cell_idx}"

    except Exception as e:
        return f"Error adding cell to notebook: {str(e)}"


@mcp.tool()
def delete_cells(notebook_path: str, cell_indices: list[int]) -> str:
    """
    Delete cells from a notebook file by their indices.

    Args:
        notebook_path: Path to the .ipynb file
        cell_indices: List of cell indices to delete (0-based)

    Returns:
        Success message or error description
    """
    try:
        with open(notebook_path, "r") as f:
            notebook = json.load(f)

        num_cells = len(notebook["cells"])

        # Validate all indices
        for idx in cell_indices:
            if idx < 0 or idx >= num_cells:
                return f"Cell index {idx} is out of range. Must be between 0 and {num_cells - 1}"

        # Check for duplicates
        if len(set(cell_indices)) != len(cell_indices):
            return "Duplicate indices found in cell_indices list"

        original_cells = notebook["cells"]
        new_cells = [
            cell for i, cell in enumerate(notebook["cells"]) if i not in cell_indices
        ]

        notebook["cells"] = new_cells

        # Write back to file
        with open(notebook_path, "w") as f:
            json.dump(notebook, f, indent=2)

        return f"Successfully deleted {len(original_cells) - len(new_cells)} cells at indices: {sorted(cell_indices)}"

    except Exception as e:
        return f"Error deleting cells from notebook: {str(e)}"


def main():
    """Main entry point for the jupymod CLI script."""
    mcp.run()
