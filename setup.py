# -*- coding: utf-8 -*-
"""
    glusterlog.setup.py
    :copyright: (c) 2017 by Aravinda VK
    :license: MIT, see LICENSE for more details.
"""

from setuptools import setup


setup(
    name="glusterlog",
    version="0.1",
    packages=["glusterlog"],
    include_package_data=True,
    install_requires=[],
    platforms="linux",
    zip_safe=False,
    author="Aravinda VK",
    author_email="mail@aravindavk.in",
    description="Gluster Log parser",
    license="MIT",
    keywords="gluster, tool, logs",
    url="https://github.com/aravindavk/glusterlog",
    long_description="""
    Gluster Log Parser
    """,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only"
    ],
)
