import random
import copy
import math
import string

# NOTE: Perm dictionaries are already inverted!!

cipherTextName = "ciphertext1.txt"

class M:
	def __init__(self):
		self.M = dict()
		self.lnM = dict()
		self.alpha = "abcdefghijklmnopqrstuvwxyzW"

		self.ds = self.convertToWordArray("war-and-peace.txt")
		self.ciphertext = self.convertToWordArray(cipherTextName)

		self.createM()
		self.createLNM()

	def convertToWordArray(self, filename):
		with open(filename, "r") as f:
			ds = f.read()

		if filename == cipherTextName:
			self.ct = ds

		# Convert docstring to array and remove
		# non-alphabetic characters
		ds = list(ds)

		for i in range(len(ds)):
			if not ds[i].isalpha():
				ds[i] = " "

		# Rejoin and split docstring on whitespace
		ds = "".join(ds).split()

		return ds

	def createM(self):
		# initialize M
		for c in self.alpha:
			self.M[c] = dict()

			for c2 in self.alpha:
				self.M[c][c2] = 0

		# count frequencies
		for word in self.ds:
			# Count whitespace with first
			self.M["W"][word[0]] += 1

			# Count all middle pairs
			for i in xrange(1, len(word)):
				self.M[ word[i-1] ][ word[i] ] += 1

			# Count last with whitespace
			self.M[word[len(word) - 1]]["W"] += 1

	def createLNM(self):
		s = 0
		# initialize lnM and calculate sum
		for c in self.alpha:
			self.lnM[c] = dict()

			for c2 in self.alpha:
				self.lnM[c][c2] = self.M[c][c2]

				# account for zero frequency possibility
				if self.lnM[c][c2] == 0:	
					self.lnM[c][c2] = 1

				# increment sum
				s += self.lnM[c][c2]

		self.S = s
		self.lnS = math.log(s)
		
		for c in self.alpha:
			for c2 in self.alpha:
				self.lnM[c][c2] = math.log(self.lnM[c][c2])
		

	def printM(self):
		for c in self.alpha:
			d = self.M[c]
			a = []

			for c2 in self.alpha:
				a.append(d[c2])

			print c, a

	def printLNM(self):
		for c in self.alpha:
			d = self.lnM[c]
			a = []

			for c2 in self.alpha:
				a.append(d[c2])

			print c, a

class Perm:
	M = M()
	lnM = M.lnM
	lnS = M.lnS
	ciphertext = M.ciphertext
	ct = M.ct

	def __init__(self, *args):
		if len(args) == 0:
			self.perm = dict()

			for c in "abcdefghijklmnopqrstuvwxyz":
				self.perm[c] = c

			self.setlnPL()

		else:
			self.perm = copy.deepcopy(args[0].perm)
			self.lnPL = 0

		# self.plaintext = self.decryptCiphertext()
	

	def setPerm(self, p):
		self.perm = p

	# Must check for valid characters i and j before calling
	def swap(self, i, j):
		self.perm[i], self.perm[j] = self.perm[j], self.perm[i]

	def randomSwap(self):
		i = random.choice(string.lowercase)
		j = random.choice(string.lowercase)

		while i == j:
			j = random.choice(string.lowercase)

		self.swap(i, j)

		self.setlnPL()

	def decryptCiphertext(self):
		pt = ""

		for c in self.ct:
			if c.isalpha():
				pt = pt + self.perm[c]
			else:
				pt = pt + c

		return pt

	def decrypt(self, c):
		return self.perm[c]

	def setlnPL(self):
		p = 0

		for w in self.ciphertext:
			# Decrypt word
			word = "".join([self.perm[c] for c in list(w)])	

			# Count whitespace with first
			p += self.lnM["W"][ word[0] ]		

			# Count all middle pairs
			for i in xrange(1, len(word)):
				p += self.lnM[ word[i-1] ][ word[i] ]	

			# Count last with whitespace
			p += self.lnM[word[len(word) - 1]]["W"]			

		# Number of bigrams is 458 in ciphertext
		p -= 458 * self.lnS			

		self.lnPL = p


	def printPerm(self):
		print string.lowercase

		s = ""

		for c in string.lowercase:
			s = s + self.perm[c]

		print s


f = Perm()		# Initial permutation is identity permutation
n = 1

while True:
	f_star = Perm(f)
	f_star.randomSwap()

	if f.lnPL < f_star.lnPL:
		f = f_star
	else:		# f > f_star
		# Calculate probability
		r = math.exp(f_star.lnPL - f.lnPL)		

		# Get random number in [0,1)
		p = random.random()						

		# Success, take new permutation
		if p < r:								
			f = f_star
		else:
			pass

	# So we can watch the algorithm converge
	if n % 1000 == 0:
		print n, f.lnPL
		f.printPerm()
		print f.decryptCiphertext()

	'''
	# Potential stopping point
	if n % 4000 == 0:
		if f.lnPL < -2327:
			# Restart algorithm if we're stuck in a local maxima
			f = Perm()
		else:
			# Termination condition because
			# we know what we're looking for
			break
	'''
	
	n += 1
	