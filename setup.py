from setuptools import setup, find_packages

setup(
    name='PyKineticsAnalyzer',
    version='0.0.1',
    author='Erik S. Carlsten',
    author_email='erik@preactiontechnology.com',
    packages = find_packages(), #['pykineticsanalyzer', 'pykineticsanalyzer.test'],
    url='https://github.com/ecarlste/PyKinecticsAnalyzer/',
    license='LICENSE.txt',
    description='Skeleton Motion Kinetics Analysis.',
    long_description=open('README.txt').read(),
    install_requires=[
        "cgkit >= 2.0",
        ],
    )