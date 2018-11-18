from gi.repository import Gtk, Gdk, Gio, GLib
from gettext import gettext as _

from dashboard import log
from dashboard.widgets.headerbar import HeaderBar

# Pages
from dashboard.widgets.loginpage import LoginPage
from dashboard.widgets.golivepage import GolivePage
from dashboard.widgets.waitpage import WaitPage
from dashboard.widgets.livepage import LivePage
from dashboard.widgets.showspage import ShowsPage

from dashboard.remote import *

from enum import IntEnum

import logging
logger = logging.getLogger(__name__)


class View(IntEnum):
    """Enum for views"""
    LOGIN = 0


class Window(Gtk.ApplicationWindow):

    def __repr__(self):
        return '<Window>'

    @log
    def __init__(self, app):
        super().__init__(application=app, title=_("Producers Dashboard"))

        self.settings = Gio.Settings.new('gr.uoc.radio.dashboard')

        self.set_size_request(200, 100)

        self.prev_view = None
        self.curr_view = None

        size_setting = self.settings.get_value('window-size')
        if isinstance(size_setting[0], int) and isinstance(size_setting[1], int):
            self.resize(size_setting[0], size_setting[1])

        position_setting = self.settings.get_value('window-position')
        if len(position_setting) == 2 \
           and isinstance(position_setting[0], int) \
           and isinstance(position_setting[1], int):
            self.move(position_setting[0], position_setting[1])

        if self.settings.get_value('window-maximized'):
            self.maximize()

        self._setup_view()

        self.window_size_update_timeout = None
        self.connect("notify::is-maximized", self._on_maximized)
        self.connect("configure-event", self._on_configure_event)
       

    @log
    def _on_configure_event(self, widget, event):
        if self.window_size_update_timeout is None:
            self.window_size_update_timeout = GLib.timeout_add(500, self.store_window_size_and_position, widget)

    @log
    def store_window_size_and_position(self, widget):
        size = widget.get_size()
        self.settings.set_value('window-size', GLib.Variant('ai', [size[0], size[1]]))

        position = widget.get_position()
        self.settings.set_value('window-position', GLib.Variant('ai', [position[0], position[1]]))
        GLib.source_remove(self.window_size_update_timeout)
        self.window_size_update_timeout = None
        return False

    @log
    def _on_maximized(self, klass, value, data=None):
        self.settings.set_boolean('window-maximized', self.is_maximized())

    @log
    def _setup_view(self):


        self._pages = \
            {
                'login_page' : LoginPage(),
                'golive_page' : GolivePage()
            }

        self._pages['login_page'].connect('login_attempted', self._on_login_attempted)

        # Setup title bar
        self._headerbar = HeaderBar()

        # Setup main box
        self._box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # 1. Log view
        self._info_bar = Gtk.InfoBar()
        self._info_bar.set_message_type(1)
        lbl = Gtk.Label()
        lbl.set_text("<infobar>")
        self._info_bar.get_content_area().add(lbl)

        # 2. Views Stack
        self._views_stack = Gtk.Stack()

        for k, p in self._pages.items():
            self._views_stack.add(p)

        # Setup root box
        self._box.add(self._info_bar)
        self._box.add(self._views_stack)

        # Setup main Window
        self.set_titlebar(self._headerbar)
        self.add(self._box)

        # Show
        self.show_all()

    
    @property
    def window(self):
        return self._window

    @log
    def _on_login_attempted(self, widget, username, password):
        login_succeded = validate_login(username, password)

        if login_succeded:
            self._views_stack.set_visible_child(self._pages['golive_page'])
