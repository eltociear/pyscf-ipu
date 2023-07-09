# Copyright (c) 2023 Graphcore Ltd. All rights reserved.
import jax
import jax.numpy as jnp
import numpy as np
import pyscf
from jsonargparse import CLI, Namespace
import sys
sys.path.append("../")
from exchange_correlation.b3lyp import b3lyp
from electron_repulsion.direct import prepare_electron_repulsion_integrals, electron_repulsion_integrals, ipu_einsum, prepare_einsum_inputs

HARTREE_TO_EV = 27.2114079527
EPSILON_B3LYP = 1e-20
B3LYP_HYB = 0.2

def energy(density_matrix, H_core, J, K, E_xc, E_nuc, _np=jax.numpy):
    """Density Functional Theory (DFT) solves the optimisation problem:

        min_{density_matrix} energy(density_matrix, ...)

    We like to think of `energy(...)` as a loss function. `density_matrix`
    represents the density of electrons as: 

        rho(r) = sum_{ij}^N density_matrix_{ij} X_i(r) X_j(r)  where X_i(r)~exp(-r^2).

    Here N is the number of atomic orbitals **and** molecular orbitals (N=66 for C6H6). 
    All input matrices (density_matrix, H_core, J, K) are (N, N). The X_i(r) are called
    Gaussian Type Orbitals (GTO). The inputs (J, K, E_xc) depend on density_matrix. 
    """
    E_core = _np.sum(density_matrix * H_core) # float = -712.04[Ha] for C6H6
    E_J    = _np.sum(density_matrix * J)      # float =  624.38[Ha] for C6H6
    E_K    = _np.sum(density_matrix * K)      # float =   26.53[Ha] for C6H6

    E      = E_core + E_J/2 - E_K/4 + E_xc + E_nuc  # float = -232.04[Ha] for C6H6

    return _np.array([E, E_core, E_J/2, -E_K/4, E_xc, E_nuc])


def nanoDFT_iteration(i, vals): 
    """Each DFT iteration updates density_matrix attempting to minimize energy(density_matrix, ... ). """ 
    density_matrix, V_xc, J, K, O, H_core, L_inv      = vals[:7]                              # All (N, N) matrices
    E_nuc, occupancy, diis_history, ERI, GW, GAO, log = vals[7:]                              # Varying types/shapes. 

    # Step 1: Update Hamiltonian (optionally use DIIS to improve DFT convergence). 
    H = H_core + V_xc                                                                         # (N, N) 
    if args.diis: H, diis_history = DIIS(i, H, density_matrix, O, diis_history) 

    # Step 2: Solve eigh (L_inv turns generalized eigh into eigh).
    eigvects = L_inv.T @ linalg_eigh(L_inv @ H @ L_inv.T)[1]                                  # (N, N) 

    # Step 3: Use result from eigenproblem to update density_matrix. 
    density_matrix   = (eigvects*occupancy*2) @ eigvects.T                                    # (N, N)
    E_xc, V_xc, J, K = electron_interactions(density_matrix, GAO, ERI, GW, J, K)              # float, (N, N), (N, N), (N, N)

    # Log SCF matrices and energies (not used by DFT algorithm). 
    log["matrices"] = log["matrices"].at[i].set(jnp.stack((density_matrix, J, K, H)))          # (iterations, 4, N, N)
    log["energy"] = log["energy"].at[i].set(energy(density_matrix, H_core, J, K, E_xc, E_nuc)) # (iterations, 6)

    return [density_matrix, V_xc, J, K, O, H_core, L_inv, E_nuc, occupancy, diis_history, ERI, GW, GAO, log]


