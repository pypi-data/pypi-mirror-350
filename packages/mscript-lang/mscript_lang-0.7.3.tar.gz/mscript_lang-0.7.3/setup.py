from setuptools import setup, find_packages

setup(
    name='mscript-lang',
    version="0.7.3",
    author="Momo-AUX1",
    description='Mscript: A lightweight interpreted scripting language',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(include=['mscript', 'mscript.*']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mscript = mscript.cli:main',
            'mpmp = mscript.mpp:main',
        ],
    },
    install_requires=[
        'lark',
        'requests',
        'colorama',
        'wget',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)