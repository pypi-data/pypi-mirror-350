@echo off
rmdir /s /q dist
python -m build
python -m twine upload dist/* --verbose