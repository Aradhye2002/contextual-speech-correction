import rospy
from it.grammar import Term, Grammar
from it.costfunc import costfunc
# input: G is the grammar specified by the file 'grammar.txt' and sentence is a list of Term objecs
# output: returns corrected sentence as list of Term objects 
def cyk(sentence : str, G : Grammar, epi, depth):
	# here it is assumed that G is in CNF
	inf = float('inf')
	nonterms = G.nonterms
	r = len(nonterms)
	n = len(sentence)
	sentence = [epi.transliterate(word) for word in sentence.split()]
	preproc = [[dict() for j in range(n-i+1)] for i in range(n+1)]
	for i in range(n+1):
		for j in range(n-i+1):
			for T in G.terms:
				preproc[i][j][T] = costfunc(''.join(sentence[j:j+i]), T.pronounciation)
	dp = [[dict() for j in range(n-i+1)] for i in range(n+1)]
	for i in range(n+1):
		for j in range(n-i+1):
			for k in nonterms:
				dp[i][j][k] = [[inf, []] for l in range(depth)]
	for l in range(1, depth):
		for i in range(n+1):
			for j in range(n-i+1):
				for k in nonterms:
					prod = k.prod
					for subprod in prod:
						if len(subprod) == 1:
							cost = preproc[i][j][subprod[0]]
							if (dp[i][j][k][l][0] > cost):
									dp[i][j][k][l] = [cost, subprod]
						else:
							# try to split
							for sp in range(i+1):
								cost = dp[sp][j][subprod[0]][l-1][0]+dp[i - sp][j+sp][subprod[1]][l-1][0]
								s = dp[sp][j][subprod[0]][l-1][1]+dp[i - sp][j+sp][subprod[1]][l-1][1]
								if (dp[i][j][k][l][0] > cost):
									dp[i][j][k][l] = [cost, s]
	return dp[n][0][G.start][depth-1][1]

