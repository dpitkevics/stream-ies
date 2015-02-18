from kivy.lang import Builder


class KvLoader:
    def __init__(self):
        self.load_kv()

    def load_kv(self):
        Builder.load_file('kv/' + self.__class__.__name__ + '.kv')