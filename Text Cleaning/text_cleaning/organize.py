import os


def filter_large_files(file_dir, large_output, threshold):

    large_files = list(
        filter(
            lambda x: os.path.getsize(os.path.join(file_dir,x)) >= threshold*1e3,
            os.listdir(file_dir)
        )
    )

    for file in large_files:
        os.replace(
            os.path.join(file_dir,file),
            os.path.join(large_output, file)
        )


if __name__ == '__main__':

    file_dir = r'C:\Users\abhis\Documents\CollegeDocs\Data+\A1_P4\A1_cleaned'
    large_output = r'C:\Users\abhis\Documents\CollegeDocs\Data+\A1_P4\A1_cleaned\test'

    filter_large_files(file_dir,large_output)

