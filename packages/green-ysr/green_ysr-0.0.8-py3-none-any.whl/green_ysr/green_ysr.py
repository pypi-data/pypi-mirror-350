import numpy as np
import scipy.special as scisp
from mpmath import struveh
from scipy import constants as const
import time
import pickle
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def fdd( E, mu, T): #fermi Dirac function
    if T == 0:
        f = np.heaviside(-(E-mu), 1)
    else:
        f = 1/(1+np.exp((E-mu)/(const.k*T/const.e)))
    return f


def dynesdos(E, Gamma, Delta): #dynes function
    dos = np.real((np.abs(E+1j*Gamma))/np.sqrt((E+1j*Gamma)**2-Delta**2))
    return np.abs(dos)

def dynesConvolute(V,E_int,conductance,delta,T,gamma): #numerical convolution 
    curr = []
    for Vp in V:
        currp = np.trapz((conductance)*dynesdos(E_int-Vp,gamma,delta)*(fdd(E_int, Vp, T)-fdd(E_int,0, T)),x=E_int)
        curr.append(currp)
    return np.gradient(np.array(curr))


def dynesConvolute_fermi(V,E_int,conductance,T): #numerical convolution 
    curr = []
    for Vp in V:
        currp = np.trapz((conductance)*1*(fdd(E_int, Vp, T)-fdd(E_int,0, T)),x=E_int)
        curr.append(currp)
    return np.gradient(np.array(curr))

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL) 
def load_obj(name ):
    with open( name + '.pkl', 'rb') as f:
        return pickle.load(f)

def sim_save(sim):
    keys = ['type','N','direction','pitch_x','mode','U','alpha','angles']
    fname = 'green_ysr/out/sim'
    for i in keys:
        fname  =  fname +'_'+ i  + '{}'.format(sim.par[i])
    save_obj(sim,fname)

def plot_LS(sim):
    plt.figure()
    plt.imshow(sim.LS,extent=[sim.E[0]/sim.par['delta_s'],sim.E[-1]/sim.par['delta_s'],0,sim.length*const.physical_constants['Bohr radius'][0]*1e9],aspect='auto')
    plt.xlim(-2,2)
    plt.ylabel('Distance (nm)')
    plt.xlabel('Energy (meV)')


def set_size_cm(w,h, ax=None):
    """ w, h: width, height in cm """
    cm = 1/2.54
    if not ax: ax=plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w*cm)/(r-l)
    figh = float(h*cm)/(t-b)
    ax.figure.set_size_inches(figw, figh)


