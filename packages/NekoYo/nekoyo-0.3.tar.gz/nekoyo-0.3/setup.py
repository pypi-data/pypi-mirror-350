from setuptools import setup, find_packages

# 使用绝对路径读取README
with open("D:\\readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='NekoYo',
    version='0.3',
    packages=find_packages(include=['NekoYo', 'NekoYo.*']),
    install_requires=[
        'pyserial',
    ],
    include_package_data=True,
    author='FatPanda8885',
    author_email='FatPanda8885@foxmail.com',

    description='A Yaesu CAT commands library based on Python.',
    long_description=long_description,
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
            'NekoYo=NekoYo:main_function',
        ],
    },
)
