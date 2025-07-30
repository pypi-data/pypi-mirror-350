"""
Test for Vanguard downloader.
"""

# from datetime import datetime
from datetime import datetime
from decimal import Decimal
import pytest
from pricedl.quotes.vanguard_au_2023_detail import (
    VanguardAu3Downloader,
    SecuritySymbol,
    Price,
)  # Assuming the main code is in vanguard_au_2023_detail.py


def test_url_generation():
    """Test if the URL gets correctly generated for a fund"""
    symbol = SecuritySymbol("VANGUARD", "HY")
    dl = VanguardAu3Downloader()
    actual = dl.get_url(symbol)
    expected = "https://www.vanguard.com.au/personal/api/products/personal/fund/8106/detail?limit=-1"
    assert actual == expected


@pytest.mark.asyncio
async def test_hy_price_dl():
    """test downloading the price for HY"""
    dl = VanguardAu3Downloader()
    symbol = SecuritySymbol("VANGUARD", "HY")

    # This test makes a live network request.
    # In a real test suite, you might want to mock this.
    try:
        actual_price = await dl.download(symbol, "AUD")
    except Exception as e:
        pytest.fail(f"Download failed: {e}")

    assert actual_price.currency == "AUD"  # API should return AUD
    assert actual_price.value != 0
    # assert actual_price.denom != 0
    assert actual_price.date is not None and actual_price.date != ""

    # Verify date format
    # try:
    #     datetime.strptime(actual_price.date, "%Y-%m-%d")
    # except ValueError:
    #     pytest.fail("Date format is incorrect, should be YYYY-MM-DD")
    assert actual_price.date

    print(f"Downloaded Price for {symbol}: {actual_price}")


@pytest.mark.asyncio
async def test_prop_price_dl():
    """test downloading the price for PROP"""
    dl = VanguardAu3Downloader()
    symbol = SecuritySymbol("VANGUARD", "PROP")
    try:
        actual_price = await dl.download(symbol, "AUD")
    except Exception as e:
        pytest.fail(f"Download failed: {e}")

    assert actual_price.currency == "AUD"
    assert actual_price.value != 0
    # assert actual_price.denom != 0
    assert actual_price.date is not None and actual_price.date != ""
    print(f"Downloaded Price for {symbol}: {actual_price}")


def test_parse_price():
    """test parsing the price"""
    dl = VanguardAu3Downloader()

    # Test case 1: Typical price
    price_obj1 = dl._parse_price("2023-10-26", "1.2345", "AUD")
    assert price_obj1.date == datetime.strptime("2023-10-26", "%Y-%m-%d").date()
    assert price_obj1.value == Decimal("1.2345")
    assert price_obj1.currency == "AUD"

    # Test case 2: Price with two decimal places
    price_obj2 = dl._parse_price("2023-10-27", "56.78", "USD")
    assert price_obj2.date == datetime.strptime("2023-10-27", "%Y-%m-%d").date()
    assert price_obj2.value == Decimal("56.78")
    assert price_obj2.currency == "USD"

    # Test case 3: Integer price
    price_obj3 = dl._parse_price("2023-10-28", "123", "EUR")
    assert price_obj3.date == datetime.strptime("2023-10-28", "%Y-%m-%d").date()
    assert price_obj3.value == Decimal("123")
    assert price_obj3.currency == "EUR"

    # Test case 4: Price like "0.987"
    price_obj4 = dl._parse_price("2023-10-29", "0.987", "AUD")
    assert price_obj4.date == datetime.strptime("2023-10-29", "%Y-%m-%d").date()
    assert price_obj4.value == Decimal("0.987")
    assert price_obj4.currency == "AUD"


# Example of how to run the downloader (optional, for direct execution)
async def main():
    """manual test"""
    downloader = VanguardAu3Downloader()
    hy_symbol = SecuritySymbol("VANGUARD", "HY")
    prop_symbol = SecuritySymbol("VANGUARD", "PROP")

    try:
        print(f"Fetching price for {hy_symbol}...")
        hy_price = await downloader.download(hy_symbol, "AUD")
        print(
            f"VANGUARD:HY Price: Date={hy_price.date}, Value={hy_price.value}, "
            "Denom={hy_price.denom}, Currency={hy_price.currency}"
        )

        print(f"Fetching price for {prop_symbol}...")
        prop_price = await downloader.download(prop_symbol, "AUD")
        print(
            f"VANGUARD:PROP Price: Date={prop_price.date}, Value={prop_price.value}, "
            "Denom={prop_price.denom}, Currency={prop_price.currency}"
        )

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # To run the main function:
    # asyncio.run(main())

    # To run tests (if not using pytest):
    # You'd need to manually call test functions and handle async if not using pytest-asyncio
    # For example:
    # test_url_generation()
    # asyncio.run(test_hy_price_dl())
    # test_parse_price()
    print(
        "Python script loaded. To run example usage, uncomment asyncio.run(main()) in __main__ block."
    )
