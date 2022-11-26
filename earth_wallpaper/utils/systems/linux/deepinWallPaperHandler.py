from dbus_next.aio import MessageBus
from subprocess import run, PIPE
import asyncio


def exec_setting(file):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.wait([set_deepin_wall_paper(file)]))


async def set_deepin_wall_paper(file):
    # https://python-dbus-next.readthedocs.io/en/latest/high-level-client/aio-proxy-interface.html
    bus = await MessageBus().connect()
    introspection = await bus.introspect('com.deepin.daemon.Appearance', '/com/deepin/daemon/Appearance')
    obj = bus.get_proxy_object('com.deepin.daemon.Appearance', '/com/deepin/daemon/Appearance', introspection)
    appearance_interface = obj.get_interface('com.deepin.daemon.Appearance')

    sub = run("xrandr|grep 'connected primary'", shell=True, universal_newlines=True, stdout=PIPE,stderr=PIPE,encoding='utf-8')
    if sub.returncode == 1:
        print(sub.stderr)
        return

    primary_screen = sub.stdout.splitlines()
    for i in primary_screen:
        screen_name = i.split(" ")[0]
        # 原始方法名为SetMonitorBackground 转换为get_wallpaper_slide_show
        await appearance_interface.call_set_monitor_background(screen_name, file)
