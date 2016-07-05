data=open("try.dat","r")
x=open("q.dat","w")
ids="8-11:"
count=1
for line in iter(data):
	x.write(ids+str(count)+" "+line)
	count+=1
data.close()
x.close()
