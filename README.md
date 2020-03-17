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
  <li> Install the certificate for https://nssac.bii.virginia.edu into your machine's certificate store</li>
<li> Unzip the Coronavirus.gdb to a location of your choice (Data Folder).</li>
<li> Update the paths in County_Coronavirus_Scraper.py (__main__ function)</li>
<li> Join the FGDB Feature Class County_pts to the Coronavirus_Case table.</li>
  
  </ol>
  
The counties feature class has been modified to account for the Guam, US Virgin Islands, Puerto Rico, and Hawaii counties.
There is a single Guam, USVI and Puerto Rico point, since individual counties are not being reported on those islands.

The counties feature class has been modified to account for the US Virgin Islands, Puerto Rico, Guam, and Hawaii counties.
There are single Guam, USVI and Puerto Rico points, since individual counties are not being reported on those islands.

I have moved Honolulu county to the island of Oahu for aesthetics.

<h3> Authoratative Sources </h3>
<ul>
  <li> https://napsg.maps.arcgis.com/apps/Media/index.html?appid=d627f416ce49405ca1fe4fe6ce520fed&center=-100.0438,35.7352&level=4</li>
  <li>https://ps-dbs.maps.arcgis.com/apps/Media/index.html?appid=3cafba99c07d43e3bef31b9e24552f28&center=-93.3957,34.1714&level=4</li>
  <li>https://www.cdc.gov/coronavirus/2019-ncov/index.html</li>
  </ul>
    <h3> Non-Authoratative, but useful (used in this project)</h3>
    <ul>
      <li>https://docs.google.com/spreadsheets/d/1itaohdPiAeniCXNlntNztZ_oRvjh0HsGuJXUJWET008/edit#gid=0</li>
      <li>https://nssac.bii.virginia.edu/covid-19/dashboard/</li>
    </ul>
