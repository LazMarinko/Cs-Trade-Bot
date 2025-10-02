"""Installation wizard UI for CS Trade Bot."""

import customtkinter as ctk


class InstallWizard(ctk.CTk):
    """First page of the installation wizard with bot information."""

    WINDOW_WIDTH = 780
    WINDOW_HEIGHT = 560

    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("CS Trade Bot • Setup")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.resizable(False, False)

        self._build_layout()

    def _build_layout(self) -> None:
        """Create the static content shown on the first page of the wizard."""

        outer_frame = ctk.CTkFrame(self, corner_radius=16)
        outer_frame.pack(expand=True, fill="both", padx=24, pady=24)

        header_frame = ctk.CTkFrame(outer_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=18, pady=(18, 12))

        title_label = ctk.CTkLabel(
            header_frame,
            text="Information about the installation",
            font=("Segoe UI", 26, "bold"),
            anchor="w",
        )
        title_label.pack(fill="x")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=(
                "Here is some useful information about the installation. "
                "Make sure you follow the installation guide to ensure that the bot functions properly."
            ),
            font=("Segoe UI", 15),
            wraplength=self.WINDOW_WIDTH - 120,
            justify="left",
        )
        subtitle_label.pack(fill="x", pady=(12, 0))

        info_frame = ctk.CTkScrollableFrame(outer_frame, corner_radius=12)
        info_frame.pack(expand=True, fill="both", padx=18, pady=12)

        sections = (
            (
                "What the bot does",
                (
                    "The bot will load your inventory, allowing you to select up to 10 of your most expensive skins. "
                    "You can then choose an item from your inventory that you want to trade. "
                    "The bot will search for trades that meet your desired profit percentage."
                ),
            ),
            (
                "What you'll need to do for the installation",
                (
                    "You will need to have Google Chrome installed on your device and a Counter-Strike inventory to trade with. "
                    "You must also follow the installation instructions and create a Discord webhook. "
                    "In addition, you need to install the CS2 Trader extension for Chrome. "
                    "All of these steps will be explained in the YouTube video below."
                ),
            ),
            (
                "Safety and responsibility",
                (
                    "The bot does not violate the Steam Community Terms of Service. "
                    "It only helps you find potentially profitable trades — it does not determine whether items are liquid or valuable. "
                    "Only accept and send the trades that you personally feel are worth it."
                ),
            )
        )


        for heading, body in sections:
            section_frame = ctk.CTkFrame(info_frame, corner_radius=10)
            section_frame.pack(fill="x", expand=False, padx=6, pady=(0, 12))

            heading_label = ctk.CTkLabel(
                section_frame,
                text=heading,
                font=("Segoe UI", 18, "bold"),
                anchor="w",
            )
            heading_label.pack(fill="x", padx=16, pady=(16, 8))

            body_label = ctk.CTkLabel(
                section_frame,
                text=body,
                font=("Segoe UI", 14),
                justify="left",
                wraplength=self.WINDOW_WIDTH - 140,
                anchor="w",
            )
            body_label.pack(fill="x", padx=16, pady=(0, 16))

        footer_frame = ctk.CTkFrame(outer_frame, fg_color="transparent")
        footer_frame.pack(fill="x", padx=18, pady=(0, 18))

        continue_button = ctk.CTkButton(
            footer_frame,
            text="Begin setup",
            command=self._handle_continue,
            height=42,
            font=("Segoe UI", 16, "bold"),
        )
        continue_button.pack(side="right")

        self.status_label = ctk.CTkLabel(
            footer_frame,
            text="Step 1 of 1 · Review the information above before continuing.",
            font=("Segoe UI", 13),
            anchor="w",
        )
        self.status_label.pack(side="left")

    def _handle_continue(self) -> None:
        """Placeholder handler until subsequent setup pages are implemented."""

        self.status_label.configure(text="Coming soon: additional setup steps.")


if __name__ == "__main__":
    InstallWizard().mainloop()