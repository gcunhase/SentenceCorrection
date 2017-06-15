#!/bin/sh
#
#  Shell script to generate output files from MTGRU
# in the 16 and 1000 sentences testing dataset,
# move it to the BLEU and ROUGE scores directory
# and get those scores
#

echo “Generate files“

# Python path
ROOT_DIR="./rnn/translate-mtgru/"
TEST_DIR="incompleteDataPOSTest/"
PYTHON_SCRIPT=$ROOT_DIR"translate.py"
echo $ROOT_DIR

# Generate 16 sentences test file and wait
echo "Generate 16 sentences test file"
TEST_FILE_IN_1="newstest2013_small2.en"
TEST_FILE_EXP_1="newstest2013_small2.fr"
TEST_FILE_OUT_1="newstest2013_small2_out_mtgru.txt"
SCORES_FILE_1="newstest2013_small2_out_mtgru_scores.txt"

python $PYTHON_SCRIPT --root_dir=$ROOT_DIR --test_file_in=$TEST_FILE_IN_1 --test_file_out=$TEST_FILE_OUT_1 --auto_decode=true --test_dir=$TEST_DIR

# Generate 1000 sentences test file and wait
echo "Generate 1000 sentences test file"
TEST_FILE_IN_2="newstest2013_1000.en"
TEST_FILE_EXP_2="newstest2013_1000.fr"
TEST_FILE_OUT_2="newstest2013_1000_out_mtgru.txt"
SCORES_FILE_2="newstest2013_1000_out_mtgru_scores.txt"

python $PYTHON_SCRIPT --root_dir=$ROOT_DIR --test_file_in=$TEST_FILE_IN_2 --test_file_out=$TEST_FILE_OUT_2 --auto_decode=true --test_dir=$TEST_DIR


# Scores path
SCORES_PYTHON_PATH="./metrics\ for\ translation\ performance/nlp-metrics-master/"

# Copy files to scores directory
echo "Copy files"
cp $ROOT_DIR$TEST_DIR$TEST_FILE_OUT_1 $SCORES_PYTHON_PATH"test-gwena"
cp $ROOT_DIR$TEST_DIR$TEST_FILE_OUT_2 $SCORES_PYTHON_PATH"test-gwena"


# Run python file to get BLEU and ROUGE scores
echo "Get scores"
HYP_FILE=$TEST_FILE_OUT_1
REF_FILE=$TEST_FILE_EXP_1
python $SCORES_PYTHON_PATH"tester_allSentencesOneFile.py" --hyp_file=$HYP_FILE --ref_file=$REF_FILE --scores_file=$SCORES_FILE_1

HYP_FILE=$TEST_FILE_OUT_2
REF_FILE=$TEST_FILE_EXP_2
python $SCORES_PYTHON_PATH"tester_allSentencesOneFile.py" --hyp_file=$HYP_FILE --ref_file=$REF_FILE --scores_file=$SCORES_FILE_2


exit 0

