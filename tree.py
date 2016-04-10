# -*- coding: utf-8 -*- 
#!/usr/bin/python


import codecs
import re
import time


LEAFNODE = 3
NODE = 1

vocalism = [u"\u064B", u"\u064C", u"\u064D", u"\u064E", u"\u064F", u"\u0650", u"\u0651", u"\u0652", u"\u0653", u"\u0670"]

	

class Node:
	def __init__(self, letter, parent = None, nodeType = NODE):
		self.type = nodeType
		self.children = {}
		self.letter = letter
		self.parent = parent

	def addNode(self, letter = "$", attributes = None):
		if attributes == None:
			self.children[letter] = Node(letter = letter, parent = self)
		else:
			self.children[letter] = LeafNode(attributes)
		return self.children[letter]


	def findNode(self, letter):
		return self.children.get(letter)

	def getChildren(self):
		return self.children

	def getLetter(self):
		return self.letter

class LeafNode(Node):
	def __init__(self, attributes):
		Node.__init__(self, letter = "$", nodeType = LEAFNODE)
		self.attributes = attributes



	def setAttr(self, attributes):
		common = self.attributes.attributes & attributes.attributes
		self.attributes.attributes = self.attributes.attributes | (attributes.attributes - common)

class NodeAttributes:
	def __init__(self):
		self.attributes = 0

	def checkAttr(self, offset):
		if self.attributes & (1 << offset) == 0:
			return False
		else:
			return True

	def setAttr(self, offset):
		self.attributes = self.attributes&(~(1 << offset)) | (1 << offset)

	def getAttr(self):
		return self.attributes



class Tree:
	def __init__(self):
		self.root = Node("")


	def deleteNode(self, letter):
		pass

	def addWord(self, word, attributes = NodeAttributes()):
		currentNode = self.root
		for letter in word:
			childNode = currentNode.findNode(letter)
			if (childNode == None):
				currentNode = currentNode.addNode(letter = letter)
			else:
				currentNode = childNode

		#узел с последней буквой слова ведет в пустую вершину
		childNode = currentNode.findNode("$")
		if childNode == None:
			currentNode.addNode(attributes = attributes)
		else:
			childNode.setAttr(attributes)	

	

	def deleteWord(self, word):
		pass


	def findVocWord(self, word):
		curLetterPos = 0
		curNode = self.root
		while curLetterPos < len(word):
			curNode = curNode.findNode(word[curLetterPos])
			if (curNode == None):
				return False
			curLetterPos += 1
		curNode = curNode.findNode("$")
		return curNode != None
	
	
	def printTree(self):
		children = self.root.getChildren()
		offsets= []
		stack = []
		for key in children.keys():
			offsets.append(0)
			stack.append(children[key])
		while (len(stack) > 0):
			offset = offsets.pop()
			top = stack.pop()
			print " "*offset, top.getLetter()

			children = top.getChildren()
			for key in children.keys():
				stack.append(children[key])
				offsets.append(offset + 1)


	def findWord(self, word):
		curLetterPos = 0
		curNode = self.root
		while curLetterPos < len(word):
			curNode = curNode.findNode(word[curLetterPos])
			if (curNode == None):
				return self.checkComposite(word)
			curLetterPos += 1
		return curNode.findNode("$") != None

	def checkComposite(self, word):
		
		curLetterPos = 0
		stack = []
		curNode = self.root

		while curLetterPos < len(word):

			leafNode = curNode.findNode("$") 
			#если вершина является листом
			if leafNode != None:
				isPrefix = False
				#проверяем, может ли она быть префиксом
				attr = leafNode.attributes.getAttr() & ~(1 << 3) & ~(1 << 2)
				print leafNode.attributes.getAttr()
				if (leafNode.attributes.checkAttr(3)):
					stack.append(attr)
					isPrefix = True

				#проверяем, может ли она завершать композит
				if (leafNode.attributes.checkAttr(2)):
					print "2"
					mask = leafNode.attributes.getAttr()
					while (len(stack) > 0):
						if mask & stack.pop() == 0:
							return False
					if self.findVocWord(word[curLetterPos + 1:]):
						return True
					curNode = self.root
					stack.append(attr)
				elif isPrefix and curLetterPos < len(word) - 1:
					curNode = self.root
			curNode = curNode.findNode(word[curLetterPos])
			if (curNode == None):
				return False
			curLetterPos += 1
		leafNode = curNode.findNode("$")
		if leafNode != None:
			if (leafNode.attributes.checkAttr(2)):
					mask = leafNode.attributes.getAttr()
					while (len(stack) > 0):
						if mask & stack.pop() == 0:
							return False
						
					return True
			else:
				return False
		else:
			return False




