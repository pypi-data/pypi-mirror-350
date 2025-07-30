from setuptools import setup, find_packages

setup(
    name="custom_flet_components",
    version="0.2.1",
    packages=find_packages(),
    install_requires=["flet>=0.27.6"],
    tests_require=["pytest"],
    test_suite="tests",
    description="Custom Components For Flet Python",
    author="Mudassir Farooq",
    author_email="pktechmania21@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/custom_flet_components",
    license="MIT",
    entry_points={
        'console_scripts': [
            'cfc=custom_flet_components.cli:main',  # Adjust 'custom_flet_components.cli:main' to your CLI module & main function
        ],
    },
)
