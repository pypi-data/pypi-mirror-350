import numpy as np
import taichi as ti
from scipy.interpolate import interp1d


######################################################################################
# Aux functions.

def simpson(x:np.ndarray) -> np.ndarray:
    if x.shape[0]==1:
        return x[0]
    assert x.shape[0]%2==1
    return np.sum(x[:-2:2] + 4*x[1:-1:2] + x[2::2], axis=0)/6

######################################################################################
# Functions of wavelength.

class Function:
    def __call__(self, x):
        x = np.asarray(x)
        if x.ndim==0:
            x = x[None]
        assert x.ndim == 1
        return self.compute(x)

    def compute(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.compute(x)

class ConstantFunction:
    def __init__(self, x):
        self.x = np.asarray(x)

    def compute(self, x: np.ndarray) -> np.ndarray:
        return np.repeat(self.x[None], x.shape[0], axis=0)

class GaussianFunction(Function):
    def __init__(self, center, width):
        self._center = np.asarray(center)
        self._width = np.asarray(width)
        self._2width2 = 2*self._width**2

    def compute(self, x):
        return np.exp(-(x[:,None]-self._center[None])**2/self._2width2)/self._width

class SimplifiedRGB(GaussianFunction):
    def __init__(self):
        super().__init__(
            center=[0.610,0.540,0.450],
            width=[0.050,0.040,0.030],
            )

class BlackbodyRadiation(Function):
    h = 6.62607015e-34 # J⋅Hz−1
    c = 299792458 # m/s
    k = 1.380649e-23 # J⋅K−1

    def __init__(self, temperature_in_K=[5800]):
        self.T = np.asarray(temperature_in_K)
        assert self.T.ndim==1, f"{self.T.shape=}"

    def compute(self, x):
        assert x.ndim==1, f"{x.shape=}"
        wavelength = x*1e-6 # meters
        b = 2.897771955e-3 # [m K], Wien displacement constant.
        print(f"Radiation peak at {b/self.T[0]*1e6:.3f} um")
        result = (2*self.h*self.c**2/wavelength[:,None]**5)/( np.exp( self.h*self.c/(self.k*self.T[None,:]*wavelength[:,None]) ) - 1 )
        return result 

class FunctionTable(Function):
    def __init__(self, x, y):
        self.x = np.asarray(x)
        self.y = np.asarray(y)
        self.poly = interp1d(x=x, y=y, axis=0, bounds_error=False, fill_value=0)

    @classmethod
    def from_csv(cls, name:str) -> 'FunctionTable':
        data = np.loadtxt(fname=name, dtype=np.float32, delimiter=None)
        return cls(x=data[:,0], y=data[:,1:])

    def compute(self, x):
        return self.poly(x)


################################################################################################################################
# Multispectral cross-polarization.

@ti.kernel
# cuda.jit((nbfloat[:,:,:,::1], nbfloat, nbfloat[::1], nbfloat[::1], nbfloat[::1], nbfloat, nbfloat, nbfloat, nbfloat, nbfloat[:,:,::1]))
def cross_polarization_filter_multi(n:ti.template(), dz:float, lambdas:ti.template(), nes:ti.template(), nos:ti.template(), 
                                    polarizerx:float, polarizery:float, filtrx:float, filtry:float, out:ti.template()):
    _sx, _sy, sz, _ = n.shape
    for w,x,y in out:
        # Constants for given wavelength
        dzoverlambda = dz/lambdas[w]
        ne = nes[w]
        no = nos[w]
        nooverne2 = (no/ne)**2
        # Incident wave field.
        Ex = ti.math.vec2(polarizerx,0)
        Ey = ti.math.vec2(polarizery,0)
        # Go layer by layer.
        for z in range(sz):
            mx = n[x,y,z,0]
            my = n[x,y,z,1]
            mz = n[x,y,z,2]
            ll = ti.math.sqrt(mx**2+my**2)+1e-15
            nx = mx/ll
            ny = my/ll
            p = Ex*nx+Ey*ny
            neff = no/ti.math.sqrt( nooverne2*(mx**2+my**2)+mz**2 )
            gammaz = np.pi*dzoverlambda*(neff-no)
            factor = ti.math.cmul(p, ti.math.vec2(1-ti.math.cos(2*gammaz), ti.math.sin(2*gammaz)))
            Ex = Ex-factor*nx
            Ey = Ey-factor*ny
        # Apply filter.
        out[w,x,y] = ti.math.length(Ex*filtrx+Ey*filtry)


def render_cp_multi(nn:np.ndarray, wavelengths:np.ndarray, ne:Function, no:Function, emission:Function, efficiency:Function, 
                    thickness:float, polarizer:float=0., deltafilter:float=np.pi/2):
    # assert isinstance(x, State)
    def todev(x):
        if isinstance(x, np.ndarray):
            f = ti.field(ti.f32, shape=x.shape)
            f.from_numpy(x.astype(np.float32))
            return f
        raise NotImplementedError

    assert nn.ndim==4 and nn.shape[3]==3, f"{nn.shape=}"
    f_nn = todev(nn)
    #
    assert wavelengths.ndim==1, f"{wavelengths.shape=}"
    f_wavelengths = todev(wavelengths)
    #
    n_ne = ne.compute(wavelengths)
    assert n_ne.shape == wavelengths.shape, f"{n_ne.shape=} {wavelengths.shape=}"
    f_ne = todev(n_ne)
    #
    n_no = no.compute(wavelengths)
    assert n_no.shape == wavelengths.shape, f"{n_no.shape=} {wavelengths.shape=}"
    f_no = todev(n_no)
    #
    n_emission = emission.compute(wavelengths)
    assert n_emission.shape == wavelengths.shape+(1,), f"{n_emission.shape=} {wavelengths.shape=}"
    n_efficiency = efficiency.compute(wavelengths)
    assert n_efficiency.shape == wavelengths.shape+(3,), f"{n_efficiency.shape=} {wavelengths.shape=}"
    # Allocate storage
    f_output = ti.field(ti.f32, shape=wavelengths.shape+nn.shape[:2])
    # Compute parameters.
    sz = nn.shape[2]
    dz = thickness/(sz-1)
    polarizer_vec=np.array([ np.cos(polarizer), np.sin(polarizer) ])
    filter_vec=np.array([ np.cos(polarizer+deltafilter), np.sin(polarizer+deltafilter) ])
    # Compute amplitudes for each wavelength.
    cross_polarization_filter_multi(f_nn, dz, f_wavelengths, f_ne, f_no, polarizer_vec[0], polarizer_vec[1], filter_vec[0], filter_vec[1], f_output)
    n_output = f_output.to_numpy()
    # Project to RGB.
    n_amp = n_output*n_emission[:,:,None] # (lambda,y,x)
    n_rgb = simpson(n_amp[:,:,:,None]*n_efficiency[:,None,None,:]) # (y,x,rgb)
    n_rgb /= np.max(n_rgb)
    return np.clip(n_rgb, 0., 1.) # Save in linear color space.
