'''Use bsearch tree to search the name
	If we can't find the name, return a proper position 
		which we can insert the new name in this position
'''
def bsearch(a, v, start=0, end=None):
	if end is None:
		end = len(a)

	n = end - start

	# base case
	if n==0 or (n==1 and a[start][0]!=v):
		if v > a[-1][0]:
			return start+1,False
		else:
			return start,False
	if n==1:
		return start,True

	# recursive case
	midpos = (n-1)//2
	midval = a[start+midpos][0]

	if v <= midval:
		return bsearch(a, v, start, start+midpos+1)
	return bsearch(a, v, start+midpos+1, end)

'''Idea:
	Firstly, read all and store all names and scores in a list named name_list.
	
	Then, using bsearch to find the postion of the name.
		if name exist, get the correlative score of this name, if it's smaller
			than best_score, then change the score by best_score.
		if name doesn't exist, insert new name into proper postion, set the score "0"
	
	Lastly,write new name_list into store.txt 
'''
def WriteScore(name, best_score):
	name = name.lower()
	name_list = []

	f = open('store.txt', 'r')
	for line in f:
		line = line.split()
		name_list.append([line[0], line[1]])
	f.close()
	
	order,flag = bsearch(name_list,name)
	if flag == True:
		if int(name_list[order][1]) < best_score:
			name_list[order][1] = str(best_score)

	elif flag == False:
		name_list.insert(order, (name,str(best_score)))

	f = open('store.txt', 'w')
	for line in name_list:
		f.write(line[0])
		f.write(" ")
		f.write(line[1])
		f.write("\n")
	f.close()
		
'''Idea:
	Firstly, read all and store all names and scores in a list named name_list. 

	Then, using bsearch to find the name.
		If name exist, return the correlative score of name.
		If name doesn't exist, return 0
'''
def ReadScore(name):
	name = name.lower()
	name_list = []

	f = open('store.txt', 'r')
	for line in f:
		line = line.split()
		name_list.append((line[0], line[1]))
	f.close()

	order,flag = bsearch(name_list, name)
	if flag == False:
		return 0
	else:
		return int(name_list[order][1])











