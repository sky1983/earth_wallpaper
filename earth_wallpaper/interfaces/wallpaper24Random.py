from .utils.platformInfo import PlatformInfo
from .utils.settings import Settings
from .utils.randomddw import RandomDdw as randomDdw
from .utils.wallpaper24Common import Wallpaper24Common

ddwFileSuffix = ".ddw"


class Wallpaper24Random(object):
    def __init__(self):
        self.wallpaperDir = Settings().wallpaper_dir()
        self.ddwFile = randomDdw().get_ddw_file(self.wallpaperDir, ddwFileSuffix)
        self.executor = Wallpaper24Common(self.ddwFile)
        self.download_path = self.executor.download_path

    def run(self):
        return self.executor.run()

    @staticmethod
    def name():
        return "24h壁纸(随机)"

    @staticmethod
    def layout():
        layout_list = ["updateTimeGroup", "wallpaperDirGroup"]
        return layout_list


if __name__ == "__main__":
    x = Wallpaper24Random()
    x.run()
