from distutils.core import setup, Extension

module1 = Extension('pykakasi',
          sources = ['pykakasi.c'],
          include_dirs=['python2.3'],
          libraries = ['kakasi']
          )

setup(name = 'pykakasi',
      version = '1.0',
      ext_modules = [module1]
     )

      
