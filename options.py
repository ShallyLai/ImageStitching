import argparse

parser = argparse.ArgumentParser(description = 'Image Stitching')

parser.add_argument('--src_dir', type = str, default = './data/DaAn_1', help = 'the directory where the input images are stored.')
parser.add_argument('--out_dir', type = str, default = './output', help = 'the directory where the outputs will be stored.')
parser.add_argument('--pano_file', type = str, default = 'pano.txt', help = 'the file name of pano file.')

parser.add_argument('-t', default=0.01, type=float, help="threshold in harris corner detector.")

parser.add_argument('--plot', action='store_true', help = 'plot features and orientation.')
parser.add_argument('--no-plot', dest='plot', action='store_false', help = "don't plot features and orientation.")
parser.set_defaults(plot=True)

args = parser.parse_args()