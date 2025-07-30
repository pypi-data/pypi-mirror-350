from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='SOLIDserverCLI',
    version='0.3.0',
    description='EfficientIP SOLIDserver cli',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Alex Chauvin',
    author_email='ach@efficientip.com',
    url='https://gitlab.com/efficientip/cli-for-solidserver',
    license=license,
    packages=['sds'],

    entry_points={
        'console_scripts': [
            'sds = sds.cli:main',
        ],
    },

    python_requires='>=3.10',
    install_requires=['typer', 'rich', 'SOLIDserverRest'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python",
        "Intended Audience :: Developers"
    ],
)
