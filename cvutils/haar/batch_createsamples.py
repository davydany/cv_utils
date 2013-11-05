import argparse
import cv
import logging
import mimetypes
import os
import subprocess
from cvutils.helpers import verify_installed, ACCEPTED_IMAGE_MIMETYPES, EMPTY_VALUES

logging.basicConfig(level=logging.DEBUG, format="%(msg)s")

clicked = False

def createsample(processfile, processfile_type, args, sample_count=None):
    logging.info("Processing %s..." % processfile)
    args_dict = {
        "bg" : args.bg,
        "num" : sample_count if sample_count else args.num,
        "bgcolor" : args.bgcolor,
        "bgthresh" : args.bgthresh,
        "inv" : args.inv,
        "randinv" : args.randinv,
        "maxidev" : args.maxidev,
        "maxxangle" : args.maxxangle,
        "maxyangle" : args.maxyangle,
        "maxzangle" : args.maxzangle,
        "show" : args.show,
        "w" : args.width or 24,
        "h" : args.height or 24
    }

    # determine output vector filename
    vector_filename = os.path.join(os.path.dirname(processfile),
                                   "%s.vec" % os.path.splitext(os.path.basename(processfile))[0])

    # determine command to execute
    process_args = ['opencv_createsamples', '-vec', vector_filename]
    if processfile_type == "info":
        process_args.append('-info')
        process_args.append(processfile)
    elif processfile_type == "image":
        process_args.append('-img')
        process_args.append(processfile)

    for k,v in args_dict.iteritems():
        if v not in EMPTY_VALUES:
            if isinstance(v, bool):
                if v:
                    process_args.append("-%s" % k)
            else:
                process_args.append("-%s" % k)
                process_args.append("%s" % v)

    print " ".join(process_args)
    subprocess.call(process_args)

class InfoFileCreator(object):

    def __init__(self, process_filepath=None, process_folderpath=None):

        # verify inputs
        if not (process_filepath or process_folderpath):
            raise ValueError("Info file cannot be created since source was not provided.")

        # determine parent folder
        parent_folder = os.path.dirname(process_filepath or process_folderpath)
        if not os.path.isabs(parent_folder): parent_folder = os.path.abspath(parent_folder)


        self.__abs_infofile_path = os.path.join(parent_folder, 'positives.dat')
        self.files_to_process = []

        # determine files to process if given as a file
        if process_filepath:
            with open(process_filepath, 'r') as process_file:
                for img_path in process_file.readlines():
                    img_path = img_path.strip()
                    img_filepath = img_path
                    if not os.path.isabs(img_filepath): img_filepath = os.path.join(parent_folder, img_filepath)
                    if not os.path.exists(img_filepath): img_filepath = os.path.abspath(img_path)
                    if not os.path.exists(img_filepath): img_filepath = img_path
                    self.files_to_process.append(img_filepath)

        # determine files to process if a folder path was given
        if process_folderpath:
            for img_filename in os.listdir(process_folderpath):
                img_filepath = os.path.join(process_folderpath, img_filename)
                guessed_mimetype = mimetypes.guess_type(img_filepath)
                if guessed_mimetype[0] not in ACCEPTED_IMAGE_MIMETYPES: continue
                self.files_to_process.append(img_filepath)

        self.draw_started = False       # used to remember the state of clicking
        self.original_img = None        # original image that will be processed (one at a time)
        self.current_selection = [
            0, # init x
            0, # init y
            0, # width
            0  # height
        ]

        self.current_processed_img_filepath = None # path of the current processed file
        self.img_selection = {}
        self.win_title = "Select the objects to detect"
        self.sample_counter = 0



    def write_selections_to_diks(self):


        with open(self.__abs_infofile_path, 'wb') as infofile:
            for img_filepath, selections in self.img_selection.iteritems():

                if len(selections) == 0:
                    continue

                selection_string = ""
                for selection in selections:
                    s = [str(i) for i in selection]
                    selection_string = selection_string + "  " + " ".join(s)
                self.sample_counter += len(selections)

                pathsplit = img_filepath.split("/")
                relpath = "%s/%s" % (pathsplit[-2], pathsplit[-1])
                infofile.write("%s  %d  %s\n" % (relpath, len(selections), selection_string))

    def process(self):
        """
        Show dialog to user to process each
        """

        for img_filepath in self.files_to_process:

            self.current_selection = [0, 0, 0, 0]
            cv.NamedWindow(self.win_title)
            cv.SetMouseCallback(self.win_title, self.mouse_callback)
            img = cv.LoadImage(img_filepath)
            self.original_img = img
            self.current_processed_img_filepath = img_filepath
            cv.ShowImage(self.win_title, img)
            while True:
                k = cv.WaitKey(100)
                if k == 13: # ENTER
                    break
                if k == 27: # ESC
                    raise KeyboardInterrupt("User pressed ESC.")
        self.write_selections_to_diks()



    def mouse_callback(self, event, x, y, *args, **kwargs):

        if event == 1: # mouse, left-click
            self.draw_started = not self.draw_started

            if self.draw_started: # start drawing
                self.current_selection[0] = x
                self.current_selection[1] = y
            else: # end drawing
                if (x < self.current_selection[0]) or (y < self.current_selection[1]):
                    self.draw_started = not self.draw_started
                    return

                self.current_selection[2] = x - self.current_selection[0]
                self.current_selection[3] = y - self.current_selection[1]

                if self.current_processed_img_filepath not in self.img_selection.keys():
                    self.img_selection[self.current_processed_img_filepath] = []

                self.img_selection[self.current_processed_img_filepath].append(
                    (self.current_selection[0],
                     self.current_selection[1],
                     self.current_selection[2],
                     self.current_selection[3])
                )

                print self.current_processed_img_filepath
                print "Saved Current Selection: %s" % str(self.current_selection)
                self.current_selection = [0, 0, 0, 0]
        elif event == 0:
            img = cv.LoadImage(self.current_processed_img_filepath)

            # draw cross hairs
            width, height = cv.GetSize(img)
            vert_pt1 = (x, 0)
            vert_pt2 = (x, height)
            hori_pt1 = (0, y)
            hori_pt2 = (width, y)
            cv.Line(img, vert_pt1, vert_pt2, cv.RGB(0, 255, 0), thickness=2)
            cv.Line(img, hori_pt1, hori_pt2, cv.RGB(0, 255, 0), thickness=2)
            cv.ShowImage(self.win_title, img)

            if self.draw_started:

                pt1 = (self.current_selection[0], self.current_selection[1])
                pt2 = (x, y)

                cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), thickness=3)
                cv.ShowImage(self.win_title, img)






    @property
    def sample_count(self):
        return self.sample_counter


    @property
    def information_file(self):
        return self.__abs_infofile_path

