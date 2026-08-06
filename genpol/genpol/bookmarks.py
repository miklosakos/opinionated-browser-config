from pathlib import Path

def parse_bookmarks(file_path):
    path = Path(file_path)
    if not path.exists():
        return None, [], []

    folder_name = "Managed Bookmarks"
    items = []
    
    with open(path, "r", encoding="utf-8") as f:
        current_name = None
        for line in f:
            line = line.strip()
            if line.startswith("folder:"):
                folder_name = line.split(":", 1)[1].strip()
            elif line.startswith("name:"):
                current_name = line.split(":", 1)[1].strip()
            elif line.startswith("url:") and current_name:
                url = line.split(":", 1)[1].strip()
                items.append({"name": current_name, "url": url})
                current_name = None

    return folder_name, items