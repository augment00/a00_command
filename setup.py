from setuptools import setup, find_packages

setup(name='a00_command',
    version='0.0.1',
    description="python package for receiving json rpc commands via Firebase",
    url="https://github.com/augment00/a00_command",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License'
    ],
    author='Paul Harter',
    author_email='username: paul, domain: glowinthedark.co.uk',
    license="LICENSE",
    install_requires=['requests', 'pyrebase', 'raven', 'sounddevice', 'soundfile', 'picamera'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False)
