import sys
import html
import pyperclip
import xml.etree.ElementTree as ET

from pathlib import Path

def cli_unbundle():
    print("After copying your FileBundler code bundle to the clipboard, simply press Enter.\n(Do NOT paste the bundle into the terminal; we'll fetch it directly from your clipboard.)\nIf you prefer to paste manually (visible), type any character and press Enter.")
    try:
        choice = input()
        if choice.strip() == "":
            pasted = pyperclip.paste()
        else:
            print("Paste your bundle below. Press Ctrl+D (Unix/macOS) or Ctrl+Z then Enter (Windows) when done:")
            pasted = sys.stdin.read()
    except Exception as e:
        print(f"Error reading input: {e}")
        sys.exit(1)
    # Remove markdown code block markers if present
    lines = pasted.splitlines()
    if lines and lines[0].strip().startswith('```'):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith('```'):
        lines = lines[:-1]
    pasted_clean = '\n'.join(lines)
    if len(pasted_clean) < 20 or '<documents' not in pasted_clean:
        print("Error: Pasted input is too short or missing <documents> tag. Please ensure you have copied the entire code bundle.")
        sys.exit(1)
    try:
        root = ET.fromstring(pasted_clean)
        if root.tag != "documents":
            raise ValueError("Root tag is not <documents>.")
        created_files = []
        for doc in root.findall("document"):
            source_elem = doc.find("source")
            content_elem = doc.find("document_content")
            if source_elem is None or content_elem is None:
                print("Warning: Skipping a <document> missing <source> or <document_content>.")
                continue
            file_path = source_elem.text.strip() if source_elem.text else None
            file_content = content_elem.text or ""
            # Unescape XML entities in file content
            file_content = html.unescape(file_content)
            if not file_path:
                print("Warning: Skipping a <document> with empty <source>.")
                continue
            # Create parent directories if needed
            out_path = Path(file_path)
            if not out_path.parent.exists():
                out_path.parent.mkdir(parents=True, exist_ok=True)
            # Write file
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(file_content)
            created_files.append(str(out_path))
        if created_files:
            print(f"[FileBundler] Created {len(created_files)} files:")
            for f in created_files:
                print(f"  - {f}")
        else:
            print("[FileBundler] No files were created. Please check your bundle.")
    except Exception as e:
        print("Error: Failed to parse the code bundle. Please ensure you have pasted a valid bundle.")
        print(f"Details: {e}")
        sys.exit(1)
