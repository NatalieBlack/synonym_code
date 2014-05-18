import sys
import re
import json
import requests
import tokenize

def synonym(word):
    try:
        r = requests.get("http://words.bighugelabs.com/api/2/e47598ad741728aecaa3bd6a5a35630c/" + word + "/json")
        if r.status_code == 200:
            data = r.json()
            results = data[data.keys()[0]]
            return results['syn'][0]
        else:
           return word
    except:
        return word

lang = sys.argv[1]
langs = ["ruby", "python"]
if lang not in langs:
    sys.exit("Invalid language option.  Supported language options include: " + str(langs))

keys = open("keywords/" + lang + ".txt")

srcfn = sys.argv[2]
src = open(srcfn)

kws = []

for line in keys:
    kws.append(line.strip())

keys.close()

contents = src.read()
src.close()

g = tokenize.generate_tokens(open(srcfn).readline)
for code,tok,_,_,_ in g:
    if code == 1:
        contents = re.sub("(\W)" + tok + "(\W)", "\g<1>" + synonym(tok) + "\g<2>", contents)

print contents
