# @Author: Jahleel Lacascade <jahleel>
# @Date:   2020-09-03T10:00:44-04:00
# @Email:  vabyz971@gmail.com
# @Last modified by:   jahleel
# @Last modified time: 2020-09-03T11:38:09-04:00
# @License: GPLv3

from setuptools import setup, find_packages

setup(
    name='django-template-nierAutomata',
    version=__import__('nierInterface').__version__,
    description='Template inspirer de l\'interface NierAutomata',
    long_description=open('README.md').read(),
    Author='vabyz971',
    url='https://github.com/vabyz971/django-template-nierAutomata',
    packages=find_packages(),
    license=open('LICENSE').read(),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    install_requires=['django>3', 'Pillow', 'easy-thumbnails'],
    include_package_data=True,
    zip_safe=False,
)
