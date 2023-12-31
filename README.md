# Vanilla Launcher Modrinth Modpack Installer
Modrinth doesn't currently support downloading modpacks directly from the website, but it is possible to do so via 3rd party launchers or the API. This tool is for anyone who simply doesn't want to use a 3rd party launcher to download modpacks.

## Instructions
### Setup
If you *understandably* don't want to download a sketchy .exe from the internet, then follow these steps to run the Python script yourself. Otherwise just skip to the next section.
1. Install [Python 3](https://www.python.org/downloads/).
2. Make sure you have pip (the Python package installer) as part of your installation.
3. In a commandline run `pip install requests`.
4. Run the Modrinth Modpack Installer with Python.

### Using The Tool
1. Download the modpack file from Modrinth.
   - The filetype is `.mrpack`.
2. Create an empty new folder to place the Minecraft profile in.
   - The folder does not need to be already initialised as a Minecraft profile, any empty folder will do.
3. Launch the modpack installer.
4. Use the buttons to browse to your newly created folder and the modpack `.mrpack` file.
5. Press download.

## Notes
- The installer will create a temporary folder in the same directory that it is placed in (`./modrinthInstallerTemp`), this folder *should* be automatically deleted when execution finishes.  
  - If the installer fails to remove the temporary folder for whatever reason then a message will be logged asking you to do so manually.
- The installer may fail if the modpack file, the destination folder, and itself are not all placed within the same drive. Move your files around as appropriate.
