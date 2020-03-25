# Coronavirus County Scraper
<img src="https://github.com/don-shaw/Coronavirus_Scraping/blob/master/Images/Mar172020.PNG" width="100%" height="50%">

<h2> Follow these steps </h2>
Make sure you have the following non-standard python dependencies:

<ul>
  <li><b>python-certifi-win32 </b></li>
  <li><b>arcpy</b></li>
  </ul>

You will need to install the UVA certifcate into your machine's certificate store. The requests module will need to verify certicates in your machine's certificate store. 

For more information, check out this stack overflow thread: https://stackoverflow.com/questions/50422136/python-requests-with-wincertstore/57053415#57053415


<ol>
  <li> Install the certificate for https://nssac.bii.virginia.edu into your machine's certificate store</li>
<li> Unzip the Coronavirus.gdb to a location of your choice (Data Folder).</li>
<li> Update the paths in config.ini</li>
<ul><li>output_path=C:/Data/coronavirus/</li>
<li>coronavirus_fgdb=C:/Data/coronavirus/Coronavirus.gdb</li>
<li>coronavirus_table=C:/Data/coronavirus/Coronavirus.gdb/Coronavirus_Cases</li>
</ul>
<li> Join the FGDB Feature Class County_pts to the Coronavirus_Case table.</li>
  
  </ol>
  
The counties feature class has been modified to account for the Guam, US Virgin Islands, Puerto Rico, and Hawaii counties.
There is a single Guam, USVI and Puerto Rico point, since individual counties are not being reported on those islands.

I have moved Honolulu county to the island of Oahu for aesthetics.

<h2> Sources </h2>
<h3> Authoritative Sources </h3>
<ul>
  <li><strong>State Map with Resources:</strong> https://napsg.maps.arcgis.com/apps/Media/index.html?appid=d627f416ce49405ca1fe4fe6ce520fed&center=-100.0438,35.7352&level=4 </li>
  <li><strong>Verified Counties: </strong> https://ps-dbs.maps.arcgis.com/apps/Media/index.html?appid=3cafba99c07d43e3bef31b9e24552f28&center=-93.3957,34.1714&level=4</li>
  <li><strong>CDC:</strong> https://www.cdc.gov/coronavirus/2019-ncov/index.html</li>
  </ul>
    <h3><strong> Non-Authoritative, but useful (used in this project)</h3>
    <ul>
   <li><strong>University of Virginia Dashboard: </strong>https://nssac.bii.virginia.edu/covid-19/dashboard/</li>
      <li><strong>Harvard Public Line List:</strong> https://docs.google.com/spreadsheets/d/1itaohdPiAeniCXNlntNztZ_oRvjh0HsGuJXUJWET008/edit#gid=0 </li>
    </ul>
  
  <h2> Disclaimer</h2>
  This repository is not an authoritative source from Esri (author's employer).
