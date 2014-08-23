from singleton import NamedSingleton

@NamedSingleton
class AssetStack:
    master = False
    content = ''

    def has_master(self):
        return self.master

    def set_master(self, value):
        self.master = value

    def register(self, asset):
        self.assets.append(asset)

    def add_content(self, content):
        self.content = self.content + content

    def get_content(self):
        return self.content