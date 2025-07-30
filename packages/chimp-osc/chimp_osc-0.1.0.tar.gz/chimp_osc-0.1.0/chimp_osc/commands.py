from enum import Enum


class Action(Enum):
    release = 0
    press = 1


class LED(Enum):
    led_off = 0
    led_on = 1


COMMANDS = {
    "fader": {
        "{nr}": {
            "go": Action,
            "pause": Action,
            "flash": Action,
            "value": int,
            "name": str,
        },
        "page": {"next": Action, "previous": Action, "template": Action, "name": str},
    },
    "master": {"{nr}": {"flash": Action, "value": int}},
    "executor": {
        "{nr}": {"flash": Action, "name": str},
        "page": {"next": Action, "previous": Action, "template": Action, "name": str},
    },
    "virtual_executor": {"{nr}": {"flash": Action, "name": str}},
    "programmer": {
        "keypad": {
            "record": Action,
            "edit": Action,
            "delete": Action,
            "copy": Action,
            "move": Action,
            "name": Action,
            "open": Action,
            "select": Action,
            "link": Action,
            "load": Action,
            "off": Action,
            "skip": Action,
            "goto": Action,
            "time": Action,
            "fixture": Action,
            "group": Action,
            "preset": Action,
            "cuelist": Action,
            "cue": Action,
            "effect": Action,
            "minus": Action,
            "plus": Action,
            "thru": Action,
            "full": Action,
            "at": Action,
            "fw_slash": Action,
            "backspace": Action,
            "0": Action,
            "1": Action,
            "2": Action,
            "3": Action,
            "4": Action,
            "5": Action,
            "6": Action,
            "7": Action,
            "8": Action,
            "9": Action,
            "dot": Action,
            "enter": Action,
            "shift": Action,
            "home": Action,
            "set": Action,
        },
        "blind": {"btn": Action, "led": LED},
        "highlight": {"btn": Action, "led": LED},
        "fan": {"btn": Action, "led": LED},
        "select": {
            "all_none": Action,
            "next": Action,
            "previous": Action,
            "even_odd": Action,
            "first_second_half": Action,
            "random": Action,
            "shuffle_selection": Action,
            "invert": Action,
        },
        "feature": {
            "select": {
                "intensity": Action,
                "position": Action,
                "color": Action,
                "gobo": Action,
                "beam": Action,
                "shaper": Action,
                "control": Action,
                "special": Action,
            }
        },
        "clear": {"btn": Action, "led": LED},
        "commandline": {"content": str, "error_led": LED},
        "encoder": {"{nr}": {"btn": Action, "inc": int, "text1": str, "text2": str}},
        "pan_tilt": float,
    },
    "use_accel": Action,
    "sync": Action,
}

TYPES: dict = {
    "nr": int,
}
