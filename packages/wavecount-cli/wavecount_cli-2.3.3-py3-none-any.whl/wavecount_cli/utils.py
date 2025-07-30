import json
import os


root_dir = os.path.expanduser(os.path.join("~", ".wavecount_cli"))
filename = os.path.expanduser(root_dir + "/config.json")


def read_config():
    cfg = {}
    if not os.path.exists(filename):
        os.makedirs(root_dir, exist_ok=True)
        with open(filename, "w+") as cfg_file:
            json.dump(cfg, cfg_file, indent=4)
    else:
        with open(filename, "r") as cfg_file:
            cfg = json.load(cfg_file)
    return cfg


def save_config(cfg):
    with open(filename, "w") as cfg_file:
        return json.dump(cfg, cfg_file, indent=4)
