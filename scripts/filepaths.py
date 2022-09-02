import csv
import argparse
import re


# 20220707-box/1093688960/1093688960.wpi
PATTERN = re.compile(r".+/(?P<plate_name>.+)/(?P<image_file>.+)\.(wpi|ome\.xml|companion\.ome)")

parser = argparse.ArgumentParser(description="Build filepaths.tsv")
parser.add_argument("file", help="Annotations file")
parser.add_argument("filelist", help="List of image files")
args = parser.parse_args()

plates = []
plate_file_map = {}

# Compile a list of plate names
with open(args.file, mode='r', encoding='utf-8-sig') as input_file:
    csv_reader = csv.DictReader(input_file)
    for row in csv_reader:
        if not row["Plate"] in plates:
            plates.append(row["Plate"])

# Check the list of images files to find the corresponding "main" file to import
with open(args.filelist, mode='r') as input_file:
    for line in input_file.readlines():
        m = PATTERN.match(line.strip())
        if m:
            plate_file_map[m.group("plate_name")] = f"/uod/idr/filesets/idr0139-lawson-fascin/{line.strip()}"

# Print the tsv to std out
for plate in plates:
    print(f"{plate_file_map.get(plate, 'NA')}\t{plate}")
