from pathos.multiprocessing import ProcessingPool as Pool
from RcToolBox.basic_op import hprint
from typing import Callable, Iterable, Any, List

""" 
Here we use pathos.multiprocessing. Unlike python's multiprocessing module, 
pathos.multiprocessing can directly utilize functions that require multiple arguments
"""

def hardcore_process(
    func: Callable,
    *iterables: Iterable,
    num_workers: int = 4
) -> List[Any]:
    """Apply a function to multiple iterable inputs in parallel using multiple processes."""

    res = None
    hprint("Using {} threads!".format(num_workers))
    
    # *with ... as ... is a context manager, which will automatically close the pool
    with Pool(num_workers) as p:
        res = p.map(func, *iterables)

    if res is None:
        raise ValueError("Returne is None, Check function and inputs.")
    
    return res

def add(a, b):
    return a + b

if __name__ == '__main__':
    
    x = [1, 2, 3, 4, 5]
    y= [2, 2, 3, 4, 5]
    res = hardcore_process(add, x, y, num_workers=4)
    print(res)