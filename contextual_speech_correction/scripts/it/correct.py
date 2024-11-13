import rospy
from it.grammar import Grammar
from it.cyk import cyk

def correct(sentence, G : Grammar, epi, depth):
	sentence = cyk(sentence, G, epi, depth)
	return ' '.join([word.symbol for word in sentence])


