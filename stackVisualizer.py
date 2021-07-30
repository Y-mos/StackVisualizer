import cairosvg
import svgwrite as svg
import sys

def split(line):
	L1=line.replace(';','|')
	L2=L1.split('|')
	L3=[L.split(',') for L in L2]
	return L3,['#FFFFFF' for i in L3]


def drawStack(ofnamePrefix,stack,cols,prms):
	if len(stack)==0:
		return
	ofname='{}-{}.svg'.format(ofnamePrefix,prms['ofsuffix'])
	dwg=svg.Drawing(ofname)
	w,h=prms['w'],prms['h']
	f=prms['fs']
	gx,gy=prms['gx'],prms['gy']
	l,L=prms['lw_block'],prms['lw_stack']
	D=prms['dir']
	N=sum([len(G) for G in stack])

	S='stroke-width:{};stroke:#000000;'.format(L)
	if D=='H':
		W,H=(gx+w)*N+gx,h+2*gy
		dwg.add(svg.shapes.Line(start=(-L/2,0),end=(W,0),style=S))
		dwg.add(svg.shapes.Line(start=(-L/2,H),end=(W,H),style=S))
		dwg.add(svg.shapes.Line(start=(0,0),end=(0,H),style=S))
	else:
		W,H=w+2*gx,(gy+h)*N+gy
		dwg.add(svg.shapes.Line(start=(0,0),end=(0,H+L/2),style=S))
		dwg.add(svg.shapes.Line(start=(W,0),end=(W,H+L/2),style=S))
		dwg.add(svg.shapes.Line(start=(0,H),end=(W,H),style=S))
	
	s='stroke-width:{};stroke:#000000;'.format(l)
	ts='text-anchor:middle;alignment-baseline:middle;font-size:{}pt;font-family:monospace;'.format(f)
	n=1
	for ig in range(len(stack)):
		col=cols[ig]
		G=stack[ig]
		for v in G:
			if D=='H':
				x,y=(n-1)*(gx+w)+gx,gy
			else:
				x,y=gx,H-n*(gy+h)
			dwg.add(svg.shapes.Rect(insert=(x,y),size=(w,h),fill=col,style=s))
			dwg.add(svg.text.Text(text=v,insert=(x+w/2,y+h/2),style=ts))
			n+=1
	dwg.save()
	cairosvg.svg2png(url=ofname,write_to=ofname[:-4]+'.png',parent_width=W,parent_height=H)

colors={'w':'#FFFFFF',
		'r':'#FFCFCF',
		'y':'#FFFFCF',
		'g':'#CFFFCF',
		'c':'#CFFFFF',
		'b':'#CFCFFF',
		'm':'#FFCFFF',
		'o':'#FFCF7F',
		'k':'#CFCFCF'
		}
if __name__=='__main__':
	if len(sys.argv)<2:
		print('Usage:')
		print('  sys.argv[0] [inputFileName]')
		sys.exit()
	ifname=sys.argv[1]
	ofindex=0
	stack=[]
	cols=[]
	cnt=0
	prmsDef={'w':50,'h':30,'fs':16,'gx':6,'gy':4,'lw_block':1,'lw_stack':2,'ofsuffix':'','dir':'V'}
	prms=prmsDef.copy()
	with open(ifname,'r') as fptr:
		for line in fptr:
			if len(line)>=2:
				if line[0]=='[':
					if prms['ofsuffix']=='':
						prms['ofsuffix']='{}'.format(ofindex)
					drawStack(ifname,stack,cols,prms)
					stack,cols=split(line[1:-1])
					cnt=0
					ofindex+=1
					prms['ofsuffix']=''
				elif line[0]=='E':
					break
				elif line[0]=='%':
					continue
				elif line[0]=='P':
					if cnt<len(stack):
						cols[cnt]=colors[line[1:-1]]
						cnt+=1
				elif line[0]=='#':
					if cnt<len(stack):
						cols[cnt]=line[:-1]
						cnt+=1
				elif line[0]=='S':
					prms['ofsuffix']=line[1:-1]
				elif line[0]=='N':
					prms['ofsuffix']='{}'.format(ofindex)+'-'+line[1:-1]
				elif line[0]=='D':
					prms['dir']=line[1:-1]
				elif line[0]=='W':
					argint=int(line[1:-1])
					prms['w']=argint if argint>0 else prmsDef['w']
				elif line[0]=='H':
					argint=int(line[1:-1])
					prms['h']=argint if argint>0 else prmsDef['h']
				elif line[0]=='X':
					argint=int(line[1:-1])
					prms['gx']=argint if argint>0 else prmsDef['gx']
				elif line[0]=='Y':
					argint=int(line[1:-1])
					prms['gy']=argint if argint>0 else prmsDef['gy']
				elif line[0]=='F':
					argint=int(line[1:-1])
					prms['fs']=argint if argint>0 else prmsDef['fs']
				elif line[0]=='L':
					argint=int(line[1:-1])
					prms['lw_stack']=argint if argint>0 else prmsDef['lw_stack']
				elif line[0]=='l':
					argint=int(line[1:-1])
					prms['lw_block']=argint if argint>0 else prmsDef['lw_block']
		if True:
			if prms['ofsuffix']=='':
				prms['ofsuffix']='{}'.format(ofindex)
			drawStack(ifname,stack,cols,prms)
