import streamlit as st
import matplotlib.pyplot as plt
from UNCStudentSummaryAnalyzerClass import UNCStudentSummaryAnalyzer
from UNCtextanalysis import DataAnalyzer

# display image logo
st.image('UNC-System-Logo-2.png')

# display page title
st.title("UNC School System Degree Analyzer")

#display page subheader
st.subheader("Welcome to the UNC School System Degree Analyzer!")

# display description paragraph part 1
st.write('''This application provides a comprehensive analysis of student completion data 
         for various degrees across UNC system institutions. Users can explore the number 
         of completers for specific degrees over different academic years and 
         compare the completion rates across different schools within the UNC system.''')

# display other description statements
st.write('Key features of the application include:')
st.write('1) Available Degrees: Users can view a list of available degrees offered by a selected UNC institution.')
st.write('2) Completion Analysis: Users can visualize the number of completers for a chosen degree at a specific institution over multiple academic years.')        
st.write('3) Cross-Institution Comparison: Users can compare the completion rates of a particular degree across different UNC system institutions.')
st.write('''With its user-friendly interface and powerful analytical capabilities, 
         our UNC Student Summary Analyzer empowers users to gain valuable insights 
         into student completion trends, aiding academic decision-making and institutional planning.''')
st.write('Start exploring below to unlock data-driven insights into student completions across the UNC system!')

# define a function for displaying agrees available for each of the UNC schools (when chosen)
def display_available_degrees(analyzer, school):
    if school_choice in analyzer.institution_dfs:
        st.subheader(f"The degrees you may search for {school_choice} are as follows:")
        school_data = analyzer.institution_dfs[school]
        unique_degrees = school_data['Level 1 Field of Study'].unique()
        for degree in unique_degrees:
            st.write(degree)
    else:
        st.error(f"School '{school}' not found. Please choose from the available schools.") 

# call degree analysis class from other file
if __name__ == "__main__":
    analyzer = UNCStudentSummaryAnalyzer('unc-student-summary-extract.csv')
    analyzer.available_schools()

    # create list of schools for following statements
    list_of_schools = ["All UNC System Institutions", "Appalachian State University",
                                    "East Carolina University", "Elizabeth City State University",
                                    "Fayetteville State University", "North Carolina A&T", "North Carolina Central University",
                                    "North Carolina State University", "UNC at Asheville", "UNC at Chapel Hill", "UNC at Charlotte",
                                    "UNC at Greensboro", "UNC at Pembroke", "UNC School of the Arts", "UNC Wilmington", 
                                    "Western Carolina University", "Winston-Salem State University"]

    # create select box for school choice
    # for st.selectbox specify unique keys to differeniate each method (tracebook doesn't allow multiple without keys)
    school_choice = st.selectbox("Select the name of the school you are interested in:", 
                                    list_of_schools, key="school_selectbox")
    # create select box for choosing degree level
    degree_level = st.selectbox("Select the name of the degree level you are interested in:", ["Undergraduate", "Graduate"], key='degree_level_selectbox')
     
    # create if statements to display button to show available degrees
    if school_choice in list_of_schools:
        button_clicked = st.button("Show Available Degrees", key='button_key')
        if button_clicked:
            display_available_degrees(analyzer, school_choice)
        
        # create text input box to input desired degree after viewing printed degrees
        degree_choice = st.text_input("Enter the degree you are interested in: (Please enter exactly how the degree is displayed)", key='degree_text_input')
        fig = analyzer.plot_completers(school_choice, degree_level, degree_choice)

        # seperate lines
        st.markdown("---")

        # plot figure with chosen school and degree
        st.set_option('deprecation.showPyplotGlobalUse', False)
        if fig is not None:
            st.pyplot(fig, use_container_width=False)
            st.markdown("<style>img {width: 130%;}</style>", unsafe_allow_html=True)
            st.success("Plotted Successfully!")
        else:
            st.warning("No plot generated, please try again")
        
        # create button to allow user to see comparison chart
        # call get comparison data and write if statement setting up the graph
        show_comparison = st.button("Show Comparison Chart", key='comparison_button')
        if show_comparison:
            compare_df = analyzer.get_comparison_data(school_choice, degree_level, degree_choice)
            if not compare_df.empty:
                fig_compare, ax_compare = plt.subplots(figsize=(10, 8))
                compare_df.set_index('School').plot(kind='barh', ax=ax_compare, legend=True, color=['blue', 'orange'])
                ax_compare.set_ylabel('School')
                ax_compare.set_xlabel('Completers')
                ax_compare.set_title(f'Comparison of {degree_choice} Completers in {degree_level} Across Schools')
                ax_compare.tick_params(axis='y', which='both', left=False, right=True)  # Show ticks only on the right side
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig_compare)
                st.markdown("<style>img {width: 150%;}</style>", unsafe_allow_html=True)
    else:
        st.warning('No comparison data available')
        
        st.warning("No plot generated. Please check your inputs and try again.")

    # seperate lines
    st.markdown("---")

    # Display Stagnant Chart
    analyzer2 = DataAnalyzer('unc-student-summary-extract.csv')
    fig, ax = plt.subplots()
    fig2 = analyzer2.plot_completers_scatter_comparison()
    st.pyplot(fig2, use_container_width=False)
    st.markdown("<style>img {width: 160%;}</style>", unsafe_allow_html=True)
    