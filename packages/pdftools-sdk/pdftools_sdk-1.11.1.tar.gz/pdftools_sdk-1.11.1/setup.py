from setuptools import find_packages, setup

setup(
    name="pdftools_sdk",
    version="1.11.1",
    packages=find_packages(),
    description="Python package for Pdftools SDK",
    long_description="""
The Pdftools SDK is a comprehensive development library that lets developers integrate advanced PDF conversion, optimization, and validation functionalities into in-house applications.

PDF software by developers for developers:
- Regular feature releases
- No external dependencies
- Comprehensive manual and code samples
- Supports PDF 1.x, PDF 2.0, PDF/A

Visit our website for more information.
""",
    long_description_content_type="text/markdown",
    author="PDF Tools AG",
    url="https://www.pdf-tools.com/products/conversion/pdf-tools-sdk/?utm_medium=repository&utm_source=pypi&utm_campaign=pdftoolssdk",
    project_urls={
        "Documentation": "https://www.pdf-tools.com/docs/pdf-tools-sdk",
        "Support": "https://www.pdf-tools.com/docs/support/",
        "Contact": "https://www.pdf-tools.com/contact/",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: Other/Proprietary License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    license="Proprietary",
    license_files=("pdf-tools-license.md",),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # Add any dependencies
    ],
    python_requires=">=3.7",
)