class green():
    def __init__(self,N,alpha,theta,r__,U=0,m=20.956,pf=0.274,delta=0.0000287,gamma=40e-6,mode=1):
        self.N = N
        self.s0 = np.array([[1,0],[0,1]])
        self.s1 = np.array([[0,1],[1,0]])
        self.s3 = np.array([[1,0],[0,-1]])
        self.theta_ = theta # theta of the spins
        self.alpha_ = alpha # alpha of the atoms in order
        self.U_ = U # potential scattering
        self.r__ = r__ #atomic positions
        self.m = m # mass electron
        self.pf = pf # fermi momentum
        self.delta = delta # delta superconductor
        self.gamma = gamma # dynes parameter
        self.mode = mode # dimensionality of fermi surface 1 circular, 2 squared

    def G0(self,r1,r2,E):
        delta = self.delta
        w = np.sqrt(delta**2-E**2)
        m=self.m
        pf=self.pf
        BCS = E/w*np.kron(self.s0,self.s0) + delta/w*np.kron(self.s1,self.s0)
        xi=np.kron(self.s3,self.s0)
        if self.mode==0:
            x = r1[0]-r2[0]
            y = r1[1]-r2[1]
            x1 = np.sqrt(x**2+y**2)
            ## mode=0 is for the spherical Fermi surface ##
            ## for this mode x1 is the radial distance and x2 is the angle ##
            u=complex(x1*pf , x1*m*w/(pf))
            a=scisp.jv(0,u) #bessel function 0th order u=argument
            b=complex(struveh(0,u)) #gives the struve function
            G0=m/2*(complex(np.real(a+complex(0,1)*b),0))*BCS + m/2*(complex(np.imag(a+complex(0,1)*b),0)) * xi
     
        if self.mode==1:
            x1=r1[0]-r2[0]
            x2=r1[1]-r2[1]
            delta = self.delta
            m=self.m
            pf=self.pf
            if np.abs(x1)<0.00001 and np.abs(x2)<0.00001:
                    G1=(2*m/np.pi)*BCS
                    G2=0.0
            elif np.abs(x2)<0.00001:
                G1=(np.exp(-(m*w/pf)*np.abs(x1))*( (1/np.abs(x1))*pf*np.sin(pf*(np.abs(x1)))+(pf**2)*np.cos(pf*np.abs(x1)) ) )*(m/(np.pi*pf**2))*BCS
                G2=(np.exp(-(m*w/pf)*np.abs(x1))*( (1/np.abs(x1))*pf*np.cos(pf*(np.abs(x1)))+(pf**2)*np.sin(pf*np.abs(x1)) ) -pf/np.abs(x1))*(m/(np.pi*pf**2))*xi
            elif np.abs(x1)<0.00001:
                G1=(np.exp(-(m*w/pf)*np.abs(x2))*( (1/np.abs(x2))*pf*np.sin(pf*(np.abs(x2)))+(pf**2)*np.cos(pf*np.abs(x2)) ) )*(m/(np.pi*pf**2))*BCS
                G2=(np.exp(-(m*w/pf)*np.abs(x2))*( (1/np.abs(x2))*pf*np.cos(pf*(np.abs(x2)))+(pf**2)*np.sin(pf*np.abs(x2)) ) -pf/np.abs(x2))*(m/(np.pi*pf**2))*xi
            elif x1+x2>=0.00001 and x1-x2>=0.00001:
                G1=(np.exp(-(m*w/pf)*(x1+x2))*(1/x1+1/x2)*pf*np.sin(pf*(x1+x2))+np.exp(-(m*w/pf)*(x1-x2))*(1/x1-1/x2)*pf*np.sin(pf*(x1-x2)) )*(m/(2*np.pi*pf**2))*BCS
                G2=(np.exp(-(m*w/pf)*(x1+x2))*(1/x1+1/x2)*pf*np.cos(pf*(x1+x2))+np.exp(-(m*w/pf)*(x1-x2))*(1/x1-1/x2)*pf*np.cos(pf*(x1-x2)) -2*pf/x1)*(m/(2*np.pi*pf**2))*xi
            elif x1+x2>0.00001 and x1-x2<0.00001:
                G1=(np.exp(-(m*w/pf)*(x1+x2))*(1/x1+1/x2)*pf*np.sin(pf*(x1+x2))+np.exp(-(m*w/pf)*(x2-x1))*(1/x2-1/x1)*pf*np.sin(pf*(x2-x1)) )*(m/(2*np.pi*pf**2))*BCS
                G2=(np.exp(-(m*w/pf)*(x1+x2))*(1/x1+1/x2)*pf*np.cos(pf*(x1+x2))+np.exp(-(m*w/pf)*(x2-x1))*(1/x2-1/x1)*pf*np.cos(pf*(x2-x1)) -2*pf/x2)*(m/(2*np.pi*pf**2))*xi
            elif x1+x2<=0.00001 and x1-x2<=0.00001:
                G1=(np.exp((m*w/pf)*(x1+x2))*(-1/x1-1/x2)*pf*np.sin(pf*(-x1-x2))+np.exp(-(m*w/pf)*(-x1+x2))*(-1/x1+1/x2)*pf*np.sin(pf*(-x1+x2)) )*(m/(2*np.pi*pf**2))*BCS
                G2=(np.exp((m*w/pf)*(x1+x2))*(-1/x1-1/x2)*pf*np.cos(pf*(-x1-x2))+np.exp(-(m*w/pf)*(-x1+x2))*(-1/x1+1/x2)*pf*np.cos(pf*(-x1+x2)) +2*pf/x1)*(m/(2*np.pi*pf**2))*xi
            elif x1+x2<0.00001 and x1-x2>0.00001:
                G1=(np.exp((m*w/pf)*(x1+x2))*(-1/x1-1/x2)*pf*np.sin(pf*(-x1-x2))+np.exp(-(m*w/pf)*(-x2+x1))*(-1/x2+1/x1)*pf*np.sin(pf*(-x2+x1)) )*(m/(2*np.pi*pf**2))*BCS
                G2=(np.exp((m*w/pf)*(x1+x2))*(-1/x1-1/x2)*pf*np.cos(pf*(-x1-x2))+np.exp(-(m*w/pf)*(-x2+x1))*(-1/x2+1/x1)*pf*np.cos(pf*(-x2+x1)) +2*pf/x2)*(m/(2*np.pi*pf**2))*xi
            G0 = G1+G2
        if self.mode==2:
            ## mode=2 is for the hexagonal-shaped Fermi contour
            ## x1=x and x2=y
            x1=r1[0]-r2[0]
            x2=r1[1]-r2[1]
            k=0
            R=[[-1/2,-np.sqrt(3)/2],[np.sqrt(3)/2,-1/2]]
            Rr=[[-1/2,np.sqrt(3)/2],[-np.sqrt(3)/2,-1/2]]
            if x2>=0 and x2>np.sqrt(3)*x1:
                D=np.matmul(Rr,[x1,x2])
                x1=D[0]
                x2=D[1]
            elif x2<=0 and x2<-np.sqrt(3)*x1:
                D=np.matmul(R,[x1,x2])
                x1=D[0]
                x2=D[1]
            chi=m*w/pf
            a=np.divide(2,np.sqrt(3))*np.abs(x2)
            b=x1-np.divide(1,np.sqrt(3))*np.abs(x2)
            c=x1+np.divide(1,np.sqrt(3))*np.abs(x2)
            if np.abs(x1) < 0.1 and np.abs(x2) < 0.1:
                G1 = np.sqrt(3)
                G2 = 0.0
            elif np.abs(x2)<0.001:
                G1=(2/(np.sqrt(3)*x1*pf))*np.exp(-chi*x1)*np.sin(pf*x1)+(np.cos(pf*x1)/np.sqrt(3))*np.exp(-chi*x1)
                G2=(2/(np.sqrt(3)*x1*pf))*np.exp(-chi*x1)*np.cos(pf*x1)-(np.sin(pf*x1)/np.sqrt(3))*np.exp(-chi*x1)-2/(np.sqrt(3)*x1*pf)
            elif np.abs(np.sqrt(3)*x1-np.abs(x2))<0.001*np.sqrt(3):
                G1=(1/(np.sqrt(3)*x1*pf))*np.exp(-2*chi*x1)*np.sin(2*pf*x1)+(np.cos(2*pf*x1)/np.sqrt(3))*np.exp(-2*chi*x1)
                G2=(1/(np.sqrt(3)*x1*pf))*np.exp(-2*chi*x1)*np.cos(2*pf*x1)-(np.sin(2*pf*x1)/np.sqrt(3))*np.exp(-2*chi*x1)-2/(2*np.sqrt(3)*x1*pf)
            else:
                G1=(np.exp(-chi*c)*np.sin(c*pf)*(1/(np.sqrt(3)*b)+1/(np.sqrt(3)*a))+np.exp(-chi*b)*np.sin(b*pf)*(-1/(np.sqrt(3)*a)+1/(np.sqrt(3)*c))+np.exp(-chi*a)*np.sin(a*pf)*(-1/(np.sqrt(3)*b)+1/(np.sqrt(3)*c)))/pf
                G2=(np.exp(-chi*c)*np.cos(c*pf)*(-1/(np.sqrt(3)*b)-1/(np.sqrt(3)*a))+np.exp(-chi*b)*np.cos(b*pf)*(1/(np.sqrt(3)*a)-1/(np.sqrt(3)*c))+np.exp(-chi*a)*np.cos(a*pf)*(1/(np.sqrt(3)*b)-1/(np.sqrt(3)*c))+2/(np.sqrt(3)*c))/pf
            G0=-(2*m/(np.sqrt(3)*np.pi))*G1*BCS-(2*m/(np.sqrt(3)*np.pi))*G2*xi
        return G0
    
    def V(self,theta,alpha,U):
        return alpha * np.cos(theta)*np.kron(self.s0,self.s3) + alpha*np.sin(theta)*np.kron(self.s0,self.s1) + U*np.kron(self.s3,self.s0)
    
    def M(self,E):
        n=self.N
        M = np.zeros((4*n,4*n),dtype=complex)
        for i in range(0,4*n,4):
            for j in range(0,4*n,4):
                M[i:i+4,j:j+4] = np.dot(self.G0(self.r__[i//4],self.r__[j//4],E),self.V(self.theta_[j//4],self.alpha_[j//4],self.U_[j//4]))
        return M

    def G0_(self,r_,E):
        G0_ = np.zeros((4*self.N,4),dtype=complex)
        n=0
        for i in range(0,4*self.N,4):
            G0_[i:i+4,0:4] = self.G0(self.r__[n],r_,E)
            n+=1
        return G0_
    
    def G(self,r_,E):
        MM = np.linalg.inv(np.identity(self.N*4,dtype=complex)-self.M(E))
        GG = np.dot(MM,self.G0_(r_,E))
        G = np.zeros((4,4),dtype=complex)
        G += self.G0((0,0),(0,0),E)
        n=0
        for i in range(0,4*self.N,4):
            G += np.dot(np.dot( self.G0(r_,self.r__[n],E) , self.V(self.theta_[n] ,self.alpha_[n],self.U_[n])), GG[i:i+4,0:4])
            n+=1
        return G

    def DOS(self,r_,E):
        return np.imag(np.trace(self.G(r_,E)))

    def ElecDOS(self,r_,E):
        return np.imag(np.trace(np.dot(self.G(r_,E),np.diag((1,1,0,0)))))

    def HoleDOS(self,r_,E):
        return np.imag(np.trace(np.dot(self.G(r_,E),np.diag((0,0,1,1)))))




class lattice():
    def __init__(self,type='atom',N=1,coords=None,pitch_x=0,direction=(1,0),alpha=0.04,U=0,spiral = 0,mode=0,m=18.7,pf = 0.21,delta_s = 1e-3,gamma_s=50e-6,E_px=500,E_range=(-5,5),V_range=(-3,3),spin_texture = None,T=1.3) -> None:
        self.N = N
        self.mode = mode
        self.m=m
        self.pf=pf
        self.delta_s = delta_s
        self.gamma_s = gamma_s
        self.U = np.zeros(self.N)+U
        self.alpha = np.zeros(self.N)+alpha
        self.V_range = V_range
        self.E_range = E_range
        self.E_px = E_px
        self.T = T
        # depending on type selected initialize an atom a 1D or 2D structure
        if type == 'atom':
            self.angles = [0,]
            self.coords = [[0,0]]
        if type == '1D':
            self.direction = direction
            self.pitch = pitch_x
            self.coords = self.coord_gen()
            # create angles
            self.angles = []
            a = 0
            for i in range(0,N):
                a += spiral
                self.angles.append(a)
        elif type == '2D':
            self.angles = np.zeros(N)
            self.coords = coords
        if spin_texture != None:
            self.angles = spin_texture

        # define energy and bias axes
        self.E = np.linspace(E_range[0]*self.delta_s,E_range[1]*self.delta_s,E_px)
        self.V = np.linspace(self.delta_s*V_range[0],self.delta_s*V_range[1],E_px)

        #initialize green function class
        self.c = const.physical_constants['Hartree energy'][0]/const.e
        self.sim = green(self.N , self.alpha , self.angles , self.coords,U=self.U ,m=self.m,pf=self.pf,delta=self.delta_s/self.c,mode=self.mode)
        self.par = { # to save parameters
            'type' : type,
            'N' : N,
            'coords' : self.coords,
            'direction' : direction,
            'pitch_x' : pitch_x,
            'mode' : mode,
            'm' : m,
            'pf' : pf,
            'delta_s' : delta_s,
            'gamma_s' : gamma_s,
            'U' : U,
            'alpha' : alpha,
            'E' : [E_range,E_px],
            'V' : [V_range,E_px],
            'angles' : spiral,
        }


    def coord_gen(self):
        n = 0
        coords = []
        for i in range(0,self.N):
            coords.append([n*self.direction[0],n*self.direction[1]])
            n+=self.pitch
        return coords

    def show_lattice(self):
        f,ax = plt.subplots(1)
        for i in self.coords:
            ax.scatter(i[0],i[1],color='C0')

    def map_coord_gen(self,resolution,size): # resolution is the number of points in one line, size= side of the square defining the mapped area
        self.resolution = resolution
        A = np.arange(-size/2,size/2+(size)/resolution,(size)/resolution)
        Gx = np.meshgrid(A,A)[0]
        Gy = np.meshgrid(A,A)[1]
        self.map_coords = [Gx,Gy]

    def show_lattice_map(self):
        f,ax = plt.subplots(1)
        for i in range(len(self.map_coords[0])):
            ax.scatter(self.map_coords[0][i],self.map_coords[1][i],color='C1')    
        for i in self.coords:
            ax.scatter(i[0],i[1],color='C0')
        ax.set_xlabel('x (a0)')
        ax.set_ylabel('Y (a0)')
        set_size_cm(8,8)

    def didv(self,coord):
        spec = []
        if self.U[0] != 0:
            for k in self.E/self.c:
                spec.append(np.sign(k)*self.sim.ElecDOS(coord, k + self.gamma_s*1j*np.sign(k)/self.c))
        else:
            for k in self.E/self.c:
                spec.append(np.sign(k)*(self.sim.DOS(coord, k + self.gamma_s*1j*np.sign(k)/self.c)))
        
        return np.array(spec/spec[-1])

    def didv_map_calc(self):
        #timecalc
        t0 = time.time()
        self.didv([0,0])
        t1 = time.time()
        total_time = (t1-t0)*self.resolution*self.resolution
        print('Simulation time = {}'.format(np.round(total_time/60,2))+' minutes')
        ####
        self.didv_map = np.zeros((self.resolution,self.resolution,self.E.shape[0]))
        for i in range(self.resolution):
            for j in range(self.resolution):
                self.didv_map[i,j,:] = self.didv([self.map_coords[0][i,j],self.map_coords[1][i,j]])


    def didv_conv(self,coord,Delta_t=1e-3,Gamma_t=50e-6):
        print('ciao')
        dos = self.didv(coord)
        conv_dos = dynesConvolute(self.V,self.E,dos,Delta_t,self.T,Gamma_t)
        return np.array(conv_dos)/np.array(conv_dos)[0]

    def didv_conv_fermi(self,coord):
        dos = self.didv(coord)
        conv_dos = dynesConvolute_fermi(self.V,self.E,dos,self.T,)
        return np.array(conv_dos)/np.array(conv_dos)[0]

    def linescan(self,density):
        x = self.pitch
        y = self.pitch*self.direction[1]
        self.length = np.sqrt(x**2+y**2)*(self.N+2)
        self.LSx = np.linspace(self.coords[0][0]-x,self.coords[-1][0]+x,(self.N)*density)
        self.LSy = np.linspace(self.coords[0][1]-y,self.coords[-1][1]+y,(self.N)*density)
        
        #timecalc
        t0 = time.time()
        self.didv((self.LSx[0],self.LSy[0]))
        t1 = time.time()
        total_time = (t1-t0)*len(self.LSx)
        print('Simulation time = {}'.format(np.round(total_time/60,2))+' minutes')
        ####

        self.LS = []

        for i in range(0,len(self.LSx)):
            self.LS.append(self.didv((self.LSx[i],self.LSy[i])))
        self.LS = np.array(self.LS)

        
    def LSconvolute(self,Delta_t,Gamma_t):
        self.LSC = np.zeros(self.LS.shape)
        self.V = np.linspace(self.delta_s*self.V_range[0],self.delta_s*self.V_range[1],self.E_px)
        for i in range(self.LS.shape[0]):
            self.LSC[i,:] = (dynesConvolute(self.V,self.E,self.LS[i,:],Delta_t,self.T,Gamma_t))
    
    def explorer(self):
        self.figure = plt.figure(figsize=(7,5))
        self.axMap = self.figure.add_subplot(2,2,1)
        self.axSpec = self.figure.add_subplot(2,2,2)
        self.figure.subplots_adjust(bottom=0)
        self.ax1 = self.figure.add_axes([0.20, 0.10, 0.65, 0.03])
        self.ax2 = self.figure.add_axes([0.20, 0.15, 0.65, 0.03])
        self.ax3 = self.figure.add_axes([0.20, 0.20, 0.65, 0.03])
        self.energyCut_slider = Slider(self.ax1,'Energy cut',self.E.min()*1e3,self.E.max()*1e3,valinit=0, valstep=(0.01))
        self.smin_slider = Slider(self.ax2, 'Min', self.didv_map.min(), self.didv_map.max(), valinit =self.didv_map.min())
        self.smax_slider = Slider(self.ax3, 'Max', self.didv_map.min(), self.didv_map.max(), valinit =self.didv_map.max()*0.5)            
        self.energyCut_slider.on_changed(self.update_energy)
        self.smin_slider.on_changed(self.update_cscale)
        self.smax_slider.on_changed(self.update_cscale)
        self.didv_map_cut = self.didv_map[:,:,0]
        self.im1 = self.axMap.imshow(np.flipud(self.didv_map_cut),interpolation='nearest')
        #axis labels
        self.axMap.set_xlabel('x (nm)')
        self.axMap.set_ylabel('y (nm)')
        self.axSpec.set_xlabel('Energy (meV)')
        self.axSpec.set_xlabel('LDOS (GN)')
        self.figure.suptitle('Click on the map to see the spectrum')

        self.figure.canvas.mpl_connect('button_press_event', self.onclick)
    def update_energy(self,val):
        self.cutIdx = (abs(self.E-val*1e-3)).argmin()
        self.im1.set_data(np.flipud(self.didv_map[:,:,self.cutIdx]))
        self.im1.set_clim(self.didv_map[:,:,self.cutIdx].min(),self.didv_map[:,:,self.cutIdx].max())
        # self.label.set_text('{} mV'.format(np.round(val,2)))
        self.figure.canvas.draw()

    def update_cscale(self,val):
        self.im1.set_clim([self.smin_slider.val,self.smax_slider.val])
        self.figure.canvas.draw()

    def onclick(self, event):
        if event.inaxes == self.axMap:
            self.axSpec.clear()
            x = int(round(event.xdata))
            y = int(round(event.ydata))
            self.axSpec.plot(self.E*1e3,np.flipud(self.didv_map)[x,y,:])
            self.axSpec.set_xlabel('Energy (meV)')
            self.axSpec.set_ylabel('LDOS (GN)')
            self.figure.canvas.draw()