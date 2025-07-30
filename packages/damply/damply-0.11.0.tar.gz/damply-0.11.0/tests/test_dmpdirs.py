#!/usr/bin/env python3
# filepath: /Users/bhklab/dev/GitHub/damply/tests/test_dmpdirs.py
"""Tests for the dmpdirs module."""

import os
import sys
import platform
import shutil
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from damply.dmpdirs import DamplyDirs, dirs, get_project_root
from damply.dmpdirs.exceptions import (
    DirectoryNameNotFoundError,
    EnvironmentVariableNotSetError,
)


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory to use as a project root."""
    # Create a temp directory
    temp_dir = tempfile.mkdtemp(prefix="damply_test_")
    try:
        yield Path(temp_dir)
    finally:
        # Clean up - remove the directory after the test completes
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def reset_dirs_singleton():
    """Reset the DamplyDirs singleton after each test."""
    # Save the original state
    original_instance = DamplyDirs._instance
    original_initialized = original_instance._initialized if original_instance else None
    original_strict = original_instance._strict if original_instance else None
    
    # Reset for test
    DamplyDirs._instance = None
    
    yield
    
    # Restore original state after test
    DamplyDirs._instance = original_instance
    if original_instance:
        original_instance._initialized = original_initialized
        original_instance._strict = original_strict


@pytest.fixture
def setup_env_vars(temp_project_dir):
    """Set up environment variables for testing."""
    old_env = os.environ.copy()
    
    # Set up environment variables
    os.environ["DMP_PROJECT_ROOT"] = str(temp_project_dir)
    os.environ["RAWDATA"] = str(temp_project_dir / "custom_rawdata")
    
    yield
    
    # Restore environment variables
    os.environ.clear()
    os.environ.update(old_env)


class TestGetProjectRoot:
    """Tests for the get_project_root function."""
    
    def test_get_project_root_env_var(self, temp_project_dir):
        """Test get_project_root uses the DMP_PROJECT_ROOT environment variable."""
        with mock.patch.dict(os.environ, {"DMP_PROJECT_ROOT": str(temp_project_dir)}):
            result = get_project_root()
            # Use resolve() on both sides to handle macOS /private prefix
            assert result.resolve() == temp_project_dir.resolve()
    
    def test_get_project_root_pixi_env_var(self, temp_project_dir):
        """Test get_project_root uses the PIXI_PROJECT_ROOT environment variable."""
        with mock.patch.dict(os.environ, {"PIXI_PROJECT_ROOT": str(temp_project_dir)}):
            assert get_project_root().resolve() == temp_project_dir.resolve()
            
    def test_get_project_root_cwd_fallback(self):
        """Test get_project_root falls back to current working directory."""
        with mock.patch.dict(os.environ, {}, clear=True):
            assert get_project_root() == Path.cwd().resolve()


class TestDamplyDirsSingleton:
    """Tests for the DamplyDirs singleton pattern."""
    
    def test_singleton_pattern(self, reset_dirs_singleton):
        """Test that DamplyDirs follows the singleton pattern."""
        dirs1 = DamplyDirs()
        dirs2 = DamplyDirs()
        assert dirs1 is dirs2
        
    def test_singleton_dir_cache(self, reset_dirs_singleton, temp_project_dir):
        """Test that the dir cache is properly maintained."""
        with mock.patch.dict(os.environ, {"DMP_PROJECT_ROOT": str(temp_project_dir)}):
            dirs1 = DamplyDirs()
            dirs1.set_strict_mode(False)
            # Access a property to cache it
            _ = dirs1.RAWDATA
            
            # Create a second instance, which should be the same object
            dirs2 = DamplyDirs()
            
            # The cached path should be available in the second instance
            assert "RAWDATA" in dirs2._dir_cache
            assert dirs2._dir_cache["RAWDATA"] == dirs1._dir_cache["RAWDATA"]


class TestDamplyDirsDirectoryCreation:
    """Tests for directory creation behavior."""
    
    def test_strict_mode_directory_access(self, reset_dirs_singleton, temp_project_dir):
        """Test that strict mode raises an error when directories don't exist."""
        with mock.patch.dict(os.environ, {"DMP_PROJECT_ROOT": str(temp_project_dir)}):
            # Initialize with strict mode enabled
            test_dirs = DamplyDirs()
            test_dirs.set_strict_mode(True)
            
            # In strict mode, it should raise EnvironmentVariableNotSetError when env var is not set
            with pytest.raises(EnvironmentVariableNotSetError):
                _ = test_dirs.RAWDATA
    
    def test_non_strict_mode_directory_creation(self, reset_dirs_singleton, temp_project_dir):
        """Test that non-strict mode creates missing directories."""
        with mock.patch.dict(os.environ, {"DMP_PROJECT_ROOT": str(temp_project_dir)}):
            # Initialize with strict mode disabled
            test_dirs = DamplyDirs()
            test_dirs.set_strict_mode(False)
            
            # This should create the directory
            rawdata_dir = test_dirs.RAWDATA
            
            # Check that the directory was created
            assert rawdata_dir.exists()
            assert rawdata_dir.resolve() == (temp_project_dir / "data" / "rawdata").resolve()
    
    def test_set_strict_mode(self, reset_dirs_singleton, temp_project_dir):
        """Test the set_strict_mode method."""
        with mock.patch.dict(os.environ, {"DMP_PROJECT_ROOT": str(temp_project_dir)}):
            test_dirs = DamplyDirs()
            test_dirs.set_strict_mode(False)
            assert test_dirs._strict is False
            
            test_dirs.set_strict_mode(True)
            assert test_dirs._strict is True
            
            # Should now raise an error for non-existent directories
            # First, let's ensure a directory doesn't exist
            results_path = temp_project_dir / "data" / "results"
            if results_path.exists():
                shutil.rmtree(results_path)
            
            # In strict mode, it should raise EnvironmentVariableNotSetError when env var is not set
            with pytest.raises(EnvironmentVariableNotSetError):
                _ = test_dirs.RESULTS


