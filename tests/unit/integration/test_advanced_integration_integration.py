from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
import pytest
import time
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_integration():

    # Arrange

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration local testing")
    advanced, creating = deploy_and_create()
    time.sleep(60)

    # Assert
    assert advanced.tokenCounter() == 1
