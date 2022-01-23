from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree as ET
from argparse import ArgumentParser
from xml.etree import ElementTree
from xml.dom import minidom
import os

# usage
# python add_annotations_to_xml.py -s D:\persons -d D:\CHECK_104_to_markup_people -cta="person"



def arguments():
    parser = ArgumentParser()
    parser.add_argument('-d', '--destination', help='Path to the xml files to wich will add objects', required=True)
    parser.add_argument('-s', '--source', help='Path to the xml files from which take objects', required=True)
    parser.add_argument('-cta', '--classes_to_add', help='Classes that need to be add Example dog,backpack,cat', required=True)
    return parser

def xml_annotation(folder=" ", filename=" ", path=" ", database='Unknown', w=0, h=0,
                   depth=0, segmented=0):
    top = Element('annotation')

    child_folder = SubElement(top, 'folder')
    child_folder.text = str(folder)

    child_filename = SubElement(top,'filename')
    child_filename.text = str(filename)

    child_path = SubElement(top, 'path')
    child_path.text = str(path)

    child_source = SubElement(top, 'source')
    db_child = SubElement(child_source, 'database')
    db_child.text = str(database)

    # size block
    size_child = SubElement(top, 'size')

    width = SubElement(size_child, 'width')
    width.text = str(w)

    height = SubElement(size_child, 'height')
    height.text = str(h)

    child_depth = SubElement(size_child, 'depth')
    child_depth.text = str(depth)

    segmented_child = SubElement(top, 'segmented')
    segmented_child.text = str(segmented)

    return top


def xml_add_object(top, name='Unknown', pose='Unspecified',
                   truncated=0, difficult=0, prob='Unspecified',
                   xmin=0, ymin=0, xmax=0, ymax=0):

    child_object = SubElement(top, 'object')

    child_name = SubElement(child_object, 'name')
    child_name.text = str(name)

    child_name = SubElement(child_object, 'prob')
    child_name.text = str(prob)

    child_pose = SubElement(child_object, 'pose')
    child_pose.text = str(pose)

    child_truncated = SubElement(child_object, 'truncated')
    child_truncated.text = str(truncated)

    child_difficult = SubElement(child_object, 'difficult')
    child_difficult.text = str(difficult)

    # bndbox block
    child_bnd = SubElement(child_object, 'bndbox')

    child_xmin = SubElement(child_bnd, 'xmin')
    child_xmin.text = str(xmin)
    child_ymin = SubElement(child_bnd, 'ymin')
    child_ymin.text = str(ymin)
    child_xmax = SubElement(child_bnd, 'xmax')
    child_xmax.text = str(xmax)
    child_ymax = SubElement(child_bnd, 'ymax')
    child_ymax.text = str(ymax)

    return top


def pretty_view(xml_entity):
    rough_string = ElementTree.tostring(xml_entity, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    
    return reparsed.toprettyxml(indent="  ")


if __name__ == '__main__':

    args = arguments().parse_args()

    destination_dir = args.destination
    source_dir = args.source

    cls_to_add = args.classes_to_add.split(sep=',')

    xml_objects = {}
    
    for file in os.listdir(source_dir):
        if file.endswith('xml'):
            
            tree = ET.parse(os.path.join(source_dir, file))
            root = tree.getroot()
            img_size = root.find("size")
            h, w, d = img_size
            
            db_bame = root.find("source").find("database").text
            
            img_w = w.text
            img_h = h.text
            depth = d.text

            objects = root.findall("object")
            for obj in objects:
                bnd_box = obj.find('bndbox')
                class_name = obj.find('name').text
                    
                xmin = int(round(float(bnd_box.find('xmin').text)))
                xmax = int(round(float(bnd_box.find('xmax').text)))
                ymin = int(round(float(bnd_box.find('ymin').text)))
                ymax = int(round(float(bnd_box.find('ymax').text)))

                if file in xml_objects.keys():
                    xml_objects[file]['objects'].append([class_name, xmin, xmax, ymin, ymax])
                else:
                    xml_objects[file] = {'objects': [], 'find': False}
                    xml_objects[file]['objects'].append([class_name, xmin, xmax, ymin, ymax])

    for path_, dirs, files in os.walk(destination_dir):
        for file in xml_objects.keys():
            if file in files:
                tree = ET.parse(os.path.join(path_, file))
                root = tree.getroot()
                save = False
                xml_objects[file]['find'] = True
                for obj in xml_objects[file]['objects']:
                    class_name, xmin, xmax, ymin, ymax = obj
                    if class_name in cls_to_add:
                        save = True
                        new_obj = xml_add_object(top=root, name=class_name, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
                        root = new_obj
                if save:
                    result_xml = pretty_view(root)
                    with open(os.path.join(path_, file), 'w+') as file:
                        file.write(str(result_xml))
    counter = 0
    for f in xml_objects.keys():
        if xml_objects[f]['find']:
            counter += 1
    print("Out of {} files {} were found and added".format(len(xml_objects.keys()), counter))