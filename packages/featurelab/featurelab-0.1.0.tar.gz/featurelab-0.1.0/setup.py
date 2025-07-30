from setuptools import setup, find_packages

setup(
    name="featurelab",
    version="0.1.0",
    description="Comprehensive feature engineering package with statistical guidance",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Shekhar Suman",
    author_email="s.sumanpathak513@gmail.com",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "featurelab=featurelab.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords="feature-engineering data-preprocessing machine-learning pandas visualization",
    include_package_data=True,
    zip_safe=False,
)