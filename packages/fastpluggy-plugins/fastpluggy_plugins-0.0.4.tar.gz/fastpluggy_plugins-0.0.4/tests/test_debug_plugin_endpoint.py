import requests
from tests.tools import get_list_plugins_json
import textwrap

def test_plugins_loaded():
    expected_plugins = set(get_list_plugins_json())

    # Fetch the plugins endpoint
    response = requests.get("http://localhost:8000/debug/plugins")
    assert response.status_code == 200, "Failed to fetch /debug/plugins"
    plugins_json = response.json()

    # Track problems
    errors = []

    # 1) Check for tracebacks in each plugin
    for plugin in plugins_json:
        for name, info in plugin.items():
            tb = info.get("traceback") or []
            if tb:
                # Join multi-line tracebacks into one block per plugin
                tb_block = "\n".join(tb)
                errors.append(f"Plugin '{name}' raised traceback:\n{textwrap.indent(tb_block, '    ')}")

    # 2) Compare loaded vs expected names
    loaded = {name for plugin in plugins_json for name in plugin}
    missing = expected_plugins - loaded
    extra   = loaded - expected_plugins

    if missing:
        errors.append(f"Missing plugins: {sorted(missing)}")
    if extra:
        errors.append(f"Extra plugins:   {sorted(extra)}")

    # If anything went wrong, fail here with the full report
    if errors:
        all_issues = "\n\n".join(errors)
        raise AssertionError(f"❌ Plugin load problems detected:\n\n{all_issues}")

    # Otherwise, happy path
    print("✅ All plugins loaded without errors, and no missing/extra items.")

if __name__ == "__main__":
    test_plugins_loaded()
