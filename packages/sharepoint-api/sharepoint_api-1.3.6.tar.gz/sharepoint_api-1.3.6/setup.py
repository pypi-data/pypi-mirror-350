from distutils.core import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='sharepoint_api',
    version='1.3.6',
    description='Python SharePoint API for folder or file operations (download, upload, delete)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Naseem AP',
    author_email='naseemalassampattil@gmail.com',
    url="https://github.com/naseemap-er/sharepoint_api",
    download_url="https://github.com/naseemap-er/sharepoint_api/archive/refs/tags/v1.0.tar.gz",
    packages=['sharepoint_api'],
    license='MIT',
    keywords=['sharepoint', 'api', 'python', 'sharepoint api', 'sharepoint folder', 'sharepoint file'],
    install_requires=[
        'pyyaml',
        'office365-rest-python-client'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)