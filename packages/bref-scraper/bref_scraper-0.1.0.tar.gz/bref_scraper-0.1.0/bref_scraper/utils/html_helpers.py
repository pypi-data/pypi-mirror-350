from bs4.element import Tag

def safe_text_from_cell(row: Tag, stat: str, is_link: bool=False, default: str =""):
    cell = row.find("td", {"data-stat": stat}) or row.find("th", {"data-stat": stat})
    if not cell:
        return default
    if is_link:
        link = cell.find("a")
        return link.text.strip() if link else default
    return cell.text.strip()