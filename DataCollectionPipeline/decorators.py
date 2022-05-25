from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import functools # used to maintain introspection on decorators
import time # used to time functions

def exceptionHandling(func):
    @functools.wraps(func) # maintains introspection
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except NoSuchElementException:
            print(f"{func.__name__} Exception: Element Not Found")
        except TimeoutException:
            print(f"{func.__name__} Exception: Timeout")
        return func(*args, **kwargs)
    return wrapper

def folderAlreadyExists(folderName):
    def wrapperOuter(func):
        @functools.wraps(func) # maintains introspection
        def wrapperInner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except:
                print(f"{func.__name__} Error")
                print(folderName, "Folder Already Exists")
            return func
        return wrapperInner
    return wrapperOuter

def functionTimer(func):
    """Prints the functions runtime"""
    @functools.wraps(func) # maintains introspection
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        runtime = end - start
        print (f"Finished {func.__name__!r} in {runtime: .4f} secs")
        return func(*args, **kwargs)
    return wrapper

# Best applied to small convenience functions that you don’t call directly yourself
def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]                     # Creates a list of positional arguments, repr() returns a string for each argument               
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()] # Creates a list of keyword arguments, f-string formats each argument as key=value, !r specifier means that repr() is used to represent the value
        signature = ", ".join(args_repr + kwargs_repr)          # Join both lists together to make a signature
        print(f"Calling {func.__name__}({signature})")
        func(*args, **kwargs)
        print(f"{func.__name__!r} returned {func!r}")           
        return func
    return wrapper

# Best applied to functions you only need to call less often
def slowDown(func):
    '''Sleep before calling the function'''
    @functools.wraps(func) # maintains introspection
    def wrapper(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)
    return wrapper

# When there is no element it returns N/A
def scrapeHandling(element):
    def wrapperOuter(func):
        @functools.wraps(func) # maintains introspection
        def wrapperInner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except NoSuchElementException:
                print(f"{func.__name__} Exception:", element, "Not Found")
                element = "N/A"
            except TimeoutException:
                print(f"{func.__name__} Exception: Timeout")
                element = "N/A"
            return func
        return wrapperInner
    return wrapperOuter

# Counts the number of time the function has been called
def callCount(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        print(f"Call {wrapper.calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper
