import os
import subprocess

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen, Rule, Match

from libqtile.lazy import lazy
from typing import List  # noqa: F401

import test_custom_widget as custom_widget

#############
# FUNCTIONS #
#############


class AndMatch:

    def __init__(self, **kwargs):
        self.matches = []
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, str):
                    value = [value]
                self.matches.append(Match(**{key: value}))

    def compare(self, client):
        for match in self.matches:
            if not match.compare(client):
                return False
        return True


def toggle_or_run(_exec, match=None):
    if match is None:
        match = Match(title=[_exec])

    @lazy.function
    def __inner(qtile):

        # If the app is already focused, toggle groups
        focused = qtile.current_group.current_window
        if focused is not None:
            if match.compare(focused):
                qtile.current_screen.toggle_group()
                return

        # Else, try to focus it
        for _id, window in qtile.windows_map.items():
            if match.compare(window):
                qtile.find_window(_id)
                return

        # If we couldn't find the app, launch it
        # Might be hard to focus it
        subprocess.Popen(_exec.split())

    return __inner


def spawn(command):
    return lambda qtile: qtile.cmd_spawn(command)


#############
# VARIABLES #
#############

terminal = 'termite'
dmenu = 'rofi -show drun'
browser = 'firefox'
file_manager = 'pcmanfm-qt'
resource_monitor = terminal + ' -e htop'
screen_locker = 'dm-tool switch-to-greeter'

# dictionary containing all the matches for our apps
matches = dict(
    firefox=Match(wm_class=['firefox']),
    bpytop=AndMatch(
        title=[terminal + ' -e bpytop', ' BpyTOP'],
        wm_instance_class=terminal
    ),
    deezer=Match(wm_class=['Deezer']),
    discord=AndMatch(wm_class='discord', role='browser-window'),
    lutris=Match(wm_class=['Lutris']),
    minecraft=Match(wm_class=['minecraft-launcher']),
    steam=Match(title=['Steam'], wm_class=['Steam']),
    teams=Match(wm_class=['Microsoft Teams - Preview']),
)


##########
# GROUPS #
##########

group_config = [
    ('Web', dict(
        label='',
        matches=[matches[browser]]
    )),
    ('Dev', dict(
        label='',
    )),
    ('Dev', dict(
        label='',
    )),
    ('System', dict(
        label='',
        matches=[matches['bpytop']],
    )),
    ('Music', dict(
        label='',
        matches=[matches['deezer']],
    )),
    ('Doc', dict(
        label='',
    )),
    ('Chat', dict(
        label='',
        matches=[matches['discord']],
    )),
    ('Game', dict(
        label='',
        matches=[matches['steam'], matches['lutris']],
        layout='floating',
    )),
    ('', {}),
    ('', {}),
]

groups = []
group_names = []
always_visible_groups = []

for i, (name, kwargs) in enumerate(group_config):
    if name != '':
        if name in group_names:
            name = name+'+'
        always_visible_groups.append(name)
    else:
        name = str(i+1)
        kwargs['label'] = f' {name} '
    group_names.append(name)
    groups.append(Group(name, position=i+1, **kwargs))


###############
# KEYBINDINGS #
###############

mod = 'mod4'
alt = 'mod1'

