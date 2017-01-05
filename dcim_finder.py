#===============================================================================
# DCIM Finder
# 
# Finds most personal photos on a hard drive and copies to dest_dir
#===============================================================================
import os
import sys
import re
import shutil
import getopt
import cv2

src_dir = ''
dest_dir = ''
verbose = False
match_all_images = False
use_min_size = False
min_size = 0
face_detect = False
pedestrian_detect = False
casc_classifier = "haarcascade_frontalface_alt.xml"
faces_directory = "faces"

def usage(arg):
    print "DCIM Finder: "
    print "Finds most personal photo files recursively starting at source_dir,"
    print "and copies them to dest_dir."
    print
    print "Usage: python %s -i <source_dir> -o <dest_dir> [-hvasfp]" % arg
    print " -h: this usage screen"
    print " -v: be verbose"
    print " -a: match all image files"
    print " -s: minimum file size in KB"
    print " -f: perform facial detection"
    print " -p: perform HoG pedestrian detection (not implemented yet)"
    print
    print "e.g.:"
    print "python dcim_finder.py -i test -o test1 -s 200 -v"
    sys.exit(1)

def face_detect(image,img_name):
    cascade = cv2.CascadeClassifier(casc_classifier)
    img = cv2.imread(image)
    rects = cascade.detectMultiScale(image,1.3,4,cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))
    if len(rects) == 0:
        return False

    rects[:, 2:] += rects[:, :2]

    # highlight the faces in the image
    for x1,y1,x2,y2 in rects:
        cv2.rectangle(image,(x1,y1),(x2,y2),(127,255,0),2)

    cv2.imwrite("%s/%s-facedetected" % (faces_directory,image_name),image)
    return True

try:
    opts, args = getopt.getopt(sys.argv[1:],"fpahvsi:o:")
except getopt.GetoptError:
    usage(sys.argv[0])
for opt, arg in opts:
    if opt == '-v':
        verbose = True
    elif opt == '-i':
        src_dir = arg
    elif opt == '-o':
        dest_dir = arg
    elif opt == '-s':
        use_min_size = True
        min_size = arg
    elif opt == '-a':
        match_all_images = True
    elif opt == '-f':
        face_detect = True
    elif opt == '-p':
        pedestrian_detect = True
    elif opt == '-h':
        usage(sys.argv[0])

fileList = []
fileSize = 0
folderCount = 0

# This tries to be an exhuastive list of different filenames for movies and pics
# created by digital camera's and phones. It is probably not complete.
smart_regexs = [ 
    r'dcp\d+\.jpg', # "dcp#####.jpg" - Kodak, range of 0 to 4000
    r'dsc\d+\.jpg', # "dsc#####.jpg" - Nikon, range of 0 to 4000
    r'dscn\d+\.jpg', # "dscn####.jpg" - Nikon, range of 0 to 4000
    r'mvc-\d+\.jpg', # "mvc-###.jpg"  - Sony Mavica
    r'mvc\d+\.jpg', # "mvc#####.jpg" - Sony Mavica
    r'P\d+\.jpg', # "P101####.jpg" - Olympus, Using default camera date of 101
    r'P[1-9a-c][0-3][0-9]\d+\.jpg', # "PMDD####.jpg" - Olympus, M is in hex from 1 to c, DD is 01-31
    r'IMAG\d+\.jpg', # "IMAG####.jpg" - RCA and Samsung
    r'1\d+-\d+\.jpg', # "1##-####.jpg" - Canon 1TH-TH##  thousands, hundreds
    r'1\d+-\d+_IMG\.jpg', # "1##-####_IMG.jpg" - Alternate Canon name. MUCH thanks to Donald
    r'_MG_\d+\.jpg', # "_MG_####.jpg" - Canon raw conversion.  Thanks to Ira
    r'dscf\d+\.jpg', # "dscf####.jpg" - Fuji Finepix
    r'pdrm\d+\.jpg', # "pdrm####.jpg" - Toshiba PDR
    r'IM\d+\.jpg', # "IM######.jpg" - HP Photosmart
    r'EX\d+\.jpg', # "EX######.jpg" - HP Photosmart timelapse?
    r'DC\d+[LSM]\.jpg', # "DC####S.jpg"  - Kodak DC-40,50,120 S is (L)arge, (M)eduim, (S)mall.  Thanks to Pholph
    r'pict\d+\.jpg', # "pict####.jpg" - Minolta Dimage.  Thanks to Bram
    r'\d+\.JPG', # "MMDD####.JPG" - Casio QV3000 and QV4000.  Thanks to Fabian
    r'IMGP\d+\.JPG', # "IMGP####.JPG" - Pentax Optio S. Thanks to Matthew
    r'PANA\d+\.JPG', # "PANA####.JPG" - Panasonic video camera stills.  Thanks to DeAnne
    #r'IMG_\d+_\d+\.JPG', # "IMG_YYYYMMDD_HHMMSS.JPG" - HTC Desire Z (AKA Tmobile G2).  Thanks to anonymously vociferous 
    r'Image\(\d+\)\.JPG', # "Image(##).JPG" - Nokia 3650 camera phone.  Thanks to usmanc
    r'DSCI\d+\.JPG', # "DSCI####.JPG" - Polaroid PDC2070.  Thanks to David
    r'\d+_\d+_\d+_[sno]\.jpg', # Facebook
    r'\d+_[0-9a-f]\.jpg', # Flickr 5041412002_bddfe9e576_b.jpg
    r'\d+_\d+_\d+_[a-z]\.jpg', # Instagram 12918537 _1719366751611008_1708400518_a.jpg
    r'image\s+\d+\.jpg', # iphone 6
    r'IMG(_\d+)+\.MOV', # iphone 4/5 movie
    r'IMG(_\d+)+\.PNG', # iphone screenshot
    r'IMG(_\d+)+\.jpg', # Android Picture
    r'\d+(_\d+)+\.jpg', # Android Picture
    r'VID(_\d+)+\.mp4', # Android video
    r'\d+(_\d+)+\.mp4', # Android video
    r'\d+_[A-F]\.jpg', # Samsung Galaxy S5
    r'\d{4}-\d{2}-\d+-\d+-\d+\.jpg', # motorola razr
    r'SNC\d+\.jpg', # sony i900
    r'IMG\d+-\d+-\d+\.jpg', # blackberry tour
    r'\d+(-\d+)+\.jpg', # Camera 360
]

match_all_regexs = [
    r'.*?\.jpg',
    r'.*?\.jpeg',
    r'.*?\.png',
    r'.*?\.tif',
    r'.*?\.tiff',
    r'.*?\.mov',
    r'.*?\.mp4',
    r'.*?\.3gp'
]

for root, subFolders, files in os.walk(src_dir):
    folderCount += len(subFolders)
    for f in files:
        if match_all_images:
            regexes = match_all_regexs
        else:
            regexes = smart_regexs
        for r in regexes:
            if re.search(r,f,re.M|re.I):
                fp = os.path.join(root,f)
                if verbose:
                    print(fp)
                fileSize = (fileSize + os.path.getsize(fp)) / 1024
                if use_min_size and fileSize <= min_size:
                    break
                fileList.append(fp)
                break

print
print("Total Size is {0} bytes".format(fileSize))
print("Total Files ", len(fileList))
print("Total Folders ", folderCount)
print

for f in fileList:
    print "Copying: %s " % f
    image_name = re.match(r'\/(.*?\.[a-z]{3,4})',f,r.M|r.I).group(1)
    shutil.copy2(f,dest_dir)
    if face_detect:
        face_detect(f,image_name)
