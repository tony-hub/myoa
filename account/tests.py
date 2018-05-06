def log(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args,**kwargs):
        print('%s called'%fn.__name__)
        return fn(*args,**kwargs)
    return wrapper

@log
def fn(n):
    result = map(lambda n:n*n, range(1,n))
    print(result)

fn(12)