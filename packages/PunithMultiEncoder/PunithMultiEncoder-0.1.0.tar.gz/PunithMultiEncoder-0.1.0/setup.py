from setuptools import setup, find_packages

setup(
    name='PunithMultiEncoder',
    version='0.1.0',
    description='A multilingual encryption and decryption library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Punithan',
    author_email='punithanae@gmail.com',
    packages=find_packages(),
    keywords=['encryption', 'multilingual', 'decryption', 'language', 'security'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)



