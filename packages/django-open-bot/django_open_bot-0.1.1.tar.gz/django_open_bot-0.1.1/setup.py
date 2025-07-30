from setuptools import setup, find_packages

setup(
    name="django_open_bot",
    version="0.1.1",
    author="Shohzodbek",
    author_email="vipfthef@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/username/mycoolapp',
    install_requires=[
        "django",
        "requests",
        "aiohttp"
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
)
