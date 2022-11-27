from dbus_next.aio import MessageBus
from subprocess import run, PIPE
from earth_wallpaper.interfaces.utils.sunCalculator import SunCalculator, DateTime
import time
import asyncio
from earth_wallpaper.interfaces.utils.AddressConfig import AddressConfig

import logging


logger = logging.getLogger(__name__)

sunriseBrightness = 0.5
dayBrightness = 0.8
sunsetBrightness = 0.6
nightBrightness = 0.2


class DeepinBrightness(object):

    def __init__(self):
        self.addressConfig = AddressConfig()

    @staticmethod
    def calculate_sun(location):
        logger.info(f"经度： {location['longitude']}")
        logger.info(f"纬度： {location['latitude']}")
        latitude = float(location['latitude'])
        longitude = float(location['longitude'])

        dt = DateTime()
        sun_calculator = SunCalculator(dt.Y, dt.M, dt.D, latitude, longitude)
        st = sun_calculator.getSunTimes()
        sunrise_time = int(st.sunrise)
        sunset_time = int(st.sunset)
        sunrise = list(range(sunrise_time, sunrise_time + 4))
        day = list(range(sunrise_time + 4, sunset_time))
        sunset = [x % 24 for x in range(sunset_time, sunset_time + 4)]
        if sunset[-1] < sunrise_time:
            night = list(range(sunset[-1], sunrise_time))
        else:
            night = list(range(sunset_time + 4, 24)) + list(range(0, sunrise_time))
        hour = time.localtime(time.time()).tm_hour
        if hour in sunrise:
            return sunriseBrightness
        elif hour in day:
            return dayBrightness
        elif hour in sunset:
            return sunsetBrightness
        elif hour in night:
            return nightBrightness

    def exec_setting(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        location = self.addressConfig.get_addr()
        loop.run_until_complete(asyncio.wait([self.set_deepin_brightness(self.calculate_sun(location))]))

    @staticmethod
    async def set_deepin_brightness(brightness):
        # https://python-dbus-next.readthedocs.io/en/latest/high-level-client/aio-proxy-interface.html
        bus = await MessageBus().connect()
        introspection = await bus.introspect('com.deepin.daemon.Display', '/com/deepin/daemon/Display')
        obj = bus.get_proxy_object('com.deepin.daemon.Display', '/com/deepin/daemon/Display', introspection)
        appearance_interface = obj.get_interface('com.deepin.daemon.Display')

        sub = run("xrandr|grep 'connected primary'", shell=True, universal_newlines=True, stdout=PIPE, stderr=PIPE,
                  encoding='utf-8')
        if sub.returncode == 1:
            logger.error(sub.stderr)
            return

        primary_screen = sub.stdout.splitlines()
        for i in primary_screen:
            screen_name = i.split(" ")[0]
            # 原始方法名为SetMonitorBackground 转换为get_wallpaper_slide_show
            await appearance_interface.call_set_brightness(screen_name, brightness)

    def run(self):
        return self.exec_setting()


if __name__ == "__main__":
    x = DeepinBrightness()
    x.run()
