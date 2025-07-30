"""
Maintains the prices in a flat-file in Ledger format.
P 2023-04-14 00:00:00 GBP 1.132283 EUR
"""

from datetime import date, datetime, time as dt_time
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Dict, List

from pricedl.model import Price


DATE_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"


class PriceRecord:
    """A row in the prices file"""

    def __init__(
        self, datetime_val: datetime, symbol: str, value: Decimal, currency: str
    ):
        self.datetime: datetime = datetime_val
        self.symbol: str = symbol
        self.value: Decimal = value
        self.currency: str = currency

    def __str__(self) -> str:
        """
        Formats the PriceRecord in Ledger flat-file format.
        Example: "P 2023-04-14 00:00:00 GBP 1.132283 EUR"
                 "P 2023-04-15 VEUR_AS 13.24 EUR" (if time is 00:00:00)
        """
        if self.datetime.time() == dt_time(0, 0, 0):
            date_time_string = self.datetime.strftime("%Y-%m-%d")
        else:
            date_time_string = self.datetime.strftime(DATE_TIME_FORMAT)

        return f"P {date_time_string} {self.symbol} {self.value} {self.currency}"

    def __repr__(self) -> str:
        return (
            f"PriceRecord(datetime_val={self.datetime!r}, symbol={self.symbol!r}, "
            f"value={self.value!r}, currency={self.currency!r})"
        )

    @classmethod
    def from_price_model(cls, item: Price) -> "PriceRecord":
        """
        Creates a PriceRecord from a Price instance.
        """
        if not isinstance(item.date, date):
            raise ValueError(f"Expected date to be a date, but got {type(item.date)}")

        # time_str = "00:00:00" if not item.time else item.time
        t = dt_time(0, 0) if not item.time else item.time
        # date_time_str = f"{item.date} {time_str}"
        dt = datetime.combine(item.date, t)

        # try:
        #     dt_val = datetime.strptime(date_time_str, DATE_TIME_FORMAT)
        # except ValueError as e:
        #     raise ValueError(
        #         f"Failed to parse date/time string: '{date_time_str}' from PriceModel - {e}"
        #     ) from e

        return cls(
            datetime_val=dt,
            symbol=str(item.symbol),
            value=item.value,
            currency=item.currency,
        )


def _parse_with_time(items: List[str]) -> PriceRecord:
    # items: [date_str, time_str, symbol, value_str, currency]
    date_time_str = f"{items[0]} {items[1]}"
    try:
        dt_val = datetime.strptime(date_time_str, DATE_TIME_FORMAT)
    except ValueError as e:
        raise ValueError(
            f"Failed to parse date/time string: '{date_time_str}' - {e}"
        ) from e

    try:
        # rust_decimal::Decimal::from_str_exact
        value = Decimal(items[3])
    except InvalidOperation as e:
        raise ValueError(f"Failed to parse decimal value: '{items[3]}'") from e

    return PriceRecord(
        datetime_val=dt_val, symbol=items[2], value=value, currency=items[4]
    )


def _parse_with_no_time(items: List[str]) -> PriceRecord:
    # items: [date_str, symbol, value_str, currency]
    date_time_str = f"{items[0]} 00:00:00"
    try:
        dt_val = datetime.strptime(date_time_str, DATE_TIME_FORMAT)
    except ValueError as e:
        raise ValueError(
            f"Failed to parse date string: '{items[0]}' (interpreted as '{date_time_str}') - {e}"
        )

    try:
        value = Decimal(items[2])
    except InvalidOperation:
        raise ValueError(f"Failed to parse decimal value: '{items[2]}'")

    return PriceRecord(
        datetime_val=dt_val, symbol=items[1], value=value, currency=items[3]
    )


def _parse_line(line: str) -> PriceRecord:
    """
    Parses a single line from the price file.
    Example: "P 2023-04-14 00:00:00 GBP 1.132283 EUR"
    """
    parts = line.split()

    if not parts or parts[0] != "P":
        raise ValueError(f"Line must start with 'P'. Got: '{line}'")

    # data_parts exclude the initial 'P'
    data_parts = parts[1:]
    num_data_parts = len(data_parts)

    if num_data_parts == 4:  # P date symbol value currency
        return _parse_with_no_time(data_parts)
    elif num_data_parts == 5:  # P date time symbol value currency
        return _parse_with_time(data_parts)
    else:
        # Corresponds to panic!("invalid number of parts parsed from the line!")
        raise ValueError(
            f"Invalid number of parts ({num_data_parts + 1} including 'P') in line: '{line}'"
        )


class PriceFlatFile:
    """
    A handler for the prices file.
    """

    def __init__(self, file_path: Path, load_on_init: bool = False):
        self.file_path: Path = file_path
        self.prices: Dict[str, PriceRecord] = {}
        if load_on_init:
            self._load_data()

    @classmethod
    def load(cls, file_path: Path) -> "PriceFlatFile":
        """Load prices from a text file."""
        instance = cls(
            file_path, load_on_init=False
        )  # Avoid double loading if __init__ also loads
        instance._load_data()
        return instance

    def _load_data(self):
        """Internal method to read and parse the price file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError as ex:
            # Corresponds to .expect("Error reading rates file")
            raise FileNotFoundError(
                f"Error reading rates file: {self.file_path} not found."
            ) from ex
        except Exception as e:
            raise IOError(f"Error reading rates file {self.file_path}: {e}") from e

        self.prices.clear()  # Clear any existing prices
        lines = content.splitlines()

        for line_num, line_content in enumerate(lines):
            line_content = line_content.strip()
            if not line_content or line_content.startswith(
                "#"
            ):  # Skip empty or comment lines
                continue
            try:
                price_record = _parse_line(line_content)
                # Last price for a symbol wins, as HashMap does in Rust
                self.prices[price_record.symbol] = price_record
            except ValueError as e:
                # In Rust, this would likely be a panic or logged error.
                # Here, we print a warning and skip the line.
                print(
                    f"Warning: Skipping malformed line {line_num + 1} in '{self.file_path}': \"{line_content}\" - {e}"
                )

    def save(self):
        """Saves the current prices to the file, ordered by date/time then symbol."""
        # Order by date/time, then symbol
        sorted_price_records = sorted(
            self.prices.values(), key=lambda pr: (pr.datetime, pr.symbol)
        )

        output_lines = [str(pr) for pr in sorted_price_records]

        output_content = "\n".join(output_lines)
        if (
            output_lines
        ):  # Add a trailing newline if there's content, matching Rust behavior
            output_content += "\n"

        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(output_content)
        except IOError as e:
            # Corresponds to .expect("saved successfully")
            raise IOError(f"Failed to save prices to {self.file_path}: {e}") from e

    # Helper for tests, similar to direct manipulation in Rust tests
    def add_price_record(self, record: PriceRecord):
        """Adds or updates a price record in the internal dictionary."""
        self.prices[record.symbol] = record

    @staticmethod
    def default() -> "PriceFlatFile":
        """Creates an empty PriceFlatFile, similar to Rust's Default trait."""
        # Default file_path could be empty or a specific default if desired.
        # For now, let's assume it needs a path, even if not immediately used for loading.
        # This matches the Rust tests which use PriceFlatFile::default() then add.
        return PriceFlatFile(file_path="", load_on_init=False)
