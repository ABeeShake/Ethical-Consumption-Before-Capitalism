def main():

    from NLP_tools.build_models import make_dataset, embed_by_year_group

    df = make_dataset(dir = r'C:\Users\abhis\Documents\CollegeDocs\Data+\relevant files')

    groups = df['5_year_group'].unique()

    for group in groups:

        print(f'Creating Embeddings for the {group}s')
        embed_by_year_group(df,group)
        print(f'Finished Embeddings for the {group}s')


if __name__ == '__main__':

    main()
