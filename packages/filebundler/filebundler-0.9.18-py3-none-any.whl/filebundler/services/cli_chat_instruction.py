import pyperclip

def cli_chat_instruction():
    instruction = """
# FileBundler Multi-File Code Bundle Instruction

To provide multiple code files as a single bundle, output your answer in the following XML format. This allows the user to copy all files at once and recreate them with FileBundler CLI.

## Format

Wrap all files in a single `<documents bundle-name="your-bundle-name">` ... `</documents>` block. For each file, use a `<document>` tag with:
- `<source>`: the file path (relative to project root)
- `<document_content>`: the full file content

## Example (for two files)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<documents bundle-name="my-bundle">
    <document index="0">
        <source>
            src/main.py
        </source>
        <document_content>
print('Hello, world!')
        </document_content>
    </document>
    <document index="1">
        <source>
            requirements.txt
        </source>
        <document_content>
requests==2.31.0
        </document_content>
    </document>
</documents>
```

- Indent and format as shown for readability.
- Do not include any text outside the XML block.
- The user will copy the entire XML and run `filebundler cli unbundle` to create all files at once.
"""
    pyperclip.copy(instruction)
    print("\n---\n")
    print(instruction)
    print("\n---\n")
    print("[FileBundler] Chat instruction copied to clipboard! Paste it in your chat to share with others.\n")
