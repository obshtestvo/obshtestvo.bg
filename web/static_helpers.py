import os
import codecs
import hashlib
import subprocess

from django.conf import settings
from compressor.filters import CompilerFilter

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
        if self.infile is None and self.filename is None and "{infile}" in self.command:
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
