# import dbus
# import markupsafe

from libqtile import widget  # , drawer, bar

# initializing the class with the import function
widget.Battery()


class Battery(widget.battery.Battery):

    defaults = [
        ("percent_chars", ["", "", "", "", ""]),
        ("wrapping_format", "{percent_char} {base_string}"),
    ]

    def __init__(self, **config):
        widget.battery.Battery.__init__(self, **config)
        self.add_defaults(widget.battery.Battery.defaults)
        self.add_defaults(Battery.defaults)

    def build_string(self, status):
        base_string = widget.battery.Battery.build_string(self, status)
        fractions = len(self.percent_chars)
        index = int(status.percent * fractions)
        if index == fractions:
            index = fractions - 1
        return self.wrapping_format.format(
            percent_char=self.percent_chars[index],
            base_string=base_string,
        )


class HideableText(widget.base._TextBox):
    def __init__(self, group=None, hidden=False, **config):
        widget.base._TextBox.__init__(self, **config)
        self.is_hidden = False
        self.oldtext = self.text
        if group is not None:
            group.append(self)
        if hidden:
            self.hide()

    def button_press(self, x, y, button):
        name = "Button{0}".format(button)
        if name in self.mouse_callbacks:
            self.mouse_callbacks[name](self.qtile)

    """
    def __setattr__(self, name, value):
        if name == 'text':
            widget.base.__TextBox
    """

    def hide(self):
        self.is_hidden = True
        self.oldtext = self.text
        self.text = ""
        if self.configured:
            self.bar.draw()

    def show(self):
        self.is_hidden = False
        self.text = self.oldtext
        if self.configured:
            self.bar.draw()

    def toggle(self):
        if self.is_hidden:
            self.show()
        else:
            self.hide()


widget.Clock()


class Clock(widget.clock.Clock):

    defaults = [
        (
            "time_format",
            '<span size="x-large">%H:%M</span>',
            "A python time format string",
        ),
        ("date_format", "%A\n%d-%m-%Y", "A python date format string"),
    ]

    def __init__(self, width=72, **config):
        widget.Clock.__init__(self, width=width, **config)
        self.add_defaults(Clock.defaults)
        self.format = self.time_format
        # Button.__init__(self, **config)

    def mouse_enter(self, x, y):
        self.format = self.date_format
        self.tick()

    def mouse_leave(self, x, y):
        self.format = self.time_format
        self.tick()

    def button_press(self, x, y, button):
        name = "Button{0}".format(button)
        if name in self.mouse_callbacks:
            self.mouse_callbacks[name](self.qtile)

    def _configure(self, qtile, bar):
        widget.base._TextBox._configure(self, qtile, bar)
        self.layout.width = self.length


widget.GroupBox()


class GroupBox(widget.groupbox.GroupBox):
    def __init__(self, always_visible, **config):
        widget.GroupBox.__init__(self, **config)
        self.always_visible = always_visible

    @property
    def groups(self):
        """
        returns list of visible groups.
        The existing groups are filtered by the visible_groups attribute and
        their label. Groups with an empty string as label are never contained.
        Groups that are not named in visible_groups are not returned.
        """
        if self.visible_groups:
            return [
                g
                for g in self.qtile.groups
                if (
                    g.label
                    and (g.windows or g.screen)
                    and g.name in self.visible_groups
                )
                or g.name in self.always_visible
            ]
        else:
            return [
                g
                for g in self.qtile.groups
                if (g.label and (g.windows or g.screen))
                or g.name in self.always_visible
            ]


