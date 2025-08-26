import nbformat
import sys
from pathlib import Path

def notebook_to_markdown(ipynb_path, md_path):
    # Load the notebook
    with open(ipynb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    
    md_lines = []

    for cell in nb.cells:
        if cell.cell_type == "markdown":
            # Just append markdown as-is
            md_lines.append(cell.source)
            md_lines.append("")  # blank line for separation
        elif cell.cell_type == "code":
            # Format code cells
            md_lines.append("```python")
            md_lines.append(cell.source)
            md_lines.append("```")
            md_lines.append("")  # blank line for separation

    # Write out to Markdown file
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"Exported {ipynb_path} → {md_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ipynb_to_md.py notebook.ipynb output.md")
    else:
        ipynb_file = Path(sys.argv[1])
        md_file = Path(sys.argv[2])
        notebook_to_markdown(ipynb_file, md_file)