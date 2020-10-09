import sys
import unittest
import re
from io import StringIO
from pathlib import Path
from unittest.mock import patch, mock_open
from pypodo.__pypodo__ import pypodo, list, add, delete, untag, tag, sort

STR_PATH_HOME__TODO_ = str(Path.home()) + '/.todo'


class TestStringMethods(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_sort_retourne_vide(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, list]):
            list(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip('\n')), "warning : the todolist is empty")

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_retourne_vide(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, sort]):
            sort(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip('\n')), "warning : the todolist is empty - nothing to do")

    @patch('builtins.open', new_callable=mock_open, read_data = '1 ma tache')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_retourne_une_tache(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, list]):
            list(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip('\n')), '1 ma tache')

    @patch('builtins.open', new_callable=mock_open, read_data = '1 ma tache #test\n2 ma seconde tache')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_TAG_retourne_une_tache_avec_un_tag(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, list, 'test']):
            list(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip('\n')),'1 ma tache #test')

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_task_inorrecte(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, add, '#pe']):
            add(mock_open)
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip('\n')),'warning : the task has not a valid format - #pe')

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_TACHE_ajoute_une_tache(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, add, 'task3']):
            add(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'a')
            mock_open().write.assert_called_once_with('1 task3\n')  
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip('\n')),'info : task is added to the todolist - 1 task3')         

    @patch('builtins.open', new_callable=mock_open, read_data = '1 ma tache #test\n2 ma seconde tache')
    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_INDEX_supprime_une_tache(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, delete, '2']):
            delete(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'w')
            mock_open().write.assert_called_once_with('1 ma tache #test\n')
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip('\n')),'info : task deleted from the todolist - 2 ma seconde tache')

    @patch('builtins.open', new_callable=mock_open, read_data = '1 ma tache #test\n2 ma seconde tache\n')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_noTAG_retourne_une_tache_avec_un_tag(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, untag]):
            untag(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip('\n')), '2 ma seconde tache')

    @patch('builtins.open', new_callable=mock_open, read_data = '1 ma tache #test\n2 ma seconde tache #test\n3 ma seconde tache #linux')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_TAGS_retourne_tags(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, tag]):
            tag(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(escape_ansi(mock_print.getvalue().rstrip('\n')), '#linux\n'+'#test')


def escape_ansi(line):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)

if __name__ == '__main__':
    unittest.main()
