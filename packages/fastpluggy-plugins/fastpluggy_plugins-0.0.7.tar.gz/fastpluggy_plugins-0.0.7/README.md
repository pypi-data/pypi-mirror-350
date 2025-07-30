# FastPluggy Official Plugins

This bundle includes FastPluggy’s pre-approved plugins for extending your application.  

## Included Plugins

- `tasks_worker`
- `ui_tools`
- `crud_tools`
- `redis_tools`

## Activation

FastPluggy will only load plugins listed in the `FP_PLUGINS` environment variable. You can specify:

- A comma-separated list of plugin names, for example:
  ```bash
  export FP_PLUGINS="tasks_worker,ui_tools,crud_tools"
  ```
- The wildcard `*` to load **all** pre-approved plugins:
  ```bash
  export FP_PLUGINS="*"
  ```

> ⚙️ **Tip:** If you leave `FP_PLUGINS` unset or empty, no plugins will be activated.

## Testing & Updating `pyproject.toml`

1. **Clone the latest plugins**  
   ```bash
   python scripts/clone_plugins.py
   ```
2. **Install `tomlkit`**  
   ```bash
   pip install tomlkit
   ```
3. **Regenerate `pyproject.toml`**  
   ```bash
   python scripts/update_pyproject.py
   ```

---
