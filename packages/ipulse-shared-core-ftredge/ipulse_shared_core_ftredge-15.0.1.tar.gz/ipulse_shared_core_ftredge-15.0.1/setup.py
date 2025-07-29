# pylint: disable=import-error
from setuptools import setup, find_packages

setup(
    name='ipulse_shared_core_ftredge',
    version='15.0.1',
    package_dir={'': 'src'},  # Specify the source directory
    packages=find_packages(where='src'),  # Look for packages in 'src'
    install_requires=[
        # List your dependencies here
        'pydantic[email]~=2.5',
        'python-dateutil~=2.8',
        'fastapi~=0.115.8',
        'pytest',
        'ipulse_shared_base_ftredge==6.5.1',
    ],
    author='Russlan Ramdowar',
    description='Shared Core models and Logger util for the Pulse platform project. Using AI for financial advisory and investment management.',
    url='https://github.com/TheFutureEdge/ipulse_shared_core',

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)