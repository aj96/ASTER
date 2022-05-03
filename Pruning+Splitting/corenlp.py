# subprocess commands for running corenlp stuff

import os
import json
import subprocess
from nltk.internals import find_jar, find_jar_iter, config_java, java, _java_options, find_jars_within_path
import tempfile
from nltk import compat
from tqdm import tqdm
import re

# stanford_dir = "/mnt/sdb1/Pipeline/tools/stanford/stanford-corenlp-full-2016-10-31"
# models = "/mnt/sdb1/Pipeline/tools/stanford/stanford-english-corenlp-2016-10-31-models"
# CURR_DIR = "/mnt/sdb1/Dropbox (GaTech)/Chicken/BootstrappedRL/"
# input_file = CURR_DIR+ 'miniSents.txt' #'SCIFI-CORPUS-noQuotes.txt'
# output_file = CURR_DIR+ 'miniSents-parsed.txt' #'scifi_parsed.txt'
# sentence_file = CURR_DIR+ 'miniSents-sentences.txt' #'scifi_sentences.txt'

stanford_root_dir = "/xmotors_ai_shared_cephfs/team/perception/adam/tmp_workspace/StoryRealization/EventCreation/tools"
stanford_dir = os.path.join(stanford_root_dir, "stanford-corenlp-4.4.0")
models = os.path.join(stanford_root_dir, "stanford-corenlp-4.4.0-models-english-kbp")
CURR_DIR = ""
input_file = CURR_DIR+ 'corpus.txt'
output_file = CURR_DIR+ 'corpus-parsed.json'
sentence_file = CURR_DIR+ 'corpus-sentences.txt'

def removePunct(sentence):
	final_sentences = []
	sentence = sentence.strip()
	#remove all punctuation except periods
	original_sent = sentence.replace("!", ".")
	original_sent = original_sent.replace("?", ".")
	original_sent = original_sent.replace("Mr.", "Mr")
	original_sent = original_sent.replace("Ms.", "Ms")
	original_sent = original_sent.replace("Mrs.", "Mrs")
	original_sent = original_sent.replace("Dr.", "Dr")
	original_sent = original_sent.replace("Drs.", "Drs")
	original_sent = original_sent.replace("St.", "St")
	original_sent = original_sent.replace("Col.", "Col")
	original_sent = original_sent.replace("Sgt.", "Sgt")
	original_sent = original_sent.replace("MSgt.", "MSgt")
	original_sent = original_sent.replace("Prof.", "Prof")
	original_sent = original_sent.replace("Dept.", "Dept")
	original_sent = original_sent.replace("Cmdr.", "Cmdr")
	original_sent = original_sent.replace("Comm.", "Comm")
	original_sent = original_sent.replace("Jr.", "Jr")
	original_sent = original_sent.replace("Sr.", "Sr")
	original_sent = original_sent.replace("Lt.", "Lt")
	original_sent = original_sent.replace("Fr.", "Fr")
	original_sent = original_sent.replace("D.C.", "DC")
	original_sent = original_sent.replace(".com", " com")
	original_sent = original_sent.replace(".net", " net")
	original_sent = original_sent.replace("...", " ")
	while "  " in original_sent:
		original_sent = original_sent.replace("  ", " ")
	sentences = original_sent.split(".")
	for sentence in sentences:
		# sentence = sentence.strip()
		if len(sentence) <= 1:
			continue
		if sentence == ".":
			continue
		if len(sentence) < 4:
			sentence = sentence.replace(".", "")
			final_sentences.append(sentence)
		elif sentence:
			final_sentences.append(sentence)
	# return "".join(final_sentences)
	return ". ".join(final_sentences)


def callStanford(sentence):
	# This function can call Stanford CoreNLP tool and support getEvent function.
	encoding = "utf8"
	# cmd = ["java", "-cp", stanford_dir+"/*","-Xmx20g", "edu.stanford.nlp.pipeline.StanfordCoreNLPClient",
	# 	"-annotators", "tokenize,ssplit,parse,ner,pos,lemma,depparse",
	# 	'-outputFormat','json',
	# 	"-parse.flags", "",
	# 	'-encoding', encoding,
	# 	'-model', models+'/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz',"-backends","localhost:9001,12"]
	cmd = ["java", "-cp", stanford_dir+"/*","-Xmx20g", "edu.stanford.nlp.pipeline.StanfordCoreNLPClient",
		"-annotators", "tokenize,ssplit,parse,pos,lemma,ner,depparse",
		'-outputFormat','json',
		"-parse.flags", "",
		'-encoding', encoding,
		'-model', models+'/edu/stanford/nlp/models/kbp/english/coreef-model.ser.gz',"-backends","localhost:9000,12"]
	input_ = ""
	default_options = ' '.join(_java_options)
	_out = {}
	# Sometimes Server doesn't properly receive/process sentence and just returns empty dictionary. Keep trying until it doesn't return empty.
	while len(_out) == 0:
		print("Trying sentence: ", sentence)
		with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
			# Write the actual sentences to the temporary input file
			temp_file.write(sentence.encode())
			temp_file.flush()
			temp_file.seek(0)
			devnull = open(os.devnull, 'w')
			out = subprocess.check_output(cmd, stdin=temp_file, stderr=devnull)
			out = out.replace(b'\xc2\xa0',b' ')
			out = out.replace(b'\xa0',b' ')
			out = out.replace(b'NLP>',b'')
			out = out.decode(encoding)
			_out = json.loads(out)
	os.unlink(temp_file.name)
	# Return java configurations to their default values.
	config_java(options=default_options, verbose=False)
	return out

write_file = open(output_file, "w")
sent_file = open(sentence_file, "w")
write_file.write('{\n"parses":[\n')
parses = {
	"parses": []
}
lines = open(input_file, 'r').readlines()
for line_num,line in enumerate(tqdm(lines)):
	if "<EOS>" in line:
		sent_file.write("<EOS>\n")
	else:
		sentences = removePunct(line)
		split = sentences.split(".")
		for sentence_num,sentence in enumerate(split):
			sentence = sentence.strip()
			if len(sentence) == 0:
				continue
			result = callStanford(sentence+".")
			sent_file.write(sentence+".\n")
			write_file.write(result)
			if sentence_num == len(split) - 1 and line_num == len(lines) - 1:
				write_file.write("\n")
			else:
				write_file.write(",\n")
			# write_file.write(result+",\n")


write_file.write("]\n}") ###MAKE SURE TO GET RID OF THAT LAST , [comma]
# write_file.close()
sent_file.close()


