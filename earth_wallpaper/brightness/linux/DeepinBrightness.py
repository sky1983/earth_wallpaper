from dbus_next.aio import MessageBus
from subprocess import run, PIPE
import asyncio
from .BrightnessUtils import BrightnessUtils

import logging


logger = logging.getLogger(__name__)

sunriseBrightness = 0.5
dayBrightness = 0.8
sunsetBrightness = 0.6
nightBrightness = 0.2


class DeepinBrightness(object):

    @staticmethod
    def calculate_sun():
        day_utils = BrightnessUtils.run()
        sunrise = day_utils.sunrise
        day = day_utils.day
        sunset = day_utils.sunset
        night = day_utils.night
        hour = day_utils.hour
        if hour in sunrise:
            logger.info(f"sunrise 屏幕亮度设置为：{sunriseBrightness}")
            return sunriseBrightness
        elif hour in day:
            logger.info(f"day 屏幕亮度设置为：{dayBrightness}")
            return dayBrightness
        elif hour in sunset:
            logger.info(f"sunset 屏幕亮度设置为：{sunsetBrightness}")
            return sunsetBrightness
        elif hour in night:
            logger.info(f"night 屏幕亮度设置为：{nightBrightness}")
            return nightBrightness

    def exec_setting(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait([self.set_deepin_brightness(self.calculate_sun())]))

    @staticmethod
    async def set_deepin_brightness(brightness):
        # https://python-dbus-next.readthedocs.io/en/latest/high-level-client/aio-proxy-interface.html
        bus = await MessageBus().connect()
        introspection = await bus.introspect('com.deepin.daemon.Display', '/com/deepin/daemon/Display')
        obj = bus.get_proxy_object('com.deepin.daemon.Display', '/com/deepin/daemon/Display', introspection)
        appearance_interface = obj.get_interface('com.deepin.daemon.Display')

        sub = run("xrandr|grep 'connected'", shell=True, universal_newlines=True, stdout=PIPE, stderr=PIPE,
                  encoding='utf-8')
        if sub.returncode == 1:
            logger.error(sub.stderr)
            return

        screens = sub.stdout.splitlines()
        for i in screens:
            if i.__contains__('disconnected'):
                continue
            screen_name = i.split(" ")[0]
            # 原始方法名为SetMonitorBackground 转换为get_wallpaper_slide_show
            await appearance_interface.call_set_brightness(screen_name, brightness)

    def run(self):
        return self.exec_setting()


if __name__ == "__main__":
    x = DeepinBrightness()
    x.run()
