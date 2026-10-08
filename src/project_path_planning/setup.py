from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'project_path_planning'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
    ),
    (
        'share/' + package_name,
        ['package.xml']
    ),
    (
        os.path.join('share', package_name, 'launch'),
        glob('launch/*.py')
    ),
    (
        os.path.join('share', package_name, 'config'),
        glob('config/*.yaml')
    ),
    ],
    
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='navjot',
    maintainer_email='navjotsinghsodhi52@gmail.com',
    description='Nav2 planning, control, behavior configuration, and reusable navigation goals',
    
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'spot_recorder = project_path_planning.spot_recorder:main',
            'move_to_spot = project_path_planning.move_to_spot:main',
        ],
    },
)
