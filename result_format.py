

import os
import pandas as pd
import csv
import argparse


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



        # print(df)
        if speaker !=[] and crossVal_mode == True:
            df.to_csv("results/" +speaker+ ".csv", sep="\t")
        else:
            df.to_csv("results/global.csv", sep="\t")

    except FileNotFoundError as error:
        print('Result file: global_raw.txt was not generated by run_iteration script.')

def save_test(results_decode_path):
    # Extract output
    #   results_decode_path = 'exp/nnet2/nnet2_simple/decode/scoring_kaldi/wer_details/'
    #   results_decode_path = 'exp/tri1/decode/scoring_kaldi/wer_details/'
    utt_results = open(results_decode_path+'per_utt','r')
    utt = utt_results.read()
    speaker_results = open(results_decode_path+'per_spk','r')
    spk = speaker_results.read()
    # print(spk)
    r = '\n--------------------------------------------------------------------\n'
    r = r + spk + r
    r = r + utt

    # l = lambda a : a.replace(' ', '')
    lines = spk.split('\n')
    lines = lines[1:-3]

    resume = pd.DataFrame(columns=('Speaker ID', 'Accuracy'))
    line = lines[-1]

    items = line.split(' ')

    x = lambda a : a.replace(' ', '')
    items = list(map(x, items))
    good_Items = []
    for item in items:
        if item != '':
            good_Items.append(item)
    items = good_Items
    speaker = 'test' #items[0]
    accuracy = items[4]
    resume.loc[0] = [speaker] + [accuracy]

    output = open('results/raw/'+speaker+'_raw.txt','+w')
    output.write(r)

    output.close()
    extract_results(True, speaker)
# end save_test


# ----------------------------------------------------- MAIN ------------------------------------------------------------------------------#


if __name__ == "__main__":

    try:
        results_decode_path = 'exp/tri1/decode/scoring_kaldi/wer_details/'
        save_test(results_decode_path)
    except:
        results_decode_path = 'exp/nnet2/nnet2_simple/decode/scoring_kaldi/wer_details/'
        save_test(results_decode_path)
        #   results_decode_path = 'exp/nnet2/nnet2_simple/decode/scoring_kaldi/wer_details/'
    #   results_decode_path = 'exp/tri1/decode/scoring_kaldi/wer_details/'

#    parser = argparse.ArgumentParser()
#    parser.add_argument("-n", "--filename", required=True,help="name of the result file")
#    args = parser.parse_args()
#
#
#    filename = args.filename
#    pathTo_perSpk = 'exp/nnet2/nnet2_simple/decode/scoring_kaldi/wer_details/per_spk'
##    pathTo_perSpk = 'exp/tri1/decode/scoring_kaldi/wer_details/per_spk'
#    simpleFormat(pathTo_perSpk,'results/' + filename)
#    #pathTo_perSpk = 'exp/tri1/decode/scoring_kaldi/wer_details/per_spk'
#    #simpleFormat(pathTo_perSpk,'results/gmmTri_result.txt')
##    speaker = []
##    extract_results(False,speaker)


