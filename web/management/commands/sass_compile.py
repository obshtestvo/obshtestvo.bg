from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
from ...static_helpers import SassSimpleFilter
import subprocess

class Command(BaseCommand):
    args = '<path>'
    help = 'Compiles a specified (by absolute path) scss file css'

    def handle(self, *args, **kwargs):
        sass_binary = settings.SASS_BINARY_PATH
        if sass_binary is None or not os.path.exists(sass_binary):
            raise CommandError( "Please set path to `sass` binary - settings.SASS_BINARY_PATH")

        if len(args) == 0:
            raise CommandError("You haven't specified path")

        path = args[0]
        if not os.path.exists(path):
            raise CommandError("Sass file %s doesn't exist" % path)

        cachefilename = SassSimpleFilter.get_cachefilename(path)
        command = '%s --compass %s:%s' % (sass_binary, path, cachefilename)
        subprocess.Popen(command, shell=True, stderr=self.stderr)

