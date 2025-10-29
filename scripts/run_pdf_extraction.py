#!/usr/bin/env python3
from table_tools.pdf_extractor.extraction_35 import main as extract_35
from table_tools.pdf_extractor.extraction_36 import main as extract_36
from table_tools.pdf_extractor.tabula_extraction import main as tabula_extract


print(" Starting PDF extraction...")
extract_35()
extract_36() 
tabula_extract()
print(" PDF extraction completed!")
