import screen_brightness_control as sbc
from earth_wallpaper.interfaces.utils.sunCalculator import SunCalculator, DateTime
import time
from earth_wallpaper.interfaces.utils.AddressConfig import AddressConfig
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
            set_brightness(sunriseBrightness)
        elif hour in day:
            set_brightness(dayBrightness)
        elif hour in sunset:
            set_brightness(sunsetBrightness)
        elif hour in night:
            set_brightness(nightBrightness)

    def run(self):
        location = self.addressConfig.get_addr()
        return self.calculate_sun(location)


if __name__ == "__main__":
    x = LinuxBrightness()
    x.run()
