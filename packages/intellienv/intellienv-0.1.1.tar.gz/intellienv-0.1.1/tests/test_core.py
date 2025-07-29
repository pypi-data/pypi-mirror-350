import os
import sys
import unittest
import tempfile
from unittest.mock import patch
import io
import json

#Add the parent directory to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intellienv.core import (
    _str_to_bool, 
    _smart_match, 
    _expand_env_vars,
    _debug_log,
    get_env,
    load_env,
    load_env_profile,
    validate_env_schema,
    generate_env_template
)


class TestStrToBool(unittest.TestCase):
    """Test string to boolean conversion."""
    
    def test_true_values(self):
        """Test values that should convert to True."""
        true_values = ["true", "True", "TRUE", "yes", "Yes", "YES", "1", "on", "On", "ON"]
        for value in true_values:
            with self.subTest(value=value):
                self.assertTrue(_str_to_bool(value))
    
    def test_false_values(self):
        """Test values that should convert to False."""
        false_values = ["false", "False", "FALSE", "no", "No", "NO", "0", "off", "Off", "OFF", "anything_else"]
        for value in false_values:
            with self.subTest(value=value):
                self.assertFalse(_str_to_bool(value))


class TestSmartMatch(unittest.TestCase):
    """Test smart matching functionality."""
    
    def test_exact_match(self):
        """Test exact match case."""
        choices = ["Development", "Production", "Staging"]
        self.assertEqual(_smart_match("Development", choices), "Development")
    
    def test_case_insensitive_match(self):
        """Test case-insensitive match."""
        choices = ["Development", "Production", "Staging"]
        self.assertEqual(_smart_match("development", choices), "Development")
        self.assertEqual(_smart_match("PRODUCTION", choices), "Production")
    
    def test_substring_match(self):
        """Test substring match."""
        choices = ["Development", "Production", "Staging"]
        self.assertEqual(_smart_match("dev", choices), "Development")
        self.assertEqual(_smart_match("prod", choices), "Production")
    
    def test_invalid_value(self):
        """Test invalid value."""
        choices = ["Development", "Production", "Staging"]
        with self.assertRaises(ValueError):
            _smart_match("invalid", choices)
    
    def test_ambiguous_match(self):
        """Test ambiguous match."""
        choices = ["Development", "DevOps", "Developer"]
        with self.assertRaises(ValueError):
            _smart_match("dev", choices)


class TestExpandEnvVars(unittest.TestCase):
    """Test environment variable expansion."""
    
    def setUp(self):
        """Set up test environment."""
        os.environ["TEST_VAR"] = "test_value"
        os.environ["NESTED_VAR"] = "nested_${TEST_VAR}"
    
    def tearDown(self):
        """Tear down test environment."""
        for key in ["TEST_VAR", "NESTED_VAR"]:
            if key in os.environ:
                del os.environ[key]
    
    def test_no_vars(self):
        """Test string with no variables."""
        self.assertEqual(_expand_env_vars("no variables"), "no variables")
    
    def test_not_string(self):
        """Test non-string input."""
        self.assertEqual(_expand_env_vars(123), 123)
        self.assertEqual(_expand_env_vars(None), None)
    
    def test_curly_brace_syntax(self):
        """Test ${VAR} syntax."""
        self.assertEqual(_expand_env_vars("Value: ${TEST_VAR}"), "Value: test_value")
    
    def test_simple_syntax(self):
        """Test $VAR syntax."""
        self.assertEqual(_expand_env_vars("Value: $TEST_VAR"), "Value: test_value")
    
    def test_missing_var(self):
        """Test missing variable."""
        self.assertEqual(_expand_env_vars("Value: ${MISSING_VAR}"), "Value: ")
    
    def test_multiple_vars(self):
        """Test multiple variables."""
        self.assertEqual(
            _expand_env_vars("Values: ${TEST_VAR} and $TEST_VAR"),
            "Values: test_value and test_value"
        )


