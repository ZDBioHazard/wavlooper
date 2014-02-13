#!/usr/bin/env python

from distutils.core import setup
from distutils.command.build_scripts import build_scripts

class build_scripts_strip_py(build_scripts):
    def run(self):
        # Process the files list, stripping '.py' from script names.
        new_list = []
        for script in self.scripts:
            if script.endswith('.py'):
                self.copy_file(script, script[:-3])
                script = script[:-3]
            new_list.append(script)
        # Pass the processed list to the original build_scripts.run()
        self.scripts = new_list
        build_scripts.run(self)

setup(name='wavlooper',
      version='1.0',
      description="Loop a WAV file with optional fadeout.",
      author="Ryan \"ZDBioHazard\" Turner",
      author_email='zdbiohazard2@gmail.com',
      url='https://github.com/ZDBioHazard/wavlooper/',
      scripts=['wavlooper.py'],
      cmdclass={"build_scripts": build_scripts_strip_py})
