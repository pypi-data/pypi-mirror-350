import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class Directory:
	directory: Path
	size_GB: int

	def __post_init__(self) -> None:
		self.parent = self.directory.parent

	def __getitem__(self, key: str) -> Any:  # noqa: ANN401
		return self.__dict__[key]

	def __repr__(self) -> str:
		return f'Directory({self.directory}, {self.size_GB})'


@dataclass
class DirectoryList:
	directories: List[Directory]

	def __post_init__(self) -> None:
		self.common_root = self.get_common_root()

	def get_common_root(self) -> Path:
		dirs = [directory.directory for directory in self.directories]
		common_path = os.path.commonpath(dirs)
		return Path(common_path)

	def __len__(self) -> int:
		return len(self.directories)

	def __getitem__(self, key: int) -> Directory:
		return self.directories[key]

	def __repr__(self) -> str:
		fmt_str = ''
		fmt_str += f'CommonPre:{self.common_root}\n'
		for directory in self.directories:
			fmt_str += f'{directory}\n'
		return fmt_str

	def dir_size_dict(self) -> Dict[Path, int]:
		return {
			directory.directory: directory.size_GB for directory in self.directories
		}
