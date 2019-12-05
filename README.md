# ASICAKaldiNNETRecipe

##### 0. Introduction

ASICA is a research project currently in progress that aims to adapt Kaldi ASR (Automatic Speech Recognition) to recognize the speech produced by subjects with aphasia while the participate in a speech therapy task (e.g. non-word repetition). In the long term we expect that the system will be able to give feedback to the patients. In order to cope with the phonetic errors observed typically in subjects with aphasia we use the following strategy: rather than training the system to learn real (Spanish) words, which is the standard approach in ASR, we train the system to recognize a relatively large number of syllables. In the rest of this document we expalin how to install and run this Kaldi recipe. It is assumed that the reader has some basic knowledge of Kaldi (visit https://kaldi-asr.org/) and Git. 

IMPORTANT NOTE: 
ASICAKaldiNNETRecipe is a set of Python scripts developed in our lab, but it also includes various standard script that are part of kaldi. These scripts have been included in this Project in oder to faciliate instalation.

##### 1. Pre-requisites

In order to use ASICAKaldiNNETRecipe:

- A UNIX-type OS must be used.
- Kaldi is correctly installed in your system
- Python3 is correctly installed, and the following libraries: pandas, time, subprocess, os, errno, csv, shutil
- You must have a training and testing corpus (see section 7).

##### 2. Download and cheking instalation  (Work in progress):

Now you can clone to the egs folder in Kaldi. You can use this command in your terminal:

git clone https://github.com/Caliope-SpeechProcessingLab/ASICAKaldiNnetRecipe
.git


  

##### 3. Files developed by our group (remember that many other are part of Kaldi)

The main python script is: 

     run.py

Auxiliary python and shell scripts called by "run":

- config.py ---> Extract .kal information to set all kaldi folders.
- local/resetDirectory.sh ---> Reset current kaldi data directory.
- local/makeFeats.sh ---> Execute a mfcc/cvmn feature extraction of a certain group of speaker/s and a another set of testing speakers.
- local/makeLanguageModel.sh ---> Execute a kaldi recipe to prepare and create a language Model.
- local/train.sh ---> Execute the training stage for a set of training speakers. This stage is composed of: 
    * Monophone/triphone GMM.
    * Neural network (5 layers, p-norm/tahn activation functions, 5 hidden layers).
    local/test.sh ---> Execute the testing (kaldi decoding) stage for a set of testing speakers (patients) using a neural network pre-trained Model.
    
Useful python scripts:

    check_format.py ---> Check if the .kal files are well formatted.
    result_format.py ---> Extract all the resulting raw files and creates a .txt file 
                          resuming each results syllable by syllable.


##### 4. The corpora for training and testing 

The training and testing corpora are composed of a list of audio files. In our case, each audio file contains the utterances produced by a single speaker. Example filenames are:


     C001QL4_H54  
     21890QL2_M23

These codes are specific to our research project. They are interpreted as follows:

- The initial "C" indicate that the speaker is used only for training. 
- The las three letters before "_" indicate the specific test used (there are four of them: QL1, QL2, QL3, QL4)
- The letter just after "_" indicate sex H (hombre, male in Spanish) or M (mujer: female in Spanish)
- The last two numbers indicate the speaker age


##### 4.1 Audio files 

These should be:
- Mono (just one channel)
- Sampling rate should be 22050 

##### 4.2 Phonetic annotations

In order to train (and test) the system, it will be necessary to make a phonetic transcription of the utterances in the audio files. 
For each audio file, we must creat an annotation file. This file must have the same filename as the corresponding audio, and the .kal extension. This is how a .kal file looks like: 

            1.3425095235733477  1.8208389765000808  cho sa  ch_o s_a
            8.00054689313044  8.527616576060607 xe za x_e z_a
            13.704390989000565  14.131627803540477  ye ma y_e m_a
            19.760438417205425  20.261476233957108  zi fo z_i f_o
            24.894236194595347  25.234239423975374  pa ni p_a n_i
            30.19150576626139 30.9468108298102  za po du  z_a p_o d_u
            36.874888510817264  38.345799488787485  ma no ta zo m_a n_o t_a z_o
            44.439531042553945  45.681633646173246  ba rre yo b_a rr_e y_o
            50.81347861375824 52.51319796607939 se nyo ri ba  s_e ny_o r_i b_a
            58.15169004829857 58.994848481745684  tu zo t_u z_o

Each line corresponds to a single utterance in the audio file, and it is composed of four tab-separted fields: 

  - start position of the utterance in the wav file
  - end position of the utterance in the wav file 
  - syllable list (separated with spaces) 
  - phone list (this is like the previous field but the phones within each syllable are separated with "_")

In order to facilitate creating these .kal files, you can use Praat textGrids. In Praat you should create two annotation tiers, one for syllables (tier 1) and another for phonemes (tier 2) using the syntax described above (fileds 3 and for). Then you can export using our Praat script Praat2Kaldi.praat and saving them with .kal extension.

##### 4. Running a basic experiment with ASICAKaldiNNETRecipe

  - 1º: Place the audio files in the folder audio/experiment1 (if you prefer another location, you must specify in config.py)
  - 2º: Place the training .kal files in info_user/control
  - 3º  Place the testing .kal files in info_user/test 
  - 4º: In the terminal, run "check_format.py". If there are errors, please edit the .kal files
  - 5º: Type the following command in CLI (main script): "python run.py --configData --resetData --makeFeats --makeLanguageModel --makeTraining --makeTesting".  
  - 6º: Type the following command in CLI: "result_format.py"

  Now you should find the predicted transcriptions (results) in the folder "results".

In step 5, each argument of the python command corresponds to a "flag". This means that the absence or existence of these flags means the execution of a certain stage of this kaldi recipe.

	- "--resetData": Reset current kaldi data directory (execute resetDirectory.sh).
	- "--configData": Extract .kal information to set all kaldi folders (execute config.py).
	- "--makeFeats": Execute a mfcc/cvmn feature extraction of a certain group of speaker/s and a another set of testing speakers (execute makeFeats.sh).
	- "--makeLanguageModel": Execute a kaldi recipe for a language Model preparation and creation (execute makeLanguageModel).
	- "--makeTraining": training stage is carried out (execute train.sh).
	- "--makeTesting": testing stage is carryied out (execute test.sh).
The order of the flags in the command is not relevance.

Examples:

Typing the command: 

	python run.py --configData --resetData 

It executes only two functionalities of the script: the reset and setting of the kaldi data folder.

If the user types: 

	python run.py --makeFeats

It executes only the parameter extraction stage (mfcc/cvmn).

If the user types:

	python run.py --makeLanguageModel --makeTraining --makeTesting


It executes only the language model creation, nnet model training and testing stages.

**Important Note**

However, if you execute the training stage:


	python run.py --makeTraining

And you didn´t create the parameter and language model files from prior stages it will prompt errors on the Terminal.

In order to avoid this, you need to understand the file dependency among each stage:

	- **resetData stage**: No file dependency
	- **configData stage**: it relies on the existence of info_user/filename.kal files.
	- **makeFeats stage**: it relies on the existence of .wav files (audio), and the setting of the kaldi data folder made by configData.
	- **makeLanguageModel stage**: it relies on the setting of the kaldi data folder made by configData.
	- **makeTraining stage**: it relies on the existence of .ark files which are parameter binary files created by the makeFeats stage. In addition, it depends on the existence of .fst files created by the makeLanguageModel stage.
	- **makeTesting stage**: it relies on the existence of trained model files created in makeTraining stage.

Therefore, this is the sequential stage dependency:

**configData** --> **makeFeats** or **makeLanguageModel** --> **makeTraining** --> **makeTesting**
	       
	






	



