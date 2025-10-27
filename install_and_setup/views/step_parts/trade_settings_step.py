import customtkinter as ctk
from install_and_setup.config import WINDOW_WIDTH, WINDOW_HEIGHT


def build_trade_settings_step(parent, on_save=None):
    """
    Fixed-size, grid-based layout so the Save button doesn't get clipped.
    Returns: (min_profit_combo, max_profit_combo, min_value_combo, save_button)
    """
    # ---- derive a stable inner size from config (with sensible minimums) ----
    frame_w = max(520, WINDOW_WIDTH - 2 * 72)  # keep some margins
    frame_h = max(320, int(WINDOW_HEIGHT * 0.45))  # tall enough for button

    # outer wrapper (centers inside step container)
    outer = ctk.CTkFrame(parent, fg_color="transparent")
    outer.pack(expand=True)

    # main frame with fixed size; we'll use GRID inside
    frame = ctk.CTkFrame(outer, corner_radius=12, width=frame_w, height=frame_h)
    frame.pack_propagate(False)  # enforce fixed size
    frame.pack(pady=12)

    # ---- grid setup ----
    # columns: labels left (0), widgets right (1)
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=0)
    # spacer row to push button down while preserving its height
    # rows we use: 0 title, 1 subtitle, 2 min label, 3 min combo, 2/3 share with max via separate container,
    # 4 value label, 5 value combo, 6 spacer, 7 button
    frame.grid_rowconfigure(6, weight=1)

    # ---- header ----
    title = ctk.CTkLabel(frame, text="Trade Settings", font=("Segoe UI", 22, "bold"))
    title.grid(row=0, column=0, columnspan=2, sticky="w", padx=18, pady=(14, 6))

    subtitle = ctk.CTkLabel(
        frame,
        text="Set the default trade parameters for the bot:",
        font=("Segoe UI", 14),
        justify="left",
    )
    subtitle.grid(row=1, column=0, columnspan=2, sticky="w", padx=18, pady=(0, 12))

    # ---- ranges ----
    min_profit_values = [f"{i}%" for i in range(2, 16)]  # 2–15
    max_profit_values = [f"{i}%" for i in range(5, 26)]  # 5–25
    min_value_values = [f"{i}%" for i in range(50, 91, 10)]  # 50–90 step 10

    # ---- profit row: two widgets side-by-side with their labels above ----
    # put them in a small inner frame to control spacing tightly
    profit_row = ctk.CTkFrame(frame, fg_color="transparent")
    profit_row.grid(row=2, column=0, columnspan=2, sticky="w", padx=18, pady=(0, 8))
    profit_row.grid_columnconfigure(0, weight=0)
    profit_row.grid_columnconfigure(1, weight=0)

    lbl_min = ctk.CTkLabel(profit_row, text="Minimum Profit %", font=("Segoe UI", 14))
    lbl_min.grid(row=0, column=0, sticky="w", padx=(0, 10))
    lbl_max = ctk.CTkLabel(profit_row, text="Maximum Profit %", font=("Segoe UI", 14))
    lbl_max.grid(row=0, column=1, sticky="w", padx=(10, 0))

    min_profit = ctk.CTkComboBox(profit_row, values=min_profit_values, width=120, state="readonly")
    min_profit.set("2%")
    min_profit.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(2, 0))

    max_profit = ctk.CTkComboBox(profit_row, values=max_profit_values, width=120, state="readonly")
    max_profit.set("8%")
    max_profit.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(2, 0))

    # ---- minimum item value row ----
    value_label = ctk.CTkLabel(frame, text="Minimum Item Value % of Base Item", font=("Segoe UI", 14))
    value_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=18, pady=(8, 0))

    min_value = ctk.CTkComboBox(frame, values=min_value_values, width=150, state="readonly")
    min_value.set("60%")
    min_value.grid(row=5, column=0, sticky="w", padx=18, pady=(4, 0))

    # ---- spacer (row 6) pushes the button down but DOESN'T shrink it ----
    spacer = ctk.CTkLabel(frame, text="")
    spacer.grid(row=6, column=0, columnspan=2, sticky="nsew")

    # ---- save button ----
    save_button = ctk.CTkButton(
        frame,
        text="Save Settings",
        font=("Segoe UI", 15, "bold"),
        width=160,
        height=36,
        command=on_save,  # wire later
    )
    save_button.grid(row=7, column=0, columnspan=2, pady=(8, 12))

    return min_profit, max_profit, min_value, save_button
