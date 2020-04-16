# Getting Started:
## Downloading Package
There are multiple ways to retrieve the package. The two that we will
discuss are downloading as a zip and using git.

### Downloading Zip
On the main web page for the repo, click "clone or download". In the
dropdown, click "download zip". Move the downloaded zip file to a
desired location on your system and extract.

### Downloading with Git
From a directory you wish to have the package, use the following
command:

```
git clone https://github.com/mmonarch/utoledo_pv_modeling.git

```

## Installing Package
Navigate to base directory of the package (you can Verify by checking
that the setup.py file is located in the location). The following
command will install the ut_pv package for your entire system (note,
you may need administrative privilages or root access):

```
python setup.py install

```

Optionally, you can install only for the current user using the
following command;

```
python setup.py install --user

```

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

