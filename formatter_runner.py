import os
import json
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUTPUT_DIR = "release_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TPG_RED = RGBColor(244, 95, 95)

def format_to_docx(data, filename="release_summary.docx"):
    doc = Document()
    title = doc.add_heading("TPG Release Summary", level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.runs[0]
    run.font.color.rgb = TPG_RED

    for entry in data:
        doc.add_heading(f"🔹 {entry['ticket_id']} — {entry['summary']}", level=2)
        for tone, text in entry["summaries"].items():
            para = doc.add_paragraph()
            para.add_run(f"🧠 {tone.title()} Summary:\n").bold = True
            para.add_run(text + "\n")
        doc.add_paragraph("—" * 40)

    footer = doc.sections[0].footer.paragraphs[0]
    footer.text = "Made with 💕 by THE PRODUCT GEEK  |  theproductgeek.club  |  Instagram: @the.productgeek"
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.runs[0].font.size = Pt(9)

    path = os.path.join(OUTPUT_DIR, filename)
    doc.save(path)
    print(f"✅ .docx saved to {path}")

def format_to_markdown(data, filename="release_summary.md"):
    lines = ["# 📦 TPG Release Summary\n"]
    for entry in data:
        lines.append(f"## 🔹 {entry['ticket_id']} — {entry['summary']}")
        for tone, text in entry["summaries"].items():
            lines.append(f"**🧠 {tone.title()} Summary:**\n{text}\n")
        lines.append("---")
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"✅ Markdown saved to {path}")

def format_to_slack_block(data, filename="release_slack.txt"):
    lines = ["*TPG Release Summary*"]
    for entry in data:
        lines.append(f"\n• *{entry['ticket_id']} – {entry['summary']}*")
        for tone, text in entry["summaries"].items():
            lines.append(f"> *{tone.title()} Summary*: {text}")
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"✅ Slack block saved to {path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Format release summaries to various formats")
    parser.add_argument("--format", choices=["docx", "markdown", "slack"], required=True, help="Output format")
    parser.add_argument("--input", default="release_summary.json", help="Input JSON file with release summaries")
    args = parser.parse_args()

    print(f"🛠 Trying to generate output in {args.format} format...")

    if not os.path.exists(args.input):
        print(f"❌ Input file '{args.input}' not found.")
        exit(1)

    with open(args.input) as f:
        data = json.load(f)

    if args.format == "docx":
        format_to_docx(data)
    elif args.format == "markdown":
        format_to_markdown(data)
    elif args.format == "slack":
        format_to_slack_block(data)

    print("✅ All done! Release summary formatted successfully.")
