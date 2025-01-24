import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread

def download_projects(start, end, output_dir):
    """Download Scratch projects within the specified range."""
    base_url = "https://scratch.mit.edu/classes/{}/studios/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    for class_id in range(start, end + 1):
        url = base_url.format(class_id)
        print(f"Searching: {url}")
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find all project links
            project_links = soup.find_all("a", href=True)
            projects = [link['href'] for link in project_links if "/projects/" in link['href']]
            
            # Download projects
            for project in projects:
                project_id = project.split("/")[-2]
                project_url = f"https://projects.scratch.mit.edu/{project_id}"
                print(f"Downloading: {project_url}")
                
                try:
                    project_response = requests.get(project_url, headers=headers)
                    project_response.raise_for_status()
                    
                    # Save project file
                    with open(os.path.join(output_dir, f"{project_id}.sb3"), "wb") as f:
                        f.write(project_response.content)
                except Exception as e:
                    print(f"Failed to download project {project_url}: {e}")
        
        except Exception as e:
            print(f"Failed to process {url}: {e}")
    
    print("Download complete.")
    messagebox.showinfo("Info", "Download complete!")

def start_download():
    """Start the download process."""
    try:
        start = int(start_entry.get())
        end = int(end_entry.get())
        if start > end:
            messagebox.showerror("Error", "Start number must be less than or equal to end number.")
            return
        
        # Ask user for output directory
        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir:
            messagebox.showerror("Error", "No output folder selected.")
            return
        
        # Run the download in a separate thread
        Thread(target=download_projects, args=(start, end, output_dir)).start()
    
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for the range.")

# Create the GUI
root = tk.Tk()
root.title("Scratch Project Downloader")

tk.Label(root, text="Start Range:").grid(row=0, column=0, padx=5, pady=5)
start_entry = tk.Entry(root)
start_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="End Range:").grid(row=1, column=0, padx=5, pady=5)
end_entry = tk.Entry(root)
end_entry.grid(row=1, column=1, padx=5, pady=5)

download_button = tk.Button(root, text="Start Download", command=start_download)
download_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
