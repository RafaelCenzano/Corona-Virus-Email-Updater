from setuptools import setup, find_packages
from os import getcwd, path

currentDir = getcwd()

# Get Readme text
with open(path.join(currentDir, 'README.md'), encoding='utf-8') as fR:
    readme = fR.read()


# Run setup
setup(

    # Project's name
    name='Covid-19 reporter',

    # Project's version number
    # Major.Moderate.Minor values
    version='1.0.0',

    # Project's description
    description='Simple project that requests and webscrapes website then sends email when new content is released.',

    # Project's long description
    # Readme can't have links to external pages but 
    # external badges and images are permitted
    long_description=readme,

    # Define markdown long description type
    long_description_content_type='text/markdown'

    # Author's name
    author='Rafael Cenzano',

    # Author's contact
    # author_email='email@domain.com',

    # Maintainer's name
    maintainer='Rafael Cenzano',

    # Maintainer's email
    # maintainer_email='email@domain.com',

    # Project's home page
    url='https://github.com/RafaelCenzano/Corona-Virus-Email-Updater',

    # Classifiers help users find your project by categorizing it.
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        #'Intended Audience :: Developers',
        #'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        #'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # Python 2 loses support as of 2020
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # Keywords/Tags
    keywords='corona virus covid-19',

    # Finds project files
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Needed installs
    #install_requires=[],

    # Data files
    # package_data={
    #    'sample': ['package_data.dat'],
    # },

    # Python requirement
    #python_requires='>=3.4',

    # Adds CLI
    #entry_points={
    #    'console_scripts': [
    #        'sample cli command = projectName.FileName:FunctionName',
    #    ],
    #},

    # Additional links
    #project_urls={
    #    'Bug Reports': '',
    #    'Source': '',
    #},
)

# setup.py generated using PyStarter
# https://pypi.org/project/PyStarter/
# pip3 install pystarter
# The above message can be deleted, it does not effect the python code.