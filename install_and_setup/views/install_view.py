import customtkinter as ctk
import tkinter.messagebox as messagebox
from typing import Callable, Optional
from install_and_setup.config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from install_and_setup.views.step_parts.welcome_step import build_welcome
from install_and_setup.views.step_parts.chrome_step import build_chrome
from install_and_setup.views.step_parts.user_input_step import build_user_input


class InstallView(ctk.CTk):
    """
    Pure UI. Exposes callbacks; no business logic.
    Controller calls `render_step(index)` to switch screens.
    """

    # Controller-provided callbacks
    on_continue: Optional[Callable[[], None]] = None
    on_launch_chrome: Optional[Callable[[], None]] = None
    on_save_info: Optional[Callable[[str, str], None]] = None

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        self._start_chrome_button = None  # used to enable/disable
        self._steam_entry = None
        self._webhook_entry = None

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
        if self._start_chrome_button is None:
            return
        self._start_chrome_button.configure(state="normal" if enabled else "disabled")

    def fill_user_inputs(self, steam_link: str, webhook_url: str):
        if self._steam_entry is not None:
            self._steam_entry.delete(0, "end")
            self._steam_entry.insert(0, steam_link or "")
        if self._webhook_entry is not None:
            self._webhook_entry.delete(0, "end")
            self._webhook_entry.insert(0, webhook_url or "")

    def get_user_inputs(self) -> tuple[str, str]:
        steam = self._steam_entry.get().strip() if self._steam_entry else ""
        hook = self._webhook_entry.get().strip() if self._webhook_entry else ""
        return steam, hook

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

    def render_welcome(self):
        build_welcome(self.step_container)

    def render_chrome(self):
        self._start_chrome_button = build_chrome(
            parent=self.step_container,
            wrap_width=WINDOW_WIDTH - 140,
            on_launch=self.launch_chrome_clicked,  # uses your existing callback
        )

    def render_user_inputs(self):
        self.steam_entry, self._webhook_entry = build_user_input(parent=self.step_container,
                                                                 on_launch=self.save_clicked())

    # ----- UI -> Controller triggers -----
    def continue_clicked(self):
        if self.on_continue:
            self.on_continue()

    def launch_chrome_clicked(self):
        if self.on_launch_chrome:
            self.on_launch_chrome()

    def save_clicked(self):
        if not self.on_save_info:
            return
        steam, hook = self.get_user_inputs()

        # lightweight input check mirroring original behavior
        if not steam or not hook or not steam.startswith("http") or not hook.startswith("http"):
            self.set_status("Please enter valid URLs for both fields.")
            return

        self.on_save_info(steam, hook)

    # ----- Minor helpers the controller can reuse -----
    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)

    def show_warning(self, title: str, message: str):
        messagebox.showwarning(title, message)
