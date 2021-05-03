# -*- coding: utf-8 -*-
"""about_dialog.py - About dialog."""

from gi.repository import Gtk
import webbrowser

from mcomix import constants
from mcomix import strings
from mcomix import image_tools
from mcomix import tools


class _AboutDialog(Gtk.AboutDialog):
    def __init__(self, window):
        super(_AboutDialog, self).__init__()
        self.set_transient_for(window)

        self.set_name(constants.APPNAME)
        self.set_program_name(constants.APPNAME + ' (glk fork)')
        self.set_version(constants.VERSION)
        self.set_website('https://sourceforge.net/p/mcomix/wiki/')
        self.set_copyright('Copyright © 2005-2016')

        icon_data = tools.read_binary('images', 'mcomix.png')
        pix_buff = image_tools.load_pixbuf_data(icon_data)
        self.set_logo(pix_buff)

        comment = f'{constants.APPNAME} is an image viewer specifically designed to handle comic books.' \
                  + ' It reads ZIP, RAR and tar archives, as well as plain image files.'
        self.set_comments(comment)

        lic = f'{constants.APPNAME} is licensed under the terms of the GNU General Public License.' \
              + ' A copy of this license can be obtained from http://www.gnu.org/licenses/gpl-2.0.html'
        self.set_wrap_license(True)
        self.set_license(lic)

        authors = [f'{name}: {description}' for name, description in strings.AUTHORS]
        self.set_authors(authors)

        translators = [f'{name}: {description}' for name, description in strings.TRANSLATORS]
        self.set_translator_credits('\n'.join(translators))

        artists = [f'{name}: {description}' for name, description in strings.ARTISTS]
        self.set_artists(artists)

        self.connect('activate-link', self._on_activate_link)

        self.show_all()

    @staticmethod
    def _on_activate_link(about_dialog, uri):
        webbrowser.open(uri)
        return True
