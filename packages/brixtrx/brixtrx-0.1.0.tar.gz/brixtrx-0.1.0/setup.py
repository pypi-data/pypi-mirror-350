from setuptools import setup, find_packages

setup(
    name='brixtrx',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Faris',
    author_email='noreply@example.com',
    description='To classified transaction data whether it is transfer, withdrawal, deposit and payment/purchase',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)