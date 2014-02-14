#!/usr/bin/env python

from distutils import log
from distutils.core import setup
from distutils.command.build_scripts import build_scripts
from distutils.command.install_data import install_data

from docutils.core import publish_file
from docutils.writers import manpage


class install_data_man_one(install_data):
    def run(self):
        # Go through each "directory" entry.
        new_data_files = []
        for data in self.data_files:
            # Skip over files not destined for man1 directories.
            if not isinstance(data, tuple) or data[0] != 'share/man/man1':
                new_data.append(data)
                continue

            # Go through the files, and look for *.rst pages.
            new_list = []
            for entry in data[1]:
                # Only process *.rst files.
                if not entry.endswith('.rst'):
                    new_list.append(entry)
                    continue

                # Use docutils to convert the RST document to manpage 1 format.
                man = entry[:-4] + '.1'
                log.info("converting %s -> %s" % (entry, man))
                publish_file(source_path=entry, destination_path=man,
                             writer=manpage.Writer())
                new_list.append(man)

            new_data_files.append((data[0], new_list))
        # Pass the processed list to the original install_data.run()
        self.data_files = new_data_files
        install_data.run(self)


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
      license='GPL-3',
      description="Loop a WAV file with optional fadeout.",
      author="Ryan \"ZDBioHazard\" Turner",
      author_email='zdbiohazard2@gmail.com',
      url='https://github.com/ZDBioHazard/wavlooper/',
      scripts=['wavlooper.py'],
      data_files=[('share/man/man1', ['wavlooper.rst'])],
      cmdclass={"build_scripts": build_scripts_strip_py,
                "install_data": install_data_man_one})
