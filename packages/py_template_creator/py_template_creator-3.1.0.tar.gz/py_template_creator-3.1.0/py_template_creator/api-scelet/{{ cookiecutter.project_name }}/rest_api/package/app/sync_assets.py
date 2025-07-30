from assetsstore.assets import FileAssets


def sync_assets_with_remote():
    asset = FileAssets.get_asset(local_store="./assets/")
    asset.del_folder("media")
    asset.put_folder("media")


if __name__ == "__main__":
    sync_assets_with_remote()
