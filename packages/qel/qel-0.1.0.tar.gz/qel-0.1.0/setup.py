from setuptools import setup, find_packages

setup(
    name='qel',
    version='0.1.0',
    author='Chetan Sanap',
    author_email='your-email@example.com',
    description='Terminal-based lightweight Python code editor using urwid',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=['urwid'],
    entry_points={
        'console_scripts': [
            'qel=qel.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