keys = [
    # Switch between windows in current stack pane
    Key([mod], 'Down', lazy.layout.down(),
        desc='Move focus down in stack pane'),
    Key([mod], 'Up', lazy.layout.up(), desc='Move focus up in stack pane'),
    Key([mod], 'Right', lazy.layout.right(),
        desc='Move focus right in stack pane'),
    Key([mod], 'Left', lazy.layout.left(),
        desc='Move focus left in stack pane'),

    # Move windows up or down in current stack
    Key([mod, 'shift'], 'Down', lazy.layout.shuffle_down(),
        desc='Move window down in current stack'),
    Key([mod, 'shift'], 'Up', lazy.layout.shuffle_up(),
        desc='Move window up in current stack'),
    Key([mod, 'shift'], 'Right', lazy.layout.shuffle_right(),
        desc='Move window right in current stack'),
    Key([mod, 'shift'], 'Left', lazy.layout.shuffle_left(),
        desc='Move window left in current stack'),

    # Adjust layout
    Key([mod], 'KP_Add', lazy.layout.increase_ratio(),
        desc='Increase master/slave size ratio'),
    Key([mod], 'KP_Subtract', lazy.layout.decrease_ratio(),
        desc='Decrease master/slave size ratio'),

    # General Qtile controls
    Key([mod], 'Tab', lazy.next_layout(), desc='Toggle between layouts'),
    Key([mod], 'f', lazy.window.toggle_fullscreen(),
        desc='Toggle fullscreen for focused window'),
    Key([mod], 'space', lazy.window.toggle_floating(),
        desc='Toggle floating for focused window'),
    Key([mod, 'shift'], 'q', lazy.window.kill(), desc='Kill focused window'),
    Key([mod, 'shift'], 'r', lazy.restart(), desc='Restart qtile'),
    Key([mod, 'control', 'shift'], 'q', lazy.shutdown(), desc='Shutdown qtile'),

    # Volume
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(
        'amixer sset Master 4%+'), desc='Raise volume'),
    Key([], 'XF86AudioLowerVolume', lazy.spawn(
        'amixer sset Master 4%-'), desc='Lower volume'),
    Key([], 'XF86AudioMute', lazy.spawn(
        'amixer sset Master toggle'), desc='Toggle mute'),

    # Brightness
    Key([], 'XF86MonBrightnessUp', lazy.spawn(
        'smart-backlight up'), desc='Brightness up'),
    Key([], 'XF86MonBrightnessDown', lazy.spawn(
        'smart-backlight down'), desc='Brightness down'),

    # Media controls
    Key([], 'XF86AudioPlay', lazy.spawn(
        'playerctl play-pause'), desc='Toggle play/pause'),
    Key([], 'XF86AudioNext', lazy.spawn('playerctl next'), desc='Next'),
    Key([], 'XF86AudioPrev', lazy.spawn('playerctl previous'), desc='Previous'),

    # Screenshots
    Key([mod], 'Print', lazy.spawn('xfce4-screenshooter -wc'),
        desc='Take window screenshot to clipboard'),
    Key([mod, alt], 'Print', lazy.spawn('gnome-screenshot -w'),
        desc='Take window screenshot to file'),
    Key([mod, 'shift'], 'Print', lazy.spawn('gnome-screenshot -fc'),
        desc='Take screenshot of an area to clipboard'),
    Key([mod, alt, 'shift'], 'Print', lazy.spawn('gnome-screenshot -f'),
        desc='Take screenshot of an area to file'),

    # Basic app launchers
    Key([mod], 'Return', lazy.spawn(terminal), desc='Launch terminal'),
    Key([mod], 'd', lazy.spawn(dmenu), desc='Launch dmenu'),
    Key([mod], 'b', toggle_or_run(browser, matches[browser]), desc='Launch web browser'),
    Key([mod], 'e', lazy.spawn(file_manager), desc='Launch file manager'),
    Key(['control', 'shift'], 'Escape', lazy.spawn(
        resource_monitor), desc='Launch resource monitor'),
    Key([mod], 'l', lazy.spawn(screen_locker), desc='Lock screen'),

    # App launchers
    Key([mod, alt], 'b', lazy.spawn('baobab'), desc='Launch baobab'),
    Key([mod, alt], 'c', lazy.spawn('chromium'), desc='Launch chromium'),
    Key([mod], 'c', lazy.spawn('code'), desc='Launch vscode'),
    Key([mod, alt], 'd', toggle_or_run('discord', matches['discord']), desc='Launch discord'),
    Key([mod, alt], 'e', lazy.spawn('dolphin'), desc='Launch dolphin'),
    Key([mod], 'g', toggle_or_run('gimp'), desc='Launch gimp'),
    Key([mod, alt], 'g', toggle_or_run('godot'), desc='Launch godot'),
    Key([mod, alt], 'l', toggle_or_run(
        'prime-run lutris', matches['lutris']), desc='Launch lutris'),
    Key([mod], 'm', toggle_or_run('deezer', matches['deezer']), desc='Launch Deezer'),
    Key([mod, alt], 'm', toggle_or_run('prime-run minecraft-launcher',
                                       matches['minecraft']), desc='Launch minecraft-launcher'),
    Key([mod], 'o', lazy.spawn('libreoffice'), desc='Launch libreoffice'),
    Key([mod], 'p', lazy.spawn('pavucontrol'), desc='Launch pavucontrol'),
    Key([mod], 's', toggle_or_run('prime-run steam', matches['steam']), desc='Launch steam'),
    Key([mod], 't', toggle_or_run('teams', matches['teams']), desc='Launch teams'),
    Key([mod], 'v', lazy.spawn('vlc'), desc='Launch vlc'),
    Key([mod], 'x', toggle_or_run(terminal + \
                                  ' -e bpytop', matches['bpytop']), desc='Launch bpytop'),
]

