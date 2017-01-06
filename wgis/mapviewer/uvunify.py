import numpy as np
from numpy import random


ui = [1 * np.sin(np.radians(i)) for i in range(360)] 
vi = [1 * np.cos(np.radians(i)) for i in range(360)] 

uvd = np.arctan2(ui,vi) * 180/np.pi

uvdir = { round(d):(u,v) for d,u,v in zip(uvd,ui,vi)}

def unifyU(ud):
	try:
		if ud>180.0:
			ud = ud - 360.0
		if ud == -180.0:
			ud = 180.0			
		return uvdir[np.floor(ud)][0]
	except KeyError as ke:
		ud = 180
	finally:
		return uvdir[np.floor(ud)][0]



def unifyV(vd):
	try:
		if vd>180.0:		
			vd = vd - 360.0
		if vd == -180.0:
			vd = 180.0	
		return uvdir[np.floor(vd)][1]
	except KeyError as ke:
		vd = 180
	finally:
		return uvdir[np.floor(vd)][1]


uvect = np.vectorize(unifyU)

vvect = np.vectorize(unifyV)

"""
inuvdir = np.array([ i for i in range(45,90) ])

outu = uvect(inuvdir)
outv = vvect(inuvdir)


ouvdir = {ouvd : (ou,ov) for ouvd, ou, ov in zip(inuvdir,outu,outv)}
print ouvdir
"""


"""
inuvdir = np.array([[ i for i in range(5) ],
	[ i for i in range(90,95) ],
	[ i for i in range(180,185) ], 
	[ i for i in range(270,275) ] ]) 

outu = uvect(inuvdir)
outv = vvect(inuvdir)

print zip(outu,outv)
"""


"""
if __name__ ==  "__main__":
	ui = [1 * np.sin(np.radians(i)) for i in range(360)] 
	vi = [1 * np.cos(np.radians(i)) for i in range(360)] 

	uvd = np.arctan2(ui,vi) * 180/np.pi

	uvdir = { round(d):(u,v) for d,u,v in zip(uvd,ui,vi)}

#	print sorted(uvdir.keys())
	def unifyU(ud):
		if ud>180:
			ud = ud - 360
		return uvdir[ud][0]

	def unifyV(vd):
		if vd>180:		
			vd = vd - 360
		return uvdir[vd][1]


#	inuvdir = np.array([[ np.random.random_integers(0,359) for i in range(45) ],
#		[ np.random.random_integers(0,359) for i in range(45) ],
#		[ np.random.random_integers(0,359) for i in range(45) ], 
#		[ np.random.random_integers(0,359) for i in range(45) ] ]) 

	inuvdir = np.array([[ i for i in range(5) ],
		[ i for i in range(90,95) ],
		[ i for i in range(180,185) ], 
		[ i for i in range(270,275) ] ]) 


	uvect = np.vectorize(unifyU)

	vvect = np.vectorize(unifyV)

	outu = uvect(inuvdir)
	outv = vvect(inuvdir)

#	print outu
#	print outv
	print zip(inuvdir,outu, outv)

#	print uvdir
#	print uvdir.keys()

#	print uvdir[0],uvdir[22],uvdir[44]
#	print uvdir[0.0],uvdir[22.0],uvdir[44.0]
#	print uvdir[0.],uvdir[22.],uvdir[44.]

"""
