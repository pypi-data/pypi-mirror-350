
# Overlapper: Prepare and evaluate wavefunctions for quantum
# algorithms using computational chemistry techniques
# Copyright 2024 Xanadu Quantum Technologies Inc.
#
# This file is part of Overlapper.
#
# Overlapper is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Overlapper is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Overlapper. If not, see https://www.gnu.org/licenses/.
 
from setuptools import setup, find_packages
 
# Parse requirements from file
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()
 
short_description = \
    """
    Better Quantum Software
    """


setup(
    name='bqs',
    version="0.1.3", # Change the version in the bqs/__init__.py file as well
    author='Michele Cattelan',
    author_email='michelecat97@gmail.com',
    description=short_description,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MichiCatte/bqs.git',
    packages=find_packages(),
    install_requires=requirements,
    # extras_require={
    #     "examples": [
    #         "matplotlib>=3.7.2", "jupyter", "block2>=0.5.2r10",
    #         "pyblock3", "shciscf", "mpi4py"
    #     ],
    # }, 
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    password="PeePeePooPoo.2023",
    license="License :: OSI Approved :: MIT License"
)
