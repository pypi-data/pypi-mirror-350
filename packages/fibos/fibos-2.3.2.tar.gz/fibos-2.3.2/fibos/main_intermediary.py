import ctypes as ct
import numpy as np
import os
from .utils import _load_library

main75 = _load_library("main75")
ds75 = _load_library("ds75")
surfcal76 = _load_library("surfcal76")

def call_main(iresf, iresl, maxres, maxat, meth, density):
    resnum = (ct.c_int*maxres)()
    x = (ct.c_double*maxat)()
    y = (ct.c_double*maxat)()
    z = (ct.c_double*maxat)()
    natm = (ct.c_int * 1)()
    natm[0] = 0
    ires_f = (ct.c_int * 1)()
    main75.main_(resnum,natm,x,y,z,iresf,iresl)
    meth_f = (ct.c_int * 1)()
    meth_f[0] = meth
    density_f = ct.c_double(density)


    for ires in range(1, iresl+1):
        ires_f[0] = ires
        main75.main_intermediate_(x,y,z,ires_f,resnum,natm)
        main75.main_intermediate01_(x,y,z,ires_f,resnum,natm)
        ds75.runsims_(meth_f, ct.byref(density_f))
        surfcal76.surfcal_()
    os.rename("file.srf","prot.srf")
