
from crewai_tools import TXTSearchTool
def txt_upload(files):
    PDF_tool = TXTSearchTool(files)
    return PDF_tool

