import os

import setuptools

with open("README.md", "r", encoding='utf-8') as rfile:
    long_description = rfile.read()

with open(os.path.join("featurize_haunter", "__about__.py")) as rfile:
    v_dict = {}
    exec(rfile.read(), v_dict)
    version = v_dict['__version__']


setuptools.setup(
    name="featurize_hanuter",
    version=version,
    author="Dongsheng Lin",
    description="command line tool for init and config",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LinDong123a/featurize-haunter",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "featurize-haunter = featurize_haunter.featurize_haunter:main",
        ],
    },
    package_dir={"featurize_haunter": "featurize_haunter"},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        "featurize==0.0.12",
        "playsound==1.2.2",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Source": "https://github.com/LinDong123a/featurize-haunter",
    },
)
