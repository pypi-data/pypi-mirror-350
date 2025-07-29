import os, re

def _str_to_bool(value:str) -> bool:
    return value.lower() in ("1", "true", "yes", "on")

def _smart_match(value, choices):
    if value in choices:
        return value
    
    lower_value = value.lower()
    case_matches = [choice for choice in choices if choice.lower() == lower_value]
    if len(case_matches) == 1:
        return case_matches[0]
    
    substring_matches = [choice for choice in choices if lower_value in choice.lower()]
    if len(substring_matches) == 1:
        return substring_matches[0]
    
    raise ValueError(
        f"Invalid value '{value}'. Did not match any of: {choices}"
        + (f". Ambiguous matches: {substring_matches}" if len(substring_matches) > 1 else "")
    )

def _expand_env_vars(value: str) -> str:
    if not isinstance(value, str):
        return value
        
    var_pattern = r'\${([A-Za-z_][A-Za-z0-9_]*)}'
    matches = re.findall(var_pattern, value)
    
    result = value
    for match in matches:
        env_value = os.environ.get(match, '')
        result = result.replace(f"${{{match}}}", env_value)
    
    var_pattern = r'\$([A-Za-z_][A-Za-z0-9_]*)'
    matches = re.findall(var_pattern, result)
    
    for match in matches:
        env_value = os.environ.get(match, '')
        result = result.replace(f"${match}", env_value)
    
    return result

def _debug_log(log, logging):
    if logging:
        print(log)

def get_env(key: str, cast_type: type = str, default: any = None, 
           required: bool = False, choices: list = None, 
           min_value: int = None) -> any:
    """
    Get a loaded environment variable with type casting and default value.

    Args:
        key (str): The name of the environment variable.
        cast_type (callable): A function to cast the value to a specific type.
        default: The default value if the variable is not set.
        required (bool): If True, raise an error if the variable is not set.
        choices (list, tuple): List or tuple of allowed values. Uses smart matching.
        min_value (int): Minimum value for numeric types.

    Returns:
        The value of the environment variable, cast to the specified type.

    Raises:
        ValueError: If the variable is required and not set or cannot be cast.
        TypeError: If choices is provided but not a list or tuple.
    """

    value = os.getenv(key)

    if value is None:
        if required:
            raise KeyError(f"Required environment variable '{key}' not found.")
        return default

    if cast_type == bool:
        return _str_to_bool(value)
    
    try:
        value = cast_type(value)
    except Exception as e:
        raise ValueError(f"Could not cast env variable '{key}' to {cast_type.__name__}: {e}")

    if choices is not None:
        if not isinstance(choices, (list, tuple)):
            raise TypeError("choices parameter must be a list or tuple of allowed values.")
        value = _smart_match(value, choices)
    
    if min_value is not None and isinstance(value, (int, float)) and value < min_value:
        raise ValueError(f"Value of '{key}' must be at least {min_value}. Found: {value}")
    
    return value
    
