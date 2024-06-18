import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

# this class is comprised of various functions we developed and experiemented with regarding the 
# extracted csv data. On the application, only 3 of the functions were called and used in the StreamLitUI.py file

# define class and initialize file path
class DataAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
    
    # define process_text_data function to collect necessary data
    def process_text_data(self):
        data_list = self.df["Level 1 Field of Study"].tolist()
        data_list = [str(item) for item in data_list if isinstance(item, str)]
        all_text = ' '.join(data_list)
        tokens = nltk.word_tokenize(all_text)
        words = [word.lower() for word in tokens if word.isalpha()]
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word not in stop_words]
        return filtered_words

    # unused function - define function to collect word frequency 
    def plot_word_frequency(self, words, num_words=30):
        word_frequency = nltk.FreqDist(words)
        word_frequency.plot(num_words)

    # define function to plot degree per school completers
    # use ax from Matplotlib to generate charts as streamlit doesn't support plt
    def plot_completers_scatter(self, ax):
        filtered_df = self.df[(self.df['Degree Level'] == 'Undergraduate') & (self.df['Residency'] == 'All')]
        grouped = filtered_df.groupby('Level 1 Field of Study').agg({'2018 - 2019 Count of Completers': 'sum', '2019 - 2020 Count of Completers': 'sum'}).reset_index()
        fig, ax = plt.subplots(figsize=(20, 18))
        sc = ax.scatter(grouped['2018 - 2019 Count of Completers'], grouped['2019 - 2020 Count of Completers'], c=range(len(grouped)), cmap='viridis')
        ax.set_xlabel('Total Completers for 2018-2019')
        ax.set_ylabel('Total Completers for 2019-2020')
        ax.set_title('Scatter Plot of UNC System Institutions (Undergraduate) by Level 1 Field of Study')
        # Add colorbar
        cbar = plt.colorbar(sc)
        cbar.set_label('Level 1 Field of Study Index')
        ax.grid(True)
        return fig

    # define function to plot scatter comparison data
    # use ax to generate charts as streamlit doesn't support plt
    def plot_completers_scatter_comparison(self):
        filtered_df = self.df[(self.df['Degree Level'] == 'Undergraduate') & (self.df['Residency'] == 'All')]
        grouped = filtered_df.groupby('Level 1 Field of Study').agg({'2018 - 2019 Count of Completers': 'sum', '2019 - 2020 Count of Completers': 'sum'}).reset_index()
        fig, ax = plt.subplots(figsize=(20, 18))
        sc = ax.scatter(grouped['2018 - 2019 Count of Completers'], grouped['2019 - 2020 Count of Completers'], c='blue', label='2018-2019')
        sc = ax.scatter(grouped['2019 - 2020 Count of Completers'], grouped['2018 - 2019 Count of Completers'], c='red', label='2019-2020')
        ax.set_xlabel('Total Completers')
        ax.set_ylabel('Total Completers')
        ax.set_title('Scatter Plot of UNC System Institutions (Undergraduate) by Level 1 Field of Study')
        ax.legend()
        cbar = plt.colorbar(sc, ax=ax)
        cbar.set_label('Level 1 Field of Study Index Comparison')
        # plt.legend()
        ax.grid(True)
        return fig
    

    # below is an example of function we developed with plt on Jupyter NB 
    # (before changing to ax to support streamlit functionality)

       # def plot_completers_scatter(self):
    #     filtered_df = self.df[(self.df['Degree Level'] == 'Undergraduate') & (self.df['Residency'] == 'All')]
    #     grouped = filtered_df.groupby('Level 1 Field of Study').agg({'2018 - 2019 Count of Completers': 'sum', '2019 - 2020 Count of Completers': 'sum'}).reset_index()
    #     plt.figure(figsize=(12, 8))
    #     plt.scatter(grouped['2018 - 2019 Count of Completers'], grouped['2019 - 2020 Count of Completers'], c=range(len(grouped)), cmap='viridis')
    #     plt.xlabel('Total Completers for 2018-2019')
    #     plt.ylabel('Total Completers for 2019-2020')
    #     plt.title('Scatter Plot of UNC System Institutions (Undergraduate) by Level 1 Field of Study')
    #     plt.colorbar(label='Level 1 Field of Study Index')
    #     plt.grid(True)
    #     plt.show()
















