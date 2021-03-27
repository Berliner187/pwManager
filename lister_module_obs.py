import enc_module_obs
F=print
Y=range
i=open
H=bool
a=False
G=str
I=enc_module_obs.DecryptionByTwoLevels
u=enc_module_obs.EncryptionByTwoLevels
import random
n=random.randrange
s=random.shuffle
import os
b=os.path
k=os.name
O=os.system
from csv import DictReader,DictWriter
y,m,f,T,mc,L,P="\033[33m","\033[36m","\033[35m","\033[32m","\033[0m","\033[31m","\033[4m"
J='files/'
z=1000
w=J+".lister.dat"
def S():
 O('cls'if k=='nt'else 'clear')
def CL(OO0OO000O0O0O0O0O,O0OO00O0OOOOOOO00):
 S()
 F(y+'Please, wait ...'+mc)
 global z
 for D in Y(z):
  K=[]
  for M in O0OO00O0OOOOOOO00:
   K.append(M)
  s(K)
  B=''.join(K)
  h=u(B,OO0OO000O0O0O0O0O)
  with i(w,"a")as E:
   E.write(h)
   E.write('\n')
   E.close()
 S()
def GL(O0O00000OO00OOO0O,OOOOO0OOO0OO00OO0):
 X=[]
 with i(w)as O00O0O0O0O000000O:
  c=0
  for C in O00O0O0O0O000000O:
   c+=1
   if c==O0O00000OO00OOO0O:
    r=I(C,OOOOO0OOO0OO00OO0)
    for N in r:
     X.append(N)
 return X
t=J+".keys.csv"
A=b.exists(t)
def HH(O0OO0O00O0O0O0O00):
 global z
 if A==H(a):
  v=n(52)
  p=n(z)
  l=u(v,O0OO0O00O0O0O0O00)
  e=u(p,O0OO0O00O0O0O0O00)
  v,p=G(v),G(p)
  with i(t,mode="w",encoding='utf-8')as O0000O000OO0O0O0O:
   W=DictWriter(O0000O000OO0O0O0O,fieldnames=['key','additional_key'])
   if A==H(a):
    W.writeheader()
   W.writerow({'key':l,'additional_key':e})
   return G(v),G(p)
 else:
  with i(t,encoding='utf-8')as OOO0OOOOO0O0OO0O0:
   d=DictReader(OOO0OOOOO0O0OO0O0,delimiter=',')
   for g in d:
    v=g["key"]
    p=g["additional_key"]
   q=I(v,O0OO0O00O0O0O0O00)
   U=I(p,O0OO0O00O0O0O0O00)
   return G(q),G(U)