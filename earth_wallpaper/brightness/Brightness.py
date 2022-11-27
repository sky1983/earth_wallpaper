from earth_wallpaper.utils.platformInfo import PlatformInfo
import os
import logging

logger = logging.getLogger(__name__)


class Brightness:

    def __init__(self):
        pass

    @staticmethod
    def set_brightness():
        sys = PlatformInfo().get_os()
        logger.info(f"当前系统为{sys}")

        if sys == "WINDOWS":
            pass

        if sys == "LINUX":
            from .linux.LinuxBrightness import LinuxBrightness
            from .linux.DeepinBrightness import DeepinBrightness
            de = os.getenv('XDG_CURRENT_DESKTOP')
            logger.info(f"当前桌面环境为{de}")
            brightness_list = {
                "ubuntu:GNOME": LinuxBrightness,
                "Deepin": DeepinBrightness,
                "Gnome": LinuxBrightness
            }
            brightness_exec = brightness_list[de]()
            brightness_exec.run()

    def run(self):
        return self.set_brightness()


if __name__ == "__main__":
    x = Brightness()
    x.run()
