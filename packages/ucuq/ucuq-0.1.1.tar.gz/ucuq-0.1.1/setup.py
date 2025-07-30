# Pypi setup file for UCUq.
import setuptools

version = "0.1.1"

with open("ucuq/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ucuq",
    version=version,
    author="Claude SIMON",
#    author_email="author@example.com",
    description="A very light Python library with no dependencies for easy prototyping of projects based on Wi-Fi equipped microcontrollers (RPi Pico (2) W, ESP32, ESP8266…)",
    keywords="microcontrolers, RPi Pico, ESP32, ESP8266, Wi-Fi, micropython, I2C, SPI, GPIO, PWM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/epeios-q37/ucuq-python",
    packages=setuptools.find_packages(),
    classifiers=[
      "Development Status :: 5 - Production/Stable",
      "Environment :: Other Environment",
      "Intended Audience :: Developers",
      "Intended Audience :: Education",
      "Intended Audience :: Other Audience",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Operating System :: Other OS",
      "Programming Language :: Python :: 3",
      "Topic :: Internet",
      "Topic :: Scientific/Engineering",
      "Topic :: Software Development",
      "Topic :: Utilities",
    ]
)