def load_env(path: str = ".env", override: bool = False, logging: bool = False):
    """
    Loads environment variables from a .env file into os.environ.

    Args:
        path (str): Path to the .env file.
        override (bool): If True, override existing environment variables.
        logging (bool): If True, log the loaded variables.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f".env file not found at: {path}")
    
    with open(path, "r") as f:
        loaded_variables = {}

        for line_number, line in enumerate(f, 1):
            line = line.strip()
            
            if not line or line.startswith("#"):
                continue

            match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)=(.*)$', line)
            if not match:
                _debug_log(f"[intellienv] Warning: Skipping invalid line {line_number}: {line}", logging=logging)
                continue
            
            key, raw_value = match.groups()

            raw_value = raw_value.split("#", 1)[0].strip()

            if (raw_value.startswith('"') and raw_value.endswith('"')) or (raw_value.startswith("'") and raw_value.endswith("'")):
                raw_value = raw_value[1:-1]

            raw_value = _expand_env_vars(raw_value)

            if key not in os.environ or override:
                loaded_variables[key] = raw_value
                os.environ[key] = raw_value
    
    if loaded_variables and logging:
        masked_vars = {}
        secret_words = [
            'secret', 'password', 'passwd', 'pwd', 'pass',
            'token', 'api_key', 'apikey', 'key',
            'auth', 'credential', 'cred',            
            'cert', 'certificate', 'private', 'pkey', 'privkey',
            'salt', 'hash', 'cipher', 'crypt',            
            'answer', 'security_question', 'secure',            
            'access', 'jwt', 'oauth', 'session',            
            'dsn', 'connection', 'conn_str', 'database',
        ]
        for k, v in loaded_variables.items():
            if any(secret_word in k.lower() for secret_word in secret_words):
                if len(v) > 8:
                    masked_vars[k] = f"{v[:3]}{'*' * (len(v) - 6)}{v[-3:]}"
                else:
                    masked_vars[k] = "********"
            else:
                masked_vars[k] = v
        _debug_log("[intellienv] Loaded: " + ", ".join([f"{k}={v}" for k, v in masked_vars.items()]), logging=logging)

def load_env_profile(profiles: list, base_path: str = ".env", override: bool = False, logging: bool = False):
    """
    Load environment variables from profile-specific .env files.
    Will try to load both base file (.env) and profile files (.env.{profile}).

    Args:
        profiles (list, tuple): List or tuple of environment profiles (dev, staging, prod, etc.)
        base_path (str): Path to the base .env file
        override (bool): If True, override existing environment variables
        logging (bool): If True, log the loaded variables

    Raises:
        TypeError: If profiles parameter is not a list or tuple.
    """
    if not isinstance(profiles, (list, tuple)):
        raise TypeError("profiles parameter must be a list or tuple of profile names.")

    try:
        load_env(base_path, override, logging)
    except FileNotFoundError:
        if logging:
            _debug_log(f"[intellienv] Base .env file not found at: {base_path}", logging=True)

    for profile in profiles:
        profile_path = f"{base_path}.{profile}"
        try:
            load_env(profile_path, override=True, logging=logging)
        except FileNotFoundError:
            if logging:
                _debug_log(f"[intellienv] Profile .env file not found at: {profile_path}", logging=True)

def validate_env_schema(schema: dict, fail_fast: bool = True, logging: bool = False):
    """
    Validate multiple environment variables against a schema.
    
    Args:
        schema (dict): Dictionary mapping env var names to validation options
        fail_fast (bool): If True, raise exception on first error
        logging (bool): If True, log validation results
        
    Returns:
        tuple: (valid, errors_dict)
        
    Example:
        schema = {
            "PORT": {"cast_type": int, "required": True, "min_value": 1024},
            "LOG_LEVEL": {"choices": ["DEBUG", "INFO", "WARNING", "ERROR"]}
        }
    """
    errors = {}
    values = {}
    
    for key, options in schema.items():
        try:
            values[key] = get_env(key, **options)
        except (ValueError, KeyError) as e:
            errors[key] = str(e)
            if fail_fast:
                if logging:
                    _debug_log(f"[intellienv] Schema validation failed: {key} - {e}", logging=True)
                return False, errors
    
    if errors and logging:
        _debug_log(f"[intellienv] Schema validation errors: {errors}", logging=True)
        
    return len(errors) == 0, errors if errors else values

def generate_env_template(output_path: str = ".env.template", schema: dict = None):
    """
    Generate a template .env file based on the current environment or a schema.
    
    Args:
        output_path (str): Path where to write the template
        schema (dict, optional): Schema with variable descriptions
        
    Examples:
        schema = {
            "API_KEY": {"description": "API key for external service", "required": True},
            "DEBUG": {"description": "Enable debug mode", "default": "turned off"}
        }
    """
    with open(output_path, 'w') as f:
        f.write("# Environment Variables Template\n\n")
        
        if schema:
            for key, options in schema.items():
                description = options.get("description", "")
                default = options.get("default", "")
                required = options.get("required", False)
                
                if description:
                    f.write(f"#{description}\n")
                if required:
                    f.write(f"#Required: Yes\n")
                if default:
                    f.write(f"#Default: {default}\n")
                f.write(f"#{key}=\n\n")
        else:
            for key in sorted(os.environ.keys()):
                if not key.startswith(('_', 'SHELL', 'PATH', 'HOME', 'USER', 'LANG', 'TERM',
                                    'VIRTUAL_ENV', 'VSCODE', 'OLDPWD', 'PWD', 'TMPDIR', 
                                    'XPC_', 'COMMAND', 'SHLVL', 'SSH_', 'LOGNAME',
                                    'COLORTERM', 'ORIGINAL_', 'LSCOLORS', 'GIT_', 'PYDEVD_',
                                    'PAGER', 'LS_', 'LDFLAGS', 'CPPFLAGS', 'PKG_CONFIG_PATH',
                                    'rvm_', 'P9K_', 'PS1', 'ZSH', 'ZDOTDIR', 'BUNDLED_')):
                    f.write(f"#{key}=\n")

def cli():
    """
    Command-line interface for intellienv package.
    
    Run with: python -m intellienv [command] [options]
    """
    import argparse
    import sys
    import json
    
    parser = argparse.ArgumentParser(description="Smart environment variable management")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    load_parser = subparsers.add_parser("load", help="Load environment variables from .env file")
    load_parser.add_argument("--file", "-f", default=".env", help="Path to .env file")
    load_parser.add_argument("--override", "-o", action="store_true", help="Override existing variables")
    load_parser.add_argument("--quiet", "-q", action="store_true", help="Don't log loaded variables")
    
    profile_parser = subparsers.add_parser("profile", help="Load environment from profile-specific .env files")
    profile_parser.add_argument("profiles", nargs="+", help="Environment profile(s) to load")
    profile_parser.add_argument("--base", "-b", default=".env", help="Path to base .env file")
    profile_parser.add_argument("--override", "-o", action="store_true", help="Override existing variables")
    profile_parser.add_argument("--quiet", "-q", action="store_true", help="Don't log loaded variables")
    
    get_parser = subparsers.add_parser("get", help="Get environment variable value")
    get_parser.add_argument("key", help="Environment variable name")
    get_parser.add_argument("--type", "-t", default="str", choices=["str", "int", "float", "bool"], 
                           help="Type to cast to")
    get_parser.add_argument("--default", "-d", help="Default value if variable is not set")
    
    validate_parser = subparsers.add_parser("validate", help="Validate environment against schema")
    validate_parser.add_argument("--schema", "-s", required=True, help="JSON schema file path")
    validate_parser.add_argument("--quiet", "-q", action="store_true", help="Don't log validation results")
    validate_parser.add_argument("--continue-on-error", "-c", action="store_true", 
                                help="Continue validation after first error")
    
    gen_parser = subparsers.add_parser("generate", help="Generate .env template")
    gen_parser.add_argument("--output", "-o", default=".env.template", help="Output file path")
    gen_parser.add_argument("--schema", "-s", help="JSON schema file path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    if args.command == "load":
        try:
            load_env(args.file, args.override, not args.quiet)
            if not args.quiet:
                print(f"Successfully loaded environment from {args.file}")
        except Exception as e:
            print(f"Error loading environment: {e}", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == "profile":
        try:
            load_env_profile(args.profiles, args.base, args.override, not args.quiet)
            if not args.quiet:
                print(f"Successfully loaded environment from profiles: {', '.join(args.profiles)}")
        except Exception as e:
            print(f"Error loading environment profiles: {e}", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == "get":
        try:
            cast_types = {"str": str, "int": int, "float": float, "bool": _str_to_bool}
            value = get_env(
                args.key, 
                cast_type=cast_types.get(args.type, str),
                default=args.default
            )
            print(value)
        except Exception as e:
            print(f"Error getting environment variable: {e}", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == "validate":
        try:
            with open(args.schema, 'r') as f:
                schema = json.load(f)
            valid, result = validate_env_schema(
                schema, 
                fail_fast=not args.continue_on_error,
                logging=not args.quiet
            )
            if valid:
                print("Environment validation successful!")
                sys.exit(0)
            else:
                print("Environment validation failed:", file=sys.stderr)
                for key, error in result.items():
                    print(f"  {key}: {error}", file=sys.stderr)
                sys.exit(1)   
        except Exception as e:
            print(f"Error validating environment: {e}", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == "generate":
        try:
            schema = None
            if args.schema:
                with open(args.schema, 'r') as f:
                    schema = json.load(f)  
            generate_env_template(args.output, schema)
            print(f"Environment template generated at {args.output}")
            
        except Exception as e:
            print(f"Error generating template: {e}", file=sys.stderr)
            sys.exit(1)