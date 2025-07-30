from setuptools import setup

setup(
    name="raspberrytq",
    version="0.1.0",
    py_modules=["raspberrytq"],
    description="MicroPython CLI for Raspberry Pi Pico RTC and LED control.",
    author="Xscripts Inc.",
    author_email="sunnyplaysyt9@gmaial.com",
    url="https://github.com/PyWebServerHosts/RaspberryTQ/",
    entry_points={
        "console_scripts": [
            "raspberrytq=raspberrytq:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
