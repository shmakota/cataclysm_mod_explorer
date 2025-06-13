import os
import json
import tkinter as tk
import re
from tkinter import filedialog, ttk

def scan_mod_directory(directory):
    mod_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                        if isinstance(content, dict):
                            content = [content]
                        elif not isinstance(content, list):
                            continue

                        for entry in content:
                            if not isinstance(entry, dict):
                                continue

                            if entry.get('type') == 'recipe':
                                result = entry.get('result', 'unknown')
                                category = entry.get('category', '')
                                subcategory = entry.get('subcategory', '')
                                description = category
                                if subcategory:
                                    description += f" > {subcategory}"

                                mod_data.append({
                                    'type': 'recipe',
                                    'id': result,
                                    'name': None,
                                    'name_plural': '',
                                    'description': description,
                                    'file': filepath,
                                    'full': entry
                                })
                            else:
                                 if 'id' in entry and 'description' in entry:
                                    name_field = entry.get('name', '')
                                    if isinstance(name_field, dict):
                                        name_str = name_field.get('str') or name_field.get('str_sp', '')
                                        name_plural = name_field.get('str_pl', '')
                                    else:
                                        name_str = name_field
                                        name_plural = ''

                                    # Remove color tags from name and name_plural
                                    name_str = re.sub(r'</?color[^>]*>', '', name_str)
                                    name_plural = re.sub(r'</?color[^>]*>', '', name_plural)

                                    mod_data.append({
                                        'type': entry.get('type', 'unknown'),
                                        'id': entry['id'],
                                        'name': name_str,
                                        'name_plural': name_plural,
                                        'description': entry['description'],
                                        'file': filepath,
                                        'full': entry
                                    })
                except Exception as e:
                    print(f"[!] Failed to read {filepath}: {e}")
    return mod_data

