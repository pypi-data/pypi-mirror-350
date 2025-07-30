from setuptools import setup, find_packages

setup(
    name='configureout',
    version='2.1',
    description='A lightweight and flexible configuration loader for Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='EightShift',
    author_email='the8shift@gmail.com',
    url='https://github.com/EightShift/configureout',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)