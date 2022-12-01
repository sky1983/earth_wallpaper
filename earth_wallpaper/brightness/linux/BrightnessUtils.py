from earth_wallpaper.interfaces.utils.sunCalculator import SunCalculator, DateTime
import time
from earth_wallpaper.interfaces.utils.AddressConfig import AddressConfig

import logging


logger = logging.getLogger(__name__)


class BrightnessUtils(object):
    def __init__(self):
        self.sunrise = None
        self.day = None
        self.sunset = None
        self.night = None
        self.hour = None
        self.addressConfig = AddressConfig()

    def calculate_sun(self):
        location = self.addressConfig.get_addr()
        logger.info(f"经度： {location['longitude']}")
        logger.info(f"纬度： {location['latitude']}")
        latitude = float(location['latitude'])
        longitude = float(location['longitude'])

        dt = DateTime()
        sun_calculator = SunCalculator(dt.Y, dt.M, dt.D, latitude, longitude)
        st = sun_calculator.getSunTimes()
        sunrise_time = int(st.sunrise)
        sunset_time = int(st.sunset)
        self.sunrise = list(range(sunrise_time, sunrise_time + 4))
        self.day = list(range(sunrise_time + 4, sunset_time))
        self.sunset = [x % 24 for x in range(sunset_time, sunset_time + 4)]
        if self.sunset[-1] < sunrise_time:
            self.night = list(range(self.sunset[-1], sunrise_time))
        else:
            self.night = list(range(sunset_time + 4, 24)) + list(range(0, sunrise_time))
        self.hour = time.localtime(time.time()).tm_hour

    @staticmethod
    def run():
        utils = BrightnessUtils()
        utils.calculate_sun()
        return utils


if __name__ == "__main__":
    x = BrightnessUtils()
    x.run()