def get_mod_name(directory):
    modinfo_path = os.path.join(directory, "modinfo.json")
    if os.path.isfile(modinfo_path):
        try:
            with open(modinfo_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    name = data.get('name', None)
                elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                    name = data[0].get('name', None)
                else:
                    name = None
                if name:
                    import re
                    name = re.sub(r'</?color[^>]*>', '', name)
                    return name
        except Exception as e:
            print(f"[!] Failed to read modinfo.json: {e}")
    return None


class ModViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cataclysm Mod Explorer")
        self.geometry("1000x650")
        self.mod_data = []
        self.filtered_data = []
        self.sort_column = None
        self.sort_reverse = False
        self.create_widgets()
        self.columns = ('name', 'description', 'id', 'type')  # default new order
    
    def update_order_and_refresh(self):
        # Update the columns and refresh the tree and detail panel
        self.update_columns()
        self.populate_tree()
        self.detail_text.delete(1.0, tk.END)

    def update_columns(self):
        if self.use_new_order.get():
            self.columns = ('name', 'description', 'id', 'type')
        else:
            self.columns = ('type', 'id', 'name', 'description')

        self.tree.config(columns=self.columns)
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize(), command=lambda c=col: self.sort_by(c))
            self.tree.column(col, width=150 if col != 'description' else 400, anchor='w')
    
    def create_widgets(self):
        # Top control bar
        top_frame = tk.Frame(self)
        top_frame.pack(fill='x', padx=10, pady=10)

        tk.Button(top_frame, text="Browse Mod Folder", command=self.browse_folder).pack(side='left')
        self.path_label = tk.Label(top_frame, text="No folder selected", anchor='w')
        self.path_label.pack(side='left', padx=10)

        # Search bar
        search_frame = tk.Frame(self)
        search_frame.pack(fill='x', padx=10)

        tk.Label(search_frame, text="Search:").pack(side='left')
        self.search_field = tk.StringVar(value='All')
        search_options = ['All', 'Type', 'ID', 'Name', 'Description']
        search_dropdown = ttk.Combobox(search_frame, textvariable=self.search_field, values=search_options, state='readonly', width=12)
        search_dropdown.pack(side='left', padx=(5, 10))
        search_dropdown.bind("<<ComboboxSelected>>", self.update_filter)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_filter)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side='left', fill='x', expand=True)

        self.use_new_order = tk.BooleanVar(value=True)
        order_toggle = tk.Checkbutton(
            search_frame,
            text="Swap Columns",
            variable=self.use_new_order,
            command=self.update_order_and_refresh
        )
        order_toggle.pack(side='right', padx=(10, 0))

        self.count_label = tk.Label(search_frame, text="Entries: 0", anchor='e', fg='gray', font=('Arial', 10, 'italic'))
        self.count_label.pack(side='right', padx=(10, 0))

        # Paned window to split tree and text
        main_pane = tk.PanedWindow(self, orient=tk.VERTICAL)
        main_pane.pack(fill='both', expand=True, padx=10, pady=(5, 10))

        # Treeview (top)
        tree_frame = tk.Frame(main_pane)
        columns = ('name', 'description', 'id', 'type')

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')

        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        for col in columns:
            self.tree.heading(col, text=col.capitalize(), command=lambda c=col: self.sort_by(c))
            self.tree.column(col, width=150 if col != 'description' else 400, anchor='w')

        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        main_pane.add(tree_frame, stretch='always')

        # Detail view (bottom, resizable)
        self.detail_text = tk.Text(main_pane, wrap='word')
        main_pane.add(self.detail_text, height=150)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            mod_name = get_mod_name(folder)
            self.title("Cataclysm Mod Explorer: " + mod_name)
            display_text = folder
            self.path_label.config(text=display_text)
            self.mod_data = scan_mod_directory(folder)
            self.update_filter()

    def update_filter(self, *_):
        query = self.search_var.get().lower()
        field = self.search_field.get()

        def match(entry):
            if field == 'All':
                return (query in str(entry['id']).lower()
                        or query in str(entry.get('name', '')).lower()
                        or query in str(entry.get('description', '')).lower()
                        or query in str(entry.get('type', '')).lower())
            elif field == 'ID':
                return query in str(entry['id']).lower()
            elif field == 'Name':
                return query in str(entry.get('name', '')).lower()
            elif field == 'Description':
                return query in str(entry.get('description', '')).lower()
            elif field == 'Type':
                return query in str(entry.get('type', '')).lower()
            return False

        self.filtered_data = [e for e in self.mod_data if match(e)]
        self.populate_tree()
        self.count_label.config(text=f"Entries: {len(self.filtered_data)}")


    # some of this is definitely redundant, as it should never be null or None
    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        for idx, entry in enumerate(self.filtered_data):
            entry_id = entry['id'] if entry['id'] else 'null'
            name = entry.get('name')
            if not name:
                name = 'null'
            description = entry['description'] if entry['description'] else 'null'

            # Build the values list in the right order dynamically
            values = []
            for col in self.columns:
                if col == 'id':
                    values.append(entry_id)
                elif col == 'name':
                    values.append(name)
                elif col == 'description':
                    values.append(description[:100])
                elif col == 'type':
                    values.append(entry['type'])
                else:
                    values.append('null')

            self.tree.insert('', 'end', iid=idx, values=values)

    def sort_by(self, column):
        reverse = (self.sort_column == column and not self.sort_reverse)
        self.filtered_data.sort(key=lambda e: str(e.get(column, '')).lower(), reverse=reverse)
        self.sort_column = column
        self.sort_reverse = reverse
        self.populate_tree()

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            index = int(selected[0])
            entry = self.filtered_data[index]
            self.detail_text.delete(1.0, tk.END)
            if self.use_new_order.get():
                self.detail_text.insert(tk.END, f"Name: {entry.get('name', '')}\n")
                self.detail_text.insert(tk.END, f"Description:\n{entry.get('description', '')}\n\n")
                self.detail_text.insert(tk.END, f"ID: {entry['id']}\n")
                self.detail_text.insert(tk.END, f"Type: {entry['type']}\n\n")
            else:
                self.detail_text.insert(tk.END, f"Type: {entry['type']}\n")
                self.detail_text.insert(tk.END, f"ID: {entry['id']}\n")
                self.detail_text.insert(tk.END, f"Name: {entry.get('name', '')}\n")
                self.detail_text.insert(tk.END, f"Description:\n{entry.get('description', '')}\n\n")

            self.detail_text.insert(tk.END, f"File: {entry['file']}\n\n")
            self.detail_text.insert(tk.END, json.dumps(entry['full'], indent=2))

if __name__ == "__main__":
    app = ModViewerApp()
    app.mainloop()
