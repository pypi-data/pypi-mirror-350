
from ibvpy.sim.i_xmodel import IXModel
from traits.api import \
    Property, cached_property, \
    provides, \
    Array
import bmcs_utils.api as bu
import numpy as np

from .xdomain_fe_grid import XDomainFEGrid


@provides(IXModel)
class XDomainFEGridAxiSym(XDomainFEGrid):

    vtk_expand_operator = Array(np.float64)

    def _vtk_expand_operator_default(self):
        return np.identity(3)

    Diff0_factor = bu.Float(1, BC=True)

    Diff0_abc = Array(np.float64)

    def _Diff0_abc_default(self):
        D3D_33 = np.array([[0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 1]], np.float64)
        D2D_22 = np.array([[0, 0],
                           [0, 1]], np.float64)
        return np.einsum('ab,cc->abc', D3D_33, D2D_22)

    Diff1_abcd = Array(np.float64)

    def _Diff1_abcd_default(self):
        delta = np.vstack([np.identity(2),
                           np.zeros((1, 2), dtype=np.float64)])
        return 0.5 * (
            np.einsum('ac,bd->abcd', delta, delta) +
            np.einsum('ad,bc->abcd', delta, delta)
        )

    det_J_Em = Property(depends_on='MESH,GEO,CS,FE')
    '''Jacobi matrix in integration points
    '''
    @cached_property
    def _get_det_J_Em(self):
        r_Em = np.einsum(
            'im,Eic->Emc',
            self.fets.N_im, self.x_Eia
        )[..., 1]
        return r_Em * np.linalg.det(self.J_Emar)

    B0_Eimabc = Property(depends_on='+input')

    @cached_property
    def _get_B0_Eimabc(self):
        x_Eia = self.x_Eia
        r_Em = np.einsum(
            'im,Eic->Emc',
            self.fets.N_im, x_Eia
        )[..., 1]
        B0_Eimabc = np.einsum(
            'abc,im, Em->Eimabc',
            self.Diff0_abc, self.fets.N_im, 1. / r_Em
        )
        return B0_Eimabc

    B_Eimabc = Property(depends_on='MESH,GEO,CS,FE')
    '''Kinematic mapping between displacements and strains in every
    integration point.
    '''
    @cached_property
    def _get_B_Eimabc(self):
        return self.B1_Eimabc + self.B0_Eimabc
