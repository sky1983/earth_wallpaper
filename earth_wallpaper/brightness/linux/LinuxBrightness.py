import screen_brightness_control as sbc
from earth_wallpaper.interfaces.utils.sunCalculator import SunCalculator, DateTime
import time
from earth_wallpaper.interfaces.utils.AddressConfig import AddressConfig
from .BrightnessUtils import BrightnessUtils
import logging


logger = logging.getLogger(__name__)

sunriseBrightness = 50
dayBrightness = 80
sunsetBrightness = 60
nightBrightness = 20

# https://pypi.org/project/screen-brightness-control/
# https://crozzers.github.io/screen_brightness_control/extras/Installing%20On%20Linux.html


def set_brightness(brightness):
    sbc.set_brightness(brightness)


class LinuxBrightness(object):

    @staticmethod
    def calculate_sun():
        day_utils = BrightnessUtils.run()
        sunrise = day_utils.sunrise
        day = day_utils.day
        sunset = day_utils.sunset
        night = day_utils.night
        hour = day_utils.hour
        if hour in sunrise:
            set_brightness(sunriseBrightness)
            logger.info(f"sunrise 屏幕亮度设置为：{sunriseBrightness}")
        elif hour in day:
            set_brightness(dayBrightness)
            logger.info(f"day 屏幕亮度设置为：{dayBrightness}")
        elif hour in sunset:
            set_brightness(sunsetBrightness)
            logger.info(f"sunset 屏幕亮度设置为：{sunsetBrightness}")
        elif hour in night:
            set_brightness(nightBrightness)
            logger.info(f"night 屏幕亮度设置为：{nightBrightness}")

    def run(self):
        return self.calculate_sun()


if __name__ == "__main__":
    x = LinuxBrightness()
    x.run()