def checkAttributes(line, attrRules, attr):
	

	for rule in attrRules:
		featNumber = min(len(rule) - 1, len(line) - 1)
		count = 0
		for j in range(featNumber):
			if (line[j + 1] == rule[j]):
				count += 1
		if count == featNumber:
			for offset in rule[-1]:
				attr.setAttr(offset)

	partOfSpeech = line[1]
	if partOfSpeech == "Adjective":
		offset = possiblePrefixoids.get(partOfSpeech + " " + line[2] + " " + line[3])
		if offset != None:
			attr.setAttr(offset)
			attr.setAttr(3)


	if partOfSpeech == "Noun":
		offset = possiblePrefixoids.get(partOfSpeech + " " + line[2] + " " + line[4])
		if offset != None:
			attr.setAttr(3)
			attr.setAttr(offset)
			

		
	if partOfSpeech == "Noun":
		offsets = rightParts.get(partOfSpeech + " " + line[3])
		if offsets != None:
			for offset in offsets:
				attr.setAttr(offset)

	for i in range(1, len(line)):
		offsets = rightParts.get(partOfSpeech + " " + line[i])
		if offsets != None:
			attr.setAttr(2)
			for offset in offsets:
				attr.setAttr(offset)


	for i in range(2, len(line)):
		offset = possiblePrefixoids.get(partOfSpeech + " " + line[i])
		if offset != None:
			attr.setAttr(offset)
			attr.setAttr(3)
	
	return attr
	

def getAttributes(line):
	attr = NodeAttributes()
	attr = checkAttributes(line, rules, attr)
	return attr

def readRules():
	rulesPath = "/home/hope/arabic/Composite.txt"
	rightParts = {}
	rules = []
	possiblePrefixoids = {}
	leftParts = {}
	with codecs.open(rulesPath, "r", "utf-8") as f:
		count = 4 #будем записывать дополнительную информацию начиная с 5-го бита
		for line in f:
			splittedLine = re.split("\t+", line)
			
			offset = leftParts.get(splittedLine[-2])
			if offset == None:
				leftParts[splittedLine[-2]] = count
				offset = count
				count += 1

			if rightParts.get(splittedLine[-1].strip("\n")) == None:
				rightParts[splittedLine[-1].strip("\n")] = [offset]
			else:
				rightParts[splittedLine[-1].strip("\n")].append(offset)
	
	"""
	for key in leftParts.keys():
		possiblePrefixoids.append(key.split(" "))
		possiblePrefixoids[-1].append(leftParts[key])
	"""
		
	for key in rightParts.keys():
		rules.append(key.split(" "))
		rules[-1].append(rightParts[key])

	possiblePrefixoids = dict(leftParts)
	return possiblePrefixoids, rules, rightParts

possiblePrefixoids, rules, rightParts = readRules()
print "rules:\n", rules
print "rightParts:\n", rightParts
print "possiblePrefixoids:\n", possiblePrefixoids

print rules
def readTreeFromDiskOld():
	baseSamplePath = "/home/hope/arabic/samples/sample"
	tree = Tree()
	for i in range(1, 1100):
		with codecs.open(baseSamplePath + str(i)+".txt", "r", "utf-16") as f:
			for line in f:
				splittedLine = re.split("\t|;", line.strip("\n"))
				attributes = getAttributes(splittedLine)
				lexeme = splittedLine[0]
				tree.addWord(lexeme, attributes)
		print i
	return tree

def readTreeFromDisk():
	baseGrammarSamplePAth = "/home/hope/arabic/grsamples/sample"
	labels = {}
	label_num = 4
	tree = Tree()
	for i in range(1, 1100):
		with codecs.open(baseGrammarSamplePAth + str(i) + ".txt", "r", "utf-16") as f:
			for line in f:
				splittedLine = re.split("\t", line.strip("\n"))
				foundLabel = labels.get(splittedLine[-1]) 
				if foundLabel == None:
					labels[splittedLine[-1]] = label_num
					label_num += 1
					foundLabel = label_num
				attr = NodeAttributes()
				attr.setAttr(label_num)
				tree.addWord(splittedLine[0], attr)
		print i
	return tree





def vocalismProcessor(lexeme):
	for voc in vocalism:
		lexeme = lexeme.replace(voc, u"")
	return lexeme




tree = Tree()
tree.addWord("simple", NodeAttributes())
tree.addWord("soo", NodeAttributes())
print tree.findWord("simple")
print tree.findWord("soo")
print tree.findWord("s")
tree.printTree()



tstart = time.clock()
t = readTreeFromDisk()
print "read tree time: ", time.clock() - tstart
"""
with codecs.open("/home/hope/arabic/results.txt", "w", "utf-16") as res:
	while (input()) :
		with codecs.open("/home/hope/arabic/ArabicSaudiArabia.Words.txt", "r", "utf-16") as f:
		#with codecs.open("/home/hope/arabic/test.txt", "r", "utf-16") as f:
			for line in f:
				word = vocalismProcessor(line.strip("\r\n"))
				if not t.findWord(word):
					res.write(word + "\n")

"""
