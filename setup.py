import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'ur16e_control_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ayesha Habib',
    maintainer_email='ayeshahabib654@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'initials_demo = ur16e_control_package.initials_demo:main',
            'spawn_entities = ur16e_control_package.spawn_entities:main',
            'move_command = ur16e_control_package.move_command:main',
        
        ],
    },
)
