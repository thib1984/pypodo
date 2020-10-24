from pypodo.__pypodo__ import add, delete, list, help, pypodo, sort, tag, untag, backup, find, test_date, read_config_boolean, read_config, read_config_level, read_config_int,  read_config_color
import re
import sys
import unittest
from datetime import datetime
from datetime import date
from io import StringIO
from pathlib import Path
from unittest.mock import mock_open, patch, MagicMock
from freezegun import freeze_time
import configparser

sys.modules['shutil'] = MagicMock()

STR_PATH_HOME__TODO_ = str(Path.home()) + '/.todo'
STR_PATH_HOME__TODORC_ = str(Path.home()) + '/.todo.rc'
STR_PATH_HOME__TODO_BACKUP_FOLDER_ = str(Path.home()) + '/.todo_backup/'


class TestStringMethods(unittest.TestCase):

    # errors
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache #test\n3 ma seconde tache #linux')
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_no_parameter_return_error(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, find]):
            mock_isfile.return_value = True
            find(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), "error   : 1 parameter is needed for pypodo find")

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_no_parameter_return_error(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, add]):
            mock_isfile.return_value = True
            add(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), 'error   : 1 or more parameter is needed for pypodo add - tasks')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_del_no_parameter_return_error(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, delete]):
            mock_isfile.return_value = True
            delete(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), 'error   : 1 or more parameter is needed for pypodo del - indexes to delete in numeric format')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_sort_with_parameters_return_error(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, sort, "toto"]):
            mock_isfile.return_value = True
            sort(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), "error   : 0 parameter is needed for pypodo sort")

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_backup_with_parameters_return_error(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, backup, "toto"]):
            mock_isfile.return_value = True
            backup(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), "error   : 0 parameter is needed for pypodo backup")

    @patch('time.strftime')
    @patch('pypodo.__pypodo__.copyfile')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('os.path.exists', autospec=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_backup(self, mock_print, mock_open, mock_path_exists, mock_makedirs, mock_isfile, mock_copyfile, mock_strftime):
        with patch.object(sys, 'argv', [pypodo, backup]):
            mock_isfile.return_value = True
            mock_path_exists.return_value = False
            mock_strftime.return_value = '1'
            backup(mock_open)
            mock_path_exists.assert_called_with(
                STR_PATH_HOME__TODO_BACKUP_FOLDER_)
            mock_makedirs.assert_called_with(
                STR_PATH_HOME__TODO_BACKUP_FOLDER_)
            mock_copyfile.assert_called_with(
                STR_PATH_HOME__TODO_, STR_PATH_HOME__TODO_BACKUP_FOLDER_ + '.todo1')
            self.assertIn("info    : creating todolist backup folder", escape_ansi(mock_print.getvalue().rstrip(
                '\n')))
            self.assertIn("creating todolist backup - .todo1", escape_ansi(mock_print.getvalue().rstrip(
                '\n')))

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_sort_if_todo_empty(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, sort]):
            mock_isfile.return_value = True
            sort(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), "warning : the todolist is empty - nothing to do")

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='2 ma tache #test\n4 ma seconde tache')
    def test_sort_if_todo_with_tasks(self, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, sort]):
            mock_isfile.return_value = True
            sort(mock_open)
            mock_open().write.assert_called_with('2 ma seconde tache')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #te#st\na ma seconde tache\n3 ma seconde tache')
    @patch('sys.stdout', new_callable=StringIO)
    def test_sort_if_todo_with_invalids_tasks(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, list]):
            mock_isfile.return_value = True
            list(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), "warning : this line has not a valid format in .todo - 1 ma tache #te#st\nwarning : this line has not a valid format in .todo - a ma seconde tache\nerror   : verify the .todo file")

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_if_todo_empty(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, list]):
            mock_isfile.return_value = True
            list(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), "warning : the todolist is empty")

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_if_todo_one_task(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, list]):
            mock_isfile.return_value = True
            list(mock_open)
            #mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(
                mock_print.getvalue().rstrip('\n')), '1 ma tache')

    @freeze_time("2020-10-14")
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #urgent #20201010 #20201015 #20201022')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_if_todo_one_task_and_tags(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, list]):
            mock_isfile.return_value = True
            list(mock_open)
            #mock_open.assert_called_with(STR_PATH_HOME__TODORC_, encoding=None)
            #mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(
                mock_print.getvalue().rstrip('\n')), '1 ma tache #urgent #20201010 #20201015 #20201022')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_with_filter_one_task(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, list, 'test']):
            mock_isfile.return_value = True
            list(mock_open)
            #mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(
                mock_print.getvalue().rstrip('\n')), '1 ma tache #test')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache #linux\n3 ma troisieme tache #linux #test\n4 ma 4 tache #toto')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_with_double_filter_one_task(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, list, 'test', 'linux']):
            mock_isfile.return_value = True
            list(mock_open)
            #mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(
                mock_print.getvalue().rstrip('\n')), '3 ma troisieme tache #linux #test')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache #linux\n3 ma troisieme tache #linux #test\n4 ma 4 tache #toto')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_with_double_filter_one_task_return_empty(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, list, 'test', 'pe']):
            mock_isfile.return_value = True
            list(mock_open)
            #mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(
                mock_print.getvalue().rstrip('\n')), 'warning : the filtered todolist is empty')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_task_not_valid_format(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, add, '#pe']):
            mock_isfile.return_value = True
            add(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), 'warning : the task has not a valid format - #pe')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_task_todolist_empty(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, add, 'task3']):
            mock_isfile.return_value = True
            add(mock_open)
            #ock_open.assert_called_with(STR_PATH_HOME__TODO_, 'a')
            mock_open().write.assert_called_once_with('1 task3\n')
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), 'info    : task is added to the todolist - 1 task3')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n4 ma seconde tache')
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_task_todolist_not_empty(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, add, 'task3']):
            mock_isfile.return_value = True
            add(mock_open)
            #mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'a')
            mock_open().write.assert_called_once_with('5 task3\n')
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), 'info    : task is added to the todolist - 5 task3')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache')
    @patch('sys.stdout', new_callable=StringIO)
    def test_del_task(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, delete, '2']):
            mock_isfile.return_value = True
            delete(mock_open)
            #mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'w')
            mock_open().write.assert_called_once_with('1 ma tache #test\n')
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), 'info    : task deleted from the todolist - 2 ma seconde tache')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test #toto\n2 ma seconde tache #tost #titi\n3 ma seconde tache #test #titi')
    @patch('sys.stdout', new_callable=StringIO)
    def test_untag_task(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, untag, 'test', '1', '2', '3']):
            mock_isfile.return_value = True
            untag(mock_open)
            #mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'w')
            mock_open().write.assert_called_with('3 ma seconde tache #titi\n')
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), 'info    : tag deleted from the task of the todolist - 1 ma tache #test #toto -> 1 ma tache #toto\nwarning : no tags is deleted from the todolist for the task - 2 ma seconde tache #tost #titi\ninfo    : tag deleted from the task of the todolist - 3 ma seconde tache #test #titi -> 3 ma seconde tache #titi')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache\n2 ma seconde tache #tost')
    @patch('sys.stdout', new_callable=StringIO)
    def test_tag_task(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, tag, 'test', '1', '2', '3']):
            mock_isfile.return_value = True
            tag(mock_open)
            #mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'w')
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), 'info    : tag added to the task of the todolist - 1 ma tache -> 1 ma tache #test\ninfo    : tag added to the task of the todolist - 2 ma seconde tache #tost -> 2 ma seconde tache #tost #test\nwarning : no task with number is in the todolist - 3')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache\n')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_notag(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, untag]):
            mock_isfile.return_value = True
            untag(mock_open)
            #mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(
                mock_print.getvalue().rstrip('\n')), '2 ma seconde tache')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache #test\n3 ma seconde tache #linux')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_tag(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, tag]):
            mock_isfile.return_value = True
            tag(mock_open)
            #mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(
                mock_print.getvalue().rstrip('\n')), '#linux\n'+'#test')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_if_todo_empty(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, find, "toto"]):
            mock_isfile.return_value = True
            find(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), "warning : the filtered todolist is empty")

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache #test\n3 ma seconde tache #linux')
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_if_one_task(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, find, "ma tache "]):
            mock_isfile.return_value = True
            find(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), "1 ma tache #test")

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache #test\n3 ma seconde tache #linux')
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_regex_if_one_task(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, find, "li.+x"]):
            mock_isfile.return_value = True
            find(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), "3 ma seconde tache #linux")

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_if_no_file(self, mock_print, mock_open, mock_isfile):
        mock_isfile.return_value = False
        with patch.object(sys, 'argv', [pypodo, find, "li.+x"]):
            find(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), "info    : creating .todolist file\nwarning : the filtered todolist is empty")

    @freeze_time("2020-10-14")
    def test_date(self):
        self.assertEqual("ok", test_date("20210101"))
        self.assertEqual("alert", test_date("20201009"))
        self.assertEqual("warning", test_date("20201020"))

    @patch('builtins.open', new_callable=mock_open, read_data='[COLOR]\nalert =red\nwarning=blue\ninfo=tyty\n[FONCTIONAL]\nmybool = False\nmybool2 = Tru\nperiodwarning = red\n[SYSTEM]\nlevel = error\nlevel2 = warning\nlevel3 = debugg')
    def test_config(self, mock_open):
        self.assertEqual("red", read_config("COLOR", "alert", "red"))
        self.assertEqual("red", read_config("COLOR", "alert", "red"))
        self.assertEqual("blue", read_config("COLOR", "warning", "yellow"))
        self.assertEqual("tyty", read_config("COLOR", "info", "green"))
        self.assertEqual("green", read_config_color("COLOR", "info", "green"))
        self.assertEqual("red", read_config_color("COLOR", "error", "red"))
        self.assertEqual("1", read_config_int("FONCTIONAL", "periodalert", "1"))
        self.assertEqual("7", read_config_int("FONCTIONAL", "periodwarning", "7"))
        self.assertEqual("error", read_config_level("SYSTEM", "level", "error"))
        self.assertEqual("warning", read_config_level("SYSTEM", "level2", "error"))
        self.assertEqual("error", read_config_level("SYSTEM", "level3", "error"))
        self.assertEqual("False", read_config_boolean("FONCTIONAL", "mybool", "True"))
        self.assertEqual("True", read_config_boolean("FONCTIONAL", "mybool2", "True"))

    def test_help(self):
        help()


def escape_ansi(line):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


if __name__ == '__main__':
    unittest.main()
