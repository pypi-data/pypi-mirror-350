import importlib
import importlib.metadata
import sys
import traceback

def get_fastpluggy_plugin_entrypoints():
    try:
        entry_points = importlib.metadata.entry_points()
        return list(entry_points.select(group="fastpluggy.plugins"))
    except Exception as e:
        print(f"❌ Could not read entry points from 'fastpluggy.plugins': {e}", file=sys.stderr)
        return []

def test_plugin_imports():
    errors = []
    entrypoints = get_fastpluggy_plugin_entrypoints()

    if not entrypoints:
        raise Exception("⚠️ No fastpluggy.plugins entry points found.")
        return

    print("🔍 Found fastpluggy plugins:")
    for ep in entrypoints:
        print(f" - {ep.name}: {ep.value}")

    for ep in entrypoints:
        try:
            module_path, object_name = ep.value.split(":")
        except ValueError:
            print(f"❌ Invalid entry point format: {ep.value} (should be 'module.submodule:ClassName')", file=sys.stderr)
            errors.append((ep.name, ep.value, "Invalid format"))
            continue

        try:
            mod = importlib.import_module(module_path)
            print(f"✅ Imported module: {module_path}")
        except Exception as e:
            print(f"❌ Failed to import module {module_path} → {e}", file=sys.stderr)
            traceback.print_exc()
            errors.append((ep.name, module_path, f"Module import error: {e}"))
            continue

        try:
            getattr(mod, object_name)
            print(f"✅ Found object: {object_name} in {module_path}")
        except Exception as e:
            print(f"❌ Failed to find object {object_name} in {module_path} → {e}", file=sys.stderr)
            traceback.print_exc()
            errors.append((ep.name, f"{module_path}:{object_name}", f"Object not found: {e}"))

    if errors:
        print("\n❌ Import errors summary:")
        for name, path, msg in errors:
            print(f" - Plugin '{name}' → {path}: {msg}", file=sys.stderr)
        raise SystemExit(f"{len(errors)} plugin(s) failed to import.")
    else:
        print("\n✅ All plugin entry points imported and resolved successfully.")

if __name__ == "__main__":
    test_plugin_imports()
