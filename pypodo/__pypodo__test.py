"""
Pypodo Tests
"""

import re
import os
import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from freezegun import freeze_time

from pypodo.__pypodo__ import (
    add,
    backup,
    delete,
    find,
    helppypodo,
    listnotag,
    listtag,
    listtask,
    pypodo,
    read_config,
    read_config_boolean,
    read_config_color,
    read_config_int,
    read_config_level,
    sort,
    tag,
    test_date,
    untag,
    generate_key_fernet,
)


class AnyStringWith(str):
    """
    Utilitary Class for contains string
    """

    def __eq__(self, other):
        """
        Test if string is in other
        """
        return self in other


sys.modules["shutil"] = MagicMock()

STR_PATH_HOME__TODO_ = str(Path.home()) + "/.todo"
STR_PATH_HOME__TODORC_ = str(Path.home()) + "/.todo.rc"
STR_PATH_HOME__TODO_BACKUP_FOLDER_ = (
    str(Path.home()) + "/.todo_backup/"
)


class TestMethodsEntryPoint(unittest.TestCase):
    """
    Class Test for entrypoints
    """

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="[SYSTEM]\nmessagelevel = debug",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_entry_point_crypt(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_pypodo_entry_point_crypt
        """
        with patch.object(sys, "argv", [pypodo, "crypt"]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : not crypt key",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="[SYSTEM]\nmessagelevel = debug",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_entry_point_decrypt(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        def test_pypodo_entry_point_decrypt
        """
        with patch.object(sys, "argv", [pypodo, "decrypt"]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : not decrypt key",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_entry_point_list(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_pypodo_entry_point_list
        """
        with patch.object(sys, "argv", [pypodo, "list"]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the todolist is empty",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_entry_point_add(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_pypodo_entry_point_add
        """
        with patch.object(sys, "argv", [pypodo, "add"]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 1 or more parameter is needed for pypodo add - tasks",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_entry_point_del(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_pypodo_entry_point_del
        """
        with patch.object(sys, "argv", [pypodo, "del"]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 1 or more parameter is needed for pypodo del "
                "- indexes to delete in numeric format",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_entry_point_sort(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_pypodo_entry_point_sort
        """
        with patch.object(sys, "argv", [pypodo, "sort"]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the todolist is empty - nothing to do",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_entry_point_untag(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_pypodo_entry_point_untag
        """
        with patch.object(sys, "argv", [pypodo, "untag", "tag"]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 0,2 or more parameters is needed for pypodo untag :"
                " the tag to delete and the indexes of the task whose tags"
                " to delete - nothing to list task without tags",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_entry_point_tag(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_pypodo_entry_point_tag
        """
        with patch.object(sys, "argv", [pypodo, "tag", "tag"]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 0,2 or more parameters is needed for pypodo tag"
                " : the tag to add and the indexes of the task whose tags"
                " to add - nothing to list tags of the todolist",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_entry_point_find(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_pypodo_entry_point_find
        """
        with patch.object(sys, "argv", [pypodo, "find"]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 1 parameter is needed for pypodo find",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_entry_point_backup(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_pypodo_entry_point_backup
        """
        with patch.object(sys, "argv", [pypodo, "backup", "bak"]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 0 parameter is needed for pypodo backup",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.print", autospec=True, side_effect=print)
    def test_pypodo_entry_point_help(
        self, mock_print, mock_open_file, mock_isfile, mock_stdout
    ):
        """
        test_pypodo_entry_point_help
        """
        with patch.object(sys, "argv", [pypodo, "help"]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            mock_print.assert_called_with(AnyStringWith("SYNOPSIS"))

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.print", autospec=True, side_effect=print)
    def test_pypodo_entry_point_bad_param(
        self, mock_print, mock_open_file, mock_isfile, mock_stdout
    ):
        """
        test_pypodo_entry_point_bad_param
        """
        with patch.object(sys, "argv", [pypodo, "param"]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            mock_print.assert_called_with(AnyStringWith("SYNOPSIS"))

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.print", autospec=True, side_effect=print)
    def test_pypodo_entry_point_no_param(
        self, mock_print, mock_open_file, mock_isfile, mock_stdout
    ):
        """
        def test_pypodo_entry_point_no_param
        """
        with patch.object(sys, "argv", [pypodo]):
            mock_isfile.return_value = True
            pypodo(mock_open_file)
            mock_print.assert_called_with(AnyStringWith("SYNOPSIS"))


class TestMethodsErrors(unittest.TestCase):
    """
    Class Test for Errors
    """

    # errors
    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_find_with_no_parameter_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_find_with_no_parameter_return_error
        """
        with patch.object(sys, "argv", [pypodo, find]):
            mock_isfile.return_value = True
            find(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 1 parameter is needed for pypodo find",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_find_with_two_parameters_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_find_with_two_parameters_return_error
        """
        with patch.object(sys, "argv", [pypodo, find, "one", "two"]):
            mock_isfile.return_value = True
            find(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 1 parameter is needed for pypodo find",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_with_no_parameter_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_add_with_no_parameter_return_error
        """
        with patch.object(sys, "argv", [pypodo, add]):
            mock_isfile.return_value = True
            add(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 1 or more parameter is needed for pypodo add"
                " - tasks",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_del_with_no_parameter_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_del_with_no_parameter_return_error
        """
        with patch.object(sys, "argv", [pypodo, delete]):
            mock_isfile.return_value = True
            delete(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 1 or more parameter is needed for pypodo del"
                " - indexes to delete in numeric format",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_sort_with_one_parameter_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_sort_with_one_parameter_return_error
        """
        with patch.object(sys, "argv", [pypodo, sort, "one"]):
            mock_isfile.return_value = True
            sort(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 0 parameter is needed for pypodo sort",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_sort_with_two_parameter_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_sort_with_two_parameter_return_error
        """
        with patch.object(sys, "argv", [pypodo, sort, "one", "two"]):
            mock_isfile.return_value = True
            sort(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 0 parameter is needed for pypodo sort",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_backup_with_one_parameter_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_backup_with_one_parameter_return_error
        """
        with patch.object(sys, "argv", [pypodo, backup, "one"]):
            mock_isfile.return_value = True
            backup(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 0 parameter is needed for pypodo backup",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_backup_with_two_parameters_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_backup_with_two_parameters_return_error
        """
        with patch.object(
            sys, "argv", [pypodo, backup, "one", "two"]
        ):
            mock_isfile.return_value = True
            backup(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 0 parameter is needed for pypodo backup",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_tag_with_one_parameter_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_tag_with_one_parameter_return_error
        """
        with patch.object(sys, "argv", [pypodo, tag, "one"]):
            mock_isfile.return_value = True
            tag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 0,2 or more parameters is needed for"
                " pypodo tag : the tag to add and the indexes of"
                " the task whose tags to add - nothing to list tags"
                " of the todolist",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_untag_with_one_parameter_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_untag_with_one_parameter_return_error
        """
        with patch.object(sys, "argv", [pypodo, untag, "param"]):
            mock_isfile.return_value = True
            untag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 0,2 or more parameters is needed for"
                " pypodo untag : the tag to delete and the indexes"
                " of the task whose tags to delete - nothing to"
                " list task without tags",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_notag_with_no_parameter_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_notag_with_no_parameter_return_error
        """
        with patch.object(sys, "argv", [pypodo, untag, "param"]):
            mock_isfile.return_value = True
            listnotag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 0 parameter is needed for pypodo listnotag",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_listtag_with_no_parameter_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_listtag_with_no_parameter_return_error
        """
        with patch.object(sys, "argv", [pypodo, untag, "param"]):
            mock_isfile.return_value = True
            listtag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : 0 parameter is needed for pypodo listtag",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="1 task"
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_tag_beginning_with_hash_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_tag_beginning_with_hash_return_error
        """
        with patch.object(sys, "argv", [pypodo, tag, "#badtag", "1"]):
            mock_isfile.return_value = True
            tag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : the tag has not a valid format - #badtag",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="1 task"
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_tag_containing_hash_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_tag_containing_hash_return_error
        """
        with patch.object(sys, "argv", [pypodo, tag, "bad#tag", "1"]):
            mock_isfile.return_value = True
            tag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : the tag has not a valid format - bad#tag",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="1 task"
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_tag_finishing_with_hash_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_tag_finishing_with_hash_return_error
        """
        with patch.object(sys, "argv", [pypodo, tag, "badtag#", "1"]):
            mock_isfile.return_value = True
            tag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : the tag has not a valid format - badtag#",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="1 task"
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_untag_beginning_with_hash_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_untag_beginning_with_hash_return_error
        """
        with patch.object(
            sys, "argv", [pypodo, untag, "#badtag", "1"]
        ):
            mock_isfile.return_value = True
            untag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : the tag has not a valid format - #badtag",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="1 task"
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_untag_containing_hash_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_untag_containing_hash_return_error
        """
        with patch.object(
            sys, "argv", [pypodo, untag, "bad#tag", "1"]
        ):
            mock_isfile.return_value = True
            tag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : the tag has not a valid format - bad#tag",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="1 task"
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_untag_finishing_with_hash_return_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_untag_finishing_with_hash_return_error
        """
        with patch.object(
            sys, "argv", [pypodo, untag, "badtag#", "1"]
        ):
            mock_isfile.return_value = True
            tag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "error   : the tag has not a valid format - badtag#",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 my task #te#st\na other task",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_sort_with_invalid_todo_return_warning_and_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_sort_with_invalid_todo_return_warning_and_error
        """
        with patch.object(sys, "argv", [pypodo, listtask]):
            mock_isfile.return_value = True
            try:
                error = False
                listtask(mock_open_file)
            except SystemExit:
                self.assertEqual(
                    escape_ansi(mock_print.getvalue().rstrip("\n")),
                    "warning : this line has not a valid format in .todo"
                    " - 1 my task #te#st\nwarning : this line has not a"
                    " valid format in .todo - a other task\nerror   :"
                    " verify the .todo file. Is it encrypted?",
                )
                error = True
            self.assertEqual(error, True)

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 my task te#st\na other task",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_sort_with_other_invalid_todo_return_warning_and_error(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_sort_with_other_invalid_todo_return_warning_and_error
        """
        with patch.object(sys, "argv", [pypodo, listtask]):
            mock_isfile.return_value = True
            try:
                error = False
                listtask(mock_open_file)
            except SystemExit:
                self.assertEqual(
                    escape_ansi(mock_print.getvalue().rstrip("\n")),
                    "warning : this line has not a"
                    " valid format in .todo - a other task\nerror   :"
                    " verify the .todo file. Is it encrypted?",
                )
                error = True
            self.assertEqual(error, True)


class TestMethodsWarnings(unittest.TestCase):
    """
    Class Test for Warnings
    """

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="[SYSTEM]\nmessagelevel = debug\ntodofile = /tmp/.todo",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_crypt_with_not_todofile(
        self, mock_print, mock_open_file
    ):
        """
        test_pypodo_crypt_with_not_todofile
        """
        with patch.object(sys, "argv", [pypodo, "crypt", "password"]):
            if os.path.isfile("/tmp/.todo"):
                os.remove("/tmp/.todo")
            pypodo()
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "debug   : fernet password - password"
                "\ndebug   : fernet key - NWY0ZGNjM2I1YWE3NjVkNjFkODMyN2RlYjg4MmNmOTk="
                "\nerror   : not .todo file",
            )

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="[SYSTEM]\nmessagelevel = debug\ntodofile = /tmp/.todo\nkey = password",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_list_with_key_and_not_todofile(
        self, mock_print, mock_open_file
    ):
        """
        test_pypodo_list_with_key_and_not_todofile
        """
        with patch.object(sys, "argv", [pypodo, "list"]):
            if os.path.isfile("/tmp/.todo"):
                os.remove("/tmp/.todo")
            try:
                error = False
                pypodo()
            # FIXME ResourceWarning: unclosed file patch for error in test
            except TypeError:
                self.assertEqual(
                    escape_ansi(mock_print.getvalue().rstrip("\n")),
                    "debug   : fernet password - password"
                    "\ndebug   : fernet key - NWY0ZGNjM2I1YWE3NjVkNjFkODMyN2RlYjg4MmNmOTk="
                    "\ndebug   : creating .todolist file\ninfo    : creating .todolist file"
                    "\nwarning : the todolist is empty\ndebug   : fernet password - password"
                    "\ndebug   : fernet key - NWY0ZGNjM2I1YWE3NjVkNjFkODMyN2RlYjg4MmNmOTk=",
                )
                error = True
            self.assertEqual(error, True)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="[SYSTEM]\nmessagelevel = debug\ntodofile = /tmp/.todo",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_pypodo_decrypt_with_not_todofile(
        self, mock_print, mock_open_file
    ):
        """
        test_pypodo_decrypt_with_not_todofile
        """
        with patch.object(
            sys, "argv", [pypodo, "decrypt", "password"]
        ):
            if os.path.isfile("/tmp/.todo"):
                os.remove("/tmp/.todo")
            pypodo()
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "debug   : fernet password - password"
                "\ndebug   : fernet key - NWY0ZGNjM2I1YWE3NjVkNjFkODMyN2RlYjg4MmNmOTk="
                "\nerror   : not .todo file",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_sort_with_empty_todofile(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_sort_with_empty_todofile
        """
        with patch.object(sys, "argv", [pypodo, sort]):
            mock_isfile.return_value = True
            sort(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the todolist is empty - nothing to do",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_tag_with_no_numeric_value_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_tag_with_no_numeric_value_return_warning
        """
        with patch.object(sys, "argv", [pypodo, tag, "param", "a"]):
            mock_isfile.return_value = True
            tag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the index to tag is not in numeric format - a",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_untag_with_no_numeric_value_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_untag_with_no_numeric_value_return_warning
        """
        with patch.object(sys, "argv", [pypodo, untag, "param", "a"]):
            mock_isfile.return_value = True
            untag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the index to untag is not in numeric format - a",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_with_no_numeric_value_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_delete_with_no_numeric_value_return_warning
        """
        with patch.object(sys, "argv", [pypodo, delete, "a"]):
            mock_isfile.return_value = True
            delete(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the index to delete is not in numeric format - a",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="1 task"
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_with_inexistant_numeric_value_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_delete_with_inexistant_numeric_value_return_warning
        """
        with patch.object(sys, "argv", [pypodo, delete, "2"]):
            mock_isfile.return_value = True
            delete(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : no task is deleted from the todolist,"
                " not existing index - 2",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="1 task"
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_tag_with_inexistant_numeric_value_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_tag_with_inexistant_numeric_value_return_warning
        """
        with patch.object(sys, "argv", [pypodo, tag, "tag", "2"]):
            mock_isfile.return_value = True
            tag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : no task with index - 2",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="1 task"
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_untag_with_inexistant_numeric_value_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_untag_with_inexistant_numeric_value_return_warning
        """
        with patch.object(sys, "argv", [pypodo, untag, "tag", "2"]):
            mock_isfile.return_value = True
            untag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : no task with index - 2",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="1 task"
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_listtag_with_empty_result_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_listtag_with_empty_result_return_warning
        """
        with patch.object(sys, "argv", [pypodo, tag]):
            mock_isfile.return_value = True
            tag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the list of todolist's tags is empty",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task #tag",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_listnottag_with_empty_result_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_listnottag_with_empty_result_return_warning
        """
        with patch.object(sys, "argv", [pypodo, untag]):
            mock_isfile.return_value = True
            untag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the filtered todolist with no tag is empty",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_with_empty_todofile_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_list_with_empty_todofile_return_warning
        """
        with patch.object(sys, "argv", [pypodo, listtask]):
            mock_isfile.return_value = True
            listtask(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the todolist is empty",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task #tag1\n2 task #tag2\n3 task #tag\n4 task",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_with_filter_and_empty_result_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_list_with_filter_and_empty_result_return_warning
        """
        with patch.object(
            sys, "argv", [pypodo, listtask, "tag1", "tag2"]
        ):
            mock_isfile.return_value = True
            listtask(mock_open_file)
            # FIXME how test?
            # mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the filtered todolist is empty",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_task_begining_with_hash_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_add_task_begining_with_hash_return_warning
        """
        with patch.object(sys, "argv", [pypodo, add, "#task"]):
            mock_isfile.return_value = True
            add(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the task has not a valid format - #task",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_task_begining_with_hash_and_with_tag_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_add_task_begining_with_hash_and_with_tag_return_warning
        """
        with patch.object(sys, "argv", [pypodo, add, "#task #task"]):
            mock_isfile.return_value = True
            add(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the task has not a valid format - #task #task",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_task_with_empty_hash_and_with_tag_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_add_task_with_empty_hash_and_with_tag_return_warning
        """
        with patch.object(sys, "argv", [pypodo, add, "task # #task"]):
            mock_isfile.return_value = True
            add(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the task has not a valid format - task # #task",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_task_containing_hash_and_return_no_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        def test_add_task_containing_hash_and_return_no_warning
        """
        with patch.object(
            sys, "argv", [pypodo, add, "task#task #task"]
        ):
            mock_isfile.return_value = True
            add(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : task is added to the todolist - 1 task#task #task",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_find_if_empty_result_return_warning(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_find_if_empty_result_return_warning
        """
        with patch.object(sys, "argv", [pypodo, find, "string"]):
            mock_isfile.return_value = True
            find(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "warning : the filtered todolist is empty",
            )


class TestMethodsTools(unittest.TestCase):
    """
    Class Test for Tools
    """

    @freeze_time("2020-10-14")
    @patch(
        "builtins.open",
        new_callable=mock_open,
    )
    def test_date_without_onfig(self, mock_open_file):
        """
        test_date_without_onfig
        """
        self.assertEqual("ok", test_date("20210101"))
        self.assertEqual("alert", test_date("20201009"))
        self.assertEqual("warning", test_date("20201020"))

    @freeze_time("2020-10-14")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="[SYSTEM]\nformatdate = %%Y%%d%%m",
    )
    def test_date_with_config(self, mock_open_file):
        """
        test_date_with_config
        """
        self.assertEqual("ok", test_date("20210101"))
        self.assertEqual("alert", test_date("20200910"))
        self.assertEqual("warning", test_date("20202010"))

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="[COLOR]\nalert =red\nwarning=blue\ninfo=bad",
    )
    def test_color_with_config(self, mock_open_file):
        """
        test_color_with_config
        """
        # read_config
        self.assertEqual("red", read_config("COLOR", "error", "red"))
        self.assertEqual("red", read_config("COLOR", "alert", "red"))
        self.assertEqual(
            "blue", read_config("COLOR", "warning", "yellow")
        )
        self.assertEqual("bad", read_config("COLOR", "info", "green"))

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="[COLOR]\nalert =red\nwarning=blue\ninfo=bad",
    )
    def test_color_with_other_config(self, mock_open_file):
        """
        test_color_with_other_config
        """
        # read_config_color
        self.assertEqual(
            "red", read_config_color("COLOR", "error", "red")
        )
        self.assertEqual(
            "red", read_config_color("COLOR", "alert", "red")
        )
        self.assertEqual(
            "blue", read_config_color("COLOR", "warning", "yellow")
        )
        self.assertEqual(
            "green", read_config_color("COLOR", "info", "green")
        )

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="[FONCTIONAL]\nperiodwarning = bad\nperiodalert = 1\nperiodinfo = -1",
    )
    def test_period_without_config(self, mock_open_file):
        """
        test_period_without_config
        """
        # read_config_int
        self.assertEqual(
            "1", read_config_int("FONCTIONAL", "periodalert", "0")
        )
        self.assertEqual(
            "7", read_config_int("FONCTIONAL", "periodwarning", "7")
        )
        self.assertEqual(
            "10", read_config_int("FONCTIONAL", "periodinfo", "10")
        )

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="[SYSTEM]\nlevel = error\nlevel2 = warning\nlevel3 = bad",
    )
    def test_period_with_config(self, mock_open_file):
        """
        test_period_with_config
        """
        # read_config_level
        self.assertEqual(
            "error", read_config_level("SYSTEM", "level", "error")
        )
        self.assertEqual(
            "warning", read_config_level("SYSTEM", "level2", "error")
        )
        self.assertEqual(
            "error", read_config_level("SYSTEM", "level3", "error")
        )

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="[FONCTIONAL]\nmybool = False\nmybool2 = bad",
    )
    def test_boolean_with_config(self, mock_open_file):
        """
        test_read_config_boolean
        """
        # read_config_boolean
        self.assertEqual(
            "False",
            read_config_boolean("FONCTIONAL", "mybool", "True"),
        )
        self.assertEqual(
            "True",
            read_config_boolean("FONCTIONAL", "mybool2", "True"),
        )


class TestMethodsOthers(unittest.TestCase):
    """
    Class Test for other
    """

    @patch("time.strftime")
    @patch("pypodo.__pypodo__.copyfile")
    @patch("os.path.isfile")
    @patch("os.makedirs")
    @patch("os.path.exists", autospec=True)
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_backup_create_file_with_good_sufix_and_good_content(
        self,
        mock_print,
        mock_open_file,
        mock_path_exists,
        mock_makedirs,
        mock_isfile,
        mock_copyfile,
        mock_strftime,
    ):
        """
        test_backup_create_file_with_good_sufix_and_good_content
        """
        with patch.object(sys, "argv", [pypodo, backup]):
            mock_isfile.return_value = True
            mock_path_exists.return_value = False
            mock_strftime.return_value = "_sufix_date"
            backup(mock_open_file)
            mock_path_exists.assert_called_with(
                STR_PATH_HOME__TODO_BACKUP_FOLDER_
            )
            mock_makedirs.assert_called_with(
                STR_PATH_HOME__TODO_BACKUP_FOLDER_
            )
            mock_copyfile.assert_called_with(
                STR_PATH_HOME__TODO_,
                STR_PATH_HOME__TODO_BACKUP_FOLDER_
                + ".todo_sufix_date",
            )
            self.assertIn(
                "info    : creating todolist backup folder",
                escape_ansi(mock_print.getvalue().rstrip("\n")),
            )
            self.assertIn(
                "creating todolist backup - .todo_sufix_date",
                escape_ansi(mock_print.getvalue().rstrip("\n")),
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="2 task one #test\n4 task two",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_sort_reorganize_index(
        self, mock_sysout, mock_open_file, mock_isfile
    ):
        """
        test_sort_reorganize_index
        """
        with patch.object(sys, "argv", [pypodo, sort]):
            mock_isfile.return_value = True
            sort(mock_open_file)
            mock_open_file().write.assert_called_with("2 task two")

    @patch("os.path.isfile")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="1 task"
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_print_one_task_if_one_task_in_todofile(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_list_print_one_task_if_one_task_in_todofile
        """
        with patch.object(sys, "argv", [pypodo, listtask]):
            mock_isfile.return_value = True
            listtask(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "1 task",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 t#urgentask# #tag1 #tag2",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_print_one_task_with_tags_if_one_task_in_todofile(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_list_print_one_task_with_tags_if_one_task_in_todofile
        """
        with patch.object(sys, "argv", [pypodo, listtask]):
            mock_isfile.return_value = True
            listtask(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "1 t#urgentask# #tag1 #tag2",
            )

    @freeze_time("2020-10-14")
    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task #urgent #20201010 #20201015 #20201022 #tag",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_print_one_task_with_specific_tags_if_one_task_in_todofile(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_list_print_one_task_with_specific_tags_if_one_task_in_todofile
        """
        with patch.object(sys, "argv", [pypodo, listtask]):
            mock_isfile.return_value = True
            listtask(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "1 task #urgent #20201010 #20201015 #20201022 #tag",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task1 #tag\n2 task2 #tag2\n3 task3#tag #tag3",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_with_filter_return_result(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_list_with_filter_return_result
        """
        with patch.object(sys, "argv", [pypodo, listtask, "tag"]):
            mock_isfile.return_value = True
            listtask(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "1 task1 #tag",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task #tag1\n2 task2 tache #tag2\n3 task3 #tag1 #tag2\n4 ma 4 task4 #tag3",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_with_double_filter_return_result_with_combinate(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_list_with_double_filter_return_result_with_combinate
        """
        with patch.object(
            sys, "argv", [pypodo, listtask, "tag1", "tag2"]
        ):
            mock_isfile.return_value = True
            listtask(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "3 task3 #tag1 #tag2",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_multi_task(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_add_multi_task
        """
        with patch.object(
            sys, "argv", [pypodo, add, "task1", "task2"]
        ):
            mock_isfile.return_value = True
            add(mock_open_file)
            mock_open_file().write.assert_called_with("2 task2\n")
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : task is added to the todolist - 1 task1\n"
                "info    : task is added to the todolist - 2 task2",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task1\n4 task2",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_task_with_no_empty_todolist(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_add_task_with_no_empty_todolist
        """
        with patch.object(sys, "argv", [pypodo, add, "task3"]):
            mock_isfile.return_value = True
            add(mock_open_file)
            # mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'a')
            mock_open_file().write.assert_called_once_with(
                "5 task3\n"
            )
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : task is added to the todolist - 5 task3",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task1 #tag\n2 task2\n4 task3",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_one_task(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_delete_one_task
        """
        with patch.object(sys, "argv", [pypodo, delete, "2"]):
            mock_isfile.return_value = True
            delete(mock_open_file)
            mock_open_file().write.assert_called_with("4 task3")
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : task deleted from the todolist - 2 task2",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task1 #tag\n2 task2\n4 task3",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_multi_task(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_delete_multi_task
        """
        with patch.object(sys, "argv", [pypodo, delete, "2", "1"]):
            mock_isfile.return_value = True
            delete(mock_open_file)
            mock_open_file().write.assert_called_with("4 task3")
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : task deleted from the todolist - 2 task2"
                "\ninfo    : task deleted from the todolist - 1 task1 #tag",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task1 #tag\n2 task2\n4 task3",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_multi_task_with_minus(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_delete_multi_task_with_min
        """
        with patch.object(
            sys, "argv", [pypodo, delete, "1-3", "2-2", "4-3"]
        ):
            mock_isfile.return_value = True
            delete(mock_open_file)

            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : task deleted from the todolist - 1 task1 #tag"
                "\ninfo    : task deleted from the todolist - 2 task2"
                "\nwarning : no task is deleted from the todolist, not existing index - 3"
                "\nwarning : the index to delete is not in numeric format - 2-2"
                "\nwarning : the index to delete is not in numeric format - 4-3",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task1 #tag\n2 task2\n4 task3\n5 task5\n6 task6\n7 task7\n8 task8\n9 task9\n10 task10",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_other_multi_task_with_minus(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_delete_multi_task_with_min
        """
        with patch.object(sys, "argv", [pypodo, delete, "6-9"]):
            mock_isfile.return_value = True
            delete(mock_open_file)

            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : task deleted from the todolist - 6 task6"
                "\ninfo    : task deleted from the todolist - 7 task7"
                "\ninfo    : task deleted from the todolist - 8 task8"
                "\ninfo    : task deleted from the todolist - 9 task9",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task #tag2\n2 task2 #tag #tag3",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_untag_one_task(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_untag_one_task
        """
        with patch.object(sys, "argv", [pypodo, untag, "tag", "2"]):
            mock_isfile.return_value = True
            untag(mock_open_file)
            mock_open_file().write.assert_called_with(
                "2 task2 #tag3\n"
            )
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : tag deleted from the task of the todolist"
                " - 2 task2 #tag #tag3 -> 2 task2 #tag3",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task#tag #tag2\n2 task#tag2 #tag #tag3",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_untag_other_one_task(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_untag_one_task
        """
        with patch.object(sys, "argv", [pypodo, untag, "tag", "2"]):
            mock_isfile.return_value = True
            untag(mock_open_file)
            mock_open_file().write.assert_called_with(
                "2 task#tag2 #tag3\n"
            )
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : tag deleted from the task of the todolist"
                " - 2 task#tag2 #tag #tag3 -> 2 task#tag2 #tag3",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 ma tache #test #toto\n2 ma seconde tache #tost"
        " #titi\n3 ma seconde tache #test #titi",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_untag_multi_task(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_untag_multi_task
        """
        with patch.object(
            sys, "argv", [pypodo, untag, "test", "1", "2", "3"]
        ):
            mock_isfile.return_value = True
            untag(mock_open_file)
            # mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'w')
            mock_open_file().write.assert_called_with(
                "3 ma seconde tache #titi\n"
            )
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : tag deleted from the task of the todolist"
                " - 1 ma tache #test #toto -> 1 ma tache #toto\n"
                "warning : no tags is deleted from the todolist for the task"
                " - 2 ma seconde tache #tost #titi\ninfo    : tag deleted"
                " from the task of the todolist - 3 ma seconde tache"
                " #test #titi -> 3 ma seconde tache #titi",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task1 #tag\n3 task3 #tag\n4 task4 #tag",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_untag_multi_task_with_minus(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_untag_multi_task_with_min
        """
        with patch.object(
            sys, "argv", [pypodo, untag, "tag", "1-3", "2-2", "4-3"]
        ):
            mock_isfile.return_value = True
            untag(mock_open_file)

            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : tag deleted from the task of the todolist"
                " - 1 task1 #tag -> 1 task1"
                "\nwarning : no task with index - 2"
                "\ninfo    : tag deleted from the task of the todolist"
                " - 3 task3 #tag -> 3 task3"
                "\nwarning : the index to untag is not in numeric format - 2-2"
                "\nwarning : the index to untag is not in numeric format - 4-3",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task1 #tagone\n3 task3 #tagtwo\n4 task4 #tagthree",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_tag_multi_task_with_minus(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_tag_multi_task_with_min
        """
        with patch.object(
            sys, "argv", [pypodo, tag, "newtag", "1-3", "2-2", "4-3"]
        ):
            mock_isfile.return_value = True
            tag(mock_open_file)

            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : tag added to the task of the todolist"
                " - 1 task1 #tagone -> 1 task1 #tagone #newtag"
                "\nwarning : no task with index - 2"
                "\ninfo    : tag added to the task of the todolist"
                " - 3 task3 #tagtwo -> 3 task3 #tagtwo #newtag"
                "\nwarning : the index to tag is not in numeric format - 2-2"
                "\nwarning : the index to tag is not in numeric format - 4-3",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task1\n2 task2 #tag1",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_tag_one_task(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_tag_one_task
        """
        with patch.object(sys, "argv", [pypodo, tag, "tag2", "2"]):
            mock_isfile.return_value = True
            tag(mock_open_file)
            mock_open_file().write.assert_called_with(
                "2 task2 #tag1 #tag2\n"
            )
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : tag added to the task of the todolist"
                " - 2 task2 #tag1 -> 2 task2 #tag1 #tag2",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task1\n2 task2 #tag1\n3 task3 #tag2",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_tag_multi_task(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_tag_multi_task
        """
        with patch.object(
            sys, "argv", [pypodo, tag, "tag3", "2", "3"]
        ):
            mock_isfile.return_value = True
            tag(mock_open_file)
            mock_open_file().write.assert_called_with(
                "3 task3 #tag2 #tag3\n"
            )
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : tag added to the task of the todolist"
                " - 2 task2 #tag1 -> 2 task2 #tag1 #tag3\n"
                "info    : tag added to the task of the todolist"
                " - 3 task3 #tag2 -> 3 task3 #tag2 #tag3",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task1 #tag\n2 task2\n3 task3\n",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_list_notag_return_result(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_list_notag_return_result
        """
        with patch.object(sys, "argv", [pypodo, untag]):
            mock_isfile.return_value = True
            untag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "2 task2\n3 task3",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 ta#urgentsk #tag\n2 task2 #tag\n3 task3 #tag2\n4 task4",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_listtag_return_other_result(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_listtag_return_result
        """
        with patch.object(sys, "argv", [pypodo, tag]):
            mock_isfile.return_value = True
            tag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "#tag\n" + "#tag2",
            )

    @freeze_time("2020-10-14")
    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task #urgent\n2 task2 #20190101"
        "\n3 task3 #20201020\n4 task4 #tag",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_listtag_with_specific_tags_return_result(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_listtag_with_specific_tags_return_result
        """
        with patch.object(sys, "argv", [pypodo, tag]):
            mock_isfile.return_value = True
            tag(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "#20190101\n#urgent\n#20201020\n#tag",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task #tag\n2 specif_task #tag2\n3 specif",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_find_one_task_without_regex(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_find_one_task_without_regex
        """
        with patch.object(sys, "argv", [pypodo, find, "specif_task"]):
            mock_isfile.return_value = True
            find(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "2 specif_task #tag2",
            )

    @patch("os.path.isfile")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="1 task #lix\n2 task2 #tag\n3 task3 #linux",
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_find_with_regex(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_find_with_regex
        """
        with patch.object(sys, "argv", [pypodo, find, "li.+x"]):
            mock_isfile.return_value = True
            find(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "3 task3 #linux",
            )

    @patch("os.path.isfile")
    @patch("builtins.open", new_callable=mock_open)
    @patch("sys.stdout", new_callable=StringIO)
    def test_find_with_regex_no_result(
        self, mock_print, mock_open_file, mock_isfile
    ):
        """
        test_find_with_regex_no_result
        """
        mock_isfile.return_value = False
        with patch.object(sys, "argv", [pypodo, find, "li.+x"]):
            find(mock_open_file)
            self.assertEqual(
                escape_ansi(mock_print.getvalue().rstrip("\n")),
                "info    : creating .todolist file\nwarning :"
                " the filtered todolist is empty",
            )

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.print", autospec=True, side_effect=print)
    def test_help_contains_synopsis(self, mock_print, mock_stdout):
        """
        test_help_contains_synopsis
        """
        helppypodo()
        mock_print.assert_called_with(AnyStringWith("SYNOPSIS"))

    def test_generate_key_fernet(self):
        """
        test key generators
        """
        self.assertEqual(
            generate_key_fernet("password"),
            "NWY0ZGNjM2I1YWE3NjVkNjFkODMyN2RlYjg4MmNmOTk=",
        )


def escape_ansi(line):
    """
    escape_colors_from_string
    """
    ansi_escape = re.compile(
        r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]"
    )
    return ansi_escape.sub("", line)


if __name__ == "__main__":
    unittest.main()