def electron_interactions(density_matrix, GAO, ERI, GW, J, K):
    """Computes electronic interactions: E_XC (float) and J, K, V_xc (N, N). """
    rho = jnp.sum(GAO[:1] @ density_matrix * GAO, axis=2)     # (4, grid_size)=(4, 45624) for C6H6
    E_xc, vrho, vgamma = b3lyp(rho, EPSILON_B3LYP)            # (gridsize,) (gridsize,) (gridsize,)          
    E_xc = jnp.sum(rho[0] * GW * E_xc)                        # float=-27.968[Ha] for C6H6 at convergence

    rho = jnp.concatenate([vrho.reshape(1, -1)*.5, 2*vgamma*rho[1:4]*2], axis=0) * GW  # (4, grid_size)=(4, 45624)
    V_xc = GAO[0].T @ jnp.sum(GAO * jnp.expand_dims(rho, axis=2), axis=0)              # (N, N)
    V_xc = V_xc + V_xc.T                                                               # (N, N)

    if args.backend != "ipu":  # ERI is (N, N, N, N) tensor. 
        J = jnp.einsum('ijkl,ji->kl', ERI, density_matrix) # (N, N) 
        K = jnp.einsum('ijkl,jk->il', ERI, density_matrix) # (N, N)
    else: # Custom C++ einsum for IPUs utilizing ERI[ijkl]=ERI[ijlk]=ERI[jikl]=ERI[jilk]=ERI[lkij]=ERI[lkji]=ERI[lkij]=ERI[lkji]
        _tuple_indices, _tuple_do_lists, _N, num_calls = prepare_einsum_inputs(mol)
        J, K = ipu_einsum(ERI, density_matrix, _tuple_indices, _tuple_do_lists, _N, num_calls, tuple(args.indxs.tolist()), tuple(args.indxs.tolist()), int(args.threads), v=int(args.multv))

    K    = K * B3LYP_HYB    # (N, N)
    V_xc = V_xc + J - K/2   # (N, N) 

    return E_xc, V_xc, J, K # (float) (N, N) (N, N) (N, N)


def make_jitted_nanoDFT(backend):
    return jax.jit(_nanoDFT, static_argnames=("DIIS_space", "N"), backend=backend)
def _nanoDFT(nuclear_energy, density_matrix, kinetic, nuclear, overlap, ao, electron_repulsion, weights, 
              DIIS_space, N, mask, _input_floats, _input_ints, L_inv):
    DIIS_H       = np.zeros((DIIS_space+1, DIIS_space+1))
    DIIS_H[0,1:] = DIIS_H[1:,0] = 1
    DIIS_H       = np.array(DIIS_H)
    _V = np.zeros((DIIS_space, N**2))
    _H = np.zeros((DIIS_space, N**2))
    H_core = kinetic + nuclear
    J, K, V_xc = [np.zeros(H_core.shape) for _ in range(3)]

    if args.backend == "ipu":
        _, _, _tuple_ijkl, _shapes, _sizes, _counts, indxs, indxs_inv, _ = prepare_electron_repulsion_integrals(mol)
        args.indxs = indxs # TODO(): clean up eri/einsum code and see whether we can remove this.
        electron_repulsion = electron_repulsion_integrals( _input_floats, _input_ints, _tuple_ijkl, _shapes, _sizes, _counts, tuple(indxs_inv), num_threads=args.threads_int, v=args.intv)[0]

    _, V_xc, J, K = electron_interactions( density_matrix, ao, electron_repulsion, weights, J, K)

    diis_history = (_V, _H, DIIS_H)
    log = {"matrices": np.zeros((args.its, 4, N, N)), 
               "E_xc": np.zeros((args.its)),
               "energy": np.zeros((args.its, 6)),
               }
    vals = jax.lax.fori_loop(0, args.its, nanoDFT_iteration, 
                             [density_matrix, V_xc, J, K, overlap, H_core, L_inv, 
                                nuclear_energy, mask, diis_history, electron_repulsion,  weights, ao, log])
    log = vals[-1]
    logged_matrices = log["matrices"]
    logged_energies = log["energy"]

    return logged_matrices, H_core, logged_energies


def init_dft_tensors_cpu(args, DIIS_space=9):
    mol = pyscf.gto.mole.Mole()
    mol.build(atom=args.mol_str, unit="Angstrom", basis=args.basis, verbose=0)
    n_electrons_half = mol.nelectron//2  # 21 for C6H6 
    N                = mol.nao_nr()      # N = 66 for C6H6 
    nuclear_energy   = mol.energy_nuc()  # float = 202.4065 [Hartree] for C6H6 
    hyb              = pyscf.dft.libxc.hybrid_coeff(args.xc, mol.spin) # float = 0.2 for b3lyp/spin=0
    assert B3LYP_HYB == hyb 
    assert args.xc == "b3lyp"
    grids            = pyscf.dft.gen_grid.Grids(mol)
    grids.level      = args.level
    grids.build()
    weights         = grids.weights  # (grid_size,) = (45624,) for C6H6 
    coord_str       = 'GTOval_cart_deriv1' if mol.cart else 'GTOval_sph_deriv1'
    ao              = mol.eval_gto(coord_str, grids.coords, 4) # (4, grid_size, N) = (4, 45624, 9) for C6H6 
    density_matrix  = pyscf.scf.hf.init_guess_by_minao(mol)    # (N,N)=(66,66) for C6H6
    kinetic         = mol.intor_symmetric('int1e_kin')         # (N,N)
    nuclear         = mol.intor_symmetric('int1e_nuc')         # (N,N)
    overlap         = mol.intor_symmetric('int1e_ovlp')        # (N,N) 
    if args.backend != "ipu": 
        electron_repulsion = mol.intor("int2e_sph") # (N,N,N,N)=(66,66,66,66) for C6H6
    else: 
        electron_repulsion = None # will be computed on device
    L_inv               = np.linalg.inv(np.linalg.cholesky(overlap)) # (N, N)=(66,66) for C6H6
    input_floats, input_ints = prepare_electron_repulsion_integrals(mol)[:2]
    mask = np.concatenate([np.ones(n_electrons_half), np.zeros(N-n_electrons_half)])

    tensors = (nuclear_energy, density_matrix, kinetic, nuclear, overlap, ao, electron_repulsion, 
               weights, DIIS_space, N, mask, input_floats, input_ints, L_inv)

    return tensors, n_electrons_half, nuclear_energy, N, L_inv 


