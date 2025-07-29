# InstallerPro v4 – Humberto Medina · Mayo 2025
#
# ◉ Multi-idioma (Español / English) – selector en menú
# ◉ Multi-proyecto  –  añade / actualiza / elimina proyectos Git
# ◉ Auto-descubrimiento – detecta carpetas con .git en C:\Workspace
# ◉ Maneja ‘dubious ownership’, credenciales, Git ausente

from __future__ import annotations  # (si usas anotaciones futuras)

import os
import subprocess
import shutil
import webbrowser
import json
import tkinter as tk
from tkinter import simpledialog, ttk

# --- referencias globales (se asignan en run_gui) ------------------------
root: tk.Tk | None = None
title_lbl: tk.Label | None = None
frame: tk.Frame | None = None
listbox: tk.Listbox | None = None
add_btn: tk.Button | None = None
rem_btn: tk.Button | None = None
upd_btn: tk.Button | None = None
exit_btn: tk.Button | None = None
menubar: tk.Menu | None = None
lang_menu: tk.Menu | None = None
theme_menu: tk.Menu | None = None
progress: ttk.Progressbar | None = None

# ---------- ajustes persistentes -------------------------------------------
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")


def load_settings() -> dict:
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        # valores por defecto
        return {"lang": "es", "theme": "System"}


def save_settings(lang: str, theme: str) -> None:
    data = {"lang": lang, "theme": theme}
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
    except Exception as e:
        print("⚠️  No se pudo guardar settings:", e)


# ============ Configuración global ============
WORKSPACE = r"C:\Workspace"
DB_FILE = os.path.join(WORKSPACE, "_projects.json")

LANG = {
    "es": {
        "title": "Instalador Automático de Entorno",
        "add": "Añadir proyecto",
        "remove": "Eliminar proyecto",
        "update": "Actualizar seleccionados",
        "exit": "Salir",
        "name?": "Nombre del proyecto:",
        "url?": "URL del repositorio Git (HTTPS):",
        "ok": "Proyecto listo en:\n{}",
        "git?": "Git no está instalado.\nDescárgalo en https://git-scm.com",
        "login": "Autoriza tu cuenta GitHub en el navegador.\nPulsa Aceptar para continuar.",
        "nothing": "No hay proyectos seleccionados.",
        "unknown": "(desconocida)",
        "menu_lang": "Idioma",
        "menu_es": "Español",
        "menu_en": "English",
    },
    "en": {
        "title": "Automatic Environment Installer",
        "add": "Add project",
        "remove": "Remove project",
        "update": "Update selected",
        "exit": "Exit",
        "name?": "Project name:",
        "url?": "Git repository URL (HTTPS):",
        "ok": "Project ready at:\n{}",
        "git?": "Git is not installed.\nDownload it from https://git-scm.com",
        "login": "Authorize GitHub account in browser.\nPress OK to continue.",
        "nothing": "No project selected.",
        "unknown": "(unknown)",
        "menu_lang": "Language",
        "menu_es": "Spanish",
        "menu_en": "English",
    },
}

# ---------- temas (Light / Dark) -------------------------------------------
THEMES = {
    "Light": {
        "bg": "#F7F7F7",
        "fg": "#000000",
        "btn_bg": "#E2E2E2",
        "btn_fg": "#000000",
        "sel_bg": "#C8DCF0",
        "sel_fg": "#000000",
    },
    "Dark": {
        "bg": "#202124",
        "fg": "#E8EAED",
        "btn_bg": "#303134",
        "btn_fg": "#E8EAED",
        "sel_bg": "#44464B",
        "sel_fg": "#E8EAED",
    },
}

_CFG = load_settings()
CURRENT = _CFG.get("lang", "es")
CURRENT_THEME = _CFG.get("theme", "System")
TXT = LANG[CURRENT]


# --------- helper: tema del sistema (Windows 10/11) ------------------------
def _detect_system_theme() -> str:
    """Lee el registro y devuelve 'Dark' o 'Light' (fallback Light)."""
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        ) as key:
            # AppsUseLightTheme: 0 = oscuro, 1 = claro
            use_light, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return "Light" if use_light else "Dark"
    except Exception:
        return "Light"  # plataformas no-Windows o error


# --------- vigilancia en vivo del tema del sistema -------------------------
_LAST_SYS_THEME = _detect_system_theme()


def _watch_system_theme():
    """Cada 3 s comprueba si el SO pasó de Light⇄Dark y reactualiza la UI."""
    global _LAST_SYS_THEME
    if CURRENT_THEME == "System":
        new = _detect_system_theme()
        if new != _LAST_SYS_THEME:
            _LAST_SYS_THEME = new
            apply_theme("System")  # aplica paleta nueva
    root.after(3000, _watch_system_theme)  # re-programa


