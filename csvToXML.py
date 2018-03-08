import csv
import oci
import argparse
from multiprocessing import Process
from glob import glob


if __name__ == "__main__":

    description = "\n".join(["This utility is meant to take csv files in COCO format to Pascal VOC annotations"])

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(dest='labelSource',
                        help="Name of label.csv")
    parser.add_argument(dest='labelDestinationDirectory',
                        help="Path to local directory with convertedfiles")
    args = parser.parse_args()


f = open(args.labelSource)
csv_f = csv.reader(f)
data = []

for row in csv_f:
    data.append(row)
f.close()

print(data[1:])


def convert_row(row):
    return """
<annotation>
    <folder>images</folder>
    <filename>%s</filename>
    <object>
        <size>
            <width>%s</width>
            <height>%s</height>
            <depth>1</depth>
        </size>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>Unspecified</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%s</xmin>
            <ymin>%s</ymin>
            <xmax>%s</xmax>
            <ymax>%s</ymax>
        </bndbox>
    </object>
</annotation>""" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

# print ('\n'.join([convert_row(row) for row in data[1:]]))
for row in data[1:]:
    newfile = row[0] + '.xml'
    with open(args.labelDestinationDirectory + '/' + newfile, 'w') as file:
        file.write(convert_row(row))


