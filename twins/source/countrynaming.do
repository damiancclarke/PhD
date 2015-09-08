********************************************************************************
global IncData "./twins/data/WB"
local file incomestatus.dta


gen WBcountry=subinstr(country, "-", " ", .)
replace WBcountry="Congo, Dem. Rep." if WBcountry=="Congo Democratic Republic"
replace WBcountry="Cote d'Ivoire" if WBcountry=="Cote d Ivoire"
replace WBcountry="Egypt, Arab Rep." if WBcountry=="Egypt"
replace WBcountry="Yemen, Rep." if WBcountry=="Yemen"
destring _year, replace
	
merge m:1 WBcountry _year using "$IncData/`file'", gen(_incmerge)
replace inc_status="LM" if WBcountry=="Brazil" & _year==1986
replace inc_status="LM" if WBcountry=="Colombia" & _year==1986
replace inc_status="LM" if WBcountry=="Congo Brazzaville"
replace inc_status="LM" if WBcountry=="Dominican Republic" & _year==1986	
replace inc_status="LM" if WBcountry=="El Salvador" & _year==1985
replace inc_status="L" if WBcountry=="Liberia" & _year==1986
replace inc_status="L" if WBcountry=="Senegal" & _year==1986
replace inc_status="LM" if WBcountry=="Peru" & _year==1986
tostring _year, replace
keep if _incmerge!=2


*THIS COMES FROM WORLD BANK ATLAS METHOD
*http://data.worldbank.org/about/country-classifications
*ACTUAL CLASSIFICATION IS HERE:
*http://data.worldbank.org/about/country-classifications/country-and-lending-groups
