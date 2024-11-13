#!/usr/bin/env python3
import rospy
import epitran
from it.grammar import Grammar 
from it.cfg2cnf import cfg2cnf
from it.correct import correct
from it.getgrammar import getgrammar
from std_msgs.msg import String
import sys
######## specify grammar below ##########
grammar_eng = ["S -> robot C | C",
			"C -> Cbar and C | Cbar",
			"Cbar -> V the N | V preposition the N | V the N preposition the N",
            "preposition -> on | from | in | at | inside | to | up", 
			"V -> go | clear | pick | inspect | grasp | search | place | stack | place | remove | retrieve | get | empty",
			"N -> front | back | right | left | block | blocks | barrel | cone | box | crate | greybox | greenbox | brick | pipe | tube | case | scene"]

grammar_hin = ['S -> रोबोट C | C',
            'C -> Cbar और C | Cbar',
            'Cbar -> Nmaster को V | Nmaster की V | Nmaster तक V | Nmaster V',
            'V -> हटाओ | उठाओ | जाओ | पकड़ो | जांचो | साफ़ करो | जांच करो',
            'Nmaster -> N | ज़मीं pe राखे N',
            'pe -> पे | पर',
            'N -> बक्सा | बक्से | पेड़ के पीछे | मलबा | ब्लॉक | ब्लॉक्स | रास्ता | रास्ते | ट्रैफिक कोन | कोन | मलबे']
######## specify depth below ##########
depth = 25
#######################################
epi = epitran.Epitran('eng-Latn') if (sys.argv[1] == 'english') else epitran.Epitran('hin-Deva')
G = cfg2cnf(Grammar(getgrammar(grammar_eng), epi)) if (sys.argv[1] == 'english') else cfg2cnf(Grammar(getgrammar(grammar_hin), epi))
pub = rospy.Publisher('/speech_recognition/speech_corrected', String, queue_size=10)

def run_speech_correction(data):
    corrected_speech = correct(data.data, G, epi, depth)
    pub.publish(corrected_speech)


if __name__ == '__main__':
    rospy.init_node('speech_corrector', anonymous=True)
    rospy.Subscriber("/speech_recognition/final_result", String, run_speech_correction)
    rospy.spin()


