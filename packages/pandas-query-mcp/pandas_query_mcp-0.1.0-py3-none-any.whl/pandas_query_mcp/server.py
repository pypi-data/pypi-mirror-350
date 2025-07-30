import pandas as pd
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Pandas Query", debug=True)
_df = None


@mcp.tool()
def describe() -> str:
    """Describe the dataframe"""
    return _df.describe().to_markdown()


@mcp.tool()
def head() -> str:
    """Head the dataframe"""
    return _df.head().to_markdown()


@mcp.tool()
def tail() -> str:
    """Tail the dataframe"""
    return _df.tail().to_markdown()


@mcp.tool()
def query(query: str) -> str:
    """Query the dataframe"""
    return _df.query(query).to_markdown()


def main():
    global _df
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--sheet", type=str, default="0")
    args = parser.parse_args()
    file_path = args.file
    if file_path.endswith(".csv"):
        _df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        if args.sheet.isdigit():
            _df = pd.read_excel(file_path, sheet_name=int(args.sheet))
        else:
            _df = pd.read_excel(file_path, sheet_name=args.sheet)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    print("Starting pandas query mcp server.")
    mcp.run(transport="stdio")
