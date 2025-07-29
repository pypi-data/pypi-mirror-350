import requests
from tests.tools import get_list_plugins_json

def test_plugins_loaded():
    expected_plugins = get_list_plugins_json()

    response = requests.get("http://localhost:8000/debug/plugins")
    assert response.status_code == 200, "Failed to fetch /debug/plugins"

    # Extract top-level plugin keys
    loaded_plugins = sorted(plugin_name for plugin in response.json() for plugin_name in plugin)
    print(f"Loaded plugins: {loaded_plugins}")
    missing = set(expected_plugins) - set(loaded_plugins)
    extra = set(loaded_plugins) - set(expected_plugins)

    assert not missing, f"❌ Missing plugins: {missing}"
    print("✅ All expected plugins are loaded.")

    if extra:
        print(f"⚠️ Extra plugins loaded: {extra}")

if __name__ == "__main__":
    test_plugins_loaded()
