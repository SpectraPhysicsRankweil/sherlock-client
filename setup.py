from distutils.core import setup


setup(name='IPSherlockClient',
      version='1.0',
      py_modules=['client'],
      install_requires=['requests', 'netifaces']
      )