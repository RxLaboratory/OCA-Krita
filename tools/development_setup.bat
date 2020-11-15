:: Edit these variables with the correct paths on your system
SET kritaDir=C:\Users\Duduf\AppData\Roaming\krita
SET DuKRIFRepo=..\..\DuKRIF

:: Need admin to create symlinks
@echo off
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)
:: Get back to original dir
pushd "%CD%"
CD /D "%~dp0"

:: link the desktop file and create the plugin dir
mklink %kritaDir%\pykrita\OCA.desktop ..\src\OCA.desktop
mkdir %kritaDir%\pykrita\OCA
:: link plugin files
FOR /f %%f IN ('dir /b ..\src\OCA\*') DO mklink %kritaDir%\pykrita\OCA\%%f ..\src\OCA\%%f
:: link DuKRIF
mklink /D %kritaDir%\pykrita\OCA\dukrif %DuKRIFRepo%\dukrif
:: Finished!
PAUSE