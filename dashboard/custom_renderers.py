import gi

gi.require_version('Gtk', '3.0')
gi.require_version('GIRepository', '2.0')
gi.require_version('Gst', '1.0')
gi.require_version('PangoCairo', '1.0')

from gi.repository import GIRepository, Gio, Gtk, Gst, Gdk, cairo, Pango, PangoCairo, GObject
from gi.repository.GdkPixbuf import Pixbuf
import sys
from enum import Enum
import lorem


class ProducerShowsCellRenderer(Gtk.CellRenderer):
    def __init__(self):
        super().__init__()

        self._icon = None
        self._title = None
        self._subtitle = None

        self._icon_renderer = Gtk.CellRendererPixbuf()
        self._title_renderer = Gtk.CellRendererText()
        self._subtitle_renderer = Gtk.CellRendererText()

        self.padding = 10

        # self.font_size = 15
        # self.font = "Sans Bold {}".format(self.font_size)

    @GObject.Property(type=Pixbuf)
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    @GObject.Property(type=str)
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @GObject.Property(type=str)
    def subtitle(self):
        return self._subtitle

    @subtitle.setter
    def subtitle(self, value):
        self._subtitle = value

    def do_get_size(self, widget, cell_area):
        return (0, 0, 100, 60)

    def do_render(self, ctx, widget, background_area, cell_area, flags):
        ctx.translate(0, 0)

        icon_area = Gdk.Rectangle()
        title_area = Gdk.Rectangle()
        subtitle_area = Gdk.Rectangle()

        self._title_renderer.set_property("text", self.title)
        size = self._title_renderer.get_preferred_size(widget)
        title_area.width, title_area.height = size[0].width, size[0].height

        self._subtitle_renderer.set_property("text", 'by {}'.format(self.subtitle))
        size = self._subtitle_renderer.get_preferred_size(widget)
        subtitle_area.width, subtitle_area.height = size[0].width, size[0].height

        self._icon_renderer.set_property("pixbuf", self.icon)
        size = self._icon_renderer.get_preferred_size(widget)
        icon_area.width, icon_area.height = size[0].width, size[0].height

        xpad = 2
        ypad = 2

        # cell layout
        fill_area = cell_area
        fill_area.x += xpad
        fill_area.y += ypad

        fill_area.width -= xpad * 2
        fill_area.height -= ypad * 2

        icon_area.x = fill_area.x
        icon_area.y = fill_area.y + (fill_area.height - icon_area.height) / 2

        title_area.x = icon_area.x + icon_area.width + self.padding
        title_area.y = fill_area.y
        title_area.width = fill_area.width - icon_area.width - self.padding

        subtitle_area.x = icon_area.x + icon_area.width + self.padding
        subtitle_area.y = title_area.y + title_area.height  # + self.padding
        subtitle_area.width = fill_area.width - icon_area.width - self.padding

        # render the cell
        self._title_renderer.render(ctx, widget, background_area, title_area, flags)
        self._icon_renderer.render(ctx, widget, background_area, icon_area, flags)
        self._subtitle_renderer.render(ctx, widget, background_area, subtitle_area, flags)


class InboxMessageCellRenderer(Gtk.CellRenderer):
    def __init__(self):
        super().__init__()

        self._sender = None
        self._timestamp = None
        self._message = None

        self._sender_renderer = Gtk.CellRendererText()
        self._timestamp_renderer = Gtk.CellRendererText()
        self._message_renderer = Gtk.CellRendererText()

        self.padding = 0

        # self.font_size = 15
        # self.font = "Sans Bold {}".format(self.font_size)

    @GObject.Property(type=str)
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, value):
        self._sender = value

    @GObject.Property(type=str)
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @GObject.Property(type=str)
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def do_get_size(self, widget, cell_area):
        return (0, 0, 200, 80)

    def do_render(self, ctx, widget, background_area, cell_area, flags):
        ctx.translate(0, 0)

        sender_area = Gdk.Rectangle()
        timestamp_area = Gdk.Rectangle()
        message_area = Gdk.Rectangle()

        self._sender_renderer.set_property("text", self.sender)
        size = self._sender_renderer.get_preferred_size(widget)
        sender_area.width, sender_area.height = size[0].width, size[0].height

        self._timestamp_renderer.set_property("text", self.timestamp)
        size = self._timestamp_renderer.get_preferred_size(widget)
        timestamp_area.width, timestamp_area.height = size[0].width, size[0].height

        self._message_renderer.set_property("text", self.message)
        self._message_renderer.set_property("wrap_width", cell_area.width - 5)
        self._message_renderer.set_property("wrap_mode", Pango.WrapMode.WORD)

        size = self._message_renderer.get_preferred_size(widget)
        message_area.width, message_area.height = size[0].width, size[0].height

        xpad = 2
        ypad = 2

        # cell layout
        fill_area = cell_area
        fill_area.x += xpad
        fill_area.y += ypad

        fill_area.width -= xpad * 2
        fill_area.height -= ypad * 2

        sender_area.x = fill_area.x
        sender_area.y = fill_area.y

        timestamp_area.x = sender_area.x + sender_area.width + self.padding
        timestamp_area.y = sender_area.y
        timestamp_area.width = fill_area.width - sender_area.width - self.padding

        message_area.x = fill_area.x
        message_area.y = fill_area.y + sender_area.height

        # render the cell
        self._sender_renderer.render(ctx, widget, background_area, sender_area, flags)
        self._message_renderer.render(ctx, widget, background_area, message_area, flags)
        self._timestamp_renderer.render(ctx, widget, background_area, timestamp_area, flags)


GObject.type_register(ProducerShowsCellRenderer)
GObject.type_register(InboxMessageCellRenderer)
