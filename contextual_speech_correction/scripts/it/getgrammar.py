import rospy
import os
def getgrammar(lines) -> list:
	grammar = []
	for line in lines:
		lexemes = scan(line)
		split1 = split_acc_to_elem(lexemes, '->')
		split2 = split_acc_to_elem(split1[1], '|')
		grammar.append((split1[0][0], split2))
	return grammar

# removes white spaces and returns sequence of lexemes
def scan(line : str) -> list:
	return line.split()

# splits list l two or more lists based on element s and returns a list of these resulting lists
def split_acc_to_elem(l : list, s : str) -> list:
	res = [[]]
	for elem in l:
		if (elem == s):
			res.append([])
		else:
			res[-1].append(elem)
	return res