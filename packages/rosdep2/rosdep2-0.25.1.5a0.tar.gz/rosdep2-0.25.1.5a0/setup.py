import os
from setuptools import setup

kwargs = {
    'name': 'rosdep2',
    # same version as in:
    # - src/rosdep2/_version.py
    # - stdeb.cfg
    'version': '0.25.1.5a0',
    'packages': ['rosdep2', 'rosdep2.ament_packages', 'rosdep2.platforms'],
    'package_dir': {'': 'src'},
    'install_requires': [
        'PyYAML >= 3.1',
        'importlib_metadata; python_version<"3.8"',
    ],
    'python_requires': '>=3.6',
    'extras_require': {
        'test': [
            'flake8',
            'flake8-builtins',
            'flake8-comprehensions',
            'flake8-quotes',
            'pytest',
        ],
    },
    'author': 'Tully Foote, Ken Conley',
    'author_email': 'tfoote@osrfoundation.org',
    'maintainer': 'ROS Infrastructure Team',
    'project_urls': {
        'Source code':
        'https://github.com/krisl/rosdep',
        'Issue tracker':
        'https://github.com/krisl/rosdep/issues',
    },
    'url': 'http://wiki.ros.org/rosdep',
    'keywords': ['ROS'],
    'entry_points': {
        'console_scripts': [
            'rosdep = rosdep2.main:rosdep_main',
            'rosdep-source = rosdep2.install:install_main'
        ]
    },
    'classifiers': [
        'Programming Language :: Python',
    ],
    'description': 'rosdep - enhanced with lovely quality of life improvements',
    'long_description': 'Command-line tool for installing system '
                        'dependencies on a variety of platforms. '
                        'Includes extra command line options to make integration '
                        'with automated build systems more convenient',
    'long_description_content_type': 'text/x-rst',
    'license': 'BSD',
}
if 'SKIP_PYTHON_MODULES' in os.environ:
    kwargs['packages'] = []
    kwargs['package_dir'] = {}
elif 'SKIP_PYTHON_SCRIPTS' in os.environ:
    kwargs['name'] += '_modules'
    kwargs['entry_points'] = {}
else:
    kwargs['install_requires'] += ['catkin_pkg >= 0.4.0', 'rospkg >= 1.4.0', 'rosdistro >= 0.7.5']

setup(**kwargs)
