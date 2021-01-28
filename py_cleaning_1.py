# ==========================================================================
#  Chapter 1 - Cleaning
# ==========================================================================

python

import pandas as pd
import os
import timet

# Show the current directory
os.getcwd()

# Use float_format to display float values
pd.options.display.float_format = '{:,.2f}'.format

# Set terminal output size
# pd.set_option('display.width', 75)
pd.set_option('display.max_columns', 10)

# ==========================================================================
#  CSV
# ==========================================================================

# import the land temperature data
# Pass an argument of 1 to the skiprows parameter to skip the first row
# Rename the original column names
# Set low_memory to False to reduce the usage of memory during the import process
landtemps = pd.read_csv('data/landtempssample.csv', 
            names=['stationid','year','month','avgtemp','latitude', 'longitude','elevation','station','countryid','country'],
            skiprows=1,
            parse_dates=[['month','year']],
            low_memory=False)

landtemps.info()
landtemps.head()
type(landtemps)

# Rename column using inplace
landtemps.rename(columns={'month_year':'measuredate'}, inplace=True)

# Summary of a column
landtemps.avgtemp.describe()

# Check Missing value
landtemps.isnull().sum()

# Use the subset parameter to tell dropna to drop rows where avgtemp is missing
landtemps.dropna(subset=['avgtemp'], inplace=True)
landtemps.info()

# ==========================================================================
#  Excel (spreadsheet)
# ==========================================================================

# Import the land temperature data
percapitaGDP = pd.read_excel("data/GDPpercapita.xlsx",
   sheet_name="OECD.Stat export",
   skiprows=4,
   skipfooter=1,
   usecols="A, C:T")

percapitaGDP.head()
percapitaGDP.info()

# Rename the Year column to metro
percapitaGDP.rename(columns={'Year':'metro'}, inplace=True)

# Use strip to remove both leading and trailing spaces
percapitaGDP.metro.str.startswith(' ').any()
percapitaGDP.metro.str.endswith(' ').any()
percapitaGDP.metro = percapitaGDP.metro.str.strip()
percapitaGDP.head(10)

percapitaGDP.columns[2:]
# convert the data columns object to numeric
# character values to missing values
# rename columns
for col in percapitaGDP.columns[1:]:
  percapitaGDP[col] = pd.to_numeric(percapitaGDP[col], errors='coerce')
  percapitaGDP.rename(columns={col:'pcGDP'+col}, inplace=True)

percapitaGDP.head(10)
percapitaGDP.describe()

# Use dropna to inspect all columns, starting with the 2nd column (zero-based)
# Use how to specify that we want to drop rows only if all of the columns specified in subset are missing
percapitaGDP.dropna(subset=percapitaGDP.columns[1:], how="all", inplace=True)
percapitaGDP.info()
percapitaGDP.head(10)

# 
percapitaGPA.metro.count()
percapitaGPA['metro'].count()

# set an index using the metropolitan area column
percapitaGDP.metro.count()
percapitaGDP.metro.nunique()
percapitaGDP.set_index('metro', inplace=True)
percapitaGDP.head()
percapitaGPA.metro.()

# Confirm that there are 480 valid values for metro and that there are 480 unique values
percapitaGDP.loc['AUS02: Greater Melbourne']

percapitaGDP.pcGDP2001.count()
percapitaGDP.info()

# ==========================================================================
#  R - First method
# ==========================================================================

# get the R data
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import rpy2 as rpy

pandas2ri.activate()
readRDS = robjects.r['readRDS']
nls97withvalues = readRDS('data/nls97withvalues.rds')

nls97withvalues

# ==========================================================================
#  R - Second method
# ==========================================================================

# import pandas, numpy, and pyreadr
import pandas as pd
import numpy as np
import pyreadr
import pprint

pd.set_option('display.width', 72)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 25)

# When reading an rds file (as opposed to an rdata file), it will return one object, having the key None. 
# We indicate None to get the pandas data frame
nls97r = pyreadr.read_r('data/nls97.rds')[None]
nls97r.info()
nls97r.head(10)

# Set up and load a dictionary that maps columns to the value labels 
with open('data/nlscodes.txt', 'r') as reader:
    setvalues = eval(reader.read())

