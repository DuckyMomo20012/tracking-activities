@echo off
cmd /k "cd /d %~dp0\env\Scripts & activate & cd /d %~dp0 & parent_program.py"