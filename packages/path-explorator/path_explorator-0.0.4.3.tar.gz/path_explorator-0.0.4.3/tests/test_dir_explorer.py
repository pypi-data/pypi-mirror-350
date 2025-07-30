import unittest
from pathlib import Path
from src.path_explorator import DirectoryExplorer

def get_folder_test_path():
    return Path(Path.cwd().parent / Path('folder_tests'))

class TestDirectoryExplorer(unittest.TestCase):
    def setUp(self):
        root_dir_abs_path = get_folder_test_path().__str__()
        self.explorer = DirectoryExplorer(root_dir_abs_path)

    def test_find_entities_path(self):
        searchable_folder = ''
        searchable = 'lobotomia.mp3'
        path = self.explorer.find_entities_path(searchable_folder, searchable)
        asserting = ['/music/egor_letov/lobotomia.mp3']
        self.assertEqual(path, asserting)


    def test_get_all_entitynames_in_dir(self):
        searchable_dir = ''
        entitynames = self.explorer.get_all_entitynames_in_dir(searchable_dir)
        asserting = ['/music','/movies', '/test_file.file']
        self.assertCountEqual(entitynames, asserting)

    def test_get_all_filenames_in_dir(self):
        searchable_dir = ''
        fnames = self.explorer.get_all_filenames_in_dir(searchable_dir)
        asserting = ['/test_file.file']
        self.assertEqual(fnames, asserting)

    def test_is_file(self):
        file_path = 'test_file.file'
        not_file_path = 'movies'
        is_file = self.explorer.is_file(file_path)
        is_not_file = self.explorer.is_file(not_file_path)
        self.assertTrue(is_file)
        self.assertFalse(is_not_file)

    def test_is_dir(self):
        dir_path = 'movies'
        not_dir_path = 'test_file.file'
        is_dir = self.explorer.is_dir(dir_path)
        is_not_dir = self.explorer.is_dir(not_dir_path)
        self.assertTrue(is_dir)
        self.assertFalse(is_not_dir)

    def test_is_exists(self):
        file_path = 'test_file.file'
        dir_path = 'movies'
        f_exists = self.explorer.is_exists(file_path)
        d_exists = self.explorer.is_exists(dir_path)
        self.assertTrue(f_exists)
        self.assertTrue(d_exists)

    def test_get_name(self):
        entity_path = '/movies/save_pvt_ryan.movie'
        name = self.explorer.get_name(entity_path)
        asserting = 'save_pvt_ryan.movie'
        self.assertEqual(name, asserting)

    def test_join_with_root(self):
        joinable = 'fake_folder'
        joined = self.explorer.join_with_root_path(joinable)
        expected = f'{self.explorer.root_path}/{joinable}'

        self.assertEqual(joined, expected)