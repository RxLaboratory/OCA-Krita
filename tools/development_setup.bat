:: Edit these variables with the correct paths on your system
SET kritaDir=%appdata%\krita
SET DuKRIFModule=..\..\DuKRIF\dukrif
SET OCAModule=..\..\..\OCA\ocapy

:: Need admin to create symlinks
@echo off
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)
:: Get back to original dir
pushd "%CD%"
CD /D "%~dp0"

call :getabsolute %DuKRIFModule%
SET DuKRIFModule=%absolute%
call :getabsolute %OCAModule%
SET OCAModule=%absolute%
call :getabsolute "..\src"
SET src==%absolute%

:: remove previous install
del /Q %kritaDir%\pykrita\OCA.desktop
del /Q %kritaDir%\pykrita\OCA\*.*
rmdir %kritaDir%\pykrita\OCA\ocapy
rmdir %kritaDir%\pykrita\OCA\dukrif
rmdir %kritaDir%\pykrita\OCA

:: link the desktop file and create the plugin dir
mklink %kritaDir%\pykrita\OCA.desktop %src%\OCA.desktop
mkdir %kritaDir%\pykrita\OCA
:: link plugin files
FOR /f %%f IN ('dir /b %src%\OCA\*') DO mklink %kritaDir%\pykrita\OCA\%%f %src%\OCA\%%f
:: link DuKRIF
mklink /D %kritaDir%\pykrita\OCA\dukrif %DuKRIFModule%
:: link OCA
mklink /D %kritaDir%\pykrita\OCA\ocapy %OCAModule%
:: Finished!
PAUSE

:getabsolute
set absolute=%~f1
goto :eof