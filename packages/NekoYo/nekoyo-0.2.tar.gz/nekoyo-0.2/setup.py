from setuptools import setup, find_packages

setup(
    name='NekoYo',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'pyserial',
    ],
    author='FatPanda8885',
    author_email='FatPanda8885@foxmail.com',

    description='A Yaesu CAT commands library based on Python.',
    long_description=open('README.md',encoding="utf-8",).read(),
    long_description_content_type='text/markdown',

    url='https://github.com/GAQPanda/NekoYo',

    license='Apache-2.0',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],

    keywords='Yaesu CAT',

    # extras_require={
    #     'dev': ['check-manifest'],
    #    'test': ['coverage'],
    # },

    # package_data={
        # 'name': ['*.txt', '*.rst'],
    # },

    entry_points={
        'console_scripts': [
            'nekyoyo=NekoYo.module:main_function',
        ],
    },
)
