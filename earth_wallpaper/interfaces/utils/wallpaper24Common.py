from .sunCalculator import SunCalculator, DateTime
from .platformInfo import PlatformInfo
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from .AddressConfig import AddressConfig
import os
import json
import time
import requests
import logging


logger = logging.getLogger(__name__)


def find_first_json(dir_):
    files = os.listdir(dir_)
    for file in files:
        if file.endswith(".json"):
            return file
    logger.fatal("找不到json文件")


class Wallpaper24Common(object):
    def __init__(self, ddw_file):
        self.wallpaperFile = ddw_file
        self.cache = PlatformInfo().download_dir()
        self.download_path = PlatformInfo().download_path(".png")
        self.unpackDir = self.cache + self.wallpaperFile.split("/")[-1].split(".")[0]
        self.addressConfig = AddressConfig()

    def check(self):
        if not os.path.exists(self.cache):
            os.makedirs(self.cache)
        if not os.path.exists(self.unpackDir):
            self.unpack()

    def unpack(self):
        import zipfile
        with zipfile.ZipFile(self.wallpaperFile) as zf:
            zf.extractall(self.unpackDir)

    def get_location(self):
        session = requests.Session()
        session.trust_env = False
        i = 0
        while i < 3:
            try:
                # ip = session.get("https://checkip.amazonaws.com/",
                #                  timeout=5).text.strip()
                # print(ip)
                # loc = session.get("https://ipapi.co/{}/json/".format(ip),
                #                   timeout=5).json()

                # loc = {"latitude": "29.5689", "longitude": "106.5577"}
                #
                # print(loc)
                # latitude = float(loc["latitude"])
                # longitude = float(loc["longitude"])

                # geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                #                                   '(KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36 '
                #                                   '@earth-wallpaper-ext')
                # location = geolocator.geocode("重庆市")
                # location = self.do_geocode(address="重庆市")
                # logger.info(location.address)
                # logger.info(f"经度： {location.longitude}")
                # logger.info(f"纬度： {location.latitude}")
                # longitude = float(location.longitude)
                # latitude = float(location.latitude)

                location = self.addressConfig.get_addr()

                logger.info(location["address"])
                logger.info(f"经度： {location['longitude']}")
                logger.info(f"纬度： {location['latitude']}")
                longitude = float(location['longitude'])
                latitude = float(location['latitude'])

                i = 3
                return self.calculate_sun(latitude, longitude)
            except ConnectionResetError:
                logger.warning(f"本机IP获取失败，第{i + 1}次重试")
                if i == 3:
                    return self.calculate_time(5, 18)
                else:
                    i += 1
            except KeyError:
                logger.warning("API响应错误，使用默认时间")
                i = 3
                return self.calculate_time(5, 18)
            except TypeError:
                logger.warning("该IP获取不到地理坐标，使用默认时间")
                i = 3
                return self.calculate_time(5, 18)
            except requests.exceptions.ReadTimeout:
                logger.warning(f"请求超时,第{i + 1}次重试...")
                if i == 3:
                    return self.calculate_time(5, 18)
                else:
                    i += 1
            except requests.exceptions.ConnectionError:
                logger.warning("无网络连接,使用默认时间")
                i = 3
                return self.calculate_time(5, 18)

    def calculate_sun(self, la, lo):
        dt = DateTime()
        sun_calculator = SunCalculator(dt.Y, dt.M, dt.D, la, lo)
        st = sun_calculator.getSunTimes()
        return self.calculate_time(int(st.sunrise), int(st.sunset))

    def calculate_time(self, sunrise_time, sunset_time):
        sunrise = list(range(sunrise_time, sunrise_time + 4))
        day = list(range(sunrise_time + 4, sunset_time))
        sunset = [x % 24 for x in range(sunset_time, sunset_time + 4)]
        if sunset[-1] < sunrise_time:
            night = list(range(sunset[-1], sunrise_time))
        else:
            night = list(range(sunset_time + 4, 24)) + list(range(0, sunrise_time))
        return self.read_json(sunrise, day, sunset, night)

    def read_json(self, sunrise, day, sunset, night):
        json_name = find_first_json(self.unpackDir)
        with open(self.unpackDir + "/" + json_name, "r") as f:
            theme = json.load(f)

        hour = time.localtime(time.time()).tm_hour

        if 'sunriseImageList' not in theme and hour in sunrise:
            logger.info('sunrise day')
            newDay = day + sunrise
            num = len(newDay) // len(theme["dayImageList"])
            index = newDay.index(hour) // num
            if index >= len(theme["dayImageList"]):
                index = -1
            with open(self.unpackDir + "/" + theme["imageFilename"].replace(
                "*", str(theme["dayImageList"][index])), 'rb') as fp:
                data = fp.read()
                return data

        if 'sunsetImageList' not in theme and hour in sunset:
            logger.info('sunset night')
            newNight = night + sunset
            num = len(newNight) // len(theme["nightImageList"])
            index = newNight.index(hour) // num
            if index >= len(theme["nightImageList"]):
                index = -1
            with open(self.unpackDir + "/" + theme["imageFilename"].replace(
                "*", str(theme["nightImageList"][index])), 'rb') as fp:
                data = fp.read()
                return data

        if hour in sunrise:
            logger.info('sunrise')
            num = len(sunrise) // len(theme["sunriseImageList"])
            index = sunrise.index(hour) // num
            if index >= len(theme["sunriseImageList"]):
                index = -1
            with open(self.unpackDir + "/" + theme["imageFilename"].replace(
                    "*", str(theme["sunriseImageList"][index])), 'rb') as fp:
                data = fp.read()
                return data
        elif hour in day:
            logger.info('day')
            num = len(day) // len(theme["dayImageList"])
            index = day.index(hour) // num
            if index >= len(theme["dayImageList"]):
                index = -1
            with open(self.unpackDir + "/" + theme["imageFilename"].replace(
                    "*", str(theme["dayImageList"][index])), 'rb') as fp:
                data = fp.read()
            return data
        elif hour in sunset:
            logger.info('sunset')
            num = len(sunset) // len(theme["sunsetImageList"])
            index = sunset.index(hour) // num
            if index >= len(theme["sunsetImageList"]):
                index = -1
            with open(self.unpackDir + "/" + theme["imageFilename"].replace(
                    "*", str(theme["sunsetImageList"][index])), 'rb') as fp:
                data = fp.read()
            return data
        elif hour in night:
            logger.info('night')
            num = len(night) // len(theme["nightImageList"])
            index = night.index(hour) // num
            if index >= len(theme["nightImageList"]):
                index = -1
            with open(self.unpackDir + "/" + theme["imageFilename"].replace(
                    "*", str(theme["nightImageList"][index])), 'rb') as fp:
                data = fp.read()
            return data
        else:
            logger.error("Error")

    def do_geocode(self, address, attempt=1, max_attempts=5):
        try:
            geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 '
                                              '(KHTML, like Gecko) Chrome/100.0.3770.90 Safari/537.36 '
                                              '@earth-wallpaper-ext')
            return geolocator.geocode(address)
        except GeocoderTimedOut:
            if attempt <= max_attempts:
                return self.do_geocode(address, attempt=attempt + 1)
            raise
        except Exception as error:
            message = str(error)
            logger.warning(f"获取经纬度信息发送严重错误{message}，将使用配置的经纬度信息...")
            loc = {"address": "", "latitude": "29.5647398", "longitude": "106.5478767"}
            return loc

    def run(self):
        self.check()
        return self.get_location()

    @staticmethod
    def name():
        return "24h壁纸"

    @staticmethod
    def layout():
        layout_list = ["updateTimeGroup", "wallpaperFileGroup"]
        return layout_list


if __name__ == "__main__":
    x = Wallpaper24Common()
    x.run()
