from setuptools import setup, find_packages

setup(
    name='ppf_measures',
    version='0.1.0',
    description='A library for computing PPF measures',
    author='Anitagutzw',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'mpmath',
        'ppf_approx',
        'numpy',
        'scipy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
