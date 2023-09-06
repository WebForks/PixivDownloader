import unittest
from unittest.mock import patch
import argparse
from cli import cli_main  # Replace with the actual import

class TestCLI(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    def test_single_image_current_dir_download(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            url='https://www.pixiv.net/en/artworks/4531683', 
            config=None,
            tag=None,
            sort_order='newest',
            page_start=1,
            page_end=100,
            s_mode='perfect_match',
            type='all',
            ai_type='perfect_match',
            resolution='all',
            ratio='all',
            period=None,
            bookmarks='all',
            file_location=r'./test',
            cookies_psshid=None,
            debug=False,
        )
        cli_main(args=mock_args.return_value)

    @patch('argparse.ArgumentParser.parse_args')
    def test_multi_image_current_dir_download(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            url='https://www.pixiv.net/en/artworks/59640290', 
            config=None,
            tag=None,
            sort_order='newest',
            page_start=1,
            page_end=100,
            s_mode='perfect_match',
            type='all',
            ai_type='perfect_match',
            resolution='all',
            ratio='all',
            period=None,
            bookmarks='all',
            file_location=r'./test',
            cookies_psshid=None,
            debug=False,
        )
        cli_main(args=mock_args.return_value)

    @patch('argparse.ArgumentParser.parse_args')
    def test_single_image_other_dir_download(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            url='https://www.pixiv.net/en/artworks/4531683', 
            config=None,
            tag=None,
            sort_order='newest',
            page_start=1,
            page_end=100,
            s_mode='perfect_match',
            type='all',
            ai_type='perfect_match',
            resolution='all',
            ratio='all',
            period=None,
            bookmarks='all',
            file_location=r'./test/test2',
            cookies_psshid=None,
            debug=False,
        )
        cli_main(args=mock_args.return_value)

    @patch('argparse.ArgumentParser.parse_args')
    def test_multi_image_other_dir_download(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            url='https://www.pixiv.net/en/artworks/59640290',
            config=None,
            tag=None,
            sort_order='newest',
            page_start=1,
            page_end=100,
            s_mode='perfect_match',
            type='all',
            ai_type='perfect_match',
            resolution='all',
            ratio='all',
            period=None,
            bookmarks='all',
            file_location=r'./test/test2',
            cookies_psshid=None,
            debug=False,
        )
        cli_main(args=mock_args.return_value)

    @patch('argparse.ArgumentParser.parse_args')
    def test_single_image_configINI_current_dir_download(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            url='https://www.pixiv.net/en/artworks/4531683', 
            config=r'config.ini',
            )
        cli_main(args=mock_args.return_value)

    @patch('argparse.ArgumentParser.parse_args')
    def test_multi_image_configINI_current_dir_download(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            url='https://www.pixiv.net/en/artworks/59640290', 
            config=r'config.ini',
            )
        cli_main(args=mock_args.return_value)

if __name__ == '__main__':
    unittest.main()
