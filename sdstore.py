import machine
import os
import json

class sd:
    
    default_store = "config"
    default_path = "sdstore"
    
    def __init__(self, slot, sck, mosi, miso, cs) -> None:

        try:
            self.sd = machine.SDCard(slot=slot, sck=sck, mosi=mosi, miso=miso, cs=cs)
            os.mount(self.sd, "/sd")
            if self.default_path not in os.listdir("/sd"):
                os.mkdir("/sd/" + self.default_path)
            if "config.sdstore.py" not in os.listdir("/sd/" + self.default_path):
                with open("/sd/" + self.default_path + "/config.sdstore.py", "w") as f:
                    f.write("{}")
        except Exception as e:
            print("Failed to mount:", e)

        self.stores = {}
        with open("/sd/" + self.default_path + "/config.sdstore.py") as f:
            self.stores["config"] = json.loads(f.read())
            
    def default(self, store="config"):
        if store + ".sdstore.py" not in os.listdir("/sd/" + self.default_path):
            with open("/sd/" + self.default_path + "/" + store + ".sdstore.py", "w") as f:
                f.write("{}")
        with open("/sd/" + self.default_path + "/" + store + ".sdstore.py") as f:
            self.stores[store] = json.loads(f.read())
            self.default = store
            return self.stores[store]

    def get(self, name, value=None, store=default_store):
        return self.stores.get(store, {}).get(name, value)

    def set(self, name, value, store=default_store):
        if store not in self.stores:
            self.load(store)
        self.stores[store][name] = value
        with open("/sd/" + self.default_path + "/" + store + ".sdstore.py", "w") as f:
            f.write(json.dumps(self.stores[store]))

    def dlt(self, name, store=default_store):
        if store not in self.stores or name not in self.stores[store]:
            return False
        del self.stores[store][name]
        with open("/sd/" + self.default_path + "/" + store + ".sdstore.py", "w") as f:
            f.write(json.dumps(self.stores[store]))
        return True

    def load(self, store=default_store):
        filename = store + ".sdstore.py"
        if filename not in os.listdir("/sd/" + self.default_path):
            with open("/sd/" + self.default_path + "/" + filename, "w") as f:
                f.write("{}")
        with open("/sd/" + self.default_path + "/" + filename) as f:
            self.stores[store] = json.loads(f.read())
        return self.stores[store]

    def fill(self, store=default_store, value=None):
        if value is None:
            value = {}
        self.stores[store] = value
        with open("/sd/" + self.default_path + "/" + store + ".sdstore.py", "w") as f:
            f.write(json.dumps(self.stores[store]))
        return self.stores[store]
    
    def save(self, store=None):
        if store is None:
            for name in self.stores:
                with open("/sd/" + self.default_path + "/" + name + ".sdstore.py", "w") as f:
                    f.write(json.dumps(self.stores[name]))
        else:
            with open("/sd/" + self.default_path + "/" + store + ".sdstore.py", "w") as f:
                f.write(json.dumps(self.stores[store]))
                
    
    class file:
        
        def dir(pth=""):
            dirpth = ""
            if pth != "":
                dirpth = "/" + pth
            return os.listdir("/sd" + dirpth)
        
        def read(pth):
            with open("/sd/" + pth) as f:
                return f.read()
            
        def exists(pth):
            if filename not in os.listdir("/sd"):
                return False
            else:
                return True
            
        def new(pth, inp=""):
            if pth not in os.listdir("/sd"):
                with open("/sd/" + pth, "w") as f:
                    f.write(inp)
                return True
            else:
                return False
            
        def write(pth, inp=""):
                with open("/sd/" + pth, "w") as f:
                    f.write(inp)
                return True
            
        def store_obj(pth, inp={}):
            with open("/sd/" + pth + ".json", "w") as f:
                f.write(json.dumps(inp))
                
        def load_obj(pth, inp={}):
            if pth + ".json" not in os.listdir("/sd"):
                return False
            with open("/sd/" + pth + ".json") as f:
                return json.loads(f.read())