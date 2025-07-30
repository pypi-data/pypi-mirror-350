# Copyright (c) 2024 The KUTE contributors

import numpy as np
import argparse
import shutil
import h5py

from warnings import warn
from ._ascii_logo import print_logo
from kute import __version__
from typing import Union
import os
_PATHLIKE = Union[str, bytes, os.PathLike]

def join_h5_files(output_file_path: _PATHLIKE, ignore_checks, *file_paths: _PATHLIKE) -> None:
    """Join two or more kute h5 files into a single file.

    Args:
        output_file_path (str): Path to the output file
        check
        file_paths (str): Paths to the files to be joined
    """

    # First check if more than one file is being joined
    if len(file_paths) < 2:
        raise ValueError("At least two files must be provided to join.")

    # Duplicate the first file and rename as the output file
    try:
        shutil.copy(file_paths[0], output_file_path)
    except shutil.SameFileError:
        pass

    # Open the output file in append mode
    with h5py.File(output_file_path, 'a') as output_file:

        # Get the attributes of the first file
        ff_version = output_file['information'].attrs['kute_version']
        time_units = output_file['information/units'].attrs['time']
        current_units = next(output_file['information/units'].attrs[key] for key in output_file['information/units'].attrs if key != 'time')
        
        # Check compatibility between files
        for file in file_paths[1:]:

            with h5py.File(file, 'r') as input_file:
                
                info_sec = input_file['information']
                
                if not ignore_checks:

                    # Check if the version of the files is the same
                    if info_sec.attrs['kute_version'] != ff_version:
                        warn("The kute version of the files is not the same. This could cause incompatibility issues.")
                    
                    # Check if the files have the same time units
                    if info_sec['units'].attrs['time'] != time_units:
                        # Close the output file and remove it
                        output_file.close()
                        os.remove(output_file_path)
                        raise ValueError("The time units of the files are not the same.")
                    
                    # Check if the files have the same current units
                    if next(info_sec['units'].attrs[key] for key in info_sec['units'].attrs if key != 'time') != current_units:
                        # Close the output file and remove it
                        output_file.close()
                        os.remove(output_file_path)
                        raise ValueError("The current units of the files are not the same.")

        current_key = next(key for key in output_file['timeseries'].keys() if  key != 'time')

        # Join the files
        for file in file_paths[1:]:
            
            with h5py.File(file, 'r') as input_file:
               
               # Combine the timseries datasets
               output_time = output_file['timeseries/time']
               input_time = input_file['timeseries/time']

               input_time = np.array(input_time[:].copy())

               if output_time[-1] == input_time[0]:
                    # If the first time is equal to the last time of the previous file, dont repeat it
                    output_time.resize((output_time.shape[0] + input_time.shape[0] - 1,))
                    output_time[-(input_time.shape[0]-1):] = input_time[1:]

               else:
                    output_time.resize((output_time.shape[0] + input_time.shape[0],))
                    output_time[-input_time.shape[0]:] = input_time[:]
               
               # Combine current datasets
               output_current = output_file[f'timeseries/{current_key}']
               try:
                   input_current = input_file[f'timeseries/{current_key}']
               except KeyError:
                    # Close the output file and remove it
                    output_file.close()
                    os.remove(output_file_path)
                    raise ValueError("The files do not have the same current datasets.")
               
               if len(output_current.shape) == 1:
                   output_current.resize((output_current.shape[0] + input_current.shape[0],))
               else:
                   new_size = list(output_current.shape)
                   new_size[0] += input_current.shape[0]
                   output_current.resize(tuple(new_size))
                    
               output_current[-input_current.shape[0]:] = input_current[:]
                               

def main():

    description = "Join two or more kute h5 files into a single file."

    parser = argparse.ArgumentParser(description=description)

    ## Input arguments

    parser.add_argument("-o", "--output", required=True, type=str, dest="output_file", metavar="output.h5", help = "Name of the output h5 file with the joined data")

    parser.add_argument("-f", required=True, type=str, dest="input_files", metavar="current.h5", nargs="+", help = "List of h5 binary files to join")

    parser.add_argument("--ignore_checks", action="store_true", default=False, dest="ignore_checks", help="Ignore compatibility checks between files")

    ## Load the arguments, print the KUTE logo

    args = parser.parse_args()
    print_logo()

    ## Join the files

    join_h5_files(args.output_file, args.ignore_checks, *args.input_files)

    print(f"Joined files saved to {args.output_file}.")

if __name__ == "__main__":
    main()

            
                



