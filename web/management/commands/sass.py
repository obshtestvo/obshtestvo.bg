import os
import subprocess
import fnmatch
from optparse import make_option

from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings
from django.contrib.staticfiles import finders

from ...static_helpers import SassSimpleFilter

class Command(NoArgsCommand):
    help = "Compress content outside of the request/response cycle"
    option_list = NoArgsCommand.option_list + (
        make_option('--watch',
            action='store_true',
            dest='watch',
            default=False,
            help='Runs sass in watch mode'),
        )

    def handle(self, watch, *args, **kwargs):
        sass_binary = settings.SASS_BINARY_PATH
        if sass_binary is None or not os.path.exists(sass_binary):
            raise CommandError( "Please set path to `sass` binary - settings.SASS_BINARY_PATH")

        sass_pairs = []
        for finder in finders.get_finders():
            for relative_filepath, storage in finder.list([]):
                filepath = os.path.join(storage.location, relative_filepath)
                if fnmatch.fnmatch(os.path.basename(filepath), '[!_]*.scss'):
                    cachefilename = SassSimpleFilter.get_cachefilename(filepath)
                    sass_pairs.append(filepath + ':' + cachefilename)

        command = [sass_binary, '--compass']
        if watch:
            command.append('--watch')
        command = command + sass_pairs
        subprocess.Popen(command, stderr=self.stderr, stdout=self.stdout).wait()