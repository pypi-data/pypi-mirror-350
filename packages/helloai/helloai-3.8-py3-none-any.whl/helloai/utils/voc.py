import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

__all__ = ["Voc"]


class Voc:
    @classmethod
    def read(cls, path):
        value = None
        tree = ET.parse(path)
        root = tree.getroot()
        for member in root.findall("object"):
            bbx = member.find("bndbox")
            xmin = int(bbx.find("xmin").text)
            ymin = int(bbx.find("ymin").text)
            xmax = int(bbx.find("xmax").text)
            ymax = int(bbx.find("ymax").text)
            label = member.find("name").text

            value = (
                int(root.find("size")[0].text),
                int(root.find("size")[1].text),
                label,
                xmin,
                ymin,
                xmax,
                ymax,
            )
        return value

    @classmethod
    def to_csv(cls, path, name):
        xml_list = []
        for xml_file in glob.glob(path + "/*.xml"):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for member in root.findall("object"):
                bbx = member.find("bndbox")
                xmin = int(bbx.find("xmin").text)
                ymin = int(bbx.find("ymin").text)
                xmax = int(bbx.find("xmax").text)
                ymax = int(bbx.find("ymax").text)
                label = member.find("name").text

                value = (
                    root.find("filename").text,
                    int(root.find("size")[0].text),
                    int(root.find("size")[1].text),
                    label,
                    xmin,
                    ymin,
                    xmax,
                    ymax,
                )
                xml_list.append(value)

        column_name = [
            "filename",
            "width",
            "height",
            "class",
            "xmin",
            "ymin",
            "xmax",
            "ymax",
        ]
        xml_df = pd.DataFrame(xml_list, columns=column_name)
        xml_df.to_csv("labels_{}.csv".format(name), index=None)
        return xml_df.to_numpy()

