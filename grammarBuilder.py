# -*- coding: utf-8 -*- 
import codecs
import re
import grammarProcessor 

baseRulesPath = "./Composite.txt"

grammarPath = "./LinearGrammar.txt"


class SetUnit:
	def __init__(self, terms, rulesInfo, name, isComplexLeft = False, isComplexRight = False):
		self._terms = set(terms)
		self._ruleNumbers = set(rulesInfo)
		self._name = name
		self._isComplexRight = isComplexRight #является ли правой частью правил вида С-> C A
		self._isComplexLeft = isComplexLeft

	def addRule(self, ruleNumber):
		self._ruleNumbers.append(ruleNumber)

	def getTerms(self):
		return self._terms

	def getName(self):
		return self._name

	def getRuleNumbers(self):
		return self._ruleNumbers

	def addRuleNumbers(self, ruleNumbers):
		self._ruleNumbers.update(ruleNumbers)

	def intersection(self, anotherSet):
		return self._terms.intersection(anotherSet._terms)

	def check(self, anotherSet):
		if (anotherSet._terms == self.intersection(anotherSet)):
			self.addRuleNumbers(anotherSet.getRuleNumbers())

	def isComplexRight(self):
		return self._isComplexRight

	def isComplexLeft(self):
		return self._isComplexLeft

			

def processTerm(term, partIndex, lineNumber, terms, ruleType):
	splittedTerm = re.split("\s+", term)
	partOfSpeech = splittedTerm[0]
	curSet = set(splittedTerm[1:])

	curRules = set()

	rule = (lineNumber, partIndex, ruleType)
	curRules.add(rule)
	isComplexRight = (ruleType == 0) and (partIndex == 1)
	isComplexLeft = (ruleType == 0) and (partIndex == 0)
	if terms.get(partOfSpeech) == None:
		terms[partOfSpeech] = [SetUnit(curSet, curRules, term, isComplexLeft, isComplexRight)]
	else:		
		found = 0
		for unit in terms[partOfSpeech]:
			intersectSet =  curSet.intersection(unit.getTerms())
			if ( len(curSet) == len( intersectSet ) ):
				unit.addRuleNumbers(curRules)
			elif ( len(unit.getTerms()) == len(intersectSet) ):
				curRules.update(unit.getRuleNumbers())
				isComplexRight = isComplexRight or unit.isComplexRight()
				isComplexLeft = isComplexLeft or unit.isComplexLeft()

			if (len(curSet) == len(intersectSet) and len(curSet) == len(unit.getTerms())):
				found = 1
		if ( not found ):
			terms[partOfSpeech].append(SetUnit(curSet, curRules, term, isComplexLeft, isComplexRight))

def printTerms(terms):
	for term in terms.keys():
		for node in terms[term]:
			print term, node.getTerms()
			for rule in node.getRuleNumbers():
				print rule[0], rule[1], rule[2]

def checkNonTerminal(term, partIndex, terms):
	splittedTerm = re.split("\s+", term)
	partOfSpeech = splittedTerm[0]
	curUnit = set(splittedTerm[1:])
	possibleTermUnits = terms[partOfSpeech]
	isNonTerminal = False 
	for possibleTerm in possibleTermUnits:
		if curUnit == possibleTerm.getTerms():
			#print curUnit
			ruleNumbers = possibleTerm.getRuleNumbers()
			for number in ruleNumbers:
				#print number[1], number[2], partIndex
				if (number[1] == int(number[2]) ):
					isNonTerminal = True

	return isNonTerminal


def buildSimpleGrammarRule(terms, grammar):
	for term in terms.keys():
		for node in terms[term]:
			for rule in node.getRuleNumbers():
				if rule[2] and (rule[0] in simpleRulesNumbers) and rule[1] == int(rule[2]):
					terminal = rules[rule[0]][1].lower()
					nonTerminal = node.getName().upper()
					grammar[rule[0]].append([nonTerminal, terminal, nonTerminal])	

def buildComplexRightRule(rule, grammar):
	pass

#строим правила вида A-> a (для каждого нетерминала)
def buildBaseRule(terminals, grammar):
	for term in terminals:
		grammar[-1].append([term.upper(), term.lower()])
	
def buildDependencies(terms, complexRules):
	dependencies = {}
	for term in terms.keys():
		for node in terms[term]:
			dependencies[node.getName()] = []
			for rule in node.getRuleNumbers():
				ruleType = rule[2]
				ruleNumber = rule[0]
				if (ruleNumber in complexRules) and (ruleType != rule[1]):
					dependencies[node.getName()].append(ruleNumber)
	return dependencies
