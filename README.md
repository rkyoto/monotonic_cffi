# monotonic_cffi
Just a cffi version of existing monotonic module on PyPI. See:

    https://pypi.python.org/pypi/monotonic

Tested with PyPy 2.6.1 and 4.0.0 on Windows, OSX and some Linux distros.

Should have better performance with PyPy. Here are some test results:

PyPy 2.6.1 on CentOS 7 x86_64:
```
>>>> timeit.timeit('monotonic()', setup='from monotonic import monotonic', number=1000000)
11.138436794281006
>>>> timeit.timeit('monotonic()', setup='from monotonic_cffi import monotonic', number=1000000)
0.06484603881835938
```

PyPy 4.0.0 on CentOS 7 x86_64:
```
>>>> timeit.timeit('monotonic()', setup='from monotonic import monotonic', number=1000000)
12.084894895553589
>>>> timeit.timeit('monotonic()', setup='from monotonic_cffi import monotonic', number=1000000)
0.06938791275024414
```

Also slightly better performance with CPython (on Ubuntu 14.04 x86_64):
```
>>> timeit.timeit('monotonic()', setup='from monotonic import monotonic', number=1000000)
0.9230430126190186
>>> timeit.timeit('monotonic()', setup='from monotonic_cffi import monotonic', number=1000000)
0.46939706802368164
```
