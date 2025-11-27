import customtkinter as ctk


class TradeSettingsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        self.min_profit_values = [f"{i}%" for i in range(2, 16)]
        self.max_profit_values = [f"{i}%" for i in range(5, 26)]
        self.min_value_values = [f"{i}%" for i in range(50, 91, 10)]

        # Min Profit
        self.min_profit_label = ctk.CTkLabel(self, text="Min Profit:")
        self.min_profit_label.grid(row=0, column=0, sticky="w", pady=(0, 2))

        self.min_profit_var = ctk.StringVar()
        self.min_profit_combo = ctk.CTkComboBox(
            self, values=self.min_profit_values, variable=self.min_profit_var,
            state="readonly", width=140
        )
        self.min_profit_combo.grid(row=1, column=0, sticky="w", pady=(0, 8))

        # Max Profit
        self.max_profit_label = ctk.CTkLabel(self, text="Max Profit:")
        self.max_profit_label.grid(row=2, column=0, sticky="w", pady=(0, 2))

        self.max_profit_var = ctk.StringVar()
        self.max_profit_combo = ctk.CTkComboBox(
            self, values=self.max_profit_values, variable=self.max_profit_var,
            state="readonly", width=140
        )
        self.max_profit_combo.grid(row=3, column=0, sticky="w", pady=(0, 8))

        # Min Value
        self.min_value_label = ctk.CTkLabel(self, text="Min Value:")
        self.min_value_label.grid(row=4, column=0, sticky="w", pady=(0, 2))

        self.min_value_var = ctk.StringVar()
        self.min_value_combo = ctk.CTkComboBox(
            self, values=self.min_value_values, variable=self.min_value_var,
            state="readonly", width=140
        )
        self.min_value_combo.grid(row=5, column=0, sticky="w", pady=(0, 8))

    # ----- load from JSON values -----
    def load_values(self, min_profit_mult: float, max_profit_mult: float, min_value_ratio: float):
        # multipliers like 1.04 → 4%
        min_profit_percent = int(round((float(min_profit_mult) - 1.0) * 100))
        max_profit_percent = int(round((float(max_profit_mult) - 1.0) * 100))
        # ratio like 0.6 → 60%
        min_value_percent = int(round(float(min_value_ratio) * 100))

        self._set_percent(self.min_profit_combo, self.min_profit_values, min_profit_percent)
        self._set_percent(self.max_profit_combo, self.max_profit_values, max_profit_percent)
        self._set_percent(self.min_value_combo, self.min_value_values, min_value_percent)

    def _set_percent(self, combo: ctk.CTkComboBox, allowed_values: list[str], percent: int):
        target = f"{percent}%"
        if target not in allowed_values:
            target = allowed_values[0]
        combo.set(target)

    # ----- getters for saving -----
    def _parse_percent(self, value: str) -> float:
        if value.endswith("%"):
            value = value[:-1]
        try:
            return float(value)
        except ValueError:
            return 0.0

    def get_min_profit_multiplier(self) -> float:
        p = self._parse_percent(self.min_profit_var.get())
        return 1.0 + p / 100.0

    def get_max_profit_multiplier(self) -> float:
        p = self._parse_percent(self.max_profit_var.get())
        return 1.0 + p / 100.0

    def get_min_target_item_ratio(self) -> float:
        p = self._parse_percent(self.min_value_var.get())
        return p / 100.0
