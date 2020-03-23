# Getting Started:
## Configuration File
To use this package, a configuration file indicating locations of data
and various other settings is by default used. The title of this file
should be 'config.ini', and it should be located in the base
directory. A sample of this can be seen below:

```
[PV_DATA]
database_path=/home/mmonarch/R1_array_data/
filename_format=20%y%m%dMinuteLog.csv

```

## Running the Code
In order to run code, you must set the python path to the base
directory. This can be done using the command below:

```
export PYTHONPATH=path/to/base/directory

```

Note, this will clear anything currently on the python path. To
instead append to the python path, use the command below:

```
export PYTHONPATH=${PYTHONPATH}:path/to/base/directory

```

## Testing
To test that the package is working, try running one of the scripts in
examples.

