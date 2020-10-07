import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch, mock_open
from colorama import Fore, Style
from termcolor import colored
from pypodo.__pypodo__ import pypodo, list, add, delete

STR_PATH_HOME__TODO_ = str(Path.home()) + '/.todo'


class TestStringMethods(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_retourne_vide(self, mock_print):
        list()
        self.assertEqual(mock_print.getvalue().rstrip('\n'), colored("warning : the todolist is empty","yellow"))

    @patch('builtins.open', new_callable=mock_open, read_data = '1 ma tache')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_retourne_une_tache(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, list]):
            list(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(mock_print.getvalue().rstrip('\n'), Fore.BLUE +'1 '+ Fore.GREEN+'ma tache' + Fore.YELLOW)

    @patch('builtins.open', new_callable=mock_open, read_data = '1 ma tache #test\n2 ma seconde tache')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_TAG_retourne_une_tache_avec_un_tag(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, list, 'test']):
            list(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(mock_print.getvalue().rstrip('\n'), Fore.BLUE +'1 '+ Fore.GREEN+'ma tache ' +Fore.YELLOW+'#test')

    @patch('builtins.open', new_callable=mock_open)
    def test_add_TACHE_ajoute_une_tache(self, mock_open):
        with patch.object(sys, 'argv', [pypodo, add, 'task3']):
            add(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'a')
            mock_open().write.assert_called_once_with('1 task3\n')

    @patch('builtins.open', new_callable=mock_open, read_data = '1 ma tache #test\n2 ma seconde tache')
    def test_delete_INDEX_supprime_une_tache(self, mock_open):
        with patch.object(sys, 'argv', [pypodo, delete, '2']):
            delete(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'w')
            mock_open().write.assert_called_once_with('1 ma tache #test\n')


if __name__ == '__main__':
    unittest.main()
