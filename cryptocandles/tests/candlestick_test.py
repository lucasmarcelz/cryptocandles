from copy import copy
from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock

import pytest

from cryptocandles.candlestick import Candlestick


@pytest.fixture(scope='session')
def candlestick_1_stateful():
    return Candlestick(crypto="FAK_FAK", frequency=1)


@pytest.fixture(scope='session')
def candlestick_5_stateful():
    return Candlestick(crypto="FAK_FAK", frequency=5)


@pytest.fixture(scope='session')
def candlestick_10_stateful():
    return Candlestick(crypto="FAK_FAK", frequency=10)


@mock.patch.object(Candlestick, 'time_now', new=MagicMock())
@mock.patch.object(Candlestick, 'send_database', new=MagicMock())
@pytest.mark.parametrize("value, date_time, change_initial_time_of_candle", [
    (40, datetime(2022, 1, 1, 1, minute=0, second=10), datetime(2022, 1, 1, 1, 0)),
    (20, datetime(2022, 1, 1, 1, minute=0, second=20), datetime(2022, 1, 1, 1, 0)),
    (10, datetime(2022, 1, 1, 1, minute=0, second=30), datetime(2022, 1, 1, 1, 0)),
    (40, datetime(2022, 1, 1, 1, minute=0, second=40), datetime(2022, 1, 1, 1, 0)),
    (30, datetime(2022, 1, 1, 1, minute=0, second=50), datetime(2022, 1, 1, 1, 0)),
    (10, datetime(2022, 1, 1, 1, minute=0, second=55), datetime(2022, 1, 1, 1, 0)),
    (10, datetime(2022, 1, 1, 1, minute=1, second=5), datetime(2022, 1, 1, 1, 0)),
])
def test_generetion_of_1_minute_candle(candlestick_1_stateful: Candlestick, value: float,
                                       date_time: datetime, change_initial_time_of_candle: datetime):
    """ Checks whether the one-minute candle is valid and sent to be saved """
    candlestick_1_stateful.initial_time = change_initial_time_of_candle
    candlestick_1_stateful.time_now.return_value = date_time
    candlestick_1_stateful.set_attributes(value)
    candle_temp = copy(candlestick_1_stateful)
    candlestick_1_stateful.save_candle_if_complete(value)
    if candlestick_1_stateful.send_database.called:
        assert candle_temp.maximum == 40
        assert candle_temp.minimum == 10
        assert candle_temp.opening == 40
        assert candle_temp.close == 10


@mock.patch.object(Candlestick, 'time_now', new=MagicMock())
@mock.patch.object(Candlestick, 'send_database', new=MagicMock())
@pytest.mark.parametrize("value, date_time, change_initial_time_of_candle", [
    (40, datetime(2022, 1, 1, 1, minute=1), datetime(2022, 1, 1, 1, 0)),
    (20, datetime(2022, 1, 1, 1, minute=1), datetime(2022, 1, 1, 1, 0)),
    (10, datetime(2022, 1, 1, 1, minute=2), datetime(2022, 1, 1, 1, 0)),
    (40, datetime(2022, 1, 1, 1, minute=3), datetime(2022, 1, 1, 1, 0)),
    (30, datetime(2022, 1, 1, 1, minute=4), datetime(2022, 1, 1, 1, 0)),
    (10, datetime(2022, 1, 1, 1, minute=4), datetime(2022, 1, 1, 1, 0)),
    (10, datetime(2022, 1, 1, 1, minute=7), datetime(2022, 1, 1, 1, 0)),
])
def test_generetion_of_5_minutes_candle(candlestick_5_stateful: Candlestick, value: float,
                                        date_time: datetime, change_initial_time_of_candle: datetime):
    """ Checks whether the one-minute candle is valid and sent to be saved """
    candlestick_5_stateful.initial_time = change_initial_time_of_candle
    candlestick_5_stateful.time_now.return_value = date_time
    candlestick_5_stateful.set_attributes(value)
    candle_temp = copy(candlestick_5_stateful)
    candlestick_5_stateful.save_candle_if_complete(value)
    if candlestick_5_stateful.send_database.called:
        assert candle_temp.maximum == 40
        assert candle_temp.minimum == 10
        assert candle_temp.opening == 40
        assert candle_temp.close == 10


@mock.patch.object(Candlestick, 'time_now', new=MagicMock())
@mock.patch.object(Candlestick, 'send_database', new=MagicMock())
@pytest.mark.parametrize("value, date_time, change_initial_time_of_candle", [
    (40, datetime(2022, 1, 1, 1, minute=1), datetime(2022, 1, 1, 1, 0)),
    (20, datetime(2022, 1, 1, 1, minute=1), datetime(2022, 1, 1, 1, 0)),
    (10, datetime(2022, 1, 1, 1, minute=2), datetime(2022, 1, 1, 1, 0)),
    (40, datetime(2022, 1, 1, 1, minute=3), datetime(2022, 1, 1, 1, 0)),
    (30, datetime(2022, 1, 1, 1, minute=4), datetime(2022, 1, 1, 1, 0)),
    (10, datetime(2022, 1, 1, 1, minute=4), datetime(2022, 1, 1, 1, 0)),
    (10, datetime(2022, 1, 1, 1, minute=11), datetime(2022, 1, 1, 1, 0)),
])
def test_generetion_of_10_minutes_candle(candlestick_10_stateful: Candlestick, value: float,
                                         date_time: datetime, change_initial_time_of_candle: datetime):
    """ Checks whether the one-minute candle is valid and sent to be saved """
    candlestick_10_stateful.initial_time = change_initial_time_of_candle
    candlestick_10_stateful.time_now.return_value = date_time
    candlestick_10_stateful.set_attributes(value)
    candle_temp = copy(candlestick_10_stateful)
    candlestick_10_stateful.save_candle_if_complete(value)
    if candlestick_10_stateful.send_database.called:
        assert candle_temp.maximum == 40
        assert candle_temp.minimum == 10
        assert candle_temp.opening == 40
        assert candle_temp.close == 10