def nanoDFT(args):
    # Init DFT tensors from CPU using PySCF. 
    tensors, n_electrons_half, nuclear_energy, N, L_inv = init_dft_tensors_cpu(args)

    # Run SCF iterations on hardware accelerator. 
    vals = jitted_nanoDFT(*tensors) 
    logged_matrices, H_core, logged_energies = [np.asarray(a).astype(np.float64) for a in vals]
    logged_E_xc = logged_energies[:, 4].copy()

    # (Optional) Recompute results in float64. 
    density_matrices, Js, Ks, hamiltonians = [logged_matrices[:, i] for i in range(4)]
    energies, hlgaps = np.zeros((args.its, 6)), np.zeros(args.its)
    for i in range(args.its):
        energies[i] = energy(density_matrices[i], H_core, Js[i], Ks[i], logged_E_xc[i], nuclear_energy, np)
        hlgaps[i]   = hlgap(L_inv, hamiltonians[i], n_electrons_half, np)
    energies, hlgaps   = [a * HARTREE_TO_EV for a in [energies, hlgaps]] 
    return energies, logged_energies*HARTREE_TO_EV, hlgaps


def DIIS(i, hamiltonian, density_matrix, electron_overlap, diis_history):
    # DIIS improves DFT convergence by computing:
    #   hamiltonian_i = c_1 hamiltonian_{i-1} + ... + c_8 hamiltonian_{i-8}  where  c=pinv(some_matrix)[0,:]
    # We thus like to think of DIIS as "fancy momentum". 
    _V, _H, DIIS_H = diis_history
    DIIS_head = i % _V.shape[0]
    nd, d     = _V.shape
    sdf         = electron_overlap @ density_matrix @ hamiltonian            # (N, N)

    # Store current (hamiltonian,errvec) as flattened as row inside _V and _H.
    errvec = (sdf - sdf.T)
    _V = jax.lax.dynamic_update_slice(_V, errvec.reshape(1, d),      (DIIS_head, 0))   # TODO(): comsider naming 
    _H = jax.lax.dynamic_update_slice(_H, hamiltonian.reshape(1, d), (DIIS_head, 0))

    tmps = (_V.reshape(nd, 1, d) @ errvec.reshape(1, d, 1))
    tmps = tmps.reshape(-1)

    # Shapes in initial code depended on min(i, _V.shape[0]).
    # To allow jax.jit, we always use nd=_V.shape[0] and zero out
    # the additional stuff with the following mask.
    mask = jnp.where(np.arange(_V.shape[0]) < jnp.minimum(i+1, _V.shape[0]),
                        jnp.ones(_V.shape[0], dtype=_V.dtype), jnp.zeros(_V.shape[0], dtype=_V.dtype))
    tmps = tmps * mask

    # Assign tmp into row/col 'DIIS_head+1' of DIIS_H
    DIIS_H = jax.lax.dynamic_update_slice( DIIS_H, tmps.reshape(1, -1), (DIIS_head+1, 1) ) # TODO(): consider naming
    DIIS_H = jax.lax.dynamic_update_slice( DIIS_H, tmps.reshape(-1, 1), (1, DIIS_head+1) )

    # Compute new hamiltonian as linear combination of previous 8.
    # Coefficients are computed as pseudo_inverse of DIIS_H.
    # The first 8 iterations we are constructing DIIS_H so it has shape (2,2), (3,3), (4,4), ...
    # To allow jax.jit we pad to (9, 9) and just zero out the additional stuff...
    mask_            = jnp.concatenate([jnp.ones(1, dtype=mask.dtype), mask])
    masked_DIIS_H = DIIS_H[:nd+1, :nd+1] * mask_.reshape(-1, 1) * mask_.reshape(1, -1)

    if args.backend == "ipu":  c = pinv0( masked_DIIS_H )
    else:                      c = jnp.linalg.pinv(masked_DIIS_H)[0, :]

    scaled_H         = _H[:nd] * c[1:].reshape(nd, 1)
    hamiltonian      = jnp.sum( scaled_H, axis=0 ).reshape(hamiltonian.shape)

    return hamiltonian,( _V, _H, DIIS_H) 


