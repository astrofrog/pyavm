def arg(x, y):
    import numpy as np
    return np.arctan2(y, x)


def get_cd(wcs):

    pc11, pc12, pc21, pc22 = wcs.wcs.get_pc().ravel()
    cdelt1, cdelt2 = wcs.wcs.get_cdelt()

    cd11 = cdelt1 * pc11
    cd12 = cdelt1 * pc12
    cd21 = cdelt2 * pc21
    cd22 = cdelt2 * pc22

    return cd11, cd12, cd21, cd22


def get_cdelt_crota(wcs):

    import numpy as np

    # This implements the algorithm from:
    #
    # Representations of celestial coordinates in FITS
    #          Calabretta & Greisen (2002)
    #
    # Section: 6.2. Supporting old interpreters

    cd11, cd12, cd21, cd22 = get_cd(wcs)

    if cd21 > 0:
        rho_a = arg(cd11, cd21)
    elif cd21 == 0:
        rho_a = 0
    else:
        rho_a = arg(-cd11, -cd21)

    if cd12 > 0:
        rho_b = arg(-cd22, cd12)
    elif cd12 == 0:
        rho_b = 0
    else:
        rho_b = arg(cd22, -cd12)

    rho_diff = abs(rho_a - rho_b)

    if rho_diff > np.pi:
        rho_diff -= 2 * np.pi

    if rho_diff > 1e-10:
        raise ValueError("WCS cannot be represented by CDELT/CROTA")

    rho = 0.5 * (rho_a + rho_b)

    if np.abs(np.cos(rho)) > 0.5:
        cdelt1 = cd11 / np.cos(rho)
        cdelt2 = cd22 / np.cos(rho)
    else:
        cdelt1 = cd21 / np.sin(rho)
        cdelt2 = -cd12 / np.sin(rho)

    crota2 = np.degrees(rho) % 360

    return cdelt1, cdelt2, crota2
