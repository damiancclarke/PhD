/* NHISRegs.do v0.00             damiancclarke             yyyy-mm-dd:2014-10-25
----|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8

This file takes processed data from the generating script NHISPrep.do and runs
OLS, IV and bounds analysis of the effect of fertility on child quality.  Speci-
fications are as similar as possible to DHS twin regressions. The twin 2sls reg-
ressions (the main regression of interest), take the following form:

quality = a + b*fert + S'C + H'D + u
fert    = e + f*twin + S'G + H'I + v

where the quality regression is the second stage.

    Contact: mailto:damian.clarke@ecnomics.ox.ac.uk

Version history
   v0.00: Running only with NHIS from 2004-2013 (2003 and earlier are diff)
*/

vers 11
clear all
set more off
cap log close

********************************************************************************
*** (1) Globals and locals
********************************************************************************
global DAT "./twins/data/NHIS"
global OUT "./twins/results/NHIS"
global FIG "./twins/figures"
global LOG "./twins/log"

cap mkdir $OUT
log using "$LOG/NHISRegs.txt", text replace

local yvars EducationZscore excellentHealth  
local age   ageFirstBirth motherAge motherAge2
local base  B_* childSex
local H     H_* `age' smoke* heightMiss
local SH    S_* `H' 
local tcon  i.surveyYear i.motherRace i.region `age'

local wt    pw=sWeight
local se    cluster(motherID)

local estopt cells(b(star fmt(%-9.3f)) se(fmt(%-9.3f) par)) /*
*/ stats (r2 N, fmt(%9.2f %9.0g)) starlevel ("*" 0.10 "**" 0.05 "***" 0.01)

********************************************************************************
*** (2) Append cleaned files, generate indicators
********************************************************************************
append using "$DAT/NHIS2011" "$DAT/NHIS2012" "$DAT/NHIS2013" "$DAT/NHIS2014"
append using "$DAT/NHIS2007" "$DAT/NHIS2008" "$DAT/NHIS2009" "$DAT/NHIS2010" 
append using                 "$DAT/NHIS2004" "$DAT/NHIS2005" "$DAT/NHIS2006" 

gen childHealth=childHealthStatus if childHealthStatus<=5
gen excellentHealth=childHealthStatus==1

foreach zVar in Education Health {
    bys ageInterview: egen mE=mean(child`zVar')
    bys ageInterview: egen sd=sd(child`zVar')
    gen `zVar'Zscore=(child`zVar'-mE)/sd
    drop mE sd
}

tab surveyYear,   gen(B_Syear)
tab ageInterview, gen(B_Bdate)
tab region,       gen(B_region)
tab motherRace,   gen(B_mrace)

tab motherHealthStatus, gen(H_mhealth)
drop H_mhealth6
drop H_mhealth7
drop H_mhealth8

gen mGoodHealth   =motherHealthStatus==1|motherHealthStatus==2
gen mPoorHealth   =motherHealthStatus==4|motherHealthStatus==5
gen mMissingHealth=motherHealthStatus==6|motherHealthStatus==7
gen H_mheight=motherHeight
gen H_mheight2=motherHeight^2
gen S_meduc=motherEducation
gen S_meduc2=motherEducation^2


gen bmi2=bmi^2

********************************************************************************
*** (3) Summary
********************************************************************************
gen mEduc=motherEducation
replace mEduc=12 if motherEducation==13
replace mEduc=12 if motherEducation==14
replace mEduc=14 if motherEducation>=15
gen BMI=bmi if bmi<99
gen BMI185=bmi<18.5
replace BMI185=. if bmi>99
gen motherExcellentHealth=motherHealthStatus==1

local motherStat fert motherAge mEduc BMI BMI185 motherExcellentHealth
local childStat  excellentHealth childEducation EducationZscore

