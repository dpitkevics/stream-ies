from kivy.lang import Builder


class KvLoader:

    loaded_kvs = []
    last_active_widget_key = None

    def __init__(self, class_name, app):
        #self.load_kv(class_name, app)
        pass

    @staticmethod
    def load_kv(class_name, app):
        im = app.interface_manager

        if KvLoader.last_active_widget_key is not None and im.active_widget_key != KvLoader.last_active_widget_key:
            for loaded_kv in KvLoader.loaded_kvs:
                Builder.unload_file('kv/' + loaded_kv + '.kv')
            KvLoader.loaded_kvs = []

        KvLoader.last_active_widget_key = im.active_widget_key

        print(KvLoader.loaded_kvs)
        print(class_name)
        if class_name not in KvLoader.loaded_kvs:
            Builder.load_file('kv/' + class_name + '.kv')
            KvLoader.loaded_kvs.append(class_name)