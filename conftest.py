import pytest
import helpers

@pytest.fixture
def cancel_order():
    tracks = []

    yield tracks

    for track in tracks:
        helpers.cancel_order(track)

@pytest.fixture
def cancel_courier():
    courier_ids = []
    yield courier_ids
    for courier_id in courier_ids:
        helpers.delete_courier(courier_id)