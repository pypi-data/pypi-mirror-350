from setuptools import setup, find_packages

setup(
    name='turkcepython',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'turkcepython=turkcepython.cli:main',
        ],
    },
    author='Sen',
    description='Türkçe Python Çeviris',
    python_requires='>=3.6',
)
