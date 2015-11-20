
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='monotonic_cffi',
    version='0.1',
    license='Apache',
    author='Matt Jones',
    author_email='mattjones1811@hotmail.com',
    url='https://github.com/rkyoto/monotonic_cffi',
    classifiers=(
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ),
    py_modules=['monotonic_cffi'],
)
