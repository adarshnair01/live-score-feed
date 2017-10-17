#!/usr/bin/env python

import os
import signal
import gi
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk as gtk
from gi.repository import Notify as notify

import constants
from helper import menu_builder as mb

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')


def main():
    indicator = appindicator.Indicator.new(constants.APP_INDICATOR_IDINDICATOR_ID, os.path.relpath(
        constants.ICON_PATH), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(mb.build_menu())
    notify.init(constants.APP_INDICATOR_ID)
    gtk.main()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
