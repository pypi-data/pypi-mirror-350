import unittest
import os
import tempfile
import json
from io import BytesIO
from serve_dir.segments import Segments, resolve_source


class TestSegmentSupport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup a temporary directory with test segments
        cls.temp_dir = tempfile.mkdtemp()
        cls.segment_data = [[0, 5, "part1.txt"], [5, 11, "part2.txt"]]  # "Hello"  # " World"

        # Create physical segment files
        with open(os.path.join(cls.temp_dir, "part1.txt"), "w") as f:
            f.write("Hello")
        with open(os.path.join(cls.temp_dir, "part2.txt"), "w") as f:
            f.write(" World")

        # Create .parts.json manifest
        cls.manifest = {"length": 11, "parts": cls.segment_data}  # "Hello World" = 11 chars
        cls.manifest_path = os.path.join(cls.temp_dir, "test.parts.json")
        with open(cls.manifest_path, "w") as f:
            json.dump(cls.manifest, f)

    def test_segment_initialization(self):
        """Test Segments class loads manifest correctly"""
        seg = Segments(self.manifest_path)
        self.assertEqual(seg.length, 11)
        self.assertEqual(len(seg.parts), 2)
        self.assertTrue(all(len(part) == 4 for part in seg.parts))  # [start,end,path,file_obj]

    def test_resolve_source(self):
        """Test path resolution for segments"""
        abs_path = resolve_source("part1.txt", self.temp_dir)
        self.assertEqual(abs_path, os.path.join(self.temp_dir, "part1.txt"))

    def test_full_read(self):
        """Test reading entire stitched content"""
        seg = Segments(self.manifest_path)
        content = seg.read(11)  # Read full length
        self.assertEqual(content, b"Hello World")

    def test_partial_read(self):
        """Test reading across segment boundaries"""
        seg = Segments(self.manifest_path)
        # Read straddling part1 and part2
        seg.seek(3)  # "Hel|lo World"
        self.assertEqual(seg.read(5), b"lo Wo")  # "lo Wo"

    def test_byte_ranges(self):
        """Test byte-range operations"""
        seg = Segments(self.manifest_path)
        # Read first 3 bytes ("Hel")
        seg.seek(0)
        self.assertEqual(seg.read(3), b"Hel")

        # Read last 4 bytes ("orld")
        seg.seek(7)
        self.assertEqual(seg.read(4), b"orld")

    def test_seek_behavior(self):
        """Test seek positions"""
        seg = Segments(self.manifest_path)
        # Seek to middle and verify position
        seg.seek(6)
        self.assertEqual(seg.tell(), 6)

        # Relative seek
        seg.seek(2, 1)  # Move +2 from current position (6 → 8)
        self.assertEqual(seg.tell(), 8)

    def test_edge_cases(self):
        """Test out-of-bounds and empty reads"""
        seg = Segments(self.manifest_path)
        # Read past EOF
        seg.seek(10)
        self.assertEqual(seg.read(10), b"d")  # Only "d" remains

        # Empty read
        seg.seek(0)
        self.assertEqual(seg.read(0), b"")

    def test_segment_file_handling(self):
        """Verify files are opened/closed properly"""
        seg = Segments(self.manifest_path)
        # First access should open files
        seg.read(1)
        self.assertIsNotNone(seg.parts[0][3])  # part1.txt file handle

        # Close and verify handles are cleared
        seg.close()
        self.assertIsNone(seg.parts[0][3])

    def test_segment_read(self):
        seg = Segments(self.manifest_path)
        self.assertEqual(seg.read(5), b"Hello")
        self.assertEqual(seg.read(-1), b" World")
        self.assertEqual(seg.tell(), 11)
        seg.close()
        seg = Segments(self.manifest_path)
        with seg:
            self.assertEqual(seg.read(3), b"Hel")
            self.assertEqual(seg.read(4), b"lo W")
            self.assertEqual(seg.read(-1), b"orld")

    @classmethod
    def tearDownClass(cls):
        # Cleanup temporary files
        for f in os.listdir(cls.temp_dir):
            os.remove(os.path.join(cls.temp_dir, f))
        os.rmdir(cls.temp_dir)


if __name__ == "__main__":
    unittest.main()
