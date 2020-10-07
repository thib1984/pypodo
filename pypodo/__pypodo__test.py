import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch, mock_open

from pypodo.__pypodo__ import pypodo, list, add, delete

STR_PATH_HOME__TODO_ = str(Path.home()) + '/.todo'


class TestStringMethods(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_retourne_vide(self, mock_print):
        list()
        self.assertEqual(mock_print.getvalue(), '')

    @patch('builtins.open', new_callable=mock_open, read_data = '1 ma tâche')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_retourne_une_tâche(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, list]):
            list(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(mock_print.getvalue(), '1 ma tâche')

    @patch('builtins.open', new_callable=mock_open, read_data = '1 ma tâche #test\n2 ma seconde tâche')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_TAG_retourne_une_tâche_avec_un_tag(self, mock_print, mock_open):
        with patch.object(sys, 'argv', [pypodo, list, 'test']):
            list(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'r')
            self.assertEqual(mock_print.getvalue(), '1 ma tâche #test\n')

    @patch('builtins.open', new_callable=mock_open)
    def test_add_TACHE_ajoute_une_tâche(self, mock_open):
        with patch.object(sys, 'argv', [pypodo, add, 'task3']):
            add(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'a')
            mock_open().write.assert_called_once_with('1 task3\n')

    @patch('builtins.open', new_callable=mock_open, read_data = '1 ma tâche #test\n2 ma seconde tâche')
    def test_delete_INDEX_supprime_une_tâche(self, mock_open):
        with patch.object(sys, 'argv', [pypodo, delete, '2']):
            delete(mock_open)
            mock_open.assert_called_with(STR_PATH_HOME__TODO_, 'w')
            mock_open().write.assert_called_once_with('1 ma tâche #test\n')


if __name__ == '__main__':
    unittest.main()