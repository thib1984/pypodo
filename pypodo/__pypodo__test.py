import re
import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import mock_open, patch

from pypodo.__pypodo__ import add, delete, list, pypodo, sort, tag, untag, help, backup, find

STR_PATH_HOME__TODO_ = str(Path.home()) + '/.todo'


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
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(
                mock_print.getvalue().rstrip('\n')), '1 ma tache')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_with_filter_one_task(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, list, 'test']):
            mock_isfile.return_value = True
            list(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(
                mock_print.getvalue().rstrip('\n')), '1 ma tache #test')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache #linux\n3 ma troisieme tache #linux #test\n4 ma 4 tache #toto')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_with_double_filter_one_task(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, list, 'test', 'linux']):
            mock_isfile.return_value = True
            list(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(
                mock_print.getvalue().rstrip('\n')), '3 ma troisieme tache #linux #test')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache #linux\n3 ma troisieme tache #linux #test\n4 ma 4 tache #toto')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_with_double_filter_one_task_return_empty(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, list, 'test', 'pe']):
            mock_isfile.return_value = True
            list(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
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
    def test_add_task(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, add, 'task3']):
            mock_isfile.return_value = True
            add(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'a')
            mock_open().write.assert_called_once_with('1 task3\n')
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), 'info    : task is added to the todolist - 1 task3')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache')
    @patch('sys.stdout', new_callable=StringIO)
    def test_del_task(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, delete, '2']):
            mock_isfile.return_value = True
            delete(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'w')
            mock_open().write.assert_called_once_with('1 ma tache #test\n')
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip(
                '\n')), 'info    : task deleted from the todolist - 2 ma seconde tache')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache\n')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_notag(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, untag]):
            mock_isfile.return_value = True
            untag(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(
                mock_print.getvalue().rstrip('\n')), '2 ma seconde tache')

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='1 ma tache #test\n2 ma seconde tache #test\n3 ma seconde tache #linux')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_tag(self, mock_print, mock_open, mock_isfile):
        with patch.object(sys, 'argv', [pypodo, tag]):
            mock_isfile.return_value = True
            tag(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
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

def escape_ansi(line):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


if __name__ == '__main__':
    unittest.main()
