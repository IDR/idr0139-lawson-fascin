import re
import subprocess
from ome_model.experimental import Plate, Image, create_companion

# Create companion files for screenC

# 1093670866WT2_A10_F01_T002_C1_Z01.tif
pat = re.compile(r".+_(?P<row>\D{1})(?P<col>\d{1,2})_F(?P<field>\d{2})_T(?P<t>\d{3})_C(?P<c>\d{1})_Z(?P<z>\d{2})\.tif")

plate_name = '1093670866'
file_list = '1093670866_files.txt'
order = "XYCZT"
img_x = 1392
img_y = 1040
pix_type = "uint8"


files = []
with open(file_list, 'r') as read:
    for line in read.readlines():
        files.append(line.strip())


# Get total numbers
n_rows = set()
n_cols = set()
n_fields = set()
n_z = set()
n_t = set()
n_c = set()
for file in files:
    m = pat.match(file).groupdict()
    n_rows.add(m['row'])
    n_cols.add(int(m['col']))
    n_fields.add(int(m['field']))
    n_z.add(int(m['z']))
    n_t.add(int(m['t']))
    n_c.add(int(m['c']))
n_rows = len(n_rows)
n_cols = len(n_cols)
n_fields = len(n_fields)
n_z = len(n_z)
n_t = len(n_t)
n_c = len(n_c)


# assemble images (key: wellrow|wellcol|field)
images = {}
for file in files:
    m = pat.match(file).groupdict()
    key = f"{m['row']}|{m['col']}|{m['field']}"
    if not key in images:
        images[key] = Image(key, img_x, img_y, n_z, n_c, n_t, order=order, type=pix_type)
        for i in range(0, n_c):
            images[key].add_channel(samplesPerPixel=1)
    images[key].add_plane(c=int(m['c']), z=int(m['z'])-1, t=int(m['t']))
    images[key].add_tiff(file, c=int(m['c']), z=int(m['z'])-1, t=int(m['t']), planeCount=1)


# assemble plate
plate = Plate(plate_name, n_rows, n_cols)
wells = {}
row_indices = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for well_pos, image in images.items():
    row = int(row_indices.index(well_pos.split("|")[0]))
    col = int(well_pos.split("|")[1])-1
    field = int(well_pos.split("|")[2])-1
    key = f"{row}|{col}"
    if not key in wells:
        wells[key] = plate.add_well(row, col)
    wells[key].add_wellsample(field, image)


# write companion file
companion_file = "{}.companion.ome".format(plate_name)
create_companion(plates=[plate], out=companion_file)


# Indent XML for readability
proc = subprocess.Popen(
    ['xmllint', '--format', '-o', companion_file, companion_file],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE)
(output, error_output) = proc.communicate()
