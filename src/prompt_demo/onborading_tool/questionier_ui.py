import logging
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
import requests
import re
import textwrap
import sys

CHUNK_SIZE = 1500
OLLAMA_MODEL="gemma3"


root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


# --- CORE LOGIC ---

def load_code_chunks(folder):
    chunks = []
    for path in Path(folder).rglob("*.py"):
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            logging.error(f"Skipping {path}: {e}")
            continue
        for i in range(0, len(content), CHUNK_SIZE):
            chunk = content[i:i + CHUNK_SIZE]
            chunks.append({"file": str(path), "content": chunk})
    return chunks

def extract_classes(folder):
    classes = []
    for path in Path(folder).rglob("*.py"):
        try:
            text = path.read_text(encoding="utf-8")
            matches = re.findall(r"^class\s+(\w+)", text, re.MULTILINE)
            for cls in matches:
                classes.append((str(path.relative_to(folder)), cls))
        except Exception as e:
            logging.error(f"Error in {path}: {e}")
    return classes

def build_prompt(code_chunks, selected_class):
    context = "\n\n".join(
        [f"# From {c['file']}:\n{textwrap.indent(c['content'], '    ')}" for c in code_chunks]
    )
    return f"""
You're a Python expert. Here's part of a codebase:

{context}

Create a multiple-choice questionnaire (5 questions) about the class `{selected_class}` to evaluate a new hire.
Each question must have:
- 4 options (A-D)
- The correct answer clearly marked
- A short explanation of the answer

Format in Markdown.
"""


def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    res = requests.post(url, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })
    return res.json()["response"]

def save_markdown(markdown, class_name):
    safe = re.sub(r'\W+', '_', class_name)
    filename = f"quiz_{safe}.md"
    Path(filename).write_text(markdown, encoding="utf-8")
    return filename

# --- UI ---

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Class Quiz Generator - Ollama LLaMA 3")

        # Folder selector
        self.folder_frame = tk.Frame(root)
        self.folder_frame.pack(fill="x", padx=10, pady=5)

        self.folder_label = tk.Label(self.folder_frame, text="Code Folder:")
        self.folder_label.pack(side="left")

        self.folder_path = tk.StringVar()
        self.folder_entry = tk.Entry(self.folder_frame, textvariable=self.folder_path, width=50)
        self.folder_entry.pack(side="left", padx=5)

        self.browse_btn = tk.Button(self.folder_frame, text="Browse", command=self.browse_folder)
        self.browse_btn.pack(side="left")

        # Class combo
        self.combo_label = tk.Label(root, text="Select Class:")
        self.combo_label.pack(anchor="w", padx=10)

        self.class_combo = ttk.Combobox(root, state="readonly", width=60)
        self.class_combo.pack(fill="x", padx=10, pady=5)

        # Generate button
        self.gen_btn = tk.Button(root, text="Generate Questionnaire", command=self.generate)
        self.gen_btn.pack(pady=10)


    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            classes = extract_classes(folder)
            self.class_map = {f"{mod} → {cls}": cls for mod, cls in classes}
            self.class_combo["values"] = list(self.class_map.keys())
            if classes:
                self.class_combo.current(0)

    def generate(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder.")
            return

        selected = self.class_combo.get()
        if not selected:
            messagebox.showerror("Error", "Please select a class.")
            return

        class_name = self.class_map[selected]

        try:
            chunks = load_code_chunks(folder)
            prompt = build_prompt(chunks, class_name)
            response = ask_ollama(prompt)
            path = save_markdown(response, class_name)
            logging.info(f"Generated {path}")
        except Exception as e:
            logging.error(f"\n❌ Error: {e}")

# --- MAIN ---
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.geometry("700x600")
    root.mainloop()
