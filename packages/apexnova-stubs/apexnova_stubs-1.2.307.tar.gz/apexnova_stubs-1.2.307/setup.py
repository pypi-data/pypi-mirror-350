from setuptools import setup, find_packages
import configparser

# Read configuration from setup.cfg
config = configparser.ConfigParser()
config.read("setup.cfg")

setup(
    name=config["metadata"]["name"],
    version=config["metadata"]["version"],
    description=config["metadata"]["description"],
    long_description=open(config["metadata"]["long_description"].split(": ")[1], "r").read(),
    long_description_content_type=config["metadata"]["long_description_content_type"],
    author=config["metadata"]["author"],
    author_email=config["metadata"]["author_email"],
    url=config["metadata"]["url"],
    packages=find_packages(where=config["options"]["package_dir"].split("= ")[1]),
    package_dir={"": config["options"]["package_dir"].split("= ")[1]},
    classifiers=config["metadata"]["classifiers"].split("\n")[1:],
    install_requires=config["options"]["install_requires"].split("\n")[1:],
    python_requires=config["options"]["python_requires"],
)