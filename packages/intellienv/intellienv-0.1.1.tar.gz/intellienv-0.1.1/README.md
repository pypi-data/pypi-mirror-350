# intellienv

A Python package for managing environment variables safely and conveniently.

## Overview

`intellienv` makes working with environment variables in Python applications simple, safe, and powerful. Whether you're building a small script or a large application, `intellienv` provides tools to manage your configuration effectively.

## Why Use intellienv?

- **Avoid common configuration bugs** with type validation and conversion
- **Simplify multi-environment deployments** with profile support
- **Prevent security issues** with automatic secret masking
- **Reduce boilerplate code** with intelligent environment variable handling
- **Improve developer experience** with CLI tools for environment management

## Features

- **Type Casting**: Automatically convert environment variables to the correct data type
- **Validation**: Validate environment variables against schemas
- **Multiple Environments**: Support for different environment profiles (dev, staging, prod)
- **Smart Matching**: Intelligent matching of environment variable values
- **Variable Expansion**: Support for variable references within values (like `$VAR` or `${VAR}`)
- **Secret Masking**: Automatic masking of sensitive values in logs
- **Template Generation**: Generate template .env files from schemas
- **CLI Support**: Command-line interface for all functionality

## Installation

```bash
pip install intellienv
```

## Getting Started

### Loading Environment Files

Load variables from a `.env` file:

```python
import intellienv

#Basic loading from .env file in current directory
intellienv.load_env()

#With log output (sensitive values automatically masked)
intellienv.load_env(logging=True)
#Example output: [intellienv] Loaded: API_KEY=abc***def, DEBUG=True

#From custom file with override
intellienv.load_env(path=".env.production", override=True)
```

### Getting Environment Variables with Type Safety

No more manual type conversion or validation - intellienv handles it for you:

```python
import intellienv

#String values (default)
api_url = intellienv.get_env("API_URL")

#Numbers with automatic type conversion
port = intellienv.get_env("PORT", cast_type=int)
timeout = intellienv.get_env("TIMEOUT_SECONDS", cast_type=float)

#Boolean values ("true", "yes", "1", "on" are all converted to True)
debug_mode = intellienv.get_env("DEBUG", cast_type=bool)

#With default values (used when variable isn't set)
worker_count = intellienv.get_env("WORKER_COUNT", cast_type=int, default=4)

#Required variables (raises KeyError if not found)
database_url = intellienv.get_env("DATABASE_URL", required=True)

#With validation
log_level = intellienv.get_env("LOG_LEVEL", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
max_connections = intellienv.get_env("MAX_CONNECTIONS", cast_type=int, min_value=1)
```

### Multi-Environment Configuration

Easily handle different environments (development, staging, production) with profile support:

```python
import intellienv

#Load base variables plus development-specific ones
#This loads variables from .env, then overrides with .env.dev
intellienv.load_env_profile(["dev"])

#Load multiple profiles (later profiles override earlier ones)
#Order: .env → .env.dev → .env.local
intellienv.load_env_profile(["dev", "local"])

#Useful for local development with personal overrides
intellienv.load_env_profile(["prod", "local"])
```

### Schema Validation

Define and validate your configuration schema in one place:

```python
import intellienv

#Define your application's configuration requirements
schema = {
    "DATABASE_URL": {
        "required": True,
        "description": "PostgreSQL connection string"  
    },
    "PORT": {
        "cast_type": int,
        "required": True,
        "min_value": 1024,
        "description": "HTTP server port"
    },
    "LOG_LEVEL": {
        "choices": ["DEBUG", "INFO", "WARNING", "ERROR"],
        "default": "INFO",
        "description": "Application logging level"
    },
    "DEBUG": {
        "cast_type": bool,
        "default": False,
        "description": "Enable debug mode"
    },
    "API_TIMEOUT": {
        "cast_type": int,
        "default": 30,
        "min_value": 1,
        "description": "API request timeout in seconds"
    }
}

#Validate all environment variables at once
valid, result = intellienv.validate_env_schema(schema)

if valid:
    #result contains all validated and cast values
    config = result
    app = create_app(config)
    app.run(port=config['PORT'])
else:
    #result contains error messages
    print("Configuration errors:")
    for var_name, error in result.items():
        print(f"  - {var_name}: {error}")
    exit(1)
```

### Environment Template Generation

Create template files for easier configuration:

```python
import intellienv

#Generate from schema with descriptions and defaults
intellienv.generate_env_template(".env.template", schema)
```

