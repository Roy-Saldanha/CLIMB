from setuptools import find_packages, setup

package_name = 'base_station_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='roysaldanha',
    maintainer_email='roysaldanha@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
	'mock_cam = base_station_pkg.mock_cam_node:main',
	'sensor_pub = base_station_pkg.sensor_publisher:main',
        ],
    },
)

