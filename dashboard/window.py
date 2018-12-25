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

from gi.repository import Gtk, Gdk, Gio, GLib, GObject
from gettext import gettext as _

import sys
import math
from multiprocessing.pool import ThreadPool
from dashboard import log
from dashboard.widgets.headerbar import HeaderBar

# Pages
from dashboard.widgets.loginpage import LoginPage
from dashboard.widgets.golivepage import GolivePage
from dashboard.widgets.waitpage import WaitPage
from dashboard.widgets.livepage import LivePage
from dashboard.widgets.showspage import ShowsPage

from dashboard.models import AsyncResult

from dashboard.remote import *
from dashboard.views import views, utils
from dashboard.utilities import PaginationState

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

        # <State>
        self.store = Store()
        self.current_user = None
        self.user_shows = None
        self.current_show = None
        self.timer_id = None
        self.time_for_live = None

        self.pagination_state = None

        # Keep a single TextBuffer for all pages
        self.message_buffer = Gtk.TextBuffer()

        self.inbox_messages_model = Gio.ListStore()

        self.pool = ThreadPool(processes=1)

        # </State>

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
                'golive_page' : GolivePage(),
                'wait_page': WaitPage(),
                'live_page': LivePage(),
            }

        # Initiate buffers
        self._pages['golive_page'].set_buffer(self.message_buffer)
        self._pages['wait_page'].set_buffer(self.message_buffer)
        self._pages['live_page'].set_buffer(self.message_buffer)


        # Connect signals
        self._pages['login_page'].connect('login-attempted', self._on_login_attempted)
        self._pages['golive_page'].connect('golive-page-shown', self._on_golive_page_shown)
        self._pages['golive_page'].connect('golive-attempted', self._on_golive_attempted)

        self._pages['wait_page'].connect('wait-page-shown', self._on_wait_page_shown)
        self._pages['wait_page'].connect('instant-attempted', self._on_instant_attempted)
        self._pages['wait_page'].connect('cancel-attempted', self._on_cancel_attempted)

        self._pages['live_page'].connect('live-page-shown', self._on_live_page_shown)
        self._pages['live_page'].connect('goto-first-clicked', self._on_goto_first_clicked)
        self._pages['live_page'].connect('goto-previous-clicked', self._on_goto_previous_clicked)
        self._pages['live_page'].connect('goto-next-clicked', self._on_goto_next_clicked)
        self._pages['live_page'].connect('goto-last-clicked', self._on_goto_last_clicked)

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
        self._views_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)

        for k, p in self._pages.items():
            self._views_stack.add(p)

        # Setup root box
        #self._box.add(self._info_bar)
        self._box.add(self._views_stack)

        # Setup main Window
        self.set_titlebar(self._headerbar)
        self.add(self._box)

        # Show
        self.show_all()


    @property
    def window(self):
        return self._window

    # Signal handlers

    @log
    def _on_login_attempted(self, widget, username, password):
        login_succeded = validate_login(username, password)

        if login_succeded:
            self.current_user = username
            self._views_stack.set_visible_child(self._pages['golive_page'])

    @log
    def _on_golive_page_shown(self, widget):
        self.user_shows = self.store.get_user_shows(self.current_user)
        lb = utils.get_descendant(widget, 'existing_shows_view', 0)
        views.setup_shows_listbox(lb, self.user_shows)

    @log
    def _on_golive_attempted(self, widget):
        golive_succeded = True

        shows_stack = utils.get_descendant(widget, 'shows_stack', 0)
        self._setup_current_show(shows_stack)

        #TODO add logic for checking user's selection
        if golive_succeded:
            self._views_stack.set_visible_child(self._pages['wait_page'])

    @log
    def _on_wait_page_shown(self, wait_page):
        wait_page.set_title(self.current_show.title)
        wait_page.set_wait()
        self.pool.apply_async(self.query_autopilot_remaining, [wait_page], callback=Window.init_timer)

    def query_autopilot_remaining(self, wait_page):
        return AsyncResult(self, wait_page, query_autopilot_remaining())

    @staticmethod
    def init_timer(result: AsyncResult):
        result.self.time_for_live = result.actual_result
        result.widget.set_remaining(str(result.self.time_for_live))
        result.self.timer_id = GLib.timeout_add(1000, result.self._timer_callback, result.widget)

    @log
    def _on_instant_attempted(self, widget):
        self._invalidate_timer()
        self.switch_to_live()

    @log
    def _on_cancel_attempted(self, widget):
        self._invalidate_timer()
        self._views_stack.set_visible_child(self._pages['golive_page'])

    @log
    def _on_live_page_shown(self, widget):
        messages_subset, total_messages = fetch_sample_messages(20, 1)
        self.pagination_state = PaginationState(total_messages)

        _, sensitivities, (first, last) = self.pagination_state.goto_first_page()
        info = self._get_pagination_info(first, last, total_messages)
        widget.update_pagination(info, sensitivities)

        lb = utils.get_descendant(widget, 'inbox_messages_view', 0)
        views.setup_inbox_listbox(lb, self.inbox_messages_model, messages_subset)

    @log
    def _on_goto_first_clicked(self, widget):
        self._handle_pagination_clicked(widget, self.pagination_state.goto_first_page)

    @log
    def _on_goto_previous_clicked(self, widget):
        self._handle_pagination_clicked(widget, self.pagination_state.goto_previous_page)

    @log
    def _on_goto_next_clicked(self, widget):
        self._handle_pagination_clicked(widget, self.pagination_state.goto_next_page)


    @log
    def _on_goto_last_clicked(self, widget):
        self._handle_pagination_clicked(widget, self.pagination_state.goto_last_page)

    # Helper functions

    def switch_to_live(self):
        self._views_stack.set_visible_child(self._pages['live_page'])

    def _timer_callback(self, widget):
        self.time_for_live -= 1

        if self.time_for_live == 0:
            self._invalidate_timer()
            self.switch_to_live()
            return False
        else:
            widget.set_remaining(str(self.time_for_live))
            return True

    def _invalidate_timer(self):
        if self.timer_id:
            GLib.source_remove(self.timer_id)

    def _setup_current_show(self, shows_stack):
        show_option = shows_stack.get_visible_child()
        show_option_name = shows_stack.get_visible_child_name()

        if show_option_name == 'Existing':
            existing_shows = utils.get_descendant(shows_stack, 'existing_shows_view', 0)
            self.current_show = self.user_shows[utils.get_row_idx_from_listbox(existing_shows)]
        elif show_option_name == 'Special':
            special_title = utils.get_descendant(shows_stack, 'special_title', 0).get_text()
            special_nickname = utils.get_descendant(shows_stack, 'special_nickname', 0).get_text()

            self.current_show = Show(special_title, [self.current_user], special_nickname, '', [], '')
        else:
            assert False

    def _get_pagination_info(self, first, last, total_messages):
        return '{}-{} out of {}'.format(first, last, total_messages)

    def _handle_pagination_clicked(self, live_page, pagination_func):
        page_number, sensitivities, (first, last) = pagination_func()
        messages_subset, _ = fetch_sample_messages(20, page_number)

        info = self._get_pagination_info(first, last, self.pagination_state.total_items)
        live_page.update_pagination(info, sensitivities)

        views.update_inbox_model(self.inbox_messages_model, messages_subset)
