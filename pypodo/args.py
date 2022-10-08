"""
pypodo argparse gestion
"""

import argparse


class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ", ".join(action.option_strings) + " " + args_string

    def _format_args(self, action, default_metavar):
        get_metavar = self._metavar_formatter(action, default_metavar)
        if action.nargs == argparse.ONE_OR_MORE:
            return "%s" % get_metavar(1)
        else:
            return super(CustomHelpFormatter, self)._format_args(
                action, default_metavar
            )


def compute_args():
    """
    check args and return them
    """
    my_parser = argparse.ArgumentParser(
        description="pypodo is a todolist tool which works in your terminal. It has a mecanism of indexes and tags.",
        epilog="""
        Full documentation at: <https://github.com/thib1984/pypodo>.
        Report bugs to <https://github.com/thib1984/pypodo/issues>.
        MIT Licence.
        Copyright (c) 2021 thib1984.
        This is free software: you are free to change and redistribute it.
        There is NO WARRANTY, to the extent permitted by law.
        Written by thib1984.""",
        formatter_class=CustomHelpFormatter,
    )
    my_group = my_parser.add_mutually_exclusive_group()
    my_group.add_argument(
        "-a",
        "--add",
        action="store",
        nargs="+",
        type=str,
        metavar="ITEM ...",
        help="add ITEM(s) in the todolist",
    )
    my_group.add_argument(
        "-w",
        "--warning",
        action="store_true",
        help="print the todolist filtered with TAG(s) alert and warning",
    )    
    my_group.add_argument(
        "-d",
        "--delete",
        action="store",
        metavar="INDEX ...",
        nargs="+",
        type=str,
        help="delete item with the given INDEX(es)",

    )
    my_group.add_argument(
        "--tag",
        action="store",
        nargs="+",
        type=str,
        metavar="TAG INDEX ...",
        help="TAG item with the given INDEX(es)",
    )
    my_group.add_argument(
        "--untag",
        action="store",
        nargs="+",
        type=str,
        metavar="TAG INDEX ...",
        help="unTAG item with the given INDEX(es)",
    )
    my_parser.add_argument(
        "-f",
        "--filter",
        action="store",
        nargs="+",
        type=str,
        metavar="TAG ...",
        help="print the todolist filtered with TAG(s) given",
    )
    my_parser.add_argument(
        "-e",
        "--exclude",
        action="store",
        nargs="+",
        type=str,
        metavar="TAG ...",
        help="print the todolist with TAG(s) given excluden",
    )
    my_group.add_argument(
        "-o",
        "--order",
        action="store_true",
        help="order the todolist",
    )
    my_group.add_argument(
        "-b",
        "--backup",
        action="store_true",
        help="backup the todolist",
    )
    my_group.add_argument(
        "-s",
        "--search",
        action="store",
        type=str,
        metavar="REGEX",
        help="search in the todolist with the REGEX given",
    )

    my_group.add_argument(
        "--info",
        action="store_true",
        help="print the infos",
    )
    my_group.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="update pypodo",
    )

    my_parser.add_argument(
        "-n",
        "--nocolor",
        action="store_true",
        help="disable color in sysout",
    )

    my_parser.add_argument(
        "-c",
        "--condensate",
        action="store_true",
        help="condensate sysout",
    )

    my_parser.add_argument(
        "-D",
        "--day",
        action="store_true",
        help="add tag actual day",
    )

    my_parser.add_argument(
        "-W",
        "--week",
        action="store_true",
        help="add tag next week",
    )

    my_parser.add_argument(
        "-M",
        "--month",
        action="store_true",
        help="add tag next month",
    )

    my_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="verbose mode",
    )
    
    args = my_parser.parse_args()
    return args