class TestDamplyDirsPathResolution:
    """Tests for path resolution behavior."""
    
    def test_path_from_env_var(self, reset_dirs_singleton, setup_env_vars, temp_project_dir):
        """Test that paths are resolved from environment variables when available."""
        test_dirs = DamplyDirs()
        rawdata_path = test_dirs.RAWDATA
        
        # Should use the env var path
        assert rawdata_path.resolve() == (temp_project_dir / "custom_rawdata").resolve()
        
    def test_default_paths(self, reset_dirs_singleton, temp_project_dir):
        """Test default path resolution when environment variables are not set."""
        with mock.patch.dict(os.environ, {"DMP_PROJECT_ROOT": str(temp_project_dir)}):
            test_dirs = DamplyDirs()
            test_dirs.set_strict_mode(False)
            
            # Test each directory type
            assert test_dirs.RAWDATA.resolve() == (temp_project_dir / "data" / "rawdata").resolve()
            assert test_dirs.PROCDATA.resolve() == (temp_project_dir / "data" / "procdata").resolve()
            assert test_dirs.RESULTS.resolve() == (temp_project_dir / "data" / "results").resolve()
            assert test_dirs.CONFIG.resolve() == (temp_project_dir / "config").resolve()
            assert test_dirs.METADATA.resolve() == (temp_project_dir / "metadata").resolve()
            assert test_dirs.LOGS.resolve() == (temp_project_dir / "logs").resolve()
            assert test_dirs.SCRIPTS.resolve() == (temp_project_dir / "workflow" / "scripts").resolve()
            assert test_dirs.NOTEBOOKS.resolve() == (temp_project_dir / "workflow" / "notebooks").resolve()
            assert test_dirs.PROJECT_ROOT.resolve() == temp_project_dir.resolve()
    
    def test_strict_env_var_requirement(self, reset_dirs_singleton, temp_project_dir):
        """Test that strict mode requires env vars to be set."""
        with mock.patch.dict(os.environ, {"DMP_PROJECT_ROOT": str(temp_project_dir)}):
            test_dirs = DamplyDirs()
            test_dirs.set_strict_mode(True)
            
            # Should raise an error because RAWDATA env var is not set and we're in strict mode
            with pytest.raises(EnvironmentVariableNotSetError):
                _ = test_dirs.RAWDATA


