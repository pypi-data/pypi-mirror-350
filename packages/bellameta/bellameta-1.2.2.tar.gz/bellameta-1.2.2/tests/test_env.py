from bellameta import constants

def test_env():
    assert constants.BELLAMETA_CONFIG_PATH == "docs/bellameta.yaml"
    assert constants.DB_PATH == "data/scans.sqlite"