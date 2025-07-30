import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import platform

from damply.utils import whose


@pytest.mark.skipif(platform.system() != "Linux", reason="Test specific to Linux")
def test_get_file_owner_full_name_linux():
    file_path = Path('/dummy/path')

    with patch('os.stat') as mock_stat, patch('pwd.getpwuid') as mock_getpwuid:
        mock_stat.return_value.st_uid = 1000
        mock_user_info = MagicMock()
        mock_user_info.pw_gecos = 'John Doe'
        mock_getpwuid.return_value = mock_user_info

        assert whose.get_file_owner_full_name(file_path) == 'John Doe'


@pytest.mark.skipif(platform.system() != "Darwin", reason="Test specific to macOS")
def test_get_file_owner_full_name_macos():
    file_path = Path('/dummy/path')

    with patch('os.stat') as mock_stat, patch('pwd.getpwuid') as mock_getpwuid:
        mock_stat.return_value.st_uid = 501  # Common uid for first user in macOS
        mock_user_info = MagicMock()
        mock_user_info.pw_gecos = 'Mac User'
        mock_getpwuid.return_value = mock_user_info

        assert whose.get_file_owner_full_name(file_path) == 'Mac User'


@pytest.mark.skipif(platform.system() != "Windows", reason="Test specific to Windows")
def test_get_file_owner_full_name_windows():
    file_path = Path('C:\\dummy\\path')

    with patch('platform.system', return_value='Windows'):
        # On Windows, the function should return the message about Windows not being supported
        result = whose.get_file_owner_full_name(file_path)
        assert result == 'Retrieving user info is not supported on Windows.'