import sys
import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class AppWindow:
    """
    Depends on a cloud_handler that can do requests such as:
    listing buckets and files, uploading and downloading files.
    """


    class TextRedirector(object):
        # To display prints in the window
        def __init__(self, widget):
            self.widget = widget

        def write(self, s):
            self.widget.insert(tk.END, s)
            self.widget.see(tk.END)

        def flush(self):
            pass  # Needed for compatibility with stdout

    # STORAGE INDEPENDANT
    def __init__(self, cloud_handler):
        self.cloud_handler = cloud_handler
        self.root = tk.Tk()
        self.root.title("Client GUI")
        self.root.geometry("900x600")

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.upper_left = tk.Frame(self.root, bd=2, relief="groove")
        self.upper_left.place(x=0, y=0, width=450, height=300)

        self.bottom_left = tk.Frame(self.root, bd=2, relief="groove")
        self.bottom_left.grid(row=1, column=0, sticky="nsew")

        btn = tk.Button(self.bottom_left, text=f"Download", command=self.on_dl_button_click)
        btn.pack(fill="x", pady=5, padx=5)

        btn = tk.Button(self.bottom_left, text=f"Upload", command=self.on_ul_button_click)
        btn.pack(fill="x", pady=5, padx=5)

        btn = tk.Button(self.bottom_left, text=f"Create bucket", command=self.on_bucket_button_click)
        btn.pack(fill="x", pady=5, padx=5)

        btn = tk.Button(self.bottom_left, text=f"Connect to HSM", command=self.on_connect_hsm_button_click)
        btn.pack(fill="x", pady=5, padx=5)

        # Logs on the right
        log_frame = tk.Frame(self.root, bd=2, relief="sunken")
        log_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        log_text = ScrolledText(log_frame, wrap="word")
        log_text.pack(fill="both", expand=True)
        sys.stdout = self.TextRedirector(log_text)


        try:
            if not self.cloud_handler.connected:
                self.cloud_handler.connect_cloud()
        except Exception as e:
            print(e)
        else:
            # Upper left
            # Title

            self.tree = ttk.Treeview(self.upper_left)
            self.tree.heading("#0", text=self.cloud_handler.get_service_name())
            self.tree.pack(fill="both", expand=True)

            if self.cloud_handler.connected:
                self.refresh_tree()
            else:
                print("Connection failed")






    def on_dl_button_click(self):
        sel = self.tree.selection()
        if not sel:
            print("Nothing selected")
            return

        item_id = sel[0]

        # Check if this item has children
        children = self.tree.get_children(item_id)
        if children:
            print("This action only applies to a file.")
            return

        (container, filename) = self.tree.item(item_id, "values")

        if not filename:
            print("Invalid item")
            return

        path = filedialog.asksaveasfilename(
        initialfile=filename,     # defaults to the original name of the blob
        title="Save blob as..."
    )
        print("Downloading:", container, filename)
        try:
            self.cloud_handler.download(path, container, filename)
        except Exception as e:
            print("Download failed", e)



    def on_ul_button_click(self):
        sel = self.tree.selection()
        if not sel:
            print("No bucket selected.")
            return

        item_id = sel[0]

        # Retrieve metadata
        container, blob_name = self.tree.item(item_id, "values")

        if blob_name != "":    # blob_name empty = container
            print("Please select a container to upload into.")
            return

        path = filedialog.askopenfilename()
        if path:
            newblob_name = simpledialog.askstring(
                "Blob name",
                "Enter the name to store online (including folders if needed):"
            )
            if not newblob_name:
                return

            print("Uploading:", path, "to container:", container)
            try:
                self.cloud_handler.upload(path, container, newblob_name)
                self.refresh_tree()
            except Exception as e:
                print("Upload failed", e)


    def on_bucket_button_click(self):
        name = simpledialog.askstring(
                "Bucket name",
                "Enter the name of the bucket to create:"
            )
        if not name:
                return
        self.cloud_handler.create_container(name)
        self.refresh_tree()

    def on_connect_hsm_button_click(self):
        self.cloud_handler.connect_hsm()

    def refresh_tree(self):
    # Clear
        for item in self.tree.get_children():
            self.tree.delete(item)

        containers = self.cloud_handler.get_list_containers()
        for container in containers:
            container_name = container.name
            container_node = self.tree.insert("", "end", text = container_name, open=False, values=(container_name, ""))

            for file in self.cloud_handler.get_list_files(container_name):
                self.tree.insert(container_node, "end", text=file.name, values=(container_name, file.name))

    def run(self):
        self.root.mainloop()



