#!/usr/bin/env python

import os
from distutils.core import setup
from distutils.command.build_scripts import build_scripts

class build_scripts_strip_py(build_scripts):
    def run(self):
        self.mkpath(self.build_dir)
        for script in self.scripts:
            path = os.path.join(self.build_dir, script)
            # Only strip the extension and change the permissions on posix.
            if os.name == 'posix':
                os.chmod(script, 0755)
                if script.endswith('.py'):
                    path = path[:-3]
            self.copy_file(script, path)

setup(name='wavlooper',
      version='1.0',
      description="Loop a WAV file with optional fadeout.",
      author="Ryan \"ZDBioHazard\" Turner",
      author_email='zdbiohazard2@gmail.com',
      url='https://github.com/ZDBioHazard/wavlooper/',
      scripts=['wavlooper.py'],
      cmdclass={"build_scripts": build_scripts_strip_py})
