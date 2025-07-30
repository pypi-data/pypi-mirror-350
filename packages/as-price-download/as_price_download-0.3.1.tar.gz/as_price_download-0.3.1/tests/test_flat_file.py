"""
Test price file handling
"""

from decimal import Decimal
from pathlib import Path

from pricedl.model import Price
from pricedl.price_flat_file import PriceFlatFile, PriceRecord


def test_reading():
    """
    Test reading a price file
    """
    file_path = Path("tests/prices.txt")
    price_file = PriceFlatFile.load(file_path)

    assert len(price_file.prices) == 4
    assert price_file.prices["VEUR_AS"].value == Decimal("1.5")
    assert price_file.prices["VEUR_AS"].currency == "EUR"
    assert price_file.prices["VEUR_AS"].datetime.strftime("%Y-%m-%d") == "2023-04-15"
    assert price_file.prices["VEUR_AS"].datetime.strftime("%H:%M:%S") == "12:00:00"
    assert price_file.prices["VEUR_AS"].symbol == "VEUR_AS"

def test_conversion_to_datarecord():
    '''
    Convert Price to PriceRecord in the prices text file.
    '''
    # arrange
    price = Price(date="2023-04-15", time="12:00:00", symbol="VEUR_AS", 
                  value=1.5, currency="EUR", source="test")
    # act
    price_record = PriceRecord.from_price_model(price)
    # assert
    assert price_record.datetime.strftime("%Y-%m-%d") == "2023-04-15"
    assert price_record.datetime.strftime("%H:%M:%S") == "12:00:00"
    assert price_record.symbol == "VEUR_AS"
    assert price_record.value == Decimal("1.5")
    assert price_record.currency == "EUR"
