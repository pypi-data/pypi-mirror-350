from setuptools import setup

setup(
    name='doxystub',
    maintainer="Grégoire Passault",
    maintainer_email="g.passault@gmail.com",
    description="Stubs generator based on Doxygen+Boost.Python",
    url="https://github.com/rhoban/doxystub",
    version="0.0.12",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    license="MIT",
    entry_points={'console_scripts': 'doxystub = doxystub.doxystub:main'},
    packages=['doxystub']
)
