"""Spike-train metrics for HD-MEA recordings: CV, population rate, network bursts, STTC."""
import numpy as np # arrays and maths


def cv_isi(t):
    """Coefficient of variation of inter-spike intervals. t = sorted spike times in s."""
    isi = np.diff(t) # inter-spike intervals
    return np.std(isi) / np.mean(isi) # CV = SD / mean (Poisson = 1)


def population_rate(trains, duration, bin_s):
    """Sum all spike trains in bins. Returns rate (spikes/s) and bin edges (s)."""
    n_bins = int(duration / bin_s) # number of full bins
    edges = np.linspace(0, n_bins * bin_s, n_bins + 1) # bin edges (linspace avoids float rounding)
    counts, _ = np.histogram(np.concatenate(trains), edges) # spikes per bin, all units together
    return counts / bin_s, edges # counts -> spikes/s


def count_bursts(pop_rate, k=3):
    """Network bursts = upward crossings of mean + k*SD. Returns (n_bursts, threshold)."""
    thr = pop_rate.mean() + k * pop_rate.std() # burst threshold
    above = pop_rate > thr # bins above threshold
    n = int((above[1:] & ~above[:-1]).sum() + above[0]) # count burst starts only
    return n, thr


def tiling_fraction(t, dt, duration):
    """T_A: fraction of the recording within ±dt of any spike in t (sorted, s)."""
    if len(t) == 0: # no spikes -> nothing covered
        return 0.0
    covered = np.minimum(np.diff(t), 2 * dt).sum() + 2 * dt # tiles of 2*dt around each spike, overlaps counted once
    covered -= max(0.0, dt - t[0]) # remove the part of the first tile before time 0
    covered -= max(0.0, t[-1] + dt - duration) # remove the part of the last tile after the end
    return covered / duration # fraction of time


def frac_close(a, b, dt):
    """P_A: fraction of spikes in a that have a spike of b within ±dt (both sorted, s)."""
    if len(a) == 0 or len(b) == 0: # nothing to compare
        return 0.0
    idx = np.searchsorted(b, a) # position each spike of a would take inside b
    left = np.abs(a - b[np.clip(idx - 1, 0, len(b) - 1)]) # distance to the nearest earlier b spike
    right = np.abs(b[np.clip(idx, 0, len(b) - 1)] - a) # distance to the nearest later b spike
    return np.mean(np.minimum(left, right) <= dt) # share of a's spikes with a b spike close by


def sttc(a, b, dt, duration):
    """Spike time tiling coefficient (Cutts & Eglen 2014). a, b = sorted spike times in s."""
    ta, tb = tiling_fraction(a, dt, duration), tiling_fraction(b, dt, duration) # time covered by each train
    pa, pb = frac_close(a, b, dt), frac_close(b, a, dt) # spikes of each train close to the other
    return 0.5 * ((pa - tb) / (1 - pa * tb) + (pb - ta) / (1 - pb * ta)) # STTC, range -1..1