def hlgap(L_inv, hamiltonian, n_electrons_half, _np):
    d = hamiltonian.shape[0]
    mo_energy   = _np.linalg.eigh(L_inv @ hamiltonian.reshape(d, d) @ L_inv.T)[0]
    return _np.abs( mo_energy[n_electrons_half] - mo_energy[n_electrons_half-1] )


def linalg_eigh(x):
    if args.backend == "ipu":
        from jax_ipu_experimental_addons.tile import ipu_eigh
        n = x.shape[0]
        pad = n % 2
        if pad:
            x = jnp.pad(x, [(0, 1), (0, 1)], mode='constant')

        eigvects, eigvals = ipu_eigh(x, sort_eigenvalues=True, num_iters=12)

        if pad:
            e1 = eigvects[-1:]
            col = jnp.argmax(e1)
            eigvects = jnp.roll(eigvects, -col-1)
            eigvects = eigvects[:, :-1]
            eigvects = jnp.roll(eigvects, -(-col))
            eigvects = eigvects[:-1]
    else:
        eigvals, eigvects = jnp.linalg.eigh(x)

    return eigvals, eigvects


def pinv0(a):  # take out first row
    cond =  9*1.1920929e-07
    vals, vect = linalg_eigh ( a )
    c = vect @ ( jnp.where( jnp.abs(vals) > cond, 1/vals, 0) * vect[0, :])
    return c


def pyscf_reference(args):
    mol = pyscf.gto.mole.Mole()
    mol.verbose = 0
    pyscf.__config__.dft_rks_RKS_grids_level = args.level
    mol.build(atom=args.mol_str, unit='Angstrom', basis=args.basis, spin=0)

    mol.max_cycle = args.its
    mf = pyscf.scf.RKS(mol)
    mf.max_cycle = args.its
    mf.xc = args.xc
    mf.diis_space = 9 
    if not args.diis:  # 
        mf.diis_space = 0 
        mf.diis = False 
    pyscf_energies = []
    pyscf_hlgaps = [] 
    lumo         = mol.nelectron//2 
    homo         = lumo - 1
    def callback(envs): # (TODO) compute different energy terms (XC, kin, ...) and compare to nanoDFT. 
        pyscf_energies.append(envs["e_tot"]*HARTREE_TO_EV)
        hl_gap_hartree = np.abs(envs["mo_energy"][homo] - envs["mo_energy"][lumo]) * HARTREE_TO_EV
        pyscf_hlgaps.append(hl_gap_hartree)
    mf.callback = callback
    mf.kernel()  
    return np.array(pyscf_energies), np.array(pyscf_hlgaps)


def print_difference(energies, logged_energies, hlgaps, pyscf_energies, pyscf_hlgaps):
    #TODO(HH): rename to match caller variable names
    print("pyscf_hlgap\t%15f"%( pyscf_hlgaps[-1]))
    print("us_hlgap\t%15f"%(    hlgaps[-1]))
    print("err_hlgap\t%15f"%np.abs(pyscf_hlgaps[-1]  - hlgaps[-1]))
    print("pyscf:\t\t%15f"%pyscf_energies[-1])
    print("us:\t\t%15f"%energies[-1, 0])
    print("mus:\t\t%15f"%np.mean(energies[-10:, 0]))
    print("diff:\t\t%15f"%np.abs(pyscf_energies[-1]-energies[-1, 0]))
    print("mdiff:\t\t%15f"%np.abs(pyscf_energies[-1]-np.mean(energies[-10:, 0])), np.std(energies[-10:, 0]))
    print("chemAcc: \t%15f"%0.043)
    print("chemAcc/diff: \t%15f"%(0.043/np.abs(pyscf_energies[-1]-energies[-1, 0])))
    print("chemAcc/mdiff: \t%15f"%(0.043/np.abs(pyscf_energies[-1]-np.mean(energies[-10:, 0]))))
    print("")
    pyscf_energies = np.concatenate([pyscf_energies, np.ones(energies.shape[0]-pyscf_energies.shape[0])*pyscf_energies[-1]])  
    pyscf_hlgaps = np.concatenate([pyscf_hlgaps, np.ones(hlgaps.shape[0]-pyscf_hlgaps.shape[0])*pyscf_hlgaps[-1]])  
    print("%18s"%"", "\t".join(["%10s"%str("iter %i "%i) for i in np.arange(1, energies.shape[0]+1)[1::3]]))
    print("%18s"%"Error Energy [eV]", "\t".join(["%10s"%str("%.2e"%f) for f in (pyscf_energies[1::3] - energies[1::3, 0]).reshape(-1)]))
    print("%18s"%"Error HLGAP [eV]", "\t".join(["%10s"%str("%.2e"%f) for f in (pyscf_hlgaps[1::3]   - hlgaps[1::3]).reshape(-1)]))
 
    # E_core, E_J/2, -E_K/4, E_xc, E_nuc
    print()
    print("%18s"%"E_core [eV]", "\t".join(["%10s"%str("%.5f"%f) for f in (energies[1::3, 1]).reshape(-1)]))
    print("%18s"%"E_J [eV]", "\t".join(["%10s"%str("%.5f"%f) for f in (energies[1::3, 2]).reshape(-1)]))
    print("%18s"%"E_K [eV]", "\t".join(["%10s"%str("%.5f"%f) for f in (energies[1::3, 3]).reshape(-1)]))
    print("%18s"%"E_xc [eV]", "\t".join(["%10s"%str("%.5f"%f) for f in (energies[1::3, 4]).reshape(-1)]))
    print("%18s"%"E_nuc [eV]", "\t".join(["%10s"%str("%.5f"%f) for f in (energies[1::3, 5]).reshape(-1)]))

    
