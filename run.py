import os
import subprocess
import configTrain
import configTest
import check_format
import time
import argparse
import result_format
start_time = time.time()


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--train',action='store_true', help='make training')
parser.add_argument('-r', '--test',action='store_true', help='make testing')


args = parser.parse_args()




#-------------------------------------------- USER VARIABLES ---------------------------------------------------------


# .wav and .kal file paths:
audioTestPath = 'audio/experiment_lm/'
testInfo_path = 'info_user/test/'

audioTrainPath = 'audio/experiment_lm/'
trainInfo_path = 'info_user/train/'

# Result filename path:
resultFilename = 'resultIniciales'

# ----------------------------------------- CHECK .KAL FORMAT ----------------------------------------------------------

check_format.checker(testInfo_path)
check_format.checker(trainInfo_path)


#------------------------------------ INITIALIZE DATA AND AUDIO LISTS -----------------------------------------------------

# ASSESMENT OF THE DIRECTORY STRUCTURE:
audioTestFilenames = list()
audioTrainFilenames = list()
dataTestFilenames = list()
dataTrainFilenames = list()

for file in os.listdir(testInfo_path):
	if file.endswith(".kal") and not(file.startswith(".")) and not(file.startswith("_")):
	    dataTestFilenames.append(file)
for file in os.listdir(trainInfo_path):
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
print("\n " + str(len(dataTestFilenames)) + " kal files in folder " + testInfo_path + "   \n\n")
print("\n " + str(len(dataTrainFilenames)) + " kal files in folder " + trainInfo_path + "   \n\n\n")

if len(audioTestFilenames) == 0 or len(audioTrainFilenames) == 0 or len(dataTestFilenames) == 0 or len(dataTrainFilenames) == 0:
	print("ABORTING EXECUTION BECAUSE SOME FOLDER IS EMPTY")
	exit()


#-----------------------------------------------------------------------------------------



if args.train:

	print("\n-----------------RESET DATA----------------------\n")
	bashCommand = "bash local/resetDirectory.sh"
	process = subprocess.Popen(bashCommand,shell=True)
	output, error = process.communicate()

	print("\n-----------------CONFIG TRAIN DATA----------------------\n")
	configTrain.main(dataTrainFilenames)

	print("\n-----------------MAKE FEATS----------------------\n")
	bashCommand = "bash local/makeFeats.sh train"
	process = subprocess.Popen(bashCommand,shell=True)
	output, error = process.communicate()

	print("\n-----------------MAKE LANGUAGE MODEL----------------------\n")
	bashCommand = "bash local/makeLanguageModel.sh"
	process = subprocess.Popen(bashCommand,shell=True)
	output, error = process.communicate()

	print("\n-----------------TRAIN----------------------\n")
	bashCommand = "bash local/train.sh {}".format(trainInfo_path)
	process = subprocess.Popen(bashCommand,shell=True)
	output, error = process.communicate()



if args.test:
	print("\n-----------------CONFIG TEST DATA----------------------\n")
	configTest.main(dataTestFilenames, audioTestPath, testInfo_path)

	print("\n-----------------MAKE FEATS----------------------\n")
	bashCommand = "bash local/makeFeats.sh test"
	process = subprocess.Popen(bashCommand,shell=True)
	output, error = process.communicate()

	print("\n-----------------TEST----------------------\n")
	bashCommand = "bash local/test.sh {}".format(testInfo_path)
	process = subprocess.Popen(bashCommand,shell=True)
	output, error = process.communicate()

	print("\n-----------------EXTRACT RESULTS----------------------\n")
	pathTo_perSpk = 'exp/nnet2/nnet2_simple/decode/scoring_kaldi/wer_details/per_spk'
	result_format.simpleFormat(pathTo_perSpk,'results/' + resultFilename)





print("--- %s seconds ---" % (time.time() - start_time))
