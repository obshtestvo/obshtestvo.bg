import os
import codecs
import hashlib
import subprocess

from django.conf import settings
from compressor.filters import CompilerFilter
from compressor.exceptions import FilterError

class SassFilter(CompilerFilter):
    command = "{binary} {compile_args}{watch_args} {infile}:{outfile}"
    type = 'css'
    options = (
        ("binary", settings.SASS_BINARY_PATH),
        ("compile_args", " --compass --sourcemap --cache-location=/var/tmp"),
        ("watch_args", " --watch --compass --cache-location=/var/tmp --sourcemap --poll"),
    )

    def __init__(self, content, attrs, *args, **kwargs):
        super(SassFilter, self).__init__(content, command=self.command, *args, **kwargs)

    def input(self, **kwargs):
        sass_binary = settings.SASS_BINARY_PATH
        if sass_binary is None or not os.path.exists(sass_binary):
            raise FilterError( "Please set path to `sass` binary - settings.SASS_BINARY_PATH")
        input_is_not_file = self.infile is None and self.filename is None and "{infile}" in self.command
        if input_is_not_file or not settings.DEBUG:
            self.options = dict(self.options)
            self.options["watch_args"] = ''
            return super(SassFilter, self).input(**kwargs)

        cachefilename = self.get_cachefilename()
        is_sass_watching = not subprocess.call([settings.IS_PROCESS_RUNNING_SCRIPT, cachefilename])
        if not is_sass_watching:
            options = dict(self.options)
            options["compile_args"] = ''
            options["outfile"] = cachefilename
            options["infile"] = self.filename
            command = self.command.format(**options)
            subprocess.Popen(command, shell=True, stderr=self.stderr, cwd=os.path.dirname(self.filename))

        cache = codecs.open(cachefilename, "r", "utf-8")
        return cache.read()

    def get_cachefilename(self):
        cached_name = hashlib.md5(self.filename).hexdigest()
        return os.path.join(settings.COMPRESS_ROOT, settings.COMPRESS_OUTPUT_DIR, cached_name + '.css')


class SassSimpleFilter(CompilerFilter):

    def input(self, **kwargs):
        sass_binary = settings.SASS_BINARY_PATH
        if sass_binary is None or not os.path.exists(sass_binary):
            raise FilterError( "Please set path to `sass` binary - settings.SASS_BINARY_PATH")
        input_is_not_file = self.infile is None and self.filename is None and "{infile}" in self.command
        if input_is_not_file:
            raise FilterError(type(self).__name__ + " can't compile embedded SASS or SCSS. Please use another compiler filter.")

        cachefilename = self.get_cachefilename(self.filename)
        if not os.path.exists(cachefilename):
            raise FilterError("Compiled CSS can't be found: %s" % cachefilename)

        cache = codecs.open(cachefilename, "r", "utf-8")
        return cache.read()

    @staticmethod
    def get_cachefilename(filename):
        cached_name = hashlib.md5(filename).hexdigest()
        return os.path.join(settings.COMPRESS_ROOT, settings.COMPRESS_OUTPUT_DIR, cached_name + '.css')
