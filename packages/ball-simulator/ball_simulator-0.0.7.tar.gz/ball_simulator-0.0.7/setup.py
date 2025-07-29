from setuptools import setup, find_packages

setup(
    name="ball-simulator",
    version="0.0.7",
    packages=find_packages(),
    install_requires=["pygame"],
    entry_points={
        "console_scripts": [
            "ball-simulator = ball_simulator.main:main",
        ],
    },
)
