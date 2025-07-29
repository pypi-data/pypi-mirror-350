from setuptools import setup, find_packages

setup(
    name="Raihan_Time",
    version="0.1",
    description="বাংলা সময় ও দিন দেখানোর Tkinter অ্যাপ",
    author="MD. Mostafa Raihan",
    author_email="m.raihan.computerscience@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pytz",
        "bangla"
    ],
    entry_points={
        'console_scripts': [
            'bangla-time = bangla_time_viewer:run',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
