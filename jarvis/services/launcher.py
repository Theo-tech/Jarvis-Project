# jarvis/services/launcher.py
import os
import shutil
import glob
import json
from pathlib import Path
import subprocess

INDEX_PATH = Path(r"C:\Projects\file_index.json")

PRIORITY_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

def load_index():
    try:
        if INDEX_PATH.exists():
            return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {}

def find_in_index(name: str):
    idx = load_index()
    key = name.lower() if name.lower().endswith(".exe") else (name + ".exe").lower()
    entries = idx.get(key)
    if entries:
        # retourne le premier résultat valide
        for p in entries:
            if os.path.exists(p):
                return p
    return None

def find_executable_by_name(name: str):
    if not name:
        return None

    # 1) index
    found = find_in_index(name)
    if found:
        return found

    # 2) shutil.which
    exe = shutil.which(name)
    if exe:
        return exe

    candidate = name if name.lower().endswith(".exe") else name + ".exe"

    # 3) prioritary known paths
    for p in PRIORITY_PATHS:
        p_exp = os.path.expandvars(p)
        if p_exp.endswith(".exe"):
            if os.path.exists(p_exp):
                return p_exp
        else:
            # support wildcard
            matches = glob.glob(p_exp)
            if matches:
                return matches[0]

    # 4) simple glob over ProgramFiles dirs (non recursive heavy)
    roots = [os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"), os.environ.get("LOCALAPPDATA")]
    roots = [r for r in roots if r]
    for root in roots:
        pattern = os.path.join(root, "**", candidate)
        try:
            matches = glob.glob(pattern, recursive=True)
            if matches:
                return matches[0]
        except Exception:
            continue

    return None

def open_target(path: str):
    try:
        # prefer os.startfile on Windows
        os.startfile(path)
        return True, None
    except Exception as e:
        try:
            subprocess.Popen([path], shell=False)
            return True, None
        except Exception as e2:
            return False, f"{e} / {e2}"

def build_open_app_handler():
    def handler(intent: dict, raw_text: str = ""):
        app_name = intent.get("slots", {}).get("app_name", "") or (raw_text or "")
        app_name = app_name.strip().lower()
        if not app_name:
            return {"reply": "Quel appareil veux-tu ouvrir ? (ex: 'ouvre chrome')"}
        target = find_executable_by_name(app_name)
        if not target:
            return {"reply": f"Je n'ai pas trouvé d'application correspondant à '{app_name}'."}
        ok, err = open_target(target)
        if ok:
            return {"reply": f"✅ Lancement de {app_name} ({target})"}
        return {"reply": f"Erreur en lançant {app_name} : {err}"}
    return handler
