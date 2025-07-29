from setuptools import setup, find_packages

setup(
    name='beautiful-terminal',
    version='1.0.0',
    description='A Python library that automatically beautifies terminal output by adding colors based on message content.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='DevStarByte',
    author_email='',
    url='https://github.com/StarByteGames/beautiful-terminal',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='terminal color console logging beautify',
    include_package_data=True,
    entry_points={},
    install_requires=[],
    extras_require={
        'version_check': ['requests', 'setuptools'],
    }
)

#python setup.py sdist bdist_wheel
#twine upload dist/*