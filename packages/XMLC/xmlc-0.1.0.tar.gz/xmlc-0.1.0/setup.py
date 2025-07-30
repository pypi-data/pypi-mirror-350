from setuptools import setup, find_packages

setup(
    name="xmlc",  # Replace with your package name
    version="0.1.0",
    author="Zohan Haque",
    author_email="zohanuhaque@gmail.com",
    description="A Framework for building console apps in xml",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-repo",  # Optional
    packages=find_packages(),  # Automatically find packages in your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Or whatever license you use
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Add any dependencies your package needs, like:
        # "requests>=2.25.1",
    ],
    include_package_data=True,
    license="MIT",  # Or your preferred license
)
