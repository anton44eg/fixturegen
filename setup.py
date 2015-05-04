from setuptools import setup, find_packages

setup(
    name='fixturegen',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "mako",
        "click",
        "sqlalchemy"
    ],
    entry_points={
        'console_scripts': ['fixturegen-sqlalchemy = fixturegen.cli:sqlalchemy'],
    },
    url='https://github.com/anton44eg/fixturegen',
    download_url='https://github.com/anton44eg/fixturegen/tarball/0.1',
    license='MIT',
    author='Anton Simernia',
    author_email='anton.simernya@gmail.com',
    keywords=['fixture', 'sqlalchemy', 'testing'],
    description='Fixture generator for fixture module',
    package_data={
        'fixturegen': ['templates/*.mako'],
    },
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Topic :: Database',
    ],
    test_suite='test_fixturegen',
)
