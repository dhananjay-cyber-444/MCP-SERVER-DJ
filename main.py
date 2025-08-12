from mcp.server.fastmcp import FastMCP
import os
import time

# Base directory where all operations will happen
BASE_DIR = r"D:\mrp79\Downloads" 

# Create the MCP server
mcp = FastMCP("FileSystem")

def find_file(filename: str) -> str:
    """
    Search for the file in BASE_DIR and subfolders.
    Returns full path if found, else None.
    """
    for root, _, files in os.walk(BASE_DIR):
        if filename in files or filename in _:
            return os.path.join(root, filename)
    return None

# Tool: Rename file with confirmation
@mcp.tool()
def rename_file(old_name: str, new_name: str, confirm: bool = False) -> str:
    """
    Rename a file or folder inside BASE_DIR or its subfolders.
    """
    old_path = find_file(old_name)
    if not old_path:
        return f"❌ File '{old_name}' not found in {BASE_DIR} or subfolders."

    new_path = os.path.join(os.path.dirname(old_path), new_name)

    if not confirm:
        return f"⚠️ Found '{old_name}' at {old_path}. Rename to '{new_name}'? Run again with confirm=True to proceed."

    try:
        os.rename(old_path, new_path)
        return f"✅ Renamed '{old_name}' to '{new_name}' at {os.path.dirname(old_path)}."
    except Exception as e:
        return f"Error renaming: {e}"

# Tool: Delete file with confirmation
@mcp.tool()
def delete_file(filename: str, confirm: bool = False) -> str:
    """
    Delete a file inside BASE_DIR or its subfolders.
    """
    file_path = find_file(filename)
    if not file_path:
        return f"❌ File '{filename}' not found in {BASE_DIR} or subfolders."

    if os.path.isdir(file_path):
        return "Error: Path is a directory, not a file."

    if not confirm:
        return f"⚠️ Found '{filename}' at {file_path}. Delete it? Run again with confirm=True to proceed."

    try:
        os.remove(file_path)
        return f"🗑 Deleted '{filename}' from {file_path}."
    except Exception as e:
        return f"Error deleting: {e}"

# Tool: File details
@mcp.tool()
def file_details(filename: str) -> str:
    """
    Get file details for a file inside BASE_DIR or subfolders.
    """
    file_path = find_file(filename)
    if not file_path:
        return f"❌ File '{filename}' not found in {BASE_DIR} or subfolders."

    try:
        size = os.path.getsize(file_path)
        mtime = time.ctime(os.path.getmtime(file_path))
        ftype = "Directory" if os.path.isdir(file_path) else "File"
        return f"📄 Type: {ftype}\n📏 Size: {size} bytes\n🕒 Modified: {mtime}\n📍 Location: {file_path}"
    except Exception as e:
        return f"Error fetching details: {e}"

if __name__ == "__main__":
    mcp.run()
