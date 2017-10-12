#
# Copyright (c) 2017 Red Hat, Inc.
#
# This file is part of gluster-health-report project which is a
# subproject of GlusterFS ( www.gluster.org)
#
# This file is licensed to you under your choice of the GNU Lesser
# General Public License, version 3 or any later version (LGPLv3 or
# later), or the GNU General Public License, version 2 (GPLv2), in all
# cases as published by the Free Software Foundation.

from setuptools import setup


setup(
    name="glusterlog",
    version="0.2",
    packages=["glusterlog"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "gluster-log-colorize = glusterlog.colorize:main",
            "gluster-log-json = glusterlog.tojson:main",
        ]
    },
    platforms="linux",
    zip_safe=False,
    author="Aravinda VK",
    author_email="avishwan@redhat.com",
    description="Gluster Log parser",
    license="GPLv2",
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
