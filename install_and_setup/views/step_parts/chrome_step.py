import customtkinter as ctk


def build_chrome(parent: ctk.CTkFrame, wrap_width: int, on_launch) -> ctk.CTkButton:
    """
    Builds the Chrome step UI and returns the 'Launch Chrome' button widget.
    The caller (InstallView) keeps a reference to enable/disable it later.
    """
    chrome_frame = ctk.CTkFrame(parent, corner_radius=12)
    chrome_frame.pack(expand=True, fill="both", padx=6, pady=6)

    heading_label = ctk.CTkLabel(
        chrome_frame,
        text="Step 2 · Prepare Google Chrome",
        font=("Segoe UI", 22, "bold"),
        anchor="w",
    )
    heading_label.pack(fill="x", padx=24, pady=(24, 12))

    body_text = (
        "Here’s what you need to do to set up Chrome for use with this bot. "
        "First, log in to your Steam profile — the button below will take you directly to the Steam login page. "
        "After logging in, make sure to install the CS2 Trader extension "
        "and set it up as explained in the installation video guide."
    )

    body_label = ctk.CTkLabel(
        chrome_frame,
        text=body_text,
        font=("Segoe UI", 15),
        justify="left",
        wraplength=wrap_width,
    )
    body_label.pack(fill="x", padx=24)

    start_chrome_button = ctk.CTkButton(
        chrome_frame,
        text="Launch Chrome",
        height=42,
        font=("Segoe UI", 16, "bold"),
        command=on_launch,
    )
    start_chrome_button.pack(padx=24, pady=(32, 12), anchor="w")

    return start_chrome_button
