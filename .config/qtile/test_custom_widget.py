from libqtile import widget, drawer, bar
from libqtile.log_utils import logger

# initializing the class with the import function
widget.Battery()


class Battery(widget.battery.Battery):

    defaults = [
        ('percent_chars', ['', '', '', '', '']),
        ('wrapping_format', '{percent_char} {base_string}'),
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


class Clock(widget.clock.Clock):

    defaults = [
        ('time_format', '<span size="x-large">%H:%M</span>',
         'A python time format string'),
        ('date_format', '%A\n%d-%m-%Y', 'A python date format string'),
    ]

    def __init__(self, width=72, **config):
        widget.Clock.__init__(self, width=width, **config)
        self.add_defaults(Clock.defaults)
        self.format = self.time_format

    def _configure(self, qtile, bar):
        widget.base._TextBox._configure(self, qtile, bar)
        print('o')

    def mouse_enter(self, x, y):
        print(type(self.layout.layout))
        print(self.layout.layout.set_spacing)
        print(self.layout.layout.get_spacing())
        self.layout.layout.set_spacing(100)
        self.layout.layout.set_text('njkn')
        self.draw()
        self.format = self.date_format
        self.tick()

    def mouse_leave(self, x, y):
        self.format = self.time_format
        self.tick()

    def _configure(self, qtile, bar):
        widget.base._TextBox._configure(self, qtile, bar)
        self.layout.width = self.length


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
            return [g for g in self.qtile.groups
                    if (g.label and (g.windows or g.screen) and g.name in self.visible_groups) or
                    g.name in self.always_visible
                    ]
        else:
            return [g for g in self.qtile.groups
                    if (g.label and (g.windows or g.screen)) or
                    g.name in self.always_visible
                    ]

widget.ImprovedMpris2()


class Mpris2In2(widget.mpris2widget.ImprovedMpris2):

    defaults = [
        ('format', '<b>{title}</b> - {artist}'),
    ]

    def __init__(self, play_pause_widget, **config):
        widget.mpris2widget.ImprovedMpris2.__init__(self, **config)
        print(self.scroll_chars)
        self.add_defaults(Mpris2In2.defaults)
        self.play_pause_widget = play_pause_widget
        self.play_pause_widget.add_callbacks(self.mouse_callbacks)

    def update_display(self):
        widget.mpris2widget.ImprovedMpris2.update_display(self)
        if self.is_playing is not None:
            self.play_pause_widget.text = self.status_char
        else:
            self.play_pause_widget.text = ''
        self.bar.draw()


# initializing the class with the import function
widget.Volume()


class Volume(widget.volume.Volume):

    defaults = [
        ('format', '{emoji} {volume}')
    ]

    def __init__(self, **config):
        widget.base._TextBox.__init__(self, '0', **config)
        self.add_defaults(widget.volume.Volume.defaults)
        self.surfaces = {}
        self.volume = None
        self.add_callbacks({
            'Button1': self.cmd_mute,
            'Button3': self.cmd_run_app,
            'Button4': self.cmd_increase_vol,
            'Button5': self.cmd_decrease_vol,
        })
        self.add_defaults(Volume.defaults)

    def _update_drawer(self):
        if self.volume <= 0:
            emoji = '  '
        elif self.volume <= 30:
            emoji = '  '
        elif self.volume < 80:
            emoji = ' '
        elif self.volume >= 80:
            emoji = ''
        if self.volume == -1:
            volume = 'M'
        else:
            volume = f'{self.volume}%'
        self.text = self.format.format(
            volume=volume,
            emoji=emoji,
        )
