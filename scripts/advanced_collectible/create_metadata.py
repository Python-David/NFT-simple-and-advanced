from genericpath import exists
from urllib import request
from brownie import AdvancedCollectible, network
from metadata.sample_metadata import metadata_template
from scripts.helpful_scripts import get_breed
from pathlib import Path
import requests
import json
import os

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")

    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdtoBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        print(metadata_file_name)

        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            image_filename = "./img/" + breed.lower().replace("_", "-") + ".png"

            image_url = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_url = upload_to_ipfs(image_filename)
            image_url = image_url if image_url else breed_to_image_uri[breed]
            collectible_metadata["image"] = image_url
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_url = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_url)
        return image_url
