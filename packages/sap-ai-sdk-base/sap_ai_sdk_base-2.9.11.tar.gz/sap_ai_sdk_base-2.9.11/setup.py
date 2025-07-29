"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding

def generate_metadata():
    classifiers = """\
    Development Status :: 1 - Planning
    License :: Other/Proprietary License
    Operating System :: MacOS
    Operating System :: Microsoft :: Windows
    Operating System :: POSIX :: Linux
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.9
    Programming Language :: Python :: 3.10
    Programming Language :: Python :: 3.11
    Programming Language :: Python :: 3.12
    Topic :: Software Development :: Libraries :: Python Modules"""
    metadata = dict(
        description="SAP Cloud SDK for AI (Python): Base Client",
        long_description_content_type='text/markdown',
        long_description="# SAP Cloud SDK for AI (Python): Base Client for AI API\n  will be published here soon ...",
        keywords="SAP AI Core",
        url="https://www.sap.com/",
        author="SAP SE",
        download_url="https://pypi.python.org/pypi/sap-ai-sdk-base",
        license='SAP DEVELOPER LICENSE AGREEMENT',
        classifiers=[_f for _f in classifiers.split('\n') if _f],
        platforms=["Windows", "Linux", "Mac OS-X", "Unix"],
        version="2.9.11",
        python_requires='>=3.9',
        zip_safe=False,
    )
    return metadata


setup(name="sap-ai-sdk-base",
      include_package_data=True,
      **generate_metadata()
      )
