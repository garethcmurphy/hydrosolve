import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

nstep=200
nx=400
nv=3
u=np.zeros((nx,nv))
prim=np.zeros((nx,nv))
gam=5./3.
dx=1./nx
dt=1e-3
time=0
x=np.linspace(0,1,num=nx)

def ptou(pri):
   u=np.zeros((nx,nv))
   rho=pri[:,0]
   v=pri[:,1]
   prs=pri[:,2]
   mom=rho*v
   u[:,0]=rho
   u[:,1]=mom
   u[:,2]=0.5*mom*v+prs/(gam-1)
   return(u)


def utop(u):
   pri=np.zeros((nx,nv))
   rho=u[:,0]
   mom=u[:,1]
   ene=u[:,2]
   vel=mom/(rho+1e-6)
   pri[:,0]=rho
   pri[:,1]=vel
   pri[:,2]=(ene-0.5*mom*vel)*(gam-1)
   return(pri)

def getmaxv(pri):
   rho=pri[:,0]
   vel=pri[:,1]
   prs=pri[:,2]
   cs=np.sqrt(gam*prs/rho)
   return(max(abs(vel)+cs))

def getflux(u):
   f=np.zeros((nx,nv))
   pri=utop(u)
   rho=pri[:,0]
   v=pri[:,1]
   prs=pri[:,2]
   mom=u[:,1]
   ene=u[:,2]
   f[:,0]=mom
   f[:,1]=mom*v+prs
   f[:,2]=(ene+prs)*v
   return(f)

prim[:,0]=1.
prim[:,1]=0.
prim[:,2]=1.
for i in range(int(nx/2),nx):
           prim[i,0]=0.1
           prim[i,1]=0.
           prim[i,2]=0.125

print (prim[:,2])
   
u=ptou(prim)
uold=u
pold=prim

fig = plt.figure()
gs = gridspec.GridSpec(nv,1)
ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[1,0])
ax3 = fig.add_subplot(gs[2,0])
ax1.plot(x,prim[:,0],'pres')
ax2.plot(x,prim[:,1],'pres')
ax3.plot(x,prim[:,2],'pres')
fig.show()
for nstep in range(0,nstep):
        print (time)
        um=np.roll(u, 1,axis=0) 
        up=np.roll(u,-1,axis=0) 
        um[0,:]   =um[1,:]
        up[nx-1,:]=up[nx-2,:]
        fm=getflux(um)
        fp=getflux(up)
        cfl=0.49
        dtdx=1./getmaxv(p)
        dt=dtdx*dx
        time=time+dt
        un=0.5*(um+up) - cfl*dtdx* (fp-fm)
        u=un
        p=utop(u)
        plt.close(fig)
        fig = plt.figure()
        gs = gridspec.GridSpec(nv,1)
        ax1 = fig.add_subplot(gs[0,0])
        ax2 = fig.add_subplot(gs[1,0])
        ax3 = fig.add_subplot(gs[2,0])
        ax1.plot(p[:,0])
        ax2.plot(p[:,1])
        ax3.plot(p[:,2])
        fig.show()