def updateRules(baseRules, otherHelpRules, dependencies, rules, dependenceNode, updatedRules, grammar, nonTerminal):
	if dependencies.get(dependenceNode) != None:
		for number in dependencies[dependenceNode]:
			index = int(rules[number][0]) + 1
			leftNonTerminal = ""
			#правые правила
			#r = dependenceNode
			for r in updatedRules[number][index]:
				#if 0 == 0:
				if rules[number][0]:
					leftNonTerminal = r.upper()#C
				else:
					leftNonTerminal = r.upper() + "SUPERALL"

				#C -> A C
				"""
				A -> b A 
				A -> a
				нашли простое правило, 
				надо добавить соотвествующее ему для сложного правила вида
				C -> A C
				
				С -> b H1 		C -> b AC
				H1 -> b H1		AC -> b AC
				H1 -> a C 		AC -> a C
					
				C -> a C  		C -> a C

				"""
				newBaseRules = []
				newOtherRules = []
				
				for ru in baseRules:
					if (len(ru) == 1):
						grammar[number].append([leftNonTerminal, ru[0], leftNonTerminal])
						grammar[number].append([nonTerminal + leftNonTerminal, ru[0], leftNonTerminal])
						newBaseRules.append([ru[0], leftNonTerminal])
						newOtherRules.append([nonTerminal + leftNonTerminal, ru[0], leftNonTerminal])
						if not rules[number][0]:
							grammar[number].append([leftNonTerminal, ru[0]])
							newOtherRules.append([leftNonTerminal, ru[0]]) #AC -> a
					else:
						newBaseRules.append([ru[0], ru[1] + leftNonTerminal])
						newOtherRules.append([nonTerminal + leftNonTerminal, ru[0], ru[1] + leftNonTerminal])
						grammar[number].append([leftNonTerminal, ru[0], ru[1] + leftNonTerminal])
						grammar[number].append([nonTerminal + leftNonTerminal, ru[0], ru[1] + leftNonTerminal])
				newBaseRules.append([leftNonTerminal.lower()])		
				
				for ru in otherHelpRules:
					if len(ru) == 2:
						grammar[number].append([ru[0] + leftNonTerminal, ru[1], leftNonTerminal])
						newOtherRules.append([ru[0] + leftNonTerminal, ru[1], leftNonTerminal])
						if not rules[number][0]:
							grammar[number].append([ru[0] + leftNonTerminal, ru[1]])
							newOtherRules.append([grammar[number][-1]])
					else:
						newOtherRules.append([ru[0] + leftNonTerminal, ru[1], ru[2] + leftNonTerminal])
						grammar[number].append([ru[0] + leftNonTerminal, ru[1], ru[2] + leftNonTerminal])
				if rules[number][0]:		
					updateRules(newBaseRules, newOtherRules, dependencies, rules, r, updatedRules, grammar, leftNonTerminal)
				else:
					updateRules(newBaseRules, newOtherRules, dependencies, rules, r, updatedRules, grammar, leftNonTerminal)

		
		#C -> C A
		"""
		ALL правила формируем не тут, а уровнем выше
		Здесь добавляем С часть
		"""
		"""
		правую часть будем накручивать, поэтому нужны ALL правила
		формируем ALL часть
		С -> C AALL
		смотрим на правила для A
		1) A -> a
		2) A -> b A
		3) A -> c CP
			CP -> cp CP
			CP -> cp


		AALL -> a AALL
		AALL -> a

		AALL -> b AALL

		AALL -> c CPAALL
		CPAALL -> cp CPAALL
		CPAALL -> cp
		CPAALL -> cp AALL

		то есть ко всем нетерминалам в нетерминальных правилах добавляем _Нетерминал_ALL
		Для двусоставных правил(они же простые правые) добавляем правую часть ALL

		Теперь посмотрим на комбинацию с левой частью

		1) С -> d C
		2) C -> c
		3) C -> p CN
			CN -> cn CN
			CN -> cn 

		C -> d LEFTC
		LEFTC -> d LEFTC
		LEFTC -> c AALL
		C -> c AALL
		
		C -> p CNLEFTC
		CNLEFTC -> cn CNLEFTC
		CNLEFTC -> cn AALL


		"""
		"""
		for r in updateRules[number][2]:
			rightPart = r.upper() + "ALL"
			leftNonTerminal = "LEFT" + nonTerminal
			newBaseRules = []
			newOtherRules = []
			for ru in baseRules:
				if len(ru) == 1: # -> c
					grammar[number].append([nonTerminal, ru[0], rightPart])#C -> c AALL
					grammar[number].append([leftNonTerminal, ru[0], rightPart])#LEFTC -> c AALL
					newBaseRules.append([ru[0], rightPart])
					newOtherRules.append([grammar[number][-1]])
				else:
					newBaseRules.append([ru[0], leftNonTerminal])

					newBaseRules.append([ru[0], ru[1] + leftNonTerminal])
					newOtherRules.append([nonTerminal + leftNonTerminal, ru[0], ru[1] + leftNonTerminal])
					grammar[number].append([leftNonTerminal, ru[0], ru[1] + leftNonTerminal])
					grammar[number].append([nonTerminal + leftNonTerminal, ru[0], ru[1] + leftNonTerminal])

		"""



