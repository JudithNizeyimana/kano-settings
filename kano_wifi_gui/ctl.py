# ctl.py
#
# Copyright (C) 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# WiFi control functions


def disconnect_wifi():
    from kano.network import KwifiCache, disconnect
    from kano.gtk3.kano_dialog import KanoDialog

    disconnect('wlan0')
    wificache = KwifiCache()
    wificache.empty()

    kdialog = KanoDialog(
        # Text from the content team.
        "Disconnect complete - you're now offline.",
    )
    kdialog.run()

    return 0


def launch_wifi_gui(socket_id=None):
    from gi.repository import GObject
    from kano_wifi_gui.wifi_window import create_wifi_gui

    GObject.threads_init()

    is_plug = socket_id is not None
    create_wifi_gui(is_plug, socket_id)

    return 0