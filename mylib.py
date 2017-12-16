#ŷ����þ���
def sim_distance(prefs,person1,person2):
	#�õ���ͬ��Ŀ���б�
    sim=[]
	for item in prefs[person1]:
	    if item in prefs[person2]:
		    sim.append(item)
	#���û�й�֮ͬ��������0
	if len(sim)==0:return 0
	#�������в�ֵƽ����
	sum_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in sim])
	return 1/(1+sqrt(sum_squares)
	
#Ƥ��ѷ���ϵ��
def sim_pearson(prefs,person1,person2):
	#�õ���ͬ��Ŀ���б�
    sim=[]
	for item in prefs[person1]:
	    if item in prefs[person2]:
		    sim.append(item)
	#���û�й�֮ͬ��������0
	n=len(sim)
	if n==0:return 0
	#������ƫ�����
	sum1=sum([prefs[person1][item] for item in sim])
	sum2=sum([prefs[person2][item] for item in sim])
	#��ƽ����
	sum1sq=sum([pow(prefs[person1[item],2) for item in sim])
	sum2sq=sum([pow(prefs[person2[item],2) for item in sim])
	#��˻���
	sumP=sum([prefs[person1][item]*prefs[person2][item] for item in sim])
	#����Ƥ��ѷ����ֵ
	num=sumP-(sum1*sum2/n)
	den=sqrt((sum1sq-pow(sum1,2)/n)*(sum2sq-pow(sum2,2)/n))
	if den==0:return 0
	return num/den
	
#�ӷ�ӳƫ�õ��ֵ��з�����Ϊƥ����
#���ؽ���ĸ��������ƶȺ�����Ϊ��ѡ����
def topMatches(prefs,person,n=5,similarity=sim_distance):
	scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]
	#���б���������������ǰ
	scores.sort()
	scores.reverse()
	return scores[0:n]
	
#������������ֵ�ļ�Ȩƽ����Ϊĳ���ṩ����
def getRecom(prefs,person,similarity=sim_distance):
	totals={}
	simSums={}
	for other in prefs:
		#�����Լ��Ƚ�
		if other==person:continue
		sim=similarity(prefs,person,other)
		#��������ֵ<=0�����
		if sim<=0:continue
		for item in prefs[other]:
			#ֻ���Լ�û�еĽ�������
			if item not in prefs[person] or prefs[person][item]==0:
				#���ƶ�*����ֵ
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				#���ƶ�֮��
				simSums.setdefault(item,0)
				simSums[item]+=sim
	#����һ����Ȩƽ�����б�
	rankings=[(totals[item]/simSums[item],item) for item in totals]
	rankings.sort()
	rankings.reverse()
	return rankings

#���Ӣ�ĵķִ�
def getWords(html):
	#ȥ������html���
	txt=re.compile(r'<[^>]+>').sub('',html)
	#�������з���ĸ�ַ���ֳ�����
	words=re.compile(r'[^A-Z^a-z]+').split(txt)
	#ת����Сд��ʽ
	return [word.lower() for word in words if word!='']
	
