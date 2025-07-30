import pickle
import os
import yaml
import time
import glob
import shutil
import sys


def get_file_size(file_path: str) -> float:
    """
    Get the size of a file in megabytes (MB).
    
    Args:
        file_path (str): Path to the file.
    
    Returns:
        float: Size of the file in MB. Rounded to nearest integer if >1 MB, else rounded to 2 decimals.
               Returns -1.0 if the file is not accessible.
    """
    try:
        file_size = os.path.getsize(file_path) / 1024 / 1024  # in MB
        return round(file_size) if file_size > 1 else round(file_size, 2)
    except (OSError, FileNotFoundError) as e:
        print(f"Error accessing file: {e}")
        return -1.0



def load_yaml(path):
    """Load a YAML file."""
    with open(path, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_pickle(path):
    """Load a pickle file."""
    with open(path, 'rb') as f:
        return pickle.load(f)


def save_pickle(data, path):
    """Save data to a pickle file."""
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def load_text_lines(path):
    """Load text file as list of lines."""
    with open(path, 'r') as f:
        return [line.rstrip('\n') for line in f]


def hprint(msg, placeholder=50):
    """print a centered message with dashes around."""
    if isinstance(msg, str):
        
        if len(msg) > placeholder:
            print(msg)
        else:
            placeholder -= len(msg)
            left_placeholder = int(placeholder / 2)
            right_placeholder = int(placeholder - left_placeholder)
            print('\n' + '-' * left_placeholder + msg +
                '-' * right_placeholder)
    else:
        print('content should be str')


def start_timer(task_name="it"):
    """Start a timer and return a handle."""

    return time.time(), task_name


def end_timer(start_info):
    """Stop the timer and print the elapsed time."""
    start_time, task_name = start_info
    end_time = time.time()
    elapsed = end_time - start_time

    if elapsed > 3600:
        print(
            f"{task_name} cost: {int(elapsed // 3600)} hour {int(elapsed % 3600 // 60)} min {elapsed % 60:.1f} s"
        )
    elif elapsed > 60:
        print(f"{task_name} cost: {int(elapsed // 60)} min {elapsed % 60:.1f} s")
    else:
        print(f"{task_name} cost: {elapsed:.1f} s")

    return elapsed
    
    

def get_current_date(detail=False):
    """Get the current date as a string."""
    fmt = '%Y-%m-%d %H-%M-%S' if detail else '%Y-%m-%d'
    return time.strftime(fmt, time.localtime())



if __name__ == '__main__':

    hprint(get_current_date(detail=False))

    timer = start_timer('Testing')
    for i in range(100000000):
        pass
    end_timer(timer)