# ============ Funciones utilitarias Git ============
def run(cmd):
    """Ejecuta comando y devuelve (ok, salida)"""
    try:
        out = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, text=True, shell=False
        )
        return True, out.strip()
    except subprocess.CalledProcessError as e:
        return False, e.output.strip()


def need_auth(text: str) -> bool:
    t = text.lower()
    return any(
        w in t for w in ("authentication", "could not read", "permission denied")
    )


def ensure_git():
    ok, _ = run(["git", "--version"])
    if not ok:
        show_msg("error", "Git", TXT["git?"])
        raise SystemExit


def safe_dir(path: str):
    run(
        [
            "git",
            "config",
            "--global",
            "--add",
            "safe.directory",
            path.replace("\\", "/"),
        ]
    )


def auth_flow():
    webbrowser.open("https://github.com/login")
    show_msg("info", "Login", TXT["login"])


# ---------- Clonar o actualizar -------------------------------------------
def clone_or_pull(name: str, url: str, branch: str) -> str:
    dest = os.path.join(WORKSPACE, name)
    safe_dir(dest)

    # --- clone ------------------------------------------------------------
    if not os.path.exists(dest) or not os.path.exists(os.path.join(dest, ".git")):
        if os.path.exists(dest):
            shutil.rmtree(dest, ignore_errors=True)

        ok, out = run(["git", "clone", "-b", branch, url, dest])

    # --- pull -------------------------------------------------------------
    else:
        ok, out = run(["git", "-C", dest, "checkout", branch])
        ok, out = run(["git", "-C", dest, "pull"])

        # ----- sin upstream: configure y repite pull --------------------------
        if not ok and "no tracking information for the current branch" in out.lower():
            # 1) Obtener branch actual
            ok_b, branch = run(["git", "-C", dest, "rev-parse", "--abbrev-ref", "HEAD"])
            branch = branch.strip() if ok_b else "main"

            # 2) fetch para asegurar refs remotas
            run(["git", "-C", dest, "fetch", "--all"])

            # 3) configurar upstream -> origin/<branch>
            run(
                [
                    "git",
                    "-C",
                    dest,
                    "branch",
                    "--set-upstream-to",
                    f"origin/{branch}",
                    branch,
                ]
            )

            # 4) intentar pull otra vez
            ok, out = run(["git", "-C", dest, "pull"])

            # ----- aún sin upstream → lo ignoramos ------------------------------
        if not ok and "no tracking information for the current branch" in out.lower():
            ok = True  # lo damos por actualizado

        if not ok:
            raise RuntimeError(out)

    return dest


# ============ Estilos de tema ==============================================
def apply_theme(theme: str) -> None:
    """
    Cambia la paleta de la interfaz.

    Si la ventana aún NO está creada (root is None) salimos silenciosamente
    — esto permite llamar a apply_theme() en pruebas, antes de run_gui().
    """
    if root is None:
        return

    global CURRENT_THEME

    if theme == "System":
        theme = _detect_system_theme()

    CURRENT_THEME = theme

    pal = THEMES[theme]
    root.configure(bg=pal["bg"])
    title_lbl.config(bg=pal["bg"], fg=pal["fg"])
    frame.config(bg=pal["bg"])
    listbox.config(
        bg=pal["bg"],
        fg=pal["fg"],
        selectbackground=pal["sel_bg"],
        selectforeground=pal["sel_fg"],
    )

    for btn in (add_btn, rem_btn, upd_btn, exit_btn):
        btn.config(
            bg=pal["btn_bg"],
            fg=pal["btn_fg"],
            activebackground=pal["btn_bg"],
            activeforeground=pal["btn_fg"],
        )

    save_settings(CURRENT, CURRENT_THEME)


# ============ Diálogos temáticos ===========================================
def show_msg(kind: str, title: str, text: str) -> None:
    """
    Mensaje modal estilado con el tema actual.
    Si la ventana principal aún no existe, simplemente imprime al stdout.
    """
    if root is None:
        print(f"[{kind.upper()}] {title}: {text}")
        return

    pal = THEMES[_detect_system_theme() if CURRENT_THEME == "System" else CURRENT_THEME]

    dlg = tk.Toplevel(root, bg=pal["bg"])
    dlg.title(title)
    dlg.transient(root)
    dlg.grab_set()
    dlg.resizable(False, False)

    tk.Label(
        dlg,
        text=text,
        bg=pal["bg"],
        fg=pal["fg"],
        wraplength=360,
        justify="left",
        padx=20,
        pady=15,
    ).pack()

    tk.Button(
        dlg,
        text="Aceptar",
        command=dlg.destroy,
        bg=pal["btn_bg"],
        fg=pal["btn_fg"],
        activebackground=pal["btn_bg"],
        activeforeground=pal["btn_fg"],
        width=12,
    ).pack(pady=(0, 12))

    dlg.update_idletasks()
    w, h = dlg.winfo_width(), dlg.winfo_height()
    x = root.winfo_x() + (root.winfo_width() - w) // 2
    y = root.winfo_y() + (root.winfo_height() - h) // 2
    dlg.geometry(f"{w}x{h}+{x}+{y}")

    root.wait_window(dlg)


