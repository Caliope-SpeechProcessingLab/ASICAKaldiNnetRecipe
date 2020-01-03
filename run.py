import os
import subprocess
import config 
import check_format
import time
import argparse
start_time = time.time()


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--resetData',action='store_true', help='Remove data directory and creates another one from data_init')
parser.add_argument('-c', '--configData',action='store_true', help='set transcription information into kaldi directories')
parser.add_argument('-f', '--makeFeats',action='store_true', help='make acoustic features')
parser.add_argument('-l', '--makeLanguageModel',action='store_true', help='prepare and created language model')
parser.add_argument('-t', '--makeTraining',action='store_true', help='carry out the training stage (mono, triphone + nnet2)')
parser.add_argument('-d', '--makeTesting',action='store_true', help='carry out the testing stage (decoding)')
args = parser.parse_args()




#-------------------------------------------- USER VARIABLES ---------------------------------------------------------


# .wav and .kal file paths:
audioTestPath = 'audio/Experiment1/test/'
audioTrainPath = 'audio/Experiment1/train/'
dataTestPath = 'info_user/test/'
dataTrainPath = 'info_user/train/'

# Internal folder Paths: 
info_testReal = 'info_user/testReal'
audio_testReal = 'audio/Experiment1/testReal'

# Internal file Paths:
global_spk = 'results/global_spk.txt'

# ----------------------------------------- CHECK .KAL FORMAT ----------------------------------------------------------

check_format.checker(dataTestPath)
check_format.checker(dataTrainPath)


#------------------------------------ INITIALIZE DATA AND AUDIO LISTS -----------------------------------------------------

# ASSESMENT OF THE DIRECTORY STRUCTURE:
audioTestFilenames = list()
audioTrainFilenames = list()
dataTestFilenames = list()
dataTrainFilenames = list()

for file in os.listdir(dataTestPath):
	if file.endswith(".kal") and not(file.startswith(".")) and not(file.startswith("_")):
	    dataTestFilenames.append(file)
for file in os.listdir(dataTrainPath):
	if file.endswith(".kal") and not(file.startswith(".")) and not(file.startswith("_")):
	    dataTrainFilenames.append(file)

for file in os.listdir(audioTestPath):
	if file.endswith(".wav") and not(file.startswith(".")) and not(file.startswith("_")):
	    audioTestFilenames.append(file)
for file in os.listdir(audioTrainPath):
	if file.endswith(".wav") and not(file.startswith(".")) and not(file.startswith("_")):
	    audioTrainFilenames.append(file)

print("\n " + str(len(audioTestFilenames)) + " wav files in folder " + audioTestPath + "   \n\n")
print("\n " + str(len(audioTrainFilenames)) + " wav files in folder " + audioTrainPath + "   \n\n\n")
print("\n " + str(len(dataTestFilenames)) + " kal files in folder " + dataTestPath + "   \n\n")
print("\n " + str(len(dataTrainFilenames)) + " kal files in folder " + dataTrainPath + "   \n\n\n")

if len(audioTestFilenames) == 0 or len(audioTrainFilenames) == 0 or len(dataTestFilenames) == 0 or len(dataTrainFilenames) == 0:
	print("ABORTING EXECUTION BECAUSE SOME FOLDER IS EMPTY")
	exit()


#-----------------------------------------------------------------------------------------


# Configure train and test data:

if args.configData:
	print("CONFIG DATA")
	config.main(dataTestFilenames, dataTrainFilenames)
if args.resetData:
	print("RESET DATA")
	bashCommand = "bash local/resetDirectory.sh"
	process = subprocess.Popen(bashCommand,shell=True)
	output, error = process.communicate()
if args.makeFeats:
	print("MAKE FEATS")
	bashCommand = "bash local/makeFeats.sh"
	process = subprocess.Popen(bashCommand,shell=True)
	output, error = process.communicate()
if args.makeLanguageModel:
	print("MAKE LANGUAGE MODEL")
	bashCommand = "bash local/makeLanguageModel.sh"
	process = subprocess.Popen(bashCommand,shell=True)
	output, error = process.communicate()
if args.makeTraining:
	print("TRAIN")
	bashCommand = "bash local/train.sh"
	process = subprocess.Popen(bashCommand,shell=True)
	output, error = process.communicate()
if args.makeTesting:
	print("TEST")
	bashCommand = "bash local/test.sh"
	process = subprocess.Popen(bashCommand,shell=True)
	output, error = process.communicate()




print("--- %s seconds ---" % (time.time() - start_time))
