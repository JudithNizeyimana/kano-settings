#!/usr/bin/env python

# set_wifi.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

from gi.repository import Gtk, Pango
import os
import kano_settings.components.heading as heading
import kano_settings.components.fixed_size_box as fixed_size_box
import kano_settings.constants as constants
import kano_settings.config_file as config_file

internet = False
network_message = ""


# TODO: Use the function in kanowifilib.py
def is_internet():
    '''
    Ping Google DNS servers avoiding name resolution delays for faster response time
    '''
    try:
        rc = os.system('ping -c 1 8.8.8.8 > /dev/null 2>&1')
        return rc == 0
    except:
        return False


def activate(_win, box, update):
    global internet, network_message

    title = heading.Heading("", "")
    box.pack_start(title.container, False, False, 0)

    # Table
    settings = fixed_size_box.Fixed()
    box.pack_start(settings.box, False, False, 0)

    # TODO: this should be done when starting the tool and only once
    # Check for internet
    internet = is_internet()

    internet_img = Gtk.Image()

    internet_status = Gtk.Label()
    internet_status.modify_font(Pango.FontDescription("Bariol bold 12"))
    internet_status_style = internet_status.get_style_context()

    internet_action = Gtk.Label()
    internet_action.modify_font(Pango.FontDescription("Bariol bold 11"))
    internet_action_style = internet_action.get_style_context()
    internet_action_style.add_class("white")
    internet_status_style.add_class("internet_status_top")
    internet_action_style.add_class("internet_status_bottom")

    status_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    status_box.set_valign(Gtk.Align.CENTER)
    status_box.pack_start(internet_status, False, False, 2)
    status_box.pack_start(internet_action, False, False, 2)

    event_box = Gtk.EventBox()
    event_box.add(status_box)
    event_box_style = event_box.get_style_context()

    container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    container.pack_start(event_box, False, False, 0)
    container.pack_start(internet_img, False, False, 0)
    container.props.halign = Gtk.Align.CENTER
    container.props.valign = Gtk.Align.CENTER

    settings.box.pack_start(container, False, False, 0)

    #event_box.set_events("button-press-event", self.on_button_press_event)
    event_box.connect("button-press-event", apply_changes)

    if internet is False:
        internet_img.set_from_file(constants.media + "/Graphics/Internet-connection.png")
        title.title.set_text("Weee you have internet")
        title.description.set_text("Great!")
        network_message = "Weee you have internet"
        internet_status.set_text(network_message)
        internet_status_style.remove_class("dark_red")
        internet_status_style.add_class("dark_green")
        internet_action.set_text("Configure")
        event_box_style.add_class("connected")
    else:
        internet_img.set_from_file(constants.media + "/Graphics/Internet-noConnection.png")
        title.title.set_text("No network found")
        title.description.set_text("Shit man")
        internet_status.set_text("No network found")
        internet_status_style.remove_class("dark_green")
        internet_status_style.add_class("dark_red")
        internet_action.set_text("+ Click to add")
        event_box_style.add_class("not_connected")

    box.pack_start(update.box, False, False, 0)


def apply_changes(event, button):
    # Call WiFi config
    os.system('rxvt -title \'WiFi\' -e sudo /usr/bin/kano-wifi')
    config_file.replace_setting("Wifi", network_message)
