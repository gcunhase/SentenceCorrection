
import os
import shutil
import argparse
from timeit import default_timer as timer
import urllib
import tarfile
import gzip
# pip install progressbar2
from progressbar import ProgressBar
from datasets.utils import ensure_dir
# Global variables
pbar = None


# Compressing and decompressing .gz files: http://xahlee.info/python/gzip.html
def unzip_gz(file_gz, output_filename):
    input = gzip.GzipFile(file_gz, 'rb')
    s = input.read()
    input.close()

    output = open(output_filename, 'wb')
    output.write(s)
    output.close()
    return output_filename


# Source: https://stackoverflow.com/questions/37748105/how-to-use-progressbar-module-with-urlretrieve
def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = ProgressBar(maxval=total_size)

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


def check_for_dataset(data_dir_path):
    """ Check for data and download it if folder doesn't exist
    :param data_dir_path: Path for data directory
    :return:
    """

    directory = data_dir_path
    tar_filename = "training-giga-fren.tar"
    if not os.path.exists(directory):
        start_time_data = timer()

        os.mkdir(directory)
        print("Downloading Dataset to: {}".format(directory))

        # Download dataset and show progress bar
        tar_path = os.path.join(directory, tar_filename)
        urllib.urlretrieve("http://www.statmt.org/wmt10/training-giga-fren.tar", filename=tar_path,
                           reporthook=show_progress)

        # Extract tar file
        tar = tarfile.open(tar_path)
        data_path = tar_path.split('.tar')[0] + "/"
        tar.extractall(path=data_path)
        tar.close()

        end_time_data = timer() - start_time_data
        print("Dataset download took {} minutes\n".format(end_time_data / 60))

    else:
        print("Dataset has been found in: {}".format(directory))
    return tar_filename


def init_parse():
    parser = argparse.ArgumentParser(description='Download original WMT data.')
    parser.add_argument('--data_dir', default='IncompleteData2',
                        help='Directory for incomplete data')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = init_parse()
    data_dir_path = args.data_dir

    # Download original data
    tar_filename = check_for_dataset(data_dir_path)

    # Extract tar file
    tar_path = os.path.join(data_dir_path, tar_filename)
    tar = tarfile.open(tar_path)
    data_path = tar_path.split('.tar')[0] + "/"
    tar.extractall(path=data_path)
    tar.close()

    # Extract .en.gz in data_dir/wmt_data/
    en_tar_path = os.path.join(data_dir_path, tar_filename.split('.tar')[0], 'giga-fren.release2.fixed.en.gz')
    output_filename = os.path.join(data_dir_path, 'output1.fr')
    output_filename = unzip_gz(en_tar_path, output_filename=output_filename)

    # Remove .tar and extracted folder
    os.remove(os.path.join(data_dir_path, tar_filename))
    shutil.rmtree(os.path.join(data_dir_path, tar_filename.split('.tar')[0]))
