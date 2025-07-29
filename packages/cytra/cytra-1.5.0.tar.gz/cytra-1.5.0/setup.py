from setuptools import find_packages, setup


def read_version(module_name):
    from os.path import dirname, join
    from re import S, match

    with open(join(dirname(__file__), module_name, "__init__.py")) as f:
        return match(r".*__version__.*('|\")(.*?)('|\")", f.read(), S).group(2)


setup(
    name="cytra",
    version=read_version("cytra"),
    keywords="database",
    packages=find_packages(),
    install_requires=[
        "gongish ~= 1.4.0",
        "sqlalchemy ~= 1.4.0",
        "pytz ~= 2021.1",
        "pyjwt ~= 2.1.0",
        "redis ~= 3.5.3",
        "user-agents ~= 2.2.0",
        "webtest ~= 2.0.35",
        "babel ~= 2.17.0",
    ],
    extras_require=dict(
        ujson=["ujson >= 4.0.0"],
    ),
)
