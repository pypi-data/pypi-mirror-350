from setuptools import setup, find_packages

setup(
    name='bbqec',
    version='1.3',
    packages=find_packages(),
    install_requires=[
        'ldpc==0.1.50',
        'matplotlib==3.4.3',
        'numpy==1.26.2',
        'networkx==3.2.1',
        'galois==0.4.1'
    ],
    author='Vansh Jhunjhunwala',
    author_email='vanshjh@gmail.com',
    description='A package for quantum error correction with bivariate bicycle codes',
    long_description_content_type='text/markdown',
    url='https://github.com/vanshjjw/qec-bicycle-bivariate',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Physics',
        'Intended Audience :: Science/Research',
    ],
    python_requires='>=3.8',
)