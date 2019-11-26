

import os
import pandas as pd
import csv


def remove_SpaceItems(items):
	new_list = list()
	for item in items:
		if item != '' and item != '\n':
			new_list.append(item)

	return new_list

def simpleFormat(pathTo_perSpk, filename):
	file = open(pathTo_perSpk, 'r')
	lines = file.readlines()
	formatFile = ""
	for iline in lines:
		pieces = iline.split(" ")
		cleanedPieces = remove_SpaceItems(pieces)
		if "sys" in cleanedPieces:
			formatFile = formatFile + cleanedPieces[0] + "\t" + cleanedPieces[4] + "\n"

	writer = open(filename, 'w')
	writer.write(formatFile)
	writer.close()


def extract_results(crossVal_mode, speaker):

	df = pd.DataFrame(columns=('Speaker ID', 'Task', 'Evaluation', 'Target', 'Response','Hit','Correct', 'Target Utterance', 'Responsed Utterance', 'Number of Syllables', 'Syllable position'))

	cnt = 0
	try:
		reader = open('results/raw/'+ speaker +'_raw.txt', 'r')
		lines = reader.readlines()
		for i in list(range(0,len(lines))):
			if lines[i].startswith('---'):
				ind = i
		lines = lines[ind+1:]

		#Utterance processing
		for i in list(range(0,len(lines),4)):
			utt = lines[i:i+4]
			for j in list(range(len(utt))):
				if j == 0:
					
					content = utt[j].split(' ')

					#Filename processing
					id = content[0]
					name_fields = id.split('_')
					spk = name_fields[0]
					ev = name_fields[1]
					ev = ev.split('-')
					ev = ev[0]
					s = spk.find('Q')
					spk_id = spk[:s]
					task = spk[s:]
					
					refs = content[1:]
					refs = remove_SpaceItems(refs)
					last_item = refs[-1].rstrip('\n')
					refs[-1] = last_item
					refs = refs[1:]
					ref_utt = ' '.join(refs)
				
					
				if j == 1:
					
					content = utt[j].split(' ')
					hyps = content[1:]
					hyps = remove_SpaceItems(hyps)
					last_item = hyps[-1].rstrip('\n')
					hyps[-1] = last_item
					hyps = hyps[1:]
					hyps_utt = ' '.join(hyps)
					
					
				if j == 2:
					id_hits = utt[j].split(' ')
					hits = id_hits[1:]
					hits = remove_SpaceItems(hits)
					last_item = hits[-1].rstrip('\n')
					hits[-1] = last_item
					hits = hits[1:]
					

				if j == 3:
					if (len(refs) + len(hyps) + len(hits)) % 3 != 0:
						raise ValueError('DIFFERENT Length of the three lists --> refs, hyps and hits')

					for z in list(range(len(refs))):
						if hits[z] == 'C':
							correct = 1
						else:
							correct = 0

						df.loc[cnt] = [spk_id] + [task] + [ev] + [refs[z]] + [hyps[z]] + [hits[z]] + [correct] + [ref_utt] + [hyps_utt] + [len(refs)] + [z+1]
						cnt = cnt + 1
						
						

		print(df)
		if speaker !=[] and crossVal_mode == True:
			df.to_csv("results/" +speaker+ ".csv", sep="\t")
		else:
			df.to_csv("results/global.csv", sep="\t")

	except FileNotFoundError as error:
		print('Result file: global_raw.txt was not generated by run_iteration script.')


# ----------------------------------------------------- MAIN ------------------------------------------------------------------------------#


if __name__ == "__main__":

	pathTo_perSpk = 'exp/nnet2/nnet2_simple/decode/scoring_kaldi/wer_details/per_spk'
	simpleFormat(pathTo_perSpk,'results/nnet2pnormOptmize_result.txt')
	#pathTo_perSpk = 'exp/tri1/decode/scoring_kaldi/wer_details/per_spk'
	#simpleFormat(pathTo_perSpk,'results/gmmTri_result.txt')
	#speaker == []
	#extract_results(False,speaker)