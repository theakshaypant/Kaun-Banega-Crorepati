data=open("x.dat","r")
temp=open("y.dat","w")
for line in iter(data):
	l=line.split()
	s=l[0]
	for i in l[1:]:
		s+=("_"+i)
	temp.write(s)
data.close()
temp.close()
