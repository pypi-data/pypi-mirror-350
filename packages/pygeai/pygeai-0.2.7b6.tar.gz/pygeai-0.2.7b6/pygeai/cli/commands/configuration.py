import sys

from pygeai.cli.commands import Option
from pygeai.core.common.config import get_settings
from pygeai.core.utils.console import Console


def configure(option_list: list[str, str] = None):
    if not any(option_list):
        Console.write_stdout("# Configuring GEAI credentials...")
        alias = str(input("-> Select an alias (Leave empty to use 'default'): "))
        if not alias:
            alias = "default"

        api_key = str(input("-> Insert your GEAI API KEY (Leave empty to keep current value): "))
        if api_key:
            configure_api_key(api_key, alias)

        base_url = str(input("-> Insert your GEAI API BASE URL (Leave empty to keep current value): "))
        if base_url:
            configure_base_url(base_url, alias)

        eval_url = str(input("-> Insert your GEAI API EVAL URL (Leave empty to keep current value): "))
        if eval_url:
            configure_eval_url(eval_url, alias)

    else:
        list_alias = None
        api_key = None
        base_url = None
        eval_url = None
        alias = "default"

        for option_flag, option_arg in option_list:
            if option_flag.name == "list":
                list_alias = True
            if option_flag.name == "alias":
                alias = option_arg
            if option_flag.name == "api_key":
                api_key = option_arg
            if option_flag.name == "base_url":
                base_url = option_arg
            if option_flag.name == "eval_url":
                eval_url = option_arg

        if list_alias:
            display_alias_list()
        else:
            if api_key:
                configure_api_key(api_key=api_key, alias=alias)
            if base_url:
                configure_base_url(base_url=base_url, alias=alias)
            if eval_url:
                configure_eval_url(eval_url=eval_url, alias=alias)


def configure_api_key(api_key: str, alias: str = "default"):
    settings = get_settings()
    settings.set_api_key(api_key, alias)
    Console.write_stdout(f"GEAI API KEY for alias '{alias}' saved successfully!")


def configure_base_url(base_url: str, alias: str = "default"):
    settings = get_settings()
    settings.set_base_url(base_url, alias)
    Console.write_stdout(f"GEAI API BASE URL for alias '{alias}' saved successfully!")


def configure_eval_url(eval_url: str, alias: str = "default"):
    settings = get_settings()
    settings.set_eval_url(eval_url, alias)
    Console.write_stdout(f"GEAI API EVAL URL for alias '{alias}' saved successfully!")


def display_alias_list():
    settings = get_settings()
    for alias, url in settings.list_aliases().items():
        Console.write_stdout(f"Alias: {alias} -> Base URL: {url}")


configuration_options = (
    Option(
        "api_key",
        ["--key", "-k"],
        "Set GEAI API KEY",
        True
    ),
    Option(
        "base_url",
        ["--url", "-u"],
        "Set GEAI API BASE URL",
        True
    ),
    Option(
        "eval_url",
        ["--eval-url", "--eu"],
        "Set GEAI API EVAL URL for the evaluation module",
        True
    ),
    Option(
        "alias",
        ["--alias", "-a"],
        "Set alias for settings section",
        True
    ),
    Option(
        "list",
        ["--list", "-l"],
        "List available alias",
        False
    ),
)