def nanoDFT_parser(
        its: int = 20,
        mol_str: str = "benzene",
        float32: bool = False,
        basis: str = "6-31G",
        xc: str = "b3lyp",
        backend: str = "cpu",
        level: int = 1,
        multv: int = 2,
        intv: int = 1,
        threads: int = 1,
        threads_int: int = 1,
        diis: bool = True, 
):
    """
    nanoDFT

    Args:
        its (int): Number of Kohn-Sham iterations.
        mol_str (str): Molecule string, e.g., "H 0 0 0; H 0 0 1; O 1 0 0; "
        float32 (bool) : Whether to use float32 (default is float64).
        basis (str): Which Gaussian basis set to use.
        xc (str): Exchange-correlation functional. Only support B3LYP
        backend (str): Accelerator backend to use: "-backend cpu" or "-backend ipu".
        level (int): Level of grids for XC numerical integration.
        gdb (int): Which version of GDP to load {10, 11, 13, 17}.
        multv (int): Which version of our einsum algorithm to use;comptues ERI@flat(v). Different versions trades-off for memory vs sequentiality
        intv (int): Which version to use of our integral algorithm.
        threads (int): For -backend ipu. Number of threads for einsum(ERI, dm) with custom C++ (trades-off speed vs memory).
        threads_int (int): For -backend ipu. Number of threads for computing ERI with custom C++ (trades off speed vs memory).
    """
    if mol_str == "benzene":  
        mol_str = "C        0.0000    0.0000    0.0000; C        1.4000    0.0000    0.0000; C        2.1000    1.2124    0.0000; C        1.4000    2.4249    0.0000; C        0.0000    2.4249    0.0000; C       -0.7000    1.2124    0.0000; H       -0.5500   -0.9526    0.0000; H       -0.5500    3.3775    0.0000; H        1.9500   -0.9526    0.0000; H       -1.8000    1.2124    0.0000; H        3.2000    1.2124    0.0000; H        1.9500    3.3775    0.0000;"
    elif mol_str == "methane":
        mol_str = "C 0 0 0; H 0 0 1; H 0 1 0; H 1 0 0; H 1 1 1;"
    args = locals()
    args = Namespace(**args)
    jax.config.update('jax_enable_x64', not float32)
    return args


if __name__ == "__main__":
    # Limit PySCF threads to mitigate problem with NUMA nodes. 
    import os
    os.environ['OMP_NUM_THREADS'] = "8"

    args = CLI(nanoDFT_parser)

    jitted_nanoDFT = make_jitted_nanoDFT(args.backend) # used later inside nanoDFT 

    # Test Case: Compare nanoDFT against PySCF.
    mol = pyscf.gto.mole.Mole()
    mol.build(atom=args.mol_str, unit="Angstrom", basis=args.basis, spin=0, verbose=0)

    nanoDFT_E, nanoDFT_logged_E, nanoDFT_hlgap = nanoDFT(args)
    pyscf_E, pyscf_hlgap = pyscf_reference(args)
    print_difference(nanoDFT_E, nanoDFT_logged_E, nanoDFT_hlgap, pyscf_E, pyscf_hlgap)
