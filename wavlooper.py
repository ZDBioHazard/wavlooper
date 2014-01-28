#!/usr/bin/env python
"""wavlooper
This script reads a wave file, splits it at given sample boundaries, and
produces a new wave file that has been looped the specified number of times.

For usage information run wavlooper with the '--help' argument.

COPYRIGHT INFO

By Ryan "BioHazard" Turner <zdbiohazard2@gmail.com>
Copyright (c) 2014

LICENSE

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>"""

import wave
import argparse


# Let's get that command line takes care of, first of all.
opts = argparse.ArgumentParser(description="Chop and loop a wav file")
opts.add_argument('file_in', type=unicode, metavar="input_file.wav",
                  help="Input file")
opts.add_argument('file_out', type=unicode, metavar="output_file.wav",
                  help="Output file")
opts.add_argument('loop_start', type=int,
                  help="Sample at the start of the loop")
opts.add_argument('loop_end', type=int, nargs='?', default=None,
                  help="Sample at the end of the loop (defaults to end)")
opts.add_argument('-l', '--loops', type=int, default=2,
                  help="Number of loop plays (defaults to 2)")
opts = opts.parse_args()

# Get the files open.
file_in = wave.open(opts.file_in, 'r')
file_out = wave.open(opts.file_out, 'w')
file_out.setparams(file_in.getparams())

# Collect some information.
if opts.loop_end is None:
    opts.loop_end = file_in.getnframes()

# Read in the audio we're going to need.
audio_start = file_in.readframes(opts.loop_start)
audio_loop = file_in.readframes(opts.loop_end-file_in.tell())
audio_end = file_in.readframes(file_in.getnframes()-file_in.tell())

# Write the start of the audio.
file_out.writeframes(audio_start)
del audio_start  # Save a bit of memory.

# Write as many loops as requested.
for i in range(opts.loops):
    file_out.writeframes(audio_loop)

# Write the end.
file_out.writeframes(audio_end)

file_in.close()
file_out.close()
