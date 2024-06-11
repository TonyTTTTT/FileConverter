import abc
import os.path
from pdf2image import convert_from_path
import img2pdf
from pypdf import PdfMerger


class Converter(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'convert') and
                callable(subclass.convert))

    @abc.abstractmethod
    def convert(self):
        raise NotImplementedError


class PDF2IMGConverter(Converter):
    def convert(self, pdf_path, save_path, pages, img_type):
        try:
            for page in pages:
                image = convert_from_path(pdf_path, first_page=page + 1, last_page=page + 1)
                image[0].save(
                    "{}/{}_{}.{}".format(save_path, os.path.split(pdf_path)[1].split('.')[0], page + 1, img_type))

            return True
        except:
            return False


class IMG2PDFConverter(Converter):
    def convert(self, images_path, save_path, ordered_filename, saved_filename):
        try:
            f_imgs = []
            with open('{}/{}.pdf'.format(save_path, saved_filename), 'wb') as f_pdf:
                for filename in ordered_filename:
                    for image_path in images_path:
                        if image_path.__contains__(filename):
                            f_img = open(image_path, 'rb')
                            f_imgs.append(f_img)
                f_pdf.write(img2pdf.convert(f_imgs))
            for f_img in f_imgs:
                f_img.close()
            return True
        except:
            return False


class PDFCombiner(Converter):
    def convert(self, pdfs_path, save_path, ordered_filename, saved_filename, *args):
        try:
            merger = PdfMerger()
            for pdf_path in pdfs_path:
                if ordered_filename[0] in pdf_path:
                    merger.append(pdf_path)
                    break

            if len(args) != 0:
                insert_page = args[0] - 1
                for pdf_path in pdfs_path:
                    if ordered_filename[1] in pdf_path:
                        merger.merge(insert_page, pdf_path)
                        break
            else:
                for i in range(1, len(ordered_filename)):
                    for pdf_path in pdfs_path:
                        if ordered_filename[i] in pdf_path:
                            merger.append(pdf_path)
                            break

            merger.write(os.path.join(save_path, '{}.pdf'.format(saved_filename)))
            merger.close()

            return True
        except:
            return False


if __name__ == '__main__':
    pdf_converter = PDF2IMGConverter()
    pdf_converter.convert(r'C:\Users\TonyTTTTT\Desktop\Guitar Sheet\i really want to stay at your house TAB.pdf'
                          , r'./result', [0, 2], 'png')

    img_converter = IMG2PDFConverter()
    img_converter.convert([r'C:\Users\TonyTTTTT\Pictures\下載.jfif'], r'./result', ['下載.jfif'], 'test')

    pdf_combiner = PDFCombiner()
    pdf_combiner.convert(['i really want to stay at your house TAB.pdf', 'passport.pdf'], r'./result',
                         ['i really want to stay at your house TAB.pdf', 'passport.pdf'], 'combined')
    pdf_combiner.convert(['i really want to stay at your house TAB.pdf', 'passport.pdf'], r'./result',
                         ['i really want to stay at your house TAB.pdf', 'passport.pdf'], 'combined_insert', 2)
