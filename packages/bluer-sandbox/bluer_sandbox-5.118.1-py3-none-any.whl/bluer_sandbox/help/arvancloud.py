from typing import List

from bluer_options.terminal import show_usage, xtra


def help_seed(
    tokens: List[str],
    mono: bool,
) -> str:
    options = xtra("screen", mono=mono)

    return show_usage(
        [
            "@arvan",
            "seed",
            f"[{options}]",
        ],
        "seed 🌱  arvancloud.",
        mono=mono,
    )


def help_set_ip(
    tokens: List[str],
    mono: bool,
) -> str:
    return show_usage(
        [
            "@arvan",
            "set_ip",
            "<ip-address>",
        ],
        "set arvancloud ip.",
        mono=mono,
    )


def help_ssh(
    tokens: List[str],
    mono: bool,
) -> str:
    options = xtra("dryrun,~seed", mono=mono)

    return show_usage(
        [
            "@arvan",
            "ssh",
            f"[{options}]",
        ],
        "ssh -> arvancloud.",
        mono=mono,
    )


help_functions = {
    "seed": help_seed,
    "set_ip": help_set_ip,
    "ssh": help_ssh,
}