preserve
collapse `motherStat' twinfamily, by(surveyYear hhx fmx)
replace twinfamily=round(twinfamily)
estpost tabstat `motherStat', by(twinfamily) statistics(mean sd) listwise /*
*/ columns(statistics)
esttab using "$OUT/Mother.txt", replace main(mean) aux(sd) nostar unstack /*
*/ noobs nonote nomtitle nonumber
restore
estpost tabstat `childStat', by(twin) statistics(mean sd) listwise /*
*/ columns(statistics)
esttab using "$OUT/Child.txt", replace main(mean) aux(sd) nostar unstack /*
*/ noobs nonote nomtitle nonumber

sum twin
sum bord if twin==1
count if fpx=="01"
count if fpx=="01"&twinfamily==1
count if fpx=="01"&twinfamily==0
count
count if twin==1
count if twin==0    

********************************************************************************
*** (4) Twin Regression
********************************************************************************
gen twin100=twin*100

reg twin100 H_mheight S_meduc* i.motherRac i.region motherAge* /*
*/ ageFirstBirth i.surveyYear bmi heightMiss
outreg2 `age' H_* S_* bmi using "$OUT/NHIStwin.tex", tex(pr) replace
reg twin100 H_mheight S_meduc* i.motherRac i.region motherAge* /*
*/ ageFirstBirth i.surveyYear bmi heightMiss if childYearBirth<=1989
outreg2 `age' H_* S_* bmi using "$OUT/NHIStwin.tex", tex(pr) append
reg twin100 H_mheight S_meduc* i.motherRac i.region motherAge* /*
*/ ageFirstBirth i.surveyYear bmi heightMiss if childYearBirth>1989
outreg2 `age' H_* S_* bmi using "$OUT/NHIStwin.tex", tex(pr) append
reg twin100 H_mheight S_meduc* smoke* i.motherRac i.region motherAge* /*
*/ ageFirstBirth i.surveyYear bmi heightMiss
outreg2 `age' H_* S_* bmi smoke* using "$OUT/NHIStwin.tex", tex(pr) append


********************************************************************************
*** (5) OLS regressions
********************************************************************************
foreach y of varlist `yvars' {
    
    eststo: reg `y' `base' `age' fert [`wt'], `se'
    eststo: reg `y' `base' `H'   fert [`wt'], `se'
    eststo: reg `y' `base' `SH'  fert [`wt'], `se'

    local Oout "$OUT/OLSAll`y'.xls"
    estout est1 est2 est3 using "`Oout'", replace `estopt' keep(fert `SH')
    estimates clear
        
    foreach f in two three four {
        eststo: reg `y' fert `base' `SH' [`wt'] if `f'_plus==1, `se'
        eststo: reg `y' fert `base' `H'  [`wt'] if `f'_plus==1&e(sample), `se'
        eststo: reg `y' fert `base'      [`wt'] if `f'_plus==1&e(sample), `se'
    }
    local estimates est3 est2 est1 est6 est5 est4 est9 est8 est7
    local Oout "$OUT/OLSFert`y'.xls"
    estout `estimates' using "`Oout'", replace `estopt' keep(fert `SH')

    estimates clear
}

********************************************************************************
*** (6a) IV regressions
********************************************************************************
foreach y of varlist `yvars' {
    foreach f in two three four {
        local F`f'
        preserve
        keep if `f'_plus==1
        eststo: ivreg29 `y' `base' `SH' (fert=twin_`f'_fam) [`wt'], /*
        */ `se' first ffirst savefirst savefp(`f's) partial(`base')
        unab svars : S_*
        test `svars'
        local F`f' `F`f'' `=`r(chi2)''
		
        eststo: ivreg29 `y' `base' `H' (fert=twin_`f'_fam) if e(sample) [`wt'], /*
        */ `se' first ffirst savefirst savefp(`f'h) partial(`base')
        unab hvars : H_* smoke*
        test `hvars'
        local F`f' `F`f'' `=`r(chi2)''

        eststo: ivreg29 `y' `base' (fert=twin_`f'_fam) if e(sample) [`wt'], /*
        */ `se' first ffirst savefirst savefp(`f'b) partial(`base')
        restore
        dis `F`f''
    }
    local estimates est3 est2 est1 est6 est5 est4 est9 est8 est7
    local fstage twobfert twohfert twosfert threebfert threehfert threesfert /*
    */ fourbfert fourhfert foursfert
    estout `estimates' using "$OUT/IVFert`y'.xls", replace `estopt' keep(fert `SH')
    estout `fstage'  using "$OUT/IVFert`y'1.xls", replace `estopt' keep(twin* `SH')
    dis "F-test two plus (S, H)  : `Ftwo'"
    dis "F-test three plus (S, H): `Fthree'"
    dis "F-test four plus (S, H) : `Ffour'"
    estimates clear
}

********************************************************************************
*** (6b) Plausibly exogenous bounds
********************************************************************************
mat ConleyBounds = J(6,4,.)
local i = 1
foreach y of varlist `yvars' {
    foreach f in two three four {
        preserve
        keep if `f'_plus==1
        
        qui reg `y' `base'
        predict Ey, resid
        qui reg fert `base'
        predict Ex, resid
        qui reg twin_`f'_fam `base'
        predict Ez, resid
        local ESH
        foreach var of varlist `SH' {
            qui reg `var' `base'
            predict E`var', resid
            local ESH `ESH' E`var'
        }
        
        plausexog uci `y' `base' `SH' (fert=twin_`f'_fam) [`wt'], /*
          */ vce(robust) gmin(0) gmax(0.0182) grid(2) level(0.90)
        mat ConleyBounds[`i',1]=e(lb_fert)
        mat ConleyBounds[`i',2]=e(ub_fert)

        local items 17
        matrix omega_eta = J(`items',`items',0)
        matrix omega_eta[1,1] = 0.00265^2
        matrix mu_eta = J(`items',1,0)
        matrix mu_eta[1,1] = 0.0091448

            
        plausexog ltz Ey `ESH' (Ex=Ez), omega(omega_eta) mu(mu_eta)
        cap mat ConleyBounds[`i',3]=_b[Ex]-1.65*_se[Ex]
        cap mat ConleyBounds[`i',4]=_b[Ex]+1.65*_se[Ex]
        
        foreach num of numlist 0(1)5 {
            matrix om`num' = J(`items',`items',0)
            matrix om`num'[1,1] = ((`num'/5)*0.1/sqrt(12))^2
            matrix mu`num' = J(`items',1,0)
            matrix mu`num'[1,1] = (`num'/5)*0.1/2
            local d`num' = (`num'/5)*0.1
        }
        plausexog ltz Ey `ESH' (Ex=Ez), mu(mu_eta) omega(omega_eta)    /*
         */ graphomega(om0 om1 om2 om3 om4 om5)                        /*
         */ graphmu(mu0 mu1 mu2 mu3 mu4 mu5) graph(Ex)                 /*
         */ graphdelta(`d0' `d1' `d2' `d3' `d4' `d5')
        graph export "$FIG/ConleyUSA_`y'_`f'.eps", as(eps) replace
            
        mat list ConleyBounds
        restore
        local ++i
    }
}
mat rownames ConleyBounds = TwoE ThreeE FourE TwoH ThreeH FourH 
mat colnames ConleyBounds = LowerBound UpperBound LowerBound UpperBound
mat2txt, matrix(ConleyBounds) saving("$OUT/ConleyGammaNHIS.txt")      /*
*/ format(%6.4f) replace


********************************************************************************
*** (X) Close
********************************************************************************
log close
