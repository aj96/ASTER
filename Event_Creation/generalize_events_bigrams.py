# takes json-file parses of stories & ner
# creates files of generalized events
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
import json
import os
import argparse
from collections import defaultdict
import nltk.corpus
from nltk.corpus import wordnet as wn
from numpy.random import choice
import copy
import sys
import importlib
importlib.reload(sys)


#VERBS
# if not os.path.exists("tools/verbnet"):
# 	os.makedirs("tools/verbnet", exist_ok=True)
# verbnet = nltk.corpus.VerbnetCorpusReader('tools/v3.3', ['absorb-39.8.xml','continue-55.3.xml','hurt-40.8.3.xml','remove-10.1.xml','accept-77.xml','contribute-13.2.xml','illustrate-25.3.xml','render-29.90.xml','accompany-51.7.xml','convert-26.6.2.xml','image_impression-25.1.xml','require-103.xml','acquiesce-95.xml','cooking-45.3.xml','indicate-78.xml','resign-10.11.xml','addict-96.xml','cooperate-73.xml','inquire-37.1.2.xml','risk-94.xml','adjust-26.9.xml','cope-83.xml','instr_communication-37.4.xml','roll-51.3.1.xml','admire-31.2.xml','correlate-86.1.xml','interrogate-37.1.3.xml','rummage-35.5.xml','admit-65.xml','correspond-36.1.xml','investigate-35.4.xml','run-51.3.2.xml','adopt-93.xml','cost-54.2.xml','involve-107.xml','rush-53.2.xml','advise-37.9.xml','crane-40.3.2.xml','judgment-33.xml','say-37.7.xml','allow-64.xml','create-26.4.xml','keep-15.2.xml','scribble-25.2.xml','amalgamate-22.2.xml','curtsey-40.3.3.xml','knead-26.5.xml','search-35.2.xml','amuse-31.1.xml','cut-21.1.xml','learn-14.xml','see-30.1.xml','animal_sounds-38.xml','debone-10.8.xml','leave-51.2.xml','seem-109.xml','appeal-31.4.xml','declare-29.4.xml','lecture-37.11.xml','send-11.1.xml','appear-48.1.1.xml','dedicate-79.xml','light_emission-43.1.xml','separate-23.1.xml','appoint-29.1.xml','deduce-97.2.xml','limit-76.xml','settle-89.xml','assessment-34.1.xml','defend-72.2.xml','linger-53.1.xml','shake-22.3.xml','assuming_position-50.xml','destroy-44.xml','sight-30.2.xml','avoid-52.xml','devour-39.4.xml','lodge-46.xml','simple_dressing-41.3.1.xml','banish-10.2.xml','differ-23.4.xml','long-32.2.xml','slide-11.2.xml','base-97.1.xml','dine-39.5.xml','manner_speaking-37.3.xml','smell_emission-43.3.xml','battle-36.4.xml','disappearance-48.2.xml','marry-36.2.xml','snooze-40.4.xml','become-109.1.xml','disassemble-23.3.xml','marvel-31.3.xml','beg-58.2.xml','discover-84.xml','masquerade-29.6.xml','sound_emission-43.2.xml','begin-55.1.xml','dress-41.1.1.xml','matter-91.xml','sound_existence-47.4.xml','being_dressed-41.3.3.xml','dressing_well-41.3.2.xml','meander-47.7.xml','spank-18.3.xml','bend-45.2.xml','drive-11.5.xml','meet-36.3.xml','spatial_configuration-47.6.xml','benefit-72.1.xml','dub-29.3.xml','mine-10.9.xml','spend_time-104.xml','berry-13.7.xml','eat-39.1.xml','mix-22.1.xml','split-23.2.xml','bill-54.5.xml','empathize-88.2.xml','modes_of_being_with_motion-47.3.xml','spray-9.7.xml','body_internal_motion-49.xml','enforce-63.xml','multiply-108.xml','stalk-35.3.xml','body_internal_states-40.6.xml','engender-27.xml','murder-42.1.xml','steal-10.5.xml','braid-41.2.2.xml','ensure-99.xml','neglect-75.xml','stimulus_subject-30.4.xml','break-45.1.xml','entity_specific_cos-45.5.xml','nonvehicle-51.4.2.xml','stop-55.4.xml','breathe-40.1.2.xml','entity_specific_modes_being-47.2.xml','nonverbal_expression-40.2.xml','subjugate-42.3.xml','bring-11.3.xml','equip-13.4.2.xml','obtain-13.5.2.xml','substance_emission-43.4.xml','build-26.1.xml','escape-51.1.xml','occurrence-48.3.xml','succeed-74.xml','bulge-47.5.3.xml','establish-55.5.xml','order-60.xml','suffocate-40.7.xml','bump-18.4.xml','estimate-34.2.xml','orphan-29.7.xml','suspect-81.xml','butter-9.9.xml','exceed-90.xml','other_cos-45.4.xml','sustain-55.6.xml','calibratable_cos-45.6.xml','exchange-13.6.xml','overstate-37.12.xml','swarm-47.5.1.xml','calve-28.xml','exhale-40.1.3.xml','own-100.xml','swat-18.2.xml','captain-29.8.xml','exist-47.1.xml','pain-40.8.1.xml','talk-37.5.xml','care-88.1.xml','feeding-39.7.xml','patent-101.xml','tape-22.4.xml','carry-11.4.xml','ferret-35.6.xml','pay-68.xml','tell-37.2.xml','carve-21.2.xml','fill-9.8.xml','peer-30.3.xml','throw-17.1.xml','change_bodily_state-40.8.4.xml','fire-10.10.xml','pelt-17.2.xml','tingle-40.8.2.xml','characterize-29.2.xml','fit-54.3.xml','performance-26.7.xml','touch-20.xml','chase-51.6.xml','flinch-40.5.xml','pit-10.7.xml','transcribe-25.4.xml','cheat-10.6.xml','floss-41.2.1.xml','pocket-9.10.xml','transfer_mesg-37.1.1.xml','chew-39.2.xml','focus-87.1.xml','poison-42.2.xml','try-61.xml','chit_chat-37.6.xml','forbid-67.xml','poke-19.xml','turn-26.6.1.xml','classify-29.10.xml','force-59.xml','pour-9.5.xml','urge-58.1.xml','clear-10.3.xml','free-80.xml','preparing-26.3.xml','use-105.xml','cling-22.5.xml','fulfilling-13.4.1.xml','price-54.4.xml','vehicle-51.4.1.xml','coil-9.6.xml','funnel-9.3.xml','promise-37.13.xml','vehicle_path-51.4.3.xml','coloring-24.xml','future_having-13.3.xml','promote-102.xml','complain-37.8.xml','get-13.5.1.xml','pronounce-29.3.1.xml','complete-55.2.xml','give-13.1.xml','push-12.xml','void-106.xml','comprehend-87.2.xml','gobble-39.3.xml','put-9.1.xml','waltz-51.5.xml','comprise-107.1.xml','gorge-39.6.xml','put_direction-9.4.xml','want-32.1.xml','concealment-16.xml','groom-41.1.2.xml','put_spatial-9.2.xml','weather-57.xml','confess-37.10.xml','grow-26.2.xml','reach-51.8.xml','weekend-56.xml','confine-92.xml','help-72.xml','reflexive_appearance-48.1.2.xml','wink-40.3.1.xml','confront-98.xml','herd-47.5.2.xml','refrain-69.xml','wipe_instr-10.4.2.xml','conjecture-29.5.xml','hiccup-40.1.1.xml','register-54.1.xml','wipe_manner-10.4.1.xml','consider-29.9.xml','hire-13.5.3.xml','rehearse-26.8.xml','wish-62.xml','conspire-71.xml','hit-18.1.xml','relate-86.2.xml','withdraw-82.xml','consume-66.xml','hold-15.1.xml','rely-70.xml','contiguous_location-47.8.xml','hunt-35.1.xml','remedy-45.7.xml'])
verbnet = nltk.corpus.VerbnetCorpusReader('./tools/v3.3',
['absorb-39.8.xml','accept-77.1.xml','accompany-51.7.xml','acquiesce-95.1.xml','act-114.xml','addict-96.xml','adjust-26.9.xml','admire-31.2.xml','admit-64.3.xml','adopt-93.xml','advise-37.9.xml','allow-64.1.xml','amalgamate-22.2.xml','amuse-31.1.xml','animal_sounds-38.xml','appeal-31.4.xml','appear-48.1.1.xml','appoint-29.1.xml','assessment-34.1.xml','assuming_position-50.xml','attend-107.4.xml','avoid-52.xml','banish-10.2.xml','base-97.1.xml','battle-36.4.xml','become-109.1.xml','beg-58.2.xml','begin-55.1.xml','being_dressed-41.3.3.xml','bend-45.2.xml','benefit-72.2.xml','berry-13.7.xml','bill-54.5.xml','birth-28.2.xml','body_internal_motion-49.1.xml','body_internal_states-40.6.xml','body_motion-49.2.xml','braid-41.2.2.xml','break-45.1.xml','break_down-45.8.xml','breathe-40.1.2.xml','bring-11.3.xml','build-26.1.xml','bulge-47.5.3.xml','bully-59.5.xml','bump-18.4.xml','butter-9.9.xml','calibratable_cos-45.6.1.xml','calve-28.1.xml','captain-29.8.xml','care-88.1.xml','caring-75.2.xml','carry-11.4.xml','carve-21.2.xml','caused_calibratable_cos-45.6.2.xml','change_bodily_state-40.8.4.xml','characterize-29.2.xml','chase-51.6.xml','cheat-10.6.1.xml','chew-39.2.xml','chit_chat-37.6.xml','classify-29.10.xml','clear-10.3.xml','cling-22.5.xml','cognize-85.xml','coil-9.6.xml','coloring-24.xml','compel-59.1.xml','complain-37.8.xml','complete-55.2.xml','comprehend-87.2.xml','comprise-107.2.xml','concealment-16.xml','conduct-111.1.xml','confess-37.10.xml','confine-92.xml','confront-98.xml','conjecture-29.5.xml','consider-29.9.xml','conspire-71.xml','consume-66.xml','contain-15.4.xml','contiguous_location-47.8.xml','continue-55.3.xml','contribute-13.2.xml','convert-26.6.2.xml','cooking-45.3.xml','cooperate-73.1.xml','cope-83.xml','correlate-86.1.xml','correspond-36.1.1.xml','cost-54.2.xml','crane-40.3.2.xml','create-26.4.xml','curtsey-40.3.3.xml','cut-21.1.xml','debone-10.8.xml','declare-29.4.xml','dedicate-79.xml','deduce-97.2.xml','defend-72.3.xml','deprive-10.6.2.xml','destroy-44.xml','devour-39.4.xml','die-42.4.xml','differ-23.4.xml','dine-39.5.xml','disappearance-48.2.xml','disassemble-23.3.xml','discover-84.xml','disfunction-105.2.2.xml','distinguish-23.5.xml','dress-41.1.1.xml','dressing_well-41.3.2.xml','drive-11.5.xml','dub-29.3.xml','earn-54.6.xml','eat-39.1.xml','empathize-88.2.xml','employment-95.3.xml','encounter-30.5.xml','enforce-63.xml','engender-27.1.xml','ensure-99.xml','entity_specific_cos-45.5.xml','entity_specific_modes_being-47.2.xml','equip-13.4.2.xml','escape-51.1.xml','establish-55.5.xml','estimate-34.2.xml','exceed-90.xml','exchange-13.6.1.xml','exclude-107.3.xml','exhale-40.1.3.xml','exist-47.1.xml','feeding-39.7.xml','ferret-35.6.xml','fill-9.8.xml','fire-10.10.xml','fit-54.3.xml','flinch-40.5.xml','floss-41.2.1.xml','focus-87.1.xml','forbid-64.4.xml','free-10.6.3.xml','free-80.xml','fulfilling-13.4.1.xml','function-105.2.1.xml','funnel-9.3.xml','future_having-13.3.xml','get-13.5.1.xml','give-13.1.xml','gobble-39.3.xml','gorge-39.6.xml','groom-41.1.2.xml','grow-26.2.1.xml','harmonize-22.6.xml','help-72.1.xml','herd-47.5.2.xml','hiccup-40.1.1.xml','hire-13.5.3.xml','hit-18.1.xml','hold-15.1.xml','hunt-35.1.xml','hurt-40.8.3.xml','illustrate-25.3.xml','image_impression-25.1.xml','indicate-78.xml','initiate_communication-37.4.2.xml','inquire-37.1.2.xml','instr_communication-37.4.1.xml','intend-61.2.xml','interact-36.6.xml','interrogate-37.1.3.xml','invest-13.5.4.xml','investigate-35.4.xml','involve-107.1.xml','judgment-33.1.xml','keep-15.2.xml','knead-26.5.xml','learn-14.xml','leave-51.2.xml','lecture-37.11.xml','let-64.2.xml','light_emission-43.1.xml','limit-76.xml','linger-53.1.xml','lodge-46.xml','long-32.2.xml','lure-59.3.xml','manner_speaking-37.3.xml','marry-36.2.xml','marvel-31.3.xml','masquerade-29.6.xml','matter-91.xml','meander-47.7.xml','meet-36.3.xml','mine-10.9.xml','mix-22.1.xml','modes_of_being_with_motion-47.3.xml','multiply-108.xml','murder-42.1.xml','neglect-75.1.xml','nonvehicle-51.4.2.xml','nonverbal_expression-40.2.xml','obtain-13.5.2.xml','occur-48.3.xml','order-58.3.xml','orphan-29.7.xml','other_cos-45.4.xml','overstate-37.12.xml','own-100.1.xml','pain-40.8.1.xml','patent-101.xml','pay-68.xml','peer-30.3.xml','pelt-17.2.xml','performance-26.7.xml','pit-10.7.xml','pocket-9.10.xml','poison-42.2.xml','poke-19.xml','pour-9.5.xml','preparing-26.3.xml','price-54.4.xml','promise-37.13.xml','promote-102.xml','pronounce-29.3.1.xml','prosecute-33.2.xml','push-12.xml','put-9.1.xml','put_direction-9.4.xml','put_spatial-9.2.xml','reach-51.8.xml','rear-26.2.2.xml','reciprocate-112.xml','reflexive_appearance-48.1.2.xml','refrain-69.xml','register-54.1.xml','rehearse-26.8.xml','reject-77.2.xml','relate-86.2.xml','rely-70.xml','remedy-45.7.xml','remove-10.1.xml','render-29.90.xml','representation-110.1.xml','require-103.xml','resign-10.11.xml','respond-113.xml','result-27.2.xml','risk-94.xml','rob-10.6.4.xml','roll-51.3.1.xml','rummage-35.5.xml','run-51.3.2.xml','rush-53.2.xml','satisfy-55.7.xml','say-37.7.xml','scribble-25.2.xml','search-35.2.xml','see-30.1.xml','seem-109.xml','send-11.1.xml','separate-23.1.xml','settle-36.1.2.xml','shake-22.3.xml','sight-30.2.xml','simple_dressing-41.3.1.xml','slide-11.2.xml','smell_emission-43.3.xml','snooze-40.4.xml','sound_emission-43.2.xml','sound_existence-47.4.xml','spank-18.3.xml','spatial_configuration-47.6.xml','spend_time-104.xml','split-23.2.xml','spray-9.7.xml','stalk-35.3.xml','steal-10.5.xml','stimulate-59.4.xml','stimulus_subject-30.4.xml','stop-55.4.xml','subjugate-42.3.xml','subordinate-95.2.1.xml','substance_emission-43.4.xml','substitute-13.6.2.xml','succeed-74.xml','suffocate-40.7.xml','supervision-95.2.2.xml','support-15.3.xml','suspect-81.xml','sustain-55.6.xml','swarm-47.5.1.xml','swat-18.2.xml','talk-37.5.xml','tape-22.4.xml','tell-37.2.xml','terminus-47.9.xml','throw-17.1.xml','tingle-40.8.2.xml','touch-20.xml','transcribe-25.4.xml','transfer_mesg-37.1.1.xml','trick-59.2.xml','trifle-105.3.xml','try-61.1.xml','turn-26.6.1.xml','urge-58.1.xml','use-105.1.xml','vehicle-51.4.1.xml','vehicle_path-51.4.3.xml','vn_class-3.dtd','vn_schema-3.xsd','void-106.xml','volunteer-95.4.xml','waltz-51.5.xml','want-32.1.xml','weather-57.xml','weekend-56.xml','wink-40.3.1.xml','wipe_instr-10.4.2.xml','wipe_manner-10.4.1.xml','wish-62.xml','withdraw-82.xml','work-73.2.xml'])

