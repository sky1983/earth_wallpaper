from .utils.settings import Settings
from .utils.randomddw import RandomDdw as randomDdw
from .utils.InterFaceEnum import InterFaceEnum

xmlFileSuffix = ".xml"


class LinuxDynamicWallpaper(object):

    def __init__(self):
        self.wallpaperDir = Settings().wallpaper_dir()
        self.download_path = randomDdw().get_ddw_file(self.wallpaperDir, xmlFileSuffix)

    def run(self):
        return "file://" + self.download_path

    @staticmethod
    def name():
        # https://github.com/saint-13/Linux_Dynamic_Wallpapers
        return InterFaceEnum.LinuxDynamicWallpaper.get_show_name()

    @staticmethod
    def layout():
        layout_list = ["updateTimeGroup", "wallpaperDirGroup"]
        return layout_list


if __name__ == "__main__":
    x = LinuxDynamicWallpaper()
    x.run()
