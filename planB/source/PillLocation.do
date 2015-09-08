*
*---|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8
*

clear all
set more off
vers 11


********************************************************************************
***(1) globals and locals
********************************************************************************
global MAP  "./planB/data/comunas"
global PILL "./planB/data/pill"
global OUT  "./planB/figures"


********************************************************************************
***(2) Import, rename
********************************************************************************
insheet using $PILL/PillDist.csv, delimiter(";")
keep if comuna_names!=""


rename comuna_names NAMES_3
gen n=1 if disponible=="1"
replace n=0 if disponible=="0"|disponible=="2"
collapse pilldistance (sum) n, by(NAMES_3)
replace n=3 if n==5

replace NAMES_3="CASA BLANCA" if NAMES_3== "CASABLANCA"
replace NAMES_3="CARAHUE" if NAMES_3=="CURAHUE"
replace NAMES_3="GOLBEA" if NAMES_3=="GORBEA"
replace NAMES_3="NATALES" if NAMES_3=="PUERTO NATALES"
replace NAMES_3="NAVARINO" if NAMES_3=="CABO DE HORNOS"
replace NAMES_3="OCEAN ISLANDS" if NAMES_3=="ISLA DE PASCUA"
replace NAMES_3="QUILAGO" if NAMES_3=="QUILACO"
replace NAMES_3="QUILLEGO" if NAMES_3=="QUILLECO"
replace NAMES_3="REQUINAO" if NAMES_3=="REQUINOA"
replace NAMES_3="ROSENDO" if NAMES_3=="SAN ROSENDO"
replace NAMES_3="SAAVEDRA" if NAMES_3=="PUERTO SAAVEDRA"
replace NAMES_3="SAN JODE DE MAIPO" if NAMES_3=="SAN JOSE DE MAIPO"
replace NAMES_3="TORRES DE PAINE" if NAMES_3=="TORRES DEL PAINE"
replace NAMES_3="TREHUACO" if NAMES_3=="TREGUACO"
replace NAMES_3="VILLARRICA" if NAMES_3=="VILLARICA"

tempfile pill
save `pill'

use "$MAP/Chile3"
rename NAME_3 NAMES_3
replace NAMES_3=upper(NAMES_3)

merge 1:1 NAMES_3 using `pill'

#delimit ;
spmap n using "$MAP/Chilecoord3" if id !=263, id(id) osize(vvthin) 
  fcolor(Greens2) legend(symy(*2) symx(*2) size(*2.6) position (10))
  clmethod(custom) clbreaks(0 0.9 1.9 2.9 3) legorder(lohi) 
  legend(label(1 "No municipal health") label(2 "No Pill") 
  label(3 "Available 1 year") label(4 "Available 2 years") 
  label(5 "Available 3 years" )) saving($OUT/avail, replace);
graph export $OUT/Pill_l.eps, as(eps) replace;
#delimit cr



