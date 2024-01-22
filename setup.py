from setuptools import setup, find_packages

setup(
    name='bugcode',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "bugcode_plugins",
    ],
    entry_points={  # Optional
        'console_scripts': [
            'bugcode-server=bugcode.start_server:main',
            'bugcode-manage=bugcode.manage:cli',
            'bugcode-worker=bugcode.server.celery_worker:main',
            'bugcode-worker-gevent=bugcode.server.celery_worker_gevent:main',
            'bugcode-start-all=bugcode.start_all:main'
        ],
    },
    # Other metadata such as author, author_email, description, etc.
)