import platform
from pathlib import Path
from typing import NoReturn


def _raise_windows_not_supported() -> NoReturn:
	msg = 'Platform not supported for retrieving user info using pwd module.'
	raise NotImplementedError(msg)


def get_file_owner_full_name(file_path: Path) -> str:
	try:
		if platform.system() == 'Windows':
			_raise_windows_not_supported()

		from pwd import getpwuid

		# Get the file's status
		file_stat = file_path.stat()
		# Get the user ID of the file owner
		uid: int = file_stat.st_uid

		# Get the user information based on the user ID
		getpwuid(uid)

	except ImportError:
		return file_path.owner()
	except NotImplementedError:
		return 'Retrieving user info is not supported on Windows.'
	except Exception as e:
		return str(e)
	else:
		return getpwuid(uid).pw_gecos
