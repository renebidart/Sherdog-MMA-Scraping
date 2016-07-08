# Sherdog-MMA-Scraping

Made in February 2015
This program scrapes UFC fight data off [Sherdog](http://www.sherdog.com/), and puts it in a useable format:

|Date|FighterA|FighterB|FighterA Height|fighterA Age|...|Winner|Method| 
|----------|----------------|-------------|-----|----|------|------------|------------------------|
|2015-05-30|Carlos Condit|Thiago Alves |6' 2"| 31 |...|Carlos Condit| TKO - Doctor's Stoppage|
|2015-05-30|Michael Bisping|CB Dollaway |6' 1"| 36 |...|Carlos Condit|Decision - Unanimous|

It looks through all the events to find the UFC fighters, then through all their profiles to find all their fights, and makes a dataset using the individial fight information.

*Because this was my first time using python and I am not a programmer, it is a bit of a mess. It also will need to be updated as the website changes.*



