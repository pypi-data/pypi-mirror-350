# Pigeon Config

Pigeon Config is a tool for managing a set of YAML configuration files. It is based on Adobe's [himl](https://github.com/adobe/himl), and compiles a collection of YAML files, merging keys as necessary. It outputs a separate YAML file for each top level key. It can also check if the compiled YAML files need to be updated.

## Command Line Usage

```
usage: pigeon-config [-h] [-c] [-r ROOT] [-o OUTPUT] [leaf]

positional arguments:
  leaf                  The leaf directory to use.

options:
  -h, --help            show this help message and exit
  -c, --check           Check if pigeon-config should be run again.
  -r ROOT, --root ROOT  The path to use as the current working directory.
  -o OUTPUT, --output OUTPUT
                        The directory to output the configuration files to.

```

Pigeon Config has two modes, 1. to compile the configuration (the default), and 2. to check if the configuration needs to be recompiled.

### Compiling

When compiling a configuration, Pigeon Config will find all YAML files in the directory tree starting from the specified leaf directory, and stopping one level short of the current directory, or the root directory if specified. The compiled output is then saved to a directory named `materialized` relative to the current directory, or to the output directory if specified.

### Checking

To check if a configuration should be recompiled, Pigeon Config can be run with the `--check` option. In this case, Pigeon Config checks if any files in the current directory, or root directory if specified, are newer than the files in the output directory, again defaulting to `materialized`. In this mode, Pigeon Config will output the files that are newer than the output, and exits with a nonzero exit code when such files exist. Note: the way the root directory option is treated is different in the configuration checking mode, than in the compiling mode.

## Removing Keys

To remove keys from the compiled configuration, they may be set to `null`. This removal is performed at all levels.

## Installing

Pigeon Config can be installed from the Python Package Index using `pip install pigeon-config`.

## Docker

A Dockerfile is also provided so Pigeon Config can be run inside a Docker container, and included as part of a Docker compose file.
