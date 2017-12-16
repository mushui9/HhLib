import cmath
import math
import random
import optimization

#reload('optimization.py')

domain=[(0,100),(0,100),(0,100),(0,100)]
newdomain=[(1,10),(1,10),(0,2),(80,130)]#厚度，相对介电常数，损耗因子,频率


c=3e8
Z0=377

def changedomain(domain,newdomain,sol):
	return [newdomain[i][0]+sol[i]/(domain[i][1]-domain[i][0])*(newdomain[i][1]-newdomain[i][0]) for i in range(len(domain))]

def costf(sol):
	newsol=changedomain(domain,newdomain,sol)
	d=newsol[0]*1e-3
	epsr=newsol[1]
	epsf=newsol[2]
	w=2*math.pi*newsol[3]*1e9
	EPS=epsr-1j*epsf
	gamma=1j*w/c*cmath.sqrt(EPS)
	Zf=Z0/cmath.sqrt(EPS)*cmath.tanh(gamma*d)
	return abs((Zf-Z0)/(Zf+Z0))**2
	
sol=optimization.geneticoptimize(domain,costf,popsize=50,step=1,mutprob=0.2,elite=0.2,maxiter=100)
#sol=optimization.annealingoptimize(domain,costf,T=10000.0,cool=0.95,step=1)
#sol=optimization.randomhillclimb(domain,costf,N=100)
newsol=changedomain(domain,newdomain,sol)
print(newsol)

	
