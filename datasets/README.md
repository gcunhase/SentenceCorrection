## Dataset
WMT'15 with POS-Tagging (Third Dataset Solution)
> For other tested solutions see [Datasets wiki](https://github.com/gcunhase/SentenceCorrection-WCCI2018/wiki/The-Search-for-an-Appropriate-Incorrect-Sentences-Dataset).

## 1. Download data
### Option 1
Download incomplete data
  * Download [incomplete dataset](https://1drv.ms/f/s!Ai9Q4WIAUMvPhFhm_AHR9kMe21lpvv) (2 files: *input1.en* and *output1.fr*) to `IncompleteData` folder 
  
### Option 2
Create your own incomplete dataset
  * Automatically download [WMT dataset](http://www.statmt.org/wmt10/training-giga-fren.tar)
    ```
    python download_wmt_data.py --data_dir IncompleteData2
    ```
  * [TODO:add] make incomplete data POS-Tag
    ```
    python make_incomplete_dataset_pos_tag.py --data_dir IncompleteData2/training-giga-fren
    ```

## 2. Separate Train and Test
```
python separate_train_test_data.py --data_dir IncompleteData/train-incompleteDataPOS-15_20words --input_filename input1.en --output_filename output1.fr --train_perc 95
```
