import os
from distutils.core import Command
from setuptools import setup, find_packages

__here__ = os.path.dirname(os.path.abspath(__file__))

package_info = {k: None for k in ["RELEASE", "COMMIT", "VERSION", "NAME"]}

for name in package_info:
    with open(os.path.join(__here__, "telemetry", name)) as f:
        package_info[name] = f.read().strip()

RULES_CORE = 'git+ssh://git@github.com/RedHatInsights/insights-core.git@3.0#egg=insights-core'


class CustomCommand(Command):
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()


class CleanCommand(CustomCommand):
    description = "clean up the current environment"

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system('rm -rf ./bin ./include ./lib ./lib64 ./*.egg-info ./man ./dist ./pip-selfcheck.json')


class BootstrapCommand(CustomCommand):
    description = "bootstrap for development"

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system('virtualenv .')
        os.system('rm -rf build/insights-core')
        os.system('rm -rf build/pyyaml')
        os.system('bin/pip install --upgrade ' + RULES_CORE)
        os.system('bin/pip install -e .[develop]')


class UpgradeCommand(CustomCommand):
    description = "upgrades to the latest version of the insights-rules-api"

    def run(self):
        assert os.getcwd() == self.cwd, "Must be in package root: %s" % self.cwd
        os.system('bin/pip install --upgrade ' + RULES_CORE)


if __name__ == "__main__":
    name = os.environ.get("CEEPH_NAME", package_info["NAME"])

    setup(
        name=name,
        version=package_info["VERSION"],
        description="Insights Plugins",
        keywords='insights-rules',
        packages=find_packages(),
        package_data={'': list(package_info.keys()) + ["*.json"]},
        install_requires=[
            'insights-core',
        ],
        extras_require={'develop': [
            'coverage>=4.4',
            'pytest>=3.6',
            'pytest-cov>=2.6.0',
            'Sphinx',
            'sphinx_rtd_theme',
            'Jinja2',
            'wheel',
            'gitpython',
            'flake8'
        ], 'optional': [
            'python-cjson'
        ]
        },
        cmdclass={
            'clean': CleanCommand,
            'bootstrap': BootstrapCommand,
            'upgrade': UpgradeCommand
        }
    )