class TestDebugLog(unittest.TestCase):
    """Test debug logging functionality."""
    
    def test_debug_log_enabled(self):
        """Test logging when enabled."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        _debug_log("Test message", True)
        self.assertEqual(captured_output.getvalue(), "Test message\n")
        
        #Reset stdout
        sys.stdout = sys.__stdout__
    
    def test_debug_log_disabled(self):
        """Test logging when disabled."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        _debug_log("Test message", False)
        self.assertEqual(captured_output.getvalue(), "")
        
        #Reset stdout
        sys.stdout = sys.__stdout__


class TestGetEnv(unittest.TestCase):
    """Test get_env function."""
    
    def setUp(self):
        """Set up test environment."""
        os.environ["TEST_STR"] = "test_value"
        os.environ["TEST_INT"] = "42"
        os.environ["TEST_FLOAT"] = "42.5"
        os.environ["TEST_BOOL_TRUE"] = "true"
        os.environ["TEST_BOOL_FALSE"] = "false"
        os.environ["TEST_CHOICE"] = "dev"
    
    def tearDown(self):
        """Tear down test environment."""
        keys = ["TEST_STR", "TEST_INT", "TEST_FLOAT", "TEST_BOOL_TRUE", 
                "TEST_BOOL_FALSE", "TEST_CHOICE", "TEST_MIN"]
        for key in keys:
            if key in os.environ:
                del os.environ[key]
    
    def test_get_string(self):
        """Test getting string value."""
        self.assertEqual(get_env("TEST_STR"), "test_value")
    
    def test_get_int(self):
        """Test getting integer value."""
        self.assertEqual(get_env("TEST_INT", cast_type=int), 42)
    
    def test_get_float(self):
        """Test getting float value."""
        self.assertEqual(get_env("TEST_FLOAT", cast_type=float), 42.5)
    
    def test_get_bool(self):
        """Test getting boolean value."""
        self.assertTrue(get_env("TEST_BOOL_TRUE", cast_type=bool))
        self.assertFalse(get_env("TEST_BOOL_FALSE", cast_type=bool))
    
    def test_default_value(self):
        """Test default value."""
        self.assertEqual(get_env("NON_EXISTENT", default="default"), "default")
    
    def test_required(self):
        """Test required value."""
        with self.assertRaises(KeyError):
            get_env("NON_EXISTENT", required=True)
    
    def test_cast_error(self):
        """Test cast error."""
        os.environ["TEST_BAD_INT"] = "not_an_int"
        with self.assertRaises(ValueError):
            get_env("TEST_BAD_INT", cast_type=int)
    
    def test_choices(self):
        """Test choices validation."""
        choices = ["development", "production", "staging"]
        self.assertEqual(get_env("TEST_CHOICE", choices=choices), "development")
        
        os.environ["TEST_BAD_CHOICE"] = "invalid"
        with self.assertRaises(ValueError):
            get_env("TEST_BAD_CHOICE", choices=choices)
    
    def test_min_value(self):
        """Test minimum value validation."""
        os.environ["TEST_MIN"] = "5"
        self.assertEqual(get_env("TEST_MIN", cast_type=int, min_value=1), 5)
        
        os.environ["TEST_MIN"] = "5"
        with self.assertRaises(ValueError):
            get_env("TEST_MIN", cast_type=int, min_value=10)


class TestLoadEnv(unittest.TestCase):
    """Test load_env function."""
    
    def setUp(self):
        """Set up test environment."""
        #Clear relevant environment variables
        for key in list(os.environ.keys()):
            if key.startswith("TEST_"):
                del os.environ[key]
    
    def test_load_env_basic(self):
        """Test basic env file loading."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write("""
