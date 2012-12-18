# Memoized fibonacci

def mem_fib(n):
    fibs = [0,1,1]
    if n < 2:
        return fibs[n]
    for i in xrange(3,n):
        fibs.append(fibs[i-1] + fibs[i-2])
    return fibs[n-1] + fibs[n-2]

if __name__ == '__main__':
    print mem_fib(100)
