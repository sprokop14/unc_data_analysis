import pandas as pd
import matplotlib.pyplot as plt

# define main class and initialize it
class UNCStudentSummaryAnalyzer:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.unique_schools = self.data['Institution'].unique()
        self.grouped_data = self.data.groupby('Institution')
        self.institution_dfs = self._group_data_by_school()
        self.unique_level1 = self.data['Level 1 Field of Study'].unique()

    # define data grouping function
    def _group_data_by_school(self):
        institution_dfs = {}
        for institution, group_df in self.grouped_data:
            institution_dfs[institution] = group_df
        return institution_dfs

    # define data filtering function
    def _filter_data(self, institution, degree_level):
        if degree_level.lower() == 'graduate':
            return self.institution_dfs[institution][(self.institution_dfs[institution]['Student Type'] == 'Graduate') & (self.institution_dfs[institution]['Residency'] == 'All')]
        else:
            return self.institution_dfs[institution][(self.institution_dfs[institution]['Student Type'] == 'All Undergraduate') & (self.institution_dfs[institution]['Residency'] == 'All')]
   
    # define main plot completers function to plot majors per degree per school (after user selection)
    def plot_completers(self, school, degree_level, degree_choice):
        if school in self.institution_dfs:
            filtered_df = self._filter_data(school, degree_level)
            degree_df = filtered_df[filtered_df['Degree Level'].str.lower() == degree_level.lower()]
            if not degree_df.empty:
                degree_choice_df = degree_df[degree_df['Level 1 Field of Study'].str.contains(degree_choice, case=False)]
                if not degree_choice_df.empty:
                    degree_choice_df = degree_choice_df[degree_choice_df['Level 2 Field of Study'] == 'All']
                    fig, ax = plt.subplots(figsize=(16, 14))
                    degree_choice_df[['2018 - 2019 Count of Completers', '2019 - 2020 Count of Completers']].plot(kind='bar', ax=ax)
                    ax.set_xlabel('Year')
                    ax.set_ylabel('Completers')
                    ax.set_title(f'Two-Year Completers for {degree_choice} in {degree_level} at {school}')
                    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
                    ax.legend(title='Year')
                    plt.tight_layout()
                    return fig
                else:
                    print(f"No data found for {degree_choice} degree in {degree_level} level at {school}. Please try again.")
                return None
            else:
                print(f"No data found for {degree_level} level in {school}. Please try again.")
                return None
        else:
            print(f"School '{school}' not found. Please choose from the available schools.")
        return None
    
    # define comparison data function for data collection
    def get_comparison_data(self, school, degree_level, degree_choice):
        compare_data_list = []
        # Populate the list with data from all schools except "All UNC System Institutions"
        for other_school, df in self.institution_dfs.items():
            if other_school != school and other_school != 'All UNC System Institutions':
                compare_data = df[(df['Degree Level'] == degree_level) & (df['Level 1 Field of Study'] == degree_choice) & (df['Level 2 Field of Study'] == 'All')]
                if not compare_data.empty:
                    compare_data_list.append({'School': other_school, '2018 - 2019 Count of Completers': compare_data.iloc[0]['2018 - 2019 Count of Completers'], '2019 - 2020 Count of Completers': compare_data.iloc[0]['2019 - 2020 Count of Completers']})
        return pd.DataFrame(compare_data_list)
    
    # define plot comparison chart function to plot comparison chart according to the users' selection above
    def plot_comparison_chart(self, school, degree_level, degree_choice):
        compare_df = pd.DataFrame(columns=['School', '2018 - 2019 Count of Completers', '2019 - 2020 Count of Completers'])
        for other_school, df in self.institution_dfs.items():
            if other_school != school and other_school != 'All UNC System Institutions':
                compare_data = df[(df['Degree Level'] == degree_level) & (df['Level 1 Field of Study'] == degree_choice) & (df['Level 2 Field of Study'] == 'All')]
                if not compare_data.empty:
                    compare_df = compare_df.append({'Institution': other_school, '2018 - 2019 Count of Completers': compare_data.iloc[0]['2018 - 2019 Count of Completers'], '2019 - 2020 Count of Completers': compare_data.iloc[0]['2019 - 2020 Count of Completers']}, ignore_index=True)
        # Plot the comparison chart
        if not compare_df.empty:
            compare_df_sorted = compare_df.sort_values(by='2019 - 2020 Count of Completers', ascending=True)
            fig_compare, ax_compare = plt.subplots(figsize=(20, 18))
            compare_df_sorted.set_index('School').plot(kind='barh', ax=ax_compare, legend=False, color='orange')
            ax_compare.set_ylabel('School')
            ax_compare.set_xlabel('Completers')
            ax_compare.set_title(f'Comparison of {degree_choice} Completers in {degree_level} Across Schools')
            ax_compare.tick_params(axis='y', which='both', left=False, right=True)  # Show ticks only on the right side
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            return fig_compare
        else:
            print("No comparison data available.")


    # define available schools (unused)
    def available_schools(self):
        print("The schools you may search are as follows:")
        for school in self.unique_schools:
            print(school)

    # define available degrees (unused)
    def available_degrees(self, school):
        if school in self.institution_dfs:
            print(f"The degrees you may search for {school} are as follows:")
            school_data = self.institution_dfs[school]
            unique_degrees = school_data['Level 1 Field of Study'].unique()
            for degree in unique_degrees:
                print(degree)
        else:
            print(f"School '{school}' not found. Please choose from the available schools.")
