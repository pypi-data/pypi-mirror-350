import os, sys
import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt

sys.path.append('../wakis')

from tqdm import tqdm
from scipy.constants import c

from wakis import SolverFIT3D
from wakis import GridFIT3D 
from wakis import WakeSolver
from wakis.sources import Beam

import pytest 

# Turn true when running local
flag_plot_3D = False 

@pytest.mark.slow
class TestMPILossyCavity:
    # Regression data
    WP = np.array([-1.20513623e-18 ,-3.43161145e-14 ,-9.12255548e-11 ,-5.96997512e-08,
                    -1.14173019e-05 ,-6.67499094e-04 ,-1.20239747e-02 ,-6.53062215e-02,
                    -9.26520639e-02 , 2.78321623e-02  ,1.25518516e-01 , 7.30670041e-02,
                    -1.90239810e-02 ,-4.85596408e-02 ,-3.20357619e-02 ,-1.41604640e-02,
                    6.08356174e-02 , 8.46570691e-02 ,-5.47181776e-02 ,-1.16180823e-01,
                    1.96111216e-02 , 9.92679050e-02 , 2.71878152e-02 ,-5.20035156e-02,
                    -4.06137472e-02 ,-1.13185667e-02 , 1.23530805e-02 , 7.68524041e-02,
                    2.25859758e-02 ,-9.37436643e-02 ,-5.75287185e-02 , 6.39890431e-02,
                    8.01280003e-02 ,-2.25671230e-02 ,-5.80154107e-02 ,-1.67525750e-02,
                    1.87720028e-03 , 4.10247646e-02  ,5.36731566e-02 ,-3.30682943e-02,
                    -8.35234400e-02 ,-3.49965114e-03 , 8.57976513e-02 , 3.52580927e-02,
                    -5.59291793e-02 ,-3.74168173e-02 ,-1.57790071e-03 , 2.16477574e-02,
                    4.65687493e-02 , 1.13356268e-02 ,-5.61946649e-02 ,-5.45040228e-02,
                    4.41993189e-02  ,7.38920452e-02 ,-1.60854441e-02 ,-5.54896162e-02,
                    -1.77145556e-02 , 1.61884877e-02 , 3.33170207e-02 , 2.63165394e-02,
                    -1.83733826e-02 ,-5.94726314e-02 ,-1.15493543e-02 , 6.90379083e-02,
                    3.30361171e-02 ,-4.32087737e-02 ,-4.14862834e-02 , 2.95742481e-03,
                    3.11653273e-02 , 2.43513549e-02 , 5.17266702e-03 ,-3.70591561e-02,
                    -4.24818163e-02 , 3.09681557e-02 , 5.76902933e-02 ,-4.78519848e-03,
                    -5.02625318e-02 ,-2.09821868e-02 , 2.46893459e-02 , 2.77009485e-02,
                    1.12395692e-02 ,-1.34117335e-02 ,-4.22375110e-02 ,-8.34037808e-03,
                    4.81709861e-02 , 3.05819110e-02 ,-2.98222467e-02 ,-4.38079436e-02,
                    6.51694708e-03 , 3.11637911e-02 , 1.61475003e-02 ,-1.03231050e-03,
                    -2.84581274e-02 ,-2.64695160e-02  ,1.92431962e-02 , 4.34036616e-02,
                    3.00897180e-03 ,-4.36364833e-02 ,-2.09601909e-02 , 2.48741294e-02,
                    2.47321674e-02  ,5.34334063e-03 ,-1.56819510e-02 ,-2.75503078e-02])

    Z = np.array([ 7.77970188e+00   -0.j      ,   -3.85415882e+00  +14.7587971j,
                -3.61177110e+00   +4.52999754j,  1.11502695e+01  +16.94389961j,
                -1.48367615e+00  +31.13414676j ,-2.42369181e+00  +20.20481814j,
                1.32631009e+01  +32.26388931j , 7.84469425e-02  +48.06727516j,
                -2.04548300e+00  +36.16821013j , 1.55741147e+01  +48.44883647j,
                1.37311998e+00  +66.93221773j ,-2.19747672e+00  +53.47374311j,
                1.86245241e+01  +66.56951352j  ,2.65234275e+00  +89.33983678j,
                -2.94989399e+00  +73.40544312j , 2.31553338e+01  +88.22587886j,
                4.16269453e+00 +118.22389548j ,-4.66524583e+00  +98.31868989j,
                3.07626943e+01 +116.67578417j , 6.41211027e+00 +160.3569522j,
                -8.36053398e+00 +133.90634108j , 4.61970915e+01 +160.6857645j,
                1.14408149e+01 +237.02472112j ,-1.72907188e+01 +200.58798515j,
                9.34171798e+01 +257.88692816j , 4.19201258e+01 +475.3131594j,
                -3.28372915e+01 +498.40274299j , 1.47161715e+03 +896.91077291j,
                4.46726052e+02-1074.75272128j , 1.48368867e+02 -150.95840903j,
                -7.65707535e+01  -95.4006897j ,  4.13011813e+01 -115.5293095j,
                5.96957058e+01  +64.38392007j ,-4.17351813e+01  +65.90769948j,
                4.16431845e+01  +45.42941094j , 5.22637205e+01 +182.75009977j,
                -2.42252500e+01 +183.45582422j , 8.56170191e+01 +206.784262j,
                9.77958353e+01 +444.21692899j , 8.26325734e+01 +560.54204926j,
                1.44414393e+03 +765.73788438j , 7.29867370e+02-1096.11716581j,
                1.17986711e+02 -317.31632024j ,-4.56173056e+01 -277.3675436j,
                7.54525872e+01 -200.5232469j ,  2.20725250e+01  -36.10606952j,
                -3.94369541e+01  -81.45040661j , 6.08389766e+01  -53.3224972j,
                1.97319998e+01  +64.35491532j ,-1.82274232e+01   +4.8794245j])

    Ez = np.array([ 2.21799580e+01, -5.78362380e+00 ,-6.00531608e+00 ,-1.01718118e+00,
                    1.73468186e+00 , 1.29313000e+00 ,-9.69312994e+00 ,-2.59107426e+01,
                    -4.73006858e+01 ,-7.11016384e+01 ,-9.36971115e+01 ,-1.12676454e+02,
                    -1.28296571e+02 ,-1.40866374e+02 ,-1.48363099e+02 ,-1.51635428e+02,
                    -1.48185125e+02 ,-1.37740237e+02 ,-1.19948398e+02 ,-9.23354987e+01,
                    -6.04105997e+01 ,-3.06532160e+01 ,-1.17749936e+01 ,-3.12574866e+00,
                    -7.35339521e-01 ,-1.13085658e-01 , 7.18247535e-01 , 8.73829036e-02])

    img_folder = 'tests/007_img/'

    def test_mpi_import(self):
        # ---------- MPI setup ------------
        global use_mpi
        try:
            # can be skipped since it is handled inside GridFIT3D
            from mpi4py import MPI 

            comm = MPI.COMM_WORLD  # Get MPI communicator
            rank = comm.Get_rank()  # Process ID
            size = comm.Get_size()  # Total number of MPI processes
            if size > 1:
                use_mpi = True
            else:
                use_mpi = False
        except:
            use_mpi = False
        
        print(f"Using mpi: {use_mpi}")

    def test_mpi_simulation(self):

        # ---------- Domain setup ---------

        # Geometry & Materials
        solid_1 = 'tests/stl/007_vacuum_cavity.stl'
        solid_2 = 'tests/stl/007_lossymetal_shell.stl'

        stl_solids = {'cavity': solid_1, 
                    'shell': solid_2
                    }

        stl_materials = {'cavity': 'vacuum', 
                        'shell': [30, 1.0, 30] #[eps_r, mu_r, sigma[S/m]]
                        }

        # Extract domain bounds from geometry
        solids = pv.read(solid_1) + pv.read(solid_2)
        xmin, xmax, ymin, ymax, ZMIN, ZMAX = solids.bounds

        # Number of mesh cells
        Nx = 60
        Ny = 60
        NZ = 140
        global use_mpi
        grid = GridFIT3D(xmin, xmax, ymin, ymax, ZMIN, ZMAX, 
                        Nx, Ny, NZ, 
                        use_mpi=use_mpi, # Enables MPI subdivision of the domain
                        stl_solids=stl_solids, 
                        stl_materials=stl_materials,
                        stl_scale=1.0,
                        stl_rotate=[0,0,0],
                        stl_translate=[0,0,0],
                        verbose=1)
        if use_mpi:
            print(f"Process {grid.rank}: Handling Z range {grid.zmin} to {grid.zmax} with {grid.Nz} cells")

        # ------------ Beam source & Wake ----------------
        # Beam parameters
        sigmaz = 10e-2      #[m] -> 2 GHz
        q = 1e-9            #[C]
        beta = 1.0          # beam beta 
        xs = 0.             # x source position [m]
        ys = 0.             # y source position [m]
        ti = 3*sigmaz/c     # injection time [s]

        beam = Beam(q=q, sigmaz=sigmaz, beta=beta,
                    xsource=xs, ysource=ys, ti=ti)

        # ----------- Solver & Simulation ----------
        # boundary conditions
        bc_low=['pec', 'pec', 'pec']
        bc_high=['pec', 'pec', 'pec']

        # Solver setup
        global solver
        solver = SolverFIT3D(grid,
                            bc_low=bc_low, 
                            bc_high=bc_high, 
                            use_stl=True, 
                            use_mpi=use_mpi, # Activate MPI
                            bg='pec' # Background material
                            )
        
        # -------------- Output folder ---------------------
        if use_mpi and solver.rank == 0:
            if not os.path.exists(self.img_folder): 
                os.mkdir(self.img_folder)
        elif not use_mpi:
            if not os.path.exists(self.img_folder): 
                os.mkdir(self.img_folder)

        # -------------- Custom time loop  -----------------
        if use_mpi:
            Nt = 3000
            for n in tqdm(range(Nt)):

                beam.update(solver, n*solver.dt)
                solver.mpi_one_step()

            Ez = solver.mpi_gather('Ez', x=int(Nx/2), y=int(Ny/2), z=np.s_[::5])
            if solver.rank == 0:
                #print(Ez)
                assert np.allclose(Ez, self.Ez, rtol=0.1), "Electric field Ez samples MPI failed"
        else:
            Nt = 3000
            for n in tqdm(range(Nt)):

                beam.update(solver, n*solver.dt)
                solver.one_step()
            
            Ez = solver.E[int(Nx/2), int(Ny/2), np.s_[::5], 'z']
            #print(Ez)
            assert np.allclose(Ez, self.Ez, rtol=0.1), "Electric field Ez samples failed"


    def test_mpi_gather_asField(self):
        # Plot inspect after mpi gather
        global solver
        if use_mpi:
            E = solver.mpi_gather_asField('E')
            if solver.rank == 0: #custom plots go in rank 0
                fig, ax = E.inspect(figsize=[20,6], plane='YZ', show=False, handles=True)
                fig.savefig(self.img_folder+'Einspect_'+str(3000).zfill(4)+'.png')
                plt.close(fig)
        else:
            fig, ax = solver.E.inspect(figsize=[20,6], plane='YZ', show=False, handles=True)
            fig.savefig(self.img_folder+'Einspect_'+str(3000).zfill(4)+'.png')
            plt.close(fig)

    def test_mpi_plot2D(self):
        # Plot E abs in 2D every 20 timesteps 
        global solver
        solver.plot2D(field='E', component='Abs', 
                    plane='YZ', pos=0.5, 
                    cmap='rainbow', vmin=0, vmax=500., interpolation='hanning',
                    off_screen=True, title=self.img_folder+'Ez2d', n=3000)

    def test_mpi_plot1D(self):
        # Plot E z in 1D at diferent transverse positions `pos` every 20 timesteps
        global solver
        solver.plot1D(field='E', component='z', 
                line='z', pos=[0.45, 0.5, 0.55], 
                xscale='linear', yscale='linear',
                off_screen=True, title=self.img_folder+'Ez1d', n=3000)
    
    @pytest.mark.skipif(not flag_plot_3D, reason="Requires interactive plotting")
    def test_mpi_plot3D(self):
        # Plot Abs Electric field on domain
        # disabled when mpi = True
        global solver
        solver.plot3D('E', component='Abs', 
                cmap='rainbow', clim=[0, 500],
                add_stl=['cavity', 'shell'], stl_opacity=0.1,
                clip_interactive=True, clip_normal='-y')
        
    @pytest.mark.skipif(not flag_plot_3D, reason="Requires interactive plotting")    
    def test_mpi_plot3DonSTL(self):
        # Plot Abs Electric field on STL solid `cavity`
        # disabled when mpi = True
        global solver
        solver.plot3DonSTL('E', component='Abs', 
                        cmap='rainbow', clim=[0, 500],
                        stl_with_field='cavity', field_opacity=1.0,
                        stl_transparent='shell', stl_opacity=0.1, stl_colors='white',
                        clip_plane=True, clip_normal='-y', clip_origin=[0,0,0], 
                        off_screen=False, zoom=1.2, title=self.img_folder+'Ez3d')
            
    
    def test_mpi_wakefield(self):
        # Reset fields
        global solver
        solver.reset_fields()

        # ------------ Beam source ----------------
        # Beam parameters
        sigmaz = 10e-2      #[m] -> 2 GHz
        q = 1e-9            #[C]
        beta = 1.0          # beam beta 
        xs = 0.             # x source position [m]
        ys = 0.             # y source position [m]
        xt = 0.             # x test position [m]
        yt = 0.             # y test position [m]
        # [DEFAULT] tinj = 8.53*sigmaz/c_light  # injection time offset [s] 

        # ----------- Wake Solver  setup  ----------
        # Wakefield post-processor
        wakelength = 10. # [m] -> Partially decayed
        skip_cells = 10  # no. cells to skip at zlo/zhi for wake integration
        results_folder = 'tests/007_results/'

        global wake
        wake = WakeSolver(q=q, sigmaz=sigmaz, beta=beta,
                        xsource=xs, ysource=ys, xtest=xt, ytest=yt,
                        skip_cells=skip_cells,
                        results_folder=results_folder,
                        Ez_file=results_folder+'Ez.h5',)

        # Run simulation
        solver.wakesolve(wakelength=wakelength, 
                         wake=wake)
    
    def test_long_wake_potential(self):
        global wake
        global solver
        if use_mpi:
            if solver.rank == 0:
                #print(wake.WP[::50])
                assert np.allclose(wake.WP[::50], self.WP, rtol=0.1), "Wake potential samples failed"
                assert np.cumsum(np.abs(wake.WP))[-1] == pytest.approx(184.43818552913254, 0.1), "Wake potential cumsum MPI failed"
        else:
            #print(wake.WP[::50])
            assert np.allclose(wake.WP[::50], self.WP, rtol=0.1), "Wake potential samples failed"
            assert np.cumsum(np.abs(wake.WP))[-1] == pytest.approx(184.43818552913254, 0.1), "Wake potential cumsum MPI failed"

    def test_long_impedance(self):
        global wake
        global solver
        if use_mpi:
            if solver.rank == 0:
                #print(wake.Z[::20])
                assert np.allclose(np.abs(wake.Z)[::20], np.abs(self.Z), rtol=0.1), "Abs Impedance samples MPI failed"
                assert np.allclose(np.real(wake.Z)[::20], np.real(self.Z), rtol=0.1), "Real Impedance samples MPI failed"
                assert np.allclose(np.imag(wake.Z)[::20], np.imag(self.Z), rtol=0.1), "Imag Impedance samples MPI failed"
                assert np.cumsum(np.abs(wake.Z))[-1] == pytest.approx(250910.51090497518, 0.1), "Abs Impedance cumsum MPI failed"
        else:
            #print(wake.Z[::20])
            assert np.allclose(np.abs(wake.Z)[::20], np.abs(self.Z), rtol=0.1), "Abs Impedance samples failed"
            assert np.allclose(np.real(wake.Z)[::20], np.real(self.Z), rtol=0.1), "Real Impedance samples failed"
            assert np.allclose(np.imag(wake.Z)[::20], np.imag(self.Z), rtol=0.1), "Imag Impedance samples failed"
            assert np.cumsum(np.abs(wake.Z))[-1] == pytest.approx(250910.51090497518, 0.1), "Abs Impedance cumsum failed"
    