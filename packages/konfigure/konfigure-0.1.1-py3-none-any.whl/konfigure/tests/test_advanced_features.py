"""
Advanced tests for the konfigure package.

These tests cover more complex scenarios including:
- Deeply nested structures
- Lists and dictionaries
- References and circular references
- Various YAML data types
"""

import os
import tempfile
import unittest
import yaml

from konfigure import load, dump, Config
from konfigure.core import StringTemplate


class TestNestedStructures(unittest.TestCase):
    """Test deeply nested structures."""
    
    def test_deep_nesting(self):
        """Test deeply nested dictionaries."""
        config = Config({
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "level5": "deep value"
                        }
                    }
                }
            }
        })
        
        # Access deep values
        self.assertEqual(config.level1.level2.level3.level4.level5, "deep value")
        
        # Modify deep values
        config.level1.level2.level3.level4.level5 = "new deep value"
        self.assertEqual(config.level1.level2.level3.level4.level5, "new deep value")
        
        # Add new deep values
        config.level1.level2.level3.level4.new_key = "another deep value"
        self.assertEqual(config.level1.level2.level3.level4.new_key, "another deep value")
    
    def test_nested_lists(self):
        """Test nested lists within dictionaries."""
        config = Config({
            "users": [
                {"name": "Alice", "roles": ["admin", "user"]},
                {"name": "Bob", "roles": ["user"]}
            ]
        })
        
        # Access nested list values
        self.assertEqual(config.users[0].name, "Alice")
        self.assertEqual(config.users[0].roles[0], "admin")
        self.assertEqual(config.users[1].name, "Bob")
        
        # Modify nested list values
        config.users[0].roles.append("developer")
        self.assertEqual(len(config.users[0].roles), 3)
        self.assertEqual(config.users[0].roles[2], "developer")
        
        # Add new items to nested lists
        new_user = Config({"name": "Charlie", "roles": ["tester"]})
        config.users.append(new_user)
        self.assertEqual(len(config.users), 3)
        self.assertEqual(config.users[2].name, "Charlie")


class TestDataTypes(unittest.TestCase):
    """Test various YAML data types."""
    
    def test_scalar_types(self):
        """Test scalar data types."""
        config = Config({
            "string": "hello",
            "integer": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
        })
        
        self.assertEqual(config.string, "hello")
        self.assertEqual(config.integer, 42)
        self.assertEqual(config.float, 3.14)
        self.assertTrue(config.boolean)
        self.assertIsNone(config.null)
        
        # Test type conversion
        config.string = 123
        self.assertEqual(config.string, "123")  # Should be converted to StringTemplate
    
    def test_complex_types(self):
        """Test more complex data types."""
        config = Config({
            "list": [1, 2, 3],
            "dict": {"a": 1, "b": 2},
            "mixed_list": [1, "two", {"three": 3}],
            "list_of_dicts": [{"a": 1}, {"b": 2}],
        })
        
        self.assertEqual(config.list, [1, 2, 3])
        self.assertEqual(config.dict.a, 1)
        self.assertEqual(config.mixed_list[2].three, 3)
        self.assertEqual(config.list_of_dicts[1].b, 2)


class TestYAMLFeatures(unittest.TestCase):
    """Test YAML-specific features."""
    
    def test_multiline_strings(self):
        """Test multiline strings in YAML."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
            temp_path = temp.name
            temp.write(b"""
literal_block: |
  This is a literal block.
  Line breaks are preserved.
  Multiple lines.

folded_block: >
  This is a folded block.
  Line breaks become spaces.
  Multiple lines become one.
""")
        
        try:
            config = load(temp_path)
            
            # Check literal block (preserves line breaks)
            self.assertEqual(config.literal_block, "This is a literal block.\nLine breaks are preserved.\nMultiple lines.\n")
            
            # Check folded block (line breaks become spaces)
            self.assertEqual(config.folded_block, "This is a folded block. Line breaks become spaces. Multiple lines become one.\n")
            
            # Test rendering templates in multiline strings
            config.literal_block = "Line 1: {{ var1 }}\nLine 2: {{ var2 }}"
            rendered = config.literal_block.render(var1="Value 1", var2="Value 2")
            self.assertEqual(rendered, "Line 1: Value 1\nLine 2: Value 2")
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_anchors_and_aliases(self):
        """Test YAML anchors and aliases."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
            temp_path = temp.name
            temp.write(b"""
default_settings: &default
  timeout: 30
  retry: 3
  logging: true

service1:
  <<: *default
  name: "Service 1"
  port: 8001

service2:
  <<: *default
  name: "Service 2"
  port: 8002
  timeout: 60  # Override the default
""")
        
        try:
            config = load(temp_path)
            
            # Check that anchors and aliases were properly resolved
            self.assertEqual(config.service1.timeout, 30)
            self.assertEqual(config.service1.retry, 3)
            self.assertTrue(config.service1.logging)
            
            # Check overridden values
            self.assertEqual(config.service2.timeout, 60)
            self.assertEqual(config.service2.retry, 3)
            
            # Modify a value and check that it doesn't affect the anchor
            config.service1.timeout = 45
            self.assertEqual(config.service1.timeout, 45)
            self.assertEqual(config.service2.timeout, 60)
            self.assertEqual(config.default_settings.timeout, 30)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestTemplateRendering(unittest.TestCase):
    """Test advanced template rendering features."""
    
    def test_nested_templates(self):
        """Test templates with nested variables."""
        config = Config({
            "name": "{{ user.first_name }} {{ user.last_name }}",
            "greeting": "Hello, {{ name }}!",
            "message": "{{ greeting }} Welcome to {{ app.name }} version {{ app.version }}."
        })
        
        variables = {
            "user": {"first_name": "John", "last_name": "Doe"},
            "app": {"name": "My App", "version": "1.0.0"}
        }
        
        # Test rendering individual templates
        self.assertEqual(config.name.render(**variables), "John Doe")
        
        # Add the rendered name to the context for the greeting
        variables["name"] = "John Doe"
        self.assertEqual(config.greeting.render(**variables), "Hello, John Doe!")
        
        # Test rendering a template that references other templates
        variables["greeting"] = "Hello, John Doe!"
        self.assertEqual(
            config.message.render(**variables),
            "Hello, John Doe! Welcome to My App version 1.0.0."
        )
    
    def test_template_control_structures(self):
        """Test Jinja2 control structures in templates."""
        config = Config({
            "conditional": "{% if condition %}True{% else %}False{% endif %}",
            "loop": "{% for item in items %}{{ item }}{% if not loop.last %}, {% endif %}{% endfor %}",
            "filter": "{{ value | upper }}",
            "complex": """
{% for user in users %}
  {% if user.active %}
  {{ user.name | title }} is active.
  {% else %}
  {{ user.name | title }} is inactive.
  {% endif %}
{% endfor %}
"""
        })
        
        # Test conditional rendering
        self.assertEqual(config.conditional.render(condition=True), "True")
        self.assertEqual(config.conditional.render(condition=False), "False")
        
        # Test loop rendering
        self.assertEqual(config.loop.render(items=["a", "b", "c"]), "a, b, c")
        
        # Test filter rendering
        self.assertEqual(config.filter.render(value="hello"), "HELLO")
        
        # Test complex template with loops, conditionals, and filters
        variables = {
            "users": [
                {"name": "alice", "active": True},
                {"name": "bob", "active": False},
                {"name": "charlie", "active": True}
            ]
        }
        expected = """
  Alice is active.
  Bob is inactive.
  Charlie is active.
"""
        self.assertEqual(config.complex.render(**variables), expected)


if __name__ == "__main__":
    unittest.main()