def show_confirm(text: str) -> bool:
    """
    Cuadro Sí/No.  Devuelve True al confirmar.
    En contexto head-less (root is None) pregunta por terminal.
    """
    if root is None:
        ans = input(f"{text} (s/N) ").strip().lower()
        return ans in ("s", "y", "yes")

    pal = THEMES[_detect_system_theme() if CURRENT_THEME == "System" else CURRENT_THEME]

    dlg = tk.Toplevel(root, bg=pal["bg"])
    dlg.title("Confirmar")
    dlg.transient(root)
    dlg.grab_set()
    dlg.resizable(False, False)

    tk.Label(
        dlg,
        text=text,
        bg=pal["bg"],
        fg=pal["fg"],
        wraplength=360,
        justify="left",
        padx=20,
        pady=15,
    ).pack()

    f = tk.Frame(dlg, bg=pal["bg"])
    f.pack(pady=(0, 12))

    tk.Button(
        f,
        text="Sí",
        width=10,
        bg=pal["btn_bg"],
        fg=pal["btn_fg"],
        activebackground=pal["btn_bg"],
        activeforeground=pal["btn_fg"],
        command=lambda: dlg.destroy() or dlg.__setattr__("result", True),
    ).pack(side="left", padx=6)

    tk.Button(
        f,
        text="No",
        width=10,
        bg=pal["btn_bg"],
        fg=pal["btn_fg"],
        activebackground=pal["btn_bg"],
        activeforeground=pal["btn_fg"],
        command=lambda: dlg.destroy() or dlg.__setattr__("result", False),
    ).pack(side="right", padx=6)

    dlg.result = False
    dlg.update_idletasks()
    w, h = dlg.winfo_width(), dlg.winfo_height()
    x = root.winfo_x() + (root.winfo_width() - w) // 2
    y = root.winfo_y() + (root.winfo_height() - h) // 2
    dlg.geometry(f"{w}x{h}+{x}+{y}")

    root.wait_window(dlg)
    return dlg.result


# ============ Base de datos de proyectos ============
def load_db() -> dict:
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as fh:
            base = json.load(fh)
    else:
        base = {}

    # --- migración formato antiguo -----------------------------------------
    for k, v in list(base.items()):
        if isinstance(v, str):
            base[k] = {"url": v, "branch": "main"}

    base = auto_discover(base)
    save_db(base)
    return base


