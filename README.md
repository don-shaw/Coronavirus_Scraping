# Coronavirus County Scraper

Make sure you have the following non-standard python dependencies:

<ul>
  <li><b>python-certifi-win32 </b></li>
  <li><b>arcpy</b></li>
  </ul>

You will need to install the UVA certifcate into your machine's certificate store. The requests module will need to verify certicates in your machine's certificate store. 

For more information, check out this stack overflow thread: https://stackoverflow.com/questions/50422136/python-requests-with-wincertstore/57053415#57053415

<h2> Follow these steps </h2>
<ol>
  <li>1. Install the certificate for https://nssac.bii.virginia.edu into your machine's certificate store</li>
<li>2. Unzip the Coronavirus.gdb to a location of your choice (Data Folder).</li>
<li>3. Update the paths in County_Coronavirus_Scraper.py (__main__ function)</li>
<li>4. Join the FGDB Feature Class County_pts to the Coronavirus_Case table.</li>
<li>5. Publish to ArcGIS Server </li>
  
  </ol>
  
The counties feature class has been modified to account for the Guam, US Virgin Islands, Puerto Rico, and Hawaii counties.
There is a single Guam, USVI and Puerto Rico point, since individual counties are not being reported on those islands.

The counties feature class has been modified to account for the US Virgin Islands, Puerto Rico, Guam, and Hawaii counties.
There are single Guam, USVI and Puerto Rico points, since individual counties are not being reported on those islands.

I have moved Honolulu county to the island of Oahu for aesthetics.
