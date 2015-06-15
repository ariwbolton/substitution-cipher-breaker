import copy
import timeit
import profile
import cProfile

s = "jca nekipieq pdra yizz sawazz oiqaeooza uyiwz"
s2 = "oeh qldu du psldu glaaq vtpoax tu oee qtjbp"

num = 0

# (oeh, oee)
# (oft, off)-> o:o, f:e, t:h
# (ego, egg)-> e:o, g:e, o:h

def runner(string, dict_path, added_words, already_known_dict):
    w = []
    found = []
    
    with open(dict_path) as dictionary:
        w = [word.strip().lower() for word in dictionary.readlines()]

    w = [word for word in w if '\'' not in word]
    w = w + added_words

    print "Length of dictionary used:", len(w)
    m = max(w, key=len)

    words_sorted = [[] for i in xrange(len(m) + 1)]

    for word in w:
        words_sorted[len(word)].append(word)
    for bucket in words_sorted:
        print len(bucket)
    string_sorted = sorted(string.split(), key=len, reverse=False)
    
    findMatches.num = 0
    findMatches(string_sorted[0], [already_known_dict],
                string_sorted[1:], words_sorted, string, found)

    found = list(set(found))

    for s in found:
        print s

def my_print(d):
    s = ""
    for i in xrange(d):
        s = s + "| "
    s = s + str(d)
    print s
    

def findMatches(encrypted, current_dict_list, nextList, words_sorted, string, found):
    length = len(encrypted)
    potentials = words_sorted[length]
    
    d = merge_dicts(current_dict_list)
    d_inv = invertMap(d)
    
    findMatches.num += 1

    #if findMatches.num % 100 == 0:
#        print findMatches.num
    #my_print(len(current_dict_list))
    
    # for each potential match
    #   isMatch returns (matched, dictionary)
    for p in potentials:
        matched, newDict = isMatch(encrypted, p, d, d_inv)

        if matched:
            if len(nextList) == 0:
                temp = copy.deepcopy(current_dict_list)
                temp.append(newDict)
                #print ''
                #print "Dict:", temp                    
                decrypt_string(temp, string, found)
            else:                    
                current_dict_list.append(newDict)
                
                findMatches(nextList[0],current_dict_list, nextList[1:],
                            words_sorted, string, found)
            
                current_dict_list.pop()

def merge_dicts(dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = dict()
    
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def decrypt_string(dict_list, string, found):
    d = merge_dicts(dict_list)
    
    reverse = {v: k for k, v in d.items()}
    
    decrypted_string = ""
    
    encrypted_list = string.split()
    
    for w in encrypted_list:
        for c in w:
            decrypted_string = decrypted_string + reverse[c]

        decrypted_string = decrypted_string + " "

    found.append(decrypted_string)
    print len(found)

# determines if word can be matched given current dictionary list
def isMatch(encrypted, potential, di, d):
    newD = dict()
    
    s = ""
       
    for i in xrange(len(potential)):
        if encrypted[i] not in d:
            # letter has not been mapped to (x -> c)
            
            if potential[i] in di:
                # mapping letter has already been used (l -> not c)
                return False, {}
            
            if encrypted[i] not in newD:
                if potential[i] in invertMap(newD):
                    return False, {}
                else:
                    newD[encrypted[i]] = potential[i]

            s = s + newD[encrypted[i]]
        else:                
            s = s + d[encrypted[i]]

    if False and s == potential:
        print ''
        print potential, "->", encrypted
        print di
        print invertMap(newD)

    return s == potential, invertMap(newD)


def invertMap(dictionary):
     return {v: k for k, v in dictionary.items()}


more_words = []
#known = {'e':'o', 'g':'e', 'o':'h'}
known = {}
path_to_dict = "my_dict2.txt"
#runner(s2, path_to_dict, more_words, known)
cProfile.run('runner(s2, path_to_dict, more_words, known)')

c_test = "\
m = {'a':'b', 'b':'c', 'c':'d','d':'e','e':'f'}\n\
from __main__ import isMatch"

#print timeit.timeit('isMatch("bcde", "abcd", m)', setup=c_test, number=100000) / 100000

'''
di = {'a':'b', 'b':'c', 'c':'d'}

iM, nD = isMatch("bcde", "abcd", di)
print iM
print nD

nl = [{'e': 'a', 'f': 's', 'i': 'i', 'h': 'c', 'l': 'z', 's': 'u',
  'r': 'w', 't': 'j', 'w': 'y'}, {'a': 'e', 'p': 'o', 'n': 'q'},
 {'d': 'n', 'v': 'k'}, {}, {}, {'k': 'r', 'b': 'p', 'o': 'd'}]
'''

