import logging
from optparse import make_option

from django.conf import settings
from django.core.management.base import NoArgsCommand

from smsgateway.tasks import send_smses

LOCK_WAIT_TIMEOUT = getattr(settings, "SMSES_LOCK_WAIT_TIMEOUT", -1)

logger = logging.getLogger(__name__)

class Command(NoArgsCommand):
    help = 'Send SMSes in the queue. Defer the failed ones. Pass --send-deferred to retry those.'

    option_list = NoArgsCommand.option_list + (
        make_option(
            '--send-deferred',
            dest='send_deferred',
            action='store_true',
            help='Whether to send the deferred smses. Default is all non-deferred.'
        ),
        make_option(
            '--backend',
            dest='backend',
            action='store',
            help='Whether to use a certain backend.'
        ),
    )

    def handle_noargs(self, **options):
        send_smses(options['send_deferred'], options['backend'])
