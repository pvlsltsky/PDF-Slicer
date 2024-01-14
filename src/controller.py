import io
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2._utils import StrByteType

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
        
def testPdfBuffer() -> bytearray:
    writer = PdfWriter()
    fullpath = "/Users/pavelslutsky/Downloads/tofes1514---spitted.pdf"
    reader = PdfReader(fullpath)
    writer.append(reader, [2, 0, 1, 2, 0])
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output.read()

def addLineToController(fullpath : str, p_from : int, p_to : int, index: int=-1) -> None:
    if index < 0 or index >= len(slicer_lines):
        slicer_lines.append((fullpath, p_from, p_to))
    else:
        slicer_lines.insert(index, (fullpath, p_from, p_to))

def removeLineFromController(index : int) -> None:
    if index >= 0 and index < len(slicer_lines):
        del slicer_lines[index]



# merger = PdfWriter()

# input1 = open("document1.pdf", "rb")
# input2 = open("document2.pdf", "rb")
# input3 = open("document3.pdf", "rb")

# # add the first 3 pages of input1 document to output
# merger.append(fileobj=input1, pages=(0, 3))

# # insert the first page of input2 into the output beginning after the second page
# merger.merge(position=2, fileobj=input2, pages=(0, 1))

# # append entire input3 document to the end of the output document
# merger.append(input3)

# # Write to an output PDF document
# output = open("document-output.pdf", "wb")
# merger.write(output)

# # Close File Descriptors
# merger.close()
# output.close()