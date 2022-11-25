from .utils.settings import Settings
from .utils.randomddw import RandomDdw as randomDdw

xmlFileSuffix = ".xml"


class DynamicWallpapers(object):

    def __init__(self):
        self.wallpaperDir = Settings().wallpaper_dir()
        self.download_path = randomDdw().get_ddw_file(self.wallpaperDir, xmlFileSuffix)

    def run(self):
        return "file://" + self.download_path

    @staticmethod
    def name():
        # https://github.com/saint-13/Linux_Dynamic_Wallpapers
        return "Linux Dynamic Wallpapers(动态壁纸)"

    @staticmethod
    def layout():
        layout_list = ["updateTimeGroup", "wallpaperDirGroup"]
        return layout_list


if __name__ == "__main__":
    x = DynamicWallpapers()
    x.run()
