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
import struct
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
opts.add_argument('-f', '--fade', type=float, default=15.0,
                  help="Looped fade out in seconds (defaults to 15s)")
opts = opts.parse_args()

# Get the files open.
file_in = wave.open(opts.file_in, 'r')
file_out = wave.open(opts.file_out, 'w')
file_out.setparams(file_in.getparams())
frame_count = file_in.getnframes()

# Collect some information.
if opts.loop_end is None:
    opts.loop_end = frame_count

# Read and write the start of the audio.
file_out.writeframes(file_in.readframes(opts.loop_start))

# Read the loop and write as many loops as requested.
audio_loop = file_in.readframes(opts.loop_end-opts.loop_start)
for i in range(opts.loops):
    file_out.writeframes(audio_loop)

# Create a looped fadeout if there is no end section.
if opts.loop_end == frame_count:
    audio_end = bytes()  # Hijack the end section since we won't be using it.
    chans = file_in.getnchannels()
    width = file_in.getsampwidth()
    pack = "<%d%c" % (chans, [None, None, 'h'][width])
    fade_len = min(opts.loop_end - opts.loop_start,
                   opts.fade * file_in.getframerate())

    for sidx in range(int(fade_len)):
        sample = list(struct.unpack_from(pack, audio_loop, sidx*chans*width))

        # Attenuate each channel.
        for cidx in range(len(sample)):
            sample[cidx] *= max(0, (1.0 - (sidx / float(fade_len))))
        audio_end += struct.pack(pack, *sample)

    file_out.writeframes(audio_end)
else:
    # Read and write the end.
    file_out.writeframes(file_in.readframes(frame_count-opts.loop_end))

file_in.close()
file_out.close()
