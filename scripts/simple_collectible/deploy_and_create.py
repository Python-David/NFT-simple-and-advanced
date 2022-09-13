from scripts.helpful_scripts import get_account, OPEN_SEA_URL
from brownie import SimpleCollectible, network, config

sample_token_uri = (
    "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
)


def main():
    deploy_and_create()


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)

    print(
        f"Awesome, you can now view your NFT on OPENSEA at {OPEN_SEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}"
    )

    print("Please wait up to 20mins, and then hit the refresh metadata button.")

    return simple_collectible
