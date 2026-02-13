# find_exes_verbose.py
import os, shutil, glob, sys, time

log_path = "find_exes_debug.txt"
def log(msg):
    print(msg)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")

def show_env():
    envs = ["ProgramFiles", "ProgramFiles(x86)", "ProgramW6432", "LOCALAPPDATA", "SystemDrive"]
    for k in envs:
        val = os.environ.get(k)
        log(f"ENV {k} -> {val}")

def test_which(names):
    for n in names:
        w = shutil.which(n)
        log(f"shutil.which('{n}') -> {w}")

def search_roots_for_exe(exe_name, roots, max_found_per_root=3, max_dirs=200000):
    found = []
    exe = exe_name if exe_name.lower().endswith(".exe") else exe_name + ".exe"
    log(f"Searching for {exe} in {len(roots)} roots")
    for root in roots:
        if not root:
            log(f" - skip empty root")
            continue
        if not os.path.exists(root):
            log(f" - root does not exist: {root}")
            continue
        log(f" - scanning root: {root}")
        count = 0
        try:
            for dirpath, dirnames, filenames in os.walk(root):
                count += 1
                if count % 1000 == 0:
                    log(f"   scanned {count} dirs in {root}...")
                if exe.lower() in (f.lower() for f in filenames):
                    matched = os.path.join(dirpath, next(f for f in filenames if f.lower()==exe.lower()))
                    log(f"   FOUND: {matched}")
                    found.append(matched)
                    if len(found) >= max_found_per_root:
                        break
                if count >= max_dirs:
                    log(f"   reached max_dirs ({max_dirs}) in {root}, stopping this root")
                    break
        except Exception as e:
            log(f"   error scanning {root}: {e}")
        if found:
            break
    return found

def quick_probe_common_paths(names):
    patterns = [
        r"%ProgramFiles%\\**\\{exe}",
        r"%ProgramFiles(x86)%\\**\\{exe}",
        r"%LOCALAPPDATA%\\**\\{exe}",
        r"%ProgramW6432%\\**\\{exe}"
    ]
    for n in names:
        exe = n if n.lower().endswith(".exe") else n + ".exe"
        log(f"--- probing common patterns for {exe}")
        for p in patterns:
            pat = os.path.expandvars(p.format(exe=exe))
            # glob with recursive
            try:
                matches = glob.glob(pat, recursive=True)
                log(f" pattern {pat} -> {len(matches)} matches (show up to 5)")
                for m in matches[:5]:
                    log(f"   -> {m}")
                if matches:
                    break
            except Exception as e:
                log(f"  glob error for {pat}: {e}")

if __name__ == "__main__":
    # supprime ancien log
    try:
        if os.path.exists(log_path):
            os.remove(log_path)
    except:
        pass

    log("=== START find_exes_verbose ===")
    show_env()
    names = ["chrome", "winword", "discord", "excel", "notepad"]
    test_which(names)

    # racines usuelles
    roots = [
        os.environ.get("ProgramFiles"),
        os.environ.get("ProgramFiles(x86)"),
        os.environ.get("LOCALAPPDATA"),
        os.environ.get("ProgramW6432"),
    ]
    log(f"Roots to scan: {roots}")

    for n in names:
        log(f"\n>>> Searching name: {n}")
        found = search_roots_for_exe(n, roots, max_found_per_root=2, max_dirs=50000)
        log(f"Result for {n}: {found}")

    # Optionnel: si tu veux que je fasse une recherche disque complète,
    # décommente la section suivante (peut prendre beaucoup de temps).
    """
    # SEARCH ENTIRE DISK (C: and D:)
    disks = []
    sys_dr = os.environ.get("SystemDrive", "C:")
    disks.append(sys_dr)
    if os.path.exists("D:\\"):
        disks.append("D:\\")
    log(f"Disks to full-scan (slow): {disks}")
    for d in disks:
        for n in names:
            log(f"--- Full-scan {d} for {n} (this can be very slow)")
            res = search_roots_for_exe(n, [d], max_found_per_root=1, max_dirs=1000000)
            log(f"full-scan result for {n} on {d}: {res}")
    """

    log("=== END find_exes_verbose ===")
    log(f"Log saved to {os.path.abspath(log_path)}")
