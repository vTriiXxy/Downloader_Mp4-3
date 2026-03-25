
import unittest
from unittest.mock import patch, MagicMock
from downloader import start_download

class TestDownloader(unittest.TestCase):

    @patch('downloader.yt_dlp.YoutubeDL')
    def test_start_download_video_success(self, mock_youtube_dl):
        # Arrange
        mock_ydl_instance = MagicMock()
        mock_youtube_dl.return_value.__enter__.return_value = mock_ydl_instance
        
        # Act
        result = start_download('fake_video_url', 'video')

        # Assert
        self.assertTrue(result)
        mock_youtube_dl.assert_called_once()
        mock_ydl_instance.download.assert_called_once_with(['fake_video_url'])

    @patch('downloader.yt_dlp.YoutubeDL')
    def test_start_download_audio_success(self, mock_youtube_dl):
        # Arrange
        mock_ydl_instance = MagicMock()
        mock_youtube_dl.return_value.__enter__.return_value = mock_ydl_instance

        # Act
        result = start_download('fake_audio_url', 'audio')

        # Assert
        self.assertTrue(result)
        mock_youtube_dl.assert_called_once()
        mock_ydl_instance.download.assert_called_once_with(['fake_audio_url'])

    @patch('downloader.yt_dlp.YoutubeDL')
    def test_start_download_download_error(self, mock_youtube_dl):
        # Arrange
        from yt_dlp.utils import DownloadError
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.download.side_effect = DownloadError("Test error")
        mock_youtube_dl.return_value.__enter__.return_value = mock_ydl_instance

        # Act
        result = start_download('fake_url_error', 'video')

        # Assert
        self.assertFalse(result)
        mock_youtube_dl.assert_called_once()
        mock_ydl_instance.download.assert_called_once_with(['fake_url_error'])

if __name__ == '__main__':
    unittest.main()
