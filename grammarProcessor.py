# -*- coding: utf-8 -*- 
import codecs


baseSamplePath = "/home/hope/arabic/samples/sample"
baseGrammarSamplePAth = "/home/hope/arabic/grsamples/sample"
newBaseGrammarPath = "/home/hope/arabic/newgrsamples/sample"

def simpleProcessor():
	for i in range(1, 1100):
		line_to_write = ""
		with codecs.open(baseSamplePath + str(i) + ".txt", "r", "utf-16") as f:
			for line in f:
				
				splitted_line = line.split("\t")
				line_to_write += splitted_line[0] + "\t"
				a = line_to_write
				grammar_categories = splitted_line[-1].strip("\n").split(";")
				if grammar_categories[0] == "Conjuction":
					if len(grammar_categories) > 1:
						if (grammar_categories[-1] == "Conj_Noun"):
							line_to_write += "cn"
						elif (grammar_categories[-1] == "Conj_Verb"):
							line_to_write += "cv"
						else:
							line_to_write += "conj"
					else:
						line_to_write += "conj"
				elif grammar_categories[0] == "Noun":
					if len(grammar_categories) > 1:
						if grammar_categories[1] == "GTNoun":
							if grammar_categories[3] == "Comp_Prefixoid":
								if grammar_categories[2] == "Genitive":
									line_to_write += "gt_noun_cp_gen"
								else:
									line_to_write += "gt_noun_cp"
							elif grammar_categories[2] == "Genitive":
								line_to_write += "gt_noun_gen"
							else:
								line_to_write += "gt_noun"
				elif grammar_categories[0] == "Verb":
					if grammar_categories[2] == "PersonThird" and grammar_categories[1] == "GTVerb":
						line_to_write += "gtv_pthird"
					elif grammar_categories[1] == "GTMasdar":
						line_to_write += "gt_masdar"
					else:
						line_to_write += "v"
						
				elif grammar_categories[0] == "Pronoun":
					if grammar_categories[1] == "GTPronounPossesivePronominal":
						line_to_write += "gt_ppp"
					elif grammar_categories[1] == "GTPronounProverbial":
						line_to_write += "gt_pp"
					else:
						line_to_write += "p"
				elif grammar_categories[0] == "Preposition" and grammar_categories[-1] == "Comp_Prefixoid":
					line_to_write += "cp"
				elif grammar_categories[0] == "Adjective":
					if grammar_categories[1] == "GTAdjective":

						if grammar_categories[-1] == "SuperlativeDegree":
							line_to_write += "adj_sup_deg"
						else:
							line_to_write += "gt_adj"
				elif grammar_categories[0] == "Participle" and grammar_categories[1] == "GTParticiple":
					line_to_write += "gt_participle"
				elif grammar_categories[0] =="Adverb":
					if grammar_categories[1] == "GTAdverb":
						line_to_write += "gt_adverb"
					else:
						line_to_write += "adv"
				elif grammar_categories[0] == "Invariable":
					line_to_write += "inv"
				elif grammar_categories[0] == "Numeral":
					line_to_write += "num"
				elif grammar_categories[0] == "Particle":
					line_to_write += "part"
				elif grammar_categories[0] == "Interjection":
					if grammar_categories[-1] == "Interjec_Noun":
						line_to_write += "in"
					elif grammar_categories[-1] == "Interjec_Verb":
						line_to_write += "iv"

				
				line_to_write += "\n"
		
		with codecs.open(baseGrammarSamplePAth + str(i) + ".txt", "w", "utf-16") as g:
			g.write(line_to_write)
		
		print i

def newGrammmarProcessor(terms):
	for i in range(1, 1100):
		line_to_write = ""
		with codecs.open(baseSamplePath + str(i) + ".txt", "r", "utf-16") as f:
			for line in f:
				splitted_line = line.split("\t")
				line_to_write += splitted_line[0] + "\t"
				grammar_categories = splitted_line[-1].strip("\n").strip(";").split(";")
				partOfSpeech = grammar_categories[0]
				grammar_categories = set(grammar_categories[1:])
				similarNode = terms[partOfSpeech][0]
				maxLength = -1
				bestIndex = 0
				for node in terms[partOfSpeech]:
					curLength = len(node.getTerms().intersection(grammar_categories))
					print node.getTerms()
					if maxLength < curLength:
						maxLength = curLength
						similarNode = node
					elif maxLength == curLength and (len(similarNode.getTerms()) > len(node.getTerms())):
						similarNode = node
				print similarNode.getName()



				print grammar_categories
				i = 0
				while (i < 100000000):
					i += 1

				line_to_write += "\n"



	
