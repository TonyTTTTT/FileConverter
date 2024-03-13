import abc
import os.path
from pdf2image import convert_from_path


class Converter(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'convert') and
                callable(subclass.convert))

    @abc.abstractmethod
    def convert(self):
        raise NotImplementedError


class PDFConverter(Converter):
    def convert(self, pdf_path, save_path, pages, img_type):
        images = convert_from_path(pdf_path)

        for page in pages:
            images[page].save("{}/{}_{}.{}".format(save_path, os.path.split(pdf_path)[1].split('.')[0], page+1, img_type))


class IMGConverter(Converter):
    def convert(self, images_path):
        pass


if __name__ == '__main__':
    pdf_converter = PDFConverter()
    img_converter = IMGConverter()

    pdf_converter.convert(r'C:\Users\TonyTTTTT\Desktop\Guitar Sheet\i really want to stay at your house TAB.pdf'
                          , r'./result', [0, 2], 'png')
