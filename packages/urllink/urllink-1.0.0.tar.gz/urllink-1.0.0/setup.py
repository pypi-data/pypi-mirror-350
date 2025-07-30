from setuptools import setup, find_packages

setup(
    name="urllink",                        # Your package name (must be unique on PyPI)
    version="1.0.0",                    
    author="Muhammad Hamza Shahzad",
    author_email="myhamza.204@gmail.com",
    description="A Python library for URL shortening and QR code generation.",
    long_description_content_type="text/markdown",
    url="https://urllink.site",
    packages=find_packages(),             # Automatically find packages in urllink/
    install_requires=[                    # Dependencies your library needs
        "requests",
    ],

)
