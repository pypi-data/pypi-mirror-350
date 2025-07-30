from typing_extensions import Literal, Any, Union, Dict
from toml import load, dump
from os import makedirs
from pathlib import Path

__version__ = "0.2.1"
__all__ = ["config", "get_config", "remove_config", "init", "initsettings",
           "LOCAL", "GLOBAL", "ALL", "HOME", "CWD"
        ]

initsettings = {}

LOCAL = "local"
GLOBAL = "global"
ALL = "all"

HOME = Path.home()
CWD = Path.cwd()

def init(**kwargs):
    global initsettings

    initsettings.update(kwargs)

def config(
    config_name: str,
    value: Any,
    config_type: Literal["local", "global"]=initsettings.get("default_config_type", LOCAL)
):
    local_config_path = initsettings.get("local_config_path", Path.home() / "appdata" / "Roaming" / "xystudio" / "configurer" / "config.toml")
    global_config_path = initsettings.get("global_config_path", Path.cwd() / ".xystudio" / "configurer" / "config.toml")

    create_config_file()

    if initsettings.get("must_two_texts", False):
        config_split = config_name.split(".", 1)
        config_char_1 = config_split[0]
        try:
            config_char_2 = config_split[1]
        except IndexError:
            raise ValueError("config name must with two texts, example : 'a.b'.")
        if config_type == LOCAL:
            with open(local_config_path, "r", encoding="utf-8") as f:
                config = load(f)
                config.update({config_char_1 : {config_char_2 : value}})
            with open(local_config_path, "w", encoding="utf-8") as f:
                dump(config, f)
        elif config_type == GLOBAL:
            with open(global_config_path, "r", encoding="utf-8") as f:
                config = load(f)
                config.update({config_char_1 : {config_char_2 : value}})
            with open(global_config_path, "w", encoding="utf-8") as f:
                dump(config, f)
        else:
            raise ValueError("This config type not found.")
    else:
        if config_type == LOCAL:
            with open(local_config_path, "r") as f:
                local_config = load(f)
            local_config[config_name] = value
            with open(local_config_path, "w") as f:
                dump(local_config, f)
        elif config_type == GLOBAL:
            with open(global_config_path, "r") as f:
                global_config = load(f)
            global_config[config_name] = value
            with open(global_config_path, "w") as f:
                dump(global_config, f)
        else:
            raise ValueError("Invalid config type.")

def get_config(config_name:str, default: Any=None, config_type: Literal["local", "global", "all"]=LOCAL) -> Any:
    global_config_path = Path(initsettings.get("global_config_path", Path.home() / ".xystudio" / "configurer"/ "config.toml"))
    local_config_path = Path(initsettings.get("local_config_path", Path.cwd() / ".xystudio" / "configurer" / "config.toml"))

    try:
        if initsettings.get("must_two_texts", False):
            config_split = config_name.split(".", 1)
            config_char_1 = config_split[0]
            try:
                config_char_2 = config_split[1]
            except IndexError:
                raise ValueError("config name must with two texts, example : 'a.b'.")
            if config_type == LOCAL:
                with open(local_config_path, "r") as f:
                    local_config = load(f)
                
                if config_name == ALL:
                    return local_config
                else:
                    if config_char_1 in local_config and config_char_2 in local_config[config_char_1]:
                        return local_config[config_char_1][config_char_2]
                    else:
                        return default
            elif config_type == GLOBAL:
                with open(global_config_path, "r") as f:
                    global_config = load(f)
                
                if config_name == ALL:
                    return global_config
                else:
                    if config_char_1 in global_config and config_char_2 in global_config[config_char_1]:
                        return global_config[config_char_1][config_char_2]
                    else:
                        return default
            elif config_type == ALL:
                with open(local_config_path, "r") as f:
                    local_config = load(f)
                with open(global_config_path, "r") as f:
                    global_config = load(f)
                union_config = {**local_config, **global_config}
                if config_name == ALL:
                    return union_config
                else:
                    if config_char_1 in union_config and config_char_2 in union_config[config_char_1]:
                        return union_config[config_char_1][config_char_2]
                    else:
                        return default
            else:
                raise ValueError("Invalid config type.")
        else:
            if config_type == LOCAL:
                with open(local_config_path, "r") as f:
                    local_config = load(f)
                if config_name in local_config:
                    return local_config[config_name]
                else:
                    return default
            elif config_type == GLOBAL:
                with open(global_config_path, "r") as f:
                    global_config = load(f)
                if config_name in global_config:
                    return global_config[config_name]
                else:
                    return default
            elif config_type == ALL:
                with open(local_config_path, "r") as f:
                    local_config = load(f)
                with open(global_config_path, "r") as f:
                    global_config = load(f)
                union_config = {**local_config, **global_config}
                if config_name in union_config:
                    return union_config[config_name]
                else:
                    return default
            else:
                raise ValueError("Invalid config type.")
    except FileNotFoundError:
        return default


