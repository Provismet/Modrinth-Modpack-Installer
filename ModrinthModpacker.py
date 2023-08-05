# 2023, Provismet

import requests, json, os.path, os
from tkinter import filedialog, ttk
import tkinter as tk
from zipfile import ZipFile
from threading import Thread

modrinthHeaders = {"User-Agent": "Provi Modpack Installer (https://github.com/Provismet) no repo yet"}

class OutputDisplay (tk.Frame):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textBox = tk.Text(self)
        self.textBox.grid(column=0, row=0, sticky="nsew", padx=2, pady=2)

        scrollb = tk.Scrollbar(self, command=self.textBox.yview)
        scrollb.grid(column=1, row=0, sticky='nsew')
        self.textBox['yscrollcommand'] = scrollb.set

        self.progressBar = ttk.Progressbar(self, mode="determinate", length=650)
        self.progressBar.grid(column=0, row=1)
    
    def append (self, message: str):
        self.textBox.insert(tk.END, "\n" + message)
        self.textBox.see(tk.END)
    
    def setProgressBarMaximum (self, maximumValue: int):
        self.progressBar.configure(maximum=maximumValue)
    
    def incrementProgressBar (self, amount=1):
        self.progressBar.step(amount)

def downloadSingleMod (url: str, downloadPath: str, output: OutputDisplay) -> None:
    modName = os.path.basename(downloadPath)
    response = None
    hadError = False

    try:
        response = requests.get(url, headers=modrinthHeaders)
    except Exception as e:
        output.append(f"Could not download mod ({modName}) from URL: {url}")
        hadError = True
    
    if response != None:
        try:
            with open(downloadPath, 'wb') as file:
                file.write(response.content)
        except Exception as e:
            output.append(f"Could not save mod ({modName}) due to error: {str(e)}")
            output.append(f"Please manually download mod ({modName}) from url: {url}")
            hadError = True
    
    if not hadError:
        output.append(f"Downloaded: {modName}")


def main (directory: str, modpack: str, output: OutputDisplay) -> None:
    tempDirectory = os.path.join(os.curdir, ".modrinthInstallerTemp")

    try:
        os.makedirs(tempDirectory)

        with ZipFile(modpack, 'r') as zip:
            zip.extractall(tempDirectory)
        
        overridesFolder = os.path.join(tempDirectory, "overrides")

        if os.path.isdir(overridesFolder):
            for filename in os.listdir(overridesFolder):
                os.rename(os.path.join(overridesFolder, filename), os.path.join(directory, filename))

        if not os.path.isdir(os.path.join(directory, "mods")):
            os.makedirs(os.path.join(directory, "mods"))
        
        indexFile = open(os.path.join(tempDirectory, "modrinth.index.json"))
        jsonIndex = json.load(indexFile)
        indexFile.close()

        output.append(f"Downloading {len(jsonIndex['files'])} mods...")
        output.setProgressBarMaximum(len((jsonIndex['files'])))
        for fileData in jsonIndex["files"]:
            downloadSingleMod(fileData["downloads"][0], os.path.join(directory, fileData["path"]), output)
            output.incrementProgressBar()
        
        output.append("\nDone.")
    except Exception as e:
        output.append(f"\nFailed due to error: {str(e)}")
        output.append("Try again with administrator privileges.\n")

    try:
        os.remove(tempDirectory)
    except Exception as e:
        output.append(f"Failed to remove temporary directory: \"{tempDirectory}\"")
        output.append("Please remove temporary directory manually.")

def setProfileDirectory (entryBox: tk.Entry) -> None:
    directoryName = filedialog.askdirectory()
    entryBox.delete(0, tk.END)
    entryBox.insert(0, directoryName)

def setModpackFile (entryBox: tk.Entry) -> None:
    filename = filedialog.askopenfilename(title = "Select a Modpack", filetypes = (("Modrinth Pack", "*.mrpack*"), ("ZIP Files", "*.zip*"), ("all files", "*.*")))
    entryBox.delete(0, tk.END)
    entryBox.insert(0, filename)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Modrinth Modpack Installer")

    profileFrame = tk.Frame(root)
    profileFrame.grid(column=0, row=0)
    tk.Label(profileFrame, text="Minecraft Profile: ", width=15).pack(side=tk.LEFT)
    profileEntry = tk.Entry(profileFrame, width=100)
    profileEntry.pack(side=tk.LEFT)
    tk.Button(profileFrame, text="Browse", command=lambda: setProfileDirectory(profileEntry)).pack(side=tk.LEFT)

    modpackFrame = tk.Frame(root)
    modpackFrame.grid(column=0, row=1)
    tk.Label(modpackFrame, text="Modpack File: ", width=15).pack(side=tk.LEFT)
    modpackEntry = tk.Entry(modpackFrame, width=100)
    modpackEntry.pack(side=tk.LEFT)
    tk.Button(modpackFrame, text="Browse", command=lambda: setModpackFile(modpackEntry)).pack(side=tk.LEFT)

    workingFrame = tk.Frame(root)
    workingFrame.grid(column=0, row=2)
    workingOutputBox = OutputDisplay(workingFrame)
    workingOutputBox.config(width=650, height=600)
    tk.Button(workingFrame, text="Download Files", command=Thread(target=lambda: main(profileEntry.get(), modpackEntry.get(), workingOutputBox)).start).pack(side=tk.TOP)
    workingOutputBox.pack(fill="both", expand=True)

    root.mainloop()