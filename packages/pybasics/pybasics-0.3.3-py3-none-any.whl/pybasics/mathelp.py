#
#
import numpy as np


def sumd(a, da, b, db):
    """.
    """
    ab = a + b

    dab = np.sqrt(da**2 + db**2)

    return ab, dab


def multid(a, da, b, db):
    """.
    """
    ab = a * b

    dab = np.sqrt((da/a)**2 + (db/b)**2) * ab

    return ab, dab
