# main.py
import json
import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as tb
from pathlib import Path

APP_NAME = "Iliya's Clipboard Manager"
MAX_ITEMS = 50
DATA_FILE = Path.home() / ".clipboard_manager.json"

# Core Palette
ABYSS_NAVY = "#0B1325"
OCEANIC_NAVY = "#1A2942"
PLASMA_GREEN = "#00E676"
BIOLUMINESCENT_MINT = "#69FFC3"
PURE_WHITE = "#FFFFFF"
GLASS_PANEL = "#152039"
GLASS_BORDER = "#3A4B67"
MUTED_TEXT = "#9BA9BF"

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
        self.root.geometry("900x600")
        self.root.minsize(520, 360)
        self.root.configure(bg=ABYSS_NAVY)

        self.items = load_data()  # most recent first
        self.filtered = list(self.items)

        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")

        # Header and search controls.
        header = tk.Frame(self.root, bg=ABYSS_NAVY)
        header.pack(fill=tk.X, padx=24, pady=(22, 16))

        title_block = tk.Frame(header, bg=ABYSS_NAVY)
        title_block.pack(side=tk.LEFT)
        tk.Label(
            title_block,
            text="CLIPBOARD",
            bg=ABYSS_NAVY,
            fg=BIOLUMINESCENT_MINT,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        tk.Label(
            title_block,
            text="Your saved moments",
            bg=ABYSS_NAVY,
            fg=PURE_WHITE,
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", pady=(2, 0))

        search_panel = tk.Frame(
            header,
            bg=GLASS_PANEL,
            highlightthickness=1,
            highlightbackground=GLASS_BORDER,
        )
        search_panel.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(40, 0), ipady=2)
        tk.Label(
            search_panel,
            text="⌕",
            bg=GLASS_PANEL,
            fg=BIOLUMINESCENT_MINT,
            font=("Segoe UI", 16),
        ).pack(side=tk.LEFT, padx=(12, 4))
        search_entry = tk.Entry(
            search_panel,
            textvariable=self.search_var,
            bg=GLASS_PANEL,
            fg=PURE_WHITE,
            insertbackground=BIOLUMINESCENT_MINT,
            relief=tk.FLAT,
            bd=0,
            font=("Segoe UI", 10),
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 12), ipady=8)
        search_entry.bind("<KeyRelease>", lambda e: self.apply_filter())

        action_bar = tk.Frame(self.root, bg=ABYSS_NAVY)
        action_bar.pack(fill=tk.X, padx=24, pady=(0, 16))
        self.make_button(action_bar, "＋  Add Clipboard", self.add_clipboard, primary=True).pack(side=tk.LEFT)
        self.make_button(action_bar, "Copy Selected", self.copy_selected).pack(side=tk.LEFT, padx=(8, 0))
        self.make_button(action_bar, "Delete", self.delete_selected).pack(side=tk.LEFT, padx=(8, 0))
        self.make_button(action_bar, "Clear All", self.clear_all).pack(side=tk.LEFT, padx=(8, 0))

        # Main glass workspace.
        mid = tk.Frame(self.root, bg=ABYSS_NAVY)
        mid.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 14))

        list_card = tk.Frame(
            mid,
            bg=GLASS_PANEL,
            highlightthickness=1,
            highlightbackground=GLASS_BORDER,
        )
        list_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_heading = tk.Frame(list_card, bg=GLASS_PANEL)
        list_heading.pack(fill=tk.X, padx=16, pady=(14, 10))
        tk.Label(
            list_heading,
            text="List",
            bg=GLASS_PANEL,
            fg=PURE_WHITE,
            font=("Segoe UI", 10, "bold"),
        ).pack(side=tk.LEFT)
        self.count_label = tk.Label(
            list_heading,
            text="",
            bg=GLASS_PANEL,
            fg=MUTED_TEXT,
            font=("Segoe UI", 9),
        )
        self.count_label.pack(side=tk.RIGHT)

        list_body = tk.Frame(list_card, bg=GLASS_PANEL)
        list_body.pack(fill=tk.BOTH, expand=True, padx=(16, 10), pady=(0, 16))
        self.listbox = tk.Listbox(
            list_body,
            activestyle="none",
            selectmode=tk.SINGLE,
            bg=OCEANIC_NAVY,
            fg=PURE_WHITE,
            selectbackground=BIOLUMINESCENT_MINT,
            selectforeground=ABYSS_NAVY,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 10),
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<Double-Button-1>", lambda e: self.copy_selected())

        scrollbar = tk.Scrollbar(
            list_body,
            orient=tk.VERTICAL,
            command=self.listbox.yview,
            bg=GLASS_PANEL,
            troughcolor=GLASS_PANEL,
            activebackground=BIOLUMINESCENT_MINT,
            relief=tk.FLAT,
            bd=0,
            width=8,
        )
        scrollbar.pack(side=tk.LEFT, fill=tk.Y, padx=(8, 0))
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Right panel: preview.
        right = tk.Frame(
            mid,
            width=300,
            bg=GLASS_PANEL,
            highlightthickness=1,
            highlightbackground=GLASS_BORDER,
        )
        right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(14, 0))
        right.pack_propagate(False)
        tk.Label(
            right,
            text="Preview",
            bg=GLASS_PANEL,
            fg=PURE_WHITE,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="nw", padx=16, pady=(14, 10))
        self.preview = tk.Text(
            right,
            wrap="word",
            state="disabled",
            bg=OCEANIC_NAVY,
            fg=PURE_WHITE,
            insertbackground=BIOLUMINESCENT_MINT,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 10),
            padx=14,
            pady=12,
        )
        self.preview.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))

        bottom = tk.Frame(self.root, bg=ABYSS_NAVY)
        bottom.pack(fill=tk.X, padx=24, pady=(0, 18))
        tk.Label(
            bottom,
            textvariable=self.status_var,
            bg=ABYSS_NAVY,
            fg=MUTED_TEXT,
            font=("Segoe UI", 9),
        ).pack(side=tk.LEFT)

        # Bind selection change
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.on_select())

        self.refresh_list()

    def make_button(self, parent, text, command, primary=False):
        background = PLASMA_GREEN if primary else GLASS_PANEL
        foreground = ABYSS_NAVY if primary else BIOLUMINESCENT_MINT
        hover_background = BIOLUMINESCENT_MINT if primary else OCEANIC_NAVY
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=background,
            fg=foreground,
            activebackground=hover_background,
            activeforeground=ABYSS_NAVY,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=PLASMA_GREEN if primary else GLASS_BORDER,
            highlightcolor=BIOLUMINESCENT_MINT,
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=8,
        )
        button.bind("<Enter>", lambda event: button.configure(bg=hover_background))
        button.bind("<Leave>", lambda event: button.configure(bg=background))
        return button

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
        self.count_label.configure(text=f"{len(self.filtered)} / {MAX_ITEMS}")
        # keep selection if possible
        self.on_select()

    def set_status(self, text):
        self.status_var.set(text)

def main():
    root = tb.Window(themename="superhero")
    app = ClipboardManager(root)
    root.resizable(True, True)
    root.mainloop()

if __name__ == "__main__":
    main()

