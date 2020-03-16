# Coronavirus County Scraper


Before using this code, please make sure that you have ran the following command in your conda environment:

"pip install python-certifi-win32" 

For more information, check out this stack overflow thread: https://stackoverflow.com/questions/50422136/python-requests-with-wincertstore/57053415#57053415

1. Install the certificate for https://nssac.bii.virginia.edu into your machine's certificate store
2. Unzip the Coronavirus.gdb to a location of your choice (Data Folder).
3. Update the paths in County_Coronavirus_Scraper.py (__main__ function)
4. Join the FGDB Feature Class County_pts to the Coronavirus_Case table.
5. Publish to ArcGIS Server

The counties feature class has been modified to account for the Guam, US Virgin Islands, Puerto Rico, and Hawaii counties.
There is a single GUam, USVI and Puerto Rico point, since individual counties are not being reported on those islands.

I have moved Honolulu county to the island of Oahu for aesthetics.