def buildComlexRules(grammar, rules):
	for rule in rules.keys():
		pass
		#grammar[rule].append()

terms = {}
def readRules(ruleTypeIndex, leftPartIndex, rightPartIndex):
	grammar = []
	leftRules = []
	rightRules = []
	
	rules = []
	terminals = set()

	with codecs.open(baseRulesPath, "r", "utf-8") as rulesFile:
		lineNumber = 0
		for line in rulesFile:
			splittedLine = re.split("[0-9]*\t+", line.strip("\n"))
			ruleType = splittedLine[ruleTypeIndex] == "R"
			leftPart = splittedLine[leftPartIndex]
			rightPart = splittedLine[rightPartIndex]
			#нетерминалы записываются в верхнем регистре
			if ruleType:
				leftRules.append([])
			else:
				rightRules.append([leftPart.lower(), rightPart.upper(), rightPart.lower()])

			rules.append([ruleType, leftPart, rightPart])
			terminals.add(rules[-1][ruleType + 1])
			processTerm(leftPart, 0, lineNumber, terms, ruleType)
			processTerm(rightPart, 1, lineNumber, terms, ruleType)
			lineNumber += 1

	updatedRules = []

	for i in range(len(rules)):
		grammar.append([])
		updatedRules.append([rules[i],[], []])
	grammar.append([])

	printTerms(terms)
	print "rules:"
	#правила с терминалами вида A->A b, A-> b A
	simpleRulesNumbers = set()
	#правила только с нетерминалами
	complexRules = set()
	i = 0
	for rule in rules:
		print rule
		ruleType = rule[0]
		if checkNonTerminal(rule[int(not ruleType) + 1], ruleType, terms):
			complexRules.add(i)
		else:
			simpleRulesNumbers.add(i)
		i += 1
			
	#строим самые простые правила вида A->a
	buildBaseRule(terminals, grammar)
	"""
	for ruleNumber in simpleRulesNumbers:
		ruleType = rules[ruleNumber][0]
		if ruleType: 
			#A -> b A
			pass
			#buildSimpleGrammarRule(rule, grammar)
		else:
			#A -> A b
			pass

	for rule in complexRules:
		if ruleType: 
			#наращиваем левую часть A -> B A
			pass
		else: 
			pass
			#наращиваем правую часть A -> A B
	"""
	#updatedRules = list : [[rule], [номера правил, ,], []]
	ALLRules = {}
	for term in terms.keys():
		for node in terms[term]:
			if node.isComplexRight():

				#grammar[-1].append(["ALL" + node.getName().upper(), node.getName().lower()])
				ALLRules[node.getName()] = [grammar[-1][-1]]

			isLeft = False
			for rule in node.getRuleNumbers():
				isLeft = isLeft or ((not rule[2]) and (rule[1] == 0))
				updatedRules[rule[0]][rule[1] + 1].append(node.getName())
			if isLeft:
				nonTerminal = node.getName().upper()
				grammar[rule[0]].append([nonTerminal, nonTerminal.lower(), nonTerminal + "SUPERALL"])#C -> с SUPERALL

	dependencies = dict(buildDependencies(terms, complexRules))
	helpIndex = 0
	superGrammar = {}#ключи - нетерминалы, находящиеся слева в правиле
	print dependencies
	leftComplexRules = {}
	
	for term in terms.keys():

		for node in terms[term]:

			#все правила, образующие данные терм
			allTerms = []
			baseComplexTerms = []	
			leftComplexRulesNumbers = []

			#правила вида A->A b надо группировать
			leftRulesNumbers = []
			complexALLNode = ""
			for rule in node.getRuleNumbers():
				ruleType = rule[2]
				ruleNumber = rule[0]
				if (rule[1] == int(rule[2])):
					if (ruleNumber in simpleRulesNumbers):
						terminal = rules[ruleNumber][1].lower()#b
						nonTerminal = node.getName().upper()#A
						baseRules = []
						otherHelpRules = []
						dependenceNode = node.getName()
						if ruleType:
							#A -> b A

							
							print node.getName(), ruleNumber
							newRule = [nonTerminal, terminal, nonTerminal]
							grammar[ruleNumber].append(newRule)
							
							baseRules = [[nonTerminal.lower()], [terminal, nonTerminal]]
							otherHelpRules = []								
									
							if node.isComplexRight():
								allTerms.append(newRule)
								#grammar[ruleNumber].append(["ALL" + nonTerminal, terminal, "ALL" + nonTerminal])

								#сохраняем только что добавленное правило еще и в ALLRules, чтобы потом можно было делать
								#рекурсивный update для друих сложных правил
								ALLRules[node.getName()].append(grammar[ruleNumber][-1])
								
							if node.isComplexLeft():
								baseComplexTerms.append(newRule)
							
							
						else:
							#A -> A b
							"""
							обрабатываем все правила вида A -> A b, A -> A c
							A -> a HSA
							HSA -> b HSA
							HSA -> c HSA
							HSA -> c
							HSA -> b
							"""
							superNonTerminal = nonTerminal + "SUPERALL"
							grammar[ruleNumber].append([superNonTerminal, terminal, superNonTerminal])#HSA -> b HSA
							grammar[ruleNumber].append([superNonTerminal, terminal])#HSA -> b
							otherHelpRules = [grammar[ruleNumber][-2], grammar[number][-1]]

						updateRules(baseRules,otherHelpRules, dependencies, rules, dependenceNode, updatedRules, grammar, nonTerminal)
						"""
						nonTerminal = "A"
						dependenceNode = "A"(без учета регистра)
						"""
					else:
						pass

							
				else:
					#C -> C A
					if (ruleNumber in complexRules) and (not ruleType):
						#заполнять левую часть сложных правил
						#leftComplexRulesNumbers.append(node.getName)
						if rule[1]:
							#для A
							pass
						else:
							#для C
							pass

				



			"""
			if (len(leftRulesNumbers) > 0):
				leftNonTerminal = node.getName().upper() #A
				nonTerminal = "HS" + leftNonTerminal #HSA
				leftTerminal = node.getName().lower() #a
				newRule = [leftNonTerminal, leftTerminal, nonTerminal]
				grammar[-1].append(newRule) #A -> a HSA
				if node.isComplexRight():
					allTerms.append(newRule)

				if node.isComplexLeft():
					baseComplexTerms.append(newRule)

				for number in leftSimpleRulesNumbers:
					print "BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
					terminal = rules[number][2].lower() # b или c
					grammar[number].append([leftNonTerminal, terminal, leftNonTerminal])
					grammar[number].append([leftNonTerminal, terminal])
					if node.isComplexRight():
						allTerms.append([leftNonTerminal, terminal, leftNonTerminal])
						allTerms.append([leftNonTerminal, terminal])
					if node.isComplexLeft():
						baseComplexTerms.append([leftNonTerminal, terminal, leftNonTerminal])
						baseComplexTerms.append([leftNonTerminal, terminal])
			"""
			

	buildComlexRules(grammar, leftComplexRules)
	"""
	for term in terms.keys():
			for node in terms[term]:
				leftNotSimpleRulesNumbers = []
				for rule in node.getRuleNumbers():
					ruleType = rule[2]
					ruleNumber = rule[0]
					if  (ruleNumber in complexRules):
						if (rule[1] != rule[2]):

							if ruleType:
								#A -> B A
								
								обрабатываем все правила вида A -> B A
								проходим по всем правилам, формирующим B

								
								#leftNotSimpleRulesNumbers.append(ruleNumber)
								pass


							else:
								#A -> A B
								pass
						else:
							if ruleType:
								leftNotSimpleRulesNumbers.append(ruleNumber)
	"""
				

	"""
	for term in terms.keys():
		for node in terms[term]:
			print term, node.getTerms()
			for rule in node.getRuleNumbers():
				print rule[0], rule[1], rule[2]
	"""


	

	print "grammar: "

	for i in range(len(grammar) - 1):
		print "RULEEEEEEE: ", i
		print rules[i]
		for rule in grammar[i]:
			print rule
			print ""

	print "simpleRules: ", len(simpleRulesNumbers)
	for rule in simpleRulesNumbers:
		print rule

	print "complexRules: ", len(complexRules)
	for rule in complexRules:
		print rule

	print "rules count: ", len(complexRules) + len(simpleRulesNumbers)

	print dependencies
	"""
	for rule in rules:
		print rule
		grammar.append(["S", rule[1].lower(), rule[2].upper()])
		if rule[0]:
			pass
		else:
			grammar.append([rule[2].upper(), rule[1].lower()])
	"""

readRules(1, -2, -1)
grammarProcessor.newGrammmarProcessor(terms)




		

