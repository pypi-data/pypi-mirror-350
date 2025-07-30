"""dmpdirs: Standardized access to project directories in data science workflows.

This package provides convenient access to common directories in data science projects,
supporting environment variable configuration and automatic directory creation.

Directory paths are determined in the following order:
1. From corresponding environment variables (if set)
2. Default paths relative to the project root

Environment variables that can be used:
- DMP_PROJECT_ROOT or PIXI_PROJECT_ROOT: The root directory of the project
- CONFIG: Configuration files directory
- METADATA: Dataset descriptions directory
- LOGS: Log files directory
- RAWDATA: Raw input data directory
- PROCDATA: Processed/intermediate data directory
- RESULTS: Analysis outputs directory
- SCRIPTS: Analysis scripts directory
- NOTEBOOKS: Jupyter notebooks directory

Default directory structure (when environment variables are not set):
```console
project_root/
├── config/         # Configuration files
├── data/           # All data in one parent directory
│   ├── procdata/   # Processed/intermediate data
│   ├── rawdata/    # Raw input data
│   └── results/    # Analysis outputs
├── logs/           # Log files
├── metadata/       # Dataset descriptions
└── workflow/       # Code organization
    ├── notebooks/  # Jupyter notebooks
    └── scripts/    # Analysis scripts
```

Usage:
    from damply.dmpdirs import dirs

    # Access paths as Path objects
    data_file = dirs.RAWDATA / "dataset.csv"

    # Print absolute paths
    print(dirs.RAWDATA)  # e.g., /Users/username/projects/my_project/data/rawdata

    # Disable strict mode to auto-create directories
    dirs.set_strict_mode(False)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import ClassVar, Dict, List
from loguru import logger

from .exceptions import DirectoryNameNotFoundError, EnvironmentVariableNotSetError

def get_project_root() -> Path:
    """Get the project root directory."""
    # Check if the environment variable is set
    if project_root := os.getenv('DMP_PROJECT_ROOT') or (
        project_root := os.getenv('PIXI_PROJECT_ROOT')
    ):
        return Path(project_root).resolve()

    # If not, use the current working directory
    return Path.cwd().resolve()


class DamplyDirs:
    """Class that provides computed properties for project directories.

    This class provides computed properties that lazily evaluate directory paths
    using environment variables when available, and raising appropriate errors 
    if directories don't exist when accessed.

    Directory access is provided through attribute access:
    - dirs.RAWDATA: Raw data directory
    - dirs.PROCDATA: Processed data directory
    - dirs.RESULTS: Results directory
    - dirs.CONFIG: Configuration files directory
    - dirs.METADATA: Metadata directory
    - dirs.LOGS: Log files directory
    - dirs.SCRIPTS: Scripts directory
    - dirs.NOTEBOOKS: Notebooks directory

    By default, the class operates in "strict" mode, which means it will raise an error
    if a requested directory doesn't exist. This can be changed using the `set_strict_mode()`
    method.
    """

    # Class variable to hold singleton instance
    _instance: ClassVar[DamplyDirs | None] = None
    
    # List of valid directory names
    _VALID_DIRS: ClassVar[List[str]] = [
        'PROJECT_ROOT',
        'RAWDATA',
        'PROCDATA',
        'RESULTS',
        'METADATA',
        'LOGS',
        'CONFIG',
        'SCRIPTS',
        'NOTEBOOKS',
    ]
    
    # Private instance attributes
    _initialized: bool
    _project_root: Path
    _dir_cache: Dict[str, Path]
    _strict: bool = False  # Controls whether directories are created when missing

    def __new__(cls) -> DamplyDirs:
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(DamplyDirs, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize the DamplyDirs object (singleton)."""
        # Skip initialization if already initialized
        if getattr(self, '_initialized', False):
            return

        # Initialize core attributes
        self._project_root = get_project_root()
        self._dir_cache: Dict[str, Path] = {}
        self._initialized = True

    def set_strict_mode(self, strict: bool) -> None:
        """Set the strict mode for directory creation.

        In strict mode, errors are raised if directories don't exist.
        Otherwise, missing directories are created automatically.

        Args:
            strict: If True, enable strict mode. If False, disable strict mode.
        """
        self._strict = strict

    def _get_dir_path(self, dir_name: str) -> Path:
        """Get the path for a directory based on environment variables or default paths.

        Args:
            dir_name: The name of the directory to get

        Returns:
            Path object for the requested directory

        Raises:
            DirectoryNameNotFoundError: If the directory doesn't exist and strict mode is enabled
            EnvironmentVariableNotSetError: If env variable check is requested but not found
        """
        # Return from cache if available
        if dir_name in self._dir_cache:
            return self._dir_cache[dir_name]

        # Special case for PROJECT_ROOT
        if dir_name == 'PROJECT_ROOT':
            return self._project_root

        # Check if an environment variable with the same name exists
        if env_path := os.getenv(dir_name):
            # Use the environment variable value
            path = Path(env_path).resolve()
        else:
            # if strict mode is on, raise an error that environment variable is not set
            if self._strict:
                raise EnvironmentVariableNotSetError(dir_name)
            else:
                # If not strict, use default paths
                logger.warning(
                    f"Environment variable '{dir_name}' is not set. "
                    "Using default path relative to project root."
                )

            # Fall back to default paths relative to project root
            if dir_name in ['RAWDATA', 'PROCDATA', 'RESULTS']:
                # Data directories are in data/ subdirectory
                data_dir = self._project_root / 'data'
                path = data_dir / dir_name.lower()
            elif dir_name in ['SCRIPTS', 'NOTEBOOKS']:
                # Code directories are in workflow/ subdirectory
                workflow_dir = self._project_root / 'workflow'
                path = workflow_dir / dir_name.lower()
            else:
                # Other directories are directly in the project root
                path = self._project_root / dir_name.lower()

        # mkdir if not strict mode and path doesn't exist
        if not path.exists() and not self._strict:
            try:
                logger.info(
                    f"Creating directory '{path}' because it does not exist.")
                path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise DirectoryNameNotFoundError(dir_name, str(path)) from e

        # Cache the path
        self._dir_cache[dir_name] = path

        # Check if directory exists and create it or raise error if needed
        if not path.exists():
            if self._strict:
                raise DirectoryNameNotFoundError(dir_name, str(path))
            else:
                # Create the directory if it doesn't exist and we're in non-strict mode
                path.mkdir(parents=True, exist_ok=True)

        return path

    def __getattr__(self, name: str) -> Path:
        """Get attribute for a directory name.

        Args:
            name: The name of the directory to get

        Returns:
            Path object for the requested directory

        Raises:
            AttributeError: If the attribute is not a recognized directory
            DirectoryNameNotFoundError: If the directory doesn't exist and strict mode is on
        """
        if name.isupper() and name in self._VALID_DIRS:
            return self._get_dir_path(name)
        errmsg = (
            f"'{name}' is not a valid directory name. "
            f'Valid names are: {", ".join(self._VALID_DIRS)}'
        )
        raise AttributeError(errmsg)
        
    def __getitem__(self, key: str) -> Path:
        """Support dictionary-style access to directories.
        
        Args:
            key: Directory name (e.g., "RAWDATA", "CONFIG")
            
        Returns:
            Path object for the requested directory
            
        Raises:
            KeyError: If the key is not a recognized directory
            DirectoryNameNotFoundError: If the directory doesn't exist and strict mode is on
        """
        try:
            return getattr(self, key)
        except AttributeError as e:
            raise KeyError(str(e)) from e

    def __dir__(self) -> List[str]:
        """Return list of available attributes for tab completion."""
        return self._VALID_DIRS + ['set_strict_mode']

    def __repr__(self) -> str:
        """Return a tree-like representation of the directory structure."""
        strict_mode = f'Strict Mode: {"ON" if self._strict else "OFF"}'
        root_info = f'Project Root: {self._project_root}'

        # Create tree structure
        tree = [f'DamplyDirs<{strict_mode}>', root_info]

        for dir_name in sorted(dir_name for dir_name in self.__dir__() if dir_name.isupper()):
            if dir_name != 'PROJECT_ROOT':
                try:
                    path = getattr(self, dir_name)
                    rel_path = path.relative_to(self._project_root)
                    tree.append(f'{dir_name:<13}: ├── {rel_path}')
                except DirectoryNameNotFoundError:
                    tree.append(f'{dir_name:<13}: ├── <not found>')
                except ValueError:
                    # For paths that can't be made relative (e.g., on different drives)
                    tree.append(f'{dir_name:<13}: ├── {path} (absolute)')

        # Fix the last item to use └── instead of ├──
        if len(tree) > 2:
            tree[-1] = tree[-1].replace('├──', '└──')

        return '\n'.join(tree)


# Create a singleton instance that will be imported by users
dirs = DamplyDirs()
