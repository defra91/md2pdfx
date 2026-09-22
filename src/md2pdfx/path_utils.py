from pathlib import Path

def wsl_to_windows(path: Path) -> str:
    p = str(path)

    if p.startswith("/mnt/"):
        drive = p[5].upper() + ":"
        rest = p[7:].replace("/", "\\")
        return f"{drive}\\{rest}"

    return p
