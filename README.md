cv_utils
========

Scripts that help make working with OpenCV a lot easier.

Requires
--------

OpenCV Installed

Utilities
---------

###dcv_createsamples

As a wrapper for opencv_createsamples, this utility allows creating samples in
a folder in a batch automated way.

    positional arguments:
    positives             Path to folder containing source images, or file
                          listing paths to source images.Source object image(s)
                          - (e.g., a company logo).

    optional arguments:
    -h, --help            show this help message and exit
    --bg BG               Background description file; contains a list of images
                          which are used as a background for randomly distorted
                          versions of the object.
    --num NUM             Number of positive samples to generate.
    --bgcolor BGCOLOR     Background color (currently grayscale images are
                          assumed);The background color denotes the transparent
                          color.Since there might be compression artifacts, the
                          amount of color tolerance can be specified by
                          -bgthresh.All pixels withing bgcolor-bgthresh and
                          bgcolor+bgthresh range are interpreted as transparent.
    --bgthresh BGTHRESH   background_color_threshold
    --inv                 If specified, colors will be inverted.
    --randinv             If specified, colors will be inverted randomly.
    --maxidev MAXIDEV     Maximal intensity deviation of pixels in foreground
                          samples.
    --maxxangle MAXXANGLE
                          max_x_rotation_angle
    --maxyangle MAXYANGLE
                          max_y_rotation_angle
    --maxzangle MAXZANGLE
                          max_z_rotation_angle
    --show                Useful debugging option. If specified, each sample
                          will be shown. Pressing Esc will continue the samples
                          creation process without.
    --width WIDTH         Width (in pixels) of the output samples.
    --height HEIGHT       Height (in pixels) of the output samples.
    ---info INFO          Description file of marked up images collection.

