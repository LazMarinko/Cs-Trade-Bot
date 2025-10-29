import customtkinter as ctk
import tkinter.messagebox as messagebox
from typing import Callable, Optional
from install_and_setup.config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from install_and_setup.views.step_parts.welcome_step import build_welcome
from install_and_setup.views.step_parts.chrome_step import build_chrome
from install_and_setup.views.step_parts.user_input_step import build_user_input
from install_and_setup.views.step_parts.trade_settings_step import build_trade_settings_step


class InstallView(ctk.CTk):
    """
    Pure UI. Exposes callbacks; no business logic.
    Controller calls `render_step(index)` to switch screens.
    """

    # Controller-provided callbacks
    on_continue: Optional[Callable[[], None]] = None
    on_launch_chrome: Optional[Callable[[], None]] = None
    on_save_info: Optional[Callable[[str, str], None]] = None
    on_final_save: Optional[Callable[[float, float, float], None]] = None

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        self.start_chrome_button = None  # used to enable/disable
        self.steam_entry = None
        self.webhook_entry = None

        self.min_profit = None
        self.max_profit = None
        self.min_value = None
        self.save_button = None

        self.build_shell()

    # ----- Shell (static chrome) -----
    def build_shell(self):
        self.outer_frame = ctk.CTkFrame(self, corner_radius=16)
        self.outer_frame.pack(expand=True, fill="both", padx=24, pady=24)

        self.header_frame = ctk.CTkFrame(self.outer_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=18, pady=(18, 12))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Welcome to the CS Trade Bot Installer",
            font=("Segoe UI", 26, "bold"),
            anchor="w",
        )
        self.title_label.pack(fill="x")

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text=(
                "This guided setup will prepare the automation bot that helps you browse "
                "Counter-Strike 2 trade offers and pre-fills the offer window with your "
                "selected inventory item."
            ),
            font=("Segoe UI", 15),
            wraplength=WINDOW_WIDTH - 120,
            justify="left",
        )
        self.subtitle_label.pack(fill="x", pady=(12, 0))

        self.step_container = ctk.CTkFrame(self.outer_frame, corner_radius=12)
        self.step_container.pack(expand=True, fill="both", padx=18, pady=12)
        self.step_container.pack_propagate(False)

        footer_frame = ctk.CTkFrame(self.outer_frame, fg_color="transparent")
        footer_frame.pack(fill="x", padx=18, pady=(0, 18))

        self.continue_button = ctk.CTkButton(
            footer_frame,
            text="Begin setup",
            command=self.continue_clicked,
            height=42,
            font=("Segoe UI", 16, "bold"),
        )
        self.continue_button.pack(side="right")

        self.status_label = ctk.CTkLabel(
            footer_frame,
            text="Step 1 of 4 · Review the information above before continuing.",
            font=("Segoe UI", 13),
            anchor="w",
        )
        self.status_label.pack(side="left")

    # ----- Public helpers for Controller -----
    def set_status(self, text: str):
        self.status_label.configure(text=text)

    def set_continue_text(self, text: str):
        self.continue_button.configure(text=text)

    def set_chrome_button_enabled(self, enabled: bool):
        if self.start_chrome_button is None:
            return
        self.start_chrome_button.configure(state="normal" if enabled else "disabled")

    def fill_user_inputs(self, steam_link: str, webhook_url: str):
        if self.steam_entry is not None:
            self.steam_entry.delete(0, "end")
            self.steam_entry.insert(0, steam_link or "")
        if self.webhook_entry is not None:
            self.webhook_entry.delete(0, "end")
            self.webhook_entry.insert(0, webhook_url or "")

    def get_user_inputs(self) -> tuple[str, str]:
        steam = self.steam_entry.get().strip() if self.steam_entry else ""
        hook = self.webhook_entry.get().strip() if self.webhook_entry else ""
        return steam, hook

    def get_trade_settings(self) -> tuple[float, float, float]:
        """
        Returns (min_profit_multiplier, max_profit_multiplier, min_value_ratio).
        Accepts user selections like "8%", "1.08" for profits -> 1.08,
        and "60%", "0.6" for min value -> 0.6.
        """

        def _as_str(x) -> str:
            return "" if x is None else str(x).strip()

        def _normalize_profit(x) -> float:
            s = _as_str(x).lower()
            if not s:
                return None
            if s.endswith("%"):
                # "8%" -> 1.08
                p = float(s[:-1])
                return 1.0 + (p / 100.0)
            # "1.08" or 1.08
            val = float(s)
            if val >= 1.0:
                return val
            # defensive: if someone typed "8" without '%', treat as 8%
            if 0.0 < val < 1.0:
                # ambiguous, but we’ll assume multiplier was intended
                return val
            return 1.0 + (val / 100.0)

        def _normalize_value_ratio(x) -> float:
            s = _as_str(x).lower()
            if not s:
                return None
            if s.endswith("%"):
                # "60%" -> 0.6
                p = float(s[:-1])
                return p / 100.0
            # "0.6" or 0.6
            val = float(s)
            if 0.0 < val <= 1.0:
                return val
            # "60" without '%' -> 0.6
            return val / 100.0

        raw_min_profit = self.min_profit.get() if self.min_profit else None
        raw_max_profit = self.max_profit.get() if self.max_profit else None
        raw_min_value = self.min_value.get() if self.min_value else None

        min_profit = _normalize_profit(raw_min_profit) or 1.02  # default to 2%
        max_profit = _normalize_profit(raw_max_profit) or 1.08  # default to 8%
        min_value = _normalize_value_ratio(raw_min_value) or 0.6  # default to 60%

        return min_profit, max_profit, min_value

    # ----- Steps -----
    def render_step(self, index: int):
        # clear
        for child in self.step_container.winfo_children():
            child.destroy()

        if index == 0:
            self.render_welcome()
            self.set_continue_text("Begin setup")
            self.set_status("Step 1 of 4 · Review the information above before continuing.")
        elif index == 1:
            self.render_chrome()
            self.set_continue_text("Next step")
            self.set_status("Step 2 of 4 · Setup Chrome browser for the bot.")
        elif index == 2:
            self.render_user_inputs()
            self.set_continue_text("Next step")
            self.set_status("Step 3 of 4 · Input the required information")
        elif index == 3:
            self.render_trade_setings()
            self.set_continue_text("Finish")
            self.set_status("Step 4 of 4 · Choose your trade settings")

    def render_welcome(self):
        build_welcome(self.step_container)

    def render_chrome(self):
        self.start_chrome_button = build_chrome(
            parent=self.step_container,
            wrap_width=WINDOW_WIDTH - 140,
            on_launch=self.launch_chrome_clicked,  # uses your existing callback
        )

    def render_user_inputs(self):
        # Build + capture: (steam_entry, webhook_entry, save_info_button)
        self.steam_entry, self.webhook_entry, self.save_info_button = build_user_input(
            parent=self.step_container,
            on_launch=self._user_inputs_save_clicked  # view-local handler
        )
        # Disable Next until a successful Save
        self.continue_button.configure(state="disabled")

    def render_trade_setings(self):
        # Build + capture: (min_profit_combo, max_profit_combo, min_value_combo, save_button)
        (self.min_profit, self.max_profit, self.min_value, self.save_button) = build_trade_settings_step(
            self.step_container,
            on_save=self._trade_settings_save_clicked  # view-local handler
        )
        # Disable Finish until final Save succeeds
        self.continue_button.configure(state="disabled")

    # ----- UI -> Controller triggers -----
    def continue_clicked(self):
        if self.on_continue:
            self.on_continue()

    def launch_chrome_clicked(self):
        if self.on_launch_chrome:
            self.on_launch_chrome()

    def _user_inputs_save_clicked(self):
        if not self.on_save_info:
            return
        steam, hook = self.get_user_inputs()

        def looks_like_url(s: str) -> bool:
            return isinstance(s, str) and s.strip().lower().startswith(("http://", "https://"))

        if not looks_like_url(steam) or not looks_like_url(hook):
            self.set_status("Please enter valid URLs for both fields, then press Save again.")
            return

        try:
            self.on_save_info(steam, hook)  # controller writes config
            if getattr(self, "save_info_button", None):
                self.save_info_button.configure(state="disabled", text="Saved")
            self.continue_button.configure(state="normal")  # ✅ allow Next
            self.set_status("✅ Information saved to config.json.")
        except Exception as e:
            self.set_status(f"Failed to save config: {e}")

    def _trade_settings_save_clicked(self):
        if not self.on_final_save:
            return

        # Pass raw selections (e.g., "8%", "60%") and let the controller/model normalize
        min_profit = self.min_profit.get() if self.min_profit else "2%"
        max_profit = self.max_profit.get() if self.max_profit else "8%"
        min_value = self.min_value.get() if self.min_value else "60%"

        try:
            # Controller does validation + saving (and conversion to multipliers/ratio)
            self.on_final_save(min_profit, max_profit, min_value)

            # Grey out Save, enable Finish
            if getattr(self, "save_button", None):
                self.save_button.configure(state="disabled", text="Saved")
            self.continue_button.configure(state="normal")  # ✅ allow Finish

            self.set_status("✅ Trade settings saved. Setup is done.")
        except Exception as e:
            self.set_status(f"Failed to save trade settings: {e}")

    # ----- Minor helpers the controller can reuse -----
    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)

    def show_warning(self, title: str, message: str):
        messagebox.showwarning(title, message)
