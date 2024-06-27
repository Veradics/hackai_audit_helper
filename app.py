import streamlit as st
# import io
from tech import *  # Ensure tech.py contains all necessary functions
from assistant import *

# Define the CSS for central alignment
central_alignment_css = """
<style>
h1, h2, h3, h4, h5, h6 {
    text-align: center;
}

div.stButton > button, div.stDownloadButton > button {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 200px; /* Set your desired width */
    height: 70px; /* Set your desired height */
}

</style>
"""

# Apply the CSS
st.markdown(central_alignment_css, unsafe_allow_html=True)


# image
st.image('./header_app.jpeg')

# PAGES
# home
def home():
    st.title('ESG Compliance AI')
    st.header("AI sustainability report evaluation")

    description = """
    This application provides automated assessments of sustainability reports, 
    ensuring full compliance with [TCFD](https://www.ifrs.org/sustainability/tcfd/) standards and delivering actionable insights 
    for further improvements.
    """

    st.markdown(description)
    
    # state variables
    st.session_state.was_report_check = False
    st.session_state.was_block_check = False
    st.session_state.was_block_generation = False

    # buttons (TCFD info)
    with open('TCFD_Checklist.docx', 'rb') as file:
        st.download_button(
            label="download TCFD checklist",
            data=file,
            file_name="TCFD_checklist.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    st.write("")
    st.write('Choose one option:')

    # buttons (options)
    if st.button("check full report"):
        st.session_state.page = "full report check 1"
        st.rerun()

    if st.button("check report block"):
        st.session_state.page = "block report check 1"
        st.rerun()


# full report check 1
def full_report_form():
    st.title("Full report check")
    st.subheader("Step 1. Fill in the form:")

    tcfd_industries = [
        "Banks",
        "Insurance Companies",
        "Energy",
        "Transportation",
        "Materials and Buildings",
        "Agriculture, Food, and Forest Products",
        "Other"
    ]
    st.session_state.industry = st.selectbox('Industry',tcfd_industries, index=None)

    st.subheader('Step 2. Upload the report')
    uploaded_report = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt'])

    if uploaded_report:
        st.session_state.uploaded_report = uploaded_report
        st.session_state.uploaded_report_type = uploaded_report.type.split('/')[-1]

        # button to continue
        if st.button("get results"):
            st.session_state.page = "full report check 2"
            st.rerun()


# full report check 2
def full_report_results():
    st.title("Full report check")
    if 'uploaded_report' in st.session_state:
        st.write(f'Your report: "{st.session_state.uploaded_report.name}"')
        if st.session_state.was_report_check and 'full_report_results' in st.session_state:
            st.markdown(st.session_state.full_report_results)

        elif not st.session_state.was_report_check:
            full_report_results = get_full_report_check(st.session_state.uploaded_report, st.session_state.industry) 
            st.session_state.full_report_results = full_report_results
            st.session_state.was_report_check = True 

        if 'full_report_results' in st.session_state:
            st.download_button(
                label="download detailed analysis",
                data=st.session_state.full_report_results,
                file_name="detailed_report_analysis.txt",
                mime="text/markdown"
            )

    if st.button('home'):
        st.session_state.page = "home"
        st.rerun()


# block report check 1
def block_report_form():
    st.title("Block report check")
    st.subheader('Type or upload the report block text')
    user_text = st.text_area("Enter your text here:")
    uploaded_file = st.file_uploader("Or choose a file:", type=['pdf', 'docx', 'txt'])

    st.session_state.report_block_text = None
    st.session_state.uploaded_file = None

    if user_text:
        st.session_state.report_block_text = user_text
    elif uploaded_file:
        st.session_state.uploaded_file = uploaded_file

    # button to continue
    if st.session_state.report_block_text or st.session_state.uploaded_file:
        if st.button("continue"):
            st.session_state.page = "block report check 2"
            st.rerun()


# # block report check 2
def block_report_results():
    st.title("Block report check")
    if st.session_state.was_block_check and 'block_analysis_results' in st.session_state:
        st.markdown(st.session_state.block_analysis_results)

    elif not st.session_state.was_block_check:
        if 'report_block_text' in st.session_state:    
            block_analysis_results = get_assistant_response(st.session_state.report_block_text)
            st.session_state.block_analysis_results = block_analysis_results
            st.session_state.was_block_check = True
        elif 'uploaded_report' in st.session_state:
            block_analysis_results = get_part_report_check(st.session_state.uploaded_report) 
            st.session_state.block_analysis_results = block_analysis_results
            st.session_state.was_block_check = True   

    if 'block_analysis_results' in st.session_state:
        # buttons
        if st.button('generate report block using recommendations and new information'):
            st.session_state.page = 'block report generation'
            st.rerun()
        if st.button('home'):
            st.session_state.page = 'home'
            st.rerun()


# block report generation
def block_report_generation():
    st.title('Block report generation')
    st.subheader('Type new information:')
    new_info_text = st.text_area("Enter your text here:")
    placeholder = st.empty()

    if st.button('generate') and st.session_state.was_block_check and not st.session_state.was_block_generation:
        # running the generation process
        placeholder.text('Generation running...')

        if 'report_block_text' in st.session_state:    
            new_report_block = generate_report_block(st.session_state.report_block_text, new_info_text, st.session_state.block_analysis_results)
            st.session_state.new_report_block = new_report_block
            st.session_state.was_block_generation = True
        elif 'uploaded_report' in st.session_state:
            new_report_block = generate_report_block(st.session_state.uploaded_report, new_info_text, st.session_state.block_analysis_results, is_file=True)
            st.session_state.new_report_block = new_report_block
            st.session_state.was_block_generation = True

        placeholder.text('Generation completed!')
    
    elif st.session_state.was_block_generation and "new_report_block" in st.session_state:
        st.markdown(st.session_state.new_report_block)
        
        
        # download results
        if 'new_report_block' in st.session_state:
            st.download_button(
                label="download generated report block",
                data=st.session_state.new_report_block,
                file_name="generated_report_block.txt",
                mime="text/markdown"
            )
    
    if st.button('home'):
        st.session_state.page = "home"
        st.rerun()

# MAIN
# initialization of the page state
if 'page' not in st.session_state:
    st.session_state.page = "home"

# display the selected page
if st.session_state.page == "home":
    home()
elif st.session_state.page == "full report check 1":
    full_report_form()
elif st.session_state.page == "full report check 2":
    full_report_results()
elif st.session_state.page == "block report check 1":
    block_report_form()
elif st.session_state.page == "block report check 2":
    block_report_results()
elif st.session_state.page == "block report generation":
    block_report_generation()