"""
modifier:
Yudha Styawan

email:
yudhastyawan@gmail.com

modified from: 
https://krischer.github.io/seismo_live_build/html/Computational%20Seismology/The%20Finite-Difference%20Method/fd_ac1d_solution_wrapper.html

usage:
as a generator output of 1D wave simulation to blender - homogeneous media

"""

import numpy as np

def getwave():
    nx   = 500          # number of grid points in x-direction
    dx   = 0.5          # grid point distance in x-direction
    c0   = 333.         # wave speed in medium (m/s)
    isrc = 10           # source location in grid in x-direction
    # ir   = 730        # receiver location in grid in x-direction
    nt   = 501          # maximum number of time steps
    dt   = 0.0010       # time step
    fps = int(1/dt)

    # eps  = c0 * dt / dx # epsilon value
    f0   = 25. # dominant frequency of the source (Hz)
    t0   = 4. / f0 # source time shift
    src  = np.zeros(nt + 1)
    time = np.linspace(0 * dt, nt * dt, nt)
    # 1st derivative of a Gaussian
    src  = -2. * (time - t0) * (f0 ** 2) * (np.exp(-1.0 * (f0 ** 2) * (time - t0) ** 2))

    p    = np.zeros(nx) # p at time n (now)
    pold = np.zeros(nx) # p at time n-1 (past)
    pnew = np.zeros(nx) # p at time n+1 (present)
    d2px = np.zeros(nx) # 2nd space derivative of p
    amps = np.zeros((nt,nx))

    c    = np.zeros(nx)
    c    = c + c0       # initialize wave velocity in model

    x    = np.arange(nx)
    x    = x * dx       # coordinate in x-direction

    op   = 5
    print(op, '- point operator')

    # Calculate Partial Derivatives
    # -----------------------------
    for it in range(nt):
        if op==3: # use 3 point operator FD scheme
            for i in range(1, nx - 1):
                d2px[i] = (p[i + 1] - 2 * p[i] + p[i - 1]) / dx ** 2

        if op==5: # use 5 point operator FD scheme
            for i in range(2, nx - 2):
                d2px[i] = (-1./12 * p[i + 2] + 4./3  * p[i + 1] - 5./2 * p[i] \
                        +4./3  * p[i - 1] - 1./12 * p[i - 2]) / dx ** 2

        # Time Extrapolation
        # ------------------
        pnew = 2 * p - pold + c ** 2 * dt ** 2 * d2px

        # Add Source Term at isrc
        # -----------------------
        # Absolute pressure w.r.t analytical solution
        pnew[isrc] = pnew[isrc] + src[it] / (dx) * dt ** 2
        
                
        # Remap Time Levels
        # -----------------
        pold, p = p, pnew

        # save it
        amps[it,:] = p

    return x, dx, amps, fps # x-axis numbers, delta x, amplitude (M x N): M as time iteration, N as amplitude along x, frames per sec (unused)


# blender python does not have matplotlib
# if __name__ == '__main__':
#     import matplotlib.pyplot as plt
#     x, dx, amps, fps = getwave()
#     amps = amps / np.max(np.abs(amps))
#     amps = amps * 10
#     for i in range(len(amps[:,0])):
#         if i == 300:
#             plt.plot(range(len(x)), amps[i, :])
#     plt.gca().axis('equal')
#     plt.show()