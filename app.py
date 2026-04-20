import customtkinter as ctk
import json
import os
from pathlib import Path
from datetime import datetime
import threading
import session

# ─── Constants ────────────────────────────────────────────────────────────────
DATA_FOLDER  = os.path.join(os.path.expanduser("~"), "Work Software")
DATA_FILE    = os.path.join(DATA_FOLDER, "employee_data.json")
LOG_FOLDER   = Path(DATA_FOLDER) / "Signing" / "logs"
LOG_FILE     = LOG_FOLDER / "employee_logs.txt"

# ─── Backend Logic (mirrors your four files) ─────────────────────────────────

def sign_in(employee_name: str, password: str) -> tuple[bool, str]:
    """Register a new employee (SignIn.py logic)."""
    if not employee_name or not password:
        return False, "Fields cannot be empty."

    os.makedirs(DATA_FOLDER, exist_ok=True)

    data_list = _read_data()

    for emp in data_list:
        if emp["employee_name"] == employee_name:
            return False, "Employee already registered."

    data_list.append({"employee_name": employee_name, "password": password})

    with open(DATA_FILE, "w") as f:
        json.dump(data_list, f, indent=4)

    return True, f'"{employee_name}" registered successfully.'


def check_credentials(employee_name: str, password: str) -> tuple[bool, str]:
    """Verify credentials (Checking.py logic)."""
    if not os.path.exists(DATA_FILE):
        return False, "No employee data found. Please register first."

    data_list = _read_data()
    if data_list is None:
        return False, "Employee data is corrupted."

    for emp in data_list:
        if emp["employee_name"] == employee_name and emp["password"] == password:
            return True, "Credentials verified."

    return False, "Invalid credentials. Access denied."


def log_login(employee_name: str, password: str) -> tuple[bool, str]:
    """Check credentials then write a log entry (logs.py logic)."""
    ok, msg = check_credentials(employee_name, password)
    if not ok:
        return False, msg

    LOG_FOLDER.mkdir(parents=True, exist_ok=True)
    timestamp  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry  = f"[{timestamp}] Employee: {employee_name} - Logged In\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    return True, f"Welcome back, {employee_name}!"


