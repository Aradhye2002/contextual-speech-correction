import rospy
class Term:
	prod = None
	symbol = None
	isterm = False
	pronounciation = None

def get_symbol_set(prod):
	s = set()
	s.add(prod[0])
	for subprod in prod[1]:
		for x in subprod:
			s.add(x)
	return s

class Grammar:
	terms_nonterms = None
	terms_nonterms_map = None
	terms = None
	terms_map = None
	nonterms = None
	nonterms_map = None
	start = None

	def __init__(self, grammar : list, epi):
		self.terms_nonterms_map = dict()
		self.nonterms_map = dict()
		self.terms_map = dict()

		for prod in grammar:
			for symbol in get_symbol_set(prod):
				if symbol not in self.terms_nonterms_map:
					term = Term()
					term.symbol = symbol
					self.terms_nonterms_map[symbol] = term
		for prod in grammar:
			symbol = prod[0]
			term = self.terms_nonterms_map[symbol]
			self.nonterms_map[symbol] = term
			term.prod = []
			for x in prod[1]:
				term.prod.append([])
				for y in x:
					term.prod[-1].append(self.terms_nonterms_map[y])
		self.start = self.terms_nonterms_map[grammar[0][0]]
		self.nonterms = list(self.nonterms_map.values())
		self.terms_nonterms = list(self.terms_nonterms_map.values())
		for term_nonterm in self.terms_nonterms:
			if term_nonterm not in self.nonterms:
				self.terms_map[term_nonterm.symbol] = term_nonterm
		self.terms = list(self.terms_map.values())
		for term in self.terms:
			term.pronounciation = epi.transliterate(term.symbol)
			term.isterm = True
		for nonterm in self.nonterms:
			nonterm.isterm = False
