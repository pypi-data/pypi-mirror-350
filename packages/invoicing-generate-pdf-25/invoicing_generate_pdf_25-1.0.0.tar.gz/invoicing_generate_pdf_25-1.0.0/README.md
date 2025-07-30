# Section 60: MODULE 10: Day 60: App 20 - Build and Publish a Python Package

# 453. Welcome to Module 10

Welcome to the "Building Python Packages" category, where you'll learn how to 
create and distribute your own Python packages through PyPi (Python Package Index) 
so everyone can install your package using "pip." We will use the code of one 
of the apps we build during the course to create our own package.


# 454. Today

### Keynotes

1. [Python Package Index (PyPI)](https://pypi.org/)
The Python Package Index (PyPI) is a repository of software for the Python 
programming language.
2. When you install a package, e.g. `pip install pandas`, then you visit PyPI
3. Scope of the course:
 a. build our own package
 b. upload the package to PyPI
 c. others can access the package and install it


## 455. Description of the Package

### Keynotes

1. Use of application 4 as base of building a package.
2. Download the _resources/app4-invoice-generation.zip_
3. The app4: create pdf invoices from the excel files.
_app4-invoice-generation/app4-invoice-generation/README.md_
4. Create a package for app4 so other users can install it and use it.


## 456. Preparing the Code of Package

### Keynotes

1. Install the 3rd party packages, pandas, FPDF
`pip install pandas`
`pip install fpdf`
2. Copy the _main.py_ and rename it into _invoice.py_
3. Block the code inside a function, _generate_. It could be
also a class.
4. Replace the strings/dirs for the columns with parameters.


## 457. Testing the Package

### Keynotes

1. Test the module (a py file)
2. Convert the module into a package (2 files in a dir).
3. Library refers either to a module or a package.
4. Import the _invoice_ module inside another .py file and test it from _main.py_
5. Inside a Python Console:
`import invoice`
`help(invoice.generate)`
Help on function generate in module invoice:
generate(invoices_path, pdfs_path, image_path, product_id, product_name, amount_purchased, price_per_unit, total_price)
6. Install the library openpyxl to read the excel files, command:
`pip install openpyxl`
7. In case of extending the invoice, e.g. convert excel to html files, then it
should be created another module (py file) inside the same package.
8. Create the directory **invoicing** for the package.
9. To import the package function from an external file,  it is used:
`from invoicing import invoice`
10. It is recommended to create a file _invoicing/__init__.py_ and add the:
`from .invoice import generate`
then from the external _main.py_ you may use the import statement for the function _generate_:
`from invoicing import generate`


## 458. Uploading the Package to PyPi

### Keynotes

1. Target: make available our package, invoicing to the https://pypi.org
2. Register an account to the pypi.org
username: stefk
password: udemyC0urs5%25
PyPI recovery codes
98fe859d97526f44
2b383ce7b033f36d
b6f334a43c8ac894
9f518cc883f28a41
9c2dc528bbcb414c
ea2806a56c320380
1070f633fd552a4e
676c7d3f13e1b7e2
3. Download and modify the file _setup.py_
4. Install the library _setuptools_
`pip install setuptools`
5. Note: search in the platform for package's name availability.
6. Type the terminal command:
`python setup.py sdist`
7. A directory _**dist**_ to be created with a tar file init.
8. Install the 3rd party library _twine_, command:
`pip install twine`
9. Upload the dist directory with the command:
`twine upload --skip-existing dist/*`
10. It asks an API token. Type the password.