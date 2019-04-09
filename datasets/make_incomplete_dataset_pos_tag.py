import argparse
import os
import csv
from collections import defaultdict
from datasets.utils import ensure_dir, get_project_path

# POS-tag for irrelevant tag selection
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

__author__ = "Gwena Cunha"


TAGS_IRRELEVANT = ['CC', 'DT', 'IN', 'LS', 'TO', 'UH']


def delete_tags(sent):
    incomplete_sentence = ''
    tokens = sent.split()  # nltk.word_tokenize(sent)
    pos_tag = nltk.pos_tag(tokens)
    for p in pos_tag:
        if p[1] in TAGS_IRRELEVANT:
            incomplete_sentence += ' '
        else:
            incomplete_sentence += p[0] + ' '

    return incomplete_sentence


def make_dataset(root_data_dir, complete_filename, incomplete_filename):
    """
    :param root_data_dir: directory to save data
    :param complete_filename: file with complete sentences
    :param incomplete_filename: file with incomplete sentences
    :return:
    """
    print("Making incomplete intention classification dataset...")

    complete_file = open(os.path.join(root_data_dir, complete_filename), 'rb')
    complete_data = complete_file.readlines()

    incomplete_file = open(os.path.join(root_data_dir, incomplete_filename), 'wb')

    incomplete_sentences = ""
    for c in complete_data:
        incomplete_sentence = delete_tags(c)
        incomplete_sentences += incomplete_sentence + "\n"

    incomplete_file.write(incomplete_sentences)
    complete_file.close()
    incomplete_file.close()
    print("Incomplete intention classification dataset completed")


def init_args():
    parser = argparse.ArgumentParser(description="Script to make intention recognition dataset")
    parser.add_argument('--root_data_dir', type=str, default=get_project_path() + "/IncompleteData2",
                        help='Directory with WMT Data')
    parser.add_argument('--incomplete_filename', default='input1.en', help='Input filename (incomplete data)')
    parser.add_argument('--complete_filename', default='output1.fr', help='Output filename (complete data)')
    return parser.parse_args()


if __name__ == '__main__':
    args = init_args()

    # Make dataset
    make_dataset(args.root_data_dir, args.complete_filename, args.incomplete_filename)