Generated template example:
```
#Environment Variables Template

#PostgreSQL connection string
#Required: Yes
#DATABASE_URL=

#HTTP server port
#Required: Yes
#PORT=

#Application logging level
#Default: INFO
#LOG_LEVEL=

#Enable debug mode
#Default: False
#DEBUG=

#API request timeout in seconds
#Default: 30
#API_TIMEOUT=
```

## Command Line Interface

`intellienv` includes a command-line interface for common tasks:

```bash
#Show available commands
intellienv --help
```

### Loading Environment Files

```bash
#Load from default .env file
intellienv load

#Load from custom file with override
intellienv load --file .env.prod --override

#Quiet mode (no output)
intellienv load --quiet
```

### Working with Profiles

```bash
#Load development profile
intellienv profile dev

#Load multiple profiles
intellienv profile dev local

#With custom base file
intellienv profile prod local --base configs/.env
```

### Getting Variables

```bash
#Get as string
intellienv get API_URL

#Get with type casting
intellienv get PORT --type int
intellienv get DEBUG --type bool

#With default value
intellienv get CACHE_TTL --type int --default 60
```

### Schema Validation

```bash
#Define schema in a JSON file
intellienv validate --schema app-config.json

#Continue validation after first error
intellienv validate --schema app-config.json --continue-on-error
```

Example schema JSON file:
```json
{
  "DATABASE_URL": {
    "required": true,
    "description": "PostgreSQL connection string"
  },
  "PORT": {
    "cast_type": "int",
    "required": true,
    "min_value": 1024
  },
  "DEBUG": {
    "cast_type": "bool", 
    "default": false
  }
}
```

### Template Generation

```bash
#Generate template from current environment
intellienv generate --output .env.template

#Generate from schema file
intellienv generate --schema app-config.json --output .env.template
```

## Best Practices

### Project Structure

Recommended project structure:
```
app/
├── .env                  #Base environment (committed with safe defaults)
├── .env.dev              #Development environment
├── .env.prod             #Production environment
├── .env.local            #Local overrides (in .gitignore)
├── .env.template         #Template with all variables
├── config.py             #Load and validate config 
└── app.py                #Your application code
```

Example `config.py`:

```python
import intellienv

#Load appropriate environment
intellienv.load_env_profile(["dev"])  #or "prod" based on ENV variable

#Define schema with all configuration options
schema = {
    "DATABASE_URL": {"required": True},
    "PORT": {"cast_type": int, "default": 8000},
    "DEBUG": {"cast_type": bool, "default": False},
    #... more variables
}

#Validate all at once
valid, config = intellienv.validate_env_schema(schema)
if not valid:
    for var, error in config.items():
        print(f"Config error: {var} - {error}")
    exit(1)

#Now use config dict throughout your application
```

### Sensitive Values

`intellienv` automatically masks sensitive values in logs based on variable names containing keywords like "password", "key", "token", "secret", etc.

```
#Regular output
[intellienv] Loaded: DEBUG=True, PORT=8000

#Sensitive values are masked
[intellienv] Loaded: DEBUG=True, PORT=8000, API_KEY=abc***xyz
```

## Examples

### Web Application Configuration

```python
import intellienv
import flask

#Load environment
intellienv.load_env_profile([os.environ.get("FLASK_ENV", "development")])

#Create app with configuration from environment
app = flask.Flask(__name__)
app.config["DEBUG"] = intellienv.get_env("DEBUG", cast_type=bool, default=False)
app.config["SECRET_KEY"] = intellienv.get_env("SECRET_KEY", required=True)
app.config["DATABASE_URL"] = intellienv.get_env("DATABASE_URL", required=True)
app.config["PORT"] = intellienv.get_env("PORT", cast_type=int, default=5000)

if __name__ == "__main__":
    app.run(port=app.config["PORT"])
```

### Data Processing Script

```python
import intellienv
import pandas as pd

#Load environment
intellienv.load_env()

#Get configuration
input_path = intellienv.get_env("INPUT_FILE_PATH", required=True)
output_path = intellienv.get_env("OUTPUT_FILE_PATH", required=True)
chunk_size = intellienv.get_env("CHUNK_SIZE", cast_type=int, default=10000)
debug = intellienv.get_env("DEBUG", cast_type=bool, default=False)

#Process data
df = pd.read_csv(input_path, chunksize=chunk_size)
#... processing code ...
df.to_csv(output_path)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.