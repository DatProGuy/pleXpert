import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import re

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Function to parse season posters
def process_season_poster(filename, image_folder, rename_data):
    season_match = re.search(r'season\s*(\d{1,2})', filename.lower())
    if season_match:
        season = season_match.group(1).zfill(2)
        ext = os.path.splitext(filename)[1]
        new_name = f"Season{season}{ext}"
        season_folder = f"Season {season}"
        rename_data[filename] = (new_name, season_folder)

# Function to parse episode title cards
def process_episode_card(filename, image_folder, destination_folder, rename_data):
    season, episode = None, None
    match = re.search(r's(\d{1,2})[^\d]?e(\d{1,3})', filename.lower())
    if match:
        season = match.group(1).zfill(2)
        episode = match.group(2).zfill(2)
        ext = os.path.splitext(filename)[1]

        for root, dirs, files in os.walk(destination_folder):
            for file in files:
                if f"s{season}e{episode}" in file.lower():
                    base_name = os.path.splitext(file)[0]
                    new_name = f"{base_name}{ext}"
                    season_folder = f"Season {season}"
                    rename_data[filename] = (new_name, season_folder)
                    return  # Stop further processing once a match is found

# Function to handle specials
def process_specials(filename, image_folder, rename_data):
    if "specials" in filename.lower():
        ext = os.path.splitext(filename)[1]
        new_name = f"season-specials-poster{ext}"
        season_folder = "Specials"
        rename_data[filename] = (new_name, season_folder)

# Function to rename and organize files
def rename_files(image_folder, output_folder, rename_data):
    for original, (new_name, season_folder) in rename_data.items():
        season_output_folder = os.path.join(output_folder, season_folder)
        os.makedirs(season_output_folder, exist_ok=True)
        shutil.copyfile(os.path.join(image_folder, original), os.path.join(season_output_folder, new_name))

# Function to populate the listbox with initial files
def populate_initial_files(*args):
    image_folder = image_folder_var.get()
    if os.path.isdir(image_folder):
        preview_textbox.config(state=tk.NORMAL)
        preview_textbox.delete(1.0, tk.END)  # Clear the textbox first
        for filename in os.listdir(image_folder):
            preview_textbox.insert(tk.END, filename + '\n')
        preview_textbox.config(state=tk.DISABLED)
        destination_button.config(state=tk.NORMAL)  # Enable destination folder button

# Function to generate preview of file renames
def generate_preview(*args):
    image_folder = image_folder_var.get()
    destination_folder = destination_folder_var.get()

    if os.path.isdir(image_folder) and os.path.isdir(destination_folder):
        rename_data = {}
        ignored_files = []

        for filename in os.listdir(image_folder):
            if "specials" in filename.lower():
                process_specials(filename, image_folder, rename_data)
            elif "season" in filename.lower():
                process_season_poster(filename, image_folder, rename_data)
            elif re.search(r's(\d{1,2})[^\d]?e(\d{1,3})', filename.lower()):
                process_episode_card(filename, image_folder, destination_folder, rename_data)
            else:
                ignored_files.append(filename)

        # Sort the remapped files by season folder
        sorted_rename_data = sorted(rename_data.items(), key=lambda x: x[1][1])

        # Show a preview in the Text widget with output folder information
        preview_textbox.config(state=tk.NORMAL)
        preview_textbox.delete(1.0, tk.END)
        for original, (new_name, season_folder) in sorted_rename_data:
            preview_textbox.insert(tk.END, f"{original} -> {os.path.join(season_folder, new_name)}\n")

        # Mark ignored files with red color
        if ignored_files:
            preview_textbox.insert(tk.END, "---------------Ignored Files After This Line--------------------\n", "red")
            for file in ignored_files:
                preview_textbox.insert(tk.END, f"Ignored: {file}\n", "red")
        
        preview_textbox.config(state=tk.DISABLED)

# Main processing function
def process_renaming():
    image_folder = image_folder_var.get()
    destination_folder = destination_folder_var.get()

    if not image_folder or not destination_folder:
        messagebox.showerror("Error", "Please select both image and destination folders.")
        return

    rename_data = {}
    ignored_files = []

    for filename in os.listdir(image_folder):
        if "specials" in filename.lower():
            process_specials(filename, image_folder, rename_data)
        elif "season" in filename.lower():
            process_season_poster(filename, image_folder, rename_data)
        elif re.search(r's(\d{1,2})[^\d]?e(\d{1,3})', filename.lower()):
            process_episode_card(filename, image_folder, destination_folder, rename_data)
        else:
            ignored_files.append(filename)

    def finalize():
        output_folder = os.path.join(image_folder, "Output")
        os.makedirs(output_folder, exist_ok=True)
        rename_files(image_folder, output_folder, rename_data)
        messagebox.showinfo("Success", "Files have been renamed and copied to the Output folder.")
        # Correct the command to open the correct output folder in file explorer
        subprocess.Popen(f'explorer /select,"{os.path.abspath(output_folder)}"')

    # Confirm action
    if messagebox.askyesno("Proceed", "Do you want to proceed with renaming?"):
        finalize()

