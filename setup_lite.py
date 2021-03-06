import setuptools

setuptools.setup(
    name='wgbs_tools',
    version='1.0',
    description='Toolkit to manipulate and analyze Whole Genome Bisulfite Sequencing data',
    packages=setuptools.find_packages(),
    include_package_data=True,
    py_modules=['wgbs_tools'],
    install_requires=[
        'click',
        'pytest',
        'pyyaml',
        'pysam',
        'pybedtools',
    ],
    entry_points='''
        [console_scripts]
        wgbs_tools=wgbs_tools_lite:cli
    '''
)