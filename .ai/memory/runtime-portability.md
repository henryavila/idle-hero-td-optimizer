# Runtime Portability

- The app is meant to be movable to any directory. Shell entrypoints should avoid absolute paths captured in virtualenv activation scripts or pip-generated console wrappers.
- Use `.venv/bin/python -m streamlit ...` from the project root instead of `source .venv/bin/activate` plus `streamlit`.
- `install.sh` should call `.venv/bin/python -m pip ...` after creating the venv, for the same reason.
- `run.sh` may automatically restart processes it can prove belong to this app. If a different process is still holding the configured port, prompt the user before killing it, with a safe default of not killing anything.
