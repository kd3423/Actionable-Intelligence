import json

f = open("fuzzy_dict.txt")
fuzzy = eval(f.read())
f.close()

f = open("opinion_words.txt")
opinions = eval(f.read())
f.close()

new_opinion = {}

for op in opinions:
	for fuz in fuzzy:
		if op in fuzzy[fuz]:
			# print opinions[op]
			if fuz in new_opinion:
				new_opinion[fuz] += opinions[op]
			else:
				new_opinion[fuz] = opinions[op]
			# print fuz, op
			break
			# print new_opinions[fuz]
	else:
		new_opinion[op] = opinions[op]

f = open("opinion_words.txt","w")
f.write(json.dumps(new_opinion))
f.close()