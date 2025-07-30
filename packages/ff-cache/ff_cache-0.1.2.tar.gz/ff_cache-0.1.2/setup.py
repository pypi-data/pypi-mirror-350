from setuptools import find_packages, setup

setup(
    name='ff-cache',
    version='0.1.2',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    zip_safe=False,
    include_package_data=True
)