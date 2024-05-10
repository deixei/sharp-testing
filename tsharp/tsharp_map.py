# Mapping tool for variable and configurations
## tsharp_map.py variables --set <collection_type> --config_folder <config_folder> --dataset <dataset> --verbose <v>

import os
import yaml
import argparse
from tsharp_constants import EnvironmentVariables

def parse_args():
    """
    Parse command line arguments and return the parsed arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    EnvironmentVariables.subscription_id

    script_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.join(script_dir, "..")

    default_config_folder = os.path.join(parent_dir, "configurations")

    parser = argparse.ArgumentParser(description='Sharp Mapping from deixei')
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    # Variables command
    parser_variables = subparsers.add_parser('variables', help='Variables help')
    parser_variables.add_argument('--set', type=str, required=True, help='Set collection type')

    # Configs command
    parser_configs = subparsers.add_parser('configs', help='Configs help')
    parser_configs.add_argument('--set', type=str, required=True, help='Set collection type')

    # Testme command
    parser_testme = subparsers.add_parser('testme', help='Testme help')
    parser_testme.add_argument('--set', type=str, required=True, help='Set collection type')

    parser.add_argument('--config_folder', type=str, default=default_config_folder, help='Configuration folder')
    parser.add_argument('--dataset', type=str, default='data_set_1', help='Configuration Dataset folder name')
    parser.add_argument('--verbose', type=str, default="v", help='Verbose output')

    return parser.parse_args()

def main():
    """
    Entry point of the program.
    
    Parses command line arguments, validates the input, and runs the main logic.
    """
    args = parse_args()

    if args.config_folder is None:
        raise ValueError("config_folder is not set")
    
    if os.path.exists(args.config_folder) is False:
        raise ValueError("config_folder does not exist")
    
    if args.dataset is None:
        raise ValueError("dataset is not set")

if __name__ == "__main__":
    main()