import io
import sys
import os.path
from PyPDF2 import PdfReader, PdfWriter

available_files = dict()

slicer_lines = []

class PdfSliceData():
    def __init__(self, fullpath : str) -> None:
        reader = PdfReader(fullpath)
        self.fullpath = fullpath
        self.max_pages = reader.pages

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

def composeToFile(list_of_donors, fullpath) -> bytearray:
    try:
        merger = compose(list_of_donors)
        if isinstance(merger, PdfWriter):
            output = open(fullpath, "wb")
            merger.write(output)
            # Close File Descriptors
            merger.close()
            output.close()
            return f"Succsessfully saved to {fullpath}"
        else:
            return f"Error in initialization PDF writer"
    except Exception as ex:
        return f"Error: {ex}"

def composeToBuffer(list_of_donors) -> bytearray:
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
