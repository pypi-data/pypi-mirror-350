import assetmaker

def test_assetmaker():
    Assets = assetmaker.Assets('test.json')
    assert assetmaker.Asset("test", 100)
    assert Assets.add_asset(assetmaker.Asset("test", 100))
    assert Assets.remove_asset(assetmaker.Asset("test", 100))
    assert Assets.add_asset(assetmaker.Asset("test", 100))
    assert Assets.save_assets()
    assert Assets.load_assets()
    assert Assets.get_asset("test")
    assert Assets.get_assets() == [assetmaker.Asset("test", 100).to_dict()]
    assert Assets.get_asset_value("test") == 100
    assert Assets.get_asset_name(100) == "test"