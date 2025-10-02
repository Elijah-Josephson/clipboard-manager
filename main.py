# main.py
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from pathlib import Path

APP_NAME = "Iliya's Clipboard Manager"
MAX_ITEMS = 50
DATA_FILE = Path.home() / ".clipboard_manager.json"

def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except Exception:
            pass
    return []

def save_data(items):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(items[:MAX_ITEMS], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Failed to save:", e)

class ClipboardManager:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("700x460")
        self.root.minsize(520, 360)

        self.items = load_data()  # most recent first
        self.filtered = list(self.items)

        # --- UI ---
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        #font customization
        #c_font = font.Font(family , size=12="Roboto")

        top = ttk.Frame(self.root)
        top.pack(fill=X, padx=10, pady=(10, 6))

        ttk.Label(top, text="Search:").pack(side=LEFT, padx=(0,6))
        search_entry = ttk.Entry(top, textvariable=self.search_var)
        search_entry.pack(side=LEFT, fill=X, expand=True)
        search_entry.bind("<KeyRelease>", lambda e: self.apply_filter())

        btn_frame = ttk.Frame(top)
        btn_frame.pack(side=LEFT, padx=8)

        ttk.Button(btn_frame, text="Add Clipboard", command=self.add_clipboard).pack(side=LEFT, padx=4)
        ttk.Button(btn_frame, text="Copy Selected", command=self.copy_selected).pack(side=LEFT, padx=4)
        ttk.Button(btn_frame, text="Delete", command=self.delete_selected).pack(side=LEFT, padx=4)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(side=LEFT, padx=4)

        # List area
        mid = ttk.Frame(self.root)
        mid.pack(fill=BOTH, expand=True, padx=10, pady=(0,10))

        self.listbox = tk.Listbox(mid, activestyle="none", selectmode=tk.SINGLE)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        self.listbox.bind("<Double-Button-1>", lambda e: self.copy_selected())

        scrollbar = ttk.Scrollbar(mid, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=LEFT, fill=Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Right panel: preview
        right = ttk.Frame(mid, width=260)
        right.pack(side=RIGHT, fill=Y, padx=(10,0))

        ttk.Label(right, text="Preview", font=("Segoe UI", 10, "bold")).pack(anchor="nw")
        self.preview = tk.Text(right, wrap="word", height=12, state="disabled")
        self.preview.pack(fill=BOTH, expand=True, pady=(6,4))

        # status
        bottom = ttk.Frame(self.root)
        bottom.pack(fill=X, padx=10, pady=(0,10))
        ttk.Label(bottom, textvariable=self.status_var).pack(side=LEFT)

        # Bind selection change
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.on_select())

        self.refresh_list()

    # --- core actions ---
    def add_clipboard(self):
        try:
            clip = self.root.clipboard_get()
            clip = clip.strip()
            if not clip:
                self.set_status("Clipboard empty.")
                return
        except tk.TclError:
            self.set_status("No text in clipboard.")
            return

        # avoid duplicates: remove existing identical entry
        self.items = [x for x in self.items if x != clip]
        self.items.insert(0, clip)
        if len(self.items) > MAX_ITEMS:
            self.items = self.items[:MAX_ITEMS]
        save_data(self.items)
        self.apply_filter()
        self.set_status("Added clipboard item.")

    def copy_selected(self):
        idx = self.get_selected_index()
        if idx is None:
            self.set_status("No selection.")
            return
        text = self.filtered[idx]
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.set_status("Copied to clipboard.")
            # move copied item to top of history
            self.items = [x for x in self.items if x != text]
            self.items.insert(0, text)
            save_data(self.items)
            self.apply_filter()
        except Exception as e:
            self.set_status(f"Copy failed: {e}")

    def delete_selected(self):
        idx = self.get_selected_index()
        if idx is None:
            self.set_status("No selection to delete.")
            return
        item = self.filtered.pop(idx)
        # remove from master
        self.items = [x for x in self.items if x != item]
        save_data(self.items)
        self.refresh_list()
        self.set_status("Deleted item.")

    def clear_all(self):
        if not messagebox.askyesno("Confirm", "Clear all saved clipboard items?"):
            return
        self.items = []
        save_data(self.items)
        self.apply_filter()
        self.set_status("Cleared all items.")

    # --- helpers ---
    def get_selected_index(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        return sel[0]

    def on_select(self):
        idx = self.get_selected_index()
        if idx is None:
            self.preview.configure(state="normal")
            self.preview.delete("1.0", tk.END)
            self.preview.configure(state="disabled")
            return
        text = self.filtered[idx]
        self.preview.configure(state="normal")
        self.preview.delete("1.0", tk.END)
        self.preview.insert("1.0", text)
        self.preview.configure(state="disabled")

    def apply_filter(self):
        q = self.search_var.get().strip().lower()
        if not q:
            self.filtered = list(self.items)
        else:
            self.filtered = [x for x in self.items if q in x.lower()]
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for item in self.filtered:
            # display a short preview line in listbox
            line = item.splitlines()[0]
            if len(line) > 80:
                line = line[:77] + "..."
            self.listbox.insert(tk.END, line)
        # keep selection if possible
        self.on_select()

    def set_status(self, text):
        self.status_var.set(text)

def main():
    root = tb.Window(themename="superhero")  # pick a clean theme
    app = ClipboardManager(root)
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()

