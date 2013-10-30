import argparse
import logging
import mimetypes
import os
import subprocess
from cvutils.helpers import verify_installed, ACCEPTED_IMAGE_MIMETYPES, EMPTY_VALUES

logging.basicConfig(level=logging.DEBUG, format="%(msg)s")

def createsample(image, args):
    logging.info("Processing %s..." % image)
    args_dict = {
        "bg" : args.bg,
        "num" : args.num,
        "bgcolor" : args.bgcolor,
        "bgthresh" : args.bgthresh,
        "inv" : args.inv,
        "randinv" : args.randinv,
        "maxidev" : args.maxidev,
        "maxxangle" : args.maxxangle,
        "maxyangle" : args.maxyangle,
        "maxzangle" : args.maxzangle,
        "show" : args.show,
        "width" : args.width,
        "height" : args.height,
        "info" : args.info
    }
    vector_filename = os.path.join(os.path.dirname(image), "%s.vec" % os.path.splitext(os.path.basename(image))[0])
    process_args = ['opencv_createsamples', '-img', image, "-vec", vector_filename]
    for k,v in args_dict.iteritems():
        if v not in EMPTY_VALUES:
            if isinstance(v, bool):
                if v:
                    process_args.append("-%s" % k)
            else:
                process_args.append("-%s" % k)
                process_args.append("%s" % v)
    #print ' '.join(process_args)
    subprocess.call(process_args)


def runner(args):

    positives = args.positives
    if not os.path.exists(positives): raise IOError("%s does not exist." % positives)

    # determine the positives source given (folder or file))
    if os.path.isabs(positives):
        positives = os.path.abspath(positives)

    if os.path.isdir(positives):
        for obj in os.listdir(positives):

            # verify the file object is valid
            obj_abspath = os.path.join(positives, obj)
            guessed = mimetypes.guess_type(obj_abspath)
            if guessed[0] not in ACCEPTED_IMAGE_MIMETYPES: continue

            # process image
            createsample(obj_abspath, args)
    elif os.path.isfile(positives):

        guessed = mimetypes.guess_type(positives)[0]
        if guessed in ACCEPTED_IMAGE_MIMETYPES:
            createsample(positives, args)
        elif guessed == "text/plain":
            with open(positives, 'r') as positives_file:
                for line in positives_file.readlines():
                    createsample(line, args)
        else:
            raise ValueError("%s is an unsupported filetype (%s)" % (positives, guessed))


def main():

    ## verify that the required utilities are installed
    verify_installed("opencv_createsamples")


    parser = argparse.ArgumentParser(description="Allows creating samples in a folder in a batch automated way.")
    parser.add_argument('positives', help="Path to folder containing source images, "
                                          "or file listing paths to source images."
                                          "Source object image(s) - (e.g., a company logo).")
    parser.add_argument('--bg', help='Background description file; contains a list of images which are used as a background for randomly distorted versions of the object.')
    parser.add_argument('--num', help='Number of positive samples to generate.')
    parser.add_argument('--bgcolor', help='Background color (currently grayscale images are assumed);'
                                            'The background color denotes the transparent color.'
                                            'Since there might be compression artifacts, '
                                            'the amount of color tolerance can be specified by -bgthresh.'
                                            'All pixels withing bgcolor-bgthresh and bgcolor+bgthresh '
                                            'range are interpreted as transparent.')
    parser.add_argument('--bgthresh', help='background_color_threshold')
    parser.add_argument('--inv', help='If specified, colors will be inverted.')
    parser.add_argument('--randinv', help='If specified, colors will be inverted randomly.')
    parser.add_argument('--maxidev', help='Maximal intensity deviation of pixels in foreground samples.')
    parser.add_argument('--maxxangle', help='max_x_rotation_angle')
    parser.add_argument('--maxyangle', help='max_y_rotation_angle')
    parser.add_argument('--maxzangle', help='max_z_rotation_angle')
    parser.add_argument('--show', help='Useful debugging option. If specified, each sample will be shown. '
                                       'Pressing Esc will continue the samples creation process without.',
                        action="store_true")
    parser.add_argument('--width', help='Width (in pixels) of the output samples.')
    parser.add_argument('--height', help='Height (in pixels) of the output samples.')
    parser.add_argument('---info', help='Description file of marked up images collection.')
    args = parser.parse_args()

    runner(args)

if __name__ == "__main__":
    try:
        main()
    except Exception, e:
        logging.error("ERROR: %s" % e.message)