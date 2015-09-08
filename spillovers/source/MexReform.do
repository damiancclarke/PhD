/* MexReform.do v0.00            damiancclarke             yyyy-mm-dd:2014-11-07
----|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8

This file runs regressions of the form:

birth(ijt) = ... + alpha*Reform(ijt-1) + beta*Close(ijt-1) + XG + u(ijt)

contact: mailto:damian.clarke@economics.ox.ac.uk

*/

vers 11
clear all
set more off
cap log close
set matsize 5000

********************************************************************************
*** (1) Globals and Locals
********************************************************************************
global DAT "./spillovers/data"
global OUT "./spillovers/tables"
global LOG "./spillovers/log"
global CHI "./planB/data/births"

cap mkdir "$LOG"
log using "$LOG/MexReform.txt", replace text
local FE i.year
local tr i.id#c.linear
local se cluster(id)
local cont medicalstaff MedMissing planteles* aulas* bibliotecas* totalinc /*
*/ totalout subsidies unemployment


********************************************************************************
*** (2) Setup data
********************************************************************************
use "$DAT/MunicipalBirths.dta"

gen AgeGroup=.
replace AgeGroup=1 if Age>=15&Age<=18
replace AgeGroup=2 if Age>=18&Age<=34
replace AgeGroup=3 if Age>=35&Age<=49
*replace AgeGroup=4 if Age>=30&Age<=39
drop if AgeGroup==.

collapse `cont' Abortion (sum) birth, by(stateid munid year AgeGroup) fast
drop if munid==""

/* START: Adding in missing zeros */
preserve
gen n=1
collapse `cont', by(stateid munid)
expand 10
bys stateid munid: gen year=2000+_n
expand 3
bys stateid munid year: gen AgeGroup=_n
tempfile full
save `full'
restore
merge 1:1 stateid munid year AgeGroup using `full', update
replace birth = 0 if _merge==2
drop _merge
/* END:   Adding in missing zeros */
    
merge m:1 stateid munid using "$DAT/DistProcessed.dta"
keep if _merge==3
drop _merge

    
egen id = concat(stateid munid)
bys id AgeGroup (year): gen linear=_n
save "$DAT/AgeBirths", replace

destring id, replace
local y birth


********************************************************************************
*** (3) Full Regressions
********************************************************************************
foreach g of numlist 1(1)3 {
    areg `y' `FE' `tr' `cont' Abortion if AgeGroup==`g', `se' absorb(id)
    outreg2 Abortion using "$OUT/AgeGroupN`g'.tex", replace tex(pretty)
    local i=0
    local d=10
    local maxD = 30
    if `g'==3 local maxD = 20
    foreach c of numlist 0(`d')`maxD' {
        gen close`g'_`i'=mindistDF>`c'&mindistDF<=`c'+`d'&year>2008
        tab close`g'_`i'
        areg `y' `FE' `tr' `cont' Abortion close`g'* if AgeG==`g', `se' absorb(id)
        outreg2 Abortion close* using "$OUT/AgeGroupN`g'.tex", append tex(pretty)
        local ++i
    }
    dis "Predicted effect for Abortion is:"
    dis _b[Abortion]*2*16
    dis "Predicted effect for Close is:"
    dis _b[close`g'_0]*2*4+_b[close`g'_1]*2*22
    dis "Predicted Total Effect"
    dis (_b[Abortion]*16+_b[close`g'_0]*4+_b[close`g'_1]*22)*2
}


********************************************************************************
*** (4) Descriptives
********************************************************************************
gen Treatment = stateid=="09"&year>2008
replace Treatment = Treatment * 100
gen Close     = meandistDF<30&year>2008
replace Close = Close*100

collapse `cont' Treatment Close meandistDF (sum) birth, by(stateid munid year)
gen birthDF    = birth if stateid=="09"&year>2008
gen birthclose = birth if meandistDF<30&year>2008
gen birthOther = Treatment==0&Close==0
replace totalinc = totalinc/1000000
replace totalout = totalout/1000000

lab var Treatment    "Treatment (Percent)"
lab var Close        "Close (Percent)"
lab var birthDF      "Number of Births (Treatment)"
lab var birthclose   "Number of Births (Close)"
lab var birthOther   "Number of Births (Other Municipalities)"
lab var year         "Year"
lab var medicalstaff "Number of Medical Staff"
lab var aulas        "Number of Classrooms"
lab var bibliotecas  "Number of Libraries"
lab var totalinc     "Municipal Income (millions of pesos)"
lab var totalout     "Municipal Spending (millions of pesos)"
lab var unemployment "Regional Unemployment Rate"

estpost tabstat Treatment Close birthDF birthclose birthOther year          /*
*/ medicalstaff aulas bibliotecas totalinc totalout unemployment,           /* 
*/ statistics(count mean sd min max) columns(statistics)  
esttab using "$OUT/MexSum.tex", title("Descriptive Statistics (Mexico)")    /*
*/ cells("count(fmt(0)) mean(fmt(2)) sd(fmt(2)) min(fmt(0)) max(fmt(0))")   /*
*/ replace label noobs

insheet using "$CHI/birthsComunaAge.csv", clear

gen Treatment = pill
replace Treatment=Treatment*100
replace pilldistance = 0 if Treatment==100
gen Close     = pilldistance<30&pilldistance!=0
replace Close = Close*100
collapse Treatment Close (sum) n, by(dom_comuna year pregnant)
reshape wide n, i(dom_comuna year) j(pregnant)

gen popln = n0+n1
rename n1 birth
replace birth=0 if birth==.

gen birthPill  = birth if Treatment==100
gen birthClose = birth if Close==100
gen birthOther = birth if Treatment==0&Close==0

lab var Treatment    "Treatment (Percent)"
lab var Close        "Close (Percent)"
lab var birthPill    "Number of Births (Treatment)"
lab var birthClose   "Number of Births (Close)"
lab var birthOther   "Number of Births (Other Municipalities)"
lab var year         "Year (2006-2012)"


#delimit ;
estpost tabstat Treatment Close birthPill birthClose birthOther year,
statistics(count mean sd min max) columns(statistics);
esttab using "$OUT/ChileSum.tex", title("Descriptive Statistics (Chile)")    /*
*/ cells("count(fmt(0)) mean(fmt(2)) sd(fmt(2)) min(fmt(0)) max(fmt(0))")   /*
*/ replace label noobs;

#delimit cr

