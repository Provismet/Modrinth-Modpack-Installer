# Vanilla Launcher Modrinth Modpack Installer
Modrinth doesn't currently support downloading modpacks directly from the website, but it is possible to do so via 3rd party launchers or the API. This tool is for anyone who simply doesn't want to use a 3rd party launcher to download modpacks.

## Instructions
1. Download the modpack file from Modrinth.
   - The filetype is `.mrpack`.
2. Create an empty new folder to place the Minecraft profile in.
   - The folder does not need to be already initialised as a Minecraft profile, any empty folder will do.
3. Launch the modpack installer.
4. Use the buttons to browse to your newly created folder and the modpack `.mrpack` file.
5. Press download.

## Notes
The installer will create a temporary folder in the same directory that it is placed in (`./modrinthInstallerTemp`), this folder *should* be automatically deleted when execution finishes.  
If the installer fails to remove the temporary folder for whatever reason then a message will be logged asking you to do so manually.
