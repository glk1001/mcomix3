'''properties_dialog.py - Properties dialog that displays information about the archive/file.'''

import os
import time
import stat

try:
    import pwd
except ImportError:
    # Running on non-Unix machine.
    pwd = None

from gi.repository import Gtk

from mcomix import i18n
from mcomix import properties_page
from mcomix import strings
from mcomix import tools


class _PropertiesDialog(Gtk.Dialog):

    def __init__(self, window):

        super(_PropertiesDialog, self).__init__(title='Properties')
        self.set_transient_for(window)
        self.add_buttons(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)
        self._window = window
        self.resize(500, 430)
        self.set_resizable(True)
        self.set_default_response(Gtk.ResponseType.CLOSE)
        self.set_border_width(4)
        self._notebook = Gtk.Notebook()
        self._notebook.set_border_width(6)

        self._archive_page = properties_page._Page()
        self._image_page = properties_page._Page()

        self._notebook.append_page(
                self._archive_page, Gtk.Label(label='Archive'))
        self._notebook.append_page(
                self._image_page, Gtk.Label(label='Image'))

        self._update_archive_page()
        self._window.page_changed += self._on_page_change
        self._window.filehandler.file_opened += self._on_book_change
        self._window.filehandler.file_closed += self._on_book_change
        self._window.imagehandler.page_available += self._on_page_available

        self.vbox.pack_start(self._notebook, True, True, 0)
        self.show_all()

    def _on_page_change(self):
        self._update_image_page()

    def _on_book_change(self):
        self._update_archive_page()

    def _on_page_available(self, page_number):
        if 1 == page_number:
            self._update_page_image(self._archive_page, 1)
        current_page_number = self._window.imagehandler.get_current_page()
        if current_page_number == page_number:
            self._update_image_page()

    def _update_archive_page(self):
        self._update_image_page()
        page = self._archive_page
        page.reset()
        window = self._window
        if window.filehandler.archive_type is None:
            if self._notebook.get_n_pages() == 2:
                self._notebook.detach_tab(page)
            return
        if self._notebook.get_n_pages() == 1:
            self._notebook.insert_page(page, Gtk.Label(label='Archive'), 0)
        # In case it's not ready yet, bump the cover extraction
        # in front of the queue.
        path = window.imagehandler.get_path_to_page(1)
        if path is not None:
            window.filehandler._ask_for_files([path])
        self._update_page_image(page, 1)
        filename = window.filehandler.get_pretty_current_filename()
        page.set_filename(filename)
        path = window.filehandler.get_path_to_base()
        main_info = (
                f'{window.imagehandler.get_number_of_pages()} pages',
                f'{window.filehandler.get_number_of_comments()} comments',
                strings.ARCHIVE_DESCRIPTIONS[window.filehandler.archive_type]
        )
        page.set_main_info(main_info)
        self._update_page_secondary_info(page, path)
        page.show_all()

    def _update_image_page(self):
        page = self._image_page
        page.reset()
        window = self._window
        if not window.imagehandler.page_is_available():
            return
        self._update_page_image(page)
        path = window.imagehandler.get_path_to_page()
        filename = os.path.basename(path)
        page.set_filename(filename)
        width, height = window.imagehandler.get_size()
        main_info = (
                '%dx%d px' % (width, height),
                window.imagehandler.get_mime_name(),
        )
        page.set_main_info(main_info)
        self._update_page_secondary_info(page, path)
        page.show_all()

    def _update_page_image(self, page, page_number=None):
        if not self._window.imagehandler.page_is_available(page_number):
            return
        thumb = self._window.imagehandler.get_thumbnail(page_number, width=128, height=128)
        page.set_thumbnail(thumb)

    @staticmethod
    def _update_page_secondary_info(page, location):
        secondary_info = [('Location', i18n.to_unicode(os.path.dirname(location))),
        ]
        try:
            stats = os.stat(location)
        except OSError as e:
            page.set_secondary_info(secondary_info)
            return
        uid = str(stats.st_uid) if pwd is None else pwd.getpwuid(stats.st_uid).pw_name
        secondary_info.extend((
                ('Size', tools.format_byte_size(stats.st_size)),
                ('Accessed', time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(stats.st_atime))),
                ('Modified', time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(stats.st_mtime))),
                ('Permissions', oct(stat.S_IMODE(stats.st_mode))),
                ('Owner', uid)
        ))
        page.set_secondary_info(secondary_info)
