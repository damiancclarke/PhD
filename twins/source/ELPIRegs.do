/* ELPIRegs.do 1.00              damiancclarke             yyyy-mm-dd:2012-07-23
----|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8

This file takes data from the Encuesta Longitudinal de Primera Infancia (Chile)
and runs regressions analysing the likelihood of twinning based on a mother's
characteristics and behaviours.

Version history
2014-04-30: Re-order regression for pre/during behaviour.
2012-07-23: Initial file.  DCC
*/


clear all
version 11
cap log close
set more off
set mem 100m

********************************************************************************
*** (0) Globals and locals
********************************************************************************
global DAT "./twins/data/ELPI"
global LOG "./twins/log"
global OUT "./twins/results/ELPI"

cap mkdir "$OUT"
log using "$LOG/ELPIRegs.txt", text replace


local base   m_age_birth m_age_sq indigenous
local region i.region i.age rural
local w      [pw=fexp_enc]
local c      if a16==13


********************************************************************************
*** (1) Create relevant vars from Hogar database
********************************************************************************
use "$DAT/Hogar"
bys folio: egen fert=total(a16==6) //a16==6 is sibling of index child
replace fert=fert+1

gen child=1 if a16==6 | a16==13 //a16==13 is child chosen to be followed
gsort folio child -a19 
bys folio: gen birthorder=_n if child==1

bys folio: gen m_age=a19 if a16==1
bys folio: egen mother_age=mean(m_age)
gen m_age_birth=mother_age-a19 if a16==6 | a16==13
drop m_age
replace m_age_birth=. if m_age_birth<10
gen m_age_sq=m_age_birth^2

gen educ=1 if b02n==19|b02n==99
replace educ=2 if b02n<=4
replace educ=3 if b02n>4 & b02n<=7
replace educ=4 if b02n>7 & b02n<=11 & b02c<4
replace educ=5 if b02n>7 & b02n<=11 & b02c>=4
replace educ=6 if b02n==12|b02n==14
replace educ=7 if b02n==16
replace educ=8 if b02n==13|b02n==15
replace educ=9 if b02n==17|b02n==18
label def educ_lab 1 "None" 2 "Pre-school" 3 "Primary" ///
4 "Secondary incomplete"  5 "Secondary complete" 6 "Technical incomplete" ///
7"University incomplete" 8"Technical complete" 9 "University Complete"
label val educ educ_lab
gen mateduc=educ if a16==1
bys folio: egen mother_educ=mean(mateduc)
gen primary=educ<4&educ!=1
gen secondary=(educ>=5&educ<=7)
gen tertiary=(educ>7&educ!=.)

gen MP=primary if a16==1
gen MS=secondary if a16==1
gen MT=tertiary if a16==1

bys folio: egen Mprimary=max(MP)
by folio: egen Msecondary=max(MS)
by folio: egen Mtertiary=max(MT)



*Gen family income, replacing for ranges
gen family_income=d11m
replace family_income=50000 if d11t==1
replace family_income=98000 if d11t==2
replace family_income=191000 if d11t==3
replace family_income=300000 if d11t==4
replace family_income=400000 if d11t==5
replace family_income=550000 if d11t==6
replace family_income=750000 if d11t==7
replace family_income=950000 if d11t==8
replace family_income=1150000 if d11t==9
replace family_income=1500000 if d11t==10
replace family_income=. if family_income==99

bys folio: egen family_inc=max(family_income)
drop family_income

gen ypc=family_inc/tot_per

gen incomepc=ypc/10000
gen incomepc2=incomepc^2

rename a18 sex
gen indigenous=(a23!=10&a23!=99)

label var m_age_birth "Age of mother at child's birth"
label var sex "Gender"
label var family_inc "Monthly family income"
label var educ "Education level (not years)"
label var mother_age "Current age of mother"
label var child "Selected child or sibling"
label var fert "Sibship size of selected child"
label var birthorder "Order of births in child's family"
label var ypc "Income per person in the household"
label var mother_educ "Maternal education (of followed child)"


