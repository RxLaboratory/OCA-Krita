"""Checks if an update is available"""

from time import time
from PyQt5.QtWidgets import QMessageBox # pylint: disable=no-name-in-module
from . import updater
from .ui_update_dialog import UpdateDialog

def checkUpdate( toolName, toolVersion, language="en", preRelease=False, discreet=True, parentWindow=None ):
    """Checks if an update is available for the tool"""

    # if discreet, only once a day
    if discreet:
        # Disabled
        if not dailyCheck(toolName):
            return
        now = time()
        latest = latestUpdateCheck(toolName)
        # Too soon
        if now - latest < 86400:
            return

    info = updater.checkUpdate(
        "http://api.rxlab.io",
        toolName,
        toolVersion,
        "Krita",
        Application.version(), # pylint: disable=undefined-variable
        preRelease,
        language
        )

    saveUpdateTime(toolName)

    if not info["update"]:
        if not discreet:
            confirmUpToDate(toolName, parentWindow)
        print(toolName + " is up-to-date (" + toolVersion + ").")
        return

    dialog = UpdateDialog( info, toolName, toolVersion, parent=parentWindow)
    dialog.exec_()

def latestUpdateCheck(toolName):
    """Gets the last time the update was checked"""
    timeStr = Application.readSetting( toolName, "latestUdpateCheck", "0") # pylint: disable=undefined-variable
    return float( timeStr )

def saveUpdateTime(toolName):
    """Saves the time at which the update was checked"""
    Application.writeSetting( toolName, "latestUdpateCheck", str(time())) # pylint: disable=undefined-variable

def confirmUpToDate(toolName, parentWindow=None):
    """Confirms the tool is up to date"""
    if parentWindow is None:
        parentWindow = Application.activeWindow().qwindow() # pylint: disable=undefined-variable
    QMessageBox.information(
        parentWindow, # pylint: disable=undefined-variable
        toolName, toolName + " is up to date!"
        )

def dailyCheck(tooLName):
    """Checks if we must check daily for udpates"""
    c = Application.readSetting(tooLName, "dailyUpdateCheck", "True") # pylint: disable=undefined-variable
    if c == "True":
        return True
    return False
