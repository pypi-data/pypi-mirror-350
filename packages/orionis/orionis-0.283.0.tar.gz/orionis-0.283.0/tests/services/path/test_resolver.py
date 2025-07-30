import tempfile
import os
from pathlib import Path
from orionis.services.paths.resolver import Resolver
from orionis.unittesting import TestCase

class TestsResolver(TestCase):
    """
    Unit tests for the Resolver class, which resolves file and directory paths relative to a base directory.
    """

    async def test_file_not_found(self):
        """
        Test that resolving a non-existent file path raises FileNotFoundError.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            resolver = Resolver(tmpdir)
            non_existent = "does_not_exist.txt"
            with self.assertRaises(FileNotFoundError):
                resolver.relativePath(non_existent)

    async def test_valid_file_path(self):
        """
        Test that resolving a valid file path returns the correct absolute path.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a temporary file inside the temp directory
            file_path = Path(tmpdir) / "testfile.txt"
            file_path.write_text("sample content")
            resolver = Resolver(tmpdir)
            resolved = resolver.relativePath("testfile.txt").toString()
            # The resolved path should end with the file name
            self.assertTrue(resolved.endswith("testfile.txt"))
            # The resolved path should be absolute
            self.assertTrue(os.path.isabs(resolved))

    async def test_valid_directory_path(self):
        """
        Test that resolving a valid directory path returns the correct absolute path.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a subdirectory inside the temp directory
            subdir = Path(tmpdir) / "subdir"
            subdir.mkdir()
            resolver = Resolver(tmpdir)
            resolved = resolver.relativePath("subdir").toString()
            self.assertTrue(resolved.endswith("subdir"))
            self.assertTrue(os.path.isabs(resolved))

    async def test_other_base_path(self):
        """
        Test that providing a different base path to Resolver works as expected.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file in a subdirectory
            subdir = Path(tmpdir) / "base"
            subdir.mkdir()
            file_path = subdir / "file.txt"
            file_path.write_text("data")
            resolver = Resolver(str(subdir))
            resolved = resolver.relativePath("file.txt").toString()
            self.assertTrue(resolved.endswith("file.txt"))
            self.assertTrue(os.path.isabs(resolved))

    async def test_equal_output_string(self):
        """
        Test that the string representation of the resolved path matches the output of toString().
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "file.txt"
            file_path.write_text("abc")
            resolver = Resolver(tmpdir).relativePath("file.txt")
            self.assertEqual(resolver.toString(), str(resolver))