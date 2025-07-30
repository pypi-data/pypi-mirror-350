from setuptools import setup, find_packages

setup(
    name='mathify',  # Name of your package
    version='0.1.0',  # Initial release version
    author='David Warner',  # Your name
    author_email='kaboom31@example.com',  # Your email
    description='A package for mathematical utilities and functions',  # Short description
    long_description=open('README.md').read(),  # Long description from README
    long_description_content_type='text/markdown',  # Format of the long description
    url="https://github.com/none/mathify",  # URL of your project
    packages=find_packages(),  # Automatically find packages in your directory
    entry_points={
        'console_scripts': [
            'mathify-cli=mathify.cli:main',  # command: function
        ],},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Or your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
    install_requires=[
        # List your package dependencies here, e.g.,
        # 'numpy>=1.21',
    ],
    include_package_data=True,
    zip_safe=False,
)
