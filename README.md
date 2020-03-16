# Coronavirus County Scraper

1. Unzip the Coronavirus.gdb to a location of your choice (Data Folder).
2. Update the paths in County_Coronavirus_Scraper.py (__main__ function)
3. Join the FGDB Feature Class County_pts to the Coronavirus_Case table.
4. Publish to ArcGIS Server

The counties feature class has been modified to account for the US Virgin Islands, Puerto Rico, Guam, and Hawaii counties.
There are single Guam, USVI and Puerto Rico points, since individual counties are not being reported on those islands.

I have moved Honolulu county to the island of Oahu for aesthetics.
