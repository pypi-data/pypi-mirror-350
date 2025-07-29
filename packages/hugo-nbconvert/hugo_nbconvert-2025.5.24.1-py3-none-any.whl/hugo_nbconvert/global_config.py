class Config:
    def __init__(self):
        self.is_toml = False

    def set_toml(self):
        self.is_toml = True

    def is_toml(self):
        return self.is_toml


config = Config()