def create_info_file(process_filepath=None, process_folderpath=None):

    info_filecreator = InfoFileCreator(process_filepath=process_filepath, process_folderpath=process_folderpath)
    info_filecreator.process()
    logging.info("Information file: %s" % info_filecreator.information_file)
    return (info_filecreator.information_file, info_filecreator.sample_count)




def runner(args):

    positives = args.positives
    if not os.path.exists(positives): raise IOError("%s does not exist." % positives)

    # determine the positives source given (folder or file))
    if os.path.isabs(positives):
        positives = os.path.abspath(positives)

    if os.path.isdir(positives):

        infofile, sample_count = create_info_file(process_folderpath=positives)
        createsample(processfile=infofile, processfile_type='info', args=args, sample_count=sample_count)


    elif os.path.isfile(positives):

        guessed = mimetypes.guess_type(positives)[0]
        if guessed in ACCEPTED_IMAGE_MIMETYPES:
            createsample(processfile=positives, processfile_type='image', args=args)
        elif guessed == "text/plain":
            infofile, sample_count = create_info_file(process_filepath=positives)
            createsample(processfile=infofile, processfile_type='info', args=args, sample_count=sample_count)
        else:
            raise ValueError("%s is an unsupported filetype (%s)" % (positives, guessed))


def main():

    ## verify that the required utilities are installed
    verify_installed("opencv_createsamples")


    parser = argparse.ArgumentParser(prog='dcv_createsamples',
                                     description="As a wrapper for opencv_createsamples, "
                                                 "this utility allows creating samples in a folder "
                                                 "in a batch automated way.")
    parser.add_argument('positives', help="Path to folder containing source images, "
                                          "or file listing paths to source images."
                                          "Source object image(s) - (e.g., a company logo).")
    parser.add_argument('--bg', help='Background description file; contains a list of images which are used as a background for randomly distorted versions of the object.')
    parser.add_argument('--num', help='Number of positive samples to generate.', default=1000)
    parser.add_argument('--bgcolor', help='Background color (currently grayscale images are assumed);'
                                            'The background color denotes the transparent color.'
                                            'Since there might be compression artifacts, '
                                            'the amount of color tolerance can be specified by -bgthresh.'
                                            'All pixels withing bgcolor-bgthresh and bgcolor+bgthresh '
                                            'range are interpreted as transparent.')
    parser.add_argument('--bgthresh', help='background_color_threshold', default=80)
    parser.add_argument('--inv', help='If specified, colors will be inverted.', action='store_true')
    parser.add_argument('--randinv', help='If specified, colors will be inverted randomly.', action='store_true')
    parser.add_argument('--maxidev', help='Maximal intensity deviation of pixels in foreground samples.', default=40)
    parser.add_argument('--maxxangle', help='max_x_rotation_angle', default=1.1)
    parser.add_argument('--maxyangle', help='max_y_rotation_angle', default=1.1)
    parser.add_argument('--maxzangle', help='max_z_rotation_angle', default=0.5)
    parser.add_argument('--show', help='Useful debugging option. If specified, each sample will be shown. '
                                       'Pressing Esc will continue the samples creation process without.',
                        action="store_true")
    parser.add_argument('--width', help='Width (in pixels) of the output samples.', default=24)
    parser.add_argument('--height', help='Height (in pixels) of the output samples.', default=24)
    args = parser.parse_args()

    runner(args)

if __name__ == "__main__":
    try:
        main()
    except Exception, e:
        logging.exception("ERROR: %s" % e.message)