# Group controls
group_keys = ['ampersand', 'eacute', 'quotedbl', 'apostrophe',
              'parenleft', 'minus', 'egrave', 'underscore', 'ccedilla', 'agrave']

for name, key in zip(group_names, group_keys):

    keys.extend([
        Key([mod], key, lazy.group[name].toscreen(),
            desc=f'Switch to group {name}'),
        Key([mod, 'shift'], key, lazy.window.togroup(name, switch_group=True),
            desc=f'Switch to & move focused window to group {name}'),
    ])


#######
# BAR #
#######

colors = dict(
    red=('#ff6610', '#d84629'),
    blue=('#7080ff', '#3a6de3'),
)

accent = colors['blue']

theme = dict(
    normal='#ffffff',
    normal_invert='#000000',
    grey='#888888',
    primary=accent[0],
    secondary=accent[1],
    neutral='#444444',
    background='#000000',
    urgent='#eebb22',
    test='#05fc47',
)

widget_defaults = dict(
    font='Noto Sans',
    fontsize=13,
    padding=10,
    background=theme['background'],
    foreground=theme['normal'],
)
extension_defaults = widget_defaults.copy()

play_pause_widget = widget.TextBox(
    text='',
    padding=3,
)

screens = [
    Screen(
        bottom=bar.Bar(
            [
                custom_widget.GroupBox(
                    # color scheme
                    active=theme['normal'],
                    inactive=theme['grey'],
                    highlight_color=theme['background'],
                    block_highlight_text_color=theme['primary'],
                    this_current_screen_border=theme['primary'],
                    this_screen_border=theme['background'],
                    urgent_border=theme['urgent'],
                    urgent_text=theme['normal'],

                    # methods: 'border', 'text', 'block', or 'line'
                    highlight_method='line',
                    urgent_alert_method='line',

                    # other settings
                    rounded=True,
                    disable_drag=True,
                    always_visible=always_visible_groups,

                    # size
                    padding=3,
                    fontsize=15,
                ),

                custom_widget.Mpris2In2(
                    play_pause_widget,
                    name='deezer',
                    objname='org.mpris.MediaPlayer2.deezer',
                ),

                #widget.Spacer(length = bar.STRETCH),

                # widget.Notify(),

                # widget.Spacer(length=10),

                custom_widget.Clock(
                    padding=0,
                ),
            ],
            size=30,
            opacity=0.8,
        ),
    ),
]


###########
# LAYOUTS #
###########

layouts = [

    layout.MonadTall(
        border_focus=theme['secondary'],
        border_normal=theme['background'],
        border_width=1,
        margin=5,
        single_border_width=0,
        single_margin=0,
    ),

    layout.Max(
    ),

    layout.Floating(
        border_width=0,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = [

    # intrusive windows
    Rule(
        Match(wm_class=['xfce4-notifyd']),
        intrusive=True,
        float=True,
    )
]

follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = 'urgent'

floating_layout = layout.Floating(
    border_width=0,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        {'wmclass': 'confirm'},
        {'wmclass': 'dialog'},
        {'wmclass': 'download'},
        {'wmclass': 'error'},
        {'wmclass': 'file_progress'},
        {'wmclass': 'notification'},
        {'wmclass': 'splash'},
        {'wmclass': 'toolbar'},
        {'wmclass': 'confirmreset'},  # gitk
        {'wmclass': 'makebranch'},  # gitk
        {'wmclass': 'maketag'},  # gitk
        {'wname': 'branchdialog'},  # gitk
        {'wname': 'pinentry'},  # GPG key password entry
        {'wmclass': 'ssh-askpass'},  # ssh-askpass
    ],
)


#########
# HOOKS #
#########

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


"""
# prevent xfce4-notifyd windows from jumping around by ignoring them
@hook.subscribe.client_new
def auto_sticky(window):
    if window.name == "xfce4-notifyd":
        if window.group:
            screen = window.group.screen.index
        else:
            screen = window.qtile.current_screen.index
        window.window.configure(stackmode=xcffib.xproto.StackMode.Above)
        window.static(screen)


# from http://qtile.readthedocs.org/en/latest/manual/config/hooks.html#automatic-floating-dialogs
@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    bubble = window.window.get_wm_window_role() == 'bubble'
    if dialog or transient or bubble:
        window.floating = True


@hook.subscribe.client_new
def float_plasma(window):
    if window:
        plasma = window_match_re(window, wmclass="plasmashell")
        if plasma:
            window.floating = True
"""
