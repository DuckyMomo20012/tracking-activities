@echo off
cmd /k "cd /d %~dp0\env\Scripts & activate.bat & cd /d %~dp0 & download.py"