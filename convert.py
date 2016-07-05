
def replace_underscore(stringlist,replaceitem):
                temp=stringlist[0]
                for i in stringlist[1:]:
			temp=temp+("_"+i)
			

                return temp
def convert():
	data=open("q8-11","r")
	x=open("try.dat","w")
	count=0
	cat=""
	ques=""
	ans=""
	o=["","","",""]
	s=""
	opt=0
	for line in iter(data):	
	  if(line=="\n"):
		pass
	  else:
		if(count%5==0):
			print line
			l=line.split()
			print l
			cat=l[-1]	
			m=l.pop()
			ques=replace_underscore(l,"_")
		if(line[0]=="*"):
			ans=line[1]
			l=line.split()[1:]
			m=replace_underscore(l,"_")
			if(opt>3):
				opt=0
				o=["","","",""]
			o[opt]="".join(m)
			opt=opt+1
			
		elif(count%5 !=0 and line[0]!="*"):
			l=line.split()[1:]
			m=replace_underscore(l,"_")
			if(opt>3):
				opt=0
				o=["","","",""]
			o[opt]="".join(m)
			opt=opt+1
		if(opt>3):
			s=ques+" "+o[0]+" "+o[1]+" "+o[2]+" "+o[3]+" "+ans+" "+cat+"\n"
			opt=0
			o=["","","",""]
			x.write(s)
		count=count+1
convert()
			
