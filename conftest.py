import pytest
import helpers
from samokat_api import SamokatApi

api = SamokatApi()

@pytest.fixture
def cancel_order():
    tracks = []

    yield tracks

    for track in tracks:
        api.cancel_order(track)

@pytest.fixture
def cancel_courier():
    courier_ids = []
    yield courier_ids
    for courier_id in courier_ids:
        api.delete_courier(courier_id)