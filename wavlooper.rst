===========
 wavlooper
===========

------------------------
Chop and loop a WAV file
------------------------

:Manual section: 1

SYNOPSIS
========

| **wavlooper** [ *options* ] *input_file* *output_file* *loop_start* [ *loop_end* ]

DESCRIPTION
===========

Wavlooper takes a Microsoft PCM WAVE file, and creates a new file with an
intro, looped part repeated a specified number of times, and the outro.

Loop points are given in samples from the beginning of the file.

OPTIONS
=======

**-h**, **--help**
    Show help. Do nothing else.

**-l**, **--loops** *integer*
    (default: 2)
    Number of times to repeat the looped part. This includes the first loop.

**-f**, **--fade** *float*
    (default: 15)
    Number of seconds to fade out at the end.
    The fadeout takes place after the last iteration of looping, so the fade
    will be over the start part of the loop audio.

    If the specified fadeout is longer than the loop, the fadeout time will
    be scaled to the length of one loop. (so effectively the audio will loop
    *loops* + 1 times)

*input_file*
    PCM WAVE file to be read. *stdin* is not currently supported.

*output_file*
    PCM WAVE file to be written. *stdout* is not currently supported.

*loop_start* (*integer*)
    Start sample of the loop audio, from the start of the file.

*loop_end* (*integer*)
    End sample of the loop audio, from the start of the file. If specified and
    *loop_end* is not the last sample of the file, the audio data after this
    point will be appended to the end of the looped file, and **--fade** will
    be ignored.

BUGS
====

Only 16-bit signed PCM files are supported. It *should* fail gracefully with
unsupported input, but I'm sure there are exceptions. ;)
