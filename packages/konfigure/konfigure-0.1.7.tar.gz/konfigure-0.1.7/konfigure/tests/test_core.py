"""
Tests for the konfigure package.
"""

import os
import tempfile
import unittest
import yaml

from konfigure import load, dump, Config
from konfigure.core import StringTemplate


class TestStringTemplate(unittest.TestCase):
    """Test the StringTemplate class."""
    
    def test_init(self):
        """Test initialization."""
        st = StringTemplate("Hello {{ name }}")
        self.assertEqual(st.raw_string, "Hello {{ name }}")
        
    def test_render(self):
        """Test rendering templates."""
        st = StringTemplate("Hello {{ name }}")
        self.assertEqual(st.render(name="World"), "Hello World")
        
    def test_str(self):
        """Test string conversion."""
        st = StringTemplate("Hello {{ name }}")
        self.assertEqual(str(st), "Hello {{ name }}")
        
    def test_repr(self):
        """Test representation."""
        st = StringTemplate("Hello {{ name }}")
        self.assertEqual(repr(st), "StringTemplate('Hello {{ name }}')")
        
    def test_eq(self):
        """Test equality."""
        st1 = StringTemplate("Hello {{ name }}")
        st2 = StringTemplate("Hello {{ name }}")
        st3 = StringTemplate("Goodbye {{ name }}")
        self.assertEqual(st1, st2)
        self.assertNotEqual(st1, st3)
        self.assertEqual(st1, "Hello {{ name }}")


class TestConfig(unittest.TestCase):
    """Test the Config class."""
    
    def test_init(self):
        """Test initialization."""
        config = Config({"a": {"b": "c"}, "d": "e"})
        self.assertEqual(config.a.b, "c")
        self.assertEqual(config.d, "e")
        
    def test_getattr(self):
        """Test attribute access."""
        config = Config({"a": {"b": "c"}, "d": "e"})
        self.assertEqual(config.a.b, "c")
        self.assertEqual(config.d, "e")
        self.assertIsNone(config.f)
        
    def test_setattr(self):
        """Test setting attributes."""
        config = Config()
        config.a = {"b": "c"}
        config.d = "e"
        self.assertEqual(config.a.b, "c")
        self.assertEqual(config.d, "e")
        
        # Test updating nested attributes
        config.a.b = "f"
        self.assertEqual(config.a.b, "f")
        
    def test_string_template_conversion(self):
        """Test that strings are converted to StringTemplate."""
        config = Config({"a": "Hello {{ name }}"})
        self.assertIsInstance(config.a, StringTemplate)
        self.assertEqual(config.a.render(name="World"), "Hello World")
        
    def test_to_serializable(self):
        """Test conversion to serializable format."""
        config = Config({"a": {"b": "c"}, "d": "e"})
        serialized = config._to_serializable()
        self.assertEqual(serialized, {"a": {"b": "c"}, "d": "e"})


class TestLoadDump(unittest.TestCase):
    """Test the load and dump functions."""
    
    def test_load_nonexistent(self):
        """Test loading a non-existent file."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
            temp_path = temp.name
        
        try:
            os.unlink(temp_path)  # Ensure the file doesn't exist
            config = load(temp_path)
            self.assertEqual(config, {})
            self.assertEqual(config._yaml_path, os.path.abspath(temp_path))
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_load_dump(self):
        """Test loading and dumping a file."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
            temp_path = temp.name
            temp.write(b"""
a:
  b: c
d: e
""")
        
        try:
            config = load(temp_path)
            self.assertEqual(config.a.b, "c")
            self.assertEqual(config.d, "e")
            
            # Modify the config
            config.a.b = "f"
            config.g = "h"
            
            # Dump to a new file
            new_temp_path = temp_path + ".new"
            dump(config, new_temp_path)
            
            # Load the new file and verify
            new_config = load(new_temp_path)
            self.assertEqual(new_config.a.b, "f")
            self.assertEqual(new_config.d, "e")
            self.assertEqual(new_config.g, "h")
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            if os.path.exists(temp_path + ".new"):
                os.unlink(temp_path + ".new")
    
    def test_dump_to_original_path(self):
        """Test dumping to the original path."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
            temp_path = temp.name
            temp.write(b"""
a:
  b: c
d: e
""")
        
        try:
            config = load(temp_path)
            config.a.b = "f"
            dump(config)  # No path provided, should use the original
            
            # Load again and verify
            new_config = load(temp_path)
            self.assertEqual(new_config.a.b, "f")
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestUsageExamples(unittest.TestCase):
    """Test the usage examples from the requirements."""
    
    def test_example(self):
        """Test the example from the requirements."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
            temp_path = temp.name
            temp.write(b"""
a:
  b: c
c: d
""")
        
        try:
            config = load(temp_path)
            self.assertEqual(config.a, {"b": "c"})
            self.assertEqual(config.a.b, "c")
            
            config.a.b = "g"
            self.assertEqual(config.a.b, "g")
            
            config.a = True
            self.assertEqual(config.a, True)
            
            dump(config)
            
            # Load again and verify
            new_config = load(temp_path)
            self.assertEqual(new_config.a, True)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_render_example(self):
        """Test the render example from the requirements."""
        config = Config({
            "a": {
                "b": "Hello {{ name }}"
            }
        })
        
        self.assertEqual(config.a.b.render(name="World"), "Hello World")


if __name__ == "__main__":
    unittest.main()
