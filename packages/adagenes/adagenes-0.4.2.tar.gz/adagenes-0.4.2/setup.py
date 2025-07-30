import setuptools
import adagenes as ag

with open("README.md", "r") as fh:
    long_description = fh.read()

version = ag.conf_reader.config['DEFAULT']['VERSION']

setuptools.setup(
    name="adagenes",
    version=version,
    author="Nadine S. Kurz",
    author_email="nadine.kurz@bioinf.med.uni-goettingen.de",
    description="Generic toolkit for processing DNA polymorphism data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.gwdg.de/MedBioinf/mtb/adagenes",
    packages=setuptools.find_packages(),
    install_requires=['requests','liftover','plotly','openpyxl','matplotlib','scikit-learn','blosum','pandas',
                      'python-magic', 'upsetplot','openpyxl',
                      'numpy','flask', 'Flask-Cors', 'flask-swagger-ui','requests','pymongo'],
    extras_require={
        "extra": ["onkopus"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    license_files = ('LICENSE.txt',)
)

