# setup.py
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

extensions = [
    Extension("moruapp_ms_sso.sso",       ["moruapp_ms_sso/sso.py"]),
    Extension("moruapp_ms_sso.config",    ["moruapp_ms_sso/config.py"]),
    Extension("moruapp_ms_sso.__main__",  ["moruapp_ms_sso/__main__.py"]),
    Extension("moruapp_ms_sso.__init__",  ["moruapp_ms_sso/__init__.py"]),
]

setup(
    name="moruapp-ms-sso",
    version="0.1.11",
    packages=find_packages(),
    include_package_data=True,
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "embedsignature": True,
            "annotation_typing": False,
            "language_level": "3"
        },
    ),
    zip_safe=False,
)
