import urwid

from urwid import AttrMap
from urwid import Text
from urwid import Frame
from urwid import Overlay
from urwid import ExitMainLoop
from urwid import ListBox
from urwid import Button
from urwid import Divider
from urwid import Padding
from urwid import SolidFill
from urwid import GridFlow
from urwid import Pile
from urwid import Filler

choice = None

palette = [
    ('header', 'bold', ''),
    ('footer', 'standout', ''),
    ('reversed', 'standout', ''),
]

def start(config):
    """Start the widget and handle user input. Blocks until the widget exits."""

    def item_chosen(button, server):
        global choice
        choice = server
        response = Text([u'Connecting to: ', server.connection_string(), u'\n'])
        done = Button(u'Ok')
        urwid.connect_signal(done, 'click', exit_program)
        main.original_widget = Filler(Pile([response, AttrMap(done, None, focus_map='reversed')]))

    def exit_program(button):
        raise urwid.ExitMainLoop()

    def unhandled(key):
        vim_map = {'h': 'left', 'j': 'down', 'k': 'up', 'l': 'right'}
        if key in vim_map.keys():
            list_box.keypress((0,1), vim_map[key])
        elif key in ['left', 'right']:
            pass
        elif key in ['esc', 'q']:
            raise ExitMainLoop()

    body = [urwid.Text(u'\nServers'), Divider(u'-')]

    for server in config.servers:
        button = Button(server.name)
        urwid.connect_signal(button, 'click', item_chosen, server)
        body.append(AttrMap(button, None, focus_map='reversed'))

    list_box = ListBox(urwid.SimpleFocusListWalker(body))

    main = Padding(list_box, left=2, right=2)

    overlay = Overlay(main, SolidFill(u'\N{MEDIUM SHADE}'),
        align='center', width=('relative', 60),
        valign='middle', height=('relative', 60),
        min_width=20, min_height=9)

    header = AttrMap(Text(u' ssh-menu'), 'header')
    footer = AttrMap(Text(u'this is the footer'), 'footer')

    frame = Frame(overlay, header=header, footer=footer)

    urwid.MainLoop(urwid.AttrMap(frame, 'body'), palette=palette, unhandled_input=unhandled).run()

    return choice
