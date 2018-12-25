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

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

# Obtained from: https://stackoverflow.com/a/41663148
def get_descendant(widget, child_name, level, doPrint=False):
    if widget is not None:
        if doPrint: print("-" * level + ": " + (Gtk.Buildable.get_name(widget) or "(None)") + " :: " + (
                    widget.get_name() or "(None)"))
    else:
        if doPrint:  print("-" * level + ": " + "None")
        return None
    # /*** If it is what we are looking for ***/
    if Gtk.Buildable.get_name(widget) == child_name:  # not widget.get_name() !
        return widget;
    # /*** If this widget has one child only search its child ***/
    if hasattr(widget, 'get_child') and callable(getattr(widget, 'get_child')) and child_name != "":
        child = widget.get_child()
        if child is not None:
            return get_descendant(child, child_name, level + 1, doPrint)
    # /*** Ity might have many children, so search them ***/
    elif hasattr(widget, 'get_children') and callable(getattr(widget, 'get_children')) and child_name != "":
        children = widget.get_children()
        # /*** For each child ***/
        found = None
        for child in children:
            if child is not None:
                found = get_descendant(child, child_name, level + 1, doPrint)  # //search the child
                if found: return found


def get_text_fom_textview(tv):
    buf = tv.get_buffer()
    return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)


def get_row_idx_from_treeview(tv):
    selection = tv.get_selection()
    model, treeiter = selection.get_selected()
    if treeiter is not None:
        return int(model.get_path(treeiter).to_string())
    else:
        return -1


def get_row_idx_from_listbox(lb):
    selection = lb.get_selected_row()
    return selection.get_index()