from gi.repository import Gtk

from dashboard import log


@Gtk.Template(resource_path='/gr/uoc/radio/dashboard/AboutDialog.ui')
class AboutDialog(Gtk.AboutDialog):
    """About dialog"""

    __gtype_name__ = 'AboutDialog'

    def __repr__(self):
        return '<AboutDialog>'

    @log
    def __init__(self):
        super().__init__()

        self.connect("response", self._about_response)

        self.show()

    @log
    def _about_response(self, klass, data=None):
        klass.destroy()
