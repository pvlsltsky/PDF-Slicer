import io
from PyPDF2 import PdfReader, PdfWriter

available_files = dict()

slicer_lines = []

def checkPdfDonor(fullpath : str) -> int:
    res = available_files.get(fullpath, 0)
    if res == 0:
        try:
            reader = PdfReader(fullpath)
            res = len(reader.pages)
            available_files[fullpath] = res
            return res
        except:
            return 0    
    return res

def compose(list_of_donors) -> PdfWriter:
    if len(list_of_donors) > 0:
        merger = PdfWriter()
        # add the pages of donor documents to output
        for (file, pf, pt) in list_of_donors:
            merger.append(file, pages=(pf-1, pt))
        return merger
    else:
        return None

def compose_to_file(list_of_donors, fullpath) -> bytearray:
    try:
        if isinstance(merger, PdfWriter):
            merger = compose(list_of_donors)
            output = open(fullpath, "wb")
            merger.write(output)
            # Close File Descriptors
            merger.close()
            output.close()
            return True
        else:
            return False
    except:
        # print("PDF file creation failed")
        return False

def compose_to_buffer(list_of_donors) -> bytearray:
    try:
        merger = compose(list_of_donors)
        if isinstance(merger, PdfWriter):
            output = io.BytesIO()
            merger.write(output)
            output.seek(0)
            return output.read()
        else:
            return None
    except:
        # print("PDF stream creation failed")
        return None
    