#This is a comment
TEST_VAR1=value1
TEST_VAR2=value2
""")
            temp_path = temp_file.name
        
        try:
            load_env(temp_path, logging=False)
            self.assertEqual(os.environ["TEST_VAR1"], "value1")
            self.assertEqual(os.environ["TEST_VAR2"], "value2")
        finally:
            os.unlink(temp_path)
    
    def test_load_env_quoted_values(self):
        """Test loading with quoted values."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write("""
TEST_QUOTED_DOUBLE="double quoted value"
TEST_QUOTED_SINGLE='single quoted value'
""")
            temp_path = temp_file.name
        
        try:
            load_env(temp_path, logging=False)
            self.assertEqual(os.environ["TEST_QUOTED_DOUBLE"], "double quoted value")
            self.assertEqual(os.environ["TEST_QUOTED_SINGLE"], "single quoted value")
        finally:
            os.unlink(temp_path)
    
    def test_load_env_comments(self):
        """Test handling of comments."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write("""
TEST_WITH_COMMENT=value #this is a comment
""")
            temp_path = temp_file.name
        
        try:
            load_env(temp_path, logging=False)
            self.assertEqual(os.environ["TEST_WITH_COMMENT"], "value")
        finally:
            os.unlink(temp_path)
    
    def test_load_env_variable_expansion(self):
        """Test variable expansion."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write("""
