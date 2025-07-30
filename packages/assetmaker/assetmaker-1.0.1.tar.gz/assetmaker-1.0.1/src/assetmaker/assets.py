import json
class Asset:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["value"])
class Assets:
    def __init__(self, json_file="assets.json"):
        self.assets = []
        self.json_file = json_file
    def add_asset(self, asset):
        self.assets.append(asset)
        self.save_assets()
    def remove_asset(self, asset):
        self.assets.remove(asset)
        self.save_assets()
    def save_assets(self):
        with open(self.json_file, "w") as f:
            json.dump([asset.to_dict() for asset in self.assets], f)
    def load_assets(self):
        try:
            with open(self.json_file, "r") as f:
                data = json.load(f)
                self.assets = [Asset.from_dict(asset_data) for asset_data in data]
        except FileNotFoundError:
            self.assets = []
    def get_asset(self, name):
        for asset in self.assets:
            if asset.name == name:
                return asset
        return None
    def get_assets(self):
        return self.assets
    def get_asset_value(self, name):
        asset = self.get_asset(name)
        if asset:
            return asset.value
        return None
    def get_asset_name(self, value):
        for asset in self.assets:
            if asset.value == value:
                return asset.name
        return None
    def get_asset_names(self):
        return [asset.name for asset in self.assets]
    def get_asset_values(self):
        return [asset.value for asset in self.assets]
    def get_asset_count(self):
        return len(self.assets)
    def get_asset_names_and_values(self):
        return [(asset.name, asset.value) for asset in self.assets]
    def get_asset_names_and_values_dict(self):
        return {asset.name: asset.value for asset in self.assets}