"""thumbbar.py - Thumbnail sidebar for main window."""

import urllib
from gi.repository import GObject, Gdk, GdkPixbuf, Gtk
import cairo

from mcomix.preferences import prefs
from mcomix import image_tools
from mcomix import tools
from mcomix import constants
from mcomix import thumbnail_view


class ThumbnailSidebar(Gtk.ScrolledWindow):
    """A thumbnail sidebar including scrollbar for the main window."""

    # Thumbnail border width in pixels.
    _BORDER_SIZE = 1

    def page_num_str(self, treeviewcolumn, cell_renderer, model, itr, data):
        pyobj = model.get_value(itr, 0)

        if self.get_page_num_str_func is None:
            cell_renderer.set_property('text', str(pyobj))
            return

        cell_renderer.set_property('text', self.get_page_num_str_func(int(pyobj)))

    def __init__(self, window):
        super(ThumbnailSidebar, self).__init__()

        self._window = window
        #: Thumbnail load status
        self._loaded = False
        #: Selected row in treeview
        self._currently_selected_row = 0

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        self.get_vadjustment().step_increment = 15
        self.get_vadjustment().page_increment = 1
        # Disable stupid overlay scrollbars...
        if hasattr(self.props, 'overlay_scrolling'):
            self.props.overlay_scrolling = False

        # models - contains data
        self.get_page_num_str_func = None
        self._thumbnail_liststore = Gtk.ListStore(int, GdkPixbuf.Pixbuf, bool)

        # view - responsible for laying out the columns
        self._treeview = thumbnail_view.ThumbnailTreeView(
                self._thumbnail_liststore,
                0,  # UID
                1,  # pixbuf
                2,  # status
        )
        self._treeview.set_headers_visible(False)
        self._treeview.generate_thumbnail = self._generate_thumbnail
        self._treeview.set_activate_on_single_click(True)

        self._treeview.connect_after('drag_begin', self._drag_begin)
        self._treeview.connect('drag_data_get', self._drag_data_get)
        self._treeview.connect('row-activated', self._row_activated_event)
        self._treeview.connect('button_press_event', self._mouse_press_event)

        # enable drag and dropping of images from thumbnail bar to some file
        # manager
        self._treeview.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK,
                                                [('text/uri-list', 0, 0)], Gdk.DragAction.COPY)

        # Page column
        self._thumbnail_page_treeviewcolumn = Gtk.TreeViewColumn(None)
        self._treeview.append_column(self._thumbnail_page_treeviewcolumn)
        self._text_cellrenderer = Gtk.CellRendererText()
        self._thumbnail_page_treeviewcolumn.set_cell_data_func(self._text_cellrenderer, self.page_num_str)
        # Right align page numbers.
        self._text_cellrenderer.set_property('xalign', 1.0)
        self._thumbnail_page_treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        self._thumbnail_page_treeviewcolumn.pack_start(self._text_cellrenderer, False)
        self._thumbnail_page_treeviewcolumn.add_attribute(self._text_cellrenderer, 'text', 0)
        self._thumbnail_page_treeviewcolumn.set_visible(False)

        # Pixbuf column
        self._thumbnail_image_treeviewcolumn = Gtk.TreeViewColumn(None)
        self._treeview.append_column(self._thumbnail_image_treeviewcolumn)
        self._pixbuf_cellrenderer = Gtk.CellRendererPixbuf()
        self._thumbnail_image_treeviewcolumn.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        self._thumbnail_image_treeviewcolumn.set_fixed_width(self._pixbuf_size)
        self._thumbnail_image_treeviewcolumn.pack_start(self._pixbuf_cellrenderer, True)
        self._thumbnail_image_treeviewcolumn.add_attribute(self._pixbuf_cellrenderer, 'pixbuf', 1)

        self._treeview.set_fixed_height_mode(True)
        self._treeview.set_can_focus(False)

        self.add(self._treeview)
        self.change_thumbnail_background_color(prefs['thumb bg colour'])
        self.show_all()

        self._window.page_changed += self._on_page_change
        self._window.imagehandler.page_available += self._on_page_available

    def toggle_page_numbers_visible(self):
        """ Enables or disables page numbers on the thumbnail bar. """

        visible = prefs['show page numbers on thumbnails']
        if visible:
            number_of_pages = self._window.imagehandler.get_number_of_pages()
            number_of_digits = tools.number_of_digits(number_of_pages)
            self._text_cellrenderer.set_property('width-chars', number_of_digits + 1)
            w = self._text_cellrenderer.get_preferred_size(self._treeview)[1].width
            self._thumbnail_page_treeviewcolumn.set_fixed_width(w)
        self._thumbnail_page_treeviewcolumn.set_visible(visible)

    def get_width(self):
        """Return the width in pixels of the ThumbnailSidebar."""
        return self.size_request().width

    def show(self, *args):
        """Show the ThumbnailSidebar."""
        self.load_thumbnails()
        super(ThumbnailSidebar, self).show()

    def hide(self):
        """Hide the ThumbnailSidebar."""
        super(ThumbnailSidebar, self).hide()
        self._treeview.stop_update()

    def clear(self):
        """Clear the ThumbnailSidebar of any loaded thumbnails."""

        self._loaded = False
        self._treeview.stop_update()
        self._thumbnail_liststore.clear()
        self._currently_selected_page = 0

    def resize(self):
        """Reload the thumbnails with the size specified by in the
        preferences.
        """
        self.clear()
        self._thumbnail_image_treeviewcolumn.set_fixed_width(self._pixbuf_size)
        self.load_thumbnails()

    def change_thumbnail_background_color(self, colour):
        """ Changes the background color of the thumbnail bar. """

        self.set_thumbnail_background(colour)
        # Force a redraw of the widget.
        self._treeview.queue_draw()

    def set_thumbnail_background(self, color):

        rgba = Gdk.RGBA(*color)
        self._pixbuf_cellrenderer.set_property('cell-background-rgba', rgba)
        self._text_cellrenderer.set_property('background-rgba', rgba)
        fg_color = image_tools.text_color_for_background_color(color)
        fg_rgba = Gdk.RGBA(*(fg_color.to_floats() + (1.0,)))
        self._text_cellrenderer.set_property('foreground-rgba', fg_rgba)

    @property
    def _pixbuf_size(self):
        # Don't forget the extra pixels for the border!
        return prefs['thumbnail size'] + 2 * self._BORDER_SIZE

    def load_thumbnails(self):
        """Load the thumbnails, if it is appropriate to do so."""

        if (not self._window.filehandler.file_loaded or
                self._window.imagehandler.get_number_of_pages() == 0 or
                self._loaded):
            return

        self.toggle_page_numbers_visible()

        # Detach model for performance reasons
        model = self._treeview.get_model()
        self._treeview.set_model(None)

        # Create empty preview thumbnails.
        filler = self._get_empty_thumbnail()
        for row in range(self._window.imagehandler.get_number_of_pages()):
            self._thumbnail_liststore.append((row + 1, filler, False))

        self._loaded = True

        # Re-attach model
        self._treeview.set_model(model)

        # Update current image selection in the thumb bar.
        self._set_selected_row(self._currently_selected_row)

    def _generate_thumbnail(self, uid):
        """ Generate the pixbuf for C{path} at demand. """
        assert isinstance(uid, int)
        page = uid
        pixbuf = self._window.imagehandler.get_thumbnail(page,
                                                         prefs['thumbnail size'], prefs['thumbnail size'], nowait=True)
        if pixbuf is not None:
            pixbuf = image_tools.add_border(pixbuf, self._BORDER_SIZE)

        return pixbuf

    def _set_selected_row(self, row, scroll=True):
        """Set currently selected row.
        If <scroll> is True, the tree is automatically
        scrolled to ensure the selected row is visible.
        """
        self._currently_selected_row = row
        self._treeview.get_selection().select_path(row)
        if self._loaded and scroll:
            self._treeview.scroll_to_cell(row, use_align=True, row_align=0.25)

    def _get_selected_row(self):
        """Return the index of the currently selected row."""
        try:
            return self._treeview.get_selection().get_selected_rows()[1][0][0]

        except IndexError:
            return 0

    def _row_activated_event(self, treeview, path, column):
        """Handle events due to changed thumbnail selection."""
        selected_row = self._get_selected_row()
        self._set_selected_row(selected_row, scroll=False)
        self._window.set_page(selected_row + 1)

    def _mouse_press_event(self, widget, event):
        if self._window.was_out_of_focus:
            # if the window was out of focus and the user clicks on
            # the thumbbar then do not select that page because they
            # more than likely have many pages open and are simply trying
            # to give mcomix focus again
            return True
        return False

    def _drag_data_get(self, treeview, context, selection, *args):
        """Put the URI of the selected file into the SelectionData, so that
        the file can be copied (e.g. to a file manager).
        """

        selected = self._get_selected_row()
        path = self._window.imagehandler.get_path_to_page(selected + 1)
        uri = 'file://localhost' + urllib.request.pathname2url(path)
        selection.set_uris([uri])

    @staticmethod
    def _drag_begin(treeview, context):
        """We hook up on drag_begin events so that we can set the hotspot
        for the cursor at the top left corner of the thumbnail (so that we
        might actually see where we are dropping!).
        """
        path = treeview.get_cursor()[0]
        surface = treeview.create_row_drag_icon(path)
        # Because of course a cairo.Win32Surface does not have
        # get_width/get_height, that would be to easy...
        cr = cairo.Context(surface)
        x1, y1, x2, y2 = cr.clip_extents()
        width, height = x2 - x1, y2 - y1
        pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, width, height)
        Gtk.drag_set_icon_pixbuf(context, pixbuf, -5, -5)

    def _get_empty_thumbnail(self):
        """ Create an empty filler pixmap. """
        pixbuf = GdkPixbuf.Pixbuf.new(colorspace=GdkPixbuf.Colorspace.RGB,
                                      has_alpha=True,
                                      bits_per_sample=8,
                                      width=self._pixbuf_size,
                                      height=self._pixbuf_size)

        # Make the pixbuf transparent.
        pixbuf.fill(0)

        return pixbuf

    def _on_page_change(self):
        row = self._window.imagehandler.get_current_page() - 1
        if row == self._currently_selected_row:
            return
        self._set_selected_row(row)

    def _on_page_available(self, page):
        """ Called whenever a new page is ready for display. """
        if self.get_visible():
            self._treeview.draw_thumbnails_on_screen()

# vim: expandtab:sw=4:ts=4
