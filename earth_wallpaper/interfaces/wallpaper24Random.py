from .utils.settings import Settings
from .utils.randomddw import RandomDdw as randomDdw
from .utils.wallpaper24Common import Wallpaper24Common
from .utils.InterFaceEnum import InterFaceEnum

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
        return InterFaceEnum.Wallpaper24Random.get_show_name()

    @staticmethod
    def layout():
        layout_list = ["updateTimeGroup", "wallpaperDirGroup"]
        return layout_list


if __name__ == "__main__":
    x = Wallpaper24Random()
    x.run()
