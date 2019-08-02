"""
Check whether the root user can login via SSH
=============================================

This rule checks the following conditions to verify if the root login is allowed via SSH:
1. Verify if 'PermitRootLogin yes' in /etc/ssh/sshd_config
2. Verify if sshd.service is running in the host
3. Fetch distro name(Optional)

Usage:
    $ insights-run -p check_ssh_root_login.py /Path/to/the/sos-report.tar.xz
"""
from insights.core.plugins import condition, make_fail, make_pass, rule
from insights.core.spec_factory import simple_file
from insights import Parser, parser
from insights.parsers.ssh import SshDConfig
from insights.parsers.systemd.unitfiles import ListUnits
from insights.parsers.redhat_release import RedhatRelease
from insights.parsers import split_kv_pairs
from insights.specs import Specs


# Define a path to locate a file witihin the sos-report
class SosSpecs(Specs):
    lsb_release = simple_file("etc/lsb-release")


@parser(SosSpecs.lsb_release)
class LsbRelease(Parser):
    """
    Returns `data`:

        {
           'product': 'Ubuntu',
           'version': '18.04'
        }
    """
    def parse_content(self, content):
        _content = split_kv_pairs(content)
        self.data = {
            'product': _content['DISTRIB_ID'],
            'version': _content['DISTRIB_RELEASE']
        }

    @property
    def product(self):
        return self.data['product']

    @property
    def version(self):
        return self.data['version']


fail_message = """
The root user can login on this {{os}} host because the 'PermitRootLogin' is set
to 'yes' in /etc/ssh/sshd_config.

It is recommended to set 'PermitRootLogin' to 'prohibit-password',
'forced-commands-only' or 'no'.

Please refer the manpage of SSHD_CONFIG for more info:
$ man 5 ssh_config
"""

pass_message = """
The root user cannot login on this {{os}} host.
"""

CONTENT = {
    'SSHD_ROOT_LOGIN_PERMITTED': fail_message,
    'SSHD_ROOT_LOGIN_DISABLED': pass_message
}


@condition(SshDConfig)
def check_permit_root_login(sshd):
    """Return True if 'PermitRootLogin yes' in /etc/ssh/sshd_config.
    """
    if sshd.get('permitrootlogin'):
        return sshd.get_values('permitrootlogin')[0] == 'yes'


@condition(ListUnits)
def is_sshd_running(units):
    """ Return True if ``sshd.service`` is running.
    """
    return units.is_running('sshd.service') or units.is_running('ssh.service')


@condition([RedhatRelease, LsbRelease])
def get_release(redhat_release, lsb_release):
    """Get the product name.

    RedhatRelease: Data from /etc/redhat-release
    LsbRelease: Data from /etc/lsb-release
    """
    if redhat_release:
        return redhat_release.product
    if lsb_release:
        return lsb_release.product


@rule(check_permit_root_login, is_sshd_running, get_release)
def report(root_login, sshd, release):
    if sshd and release:
        if root_login:
            # The issue is detected.
            return make_fail('SSHD_ROOT_LOGIN_PERMITTED',
                             os=release)
        # The issue does not exist.
        return make_pass('SSHD_ROOT_LOGIN_DISABLED',
                         os=release)