TEST_BASE=base_value
TEST_EXPANDED=${TEST_BASE}_expanded
""")
            temp_path = temp_file.name
        
        try:
            load_env(temp_path, logging=False)
            self.assertEqual(os.environ["TEST_EXPANDED"], "base_value_expanded")
        finally:
            os.unlink(temp_path)
    
    def test_load_env_override(self):
        """Test override option."""
        os.environ["TEST_OVERRIDE"] = "original"
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write("TEST_OVERRIDE=new")
            temp_path = temp_file.name
        
        try:
            #Without override
            load_env(temp_path, override=False, logging=False)
            self.assertEqual(os.environ["TEST_OVERRIDE"], "original")
            
            #With override
            load_env(temp_path, override=True, logging=False)
            self.assertEqual(os.environ["TEST_OVERRIDE"], "new")
        finally:
            os.unlink(temp_path)
    
    def test_file_not_found(self):
        """Test file not found error."""
        with self.assertRaises(FileNotFoundError):
            load_env("non_existent_file.env")


class TestLoadEnvProfile(unittest.TestCase):
    """Test load_env_profile function."""
    
    def setUp(self):
        """Set up test environment."""
        #Save original environment to restore later
        self.original_environ = os.environ.copy()
        
        #Clear test variables
        for key in list(os.environ.keys()):
            if key.startswith("TEST_"):
                del os.environ[key]
        
        #Create a temp directory
        self.temp_dir = tempfile.mkdtemp()
        
        #Create base env file
        self.base_file = os.path.join(self.temp_dir, ".env")
        with open(self.base_file, 'w') as f:
            f.write("TEST_BASE=base_value\nTEST_OVERRIDE=base_override\n")
        
        #Create profile files
        self.dev_file = os.path.join(self.temp_dir, ".env.dev")
        with open(self.dev_file, 'w') as f:
            f.write("TEST_DEV=dev_value\nTEST_OVERRIDE=dev_override\n")
        
        self.prod_file = os.path.join(self.temp_dir, ".env.prod")
        with open(self.prod_file, 'w') as f:
            f.write("TEST_PROD=prod_value\nTEST_OVERRIDE=prod_override\n")
    
    def tearDown(self):
        """Tear down test environment."""
        #Clean up files
        import shutil
        shutil.rmtree(self.temp_dir)
        
        #Restore original environment
        os.environ.clear()
        os.environ.update(self.original_environ)
    
    def test_single_profile(self):
        """Test loading a single profile."""
        load_env_profile(["dev"], self.base_file, logging=False)
        
        #Check results
        self.assertEqual(os.environ.get("TEST_BASE"), "base_value")
        self.assertEqual(os.environ.get("TEST_DEV"), "dev_value")
        self.assertEqual(os.environ.get("TEST_OVERRIDE"), "dev_override")
    
    def test_multiple_profiles(self):
        """Test loading multiple profiles."""
        load_env_profile(["dev", "prod"], self.base_file, logging=False)
        
        #Check results
        self.assertEqual(os.environ.get("TEST_BASE"), "base_value")
        self.assertEqual(os.environ.get("TEST_DEV"), "dev_value")
        self.assertEqual(os.environ.get("TEST_PROD"), "prod_value")
        self.assertEqual(os.environ.get("TEST_OVERRIDE"), "prod_override")


class TestValidateEnvSchema(unittest.TestCase):
    """Test validate_env_schema function."""
    
    def setUp(self):
        """Set up test environment."""
        os.environ["TEST_STR"] = "test_value"
        os.environ["TEST_INT"] = "42"
        os.environ["TEST_CHOICE"] = "development"
    
    def tearDown(self):
        """Tear down test environment."""
        keys = ["TEST_STR", "TEST_INT", "TEST_CHOICE", "TEST_REQUIRED"]
        for key in keys:
            if key in os.environ:
                del os.environ[key]
    
    def test_valid_schema(self):
        """Test valid schema."""
        schema = {
            "TEST_STR": {"cast_type": str},
            "TEST_INT": {"cast_type": int, "min_value": 10},
            "TEST_CHOICE": {"choices": ["development", "production"]}
        }
        
        valid, result = validate_env_schema(schema, logging=False)
        self.assertTrue(valid)
        self.assertEqual(result["TEST_STR"], "test_value")
        self.assertEqual(result["TEST_INT"], 42)
        self.assertEqual(result["TEST_CHOICE"], "development")
    
    def test_invalid_schema_fail_fast(self):
        """Test invalid schema with fail fast."""
        schema = {
            "TEST_STR": {"cast_type": int},  #Will fail
            "TEST_REQUIRED": {"required": True}  #Won't be checked
        }
        
        valid, result = validate_env_schema(schema, fail_fast=True, logging=False)
        self.assertFalse(valid)
        self.assertEqual(len(result), 1)  #Only one error
        self.assertIn("TEST_STR", result)
    
    def test_invalid_schema_no_fail_fast(self):
        """Test invalid schema without fail fast."""
        schema = {
            "TEST_STR": {"cast_type": int},  #Will fail
            "TEST_REQUIRED": {"required": True}  #Will also fail
        }
        
        valid, result = validate_env_schema(schema, fail_fast=False, logging=False)
        self.assertFalse(valid)
        self.assertEqual(len(result), 2)  #Both errors
        self.assertIn("TEST_STR", result)
        self.assertIn("TEST_REQUIRED", result)


class TestGenerateEnvTemplate(unittest.TestCase):
    """Test generate_env_template function."""
    
    def setUp(self):
        """Set up test environment."""
        os.environ["TEST_VAR"] = "test_value"
    
    def test_generate_from_env(self):
        """Test generating template from environment."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            generate_env_template(temp_path)
            
            with open(temp_path, 'r') as f:
                content = f.read()
                self.assertIn("#TEST_VAR=", content)
        finally:
            os.unlink(temp_path)
    
    def test_generate_from_schema(self):
        """Test generating template from schema."""
        schema = {
            "API_KEY": {"description": "API key for service", "required": True},
            "DEBUG": {"description": "Enable debug mode", "default": "false"}
        }
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            generate_env_template(temp_path, schema)
            
            with open(temp_path, 'r') as f:
                content = f.read()
                self.assertIn("#API key for service", content)
                self.assertIn("#Required: Yes", content)
                self.assertIn("#API_KEY=", content)
                self.assertIn("#Enable debug mode", content)
                self.assertIn("#Default: false", content)
                self.assertIn("#DEBUG=", content)
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()