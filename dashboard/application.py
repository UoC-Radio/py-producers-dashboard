# Copyright (c) 2013 Arnel A. Borja <kyoushuu@yahoo.com>
# Copyright (c) 2013 Vadim Rutkovsky <vrutkovs@redhat.com>
# Copyright (c) 2013 Lubosz Sarnecki <lubosz@gmail.com>
# Copyright (c) 2013 Guillaume Quintard <guillaume.quintard@gmail.com>
# Copyright (c) 2013 Felipe Borges <felipe10borges@gmail.com>
# Copyright (c) 2013 Eslam Mostafa <cseslam@gmail.com>
# Copyright (c) 2013 Shivani Poddar <shivani.poddar92@gmail.com>
# Copyright (c) 2013 Sai Suman Prayaga <suman.sai14@gmail.com>
# Copyright (c) 2013 Seif Lotfy <seif@lotfy.com>
# Copyright © 2018 George Galanakis <ggalan87@gmail.com>
#
# This software is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from gettext import gettext as _

from gi.repository import Gtk, Gio, GLib, Gdk

from dashboard import log
from dashboard.widgets.aboutdialog import AboutDialog
from dashboard.window import Window


class Application(Gtk.Application):
    def __repr__(self):
        return '<Application>'

    @log
    def __init__(self, application_id):
        super().__init__(
            application_id=application_id,
            flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.props.resource_base_path = "/gr/uoc/radio/dashboard"
        GLib.set_application_name(_("Producers Dashboard"))
        GLib.set_prgname('producers-dashboard')
        self._settings = Gio.Settings.new('gr.uoc.radio.dashboard')
        self._init_style()
        self._window = None
        self._application_id = application_id

    def _init_style(self):
        css_provider_file = Gio.File.new_for_uri(
            'resource:///gr/uoc/radio/dashboard/application.css')
        css_provider = Gtk.CssProvider()
        css_provider.load_from_file(css_provider_file)
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    @log
    def _build_app_menu(self):
        action_entries = [
            ('about', self._about),
            ('quit', self.quit),
        ]

        for action, callback in action_entries:
            simple_action = Gio.SimpleAction.new(action, None)
            simple_action.connect('activate', callback)
            self.add_action(simple_action)

    @log
    def _about(self, action, param):
        about = AboutDialog()
        about.props.transient_for = self._window

    @log
    def do_startup(self):
        Gtk.Application.do_startup(self)

        self._build_app_menu()

    @log
    def quit(self, action=None, param=None):
        self._window.destroy()

    def do_activate(self):
        if not self._window:
            self._window = Window(self)
            self._window.set_default_icon_name(self._application_id)
            if self._application_id == 'gr.uoc.radio.dashboardDevel':
                window.get_style_context().add_class('devel')

        self._window.present()

