import setuptools



from jypypkg import __version__, __author__, __email__, __description__, __url__
setuptools.setup(
    name="jypypkg",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=__description__,
    long_description_content_type="text/markdown",
    url=__url__,
    packages=setuptools.find_packages(),
    
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
       
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
       
        'Operating System :: OS Independent',
    ],
)