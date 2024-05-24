# TSharp map documentation

The purpose of this tool is to load from Azure different targets, like subscriptions, regions, management groups, etc...

Then set them as variables in ADO Test hub, with that setup, generate valid configurations matrix combining multiple variables.

As your cloud setup grows so does the variables and configurations need to be updated. Having this tools executed regularly, makes it more easier to trust in audit situations. Remember that some variables like subscriptions can end up, with time, to contain invalid guids, as subscriptions are off boarded.

...

## Usage

```bash
usage: tsharp_map.py [-h] [--config_folder CONFIG_FOLDER] [--dataset DATASET] [--verbose VERBOSE] {variables,configs,testme} ...

Sharp Mapping from deixei

positional arguments:
  {variables,configs,testme}
                        Sub-command help
    variables           Variables help
    configs             Configs help
    testme              Testme help

options:
  -h, --help                        show this help message and exit
  --config_folder CONFIG_FOLDER     Configuration folder
  --dataset DATASET                 Configuration Dataset folder name
  --verbose VERBOSE                 Verbose output

```

## Author

[Marcio Parente](https://github.com/deixei) from deixei.com

To understand the overall context of this project read this book: [ENTERPRISE SOFTWARE DELIVERY: A ROADMAP FOR THE FUTURE](https://www.amazon.de/-/en/Marcio-Parente/dp/B0CXTJZJ2X/)