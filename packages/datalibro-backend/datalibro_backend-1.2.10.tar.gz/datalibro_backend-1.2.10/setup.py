import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="datalibro_backend",
  version="1.2.10",
  author="lucy",
  author_email="lucy@petlibro.com",
  description="A small package for your backend service",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/DesignLibro/datalibro_backend",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  install_requires=[
    "pymysql",
    "pandas"
  ],
)

