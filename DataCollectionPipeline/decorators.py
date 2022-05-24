from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import functools # used to maintain introspection on decorators

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

def folderAlreadyExists(func):
    @functools.wraps(func) # maintains introspection
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print(f"{func.__name__} Folder Already Exists")
        return func(*args, **kwargs)
    return wrapper



    error downloading images
    scraper exceptions