def save_db(db: dict):
    os.makedirs(WORKSPACE, exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as fh:
        json.dump(db, fh, indent=2)


def auto_discover(db: dict) -> dict:
    """Añade a db las carpetas con .git no registradas."""
    if not os.path.isdir(WORKSPACE):
        return db
    for entry in os.listdir(WORKSPACE):
        path = os.path.join(WORKSPACE, entry)
        if entry.startswith("_") or not os.path.isdir(path):
            continue
        if entry in db:
            continue
        if os.path.isdir(os.path.join(path, ".git")):
            ok, out = run(["git", "-C", path, "config", "--get", "remote.origin.url"])
            # migración: si antes guardábamos solo la URL → dict con branch=main
            db[entry] = (
                {"url": out, "branch": "main"}
                if ok and out
                else {"url": TXT["unknown"], "branch": "main"}
            )
    return db


# ============ GUI callbacks ============
def refresh_list():
    listbox.delete(0, tk.END)
    for k in sorted(load_db().keys()):
        listbox.insert(tk.END, k)


def add_project():
    name = simpledialog.askstring("name", TXT["name?"])
    if not name:
        return
    url = simpledialog.askstring("url", TXT["url?"])
    if not url:
        return
    branch = simpledialog.askstring("branch", "Branch (default: main)") or "main"

    db = load_db()
    db[name] = {"url": url, "branch": branch}  # ← guarda como dict
    save_db(db)
    refresh_list()


def remove_project():
    sel = list(listbox.curselection())
    if not sel:
        return

    names = [listbox.get(i) for i in sel]
    msg = "\n".join(names)
    if len(names) == 1:
        txt = f"¿Eliminar el proyecto?\n\n{msg}"
    else:
        txt = f"¿Eliminar estos {len(names)} proyectos?\n\n{msg}"

    if show_confirm(txt) is False:  # ← usuario canceló
        return

    db = load_db()
    for idx in reversed(sel):
        name = listbox.get(idx)
        listbox.delete(idx)
        db.pop(name, None)
    save_db(db)


def update_selected():
    sel = list(listbox.curselection())
    if not sel:
        show_msg("info", "Info", TXT["nothing"])
        return

    ensure_git()
    db = load_db()
    jobs = [listbox.get(i) for i in sel]

    progress["maximum"] = len(jobs)
    progress["value"] = 0
    root.update_idletasks()

    for i, name in enumerate(jobs, 1):
        data = db[name]
        url = data["url"]
        branch = data["branch"]
        try:
            clone_or_pull(name, url, branch)
        except RuntimeError as e:
            show_msg("error", "Git", f"{name} → {e}")
            continue
        finally:
            progress["value"] = i
            root.update_idletasks()

    show_msg("info", "OK", TXT["ok"].format(WORKSPACE))
    progress["value"] = 0  # reinicia


def set_language(lang_code):
    global CURRENT, TXT
    CURRENT = lang_code
    TXT = LANG[CURRENT]

    # Renombra la etiqueta del cascade Idioma
    try:
        menubar.entryconfigure(0, label=TXT["menu_lang"])
    except tk.TclError:
        pass  # primera carga

    lang_menu.entryconfigure(0, label=LANG["es"]["menu_es"])
    lang_menu.entryconfigure(1, label=LANG["en"]["menu_en"])

    root.title("InstallerPro")
    title_lbl.config(text=TXT["title"])
    add_btn.config(text=TXT["add"])
    rem_btn.config(text=TXT["remove"])
    upd_btn.config(text=TXT["update"])
    exit_btn.config(text=TXT["exit"])
    refresh_list()

    save_settings(CURRENT, CURRENT_THEME)


# ============ GUI ============
def run_gui() -> None:
    global root, title_lbl, frame, listbox
    global add_btn, rem_btn, upd_btn, exit_btn
    global menubar, lang_menu, theme_menu, progress

    # --- instancia raíz --------------------------------------------------
    root = tk.Tk()
    root.title("InstallerPro")
    root.geometry("480x400")
    root.resizable(False, False)

    # ---- barra de menú --------------------------------------------------
    menubar = tk.Menu(root)
    lang_menu = tk.Menu(menubar, tearoff=0)
    lang_menu.add_command(
        label=LANG["es"]["menu_es"], command=lambda: set_language("es")
    )
    lang_menu.add_command(
        label=LANG["en"]["menu_en"], command=lambda: set_language("en")
    )
    menubar.add_cascade(label=LANG["es"]["menu_lang"], menu=lang_menu)

    theme_menu = tk.Menu(menubar, tearoff=0)
    for lbl in ("System", "Light", "Dark"):
        theme_menu.add_command(label=lbl, command=lambda v=lbl: apply_theme(v))
    menubar.add_cascade(label="Tema", menu=theme_menu)
    root.config(menu=menubar)

    # ---- widgets principales -------------------------------------------
    title_lbl = tk.Label(root, text=TXT["title"], font=("Segoe UI", 14, "bold"))
    title_lbl.pack(pady=12)

    frame = tk.Frame(root)
    frame.pack()

    scroll = tk.Scrollbar(frame, orient="vertical")
    listbox = tk.Listbox(
        frame, selectmode=tk.EXTENDED, width=42, height=8, yscrollcommand=scroll.set
    )
    scroll.config(command=listbox.yview)
    scroll.pack(side="right", fill="y")
    listbox.pack(side="left")

    add_btn = tk.Button(root, text=TXT["add"], width=22, command=add_project)
    rem_btn = tk.Button(root, text=TXT["remove"], width=22, command=remove_project)
    upd_btn = tk.Button(root, text=TXT["update"], width=22, command=update_selected)
    exit_btn = tk.Button(root, text=TXT["exit"], width=22, command=root.destroy)

    for btn in (add_btn, rem_btn, upd_btn, exit_btn):
        btn.pack(pady=4)
    upd_btn.pack_configure(pady=6)  # deje un poco más de aire

    progress = ttk.Progressbar(root, length=260, mode="determinate")
    progress.pack(pady=(2, 4))

    # ---- puesta en marcha ----------------------------------------------
    refresh_list()
    apply_theme(CURRENT_THEME)
    if CURRENT_THEME == "System":
        _watch_system_theme()

    root.mainloop()


def main() -> None:  # lo usará el “script” installerpro
    run_gui()


if __name__ == "__main__":  # ejecución directa: `python -m installerpro.ui.gui`
    run_gui()
