from setuptools import setup, find_packages

setup(
    name='AIModeler',
    version='0.91',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["PyMuPDF", "tiktoken"],
    include_package_data=True,
    author='Alexander Brown',
    author_email='ajbrownt@gmail.com',
    description='AIModeler - AI and ML model building tool',
    long_description='A longer description of your package',
    long_description_content_type='text/markdown',
    url='https://github.com/AIModeler/aimodeler',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13'
    ],
)
