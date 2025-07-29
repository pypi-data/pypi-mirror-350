from setuptools import setup, find_packages

setup(
    name='emox',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,  # Includes non-code files specified in MANIFEST.in
    package_data={
        'emox': ['*.pkl']  # Includes all .pkl files in the emox package
    },
    install_requires=[
        'scipy==1.13.1',
        'numpy==1.26.4',
        'gensim==4.3.3',
        'tensorflow==2.18.0'
    ],
)

