from setuptools import find_packages, setup

__author__ = """Matej Lanca"""
__email__ = "lancamatej@gmail.com"
__version__ = "1.0.6a"
__description__ = "NetBox plugin for integration with the netauto ecosystem."

setup(
    name='netbox-netauto-plugin',
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)