def generalize_verb(word,tokens):
	#tokens[word] = [lemma, POS, NER]
	word = tokens[word][0]
	if word == "have": return "own-100" #most likely not "consume"
	classids = verbnet.classids(word)
	if len(classids) > 0:
		#return choice based on weight of number of members
		mems = []
		for classid in classids:
			vnclass = verbnet.vnclass(classid)
			num = len(list(vnclass.findall('MEMBERS/MEMBER')))
			mems.append(num)
		mem_count = mems
		mems = [x/float(sum(mem_count)) for x in mems]
		return str(choice(classids, 1, p=mems)[0])
	else:
		return word


#NOUNS
def lookupNoun(word):
	result = ""
	if len(wn.synsets(word)) > 0:
		word1 = wn.synsets(word)[0]
	else:
		return word.lower()
	hyper = lambda s: s.hypernyms()
	TREE = word1.tree(hyper, depth=6)
	#pprint(TREE)
	temp_tree = TREE
	for i in range(2): #each word should have at least 2-3 levels
		try:
			temp_tree = temp_tree[1]
		except:
			break
	#print(temp_tree[0])
	result = temp_tree[0]
	return str(result)

def generalize_noun(word, tokens):
	lemma = tokens[word][0]
	pos = tokens[word][1]
	ner = tokens[word][2]
	resultString = ""
	if ner != "O":
		if ner == "PERSON":
			resultString = "<NE>"+word
		else:
			resultString = ner #location or something
	else:
		word = lemma
		if "NN" in pos:
			resultString = lookupNoun(word)
		elif "PRP" in pos:
			if word == "he" or word == "him":
				resultString = "Synset('male.n.02')"
			elif word == "she" or word == "her":
				resultString = "Synset('female.n.02')"
			elif word == "I" or word == "me" or word == "we" or word == "us":
				resultString = "Synset('person.n.01')"
			elif word == "they" or word == "them":
				resultString = "Synset('physical_entity.n.01')"
			else:
				resultString = "Synset('entity.n.01')" ##
		else:
			resultString = word
	return resultString

