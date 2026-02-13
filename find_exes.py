# find_exes.py
import os, shutil, glob

def find_in_env(name):
    print(f"--- Recherche via shutil.which('{name}')")
    print(shutil.which(name))

def search_roots_for_exe(exe_name, roots):
    found = []
    exe = exe_name if exe_name.lower().endswith(".exe") else exe_name + ".exe"
    for root in roots:
        if not root or not os.path.exists(root):
            continue
        print(f"Search in root: {root}")
        # glob pour chemins avec jokers
        matches = []
        for dirpath, dirnames, filenames in os.walk(root):
            if exe.lower() in (f.lower() for f in filenames):
                full = os.path.join(dirpath, next(f for f in filenames if f.lower() == exe.lower()))
                matches.append(full)
                if len(matches) >= 5:
                    break
        if matches:
            found.extend(matches)
            break
    return found

roots = [os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"),
         os.environ.get("LOCALAPPDATA"), os.environ.get("ProgramW6432")]
print("Roots:", roots)

# noms à tester
names = ["chrome", "winword", "discord", "excel", "notepad"]

for n in names:
    print("\n====", n)
    find_in_env(n)
    res = search_roots_for_exe(n, roots)
    print("Found:", res)
