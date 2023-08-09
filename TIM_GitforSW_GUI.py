import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os, webbrowser, subprocess, shutil, stat

CONFIG_FILE = ".TIM_SW_GitHub_Tool_Config"
PATH = None
DEPTH = None
DEFAULT_DEPTH = "2"
GITHUB_URL = "https://github.com/tim-balloon/tim-mechanical_drawings"
GIT_REPO = GITHUB_URL.split("/")[-1]

def pull_click():
    cwd = os.getcwd()
    label.config(text="Pulling from GitHub...")
    if os.path.exists(os.path.join(PATH, GIT_REPO)):    
        os.chdir(os.path.join(PATH, GIT_REPO))
        subprocess.run(["git", "pull", f"--depth{DEPTH}"])
    else:
        os.chdir(PATH)
        subprocess.run(["git", "clone", f"--depth={DEPTH}", GITHUB_URL])
    os.chdir(cwd)
    label.config(text="Pulling from GitHub...Done!")

def push_click():
    cwd = os.getcwd()
    commit_message = "Update"
    def get_commit_message():
        global commit_message
        commit_message = entry1.get()
    label.config(text="Pushing to GitHub...")

    if os.path.exists(os.path.join(PATH, GIT_REPO)):
        os.chdir(os.path.join(PATH, GIT_REPO))
        subprocess.run(["git", "add", "."])
        
        input_window = tk.Toplevel(root)
        input_window.title("Commit Message")

        label1 = tk.Label(input_window, text="Commit Message:")
        entry1 = tk.Entry(input_window, width=60)
        entry1.insert(0, "Update")
        save_button = tk.Button(input_window, text="Commit", command=get_commit_message)
        exit_button = tk.Button(input_window, text="Push", command=input_window.destroy)
        entry1.bind("<Return>", lambda event: get_commit_message)

        label1.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry1.grid(row=0, column=1, padx=10, pady=5)
        save_button.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        exit_button.grid(row=1, column=1, padx=10, pady=5, sticky="e")

        subprocess.run(["git", "commit", "-m", commit_message])
        subprocess.run(["git", "push"])
    else:
        label.config(text="Please pull from GitHub first")
    os.chdir(cwd)
    label.config(text="Pushing to GitHub...Done!")
    

def refresh_click():
    def remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    
    cwd = os.getcwd()
    label.config(text="Refreshing...")
    if os.path.exists(os.path.join(PATH, GIT_REPO)):
        os.chdir(os.path.join(PATH))
        shutil.rmtree(GIT_REPO, onerror=remove_readonly)
        subprocess.run(["git", "clone", f"--depth={DEPTH}", GITHUB_URL])
    else:
        label.config(text="Please pull from GitHub first")
    os.chdir(cwd)
    label.config(text="Refreshing...Done!")

def restore_click():
    cwd = os.getcwd()
    label.config(text="Restoring...")
    if os.path.exists(os.path.join(PATH, GIT_REPO)):
        os.chdir(os.path.join(PATH, GIT_REPO))
        subprocess.run(["git", "restore", "."])
    else:
        label.config(text="Please pull from GitHub first")
    os.chdir(cwd)
    label.config(text="Restoring...Done!")

def exit_click():
    root.quit()

def save_values(entry1, entry2):
    label.config(text="Settings saved")
    with open(CONFIG_FILE, "w") as f:
        f.write(entry1.get() + "\n")
        f.write(entry2.get() + "\n")

def current_values():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]

