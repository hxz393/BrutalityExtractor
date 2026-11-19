import importlib.util
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GroupingTests(unittest.TestCase):
    def test_seven_zip_volumes_are_grouped_as_one_archive(self):
        group_paths = load_module('test_group_file_paths', 'modules/main_func/group_file_paths.py')
        group_pattern = load_module('test_group_files_by_pattern', 'modules/main_func/group_files_by_pattern.py')
        paths = [
            os.path.join('C:\\archives', 'nested.7z.001'),
            os.path.join('C:\\archives', 'nested.7z.002'),
        ]

        groups = group_paths.group_file_paths(paths)
        infos = group_pattern.group_files_by_pattern({
            'target_path': 'C:\\archives\\nested',
            'grouped_file_list': paths,
        })

        self.assertEqual(list(groups), ['C:\\archives\\nested'])
        self.assertEqual(len(infos), 1)
        self.assertTrue(infos[0]['main_file_path'].endswith('nested.7z.001'))
        self.assertEqual(infos[0]['grouped_file_list'], sorted(paths))

    def test_archive_output_is_in_archive_directory(self):
        group_main = load_module(
            'test_group_files_main',
            'modules/main_func/group_files_main.py',
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            archive = Path(temp_dir) / 'sample.7z'
            archive.write_bytes(b'7z\xbc\xaf\x27\x1c')
            full_infos = [{
                'target_path': str(Path(temp_dir) / 'sample'),
                'main_file_path': str(archive),
                'grouped_file_list': [str(archive)],
            }]
            with patch.object(group_main, 'get_file_type', return_value='application/x-7z-compressed'):
                file_infos = group_main.group_files_main(full_infos)

            self.assertEqual(file_infos[0]['target_path'], temp_dir)


class FileTypeFallbackTests(unittest.TestCase):
    def test_split_seven_zip_volume_uses_signature_fallback(self):
        get_file_type = load_module(
            'test_get_file_type',
            'modules/file_ops/get_file_type.py',
        )

        with tempfile.NamedTemporaryFile(suffix='.001', delete=False) as archive:
            archive.write(b'7z\xbc\xaf\x27\x1c' + b'\x00' * 32)
            archive_path = archive.name

        try:
            with patch.dict(sys.modules, {'magic': None}):
                self.assertEqual(
                    get_file_type.get_file_type(archive_path),
                    'application/x-7z-compressed',
                )
        finally:
            os.unlink(archive_path)

    def test_plain_seven_zip_uses_signature_before_magic(self):
        get_file_type = load_module(
            'test_get_plain_7z_type',
            'modules/file_ops/get_file_type.py',
        )

        with tempfile.NamedTemporaryFile(suffix='.7z', delete=False) as archive:
            archive.write(b'7z\xbc\xaf\x27\x1c' + b'\x00' * 32)
            archive_path = archive.name

        try:
            with patch.dict(sys.modules, {'magic': object()}):
                self.assertEqual(
                    get_file_type.get_file_type(archive_path),
                    'application/x-7z-compressed',
                )
        finally:
            os.unlink(archive_path)


class RecursiveExtractionTests(unittest.TestCase):
    def test_same_directory_return_code_zero_is_success(self):
        file_unzip = load_module('test_file_unzip_same_dir', 'modules/main_func/file_unzip.py')

        with tempfile.TemporaryDirectory() as temp_dir:
            archive = Path(temp_dir) / 'inner.7z'
            archive.write_bytes(b'7z\xbc\xaf\x27\x1c')
            file_info = {
                'target_path': temp_dir,
                'main_file': str(archive),
                'file_list': [str(archive)],
            }
            completed = SimpleNamespace(returncode=0, stdout=b'', stderr=b'')

            with patch.object(file_unzip.subprocess, 'run', return_value=completed):
                result = file_unzip._file_unzip_once(file_info, {''})

            self.assertEqual(result['code'], 0)

    def test_nested_archives_are_processed_until_exhausted_and_removed(self):
        file_ops = types.ModuleType('modules.file_ops')
        file_ops.get_file_paths = lambda path: []
        file_ops.get_resource_path = lambda path: path
        file_ops.get_target_size = lambda path: 0
        main_func = types.ModuleType('modules.main_func')
        main_func.__path__ = [str(ROOT / 'modules' / 'main_func')]
        modules = types.ModuleType('modules')
        modules.__path__ = [str(ROOT / 'modules')]
        sys.modules.update({
            'modules': modules,
            'modules.file_ops': file_ops,
            'modules.main_func': main_func,
        })

        group_paths = types.ModuleType('modules.main_func.group_file_paths')
        group_paths.group_file_paths = lambda paths: {}
        group_main = types.ModuleType('modules.main_func.group_files_main')
        group_main.group_files_main = lambda infos: []
        group_lens = types.ModuleType('modules.main_func.group_list_by_lens')
        group_lens.group_list_by_lens = lambda groups: []
        sys.modules.update({
            'modules.main_func.group_file_paths': group_paths,
            'modules.main_func.group_files_main': group_main,
            'modules.main_func.group_list_by_lens': group_lens,
        })
        file_unzip = load_module('test_file_unzip', 'modules/main_func/file_unzip.py')

        with tempfile.TemporaryDirectory() as temp_dir:
            first = Path(temp_dir) / 'inner.7z.001'
            second = Path(temp_dir) / 'deep.7z.001'
            first.write_bytes(b'first')
            second.write_bytes(b'second')
            infos = [
                {'target_path': str(Path(temp_dir) / 'inner'), 'main_file': str(first), 'file_list': [str(first)]},
                {'target_path': str(Path(temp_dir) / 'deep'), 'main_file': str(second), 'file_list': [str(second)]},
            ]
            pending = list(infos)

            def discover(_target, processed, _protected_archives=None):
                return [info for info in pending if os.path.abspath(info['main_file']).lower() not in processed]

            with patch.object(file_unzip, '_get_nested_file_infos', side_effect=discover), \
                    patch.object(file_unzip, '_file_unzip_once', return_value={'code': 0, 'file_info': infos[0]}):
                file_unzip._extract_nested_archives(temp_dir, {''}, False)

            self.assertFalse(first.exists())
            self.assertFalse(second.exists())

    def test_flatten_moves_final_files_to_target_root_and_removes_folders(self):
        file_unzip = load_module('test_file_unzip_flatten', 'modules/main_func/file_unzip.py')

        with tempfile.TemporaryDirectory() as temp_dir:
            intermediate = Path(temp_dir) / 'outer' / 'inner'
            intermediate.mkdir(parents=True)
            final_file = intermediate / 'payload.bin'
            final_file.write_bytes(b'final sample')

            file_unzip.flatten_extracted_output(temp_dir)

            flattened_file = Path(temp_dir) / 'payload.bin'
            self.assertTrue(flattened_file.exists())
            self.assertEqual(flattened_file.read_bytes(), b'final sample')
            self.assertFalse((Path(temp_dir) / 'outer').exists())

    def test_failed_extraction_does_not_flatten_or_delete_target_directory(self):
        file_unzip = load_module('test_file_unzip_failure', 'modules/main_func/file_unzip.py')

        with tempfile.TemporaryDirectory() as temp_dir:
            archive = Path(temp_dir) / 'broken.7z'
            archive.write_bytes(b'broken')
            keep_file = Path(temp_dir) / 'keep.txt'
            keep_file.write_text('keep', encoding='utf-8')
            file_info = {
                'target_path': temp_dir,
                'main_file': str(archive),
                'file_list': [str(archive)],
            }

            with patch.object(file_unzip, '_file_unzip_once', return_value={'code': 10, 'file_info': file_info}), \
                    patch.object(file_unzip, 'flatten_extracted_output') as flatten:
                result = file_unzip.file_unzip(file_info, {''}, False)

            self.assertEqual(result['code'], 10)
            flatten.assert_not_called()
            self.assertTrue(keep_file.exists())
            self.assertTrue(archive.exists())

    def test_original_archive_is_always_protected_from_nested_cleanup(self):
        file_unzip = load_module('test_file_unzip_original_protection', 'modules/main_func/file_unzip.py')

        with tempfile.TemporaryDirectory() as temp_dir:
            original = Path(temp_dir) / 'original.7z'
            original.write_bytes(b'original archive')
            nested = Path(temp_dir) / 'nested.7z'
            nested.write_bytes(b'nested archive')
            protected = {
                os.path.normcase(os.path.abspath(str(original))),
            }

            nested_infos = file_unzip._get_nested_file_infos(
                temp_dir,
                set(),
                protected,
            )

            self.assertTrue(original.exists())
            nested_keys = {
                os.path.normcase(os.path.abspath(info['main_file']))
                for info in nested_infos
            }
            self.assertNotIn(
                os.path.normcase(os.path.abspath(str(original))),
                nested_keys,
            )


if __name__ == '__main__':
    unittest.main()