'''
class ScrollingDrawer(drawer.Drawer):
    def __init__(self, *args, **kwargs):
        drawer.Drawer.__init__(self, *args, **kwargs)

    def draw(self, offsetx=0, offsety=0, width=None, height=None, srcx=0, srcy=0):
        """
        Parameters
        ==========

        offsetx :
            the X offset to start drawing at.
        offsety :
            the Y offset to start drawing at.
        width :
            the X portion of the canvas to draw at the starting point.
        height :
            the Y portion of the canvas to draw at the starting point.
        """
        self.qtile.conn.conn.core.CopyArea(
            self.pixmap,
            self.wid,
            self.gc,
            srcx,
            srcy,  # srcx, srcy
            offsetx,
            offsety,  # dstx, dsty
            self.width if width is None else width,
            self.height if height is None else height,
        )


class ScrollText(widget.base._TextBox):

    defaults = [
        ("scroll_interval", 0.04),
        ("scroll_downtime", 2),
        ("scroll_step", 1),
        ("loop", True),
        ("max_width", 200),
        ("minimize_width", True),
    ]

    def __init__(self, **config):
        widget.base._TextBox.__init__(self, **config)
        self.add_defaults(ScrollText.defaults)

        # intern scrolling variables
        self.is_scrolling = False
        self.scroll_index = 0
        self.scroll_id = 0

        # width attributes
        if not self.minimize_width:
            self.length_type = bar.STATIC
            self.length = self.max_width

    def _configure(self, qtile, bar):
        # widget.base._Widget configuration with changed drawer
        self.qtile = qtile
        self.bar = bar
        self.drawer = ScrollingDrawer(
            qtile, self.win.wid, self.bar.width, self.bar.height
        )
        if not self.configured:
            self.configured = True
            self.qtile.call_soon(self.timer_setup)
        # widget.base._TextBox configuration
        if self.fontsize is None:
            self.fontsize = self.bar.height - self.bar.height / 5
        self.layout = self.drawer.textlayout(
            self.formatted_text,
            self.foreground,
            self.font,
            self.fontsize,
            self.fontshadow,
            markup=self.markup,
        )
        self.prepare_scroll()

    def get_content_width(self):
        sizelayout = self.drawer.textlayout(
            self.text,
            "ffffff",
            self.font,
            self.fontsize,
            None,
            markup=self.markup,
        )
        return sizelayout.width

    def is_drawable(self):
        return self.width - 2 * self.actual_padding > 0

    def can_scroll(self):
        return (
            self.scroll_index + self.max_width
            < self.content_width + 2 * self.actual_padding
        )

    def draw(self, same_layout=False):
        """Draw the widget, taking scrolling into account"""

        # if the bar hasn't placed us yet
        if self.offsetx is None:
            return
        if self.is_drawable() and self.text != "":
            # clear if needed
            if not same_layout:
                self.drawer.clear(self.background or self.bar.background)
                self.layout.draw(
                    0 or self.actual_padding,
                    int(self.bar.height / 2.0 - self.layout.height / 2.0) + 1,
                )
            # left padding
            if not same_layout:
                self.drawer.draw(offsetx=self.offsetx, width=self.actual_padding)
            # drawing text with scroll offset
            self.drawer.draw(
                offsetx=self.offsetx + self.actual_padding,
                width=self.width - 2 * self.actual_padding,
                srcx=self.actual_padding + self.scroll_index,
            )
            # right padding
            if not same_layout:
                self.drawer.draw(
                    offsetx=self.offsetx + self.width - self.actual_padding,
                    width=self.actual_padding,
                )

    def prepare_scroll(self):
        self.scroll_index = 0
        self.content_width = self.get_content_width()
        if self.can_scroll():
            self.length_type = bar.STATIC
            self.length = self.max_width
        elif self.minimize_width:
            self.length_type = bar.CALCULATED
        self.bar.draw()

    def start_scroll(self, _id=None):
        if _id is None or self.scroll_id == _id:
            self.prepare_scroll()
            if self.length_type == bar.STATIC:
                _id = self.scroll_id
                self.timeout_add(self.scroll_downtime, lambda: self.scroll(_id, 0))
                self.is_scrolling = True

    def scroll(self, _id, index):
        if self.scroll_id != _id or index != self.scroll_index or not self.is_scrolling:
            return
        self.scroll_index += self.scroll_step
        self.draw(same_layout=True)
        if self.can_scroll():
            index = self.scroll_index
            self.timeout_add(self.scroll_interval, lambda: self.scroll(_id, index))
        else:
            if self.loop:
                self.timeout_add(self.scroll_downtime, lambda: self.start_scroll(_id))
            else:
                self.stop_scroll()

    def stop_scroll(self):
        if self.is_scrolling:
            self.scroll_id += 1
            self.is_scrolling = False


def log(content):
    open("mpris.log", "a").write(str(content) + "\n")


# initializing the class with the import function
widget.Mpris2()


class Mpris2(widget.mpris2widget.Mpris2, ScrollText):

    defaults = [
        ("play_char", ""),
        ("pause_char", ""),
        ("format", "{status_char}  <b>{title}</b> - {artist}"),
        ("txt_inactive", ""),
        ("scrolling_enabled", True),
        ("fetch_song_buffer_delay", 0.12),
    ]

    def __init__(self, **config):
        widget.mpris2widget.Mpris2.__init__(self, **config)
        ScrollText.__init__(self, **config)
        self.add_defaults(Mpris2.defaults)
        self.interface = None
        self.add_callbacks(
            {
                "Button1": lambda: self.send_cmd("PlayPause"),
                "Button4": lambda: self.fetch_song("Previous"),
                "Button5": lambda: self.fetch_song("Next"),
            }
        )
        self.metadata = {}
        self.status_char = ""
        self.is_playing = None
        self.text = self.txt_inactive
        self.is_fetching = None
        open("mpris.log", "w")

    def _configure(self, qtile, bar):
        ScrollText._configure(self, qtile, bar)

        # we don't need to reconnect all the dbus stuff if we already
        # connected it.
        if self.dbus_loop is not None:
            return

        # we need a main loop to get event signals
        # we just piggyback on qtile's main loop
        self.dbus_loop = dbus.mainloop.glib.DBusGMainLoop()
        self.bus = dbus.SessionBus(mainloop=self.dbus_loop)
        self.bus.add_signal_receiver(
            self.update,
            "PropertiesChanged",
            "org.freedesktop.DBus.Properties",
            self.objname,
            "/org/mpris/MediaPlayer2",
        )

    def _init_interface(self):
        try:
            obj = self.bus.get_object(self.objname, "/org/mpris/MediaPlayer2")
            self.interface = dbus.Interface(obj, "org.mpris.MediaPlayer2.Player")
        except dbus.DBusException:
            self.interface = None
            self.is_playing = None
            self.update_display()

    def send_cmd(self, command):
        if self.interface is None:
            self._init_interface()
        try:
            getattr(self.interface, command)()
        except dbus.DBusException as e:
            self._init_interface()
            if self.interface is not None:
                getattr(self.interface, command)()

    def update(self, interface_name, changed_properties, invalidated_properties):
        """http://specifications.freedesktop.org/mpris-spec/latest/Track_List_Interface.html#Mapping:Metadata_Map"""
        if not self.configured:
            return True

        # collecting and updating playback status
        playbackstatus = changed_properties.get("PlaybackStatus")
        if playbackstatus == "Paused":
            self.is_playing = False
            self.status_char = self.pause_char
        elif playbackstatus == "Playing":
            self.is_playing = True
            self.status_char = self.play_char

        # collecting and updating metadata
        m = changed_properties.get("Metadata")
        if m:
            self.metadata = {
                x.replace("xesam:", ""): str(m.get(x))
                if isinstance(m.get(x), dbus.String)
                else " + ".join(y for y in m.get(x) if isinstance(y, dbus.String))
                for x in self.display_metadata
                if m.get(x)
            }
            if self.markup:
                self.metadata = {
                    key: str(markupsafe.escape(value))
                    for key, value in self.metadata.items()
                }

        # updating display
        self.update_display()

    def update_display(self):

        # creating new displaytext
        if self.is_playing is not None:
            try:
                self.displaytext = self.format.format(
                    status_char=self.status_char, **self.metadata
                )
            except KeyError:
                self.is_playing = None
                self.displaytext = self.txt_inactive
        else:
            self.displaytext = self.txt_inactive

        # effectively displaying it
        self.text = self.displaytext
        if self.scrolling_enabled:
            if self.is_playing:
                self.start_scroll()
            else:
                self.stop_scroll()
                self.prepare_scroll()
        else:
            self.bar.draw()

    def fetch_song(self, command):
        if self.is_fetching != command:
            self.is_fetching = command
            self.send_cmd(command)

            def timeout():
                self.is_fetching = None

            self.timeout_add(self.fetch_song_buffer_delay, timeout)


class Mpris2In2(Mpris2):

    defaults = [
        ("format", "<b>{title}</b> - {artist}"),
    ]

    def __init__(self, play_pause_widget, **config):
        super().__init__(**config)
        self.add_defaults(Mpris2In2.defaults)
        self.play_pause_widget = play_pause_widget
        self.play_pause_widget.add_callbacks(self.mouse_callbacks)

    def update_display(self):
        Mpris2.update_display(self)
        if self.is_playing is not None:
            self.play_pause_widget.text = self.status_char
        else:
            self.play_pause_widget.text = ""
        self.bar.draw()
'''


# initializing the class with the import function
widget.Volume()


class Volume(widget.volume.Volume):

    defaults = [("format", "{emoji} {volume}")]

    def __init__(self, **config):
        widget.base._TextBox.__init__(self, "0", **config)
        self.add_defaults(widget.volume.Volume.defaults)
        self.surfaces = {}
        self.volume = None
        self.add_callbacks(
            {
                "Button1": self.cmd_mute,
                "Button3": self.cmd_run_app,
                "Button4": self.cmd_increase_vol,
                "Button5": self.cmd_decrease_vol,
            }
        )
        self.add_defaults(Volume.defaults)

    def _update_drawer(self):
        if self.volume <= 0:
            emoji = "  "
        elif self.volume <= 30:
            emoji = "  "
        elif self.volume < 80:
            emoji = " "
        elif self.volume >= 80:
            emoji = ""
        if self.volume == -1:
            volume = "M"
        else:
            volume = f"{self.volume}%"
        self.text = self.format.format(
            volume=volume,
            emoji=emoji,
        )
