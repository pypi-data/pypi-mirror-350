from setuptools import setup, find_packages

setup(
    name='ArtusAPI',
    version='1.3.8',
    description='API to control Artus Family of Robots by Sarcomere Dynamics Inc',
    project_description='Python API to control Artus Family of Robots by Sarcomere Dynamics Inc',
    # package_dir={'': '/'},  # tells setuptools that your packages are under src
    packages=find_packages(exclude=['data*', 'examples*', 'tests*','venv*', 'urdf*', 'ros2*']),
    author='Sarcomere Dynamics Inc.',
    url='https://sarcomeredynamics.com/home',
    install_requires=[
        'psutil',
        'pyserial',
        'esptool',
        'pyyaml',
        'tqdm',
        'requests'
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'artusapiflash = ArtusAPI.artus_api:main_flash',
            'artusapimain = ArtusAPI.artus_api:main'
        ]
    }
    # packages=find_packages(where='/'),
    # other setup configurations
)   