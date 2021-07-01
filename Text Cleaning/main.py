import csv
import os

import pandas as pd
from bs4 import BeautifulSoup
import text_cleaning.clean as clean
import text_cleaning.VARD as vard

if __name__ == '__main__':

    xml_folder = r'C:\Users\abhis\Documents\CollegeDocs\Data+\B2_P4\B2'
    csv_folder = r'C:\Users\abhis\Documents\CollegeDocs\Data+\B2_P4\B2_cleaned'

    jar_file = r'C:\Users\abhis\Documents\CollegeDocs\Data+\VARD2.5.4\VARD2.5.4/clui.jar'
    setup_folder = r'C:\Users\abhis\Documents\CollegeDocs\Data+\VARD2.5.4\VARD2.5.4\default'
    threshold = '50'
    f_score = '1'
    input_folder = csv_folder
    search_subfolders = 'false'
    output_folder = r'C:\Users\abhis\Documents\CollegeDocs\Data+\B2\output'
    use_normalization_cache = 'true'

    # for idx, file in enumerate(os.listdir(xml_folder)):
    #     print(file)
    #     with open(os.path.join(xml_folder, file), 'rb') as f:
    #         contents = f.read()
    #         soup = BeautifulSoup(contents, 'html.parser')
    #         title,author,publisher,date,text = clean.parse_xml(soup)
    #         new_row = [[idx], [title], [author], [publisher], [date], [text]]
    #         clean.make_csv(new_row, file[:-4], csv_folder)

    vard.call_vard(jar_file,
                   setup_folder,
                   threshold,
                   f_score,
                   input_folder,
                   search_subfolders,
                   output_folder,
                   use_normalization_cache)

    normalized_folder = os.path.join(output_folder,r'varded(50%) - Changes Unmarked')

    combined_csv = pd.concat([pd.read_csv(os.path.join(normalized_folder,f))
                              for f
                              in os.listdir(normalized_folder)])

    combined_csv.to_csv(f'./{xml_folder[-8:-3]}.csv', index = False)