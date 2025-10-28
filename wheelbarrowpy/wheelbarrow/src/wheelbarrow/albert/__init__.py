from functools import cache
from pickle import UnpicklingError

@cache
def pickle_memoize(fname, creation_callback, verbose=False):
    """
    Try to read data from the pickle at `fname`; if it doesn't exist, save the
    output of `creation_callback` to `fname` as a pickle. Also memoizes in mem
    with functools.cache.
    """
    from pickle import load, dump
    if verbose: print(f"pickle_memoize: looking for pickle file '{fname}'...")
    try:
        with open(fname, 'rb') as rf:
            if verbose: print(f"    found pickle file '{fname}'! :)) loading it...")
            return load(rf)
    except (FileNotFoundError, UnpicklingError):
        if verbose: print(f"    did not find pickle file '{fname}' or it was corrupted :( making it...")
        got = creation_callback()
        try:
            with open(fname, 'wb') as wf:
                dump(got, wf)
            if verbose: print(f"    successfully made pickle file '{fname}'! :)")
        except TypeError as err:
            from sys import stderr
            if verbose: print("    couldn't pickle the object! :(", err, file=stderr)
        return got

def style_matplotlib(plt):
    plt.rcParams.update({
        'figure.dpi': 200,
        'savefig.dpi': 200,
        'font.family': 'serif',
        'axes.titlesize': 18,
        'axes.titleweight': 'bold',
        'font.size': 18,
        'font.weight': 'bold',
        'axes.labelweight': 'bold',
    })

def parse_argv(config):
    '''
    lightweight parser which just reads argv. (LLM implement this)
    - if any of the args is '--help', dump the config keys and default values/types
    - otherwise, parse all the command line arguments. for each argument (--key value), update the config dict recursively because it may be --nested.like.this. parse the value to the type in the config dict
    return config
    '''
    import sys
    
    def print_config_help(cfg, prefix=""):
        """Recursively print configuration help."""
        for key, value in cfg.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                print(f"  --{full_key}.*")
                print_config_help(value, full_key)
            else:
                print(f"  --{full_key} <{type(value).__name__}> (default: {value})")
    
    def convert_type(val_str, target_type):
        """Convert string value to target type."""
        if target_type == bool:
            return val_str.lower() in ('true', '1', 'yes', 'on')
        elif target_type == int:
            return int(val_str)
        elif target_type == float:
            return float(val_str)
        elif target_type == list:
            return val_str.split(',')
        else:
            return val_str
    
    def auto_convert_type(val_str):
        """Auto-detect and convert string value to appropriate type."""
        # Boolean
        if val_str.lower() in ('true', 'false'):
            return val_str.lower() == 'true'
        # Integer
        try:
            return int(val_str)
        except ValueError:
            pass
        # Float
        try:
            return float(val_str)
        except ValueError:
            pass
        # List (comma-separated)
        if ',' in val_str:
            return val_str.split(',')
        # String
        return val_str
    
    def set_nested_config(cfg, key, value_str):
        """Set nested configuration value."""
        parts = key.split('.')
        current = cfg
        
        # Navigate to the parent dict
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set the final value
        final_key = parts[-1]
        original_value = current.get(final_key)
        
        if original_value is not None:
            value = convert_type(value_str, type(original_value))
        else:
            value = auto_convert_type(value_str)
        current[final_key] = value
    
    args = sys.argv[1:]
    
    # Help functionality
    if '--help' in args or '-h' in args:
        print("Available configuration options:")
        print("=" * 50)
        print_config_help(config)
        sys.exit(0)
    
    # Parse arguments
    i = 0
    while i < len(args):
        if args[i].startswith('--'):
            key = args[i][2:]  # Remove --
            if i + 1 < len(args) and not args[i + 1].startswith('--'):
                value_str = args[i + 1]
                i += 2
            else:
                # Boolean flag
                value_str = 'True'
                i += 1
            
            # Handle nested keys
            if '.' in key:
                set_nested_config(config, key, value_str)
            else:
                # Convert value to appropriate type  
                original_value = config.get(key)
                if original_value is not None:
                    value = convert_type(value_str, type(original_value))
                else:
                    value = auto_convert_type(value_str)
                config[key] = value
        else:
            i += 1

    return config

def increment_version(key):
    '''
    Read .version_numbers file, increment the version for the given key, and return key_vN.
    If the key doesn't exist, start at v0.

    File format: newline-separated lines with "key value" where value is an int.

    Args:
        key: The key to increment

    Returns:
        String formatted as "key_vN" where N is the new version number
    '''
    from pathlib import Path

    version_file = Path('.version_numbers')
    versions = {}

    # Read existing versions if file exists
    if version_file.exists():
        with open(version_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) == 2:
                        versions[parts[0]] = int(parts[1])

    # Get current version or start at -1 (so after increment it's 0)
    current_version = versions.get(key, -1)
    new_version = current_version + 1
    versions[key] = new_version

    # Write back all versions
    with open(version_file, 'w') as f:
        for k, v in sorted(versions.items()):
            f.write(f"{k} {v}\n")

    return f"{key}.{new_version}" if len(key) > 0 and key[-1].isdigit() else f"{key}_v{new_version}"