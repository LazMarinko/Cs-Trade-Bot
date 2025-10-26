import customtkinter as ctk


def build_user_input(parent: ctk.CTkFrame, on_launch) -> ctk.CTkEntry:
    user_input_frame = ctk.CTkFrame(parent, corner_radius=12)
    user_input_frame.pack(expand=True, fill="both", padx=6, pady=6)

    user_input_heading = ctk.CTkLabel(
        user_input_frame,
        text="Step 3 · Inputting the required information",
        font=("Segoe UI", 20, "bold"),
        anchor="w",
    )
    user_input_heading.pack(fill="x", padx=20, pady=(16, 8))

    input_container = ctk.CTkFrame(user_input_frame, corner_radius=8)
    input_container.pack(fill="x", padx=20, pady=(0, 12))

    inner_frame = ctk.CTkFrame(input_container, fg_color="transparent")
    inner_frame.pack(fill="x", padx=16, pady=16)

    steam_label = ctk.CTkLabel(
        inner_frame,
        text="Steam Inventory Link:",
        font=("Segoe UI", 14, "bold"),
        anchor="w",
    )
    steam_label.pack(fill="x", pady=(0, 4))

    steam_entry = ctk.CTkEntry(
        inner_frame,
        placeholder_text="https://steamcommunity.com/id/yourname/inventory",
        height=32,
        font=("Segoe UI", 13),
    )
    steam_entry.pack(fill="x", pady=(0, 10))

    webhook_label = ctk.CTkLabel(
        inner_frame,
        text="Discord Webhook URL:",
        font=("Segoe UI", 14, "bold"),
        anchor="w",
    )
    webhook_label.pack(fill="x", pady=(0, 4))

    webhook_entry = ctk.CTkEntry(
        inner_frame,
        placeholder_text="https://discord.com/api/webhooks/...",
        height=32,
        font=("Segoe UI", 13),
    )
    webhook_entry.pack(fill="x")

    button_frame = ctk.CTkFrame(user_input_frame, fg_color="transparent")
    button_frame.pack(fill="x", pady=(8, 16), padx=20)

    save_button = ctk.CTkButton(
        button_frame,
        text="Save Information",
        width=160,
        height=36,
        font=("Segoe UI", 14, "bold"),
        corner_radius=6,
        command=on_launch,
    )
    save_button.pack(anchor="e")

    return steam_entry, webhook_entry
