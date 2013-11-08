import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name="cv_utils",
        version="0.0.1",
        author="David Daniel",
        author_email="davydany@gmail.com",
        description=("Scripts that help make working with OpenCV a lot easier."),
        license="BSD",
        keywords="opencv cv machine learning computer vision",
        packages=find_packages(),
        long_description=read('README.md'),
        entry_points={
                'console_scripts' : [
                        'cvutils_createsamples = cvutils.haar.batch_createsamples:main'
                ]
        },
)