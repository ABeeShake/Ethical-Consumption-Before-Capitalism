from NLP_tools.build_models import make_dataset, embed_by_decade
from NLP_tools.preprocessing import preprocess

df = make_dataset(dir = r'C:\Users\abhis\PycharmProjects\TextCleaning')

decades = df.decade.unique()

for decade in decades:

    print(f'Creating Embeddings for the {decade}s')
    embed_by_decade(df,decade)
    print(f'Finished Embeddings for the {decade}s')
