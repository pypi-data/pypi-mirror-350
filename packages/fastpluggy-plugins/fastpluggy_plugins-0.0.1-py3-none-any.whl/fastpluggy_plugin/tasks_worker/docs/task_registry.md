# 🧠 Task Registry Enhancements — Roadmap

This document tracks planned improvements for the `TaskRegistry` system in the FastPluggy Task Runner module.

---

## ✅ Current Capabilities

- [x] Manual task registration with metadata
- [x] Task retrieval via `get(name)`
- [x] Metadata listing via `list_metadata()`
- [x] Global storage via `FastPluggy.register_global(...)`
- [x] Autodiscover tasks from a module or folder
  - E.g., scan `..tasks` and auto-register all decorated functions
  - ✅ Detect decorated functions automatically
- [x] Autodiscover celery tasks
---

## 🚧 Enhancements Roadmap

### 🔍 Task Discovery & Registration


  - ☐ Option to specify custom modules/folders

---

### 🧹 Validation & UX

- [ ] **Conflict detection**
  - Warn or raise if two tasks are registered with the same name

- [ ] **Registry summary view**
  - Count total tasks, async vs sync, and most used tags

---

### 🏷️ Tag Utilities

- [ ] **Group by tag**
  - `list_by_tag("sync")` to find all tagged tasks
- [ ] **Get all unique tags**
  - `get_all_tags()` returns set of known tags

---

### 🔌 Plugin Extensions

- [ ] **Plugin-based dynamic registration**
  - Tasks can be dynamically registered by plugins at load time

- [ ] **`run_by_name()` utility**
  - `run_by_name("task_name", kwargs)` to invoke any registered task easily

---

## 💡 Notes

- Consider moving `task_registry.py` to a core service or helper location (`tasks_worker.services.registry`) if it grows further.
- Could integrate with plugin discovery in the future (e.g., `FastPluggy.load_tasks_from_plugin()`).

---

