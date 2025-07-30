'''
Test beancount methods
'''

import pytest
import main


@pytest.mark.asyncio
async def test_beancount_method():
    '''Invoke the beancount method directly'''
    actual = await main.beancount('.tables')

    assert actual is not None
