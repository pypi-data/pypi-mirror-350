@echo off
setlocal enabledelayedexpansion
.venv\Scripts\activate && rmdir /s /q dist && python -m build && twine upload --username __token__ --password "%PYPI_TOKEN%" dist/*
