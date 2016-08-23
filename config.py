from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
try:
	from libqtile.manager import Key, Group
except ImportError:
	from libqtile.config import Key, Group
from libqtile.manager import Click, Drag, Screen

sup = "mod4"
alt = "mod1"

keys = [
	# General Keybindings
	Key(
		[sup, "shift"], "q",
		lazy.shutdown()
	),
	Key(
		[sup], "k",
        lazy.layout.down()
	),
	Key(
		[sup], "j",
		lazy.layout.up()
	),
	Key(
		[sup, "control"], "k",
        lazy.layout.shuffle_down()
	),
	Key(
		[sup, "control"], "j",
		lazy.layout.shuffle_up()
	),
	Key(
		[sup], "space",
        lazy.layout.next()
	),
	Key(
		[sup, "shift"], "space",
        lazy.layout.rotate()
	),
	Key(
        [sup, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key(
    	[sup], "Tab",
    	lazy.next_layout()
	),
    Key(
    	[sup], "w",
    	lazy.window.kill()
	),
    Key(
    	[sup, "control"], "r",
    	lazy.restart()
	),
    Key(
    	[sup, "control"], "q",
    	lazy.shutdown()
	),
    Key(
    	[sup], "r",
    	lazy.spawncmd()
    ),
    Key(
    	[], "XF86AudioMute",
    	lazy.spawn("amixer -q set Master toggle")
	),
	Key(
		[], "XF86AudioLowerVolume",
		lazy.spawn("amixer -c 0 sset Master 1- unmute")
	),
	Key(
		[], "XF86AudioRaiseVolume",
		lazy.spawn("amixer -c 0 sset Master 1+ unmute")
	),
	# Application bindings
    Key(
    	[sup], "Return",
    	lazy.spawn("terminator")
    ),
    Key(
    	[sup], "c",
    	lazy.spawn("chromium")
    ),
    Key(
    	[sup], "p",
    	lazy.spawn("phpstorm")
	),
    Key(
    	[sup], "s",
    	lazy.spawn("subl3")
	),
]

defaultGroups = {
	'chromium': 'web',
	'firefox': 'web',
	'terminator': 'term',
	'subl3': 'development',
	'Welcome to PhpStorm': 'development',
}

groups = [
	Group("home"),
	Group("term"),
	Group("irc"),
	Group("web"),
	Group("development"),
]

for index,grp in enumerate(groups):
	keys.extend([
        Key(
         	[sup], grp.name[0],
         	lazy.group[grp.name].toscreen()
     	),
		Key(
			[sup, "control"], grp.name[0],
			lazy.window.togroup(grp.name)
		),
	])

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2),
    layout.Tile(ratio=0.25),
]

widget_defaults = dict(
    font='Arial',
    fontsize=16,
    padding=3,
)

default_style = dict(
	fontsize = 10,
	foreground = "FF6600",
	background = "1D1D1D",
	font = "ttf-droid"
)

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.TextBox("Eray-Arch", name="default"),
                widget.Battery(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            30,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([sup], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([sup], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([sup], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.client_new
def dialogs(window):
	if(window.window.get_wm_type() == 'dialog' or window.window.get_wm_transient_for()):
		window.floating = True

@hook.subscribe.client_new
def grouper(window, windows=defaultGroups):
	windowType = window.window.get_wm_class()[0]
	f = open('/home/eray/.qtile.log', 'w+')
	f.write(window.window.get_name())
	if windowType in windows.keys():
		window.togroup(windows[windowType])
		windows.pop(windowType)
	else:
		try:
			window.togroup(windows[windowType][0])
			windows[windowType].pop(0)
		except IndexError:
			pass
	f.close()

@hook.subscribe.startup
def runner():
	import subprocess

	subprocess.Popen('startup-script')