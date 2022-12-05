# webpageMathPbActorCritic
Webpage for result presentation of Actor Critic method for Math problem answering

Semester project of [Emilien Seiler](mailto:emilien.seiler@epfl.ch), Master in Computational Science and Engineering at EPFL. 
Project in collaboration with Atificial Intelligence Laboratory and Natural Language Processing Laboratory at EPFL.

## Installing
To setup a miniconda environement
```
conda env create -f <path_to_environement.yml_file>
```

## Structure

This is the structure of the repository:

- `services`: python class and function for the server
  - `data_service.py`: service for data management on the server
  - `model_service.py`: service for actor and critic model management on the server
- `static`: 
  - `css`: webpage style
    - `my_style.css`: personalized style
  - `data`: dataset
    - `Math-problem-nlp.pdf`: download pdf on the webpage (to change)
    - `dev.csv`: test set
    - `train.csv`: train set
  - `img` : img dispay on the webpage
  - `js` : json file with jQuery request for on click/change action
    - `actor_model.js`: actor model related action
    - `critic_model.js`: critic model related action
    - `data_selection.js`: data selection related action
- `templates`: html template page
  - `home.html`: home page
- `requirement.txt`: python requierement
- `webpage_project.py`: script for run the webpage (see args bellow)


## Data
Data are provided from SVAMP dataset <br> 
Train dataset 3139 math problem 
Test dataset 1000 math problem

## Run
```
python3 .py --epoch <nb_epoch> --batch <batch_size> --parquet-dir <path_to_parquet> --input-channels <channel 150 or 372>
```
To train on a pretrained model use:
- `--prtrain-model`: str, name of the model file
- `--prtrain-log`: str, name of the log file
- `--prtrain-dir`: str, directory of the pretrained file

To train on a Wavenet with other hyperparameters:
- `--kernel-size`: int
- `--stack-size`: int
- `--layer-size`: int
- `--nrecept`: int, depand of the three hyperparameter look in the [report](https://github.com/eseiler18/NuclearFusion/blob/main/Report_EmilienSeiler_SemesterProject_MasterCSE.pdf) Eq. 4
- `--dropout`: float

Other parameter
- `--in-memory`: boolean, to keep all data in memory if you have enougth RAM
- `--lr`: float, initial learning rate
- `--validation`: boolean, split data in train and test set
- `--split`: float, split ratio

On lac10 cluster recommend batch-size < 12.  
Model and log of the training will be save in `project/output` at the end of the training
