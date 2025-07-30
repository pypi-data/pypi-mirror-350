# filebundler/utils/language_formatting.py
from pathlib import Path


def set_language_from_filename(file: Path):
    file_extension = file.suffix.lower()

    if file_extension in [".py"]:
        language = "python"
    elif file_extension in [".js", ".jsx", ".ts", ".tsx"]:
        language = "javascript"
    elif file_extension in [".html", ".htm"]:
        language = "html"
    elif file_extension in [".css"]:
        language = "css"
    elif file_extension in [".md"]:
        language = "markdown"
    elif file_extension in [".json"]:
        language = "json"
    elif file_extension in [".yml", ".yaml"]:
        language = "yaml"
    else:
        language = None

    return language
