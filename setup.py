from setuptools import setup, find_packages

setup(
    name='headache',
    description='Wrap external libraries without the associated headache',
    version='0.1',
    author='Kosio Karchev',
    author_email='kosiokarchev@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'astor',
        'frozendict', 'frozenlist',
        'lxml',
        'more_itertools',
        'pygccxml',
    ]
)