def NEs(event, named_entities):
	new_event = []
	for word in event:
		if "<NE>" in word:
			_,name = word.split(">")
			if name not in named_entities:
				named_entities.append(name)
			new_event.append("<NE>"+str(named_entities.index(name)))
		else:
			new_event.append(word)
	return new_event, named_entities


#read in parsed json files
#read in ner files

#for each pair of parse/ner files (for each genre)
# for genreNum in range(0,100):
f = open("events.txt", "w+")
f.close()

for genreNum in range(0,1):
	# json_file = "cmu_parsed/genre_"+str(genreNum)+"_sents.txt.json"
	# ner_file = open("cmu_ner/genre_"+str(genreNum)+"_sents.txt.ner", 'r')
	root_dir = "../Pruning+Splitting/"
	json_file = os.path.join(root_dir, "corpus-parsed.json")
	ner_file = open(os.path.join(root_dir, "corpus-sentences.txt"), "r")
	ner = [line.strip().split(' ') for line in ner_file.readlines()] 
	original_sents = [" ".join([word.split("/")[0] for word in sentence]) for sentence in ner]
	ner_dict = [] #json sentence index should match up with sentence index here; list of dictionaries with {word:label} pairs for each sentence
	story_events = []

	for sent in ner:
		tiny_dict = defaultdict(str)
		import pdb; pdb.set_trace()
		for pair in sent:
			word, label = pair.rsplit("/", 1)
			tiny_dict[word] = label
		ner_dict.append(tiny_dict)

	with open(json_file) as json_data:
		d = json.load(json_data)
		all_json = d["sentences"]
		#story_count = 0
		# with open("cmu_NEfixed_events-bigram/genre_"+str(genreNum)+"_fixedNE_events-bigram.txt", "w") as outfile:	
		with open("events.txt", "w") as outfile:	
			for sent_num, sentence in enumerate(all_json): # for each sentence in the entire genre
				new_story = False
				tokens = defaultdict(list)#TODO: atm, assuming same POS for same word in sentence

				#from "tokens", put "word" into dictionary & store "lemma", "pos", and get ner from other file
				for token in sentence["tokens"]:
					#each word in the dictionary has a list of [lemma, POS, NER]
					tokens[token["word"]] = [token["lemma"], token["pos"], ner_dict[sentence["index"]][token["word"]] ]

					#stories split when last word's "after" is "\n"
					if "\n" in token["after"]:
						new_story=True

				deps = sentence["enhancedPlusPlusDependencies"]	
				conj = defaultdict(str)

				#Shruti's version
				verbs = []
				subjects = []
				modifiers = []
				objects = []
				negs = []
				pos = {}
				#chaining of mods
				chainMods = {}


				# create events
				for d in deps:
					#[(d["governorGloss"],tokens[d["governorGloss"]][1]), d["dep"], (d["dependentGloss"],tokens[d["dependentGloss"]][1])]
					#subject
					if 'subj' in d["dep"]:
						if d["governorGloss"] not in verbs:
							#create new event
							if not "VB" in tokens[d["governorGloss"]][1]: continue
							verbs.append(d["governorGloss"])
							subjects.append(d["dependentGloss"])
							pos[d["dependentGloss"]] = tokens[d["dependentGloss"]][1]
							modifiers.append('EmptyParameter')
							objects.append('EmptyParameter')
						elif d["governorGloss"] in verbs:
							if subjects[verbs.index(d["governorGloss"])] == "EmptyParameter":
								subjects[verbs.index(d["governorGloss"])] = d["dependentGloss"]
							else:
								subjects.append(d["dependentGloss"])
								verbs.append(d["governorGloss"])
								modifiers.append('EmptyParameter')
								objects.append('EmptyParameter')
							pos[d["dependentGloss"]] = tokens[d["dependentGloss"]][1]
						elif d["dependentGloss"] in subjects:
							verbs[subjects.index(d["dependentGloss"])] = d["governorGloss"]
							pos[d["dependentGloss"]] = tokens[d["dependentGloss"]][1]
					else: #check to see if we have a subject filled
						if len(subjects) >1:
							if subjects[-1] == "EmptyParameter":
								subjects[-1] = subjects[-2]
						#conjunction of subjects
						if 'conj' in d["dep"] and 'VB' in tokens[d["dependentGloss"]][1]:
							if d["dependentGloss"] not in verbs:
								verbs.append(d["dependentGloss"])
								subjects.append('EmptyParameter')
								modifiers.append('EmptyParameter')
								objects.append('EmptyParameter')
						#conjunction of verbs
						elif 'conj' in d["dep"] and d["governorGloss"] in subjects:
							loc = subjects.index(d["governorGloss"])
							verb = verbs[loc]
							subjects.append(d["dependentGloss"])
							verbs.append(verb)
							modifiers.append('EmptyParameter')
							objects.append('EmptyParameter')
							pos[d["dependentGloss"]] = tokens[d["dependentGloss"]][1]
						elif 'conj' in d["dep"] and d["governorGloss"] in objects:
							loc = objects.index(d["governorGloss"])
							match_verb = verbs[loc]
							#print(match_verb)
							temp_verbs = copy.deepcopy(verbs)
							for i, verb in enumerate(temp_verbs):
								if match_verb == verb:
									subjects.append(subjects[i])
									verbs.append(verb)
									modifiers.append('EmptyParameter')
									objects.append(d["dependentGloss"])
							pos[d["dependentGloss"]] = tokens[d["dependentGloss"]][1]			
						# case 1: obj
						elif 'dobj' in d["dep"] or 'xcomp' == d["dep"]:
							if d["governorGloss"] in verbs:
								#modify that object
								pos[d["dependentGloss"]] = tokens[d["dependentGloss"]][1]
								for i, verb in reversed(list(enumerate(verbs))):
									if verb == d["governorGloss"] and objects[i] == "EmptyParameter":
										objects[i] = d["dependentGloss"]
						# case 2: nmod
						elif ('nmod' in d["dep"] or 'ccomp' in d["dep"] or 'iobj' in d["dep"] or 'dep' in d["dep"]) and 'NN' in tokens[d["dependentGloss"]][1]:
							if d["governorGloss"] in verbs:
								#modify that modifier
								for i, verb in reversed(list(enumerate(verbs))):
									if verb == d["governorGloss"] and modifiers[i] == "EmptyParameter":
										modifiers[i] = d["dependentGloss"]
								pos[d["dependentGloss"]] = tokens[d["dependentGloss"]][1]
							elif d["governorGloss"] in chainMods:
								v = chainMods[d["governorGloss"]]
								if v in verbs:
									modifiers[verbs.index(v)] = d["dependentGloss"]
									pos[d["dependentGloss"]] = tokens[d["dependentGloss"]][1]


				for (a,b,c,d) in zip(subjects, verbs, objects, modifiers):
					if a != 'EmptyParameter':
						a1 = generalize_noun(a, tokens)
					else:
						a1 = a
					if b != 'EmptyParameter':
						b1 = generalize_verb(b, tokens)
					else:
						b1 = b
					if c != 'EmptyParameter':
						c1 = generalize_noun(c, tokens)
					else:
						c1 = c
					if d != 'EmptyParameter':
						d1 = generalize_noun(d, tokens)
					else:
						d1 = d
					story_events.append([a1,b1,c1,d1])
					break #only want one event per sentence
					#output_str = " ".join([a1,b1,c1,d1])+";"+original_sents[sent_num]+"\n"
					#outfile.write(output_str)
				if new_story:
					previous_event = []
					prev_prev_event = []
					prev_prev_prev_event = []
					for event in story_events:
						new_event = []
						new_prev_event = []
						new_prev_prev_event = []
						new_prev_prev_prev_event = []
						named_entities = []
						if not prev_prev_prev_event:
							prev_prev_prev_event = prev_prev_event
							prev_prev_event = previous_event
							previous_event = event
							continue
						else:
							new_prev_prev_prev_event, named_entities = NEs(prev_prev_prev_event, named_entities)
							new_prev_prev_event, named_entities = NEs(prev_prev_event, named_entities)
							new_prev_event, named_entities = NEs(previous_event, named_entities)
							new_event, named_entities = NEs(event, named_entities)
							outfile.write(" ".join(new_prev_prev_prev_event)+" "+" ".join(new_prev_prev_event)+","+" ".join(new_prev_event)+" "+" ".join(new_event)+"\n")
							prev_prev_prev_event = prev_prev_event
							prev_prev_event = previous_event
							previous_event = event
					story_events = []
					#outfile.write("<EOS>\n")
