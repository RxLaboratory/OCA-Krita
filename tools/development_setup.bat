:: Edit these variables with the correct paths on your system
SET kritaDir=%appdata%\krita
SET OCAModule=..\..\..\OCA\lib\py

:: Need admin to create symlinks
@echo off
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)
:: Get back to original dir
pushd "%CD%"
CD /D "%~dp0"

call :getabsolute %OCAModule%
SET OCAModule=%absolute%
call :getabsolute "..\src"
SET src==%absolute%

:: remove previous install
del /Q %kritaDir%\pykrita\OCA.desktop
del /Q %kritaDir%\pykrita\OCA\*.*
rmdir %kritaDir%\pykrita\OCA

:: link the desktop file and create the plugin dir
mklink %kritaDir%\pykrita\OCA.desktop %src%\OCA.desktop
mkdir %kritaDir%\pykrita\OCA

:: link plugin files
mklink %kritaDir%\pykrita\OCA\__init__.py %src%\OCA\__init__.py
mklink %kritaDir%\pykrita\OCA\config.py %src%\OCA\config.py
mklink %kritaDir%\pykrita\OCA\oca_plugin.py %src%\OCA\oca_plugin.py
mklink %kritaDir%\pykrita\OCA\ui_oca_export.py %src%\OCA\ui_oca_export.py

mklink %kritaDir%\pykrita\OCA\manual.html %src%\OCA\manual.html

:: link OCA
mklink /D %kritaDir%\pykrita\OCA\oca_core %OCAModule%\oca_core
mklink /D %kritaDir%\pykrita\OCA\oca_krita %OCAModule%\oca_krita

:: Finished!
PAUSE

:getabsolute
set absolute=%~f1
goto :eof