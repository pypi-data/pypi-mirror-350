"""
Setup script for the Logbee SDK.
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages

# Read version from __init__.py file
with open('src/logbee/__init__.py', 'r', encoding='utf-8') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        version = '0.1.0'  # If no version is defined, use 0.1.0

# Read README content
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

# Package requirements
requirements = [
    'requests>=2.25.0',
]

# Optional requirements for adapters
extras_require = {
    'flask': ['flask>=2.0.0'],
    'fastapi': ['fastapi>=0.68.0'],
    'django': ['django>=3.2.0'],
    'all': ['flask>=2.0.0', 'fastapi>=0.68.0', 'django>=3.2.0'],
    'dev': [
        'pytest>=6.2.0',
        'pytest-cov>=2.12.0',
        'flake8>=3.9.0',
        'black>=21.5b2',
    ],
}

setup(
    name='logbee-sdk',
    version=version,
    description='SDK for integrating Python applications with Logbee',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Logbee',
    author_email='info@logbee.dev',
    url='https://github.com/logbee/logbee-sdk-py',
    packages=['logbee'],
    package_dir={'logbee': 'src/logbee'},
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    license='MIT',
    zip_safe=False,
    keywords='logbee, logging, monitoring, errors, api',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.7',
)
