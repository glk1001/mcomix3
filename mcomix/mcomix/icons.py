"""icons.py - Load MComix specific icons."""

from gi.repository import Gtk

from mcomix import image_tools
from mcomix import log
from mcomix import tools


def mcomix_icons():
    """ Returns a list of differently sized pixbufs for the
    application icon. """

    sizes = ('16x16', '32x32', '48x48')
    pixbufs = [image_tools.load_pixbuf_data(tools.read_binary('images', size, 'mcomix.png')) for size in sizes]

    return pixbufs


def load_icons():
    _icons = (('gimp-flip-horizontal.png', 'mcomix-flip-horizontal'),
              ('gimp-flip-vertical.png', 'mcomix-flip-vertical'),
              ('gimp-rotate-180.png', 'mcomix-rotate-180'),
              ('gimp-rotate-270.png', 'mcomix-rotate-270'),
              ('gimp-rotate-90.png', 'mcomix-rotate-90'),
              ('gimp-thumbnails.png', 'mcomix-thumbnails'),
              ('gimp-transform.png', 'mcomix-transform'),
              ('tango-enhance-image.png', 'mcomix-enhance-image'),
              ('tango-add-bookmark.png', 'mcomix-add-bookmark'),
              ('tango-archive.png', 'mcomix-archive'),
              ('tango-image.png', 'mcomix-image'),
              ('library.png', 'mcomix-library'),
              ('comments.png', 'mcomix-comments'),
              ('zoom.png', 'mcomix-zoom'),
              ('lens.png', 'mcomix-lens'),
              ('double-page.png', 'mcomix-double-page'),
              ('manga.png', 'mcomix-manga'),
              ('fitbest.png', 'mcomix-fitbest'),
              ('fitwidth.png', 'mcomix-fitwidth'),
              ('fitheight.png', 'mcomix-fitheight'),
              ('fitmanual.png', 'mcomix-fitmanual'),
              ('fitsize.png', 'mcomix-fitsize'))

    # Load window title icons.
    pixbufs = mcomix_icons()
    Gtk.Window.set_default_icon_list(pixbufs)
    # Load application icons.
    factory = Gtk.IconFactory()
    for filename, stockid in _icons:
        try:
            icon_data = tools.read_binary('images', filename)
            pixbuf = image_tools.load_pixbuf_data(icon_data)
            iconset = Gtk.IconSet.new_from_pixbuf(pixbuf)
            factory.add(stockid, iconset)
        except Exception:
            log.warning(f'! Could not load icon "{filename}"')
    factory.add_default()
