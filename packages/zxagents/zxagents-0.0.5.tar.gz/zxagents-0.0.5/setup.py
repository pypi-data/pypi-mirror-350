import os
from setuptools import setup, find_packages

setup(
    name='zxagents',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        
    ],
    author='Meng',
    author_email='meng@zxtech.info',
    description='openai-agnets自定义配置',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/menghuiqiang777/zx-agents',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    
        'Programming Language :: Python :: 3.12',
    ],
)