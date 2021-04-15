from base64 import urlsafe_b64encode,urlsafe_b64decode
q=bin
g=int
l=len
w=str
h=range
z=chr
c=ord
def d(text,encoding='utf-8',errors='surrogatepass'):
 b=q(g.from_bytes(text.encode(encoding,errors),'big'))[2:]
 return b.zfill(8*((l(b)+7)//8))
def M(b,encoding='utf-8',errors='surrogatepass'):
 n=g(b,2)
 return n.to_bytes((n.bit_length()+7)//8,'big').decode(encoding,errors)or '\0'
def e(password,E,k):
 E=g(E)
 f=''
 Q=''
 W=''
 for a in password:
  f+=k[(k.index(a)-E)%l(k)]
 for b in f:
  Q+=k[(k.index(b)-E)%l(k)]
 for c in Q:
  W+=k[(k.index(c)-E)%l(k)]
 return W
def V(password,E,k):
 E=g(E)
 f=''
 Q=''
 W=''
 for a in password:
  f+=k[(k.index(a)+E)%l(k)]
 for b in f:
  Q+=k[(k.index(b)+E)%l(k)]
 for c in Q:
  W+=k[(k.index(c)+E)%l(k)]
 return W
def j(s,E):
 E,s=w(E),w(s)
 N=[]
 for i in h(l(s)):
  F=E[i%l(E)]
  N.append(z((c(s[i])+c(F))%256))
 Y=urlsafe_b64encode("".join(N).encode()).decode()
 return Y
def X(Y,E):
 E=w(E)
 D=[]
 s=urlsafe_b64decode(Y).decode()
 for i in h(l(s)):
  F=E[i%l(E)]
  D.append(z((256+c(s[i])-c(F))%256))
 return "".join(D)
def enc_data(anything,master_password):
 S=j(anything,master_password)
 u=d(S)
 return u
def dec_data(anything,master_password):
 U=M(anything)
 I=X(U,master_password)
 return I