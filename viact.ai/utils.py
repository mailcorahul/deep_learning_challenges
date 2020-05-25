def _object_xml(box):

    for a_key in box:
        name = a_key
        xmin = box[a_key]['xmin']
        xmax = box[a_key]['xmax']
        ymin = box[a_key]['ymin']
        ymax = box[a_key]['ymax']

    box_xml = "\t<object>\n \
                <name>{}</name>\n \
                <pose>Frontal</pose>\n \
                <truncated>0</truncated>\n \
                <difficult>0</difficult>\n \
                <bndbox>\n \
                        \t<xmin>{}</xmin>\n \
                        \t<ymin>{}</ymin>\n \
                        \t<xmax>{}</xmax>\n \
                        \t<ymax>{}</ymax>\n \
                </bndbox>\n \
        </object>\n".format(name, xmin, ymin, xmax, ymax)

    return box_xml


def _annotation_xml(bboxes, img_name, dims):

    width, height, channels = dims
    annotation_start = "<annotation>\n \
        <folder>fashion</folder>\n \
        <filename>{}</filename>\n \
        <source>\n \
                \t<database>fashion</database>\n \
                \t<annotation>fashion</annotation>\n \
                \t<image>na</image>\n \
                \t<flickrid>na</flickrid>\n \
        </source>\n \
        <owner>\n \
                \t<flickrid>na</flickrid>\n \
                \t<name>na</name>\n \
        </owner>\n \
        <size>\n \
                \t<width>{}</width>\n \
                \t<height>{}</height>\n \
                \t<depth>{}</depth>\n \
        </size>\n \
        <segmented>0</segmented>\n".format(img_name, width, height, channels)

    for a_box in bboxes:
        box_xml = _object_xml(a_box)
        annotation_start = annotation_start + box_xml

    annotation_end = "\n</annotation>"
    annotation_xml = annotation_start + annotation_end

    return annotation_xml