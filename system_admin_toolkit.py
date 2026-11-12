"""
Python System Administration Toolkit
A beginner-friendly, read-only system monitoring and backup utility.

Features:
1. System overview
2. Disk usage check with low-space warning
3. Folder backup to a timestamped ZIP archive
4. Recent log-file summary
5. Running process list (Windows)
"""

import os
import platform
import shutil
import socket
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path


def show_system_overview():
    """Display basic operating-system and Python information."""
    print("\n=== SYSTEM OVERVIEW ===")
    print(f"Computer name : {socket.gethostname()}")
    print(f"Operating system: {platform.system()} {platform.release()}")
    print(f"OS version    : {platform.version()}")
    print(f"Architecture  : {platform.machine()}")
    print(f"Python version: {platform.python_version()}")


def check_disk_usage():
    """Show disk capacity and warn when free space is below 15 percent."""
    print("\n=== DISK USAGE MONITOR ===")
    drive = os.environ.get("SystemDrive", "C:") + "\\" if os.name == "nt" else "/"
    try:
        total, used, free = shutil.disk_usage(drive)
        total_gb = total / (1024 ** 3)
        used_gb = used / (1024 ** 3)
        free_gb = free / (1024 ** 3)
        free_percent = (free / total) * 100 if total else 0

        print(f"Drive         : {drive}")
        print(f"Total space   : {total_gb:.2f} GB")
        print(f"Used space    : {used_gb:.2f} GB")
        print(f"Free space    : {free_gb:.2f} GB")
        print(f"Free space %  : {free_percent:.1f}%")

        if free_percent < 15:
            print("WARNING: Low disk space. Consider reviewing large files.")
        else:
            print("Status        : Disk space is healthy.")
    except OSError as error:
        print(f"Could not check disk usage: {error}")


def create_folder_backup():
    """Create a timestamped ZIP backup of a folder chosen by the user."""
    print("\n=== FOLDER BACKUP ===")
    source_text = input("Enter the full path of the folder to back up: ").strip().strip('"')
    destination_text = input("Enter the folder where the backup ZIP should be saved: ").strip().strip('"')

    source = Path(source_text).expanduser()
    destination = Path(destination_text).expanduser()

    if not source.exists() or not source.is_dir():
        print("Error: The source path does not exist or is not a folder.")
        return

    # Prevent placing the backup inside the source folder.
    try:
        destination_resolved = destination.resolve()
        source_resolved = source.resolve()
        if destination_resolved == source_resolved or source_resolved in destination_resolved.parents:
            print("Error: Choose a backup destination outside the source folder.")
            return
    except OSError as error:
        print(f"Could not validate paths: {error}")
        return

    try:
        destination.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_path = destination / f"{source.name}_backup_{timestamp}.zip"

        file_count = 0
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file_path in source.rglob("*"):
                if file_path.is_file():
                    archive.write(file_path, file_path.relative_to(source.parent))
                    file_count += 1

        print(f"Backup created : {archive_path}")
        print(f"Files archived: {file_count}")
        print("Status         : Backup completed.")
    except (OSError, zipfile.BadZipFile) as error:
        print(f"Backup failed: {error}")


def summarize_log_file():
    """Display the last lines of a text log file without changing it."""
    print("\n=== LOG FILE SUMMARY ===")
    log_text = input("Enter the full path of a .log or .txt file: ").strip().strip('"')
    log_path = Path(log_text).expanduser()

    if not log_path.is_file():
        print("Error: File not found.")
        return

    if log_path.suffix.lower() not in {".log", ".txt"}:
        print("Please choose a .log or .txt file.")
        return

    try:
        with log_path.open("r", encoding="utf-8", errors="replace") as log_file:
            lines = log_file.readlines()

        print(f"File          : {log_path.name}")
        print(f"Total lines   : {len(lines)}")
        print("Last 10 lines :")
        for line in lines[-10:]:
            print(line.rstrip())
    except OSError as error:
        print(f"Could not read log file: {error}")


def show_running_processes():
    """Display a short list of running processes on Windows."""
    print("\n=== RUNNING PROCESSES ===")
    if os.name != "nt":
        print("This feature currently supports Windows only.")
        return

    try:
        result = subprocess.run(
            ["tasklist", "/FO", "TABLE"],
            capture_output=True,
            text=True,
            check=True,
            timeout=15,
        )
        print("\n".join(result.stdout.splitlines()[:16]))
        print("\nShowing the header and first 15 process entries.")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as error:
        print(f"Could not retrieve process list: {error}")


def show_menu():
    """Display the application menu."""
    print("\n" + "=" * 48)
    print("       PYTHON SYSTEM ADMINISTRATION TOOLKIT")
    print("=" * 48)
    print("1. System overview")
    print("2. Disk usage monitor")
    print("3. Create folder backup (ZIP)")
    print("4. Read recent log entries")
    print("5. View running processes")
    print("0. Exit")
    print("-" * 48)


def main():
    """Run the interactive toolkit."""
    actions = {
        "1": show_system_overview,
        "2": check_disk_usage,
        "3": create_folder_backup,
        "4": summarize_log_file,
        "5": show_running_processes,
    }

    while True:
        show_menu()
        choice = input("Select an option: ").strip()

        if choice == "0":
            print("Exiting toolkit. Goodbye!")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Please choose 0 to 5.")


if __name__ == "__main__":
    main()
