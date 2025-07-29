import pandas as pd

from state_of_the_art.tables.text_feedback_table import TextFeedbackTable


class Dataset:
    def __init__(self):
        self.train_data = None
        self.test_data = None
        self.train_split = None
        self.test_split = None
        self.train_y = None
        self.test_y = None

    def get_feedback_data(self) -> pd.DataFrame:

        df = self.get_raw_feedback_table()
        df = df[df['score'].notnull()]
        df =  df[['text', 'score', 'tdw_uuid']]
        return df

    def get_raw_feedback_table(self) -> pd.DataFrame:
        return TextFeedbackTable().read().sort_values(by='tdw_timestamp', ascending=False)

    def get_train_test_split(self):
        df = self.get_feedback_data()
        print(len(df))
        print("Clasess balance")
        print(df['score'].value_counts())

        self._create_train_test_split(df)
        self._create_train_test_embeddings()
        self.train_data = list(zip(self.train_embedding, self.train_y))
        self.test_data = list(zip(self.test_embedding, self.test_y))

        # class distribution over train and test
        print("Class distributions over train and test")
        print("Train Labels: ", self.train_df['score'].value_counts())
        print("Test Labels: ", self.test_df['score'].value_counts())

        return self.train_data, self.test_data

    def _create_train_test_split(self, df):
        # split train and test
        rows_number=len(df) 
        test_size = int(rows_number*0.3)
        train_size = rows_number - test_size

        self.train_df = df.sample(train_size, random_state=42)
        self.test_df = df.merge(self.train_df.drop_duplicates(), on=['tdw_uuid','tdw_uuid'],
                        how='left', indicator=True, suffixes=('', '_y'))

        #create DataFrame with rows that exist in first DataFrame only
        self.test_df = self.test_df[self.test_df['_merge'] == 'left_only']
        self.test_df = self.test_df[[c for c in self.test_df.columns if not c.endswith('_y')]]
        # drop merge column
        self.test_df = self.test_df.drop(columns=['_merge'])
        self.train_y = self.train_df['score'].astype('int64').to_numpy()
        self.test_y =  self.test_df['score'].astype('int64').to_numpy()
        print(len(self.train_df), len(self.test_df))

        self.train_split = self.train_df
        self.test_split = self.test_df
        self.train_y = self.train_y
        self.test_y = self.test_y

        return self.train_df, self.test_df, self.train_y, self.test_y

    def _create_train_test_embeddings(self):
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-mpnet-base-v2")
        # The sentences to encode
        # 2. Calculate embeddings by calling model.encode()
        train_embedding = model.encode(self.train_split['text'].to_list())
        test_embedding = model.encode(self.test_split['text'].to_list())

        self.train_embedding = train_embedding
        self.test_embedding = test_embedding


        return train_embedding, test_embedding
