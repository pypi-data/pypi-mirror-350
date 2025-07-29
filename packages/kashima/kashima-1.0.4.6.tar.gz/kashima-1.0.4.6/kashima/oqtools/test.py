#!/usr/bin/env python

import numpy as np
import traceback
import openquake.hazardlib
from openquake.hazardlib import const
from openquake.hazardlib.gsim import get_available_gsims, get_gsim_by_name
from openquake.hazardlib.gsim.base import RuptureContext, DistancesContext, SitesContext
from openquake.hazardlib.imt import PGA, SA


def get_supported_periods(gmpe, period_array=None):
    """
    Returns a sub-list of periods from period_array that
    do not raise ValueErrors when computing SA(T).
    """
    # Dummy contexts
    rctx = RuptureContext()
    rctx.mag = 7.0
    rctx.rake = 0.0
    rctx.hypo_depth = 10.0

    dctx = DistancesContext()
    dctx.rjb = np.array([20.0])
    dctx.rrup = np.array([20.0])
    dctx.rx = np.array([0.0])

    sctx = SitesContext()
    sctx.vs30 = np.array([600.0])
    sctx.vs30measured = np.array([False])
    sctx.z1pt0 = np.array([999.])
    sctx.z2pt5 = np.array([999.])

    if period_array is None:
        # Default sampling from 0.01 s to 10 s
        period_array = np.logspace(-2, 1, 40)

    supported = []
    for T in period_array:
        try:
            gmpe.get_mean_and_stddevs(
                sctx, rctx, dctx, SA(T), [const.StdDev.TOTAL]
            )
            supported.append(T)
        except ValueError:
            pass
    return supported


def example_all_gmpes():
    """
    Iterates over all GMPE names found in the OpenQuake hazardlib,
    prints out the ones that support at least some range
    of spectral periods, and demonstrates a single scenario
    call for PGA if possible.
    """
    all_names = sorted(get_available_gsims())
    print(f"Found {len(all_names)} GMPEs in hazardlib.")
    for gname in all_names:
        GMPEClass = get_gsim_by_name(gname)
        gmpe = GMPEClass()

        print(f"\n--- GMPE: {gname} ---")
        try:
            # Check supported periods
            sp = get_supported_periods(gmpe)
            if len(sp) == 0:
                print("  No SA periods supported in [0.01, 10] s (or requires more complex context).")
            else:
                print(f"  Supports {len(sp)} spectral periods in [0.01, 10.0] s.")
                # e.g. print them
                # print("  Periods:", sp)

            # Try a quick scenario for PGA:
            # (We won't do a full context here, just the same dummy used above)
            rctx = RuptureContext()
            rctx.mag = 7.0
            rctx.rake = 0.0
            rctx.hypo_depth = 10.0

            dctx = DistancesContext()
            dctx.rjb = np.array([20.0])
            dctx.rrup = np.array([20.0])
            dctx.rx = np.array([0.0])

            sctx = SitesContext()
            sctx.vs30 = np.array([600.0])
            sctx.vs30measured = np.array([False])
            sctx.z1pt0 = np.array([999.])
            sctx.z2pt5 = np.array([999.])

            mean_pga, stddev_pga = gmpe.get_mean_and_stddevs(
                sctx, rctx, dctx, PGA(), [const.StdDev.TOTAL]
            )
            print(f"  Example scenario PGA ln(g) => {mean_pga} ; std => {stddev_pga}")
        except Exception as e:
            print("  Could not compute scenario: ", e)
            # For debugging:
            # traceback.print_exc()


if __name__ == "__main__":
    example_all_gmpes()
