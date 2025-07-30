import os
import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD


#The below class creates a window for dragging and dropping or browsing and selecting files
#And each time one or more file is added, the full file list and most recently added files will be passed to
#The function supplied by the user (function_for_after_file_addition)
#with the two variables passed being all_selected_file_paths, newly_added_file_paths
#This class **cannot** be initiated directly, it should initiated using the
#companion function create_and_launch
class DragDropApp:
    def __init__(self, root, app_name = '', function_for_after_file_addition = None):
        self.root = root
        self.root.title(app_name)
        self.function_for_after_file_addition = function_for_after_file_addition

        # Enable native drag-and-drop capability
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.drop_files)

        # Create a drop zone
        self.drop_frame = tk.Label(root, text="Drag and drop files here \n\n Click End When Finished", bg="lightgray", width=50, height=10)
        self.drop_frame.pack(pady=10)

        # Create a listbox to display selected files
        self.file_listbox = tk.Listbox(root, width=60, height=10)
        self.file_listbox.pack(pady=10)

        # Buttons for manual selection and finalizing selection
        self.select_button = tk.Button(root, text="Select Files By Browsing", command=self.open_file_dialog)
        self.select_button.pack(pady=5)

        # Create a frame for the middle buttons
        button_frame_middle = tk.Frame(root)
        button_frame_middle.pack(pady=5)

        self.clear_button = tk.Button(button_frame_middle, text="Clear Files List", command=self.clear_file_list)  # New "Clear" button
        self.clear_button.pack(side = tk.LEFT, pady=5)

        # "Download Output" button
        self.download_button = tk.Button(button_frame_middle, text="Download Output", command=self.download_output)
        self.download_button.pack(side = tk.RIGHT, pady=5)

        self.done_button = tk.Button(root, text="End", command=self.finish_selection)
        self.done_button.pack(pady=5)

        # Store selected file paths
        self.all_selected_file_paths = []

    def clear_file_list(self):
        """Clears the listbox and resets selected files."""
        self.file_listbox.delete(0, tk.END)  # Clear listbox
        self.all_selected_file_paths = []  # Reset file list
        self.function_for_after_file_addition(all_selected_file_paths=[], newly_added_file_paths=[])
        print("File list cleared!")  # Optional debug message

    def open_file_dialog(self):
        """Opens a file dialog to manually select files."""
        newly_added_file_paths = self.root.tk.splitlist(tk.filedialog.askopenfilenames(title="Select files"))
        if newly_added_file_paths:
            self.all_selected_file_paths.extend(newly_added_file_paths)
            self.update_file_list(newly_added_file_paths)

    def drop_files(self, event):
        """Handles dropped files into the window."""
        newly_added_file_paths = self.root.tk.splitlist(event.data)
        if newly_added_file_paths:
            self.all_selected_file_paths.extend(newly_added_file_paths)
            self.update_file_list(newly_added_file_paths)

    def update_file_list(self, newly_added_file_paths):
        """Updates the listbox with selected filenames."""
        self.file_listbox.delete(0, tk.END)  # Clear listbox
        for filename_and_path in self.all_selected_file_paths:
            self.file_listbox.insert(tk.END, os.path.basename(filename_and_path))  # Show filenames only
        # If there is a function_for_after_file_addition, pass full list and newly added files into function_for_after_file_addition
        if self.function_for_after_file_addition is not None:
            output = self.function_for_after_file_addition(self.all_selected_file_paths, newly_added_file_paths)
            self.output_for_download = output[0] #store the first part of the output for download.

    def download_output(self):
        """Allows user to choose where to save the output."""
        if hasattr(self, "output_for_download"):
            file_path = filedialog.asksaveasfilename(filetypes=[("*.*", "*.txt")], title="Save Output As")
            if file_path:  # If a valid path is chosen
                with open(file_path, "w") as file:
                    file.write(str(self.output_for_download))
                print(f"Output saved as '{file_path}'!")
            else:
                print("File save operation canceled.")
        else:
            print("No output available to download.")


    def finish_selection(self):
        """Closes the window and returns selected files."""
        self.root.quit() # Close the window

# This function is a companion function to
# The class DragDropApp for creating a file selection and function call app
# The function_for_after_file_addition should return a list where the first item is something that can be downloaded.
def create_and_launch(app_name = '', function_for_after_file_addition=None):
    """Starts the GUI and returns selected files."""
    root = TkinterDnD.Tk()
    app = DragDropApp(root, app_name=app_name, function_for_after_file_addition=function_for_after_file_addition)
    root.mainloop() # Runs the Tkinter event loop
    return app.all_selected_file_paths # Returns selected files after the window closes
