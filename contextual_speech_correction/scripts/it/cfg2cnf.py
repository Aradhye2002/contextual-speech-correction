import rospy
from it.grammar import Grammar, Term
from it.getgrammar import getgrammar

def TERM(G : Grammar) -> Grammar:
	terms = G.terms
	nonterms = G.nonterms
	new_nonterms = dict()
	for term in terms:
		N = Term()
		N.symbol = term.symbol+'_'
		N.prod = [[term]]
		new_nonterms[term] = N
	for N in nonterms:
		prod = N.prod
		for subprod in prod:
			for i in range(len(subprod)):
				T_N = subprod[i]
				if T_N.isterm:
					subprod[i] = new_nonterms[T_N]
	new_nonterms = list(new_nonterms.values())
	G.nonterms += new_nonterms
	G.terms_nonterms += new_nonterms
	for N in new_nonterms:
		G.nonterms_map[N.symbol] = N
	return G

def BIN(G : Grammar) -> Grammar:
	nonterms = G.nonterms
	for N in nonterms:
		prod = N.prod
		for i in range(len(prod)):
			subprod = prod[i]
			l = len(subprod)
			if not(subprod[0].isterm) and l > 2:
				new_nonterms_map = dict()
				X = Term()
				X.symbol = N.symbol+str(l-2)
				X.prod = [[subprod[l-2], subprod[l-1]]]
				new_nonterms_map[X.symbol] = X
				last = X
				for j in range(l-3, -1, -1):
					X = Term()
					X.symbol = N.symbol+str(j)
					X.prod = [[subprod[j], last]]
					new_nonterms_map[X.symbol] = X
					last = X
				prod[i] = [X]
				new_nonterms = list(new_nonterms_map.values())
				G.nonterms += new_nonterms
				G.terms_nonterms += new_nonterms
				for N in new_nonterms:
					G.nonterms_map[N.symbol] = N
	return G

def UNIT(G: Grammar) -> Grammar:
	nonterms = G.nonterms
	for N in nonterms:
		prod = N.prod
		flag = True
		while(flag):
			flag = False
			for subprod in prod:
				if (len(subprod) == 1 and not(subprod[0].isterm)):
					M = subprod[0]
					prod.remove(subprod)
					prod+= M.prod
					flag = True
	return G
def cfg2cnf(G : Grammar) -> Grammar:
	return UNIT(BIN(TERM(G)))