pprint.pprint(setvalues)

# create a list of preferred column names
newcols = ['personid','gender','birthmonth','birthyear',
  'sampletype',  'category','satverbal','satmath',
  'gpaoverall','gpaeng','gpamath','gpascience','govjobs',
  'govprices','govhealth','goveld','govind','govunemp',
  'govinc','govcollege','govhousing','govenvironment',
  'bacredits','coltype1','coltype2','coltype3','coltype4',
  'coltype5','coltype6','highestgrade','maritalstatus',
  'childnumhome','childnumaway','degreecol1',
  'degreecol2','degreecol3','degreecol4','wageincome',
  'weeklyhrscomputer','weeklyhrstv',
  'nightlyhrssleep','weeksworkedlastyear']

# set value labels, missing values, and change data type to category
nls97r.replace(setvalues, inplace=True)
nls97r.head()
nls97r.replace(list(range(-9,0)), np.nan, inplace=True)
for col in nls97r[[k for k in setvalues]].columns:
    nls97r[col] = nls97r[col].astype('category')

nls97r.dtypes

# set meaningful column headings and set category data types
nls97r.columns = newcols
nls97r.head()

# ==========================================================================
#  SPSS data
# ==========================================================================

# import pandas, numpy, and pyreadstat
import pandas as pd
import numpy as np
import pyreadstat

pd.set_option('display.max_columns', 10)
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.width', 75)

# import spss data, along with the meta data
nls97spss, metaspss = pyreadstat.read_sav('data/nls97.sav')

nls97spss.info()
nls97spss.head()

nls97spss['R0536300'].value_counts(normalize=True)

# use column labels and value labels
metaspss.variable_value_labels['R0536300']

nls97spss['R0536300'].\
  map(metaspss.variable_value_labels['R0536300']).\
  value_counts(normalize=True)
nls97spss = pyreadstat.set_value_labels(nls97spss, metaspss, formats_as_category=True)
nls97spss.columns = metaspss.column_labels
nls97spss['KEY!SEX (SYMBOL) 1997'].value_counts(normalize=True)
nls97spss.dtypes
nls97spss.columns = nls97spss.columns.\
    str.lower().\
    str.replace(' ','_').\
    str.replace('[^a-z0-9_]', '')
nls97spss.set_index('pubid__yth_id_code_1997', inplace=True)

# apply the formats from the beginning
nls97spss, metaspss = pyreadstat.read_sav('data/nls97.sav', apply_value_formats=True, formats_as_category=True)
nls97spss.columns = metaspss.column_labels
nls97spss.columns = nls97spss.columns.\
  str.lower().\
  str.replace(' ','_').\
  str.replace('[^a-z0-9_]', '')
nls97spss.dtypes
nls97spss.head()
nls97spss.govt_responsibility__provide_jobs_2006.\
  value_counts(sort=False)
nls97spss.set_index('pubid__yth_id_code_1997', inplace=True)
 
# do the same for stata data
nls97stata, metastata = pyreadstat.read_dta('data/nls97.dta', apply_value_formats=True, formats_as_category=True)
nls97stata.columns = metastata.column_labels
nls97stata.columns = nls97stata.columns.\
    str.lower().\
    str.replace(' ','_').\
    str.replace('[^a-z0-9_]', '')
nls97stata.dtypes
nls97stata.head()
nls97stata.govt_responsibility__provide_jobs_2006.\
  value_counts(sort=False)
nls97stata.min()
nls97stata.replace(list(range(-9,0)), np.nan, inplace=True)
nls97stata.min()
nls97stata.set_index('pubid__yth_id_code_1997', inplace=True)

# pull sas data, using the sas catalog file for value labels
nls97sas, metasas = pyreadstat.read_sas7bdat('data/nls97.sas7bdat', catalog_file='data/nlsformats3.sas7bcat', formats_as_category=True)
nls97sas.columns = metasas.column_labels
nls97sas.columns = nls97sas.columns.\
    str.lower().\
    str.replace(' ','_').\
    str.replace('[^a-z0-9_]', '')
nls97sas.head()
nls97sas.keysex_symbol_1997.value_counts()
nls97sas.set_index('pubid__yth_id_code_1997', inplace=True)