class TestDamplyDirsAccess:
    """Tests for different ways to access directories."""
    
    def test_attribute_access(self, reset_dirs_singleton, temp_project_dir):
        """Test attribute-style access to directories."""
        with mock.patch.dict(os.environ, {"DMP_PROJECT_ROOT": str(temp_project_dir)}):
            test_dirs = DamplyDirs()
            test_dirs.set_strict_mode(False)
            
            # Test attribute access
            assert test_dirs.RAWDATA.resolve() == (temp_project_dir / "data" / "rawdata").resolve()
    
    def test_dictionary_access(self, reset_dirs_singleton, temp_project_dir):
        """Test dictionary-style access to directories."""
        with mock.patch.dict(os.environ, {"DMP_PROJECT_ROOT": str(temp_project_dir)}):
            test_dirs = DamplyDirs()
            test_dirs.set_strict_mode(False)
            
            # Test dictionary access
            assert test_dirs["RAWDATA"].resolve() == (temp_project_dir / "data" / "rawdata").resolve()
    
    def test_invalid_directory_name(self, reset_dirs_singleton):
        """Test that accessing an invalid directory name raises an error."""
        test_dirs = DamplyDirs()
        
        # Test attribute access with invalid name
        with pytest.raises(AttributeError):
            _ = test_dirs.INVALID_DIR
        
        # Test dictionary access with invalid name
        with pytest.raises(KeyError):
            _ = test_dirs["INVALID_DIR"]


@pytest.mark.skipif(
    platform.system() != "Windows", 
    reason="This test is only relevant on Windows"
)
class TestWindowsSpecific:
    """Windows-specific tests."""
    
    def test_windows_paths(self, reset_dirs_singleton, temp_project_dir):
        """Test path handling on Windows."""
        with mock.patch.dict(os.environ, {"DMP_PROJECT_ROOT": str(temp_project_dir)}):
            test_dirs = DamplyDirs()
            test_dirs.set_strict_mode(False)
            
            # On Windows, check that backslashes are handled correctly
            rawdata_dir = test_dirs.RAWDATA
            assert "\\" in str(rawdata_dir)
            assert rawdata_dir.exists()


@pytest.mark.skipif(
    platform.system() == "Windows", 
    reason="This test is only relevant on Unix-like systems"
)
class TestUnixSpecific:
    """Unix-specific tests."""
    
    def test_unix_symlinks(self, reset_dirs_singleton, temp_project_dir):
        """Test handling of symlinks on Unix-like systems."""
        # Create a real directory to link to
        real_dir = temp_project_dir / "real_rawdata"
        real_dir.mkdir(parents=True)
        
        # Create a symlink
        symlink_path = temp_project_dir / "data" / "rawdata"
        symlink_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use os.symlink directly to handle potential permissions issues
        try:
            os.symlink(str(real_dir), str(symlink_path))
        except OSError:
            pytest.skip("Unable to create symlink - might need elevated permissions")
            
        # Use non-strict mode and also set RAWDATA env var to make the test more robust
        with mock.patch.dict(os.environ, {
            "DMP_PROJECT_ROOT": str(temp_project_dir),
            "RAWDATA": str(symlink_path)
        }):
            test_dirs = DamplyDirs()
            
            # Should correctly resolve the symlink
            assert test_dirs.RAWDATA.resolve() == real_dir.resolve()


class TestInstanceRepr:
    """Tests for the string representation of directories."""
    
    def test_repr_format(self, reset_dirs_singleton, temp_project_dir):
        """Test the __repr__ method format."""
        with mock.patch.dict(os.environ, {"DMP_PROJECT_ROOT": str(temp_project_dir)}):
            test_dirs = DamplyDirs()
            test_dirs.set_strict_mode(False)
            
            # Create a couple of directories to ensure they show up in repr
            _ = test_dirs.RAWDATA
            _ = test_dirs.CONFIG
            
            repr_str = repr(test_dirs)
            
            # Check that the repr contains expected elements
            assert "Project Root:" in repr_str
            assert "Strict Mode: OFF" in repr_str
            assert "RAWDATA" in repr_str
            assert "CONFIG" in repr_str


class TestImportedDirs:
    """Tests for the pre-imported dirs object."""
    
    def test_imported_dirs_instance(self):
        """Test that the imported dirs object is a DamplyDirs instance."""
        assert isinstance(dirs, DamplyDirs)
    
    def test_imported_dirs_attributes(self, temp_project_dir):
        """Test that the imported dirs object has the expected attributes."""
        with mock.patch.dict(os.environ, {"DMP_PROJECT_ROOT": str(temp_project_dir)}):
            # Reset dirs for this test
            dirs._dir_cache = {}
            dirs._project_root = get_project_root()
            
            # Test that we can access the attributes
            assert hasattr(dirs, "RAWDATA")
            assert hasattr(dirs, "set_strict_mode")
            
            # Test dir() includes the valid directories
            dir_list = dir(dirs)
            for valid_dir in dirs._VALID_DIRS:
                assert valid_dir in dir_list


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])