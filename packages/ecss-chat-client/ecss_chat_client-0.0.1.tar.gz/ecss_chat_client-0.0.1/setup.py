from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='ecss-chat-client',
    version='0.0.1',
    author='maxstolpovskikh',
    author_email='maximstolpovskikh@gmail.com',
    description='This is the simplest module for quick work with files.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='files speedfiles ',
    python_requires='>=3.12.3'
)
