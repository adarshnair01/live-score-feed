from gi.repository import Gtk as gtk
from gi.repository import Notify as notify

import live_score_puller as lsp


def build_menu():
    menu = gtk.Menu()
    item_joke = gtk.MenuItem('Live Score')
    item_joke.connect('activate', joke)
    menu.append(item_joke)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def joke(_):
    notify.Notification.new("<b>Live Score</b>", lsp.live_scores(), None).show()


def quit(_):
    notify.uninit()
    gtk.main_quit()
