from uncertainties import ufloat
import numpy as np

def get_leading_figure(unc):
    sci = str(unc).split('e')
    if len(sci) > 1:
        dig = -int(sci[-1])
    else:
        sp = str(unc).split('.')
        if len(sp) > 1:
            if int(sp[0]) > 0:
                decimal = False
            else:
                decimal = True            
        else:
            decimal = True

        if decimal:
            te = unc
            dig = 0
            while te < 1:
                te *= 10
                dig += 1

        else:
            te = unc
            dig = 0
            while te > 10:
                te /= 10
                dig -= 1
    return dig

def print_unc(val, unc = []):
    if isinstance(unc, list):
        val, unc = val.n, val.s
    dig = get_leading_figure(unc)

    print("{:.{}f} +- {:.{}f}".format(val, dig, unc, dig))
    return np.round(val, dig), np.round(unc, dig), dig
