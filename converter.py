import abc
import os.path

from pdf2image import convert_from_path

class Converter(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'convert') and
                callable(subclass.convert))

    @abc.abstractmethod
    def convert(self, path: str) -> str:
        raise NotImplementedError


class PDFConverter(Converter):
    def convert(self, pdf_path, save_path, pages, img_type):
        images = convert_from_path(pdf_path)

        for page in pages:
            images[page].save("{}/{}_{}.{}".format(save_path, os.path.split(pdf_path)[1].split('.')[0], page, img_type))


class IMGConverter(Converter):
    pass