def remove_config(
    config_name: str, config_type: Literal["local", "global"] = LOCAL
):
    global_config_path = Path(initsettings.get("global_config_path", Path.home() / ".xystudio" / "configurer" / "config.toml"))
    local_config_path = Path(initsettings.get("local_config_path", Path.cwd() / ".xystudio" / "configurer" / "config.toml"))

    if config_type == LOCAL:
        with open(local_config_path, "r") as f:
            local_config = load(f)
        if config_name in local_config:
            del local_config[config_name]
        with open(local_config_path, "w") as f:
            dump(local_config, f)
    elif config_type == GLOBAL:
        with open(global_config_path, "r") as f:
            global_config = load(f)
        if config_name in global_config:
            del global_config[config_name]
        with open(global_config_path, "w") as f:
            dump(global_config, f)
    else:
        raise ValueError("Invalid config type.")
    
def create_config_file():
    global_config_path = Path(initsettings.get("global_config_path", Path.home() / ".xystudio" / "configurer" / "config.toml"))
    local_config_path = Path(initsettings.get("local_config_path", Path.cwd() / ".xystudio" / "configurer" / "config.toml"))
 
    makedirs(global_config_path.parent, exist_ok=True)
    makedirs(local_config_path.parent, exist_ok=True)

    if not(local_config_path.exists()):
        local_config_path.touch()
    if not(global_config_path.exists()):
        global_config_path.touch()

__init__ = init

def _write_init_settings():
    with open(initsettings.get("local_config_path", Path.home() / ".xystudio" / "configurer" / "init_settings.xys"), "init_settings.xys", "w") as f:
        dump(initsettings, f)

def _read_init_settings():
    global initsettings
    try:
        with open(initsettings.get("local_config_path", Path.home() / ".xystudio" / "configurer" / "init_settings.xys"), "r") as f:
            initsettings = load(f)
    except FileNotFoundError:
        pass

def main():
    import argparse

    class globalAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            self.handle_output(parser, namespace, values)

        @staticmethod
        def handle_output(parser, namespace, values):
            setattr(namespace, "_global", values)

    class allAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            self.handle_output(parser, namespace, values)

        @staticmethod
        def handle_output(parser, namespace, values):
            setattr(namespace, "_all", values)

    class localAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            self.handle_output(parser, namespace, values)

        @staticmethod
        def handle_output(parser, namespace, values):
            setattr(namespace, "_local", values)

    parser = argparse.ArgumentParser(description="imgfit commands")
    subparsers = parser.add_subparsers(dest="command", required=False)

    _read_init_settings()

    init_cmd = subparsers.add_parser("init", help="Set the config")
    init_cmd.add_argument("setting")
    init_cmd.add_argument("value")

    set_cmd = subparsers.add_parser("set", help="Set the config")
    set_namespace = set_cmd.add_subparsers(dest="set_namespace", required=True)
    local_config_cmd = set_namespace.add_parser(
        "local",
        help="Config file only in your project.Local config in './.xystudio/pyplus/config.toml'",
    )
    global_config_cmd = set_namespace.add_parser(
        "global",
        help="Config file in all project.Global config in 'Users/Appdata/roaming/xystudio/pyplus/config.toml'",
    )

    local_config_cmd.add_argument("setting", help="Config setting.")
    local_config_cmd.add_argument("value", help="Config value.")

    global_config_cmd.add_argument("setting", help="Config setting.")
    global_config_cmd.add_argument("value", help="Config value.")

    get_conf = subparsers.add_parser("get", help="Get the config.")
    get_conf.add_argument(
        "-l",
        "--local",
        action=localAction,
        nargs="?",
        help="Get the local config in your project.Local config in './.xystudio/pyplus/config.toml'",
    )
    get_conf.add_argument(
        "-g",
        "--global",
        action=globalAction,
        nargs="?",
        help="Output the global config.",
    )
    get_conf.add_argument(
        "-a", "--all", nargs="?", action=allAction, help="Output all the config."
    )

    remove_namespace = subparsers.add_parser("remove", help="Remove the config").add_subparsers(dest="remove_namespace", required=True)
    local_config_cmd = remove_namespace.add_parser(
        "local",
        help="Config file only in your project.Local config in './.xystudio/pyplus/config.toml'",
    )
    global_config_cmd = remove_namespace.add_parser(
        "global",
        help="Config file in all project.Global config in 'Users/Appdata/roaming/xystudio/pyplus/config.toml'",
    )

    local_config_cmd.add_argument("setting", help="Config setting.")
    global_config_cmd.add_argument("setting", help="Config setting.")

    args = parser.parse_args()

    if args.config_command == "set":
        if args.value.lower() == "true":
            value = True
        elif args.value.lower() == "false":
            value = False
        else:
            value = args.value
        print("Run code again to set the config.")
        config(args.setting, value, args.set_namespace)
    elif args.config_command == "get":
        print(args)
        if hasattr(args, "_local"):
            if args._local is None:
                print(get_config(args.setting, namespace=LOCAL))
            else:
                print(args._local)
                print(get_config(args._local, namespace=LOCAL))
        if hasattr(args, "_global"):
                print(get_config(args.setting, namespace=GLOBAL))
        else:
            print(args._global)
            print(get_config(args._global, namespace=GLOBAL))
        if hasattr(args, "_all"):
            print(get_config(args.setting, namespace=ALL))
        else:
            print(args._all)
            print(get_config(args._all, namespace=ALL))
    elif args.config_command == "remove":
        remove_config(args.setting, args.remove_namespace)
    elif args.config_command == "init":
        initsettings[args.setting] = args.value

if __name__ == "__main__":
    main()