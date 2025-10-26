import customtkinter as ctk
from install_and_setup.config import WINDOW_WIDTH


def build_welcome(parent: ctk.CTkFrame) -> None:
    info_frame = ctk.CTkScrollableFrame(parent, corner_radius=12, fg_color="transparent")
    info_frame.pack(fill="both", expand=True)

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
            wraplength=WINDOW_WIDTH - 140,
            anchor="w",
        )
        body_label.pack(fill="x", padx=16, pady=(0, 16))
