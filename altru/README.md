# Altru Script

The goal is to be able to input an address and a real estate listing website and retrieve relevant information about that listing
as it pertains to the specific listing website.

Some relevant information includes:
1. Address
2. Price
3. No. of Bedrooms
4. No. of Bathrooms
5. Square footage
6. Acreage
7. Year Built

---

For testing, I am going to use the following property : 88 Rose Way, Bridgehampton, NY 11932. Below is the property information in order. This will also act as a checklist for developing the scraping methods.
- [ ] 88 Rose Way, Bridgehampton, NY 11932
- [x] $21,000,000 
- [ ] 10
- [ ] 13 full + 2 partial
- [ ] 12,300 sq. ft.
- [ ] 1.5 acres
- [ ] 2022

---

# Streamlit

To start it up, execute the following command:
```bash

streamlit run path/to/file/run_streamlit.py
```

---

# Getting started with development.
First start the virtual environment.

1. beautifulsoup4 -- `pip install beautifulsoup4`
2. streamlit -- `pip install streamlit`
3. streamlit-authenticator -- `pip install streamlit-authenticator`
4. streamlit-extras -- `pip install streamlit-extras`
5. google-cloud-firestore -- `pip install google-cloud-firestore`
6. streamlit-aggrid -- `pip install streamlit-aggrid`

Next, we need to package up our own code so that the import statements work.
First, make sure you're in the root directory (i.e. the directory whose children are `altru`, `.gitignore`, `setup.py`).
Then, run the following command:
`pip install -e .`