from distutils.core import Extension, setup
from Cython.Build import cythonize

# define an extension that will be cythonized and compiled
ext = Extension(name="dpsFunction", sources=["dpsFunction.pyx"])
setup(ext_modules=cythonize(ext))
