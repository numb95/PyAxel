from distutils.core import setup

setup(
    name='PyAxel',
    version='0.1',
    packages=['PyAxel'],
    install_requires=['click'],
    entry_points='''
    [console_scripts]
    PyAxel=PyAxel.PyAxel:generate
    ''',
    url='http://mehdy.github.io/PyAxel',
    license='GPLv2',
    author='mehdy',
    author_email='mehdy.khoshnoody@gmail.com',
    description='An Improvement of axel download accelerator'
)
