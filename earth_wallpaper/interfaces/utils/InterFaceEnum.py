from enum import Enum, unique


@unique
class InterFaceEnum(Enum):
    Anime = ('Anime', '动漫壁纸')
    BingRand = ('BingRand', '必应壁纸(随机)')
    BingToday = ('BingToday', '必应壁纸(今日)')
    LocalWallpaper = ('LocalWallpaper', '本地壁纸')
    Wallpaper24 = ('Wallpaper24', '24h壁纸')
    FengYun4 = ('FengYun4', '风云四号')
    Himawari8 = ('Himawari8', '向日葵八号')
    Wallhaven = ('Wallhaven', '24h壁纸')
    Wallpaper24Random = ('Wallpaper24Random', '24h壁纸(随机)')
    LinuxDynamicWallpaper = ('LinuxDynamicWallpaper', 'Linux Dynamic Wallpapers(动态壁纸)')

    def __init__(self, name, show_name):
        self.api_name = name
        self.show_name = show_name

    def get_api_name(self):
        return self.api_name

    def get_show_name(self):
        return self.show_name