# Function to browse for a folder
def browse_folder(var):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        var.set(folder_selected)

# Initialize the main application window
root = tk.Tk()
root.title("PLEX Image Renamer")
root.geometry("1000x750")  # Set a reasonable default window size

# Load and use the logo image using PhotoImage
logo_path = resource_path("pleXpertLogo.png")
logo_image = tk.PhotoImage(file=logo_path)

logo_label = tk.Label(root, image=logo_image, bg='#2e2e2e')
logo_label.pack(pady=10)

# Initialize the StringVars for the folder paths
image_folder_var = tk.StringVar()
destination_folder_var = tk.StringVar()

# Bind the image folder variable to auto-update the file list
image_folder_var.trace_add("write", populate_initial_files)
destination_folder_var.trace_add("write", generate_preview)

# Apply dark mode theme
root.configure(bg='#2e2e2e')

# User inputs and checkboxes
tv_posters_var = tk.BooleanVar()
episode_cards_var = tk.BooleanVar()

frame = tk.Frame(root, bg='#2e2e2e')
frame.pack(padx=10, pady=10, fill="both", expand=True)

checkbox_frame = tk.Frame(frame, bg='#2e2e2e')
checkbox_frame.pack(anchor="w")

tv_check = tk.Checkbutton(checkbox_frame, text="TV Season Posters", variable=tv_posters_var, bg='#2e2e2e', fg='white', selectcolor='#454545', activebackground='#454545')
tv_check.grid(row=0, column=0, sticky="w")

season_label = tk.Label(checkbox_frame, text="(Ensure all Season Posters have 'Season' or 'Specials' in the file name.)", fg="#9E9E9E", bg='#2e2e2e')
season_label.grid(row=0, column=1, sticky="w", padx=10)

episode_check = tk.Checkbutton(checkbox_frame, text="Episode Title Cards", variable=episode_cards_var, bg='#2e2e2e', fg='white', selectcolor='#454545', activebackground='#454545')
episode_check.grid(row=1, column=0, sticky="w")

episode_label = tk.Label(checkbox_frame, text="(Ensure Episode Title Cards contain Season and Episode Number)", fg="#9E9E9E", bg='#2e2e2e')
episode_label.grid(row=1, column=1, sticky="w", padx=10)

folder_frame = tk.Frame(frame, bg='#2e2e2e')
folder_frame.pack(pady=10, anchor="w", fill="x")

tk.Label(folder_frame, text="Image Folder:", bg='#2e2e2e', fg='white').pack(anchor="w")
tk.Entry(folder_frame, textvariable=image_folder_var, width=60, bg='#454545', fg='white').pack(anchor="w")
tk.Button(folder_frame, text="Browse", command=lambda: browse_folder(image_folder_var), bg='#3a3a3a', fg='white', activebackground='#454545').pack(anchor="w")

tk.Label(folder_frame, text="Destination Folder:", bg='#2e2e2e', fg='white').pack(anchor="w", pady=(10, 0))
destination_entry = tk.Entry(folder_frame, textvariable=destination_folder_var, width=60, bg='#454545', fg='white')
destination_entry.pack(anchor="w")
destination_button = tk.Button(folder_frame, text="Browse", command=lambda: browse_folder(destination_folder_var), bg='#3a3a3a', fg='white', activebackground='#454545')
destination_button.pack(anchor="w")
destination_button.config(state=tk.DISABLED)  # Disable until image folder is set

# Action buttons - Place this frame before the preview text box
button_frame = tk.Frame(frame, bg='#2e2e2e')
button_frame.pack(fill="x", pady=0)

# Proceed button
proceed_button = tk.Button(button_frame, text="Proceed", command=process_renaming, bg='#3a3a3a', fg='white', activebackground='#454545')
proceed_button.pack(side="right", padx=10, pady=0)

# Cancel button
cancel_button = tk.Button(button_frame, text="Cancel", command=root.quit, bg='#3a3a3a', fg='white', activebackground='#454545')
cancel_button.pack(side="right", padx=10, pady=0)

# Preview Text widget that scales with the window but leaves space for buttons
preview_frame = tk.Frame(frame, bg='#2e2e2e')
preview_frame.pack(pady=10, fill="both", expand=True)

preview_textbox = tk.Text(preview_frame, width=100, bg='#454545', fg='white', wrap='none')
preview_textbox.pack(side="left", fill="both", expand=True)

preview_scrollbar = tk.Scrollbar(preview_frame, bg='#2e2e2e')
preview_scrollbar.pack(side="right", fill="y")

preview_textbox.config(yscrollcommand=preview_scrollbar.set)
preview_scrollbar.config(command=preview_textbox.yview)


# Show/hide labels based on checkbox selection
def update_labels():
    season_label.grid() if tv_posters_var.get() else season_label.grid_remove()
    episode_label.grid() if episode_cards_var.get() else episode_label.grid_remove()

tv_posters_var.trace_add("write", lambda *args: update_labels())
episode_cards_var.trace_add("write", lambda *args: update_labels())

season_label.grid_remove()
episode_label.grid_remove()

# Start the main loop
root.mainloop()
