from pathlib import Path

from application import App, AppGroup, SpawnMode
from group import CustomGroup, create_groups_with_keys
from keys import ALT, SUPER, keys
from libqtile import bar, layout, widget
from libqtile.backend.wayland import InputConfig
from libqtile.config import Click, Drag, Match, Screen
from libqtile.lazy import lazy
from theme import ColorScheme

HOME = Path.home()
wallpaper_path = HOME / "Pictures/Wallpapers/arch_wallpaper.png"

APPS = [
    App("konsole", ([SUPER], "Return")),
    App(
        "rofi -show drun -kb-cancel 'Escape,Super_L,Super-d'",
        ([SUPER], "d"),
        # SpawnMode.KILL,
        # Match(wm_class="Rofi", title="rofi - drun"),
        # True,
    ),
    App(
        "rofi -show window"
        " -kb-cancel 'Alt-Escape,Escape' -kb-accept-entry '!Alt-Tab,Return'"
        " -kb-row-down Alt-Tab -kb-row-up Alt-ISO_Left_Tab",
        ([ALT], "Tab"),
    ),
    App(
        "firefox",
        ([SUPER], "b"),
        SpawnMode.FOCUS,
        Match(wm_class="firefox"),
        group=AppGroup.WEB,
    ),
    App("dolphin", ([SUPER], "e")),
    App("code", ([SUPER], "c"), matcher_=Match(wm_class="Code"), group=AppGroup.DEV),
    App(
        "deezer-enhanced",
        ([SUPER], "m"),
        SpawnMode.FOCUS,
        Match(wm_class="deezer-enhanced"),
        group=AppGroup.MUSIC,
    ),
    App(
        "pavucontrol",
        ([SUPER], "p"),
        SpawnMode.KILL,
        Match(wm_class="Pavucontrol", title="Volume Control"),
        True,  # Qt version exists
    ),
    App(
        "steam",
        ([SUPER], "s"),
        SpawnMode.FOCUS,
        Match(wm_class="Steam", title="Steam"),
        group=AppGroup.GAME,
    ),
    App("libreoffice", ([SUPER], "o"), group=AppGroup.DOC),
    App("gimp", ([SUPER], "g"), SpawnMode.FOCUS, group=AppGroup.DOC),
]

GROUPS = [
    CustomGroup("Home", ""),
    CustomGroup("Web", "", AppGroup.WEB),
    CustomGroup("Dev", "", AppGroup.DEV),
    CustomGroup("System", "", AppGroup.SYS),
    CustomGroup("Doc", "", AppGroup.DOC),
    CustomGroup("Music", "", AppGroup.MUSIC),
    CustomGroup("Chat", "", AppGroup.CHAT),
    CustomGroup("Game", "", AppGroup.GAME),
]

COLORS = ColorScheme(
    fg="#ffffff",
    dim_fg="#888888",
    bg="#000000",
    accent="#007cdb",
    dark_accent="#002d81",
    neutral_accent="#888888",
    urgent_accent="#fffb00",
)

groups, group_keys = create_groups_with_keys(GROUPS, APPS)

keys.extend(app.get_key() for app in APPS)
keys.extend(group_keys)


layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Noto Sans",
    fontsize=13,
    padding=10,
    background=COLORS.bg,
    foreground=COLORS.fg,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(
                    block_highlight_text_color=COLORS.fg,
                    active=COLORS.fg,
                    inactive=COLORS.dim_fg,
                    highlight_method="block",
                    rounded=True,
                    this_current_screen_border=COLORS.accent,
                    this_screen_border=COLORS.bg,
                    highlight_color=COLORS.bg,
                    urgent_alert_method="block",
                    urgent_text=COLORS.fg,
                    urgent_border=COLORS.urgent_accent,
                    disable_drag=True,
                    padding=3,
                    margin=5,
                    fontsize=15,
                ),
                widget.TaskList(
                    border=COLORS.accent,
                    urgent_border=COLORS.urgent_accent,
                    highlight_method="block",
                    markup_floating="   {}  ",
                    markup_focused="  {}  ",
                    markup_maximized="   {}  ",
                    markup_minimized="   {}  ",
                    markup_normal="  {}  ",
                    theme_path="papirus-dark",  # Not functional
                    borderwidth=1,
                    margin=5,
                    padding=1,
                    icon_size=20,
                ),
                widget.Mpris2(  # needs deezer-enhanced ?
                    name="Deezer",
                    objname="org.mpris.MediaPlayer2.Deezer",
                    display_metadata=["xesam:title", "xesam:artist"],
                    playing_text="",
                    paused_text="",
                    stopped_text="",
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %H:%M"),
            ],
            25,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        wallpaper=str(wallpaper_path),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [SUPER],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [SUPER],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    Click([SUPER], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="ColorGrab"),
        *(app.matcher for app in APPS if app.floating),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"  # "urgent"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = {"type:touchpad": InputConfig(tap=True, natural_scroll=True)}

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
