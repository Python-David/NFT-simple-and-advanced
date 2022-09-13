from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():

    # Arrange

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    advanced, creating = deploy_and_create()
    requestId = creating.events["requestedCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced.address, {"from": get_account()}
    )
    # Assert
    assert advanced.tokenCounter() == 1
    assert advanced.tokenIdtoBreed(0) == random_number % 3
