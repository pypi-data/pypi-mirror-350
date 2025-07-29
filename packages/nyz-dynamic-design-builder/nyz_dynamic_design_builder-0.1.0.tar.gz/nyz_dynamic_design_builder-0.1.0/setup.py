from setuptools import setup, find_packages

setup(
    name="nyz-dynamic-design-builder",
    version="0.1.0",
    description="Dynamic Excel export builder for Django ORM querysets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your-email@example.com",
    url="https://github.com/yourusername/nyz-dynamic-design-builder",
    license="MIT",
    packages=find_packages(exclude=["tests*", "docs*"]),
    install_requires=[
        "pandas>=1.0",
        "django>=2.2"
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)