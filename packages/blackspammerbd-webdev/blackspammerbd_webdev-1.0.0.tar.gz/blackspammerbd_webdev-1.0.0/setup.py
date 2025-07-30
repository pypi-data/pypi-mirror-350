from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blackspammerbd-webdev",
    version="1.0.0",
    author="BLACK SPAMMER BD",
    author_email="shawponsp6@gmail.com",
    description=(
        "The world’s most powerful, efficient, and professional web-pentester "
        "(2025), with dynamic payload loading and AJAX-aware crawling."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BlackSpammerBd/blackspammerbd-webdev",
    project_urls={
        "Bug Tracker": "https://github.com/BlackSpammerBd/blackspammerbd-webdev/issues",
        "Documentation": "https://github.com/BlackSpammerBd/blackspammerbd-webdev/wiki",
        "Source Code": "https://github.com/BlackSpammerBd/blackspammerbd-webdev",
        "Author's Facebook": "https://www.facebook.com/original.Typeboss.ur.father"
    },
    packages=find_packages(exclude=["tests*", "docs*", "examples*"]),
    install_requires=[
        "click>=8.0",
        "requests>=2.25",
        "beautifulsoup4>=4.9",
        "tqdm>=4.64",
        "PyYAML>=6.0",
        "colorama>=0.4"
    ],
    entry_points={
        "console_scripts": [
            "sp=blackspammerbd_webdev.core:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    keywords="blackspammerbd web pentest ethical hacking cybersecurity cli tool",
)