def _read_data() -> list | None:
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def get_recent_logs(n: int = 6) -> list[str]:
    if not LOG_FILE.exists():
        return []
    with open(LOG_FILE, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    return lines[-n:]


# ─── UI ───────────────────────────────────────────────────────────────────────

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DARK_BG  = "#0d0f14"
PANEL_BG = "#141720"
CARD_BG  = "#1a1f2e"
BORDER   = "#252c3d"
ACCENT   = "#4f8ef7"
ACCENT2  = "#7b5ef8"
SUCCESS  = "#22c55e"
ERROR    = "#ef4444"
TEXT_MAIN = "#e8eaf0"
TEXT_SUB  = "#6b7280"

# ── Dynamic font scaling ──────────────────────────────────────────────────────
BASE_W = 860
BASE_H = 560
_S     = 1.0   # global scale factor, updated on resize

def _sz(base: int) -> int:
    return max(6, round(base * _S))

def F_HEAD():  return ("Segoe UI", _sz(24), "bold")
def F_LABEL(): return ("Segoe UI", _sz(13))
def F_SMALL(): return ("Segoe UI", _sz(11))
def F_ENTRY(): return ("Segoe UI", _sz(14))
def F_BTN():   return ("Segoe UI", _sz(13), "bold")
def F_LOG():   return ("Consolas",  _sz(11))
def F_BRAND(): return ("Segoe UI", _sz(15), "bold")
def F_ICON():  return ("Segoe UI", _sz(30))


class WorkApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Work Software — Employee Portal")
        self.geometry("1980x1080")
        self.minsize(600, 400)
        self.configure(fg_color=DARK_BG)
        self.resizable(True, True)

        self._current_screen = "login"
        self._resize_job     = None
        self.bind("<Configure>", self._on_resize)

        self._build_layout()
        self._show_login()

    def _on_resize(self, event):
        if event.widget is not self:
            return
        if self._resize_job:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(
            120, lambda: self._apply_scale(event.width, event.height))

    def _apply_scale(self, w: int, h: int):
        global _S
        _S = max(0.55, min(min(w / BASE_W, h / BASE_H), 2.4))
        self._redraw_current()

    def _redraw_current(self):
        self._refresh_sidebar_fonts()
        {"login":     self._show_login,
         "register":  self._show_register,
         "logs":      self._show_logs,
         "dashboard": self._show_dashboard,
         }.get(self._current_screen, self._show_login)()

    # ── Layout skeleton ───────────────────────────────────────────────────────

    def _build_layout(self):
        # Left sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color=PANEL_BG,
                                    corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand
        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=80)
        brand.pack(fill="x", padx=20, pady=(28, 0))
        self._lbl_brand_icon = ctk.CTkLabel(
            brand, text="⬡", font=F_ICON(), text_color=ACCENT)
        self._lbl_brand_icon.pack(anchor="w")
        self._lbl_brand_name = ctk.CTkLabel(
            brand, text="WorkPortal", font=F_BRAND(), text_color=TEXT_MAIN)
        self._lbl_brand_name.pack(anchor="w")

        ctk.CTkFrame(self.sidebar, height=1, fg_color=BORDER).pack(
            fill="x", padx=20, pady=18)

        # Nav buttons
        self._nav_btns: dict[str, ctk.CTkButton] = {}
        nav_items = [
            ("🔐  Login",      self._show_login),
            ("📋  Register",   self._show_register),
            ("📜  Logs",       self._show_logs),
            ("🏠  Dashboard",  self._show_dashboard),
        ]
        for label, cmd in nav_items:
            btn = ctk.CTkButton(
                self.sidebar, text=label, anchor="w",
                font=F_LABEL(), height=40,
                fg_color="transparent", hover_color=BORDER,
                text_color=TEXT_SUB, corner_radius=8,
                command=cmd,
            )
            btn.pack(fill="x", padx=12, pady=3)
            self._nav_btns[label] = btn

        # Version at bottom
        self._lbl_version = ctk.CTkLabel(
            self.sidebar, text="v1.0.0", font=F_SMALL(), text_color=TEXT_SUB)
        self._lbl_version.pack(side="bottom", pady=16)

        # Main content area
        self.main = ctk.CTkFrame(self, fg_color=DARK_BG, corner_radius=0)
        self.main.pack(side="right", fill="both", expand=True)

    def _refresh_sidebar_fonts(self):
        """Update sidebar fonts after a scale change without rebuilding it."""
        self._lbl_brand_icon.configure(font=F_ICON())
        self._lbl_brand_name.configure(font=F_BRAND())
        self._lbl_version.configure(font=F_SMALL())
        active = next(
            (l for l, b in self._nav_btns.items()
             if b.cget("fg_color") == BORDER), None)
        for label, btn in self._nav_btns.items():
            btn.configure(font=F_LABEL())

    def _clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()

    def _set_nav_active(self, active_label: str):
        for label, btn in self._nav_btns.items():
            if label == active_label:
                btn.configure(text_color=ACCENT, fg_color=BORDER)
            else:
                btn.configure(text_color=TEXT_SUB, fg_color="transparent")

    # ── Reusable widgets ──────────────────────────────────────────────────────

    def _make_card(self, parent, title: str, subtitle: str = ""):
        card = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=16,
                            border_width=1, border_color=BORDER)
        card.pack(expand=True)
        ctk.CTkLabel(card, text=title, font=F_HEAD(),
                     text_color=TEXT_MAIN).pack(anchor="w", padx=36, pady=(36, 2))
        if subtitle:
            ctk.CTkLabel(card, text=subtitle, font=F_LABEL(),
                         text_color=TEXT_SUB).pack(anchor="w", padx=36, pady=(0, 22))
        return card

    def _field(self, parent, label: str, placeholder: str,
                show: str = "") -> ctk.CTkEntry:
        ctk.CTkLabel(parent, text=label, font=F_LABEL(),
                     text_color=TEXT_SUB).pack(anchor="w", padx=36)
        entry = ctk.CTkEntry(
            parent, placeholder_text=placeholder,
            font=F_ENTRY(), height=_sz(44), corner_radius=10,
            fg_color="#0f1219", border_color=BORDER, border_width=1,
            text_color=TEXT_MAIN, placeholder_text_color="#4b5563",
            show=show,
        )
        entry.pack(fill="x", padx=36, pady=(4, 16))
        return entry

    def _status_label(self, parent) -> ctk.CTkLabel:
        lbl = ctk.CTkLabel(parent, text="", font=F_LABEL(), text_color=TEXT_SUB)
        lbl.pack(padx=36, pady=(0, 4))
        return lbl

    def _show_status(self, lbl: ctk.CTkLabel, msg: str, ok: bool):
        lbl.configure(text=msg, text_color=SUCCESS if ok else ERROR)
        self.after(4000, lambda: lbl.configure(text=""))

    def _accent_btn(self, parent, text: str, cmd) -> ctk.CTkButton:
        return ctk.CTkButton(
            parent, text=text, font=F_BTN(), height=_sz(46),
            corner_radius=10, fg_color=ACCENT, hover_color="#3a74e0",
            text_color="white", command=cmd,
        )

    # ── Login screen ──────────────────────────────────────────────────────────

    def _show_login(self):
        self._current_screen = "login"
        self._clear_main()
        self._set_nav_active("🔐  Login")

        card = self._make_card(self.main,
                               "Employee Login",
                               "Enter your credentials to access the system.")

        self._login_name = self._field(card, "EMPLOYEE NAME", "e.g. john.doe")
        self._login_pass = self._field(card, "PASSWORD", "••••••••", show="•")

        self._login_status = self._status_label(card)

        self._accent_btn(card, "Sign In →", self._do_login).pack(
            fill="x", padx=36, pady=(6, 36))

    def _do_login(self):
        name = self._login_name.get().strip()
        pw   = self._login_pass.get().strip()
        ok, msg = log_login(name, pw)
        if ok:
            session.login(name)
            self._login_pass.delete(0, "end")
            self.after(300, self._show_dashboard)
        else:
            self._show_status(self._login_status, msg, ok)

    # ── Register screen ───────────────────────────────────────────────────────

    def _show_register(self):
        self._current_screen = "register"
        self._clear_main()
        self._set_nav_active("📋  Register")

        card = self._make_card(self.main,
                               "Register Employee",
                               "Create a new employee account.")

        self._reg_name = self._field(card, "EMPLOYEE NAME", "e.g. jane.smith")
        self._reg_pass = self._field(card, "PASSWORD", "Choose a password", show="•")
        self._reg_pass2= self._field(card, "CONFIRM PASSWORD", "Repeat password", show="•")

        self._reg_status = self._status_label(card)

        self._accent_btn(card, "Create Account", self._do_register).pack(
            fill="x", padx=36, pady=(6, 36))

    def _do_register(self):
        name = self._reg_name.get().strip()
        pw   = self._reg_pass.get().strip()
        pw2  = self._reg_pass2.get().strip()

        if pw != pw2:
            self._show_status(self._reg_status, "Passwords do not match.", False)
            return

        ok, msg = sign_in(name, pw)
        self._show_status(self._reg_status, msg, ok)
        if ok:
            self._reg_name.delete(0, "end")
            self._reg_pass.delete(0, "end")
            self._reg_pass2.delete(0, "end")

    # ── Logs screen ───────────────────────────────────────────────────────────

    def _show_logs(self):
        self._current_screen = "logs"
        self._clear_main()
        self._set_nav_active("📜  Logs")

        hdr = ctk.CTkFrame(self.main, fg_color="transparent")
        hdr.pack(fill="x", padx=36, pady=(36, 0))
        ctk.CTkLabel(hdr, text="Activity Logs", font=F_HEAD(),
                     text_color=TEXT_MAIN).pack(side="left")
        ctk.CTkButton(hdr, text="↻ Refresh", font=F_SMALL(), height=_sz(30),
                      width=_sz(90), corner_radius=8,
                      fg_color=BORDER, hover_color="#2a3147",
                      text_color=TEXT_MAIN,
                      command=self._show_logs).pack(side="right")

        ctk.CTkLabel(self.main, text="Recent login activity",
                     font=F_LABEL(), text_color=TEXT_SUB).pack(
                         anchor="w", padx=36, pady=(4, 18))

        scroll = ctk.CTkScrollableFrame(
            self.main, fg_color=CARD_BG, corner_radius=14,
            border_width=1, border_color=BORDER,
        )
        scroll.pack(fill="both", expand=True, padx=36, pady=(0, 36))

        entries = get_recent_logs(n=50)
        if not entries:
            ctk.CTkLabel(scroll, text="No logs recorded yet.",
                         font=F_LABEL(), text_color=TEXT_SUB).pack(pady=40)
        else:
            for line in reversed(entries):
                row = ctk.CTkFrame(scroll, fg_color="#1f2436", corner_radius=8)
                row.pack(fill="x", padx=12, pady=4)
                ctk.CTkLabel(row, text="●", font=F_SMALL(),
                             text_color=SUCCESS).pack(side="left", padx=(12, 6), pady=12)
                ctk.CTkLabel(row, text=line, font=F_LOG(),
                             text_color=TEXT_MAIN, anchor="w").pack(side="left", pady=12)


    def _show_dashboard(self):
        self._current_screen = "dashboard"
        self._clear_main()
        self._set_nav_active("🏠  Dashboard")

        if not session.is_logged_in():
            guard = ctk.CTkFrame(self.main, fg_color="transparent")
            guard.pack(expand=True)
            ctk.CTkLabel(guard, text="🔒", font=("Segoe UI", _sz(44)),
                         text_color=TEXT_SUB).pack()
            ctk.CTkLabel(guard, text="Access Restricted",
                         font=("Segoe UI", _sz(18), "bold"), text_color=TEXT_MAIN).pack(pady=(10, 6))
            ctk.CTkLabel(guard,
                         text="You need to sign in first to view the dashboard.",
                         font=F_LABEL(), text_color=TEXT_SUB).pack()
            ctk.CTkButton(
                guard, text="Go to Login →", font=F_BTN(), height=_sz(42),
                width=_sz(180), corner_radius=10,
                fg_color=ACCENT, hover_color="#3a74e0", text_color="white",
                command=self._show_login,
            ).pack(pady=(22, 0))
            return

        top = ctk.CTkFrame(self.main, fg_color="transparent")
        top.pack(fill="x", padx=36, pady=(36, 0))

        name_display = session.current_user()
        ctk.CTkLabel(top, text=f"Welcome back, {name_display} 👋",
                     font=F_HEAD(), text_color=TEXT_MAIN).pack(side="left")

        ctk.CTkButton(
            top, text="⏻  Log Out", font=F_SMALL(), height=_sz(32), width=_sz(100),
            corner_radius=8, fg_color="#2a1f1f", hover_color="#3d2222",
            text_color="#f87171", border_width=1, border_color="#5c2626",
            command=self._do_logout,
        ).pack(side="right")

        ctk.CTkLabel(self.main,
                     text=f"Logged in · {datetime.now().strftime('%A, %B %d %Y  %H:%M')}",
                     font=F_SMALL(), text_color=TEXT_SUB).pack(
                         anchor="w", padx=36, pady=(6, 28))

        ctk.CTkFrame(self.main, height=1, fg_color=BORDER).pack(
            fill="x", padx=36, pady=(0, 28))

        workspace = ctk.CTkFrame(
            self.main, fg_color=CARD_BG, corner_radius=16,
            border_width=1, border_color=BORDER,
        )
        workspace.pack(fill="both", expand=True, padx=36, pady=(0, 36))

        ph = ctk.CTkFrame(workspace, fg_color="transparent")
        ph.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(ph, text="⬡", font=("Segoe UI", _sz(48)),
                     text_color=BORDER).pack()
        ctk.CTkLabel(ph, text="Your workspace",
                     font=("Segoe UI", _sz(16), "bold"), text_color=TEXT_SUB).pack(pady=(8, 4))
        ctk.CTkLabel(ph, text="This area is ready for your content.",
                     font=F_LABEL(), text_color="#374151").pack()

    def _do_logout(self):
        session.logout()
        self._show_login()

# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = WorkApp()
    app.mainloop()