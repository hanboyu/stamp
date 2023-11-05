from setuptools import setup
from setuptools import find_packages
  
setup(
    name='stamp',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        "grpcio>=1.53.0",
        "grpcio-tools>=1.50.0",
        "netifaces==0.11.0",
        "scapy==2.5",
        "pandas>=2.0.0"
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'STAMPSender = ProbingAgent.utility.STAMPSender:main',
            'STAMPReflector = ProbingAgent.utility.STAMPReflector:main'
        ]
    }
)