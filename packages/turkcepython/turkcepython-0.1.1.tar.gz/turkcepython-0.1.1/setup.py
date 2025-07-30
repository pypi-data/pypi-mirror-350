from setuptools import setup

setup(
    name='turkcepython',
    version='0.1.1',
    description='Türkçe anahtar kelimelerle Python yazmayı sağlayan eğitim amaçlı bir paket.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',  
    author='Utku Coban',
    license='MIT',
    packages=['turkcepython'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Turkish',
        'Intended Audience :: Education',
    ],
)
