import time

class Globals():
    def __init__(self, jinja):
        self.jinja = jinja

    def unixNano(self):
        return int(time.time())

    def init(self):
        for obj in dir(self):
            if obj.startswith("__") and obj.endswith("__") or obj == "init":
                continue

            if callable(getattr(self, obj)):
                self.jinja.env.globals[obj] = getattr(self, obj)