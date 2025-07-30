from setuptools import setup, find_packages

setup(
    name='twotuft2count',
    version='0.1',
    description='A CLI pipeline for combining, segmenting, quantifying, and visualizing multiplexed imaging data.',
    author='Pascal Flüchter',
    author_email='pascal.fluechter@uzh.ch',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas',
        'tifffile',
        'scipy',
        'napari[all]',
        'magicgui',
        'click',
        'tifftools',
        'instanseg-torch',
        'fcswrite',
        'scikit-image'
    ],
    entry_points={
        'console_scripts': [
            'twotuft2count=twotuft2count.cli:main',
        ],
    },
)
