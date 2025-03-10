from functools import cache
from pickle import UnpicklingError

@cache
def pickle_memoize(fname, creation_callback, verbose=False):
    """
    Try to read data from the pickle at `fname`; if it doesn't exist, save the
    output of `creation_callback` to `fname` as a pickle. Also memoizes in mem
    with functools.cache.
    """
    from pickle import load, dump
    if verbose: print(f"pickle_memoize: looking for pickle file '{fname}'...")
    try:
        with open(fname, 'rb') as rf:
            if verbose: print(f"    found pickle file '{fname}'! :)) loading it...")
            return load(rf)
    except (FileNotFoundError, UnpicklingError):
        if verbose: print(f"    did not find pickle file '{fname}' or it was corrupted :( making it...")
        got = creation_callback()
        try:
            with open(fname, 'wb') as wf:
                dump(got, wf)
            if verbose: print(f"    successfully made pickle file '{fname}'! :)")
        except TypeError as err:
            from sys import stderr
            if verbose: print("    couldn't pickle the object! :(", err, file=stderr)
        return got

def style_matplotlib(plt):
    plt.rcParams.update({
        'figure.dpi': 200,
        'savefig.dpi': 200,
        'font.family': 'serif',
        'axis.titlesize': 18,
        'axis.titleweight': 'bold',
        'font.size': 18,
        'font.weight': 'bold',
        'axes.labelweight': 'bold',
    })