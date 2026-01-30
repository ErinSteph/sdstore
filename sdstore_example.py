# Lib for using SD Cards as value storage
# (with simplified file system manager included)
# `*` = mandatory

# V1.0.0 - initial

import sdstore
import machine

# sd = sdstore.sd(slot*=[sd slot], sck*=[sck pin], mosi*=[mosi pin], miso*=[miso pin], cs*=[cs pin])
sd = sdstore.sd(slot=2, sck=machine.Pin(18), mosi=machine.Pin(23), miso=machine.Pin(19), cs=machine.Pin(5))

# storage uses dictionaries and files.
# the default store is "config"
# you can access the dictionary directly at sd.stores["config"]
# it's saved to file in sd/sdstore/config.sdstore
# if you like, you can use sd.default(name) to change the default store after init, or just sd.default() to reset back.
sd.default()
# you could also change the storage path from /sdstore/ by setting `path` if you want, sd.default(path="user/storage/skibidi")
print("Defaults: ", sd.default_path, sd.default_store)


# get stored values with sd.get(name*, value=None, store=default_store)
# sd.get(name*) return stored, or None if empty.
# sd.get(name*, "alt") return stored, or "alt" if empty.
# sd.get(name*, store="friends") = use friends.sdstore and sd.stores["friends"] instead of config.sdstore and sd.stores["config"].
if sd.get("something") is None:
    # sd.set(name*, value*, store)
    # adds the key/value to the store dict, then saves dict to the store file.
    sd.set("something", "beans")
#will print beans
print(sd.get("something"))

# delete stored value with sd.dlt(name*, store)

# lets have a dict:
group = {
    "Amy": "Girl",
    "Andy": "Boy",
    "Justin": "Dog"
}

# set adds key and value to store dict, then saves dict as JSON, so non-raw objects are fine
sd.set("friendgroup", group)
print(sd.stores["config"]["friendgroup"]["Amy"])
print(sd.get("friendgroup")["Andy"])

# create a whole store with sd.fill(name*, object)
# populates a whole storage file (name.sdstore) and dictionary (sd.stores[name]).
sd.fill("friends", group)

# sd.load("friends")
# loads a whole storage file, adds it to the dictionary, and returns it.
# the dic is returned, and sd.stores["friends"] is populated.
group = sd.load("friends")

# save all stores to files with sd.save(), or one with sd.save(name)
# if you modify the dict manually instead of with sd.set(), this will be needed.
sd.stores["config"]["friendgroup"]["Amy"] = "Plant"
sd.save()
print(sd.get("friendgroup")["Amy"])

## --- File System --- ##
# These handle files directly, and default to sd/, not sd/sdstore/

# sd.file.dir() returns sd root contents
# sd.file.dir("user") returns sd/user/ contents
# lets check the main storage files:
print(sd.file.dir("sdstore"))

# load file contents with sd.read(file*)
# like sd.read("book.txt") or sd.read("user/files/book.txt")

# sd.file.exists("book.txt") True if exists, False if not

# not everything autocreates directories.
# make your directory first, before attempting to save to it, like:
# sd.file.newdir("some/new/folders")

# sd.file.new("book.txt")
# sd.file.new("user/book.txt", "This one isn't blank.")

# sd.file.write("book.txt", "This is the beginning of my new book...")

# store_obj("group", group) - stores the dic to file as group.json

# group = load_obj("group") - loads group.json file back to a dic


