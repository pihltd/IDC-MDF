import bento_mdf
import bento_meta
import pandas as pd
import argparse


def readExcel(filename, sheetname):
    exeldf = pd.read_excel(filename, sheet_name=sheetname)
    return exeldf


def main(args):
    excelfile = r'C:\Users\pihltd\OneDrive - National Institutes of Health\FNLCR Projects\Imaging Data Commons\Data Model\Copy of CDS Imaging Template_V1.0_June10th2024.xlsx'
    all_df = pd.ExcelFile(excelfile)
    sheetlist = all_df.sheet_names

    sheetlist.pop(0)
    sheetlist.pop(0)
    pv_df = readExcel(excelfile, 'Terms and Value Sets')
    sheetlist.pop(0)
    finalmess = {}
    for sheet in sheetlist:
        nodename = sheet.split('-')[-1]
        temp_df = readExcel(excelfile, sheet)
        finalmess[nodename] = temp_df
        
    for node, df in finalmess.items():
        print(f"Node: {node}\nColumns: {list(df.columns)}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("-c", "--config", required=True, help="Configuration file to convert CRDS Search XLS file to MDF")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    #parser.add_argument("-w", "--writefile", action="store_true", help="Write out summary.txt file")

    args = parser.parse_args()

    main(args)