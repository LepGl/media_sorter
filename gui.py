import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import main
import config

class MediaSorterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Media Sorter")

        # Path selection
        self.folder_label = tk.Label(master, text="Unsorted Folder:")
        self.folder_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.folder_var = tk.StringVar(value=str(config.UNSORTED_FOLDER))
        self.folder_entry = tk.Entry(master, textvariable=self.folder_var, width=50)
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5)

        self.browse_button = tk.Button(master, text="Browse...", command=self.browse_folder)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Dry-run checkbox
        self.dry_run_var = tk.BooleanVar(value=config.DRY_RUN)
        self.dry_run_check = tk.Checkbutton(master, text="Dry Run (No changes made)", variable=self.dry_run_var)
        self.dry_run_check.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Buttons
        self.preview_button = tk.Button(master, text="Preview Sort", command=self.preview_sort)
        self.preview_button.grid(row=2, column=0, padx=5, pady=5)

        self.sort_button = tk.Button(master, text="Run Sort", command=self.run_sort)
        self.sort_button.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        self.undo_button = tk.Button(master, text="Undo Last Sort", command=self.run_undo)
        self.undo_button.grid(row=2, column=1, sticky="e", padx=5, pady=5)

        # Log output
        self.log_text = tk.Text(master, height=15, width=80)
        self.log_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        self.log("Ready.")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_var.set(folder_selected)

    def run_sort(self):
        folder = Path(self.folder_var.get())
        if not folder.exists():
            messagebox.showerror("Error", "Selected folder does not exist.")
            return
        config.UNSORTED_FOLDER = folder
        config.DRY_RUN = self.dry_run_var.get()
        self.log(f"[START SORT] Folder: {folder} | Dry-run: {config.DRY_RUN}")
        main.run_sort()
        self.log("[DONE] Sorting complete.")

    def run_undo(self):
        config.UNSORTED_FOLDER = Path(self.folder_var.get())
        config.DRY_RUN = self.dry_run_var.get()
        self.log(f"[UNDO] Undoing last sort in {config.UNSORTED_FOLDER}")
        main.undo_last_sort()
        self.log("[DONE] Undo complete.")

    def preview_sort(self):
        config.UNSORTED_FOLDER = Path(self.folder_var.get())
        config.DRY_RUN = self.dry_run_var.get()

        preview_items = main.generate_preview()

        preview_win = tk.Toplevel()
        preview_win.title("Sort Preview")
        preview_win.geometry("800x400")

        tree = ttk.Treeview(preview_win, columns=("original", "clean_name", "category", "source"), show="headings")
        tree.heading("original", text="Original Name")
        tree.heading("clean_name", text="Clean Name")
        tree.heading("category", text="Category")
        tree.heading("source", text="Source")
        tree.column("original", width=200)
        tree.column("clean_name", width=250)
        tree.column("category", width=100)
        tree.column("source", width=150)

        vsb = ttk.Scrollbar(preview_win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        for item in preview_items:
            tree.insert("", "end", values=(item["original"], item["clean_name"], item["category"], item["source"]))

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        preview_win.grid_columnconfigure(0, weight=1)
        preview_win.grid_rowconfigure(0, weight=1)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaSorterGUI(root)
    root.mainloop()
