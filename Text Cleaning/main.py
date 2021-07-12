import os
import pandas as pd
from bs4 import BeautifulSoup
import text_cleaning.box as box
import text_cleaning.clean as clean
import text_cleaning.VARD as vard
import text_cleaning.organize as org
from glob import glob

if __name__ == '__main__':
    dir = rf'C:\Users\abhis\Documents\CollegeDocs\Data+'
    folders = glob(dir + r'/*/')
    files = [folder[-7:-4] for folder in folders if folder.endswith('_P5\\')]
    file_num = 'A56'
    for file_num in files:

        xml_folder = rf'C:\Users\abhis\Documents\CollegeDocs\Data+\{file_num}_P5\{file_num}'
        csv_folder = rf'C:\Users\abhis\Documents\CollegeDocs\Data+\{file_num}_P5\{file_num}_cleaned'

        jar_file = rf'C:\Users\abhis\Documents\CollegeDocs\Data+\VARD2.5.4\VARD2.5.4/clui.jar'
        setup_folder = rf'C:\Users\abhis\Documents\CollegeDocs\Data+\VARD2.5.4\VARD2.5.4\default'
        threshold = '45'
        f_score = '1'
        input_folder = csv_folder
        search_subfolders = 'false'
        output_folder = rf'C:\Users\abhis\Documents\CollegeDocs\Data+\{file_num}_P5\output'
        use_normalization_cache = 'true'

        csv_file = f'./{file_num}_P5.csv'

        for idx, file in enumerate(os.listdir(xml_folder)):
            print(file)
            with open(os.path.join(xml_folder, file), 'rb') as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'html.parser')
                title, author, publisher, date, text = clean.parse_xml(soup,body_tag = 'div')
                new_row = [[idx], [title], [author], [publisher], [date], [text]]
                clean.make_csv(new_row, file[:-4], csv_folder)

        org.filter_large_files(csv_folder, os.path.join(csv_folder, 'uncleaned'),1500)

        vard.call_vard(jar_file,
                       setup_folder,
                       threshold,
                       f_score,
                       input_folder,
                       search_subfolders,
                       output_folder,
                       use_normalization_cache)

        normalized_folder = os.path.join(output_folder, rf'varded({threshold}%) - Changes Unmarked')

        combined_csv = pd.concat([pd.read_csv(os.path.join(normalized_folder, f))
                                  for f
                                  in os.listdir(normalized_folder)])

        combined_csv.to_csv(csv_file, index=False)

        box.auto_upload(csv_file)
