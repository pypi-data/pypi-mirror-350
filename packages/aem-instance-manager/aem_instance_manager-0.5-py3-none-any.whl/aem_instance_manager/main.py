import tkinter as tk
from tkinter import ttk
import pandas as pd
import subprocess
import os
import socket
import time
import sys
import re

class ProjectManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AEM Instance Manager")

        # Variables
        self.projects = pd.DataFrame(columns=["Project Name", "Author Port", "Publish Port", "Folder Path", "Status"])
        self.current_project_name = tk.StringVar(value="")
        self.current_author_port = tk.StringVar(value="")
        self.current_publish_port = tk.StringVar(value="")
        self.current_folder_path = tk.StringVar(value="")
        self.current_status = "Stopped"  # Default status
        self.selected_project = tk.StringVar(value="")
        
        # Left side: Input fields
        self.input_frame = ttk.Frame(root)
        self.input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.project_name_label = ttk.Label(self.input_frame, text="Project Name:")
        self.project_name_entry = ttk.Entry(self.input_frame, textvariable=self.current_project_name, validate="key", validatecommand=(root.register(self.validate_project_name), '%P'), width=10)
        self.author_port_label = ttk.Label(self.input_frame, text="Author Port:")
        self.author_port_entry = ttk.Entry(self.input_frame, textvariable=self.current_author_port,validate="key", validatecommand=(root.register(self.validate_author_port), '%P'), width=10)
        self.publish_port_label = ttk.Label(self.input_frame, text="Publish Port:")
        self.publish_port_entry = ttk.Entry(self.input_frame, textvariable=self.current_publish_port,validate="key", validatecommand=(root.register(self.validate_publish_port), '%P'), width=10)
        self.folder_path_label = ttk.Label(self.input_frame, text="Folder Path:")
        self.folder_path_entry = ttk.Entry(self.input_frame, textvariable=self.current_folder_path, width=10)
        self.save_button = ttk.Button(self.input_frame, text="Save", command=self.save_project, width=6)
        self.exit_button = ttk.Button(self.input_frame, text="Exit", command=root.destroy, width=6)
        self.project_display_error = tk.Text(self.input_frame, height=3.5, width=10, state=tk.DISABLED, bg="black", fg="#00FF00")

        # Right side: Project controls
        self.project_controls_frame = ttk.Frame(root, borderwidth=0.5, relief="solid")
        self.project_controls_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        self.project_dropdown_label = ttk.Label(self.project_controls_frame, text="Select Project:")
        self.project_dropdown = ttk.Combobox(self.project_controls_frame, values=[], textvariable=self.selected_project, state="readonly")

        # self.extra_args_label = ttk.Label(self.project_controls_frame, text="Extra Args:")
        # self.extra_args_entry = ttk.Entry(self.project_controls_frame, width=20)

        # Debug Mode Checkbox
        self.debug_mode = tk.BooleanVar(value=False)
        self.debug_checkbox = ttk.Checkbutton(self.project_controls_frame, text="Debug Mode", variable=self.debug_mode)
        self.debug_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Open Project Folder Button
        self.open_folder_button = ttk.Button(self.project_controls_frame, text="Open Project Folder", command=self.open_project_folder)
        self.open_folder_button.grid(row=1, column=1, padx=10, pady=1, sticky="w")


        self.start_button = ttk.Button(self.project_controls_frame, text="Start", command=self.start_project)
        self.stop_button = ttk.Button(self.project_controls_frame, text="Stop", command=self.stop_project)
        self.remove_button = ttk.Button(self.project_controls_frame, text="Remove", command=self.remove_project)
        # self.project_display_label = ttk.Label(self.project_controls_frame, text="Project Details:")
        self.project_display_text = tk.Text(self.project_controls_frame, height=12, width=30, state=tk.DISABLED)
        

        # Grid layout
        self.project_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.project_name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.author_port_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.author_port_entry.grid(row=1, column=1, padx=10, pady=5)
        self.publish_port_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.publish_port_entry.grid(row=2, column=1, padx=10, pady=5)
        self.folder_path_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.folder_path_entry.grid(row=3, column=1, padx=10, pady=5)
        self.save_button.grid(row=5, column=0, pady=10)
        self.exit_button.grid(row=5, column=1, pady=10)
        self.project_display_error.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="nsew") 

        self.project_dropdown_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.project_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # self.extra_args_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        # self.extra_args_entry.grid(row=1, column=1, padx=10, pady=5)

        self.start_button.grid(row=2, column=0, padx=10, pady=1, sticky="w")
        self.stop_button.grid(row=2, column=1, padx=10, pady=1,sticky="w")
        self.remove_button.grid(row=2, column=1, padx=10, pady=1,sticky="e")
        # self.project_display_label.grid(row=2, column=0, columnspan=2, pady=5)
        self.project_display_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Configure grid weights for resizing
        for i in range(6):
            root.grid_rowconfigure(i, weight=1)

        for i in range(2):
            root.grid_columnconfigure(i, weight=1)

        # Load projects
        self.load_projects()

        # Binding event for dropdown selection
        self.project_dropdown.bind("<<ComboboxSelected>>", self.display_project_details)

        # Footer Label
        self.footer_label = ttk.Label(root, text="Created by Mayur Satav                   www.mayursatav.in                   Version v0.4", anchor="center", font=("Helvetica", 9), foreground="gray")
        self.footer_label.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
    
    def display_messages(self, message):
        self.project_display_error.config(state=tk.NORMAL)
        self.project_display_error.delete("1.0", tk.END)
        self.project_display_error.insert(tk.END, f"{message}\n")
        self.project_display_error.config(state=tk.DISABLED)

    def open_project_folder(self):
        selected_project_name = self.selected_project.get()
        if selected_project_name:
            project_index = self.projects.index[self.projects["Project Name"] == selected_project_name][0]
            folder_path = self.projects.at[project_index, "Folder Path"]

            # Open the folder using the default file explorer
            try:
                if os.name == 'nt':  # For Windows
                    os.startfile(folder_path)
                elif os.name == 'posix':  # For MacOS and Linux
                    subprocess.run(["open", folder_path] if sys.platform == "darwin" else ["xdg-open", folder_path])
                else:
                    self.display_messages(f"Unsupported OS for opening folder: {os.name}")
            except Exception as e:
                self.display_messages(f"Error opening folder: {str(e)}")

    def validate_project_name(self, new_value):
        return len(new_value) <= 10

    def validate_author_port(self, new_value):
        return len(new_value) <= 5 and (new_value.isdigit() or not new_value)

    def validate_publish_port(self, new_value):
        return len(new_value) <= 5 and (new_value.isdigit() or not new_value)
    
    def remove_project(self):
        selected_project_name = self.selected_project.get()
        if selected_project_name:
            # Remove the selected project entry
            self.projects = self.projects[self.projects["Project Name"] != selected_project_name]
            self.projects.to_csv("projects.csv", index=False)
            self.load_projects()
            # Clear the input fields after removing the project
            self.clear_input_fields()

    def remove_project(self):
        selected_project_name = self.selected_project.get()
        if selected_project_name:
            # Remove the selected project entry
            self.projects = self.projects[self.projects["Project Name"] != selected_project_name]
            self.projects.to_csv("projects.csv", index=False)
            self.load_projects()
            # Clear the input fields after removing the project
            self.clear_input_fields()
        
        # Display the project start/stop message in the message display text box
        message = f"Project {selected_project_name} Removed. \n"
        self.display_messages(message)
    
    def clear_input_fields(self):
        self.current_project_name.set("")
        self.current_author_port.set("")
        self.current_publish_port.set("")
        self.current_folder_path.set("")

    def save_project(self):
        project_name = self.current_project_name.get()
        author_port = self.current_author_port.get()
        publish_port = self.current_publish_port.get()
        folder_path = self.current_folder_path.get()

        if not re.search(r"/$", folder_path):
            folder_path += "/"

        print(folder_path)
        
        if project_name and author_port:
            new_project = pd.DataFrame({
                "Project Name": [project_name],
                "Author Port": [author_port],
                "Publish Port": [publish_port],
                "Folder Path": [folder_path],
                "Status": [self.current_status]
            })
            self.projects = pd.concat([self.projects, new_project], ignore_index=True)
            self.projects.to_csv("projects.csv", index=False)
            self.load_projects()
            self.current_project_name.set("")
            self.current_author_port.set("")
            self.current_publish_port.set("")
            self.current_folder_path.set("")
        
        # Display the project start/stop message in the message display text box
        message = f"Project {project_name} Added!!!. \n"
        self.display_messages(message)

    def load_projects(self):
        try:
            self.projects = pd.read_csv("projects.csv")
            project_names = self.projects["Project Name"].tolist()
            self.project_dropdown["values"] = project_names
            if not self.projects.empty:
                self.selected_project.set(project_names[0])
                self.display_project_details()
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # If the file is not found or empty, create an empty DataFrame
            self.projects = pd.DataFrame(columns=["Project Name", "Author Port", "Publish Port","Status", "Folder Path"])

    def start_project(self):
        selected_project_name = self.selected_project.get()

        if selected_project_name:
            project_index = self.projects.index[self.projects["Project Name"] == selected_project_name][0]
            author_port = self.projects.at[project_index, "Author Port"]
            publish_port = self.projects.at[project_index, "Publish Port"]
            folder_path = self.projects.at[project_index, "Folder Path"]

            authorPath = os.path.join(folder_path, "author")
            publishPath = os.path.join(folder_path, "publish")
            authorJar = self.print_jar_files_in_folder(authorPath)
            publishJar = self.print_jar_files_in_folder(publishPath)
            print(authorJar)
            print(publishJar)

            # Check if the author and publish ports are already in use
            if self.is_port_in_use(author_port) or self.is_port_in_use(publish_port):
                self.display_messages(f"another project already using both {author_port} and {publish_port} ports")
            else:
                if self.debug_mode.get():  # If Debug Mode is checked
                    # Debug mode command
                    author_command = f"cd {authorPath} ; java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 -jar {authorJar} -p {author_port}"
                    publish_command = f"cd {publishPath} ; java -jar {publishJar} -p {publish_port}"
                else:
                    # Regular command
                    author_command = f"cd {authorPath} ; java -jar {authorJar} -p {author_port}"
                    publish_command = f"cd {publishPath} ; java -jar {publishJar} -p {publish_port}"

                print(author_command)
                print(publish_command)

                # Run the command in the background
                self.run_command_in_background(author_command)
                self.run_command_in_background(publish_command)
                time.sleep(5)
                self.update_project_status("Running")

    def stop_project(self):
        selected_project_name = self.selected_project.get()

        if selected_project_name:
            project_index = self.projects.index[self.projects["Project Name"] == selected_project_name][0]
            author_port = self.projects.at[project_index, "Author Port"]
            publish_port = self.projects.at[project_index, "Publish Port"]
            folder_path = self.projects.at[project_index, "Folder Path"]

            command_to_run = f"lsof -t -i tcp:{author_port} | xargs kill -9;lsof -t -i tcp:{publish_port} | xargs kill -9;"
            # Run the command in the background
            self.run_command_in_background(command_to_run)
            self.update_project_status("Stopped")
    
    def print_jar_files_in_folder(self, folder_path):
        try:
            # List all files in the specified folder
            files = os.listdir(folder_path)

            # Return only the JAR files in the list
            jar_files = [file for file in files if file.endswith('.jar')]
            
            if jar_files:
                print(f"JAR Files in {folder_path}: {', '.join(jar_files)}")
                return ', '.join(jar_files)
            else:
                self.display_messages(f"No JAR files found in {folder_path}")
                return ''

        except FileNotFoundError:
            self.display_messages(f"The specified folder '{folder_path}' does not exist.")
            return ''

    
    def is_port_in_use(self, port):
        # Check if the specified port is in use
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    def run_command_in_background(self, command):
        print("command running")
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    def close_terminal_windows(self, path):
        # Create an AppleScript to close Terminal windows for the specified path
        script_content = f'tell application "Terminal"\n' \
                 f'  close (every window whose tab 1 \'s custom title contains "{path}")\n' \
                 f'end tell\n'


        script_path = os.path.join(os.path.expanduser("~"), "close_terminal_script.scpt")
        with open(script_path, "w") as script:
            script.write(script_content)

        # Execute the AppleScript to close Terminal windows
        subprocess.run(["osascript", script_path])

    def update_project_status(self, new_status):
        selected_project_name = self.selected_project.get()
        if selected_project_name:
            project_index = self.projects.index[self.projects["Project Name"] == selected_project_name][0]
            self.projects.at[project_index, "Status"] = new_status
            self.projects.to_csv("projects.csv", index=False)
            self.load_projects()
        
        # Display the project start/stop message in the message display text box
        message = f"Project {selected_project_name} is {new_status.lower()}.\n"
        self.display_messages(message)

    def display_project_details(self, event=None):
        self.project_display_text.config(state=tk.NORMAL)
        self.project_display_text.delete("1.0", tk.END)

        # Configure tags for text colors
        self.project_display_text.tag_configure("red", foreground="red")
        self.project_display_text.tag_configure("green", foreground="green")
        self.project_display_text.tag_configure("heading", font=("Helvetica", 12, "bold"))

        # Insert heading
        all_project_details = "-" * 44 + "\n"
        all_project_details += "# | Project    | Author | Publish | Status  \n"
        all_project_details += "-" * 44 + "\n"

        self.project_display_text.insert(tk.END, all_project_details)

        # Counter variable
        serial_number = 1

        for _, project in self.projects.iterrows():
            project_name = project['Project Name']
            author_port = project['Author Port']
            publish_port = project['Publish Port']
            status = project['Status']

            # Determine the tag based on status for color
            status_tag = "red" if status == "Stopped" else "green"

            details = f"{serial_number: <2}| {project_name: <10} | {author_port: <6} | {publish_port: <7} | "
            self.project_display_text.insert(tk.END, details)

            # Insert status separately with the appropriate color tag
            if status == "Stopped":
                self.project_display_text.insert(tk.END, f"{status}  ", status_tag)
            else:
                self.project_display_text.insert(tk.END, f"{status} ", status_tag)

            self.project_display_text.insert(tk.END, " \n")
            # Increment the serial number
            serial_number += 1

        self.project_display_text.config(state=tk.DISABLED)
        self.display_messages("Project details displayed.")

def main():
    """Entry point for running the GUI application."""
    root = tk.Tk()
    app = ProjectManagerApp(root)
    root.resizable(width=False, height=False)
    root.mainloop()

if __name__ == "__main__":
    main()