def settings_click():
    def browse_file():
        selected_file = filedialog.askdirectory()
        entry1.delete(0, tk.END)  # Clear existing text
        entry1.insert(0, selected_file)
    input_window = tk.Toplevel(root)
    input_window.title("Settings")

    label1 = tk.Label(input_window, text="Path:")
    label2 = tk.Label(input_window, text="Depth:")

    entry1 = tk.Entry(input_window, width=50)
    entry2 = tk.Entry(input_window, width=10)
    button_browse = tk.Button(input_window, text="Browse", command=browse_file)

    values = current_values()
    if values:
        entry1.insert(0, values[0])
        entry2.insert(0, values[1])
    else:
        entry2.insert(0, DEFAULT_DEPTH)

    save_button = tk.Button(input_window, text="Save", command=lambda: \
                            save_values(entry1, entry2))
    exit_button = tk.Button(input_window, text="Exit", command=input_window.destroy)
    entry1.bind("<Return>", lambda event: save_values(entry1, entry2)) 
    entry2.bind("<Return>", lambda event: save_values(entry1, entry2))

    label1.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    label2.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry1.grid(row=0, column=1, padx=10, pady=5)
    entry2.grid(row=1, column=1, padx=10, pady=5)
    button_browse.grid(row=0, column=2, padx=10, pady=5)

    save_button.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    exit_button.grid(row=2, column=1, padx=10, pady=5, sticky="e")

def open_mailto_link(event):
    root.clipboard_clear()
    root.clipboard_append("shubh@sas.upenn.edu")
    root.update()
    root.after(100, lambda: root.event_generate('<<Paste>>'))
    webbrowser.open("mailto:shubh@sas.upenn.edu")

# Create the main window
root = tk.Tk()
root.title("TIM SolidWorks GitHub Tool")
root.geometry("450x300")  # Set the initial window size

# Create style for buttons
style = ttk.Style()
style.configure("TButton", padding=10, font=("Helvetica", 12))
style.configure("Red.TButton", padding=10, font=("Helvetica", 12, "italic"), \
                background="red")

# Create buttons
pull_button = ttk.Button(root, text="Pull", command=pull_click)
push_button = ttk.Button(root, text="Push", command=push_click)
restore_button = ttk.Button(root, text="Restore", command=restore_click, style="Red.TButton")
refresh_button = ttk.Button(root, text="Refresh", command=refresh_click, style="Red.TButton")
exit_button = ttk.Button(root, text="Exit", command=exit_click)
settings_button = ttk.Button(root, text="Settings", command=settings_click)

# Create a label to display messages
label = tk.Label(root, text="Welcome!", font=("Helvetica", 10))
email = tk.Label(root, text="Contact Shubh (shubh@sas.upenn.edu) for help or comments", \
                 font=("Helvetica", 10, "underline italic"), fg="blue", cursor="hand2")
email.bind("<Button-1>", open_mailto_link)

# Arrange widgets using the grid layout manager
label.grid(row=0, column=0, columnspan=7, padx=20, pady=20)
pull_button.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="ew")
push_button.grid(row=1, column=4, padx=10, pady=10, columnspan=4, sticky="ew")
refresh_button.grid(row=2, column=0, padx=10, pady=10, columnspan=3, sticky="ew")
restore_button.grid(row=2, column=4, padx=10, pady=10, columnspan=4, sticky="ew")
settings_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2, sticky="w")
exit_button.grid(row=3, column=5, padx=10, pady=10, columnspan=2, sticky="e")
email.grid(row=4, column=0, columnspan=7, padx=10, pady=10)

[root.rowconfigure(ind, weight=1) for ind in range(5)]
[root.columnconfigure(ind, weight=1) for ind in range(7)]

def check_config_file_existence():
    global DEPTH, PATH
    buttons = [pull_button, push_button, refresh_button, restore_button]
    if os.path.exists(CONFIG_FILE):
        for button in buttons:
            button.config(state="enabled")
        PATH, DEPTH = current_values()
    else:
        for button in buttons:
            button.config(state="disabled")
        label.config(text="Please set PATH using Settings first")

    if PATH:
        if not os.path.exists(PATH):
            label.config(text="Given PATH does not exist. Please set PATH using Settings first")
            for button in buttons:
                button.config(state="disabled")
    if DEPTH:
        if not DEPTH.isnumeric() or int(DEPTH) < 0:
            label.config(text="Given DEPTH is invalid. Please set DEPTH using Settings first")
            for button in buttons:
                button.config(state="disabled")
            
    
    root.after(1000, check_config_file_existence)

check_config_file_existence()

# Start the Tkinter event loop
root.mainloop()
