# jarvis/core/app_launcher.py
import os
import subprocess
import shutil
from pathlib import Path
from difflib import get_close_matches
import winreg  # Windows only
try:
    # pywin32 is optional but recommended to resolve .lnk targets
    from win32com.client import Dispatch
except Exception:
    Dispatch = None

START_MENU_PATHS = [
    Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
    Path(os.environ.get("APPDATA", r"C:\Users\Default\AppData\Roaming")) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
]

PROGRAM_FILES_PATHS = [
    Path(os.environ.get("ProgramFiles", r"C:\Program Files")),
    Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")),
]

# Optional: explicit whitelist (only these apps allowed to be started)
DEFAULT_WHITELIST = None  # e.g. {"chrome", "notepad", "code"}

class AppLauncher:
    def __init__(self, whitelist: set | None = DEFAULT_WHITELIST):
        self.whitelist = {w.lower() for w in whitelist} if whitelist else None
        self._index = {}  # name_lower -> {"name":display, "path":path}
        self.index_apps()

    def index_apps(self):
        apps = {}
        # 1) scan Start Menu shortcuts (.lnk, .url, .exe)
        for sm_path in START_MENU_PATHS:
            if not sm_path.exists():
                continue
            for p in sm_path.rglob("*"):
                if p.is_file():
                    name = p.stem.lower()
                    if p.suffix.lower() in (".lnk", ".url"):
                        target = self._resolve_lnk(p) or str(p)
                        apps.setdefault(name, []).append({"display": p.stem, "path": target, "source": str(p)})
                    elif p.suffix.lower() == ".exe":
                        apps.setdefault(name, []).append({"display": p.stem, "path": str(p), "source": str(p)})

        # 2) scan PATH executables
        for dir_path in os.environ.get("PATH", "").split(os.pathsep):
            try:
                d = Path(dir_path)
            except Exception:
                continue
            if not d.exists():
                continue
            for f in d.iterdir():
                if f.is_file() and f.suffix.lower() in (".exe", ".bat", ".cmd"):
                    name = f.stem.lower()
                    apps.setdefault(name, []).append({"display": f.stem, "path": str(f), "source": str(d)})

        # 3) optionally scan Program Files for common exes (quick scan)
        for base in PROGRAM_FILES_PATHS:
            if not base.exists():
                continue
            for exe in base.rglob("*.exe"):
                name = exe.stem.lower()
                apps.setdefault(name, []).append({"display": exe.stem, "path": str(exe), "source": str(exe.parent)})

        # 4) registry "Uninstall" keys (gives DisplayName and InstallLocation) - optional best-effort
        for hive, flag in ((winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY | winreg.KEY_READ),
                           (winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY | winreg.KEY_READ),
                           (winreg.HKEY_CURRENT_USER, winreg.KEY_READ)):
            try:
                with winreg.OpenKey(hive, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, flag) as root:
                    for i in range(0, winreg.QueryInfoKey(root)[0]):
                        try:
                            sub = winreg.EnumKey(root, i)
                            with winreg.OpenKey(root, sub) as k:
                                try:
                                    disp, _ = winreg.QueryValueEx(k, "DisplayName")
                                except Exception:
                                    continue
                                try:
                                    installloc, _ = winreg.QueryValueEx(k, "InstallLocation")
                                except Exception:
                                    installloc = ""
                                disp_name = disp.strip().lower()
                                if installloc:
                                    apps.setdefault(disp_name, []).append({"display": disp, "path": installloc, "source": "registry"})
                        except OSError:
                            continue
            except Exception:
                continue

        # pick canonical entry for each name (first one)
        final = {}
        for k, v in apps.items():
            final[k] = v  # keep list of candidates
        self._index = final

    def _resolve_lnk(self, lnk_path: Path) -> str | None:
        """Try to resolve .lnk using pywin32 if available."""
        if Dispatch is None:
            return None
        try:
            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(lnk_path))
            return shortcut.Targetpath or None
        except Exception:
            return None

    def list_index(self) -> dict:
        return self._index

    def find_candidates(self, name: str, max_matches: int = 5) -> list:
        name_l = name.lower()
        keys = list(self._index.keys())
        # exact match
        if name_l in self._index:
            return self._index[name_l]
        # substring matches
        subs = [k for k in keys if name_l in k]
        if subs:
            candidates = []
            for k in subs[:max_matches]:
                candidates.extend(self._index[k])
            return candidates
        # fuzzy matches
        close = get_close_matches(name_l, keys, n=max_matches, cutoff=0.6)
        candidates = []
        for k in close:
            candidates.extend(self._index[k])
        return candidates

    def _is_allowed(self, display_name: str) -> bool:
        if self.whitelist is None:
            return True
        return display_name.lower() in self.whitelist

    def launch(self, candidate: dict, wait: bool = False) -> dict:
        """
        candidate is a dict {"display":..., "path":..., "source":...}
        returns info dict {ok:bool, message:str}
        """
        path = candidate.get("path")
        if not path:
            return {"ok": False, "message": "Pas de chemin cible."}

        display = candidate.get("display", path)
        if not self._is_allowed(display):
            return {"ok": False, "message": f"Application '{display}' non autorisée par la whitelist."}

        # If path points to a directory, try to find an exe inside, or use start to open the folder
        p = Path(path)
        try:
            if p.exists() and p.is_dir():
                # try to find exe in folder
                exes = list(p.glob("*.exe"))
                if exes:
                    target = str(exes[0])
                    subprocess.Popen(["start", "", target], shell=True)
                    return {"ok": True, "message": f"Lancement de {display} ({target})"}
                else:
                    subprocess.Popen(["start", "", str(p)], shell=True)
                    return {"ok": True, "message": f"Ouverture du dossier {display}"}
            else:
                # if the path is an exe or other file, use start (lets Windows handle it)
                subprocess.Popen(["start", "", str(path)], shell=True)
                return {"ok": True, "message": f"Lancement de {display} ({path})"}
        except Exception as e:
            return {"ok": False, "message": f"Erreur lors du lancement: {e}"}
