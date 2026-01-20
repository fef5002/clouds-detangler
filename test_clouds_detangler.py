#!/usr/bin/env python3
"""
Unit tests for clouds_detangler module
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# Import from main module
sys.path.insert(0, str(Path(__file__).parent))
from clouds_detangler import (
    CloudDetector, FileScanner, DuplicateFinder, 
    CloudFile, ManifestGenerator
)


class TestFileScanner(unittest.TestCase):
    """Test the FileScanner class"""
    
    def setUp(self):
        """Create temporary test directory"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.scanner = FileScanner()
    
    def tearDown(self):
        """Clean up test directory"""
        shutil.rmtree(self.test_dir)
    
    def test_compute_file_hash(self):
        """Test file hash computation"""
        test_file = self.test_dir / "test.txt"
        test_file.write_text("Hello, World!")
        
        hash1 = self.scanner.compute_file_hash(test_file)
        self.assertTrue(len(hash1) > 0)
        self.assertEqual(len(hash1), 64)  # SHA256 is 64 hex chars
        
        # Same content should give same hash
        test_file2 = self.test_dir / "test2.txt"
        test_file2.write_text("Hello, World!")
        hash2 = self.scanner.compute_file_hash(test_file2)
        self.assertEqual(hash1, hash2)
    
    def test_scan_directory(self):
        """Test directory scanning"""
        # Create test files
        (self.test_dir / "file1.txt").write_text("Content 1")
        (self.test_dir / "file2.txt").write_text("Content 2")
        subdir = self.test_dir / "subdir"
        subdir.mkdir()
        (subdir / "file3.txt").write_text("Content 3")
        
        files = self.scanner.scan_directory(self.test_dir, "test_provider")
        
        self.assertEqual(len(files), 3)
        for file in files:
            self.assertIsInstance(file, CloudFile)
            self.assertEqual(file.cloud_provider, "test_provider")
            self.assertTrue(len(file.hash) > 0)


class TestDuplicateFinder(unittest.TestCase):
    """Test the DuplicateFinder class"""
    
    def test_find_duplicates(self):
        """Test duplicate detection"""
        finder = DuplicateFinder()
        
        # Create test files (same hash = duplicate)
        files = [
            CloudFile(
                path="/path/to/file1.txt",
                size=100,
                hash="abc123",
                cloud_provider="google_drive",
                last_modified="2026-01-01T00:00:00"
            ),
            CloudFile(
                path="/path/to/file2.txt",
                size=100,
                hash="abc123",
                cloud_provider="onedrive",
                last_modified="2026-01-01T00:00:00"
            ),
            CloudFile(
                path="/path/to/file3.txt",
                size=200,
                hash="def456",
                cloud_provider="google_drive",
                last_modified="2026-01-01T00:00:00"
            )
        ]
        
        duplicates = finder.find_duplicates(files)
        
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0].hash, "abc123")
        self.assertEqual(len(duplicates[0].files), 2)
        self.assertEqual(duplicates[0].total_waste, 100)
    
    def test_no_duplicates_same_provider(self):
        """Test that files in same provider aren't marked as duplicates"""
        finder = DuplicateFinder()
        
        files = [
            CloudFile(
                path="/path/to/file1.txt",
                size=100,
                hash="abc123",
                cloud_provider="google_drive",
                last_modified="2026-01-01T00:00:00"
            ),
            CloudFile(
                path="/path/to/file2.txt",
                size=100,
                hash="abc123",
                cloud_provider="google_drive",
                last_modified="2026-01-01T00:00:00"
            )
        ]
        
        duplicates = finder.find_duplicates(files)
        
        # Same provider duplicates are still found but should be in the same group
        self.assertEqual(len(duplicates), 0)  # No cross-provider duplicates


class TestManifestGenerator(unittest.TestCase):
    """Test the ManifestGenerator class"""
    
    def setUp(self):
        """Create temporary output directory"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.generator = ManifestGenerator(self.test_dir)
    
    def tearDown(self):
        """Clean up test directory"""
        shutil.rmtree(self.test_dir)
    
    def test_generate_manifest(self):
        """Test manifest generation"""
        files = [
            CloudFile(
                path="/path/to/file1.txt",
                size=100,
                hash="abc123",
                cloud_provider="google_drive",
                last_modified="2026-01-01T00:00:00"
            )
        ]
        
        manifest_json = self.generator.generate_manifest(files, [])
        
        self.assertIn('"total_files": 1', manifest_json)
        self.assertIn('"total_duplicates": 0', manifest_json)
        self.assertIn('generated_at', manifest_json)
    
    def test_save_manifest(self):
        """Test saving manifest to file"""
        manifest_json = '{"test": "data"}'
        output_path = self.generator.save_manifest(manifest_json, "test.json")
        
        self.assertTrue(output_path.exists())
        content = output_path.read_text()
        self.assertEqual(content, manifest_json)


class TestCloudDetector(unittest.TestCase):
    """Test the CloudDetector class"""
    
    def test_is_cloud_directory(self):
        """Test cloud directory detection"""
        detector = CloudDetector()
        
        # This will return False in test environment
        is_cloud, provider = detector.is_cloud_directory(Path("/tmp"))
        self.assertFalse(is_cloud)
        self.assertEqual(provider, "")


if __name__ == '__main__':
    unittest.main()
