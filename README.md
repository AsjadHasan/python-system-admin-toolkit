# Python System Administration Toolkit

A beginner-friendly Python command-line project for basic Windows system administration tasks. It uses Python's standard library and is designed for learning and portfolio demonstration.

## Features

- **System overview:** hostname, OS, architecture, and Python version.
- **Disk usage monitor:** total, used, and free disk space, with a warning when free space is below 15%.
- **Folder backup:** creates a timestamped ZIP archive of a folder chosen by the user.
- **Log-file reader:** displays the total number of lines and the last 10 lines of a `.log` or `.txt` file.
- **Running processes:** displays a short process list using Windows `tasklist`.

## Requirements

- Python 3.10 or later (tested target: Python 3.x)
- Windows 10/11 for the running-process feature
- No third-party packages required

## Run

```powershell
python system_admin_toolkit.py
```

## Backup example

When prompted, enter a source folder and a separate destination folder, for example:

```text
Source: E:\Work\Reports
Destination: E:\Backups
```

The program creates a timestamped ZIP file in the destination folder. It does not delete or modify the source files.

## Safety notes

- The toolkit is intended for local, read-only inspection except for the explicit ZIP backup operation.
- It does not delete files, terminate processes, change system settings, or upload data.
- Choose a backup destination outside the source folder.
- Do not publish private logs, personal files, usernames, IP addresses, or screenshots containing sensitive information.

## Technologies

- Python
- `os`, `platform`, `socket`, `shutil`, `subprocess`, `zipfile`, `pathlib`, `datetime`

## Planned improvements

- Export system and disk reports to text/CSV.
- Add backup verification.
- Add configurable disk-space warning thresholds.
- Add unit tests.
