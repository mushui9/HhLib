#欧几里得距离
def sim_distance(prefs,person1,person2):
	#得到共同条目的列表
    sim=[]
	for item in prefs[person1]:
	    if item in prefs[person2]:
		    sim.append(item)
	#如果没有共同之处，返回0
	if len(sim)==0:return 0
	#计算所有差值平方和
	sum_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in sim])
	return 1/(1+sqrt(sum_squares)
	
#皮尔逊相关系数
def sim_pearson(prefs,person1,person2):
	#得到共同条目的列表
    sim=[]
	for item in prefs[person1]:
	    if item in prefs[person2]:
		    sim.append(item)
	#如果没有共同之处，返回0
	n=len(sim)
	if n==0:return 0
	#对所有偏好求和
	sum1=sum([prefs[person1][item] for item in sim])
	sum2=sum([prefs[person2][item] for item in sim])
	#求平方和
	sum1sq=sum([pow(prefs[person1[item],2) for item in sim])
	sum2sq=sum([pow(prefs[person2[item],2) for item in sim])
	#求乘积和
	sumP=sum([prefs[person1][item]*prefs[person2][item] for item in sim])
	#计算皮尔逊评价值
	num=sumP-(sum1*sum2/n)
	den=sqrt((sum1sq-pow(sum1,2)/n)*(sum2sq-pow(sum2,2)/n))
	if den==0:return 0
	return num/den
	
#从反映偏好的字典中返回最为匹配者
#返回结果的个数和相似度函数均为可选参数
def topMatches(prefs,person,n=5,similarity=sim_distance):
	scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]
	#对列表进行排序，最高者在前
	scores.sort()
	scores.reverse()
	return scores[0:n]
	
#利用他人评价值的加权平均，为某人提供建议
def getRecom(prefs,person,similarity=sim_distance):
	totals={}
	simSums={}
	for other in prefs:
		#不和自己比较
		if other==person:continue
		sim=similarity(prefs,person,other)
		#忽略评价值<=0的情况
		if sim<=0:continue
		for item in prefs[other]:
			#只对自己没有的进行评价
			if item not in prefs[person] or prefs[person][item]==0:
				#相似度*评价值
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				#相似度之和
				simSums.setdefault(item,0)
				simSums[item]+=sim
	#建立一个加权平均的列表
	rankings=[(totals[item]/simSums[item],item) for item in totals]
	rankings.sort()
	rankings.reverse()
	return rankings

#针对英文的分词
def getWords(html):
	#去除所有html标记
	txt=re.compile(r'<[^>]+>').sub('',html)
	#利用所有非字母字符拆分出单词
	words=re.compile(r'[^A-Z^a-z]+').split(txt)
	#转化成小写形式
	return [word.lower() for word in words if word!='']
	
