#随机优化
#20171206

import math
import random

#解，对有很多变量的情况求最优解
#sol=[45,21]

#域，由二元组构成的列表，指定每个变量的最大最小值
#处理的是整数值，可以将实际域进行适当的放大
#domain=[(0,100),(0,100)]
#域转换，将算法域中的值转换到实际域中
#def changedomain(domain,newdomain,sol):return [newdomain[i][0]+sol[i]/(domain[i][1]-domain[i][0])*(newdomain[i][1]-newdomain[i][0]) for i in range(len(domain))]


#成本函数，计算输入解的成本，越小越好
#def costf(sol):return cost

#优化算法，输出最优解（及最优解成本）	
#随机搜索算法
def randomoptimize(domain,costf,N=1000):
	best=999999999
	bestr=None
	for i in range(N):
		#创建一个随机解
		r=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
		#计算成本
		cost=costf(r)
		#与目前为止的最优解进行比较
		if cost<best:
			best=cost
			bestr=r
	return r
	
#爬山法
def hillclimb(domain,costf):
	#创建一个随机解（整数值）
	sol=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
	while True:
		#创建相邻解的列表
		neighbors=[]
		#在每个方向上相对原值偏离一点
		for j in range(len(domain)):
			if sol[j]>domain[j][0]:
				neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
			if sol[j]<domain[j][0]:
				neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])	
		#在相邻解中寻找最优解
		current=costf(sol)
		best=current
		for j in range(len(neighbors)):
			cost=costf(neighbors[j])
			if cost<best:
				best=cost
				sol=neighbors[j]
		#如果没有更好的解，退出循环
		if best==current:
			break
	return sol

#随机重复爬山法
def randomhillclimb(domain,costf,N=50):
	best=9999999
	bestsol=None
	while N>0:
		sol=hillclimb(domain,costf)
		cost=costf(sol)
		if cost<best:
			best=cost
			bestsol=sol
		N=N-1
#输出成本（可选）
		print(best)
	return bestsol

#模拟退火算法,cool表示冷却速度
def annealingoptimize(domain,costf,T=1000.0,cool=0.95,step=1):
	#随机初始化值
	vec=[float(random.randint(domain[i][0],domain[i][1])) for i in range(len(domain))]
	while T>0.1:
		#选择一个索引值
		i=random.randint(0,len(domain)-1)
		#选择一个改变索引值的方向
		dir=random.randint(-step,step)
		#创建一个代表题解的新列表，改变其中一个值
		vecb=vec[:]#新的内存地址
		vecb[i]+=dir
		if vecb[i]<domain[i][0]:vecb[i]=domain[i][0]
		elif vecb[i]>domain[i][1]:vecb[i]=domain[i][1]
		#计算当前成本和新的成本
		ea=costf(vec)
		eb=costf(vecb)
		#是更好的解？或者是趋向最优解的可能的临界解？
		if(eb<ea or random.random()<pow(math.e,-(eb-ea)/T)):
			vec=vecb
		#降低温度
		T=T*cool
#输出成本（可选）
		print(eb)
	return vec
	
#遗传算法,popsize表示种群大小，elite表示优胜比例，maxiter表示进行代数
def geneticoptimize(domain,costf,popsize=50,step=1,mutprob=0.2,elite=0.2,maxiter=50):
	#变异操作
	def mutate(vec):
		i=random.randint(0,len(domain)-1)
		if(random.random()<0.5 and vec[i]>domain[i][0]):
			return vec[0:i]+[vec[i]-step]+vec[i+1:]
		elif(vec[i]<domain[i][1]):
			return vec[0:i]+[vec[i]+step]+vec[i+1:]
		else:
			return vec
	
	#交叉操作
	def crossover(r1,r2):
		i=random.randint(1,len(domain)-2)
		return r1[0:i]+r2[i:]
		
	#构造初始种群
	pop=[]
	for i in range(popsize):
		vec=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
		pop.append(vec)
	#每一代中胜出者数量
	topelite=int(elite*popsize)
	#主循环
	for i in range(maxiter):
		scores=[(costf(v),v) for v in pop]
		scores.sort()
		#胜利存活的种群
		ranked=[v for (s,v) in scores]
		pop=ranked[0:topelite]
		#添加胜出者变异和配对后的个体
		while (len(pop)<popsize):
			if (random.random()<mutprob):
				#变异
				c=random.randint(0,topelite)
				pop.append(mutate(ranked[c]))
			else:
				#交叉
				c1=random.randint(0,topelite)
				c2=random.randint(0,topelite)
				pop.append(crossover(ranked[c1],ranked[c2]))
#输出成本（可选）
		print(scores[0][0])
	return scores[0][1]
