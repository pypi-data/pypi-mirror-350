'''
Test the new logic, that downloads in memory.
'''
import pytest

from pricedl.direct_dl import dl_quotes
from pricedl.model import SecurityFilter


@pytest.mark.asyncio
async def test_xetra_dl():
    '''
    EXH9
    '''
    sec_filter = SecurityFilter(None, None, None, 'EXH9')
    await dl_quotes(sec_filter)

@pytest.mark.asyncio
async def test_nasdaq_dl():
    '''
    OPI
    '''
    sec_filter = SecurityFilter(None, None, None, 'OPI')
    await dl_quotes(sec_filter)

@pytest.mark.asyncio
async def test_aud_rate():
    '''
    CURRENCY:AUD
    '''
    sec_filter = SecurityFilter(None, None, 'CURRENCY', 'AUD')
    await dl_quotes(sec_filter)

@pytest.mark.asyncio
async def test_aussie_stock():
    '''
    ASX:VHY
    '''
    sec_filter = SecurityFilter(None, None, 'ASX', 'VHY')
    await dl_quotes(sec_filter)

@pytest.mark.asyncio
async def test_vanguard():
    '''
    VANGUARD:HY
    '''
    sec_filter = SecurityFilter(None, None, 'VANGUARD', 'HY')
    await dl_quotes(sec_filter)
