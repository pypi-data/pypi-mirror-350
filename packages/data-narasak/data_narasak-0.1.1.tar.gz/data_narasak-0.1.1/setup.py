from setuptools import setup, find_packages

setup(
    name='data_narasak',
    version='0.1.1',
    author='Kumaran Ravichandran',
    author_email='kumaranravi3112003@gmail.com',
    description='A Python package for data transformation and generating PDF reports with detailed analysis and visualizations.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),  # Automatically find name of your package
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'matplotlib>=3.4.0',
        'reportlab>=3.6.0',
        'openpyxl>=3.0.0',
        'scikit-learn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    python_requires='>=3.7',
)