keep folio a16 a19 orden tot_per d11m fexp_hog fert birthorder mother_age /*
*/ m_age_birth educ family_inc sex indigenous child ypc mother_educ m_age_sq /*
*/ Mprimary Msecondary Mtertiary incomepc*

********************************************************************************
*** (2) Create relevant vars from Entrevistada database
********************************************************************************
merge m:1 folio using "$DAT/Entrevistada"

gen twin=(a03!=5)
sort folio a03 child a19
bys folio: gen agedif=a19[_n+1]-a19[_n] 
replace agedif=agedif*child
gen agedif2=agedif[_n-1]
replace agedif2=agedif2*child



gen pregNoAttention = g01
gen pregNumControls = g02
gen pregAnemia = (g03_08==8)
gen pregDiabetes = g03_07==7
gen pregCondPhysical = g03_13!=13
gen pregCondPsychological = g04a_9!=9
gen pregDepression = g04a_1==1
gen pregNutrition = g06a
gen pregLowWeight = g06a==1
gen pregObese = g06a==4
gen pregSmoked = g07a==1
gen pregSmokedQuant = g07b
gen pregDrugs=g11b
gen pregAlcohol=g09
gen pregHosp=g16==1
gen pregPublicHosp=g16==3
gen lowWeightPre = g05b==1
gen obesePre = g05b==4
gen nutritionPre = g05b

gen poor =ypc<32000
gen age = a19
gen rural = area

replace nutritionPre = . if nutritionPre>4
replace pregNutrition = . if pregNutrition>4
replace pregNoAttention = . if pregNoAttention==9
replace pregNumControls = . if pregNumControls==9
replace pregSmokedQuant = 0 if pregSmokedQuant==.
replace pregSmokedQuant = . if pregSmokedQuant==999
replace pregDrugs=. if pregDrugs==8
replace pregAlcohol=. if pregAlcohol==8


label def nutr 1 "Low weight" 2 "Normal" 3 "Overweight" 4 "Obese"  
label val pregNutrition nutr
label val nutritionPre nutr



label var pregNoAttention "Mother received no medical attention during pregnancy"
label var pregNumControls "Number of pregnancy controls"
label var pregAnemia "Mother suffered from Anemia during pregnancy"
label var pregCondPhysical "Suffered from a physical condition during pregnancy"
label var pregCondPsych "Suffered from a psychological condition during pregnancy"
label var pregNutrition "Mother's nutritional status during pregnancy"
label var nutritionPre "Mother's nutritional status before pregnancy"
label var pregSmoked "Mother smoked during pregnancy (binary)"
label var pregSmokedQuant "Quantity cigarettes smoked per month during pregnancy"
label var pregDrugs "Mother consumed recreational drugs during pregnancy"
label var pregAlcohol "Mother consumed alcohol during pregnancy"
label var pregHosp "Birth took place in public hospital"
label var pregPublicHosp "Birth took place in private system"


********************************************************************************
*** (3b) Updated output (pre versus during)
********************************************************************************
fvexpand Msecondary Mtertiary incomepc* lowWeightPre obesePre
local prePreg `r(varlist)'
fvexpand pregNoAt pregDiab pregDepr pregLowW pregObese pregSmoked i.pregDru /*
*/ i.pregAlc pregHosp
local preg `r(varlist)'

replace twin=twin*100
eststo: reg twin `region' `prePreg' `preg' `base' `c' `w'

#delimit ;
estout est1 using "$OUT/twinELPI.xls", keep(`prePreg' `preg' `base') replace 
	 cells(b(star fmt(%-9.3f)) se(fmt(%-9.3f) par)) 
	 stats (r2 N, fmt(%9.2f %9.0g)) starlevel ("*" 0.10 "**" 0.05 "***" 0.01);
#delimit cr
