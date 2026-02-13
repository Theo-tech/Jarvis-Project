# jarvis/agents/system_agent.py
import shlex, subprocess

class SystemAgent:
    def run_command(self, cmd: str) -> dict:
        if not cmd:
            return {"reply": "Aucune commande fournie."}
        # protection simple : blacklist de commandes dangereuses
        blacklist = {"rm", "del", "format", "shutdown", "poweroff"}
        if any(token in blacklist for token in cmd.split()):
            return {"reply": "Commande bloquée pour sécurité."}
        try:
            args = shlex.split(cmd)
            result = subprocess.run(args, capture_output=True, text=True, timeout=10)
            out = result.stdout.strip() or result.stderr.strip()
            return {"reply": f"Résultat : {out}"}
        except Exception as e:
            return {"reply": f"Erreur exécution : {e}"}
