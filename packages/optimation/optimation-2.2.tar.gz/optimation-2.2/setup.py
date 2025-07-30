from setuptools import setup, find_packages

setup(
    name='optimation',
    version='2.2',
    packages=find_packages(),
    install_requires=["numpy"],
    include_package_data=True,
    author='Sourceduty',
    author_email='sourceduty@gmail.com',
    description='Enhanced version 2.2 with variable modeling and optimation.',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/optimation',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
