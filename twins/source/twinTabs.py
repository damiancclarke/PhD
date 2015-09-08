# twinTabs.py v 0.0.0            damiancclarke             yyyy-mm-dd:2014-03-29
#---|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8
#

from sys import argv
import re
import os
import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

script, ftype = argv
print('\n\nHey DCC. The script %s is making %s files \n' %(script, ftype))

#==============================================================================
#== (1a) File names (comes from Twin_Regressions.do)
#==============================================================================
cdir     = os.getcwd()
Results  = cdir + '/twins/results/'
Tables   = cdir + '/twins/tables/'

base     = Results+'DHS/IV/'+'All.xls'
lowi     = Results+'DHS/IV/'+'LowIncome.xls'
midi     = Results+'DHS/IV/'+'MidIncome.xls'
gend     = [Results+'DHS/IV/'+'Girls.xls',Results+'DHS/IV/'+'Boys.xls']
         
firs     = Results+'DHS/IV/'+'All_first.xls'
flow     = Results+'DHS/IV/'+'LowIncome_first.xls'
fmid     = Results+'DHS/IV/'+'MidIncome_first.xls'
         
ols      = Results+'DHS/OLS/'+"QQ_ols.txt"
bala     = Results+'DHS/Summary/'+"Balance_mother.tex"
twin     = Results+'DHS/Twin/'+"Twin_Predict.xls"
twiP     = Results+'DHS/Twin/'+"Twin_PredictProbit.xls"
summ     = Results+'DHS/Summary/'+"Summary.txt"
sumc     = Results+'DHS/Summary/'+"SummaryChild.txt"
sumf     = Results+'DHS/Summary/'+"SummaryMortality.txt"
coun     = Results+'DHS/Summary/'+"Count.txt"
dhss     = Results+'DHS/Summary/'+"Countries.txt"
         
conl     = Results+'DHS/Conley/'+"ConleyGamma.txt"
conU     = Results+'NHIS/'+"ConleyGammaNHIS.txt"
imrt     = Results+'DHS/Twin/'+"PreTwinTest.xls"
         
gamT     = Results+"gamma/gammaEstimates.txt"

#==============================================================================
#== (1b) Options (tex or csv out)
#==============================================================================
dd   = "&"
dd1  = "&\\begin{footnotesize}"
dd2  = "\\end{footnotesize}&\\begin{footnotesize}"
dd3  = "\\end{footnotesize}"
end  = "tex"
foot = "$^{*}$p$<$0.1; $^{**}$p$<$0.05; $^{***}$p$<$0.01"
ls   = "\\\\"
mr   = '\\midrule'
hr   = '\\hline'
tr   = '\\toprule'
br   = '\\bottomrule'
mc1  = '\\multicolumn{'
mcsc = '}{l}{\\textsc{'
mcbf = '}{l}{\\textbf{'    
mc2  = '}}'
twid = ['5','8','4','5','9','9','4','6','10','7','12','6','12','5','10']
tcm  = ['}{p{10.0cm}}','}{p{17.8cm}}','}{p{10.4cm}}','}{p{11.6cm}}',
        '}{p{13.8cm}}','}{p{14.2cm}}','}{p{12.1cm}}','}{p{13.8cm}}',
        '}{p{18.0cm}}','}{p{12.8cm}}','}{p{18cm  }}','}{p{10.0cm}}',
        '}{p{18.8cm}}','}{p{10.6cm}}','}{p{20.2cm}}']
mc3  = '{\\begin{footnotesize}\\textsc{Notes:} '
lname = "Fertility$\\times$desire"
tname = "Twin$\\times$desire"
tsc  = '\\textsc{' 
ebr  = '}'
R2   = 'R$^2$'
mi   = '$\\'
mo   = '$'
lineadd = '\\begin{footnotesize}\\end{footnotesize}&'*6+ls
lA   = '\\begin{footnotesize}\\end{footnotesize}&'*9
+'\\begin{footnotesize}\\end{footnotesize}'+ls
lA2  = '\\begin{footnotesize}\\end{footnotesize}&'*11
+'\\begin{footnotesize}\\end{footnotesize}'+ls

hs   = '\\hspace{5mm}'

rIVa = '\\ref{TWINtab:IVAll}'
rTwi = '\\label{TWINtab:twinreg1}'
rSuS = '\\ref{TWINtab:sumstats}'
rFSt = '\\ref{TWINtab:FS}'
rCou = '\\ref{TWINtab:countries}'
rGen = '\\ref{TWINtab:IVgend}'

#==============================================================================
#== (2a) Function to return fertilility beta and SE for IV tables
#==============================================================================
def plustable(ffile,n1,n2,searchterm,alt,n3):
    beta = []
    se   = []
    N    = []

    f = open(ffile, 'r').readlines()

    for i, line in enumerate(f):
        if re.match(searchterm, line):
            beta.append(i)
            se.append(i+1)
        if re.match("N", line):
            N.append(i)
    
    TB = []
    TS = []
    TN = []
    if alt=='alt':
        for i,n in enumerate(beta):
            if i==0:
                TB.append(f[n].split()[n1:n2])
            elif i==1:
                TB.append(f[n].split()[n3])
        for i,n in enumerate(se):
            if i==0:
                TS.append(f[n].split()[n1-1:n2-1])
            elif i==1:
                TS.append(f[n].split()[n3-1])
    else:
        for n in beta:
            TB.append(f[n].split()[n1:n2])
        for n in se:
            TS.append(f[n].split()[n1-1:n2-1])
    for n in N:
        TN.append(f[n].split()[n1:n2])

    return TB, TS, TN


#==============================================================================
#== (2b) Function to return fertilility beta and SE for OLS tables
#==============================================================================
def olstable(ffile,n1,n2,n3):
    beta = []
    se   = []
    N    = []
    R    = []

    f = open(ffile, 'r').readlines()

    for i, line in enumerate(f):
        if re.match("fert", line):
            beta.append(i)
            se.append(i+1)
        if re.match("Observations", line):
            N.append(i)
        if re.match("R-squared", line):
            R.append(i)

    TB = []
    TS = []
    TN = []
    TR = []

    for i,n in enumerate(beta):
        if i==0:
            TB.append(f[n].split()[n1:n2])
        elif i==1:
            TB.append(f[n].split()[n3:n3+1])
    for i,n in enumerate(se):
        if i==0:
            TS.append(f[n].split()[n1-1:n2-1])
        elif i==1:
            TS.append(f[n].split()[n3-1:n3])
    for n in N:
        TN.append(f[n].split()[n1:n2])
    for n in R:
        TR.append(f[n].split()[n1:n2])

    A1 = float(re.search("-\d*\.\d*", TB[0][0]).group(0))
    A2 = float(re.search("-\d*\.\d*", TB[0][1]).group(0))
    A3 = float(re.search("-\d*\.\d*", TB[0][2]).group(0))
    AR1 = str(round(A2/(A1-A2), 3))
    AR2 = str(round(A3/(A1-A3), 3))

    return TB, TS, TN, TR, AR1, AR2


#==============================================================================
#== (3) Table Full IVResults
#==============================================================================
IV2 = open(Tables+"IVTogether."+end, 'w')

IV2.write("\\begin{landscape}\\begin{table}[htpb!]"
          "\\caption{Principal IV Results}\n"
          "\\label{TWINtab:IVAll}\n\\begin{center}"
          "\\begin{tabular}{lcccp{2mm}cccp{2mm}ccc}\n\\toprule \\toprule \n"
          "&\\multicolumn{3}{c}{2+}&&\\multicolumn{3}{c}{3+}&"
          "&\\multicolumn{3}{c}{4+} \\\\ \\cmidrule(r){2-4} \\cmidrule(r){6-8}"
          " \\cmidrule(r){10-12} \n"
          "\\textsc{School Z-Score}&Base&+H&+S\&H&&Base&+H&+S\&H&&Base&+H&+S\&H"
          "\\\\ \\midrule \n"
          +"\\begin{footnotesize}\\end{footnotesize}& \n"*11+
          "\\begin{footnotesize}\\end{footnotesize}\\\\ \n")

AllB = []
AllS = []
AllN = []
LowB = []
LowS = []
LowN = []
MidB = []
MidS = []
MidN = []
TwiB = []
TwiS = []
TwiN = []
AdjB = []
AdjS = []
AdjN = []

for num in [1,5,9]:
    BB, BS, BN    = plustable(base, num, num+3,'fert','normal',1000)
    LB, LS, LN    = plustable(lowi, num, num+3,'fert','normal',1000)
    MB, MS, MN    = plustable(midi, num, num+3,'fert','normal',1000)
    
    AllB.append(dd + BB[0][0] + dd + BB[0][1] + dd + BB[0][2])
    AllS.append(dd + BS[0][0] + dd + BS[0][1] + dd + BS[0][2])
    AllN.append(dd + BN[0][0] + dd + BN[0][1] + dd + BN[0][2])
    LowB.append(dd + LB[0][0] + dd + LB[0][1] + dd + LB[0][2])
    LowS.append(dd + LS[0][0] + dd + LS[0][1] + dd + LS[0][2])
    LowN.append(dd + LN[0][0] + dd + LN[0][1] + dd + LN[0][2])
    MidB.append(dd + MB[0][0] + dd + MB[0][1] + dd + MB[0][2])
    MidS.append(dd + MS[0][0] + dd + MS[0][1] + dd + MS[0][2])
    MidN.append(dd + MN[0][0] + dd + MN[0][1] + dd + MN[0][2])


IV2.write(mc1+twid[10]+mcbf+"All"+mc2+ls+" \n"
"Fertility"+AllB[0]+dd+AllB[1]+dd+AllB[2]+ls+'\n'
+AllS[0]+dd+AllS[1]+dd+AllS[2]+ls+'\n'+lA2+
"Observations"+AllN[0]+dd+AllN[1]+dd+AllN[2]+ls+'\n'+

mc1+twid[10]+mcbf+"Low-Income"+mc2+ls+" \n"
"Fertility"+LowB[0]+dd+LowB[1]+dd+LowB[2]+ls+'\n'
+LowS[0]+dd+LowS[1]+dd+LowS[2]+ls+'\n'+lA+
"Observations"+LowN[0]+dd+LowN[1]+dd+LowN[2]+ls+'\n'+

mc1+twid[10]+mcbf+"Middle-Income"+mc2+ls+" \n"
"Fertility"+MidB[0]+dd+MidB[1]+dd+MidB[2]+ls+'\n'
+MidS[0]+dd+MidS[1]+dd+MidS[2]+ls+'\n'+lA+
"Observations"+MidN[0]+dd+MidN[1]+dd+MidN[2]+ls+'\n')

IV2.write('\n'+mr+mc1+twid[10]+tcm[10]+mc3+
          "The two plus subsample refers to all first born children in       "
          "families with at least two births.  Three plus refers to first-   "
          "and second-borns in families with at least three births, and four "
          "plus refers to first- to third-borns in families with at least    "
          "four births.  Each cell presents the coefficient of a 2SLS        "
          "regression where fertility is instrumented by twinning at birth   "
          "order two, three or four (for 2+, 3+ and 4+ respectively).        "
          "Different rows of the table correspond to different sub-groups or "
          "specifications. In order these correspond to: all children,       "
          "grouped by country income status, adjusting fertility to correct  "
          "exclude children who did not survive to one year, and including   "
          "both pre-twins \emph{and} twins in the regression. Base controls  "
          "include child age, mother's age, and mother's age at birth fixed  "
          "effects plus country and year-of-birth FEs.  In each case the     "
          "sample is made up of all children aged between 6-18 years from    "
          "families in the DHS who fulfill 2+ to 4+ requirements. First-stage" 
          " results in the final panel correspond to the second stage in row "
          "1. Full first stage results for each row are available in table   "
          +rFSt+". Standard errors are clustered by mother."+foot+" \n")
IV2.write("\\end{footnotesize}} \\\\ \\bottomrule \n"
          "\\end{tabular}\\end{center}\\end{table}\\end{landscape}")

IV2.close()


#==============================================================================
#== (4) Write OLS Table
#==============================================================================
TBa, TSa, TNa, TRa, A1a, A2a = olstable(ols, 1, 6, 1)
TBl, TSl, TNl, TRl, A1l, A2l = olstable(ols, 6, 11, 2)
TBm, TSm, TNm, TRm, A1m, A2m = olstable(ols, 11, 16, 3)


OLSf = open(Tables+'OLS.'+end, 'w')

OLSf.write("\\begin{landscape}\\begin{table}[!htbp] \\centering \n"
           "\\caption{OLS Estimates of the Q-Q Trade-off} \n "
           "\\label{TWINtab:OLS} \n"
           "\\begin{tabular}{lccccccc} \\toprule \\toprule \n")

OLSf.write(dd+"Base"+dd+"+"+dd+"+Health"+dd+"Bord"+dd+"Desired"+dd+"Altonji" +
           dd+"Altonji"+ls+"\n"
           +dd+"Controls"+dd+"Health"+dd+"\&Socioec"+dd+"Controls&&Ratio 1"  +
           dd+"Ratio 2"+ls+mr+"\n"
           +tsc+"Panel A: All Countries"+ebr+dd+dd+dd+dd+dd+dd+dd+ls+"\n"

           "Fertility "+dd+TBa[0][0]+dd+TBa[0][1]+dd+TBa[0][2]+dd+TBa[0][3]+dd
           +            TBa[0][4]+dd+A1a+dd+A2a+ls+"\n"
           +            dd+TSa[0][0]+dd+TSa[0][1]+dd+TSa[0][2]+dd+TSa[0][3]+dd
           +            TSa[0][4]+dd+dd+ls+  "\n"
           +lname+dd+dd+dd+dd+dd+TBa[1][0]+dd+dd+ls+"\n"
           +            dd+dd+dd+dd+dd+TSa[1][0]+dd+dd+ls+  "\n"
           +dd+dd+dd+dd+dd+dd+dd+ls+"\n"
           "Observations "+dd+str(TNa[0][0])+dd+str(TNa[0][1])+dd
           +str(TNa[0][2])+dd+str(TNa[0][3])+dd+str(TNa[0][4])+dd+dd+ls+"\n"
           +R2+dd+str(TRa[0][0])+dd+ str(TRa[0][1])+dd+str(TRa[0][2])+dd
           +            str(TRa[0][3])+dd+str(TRa[0][4])+dd+dd+ls+mr+"\n")
           
OLSf.write(tsc+"Panel B: Low Income"+ebr+dd+dd+dd+dd+dd+dd+dd+ls+"\n"
           "Fertility "+dd+TBl[0][0]+dd+TBl[0][1]+dd+TBl[0][2]+dd+TBl[0][3]+dd
           +            TBl[0][4]+dd+A1l+dd+A2l+ls+"\n"
           +            dd+TSl[0][0]+dd+TSl[0][1]+dd+TSl[0][2]+dd+TSl[0][3]+dd
           +            TSl[0][4]+dd+dd+ls+  "\n"
           +lname+dd+dd+dd+dd+dd+TBl[1][0]+dd+dd+ls+"\n"
           +            dd+dd+dd+dd+dd+TSl[1][0]+dd+dd+ls+  "\n"
           +dd+dd+dd+dd+dd+dd+dd+ls+"\n"
           "Observations "+dd+str(TNl[0][0])+dd+str(TNl[0][1])+dd
           +str(TNl[0][2])+dd+str(TNl[0][3])+dd+str(TNl[0][4])+dd+dd+ls+"\n"
           +R2+dd+str(TRl[0][0])+dd+ str(TRl[0][1])+dd+str(TRl[0][2])+dd
           +            str(TRl[0][3])+dd+str(TRl[0][4])+dd+dd+ls+mr+"\n"
           
           +tsc+"Panel C: Middle Income"+ebr+dd+dd+dd+dd+dd+dd+dd+ls+"\n"
           "Fertility "+dd+TBm[0][0]+dd+TBm[0][1]+dd+TBm[0][2]+dd+TBm[0][3]+dd
           +            TBm[0][4]+dd+A1m+dd+A2m+ls+"\n"
           +            dd+TSm[0][0]+dd+TSm[0][1]+dd+TSm[0][2]+dd+TSm[0][3]+dd
           +            TSm[0][4]+dd+dd+ls+  "\n"
           +lname+dd+dd+dd+dd+dd+TBm[1][0]+dd+dd+ls+"\n"
           +            dd+dd+dd+dd+dd+TSm[1][0]+dd+dd+ls+  "\n"
           +dd+dd+dd+dd+dd+dd+dd+ls+"\n"
           "Observations "+dd+str(TNm[0][0])+dd+str(TNm[0][1])+dd
           +str(TNm[0][2])+dd+str(TNm[0][3])+dd+str(TNm[0][4])+dd+dd+ls+"\n"
           +R2+dd+str(TRm[0][0])+dd+ str(TRm[0][1])+dd+str(TRm[0][2])+dd
           +            str(TRm[0][3])+dd+str(TRm[0][4])+dd+dd+ls+hr+hr+"\n"
           +mc1+twid[1]+tcm[1]+mc3+
           "Base controls consist of child gender, mother's age and age      "
           "squared mother's age at first birth, child age, country, and year"
           " of birth dummies.  Socioeconomic augments `Base' to include     "
           "mother's education and education squared, and Health includes    "
           "mother's height and BMI. ``Desire'' takes 1 if the child is born "
           "before the family reaches its desired size, and 0 if the child is"
           " born after the desired size is reached. The                     "
           "\\citet{Altonjietal2005} ratio determines how important          "
           "unobservable factors must be compared with included observables  "
           "to imply that the true effect of fertilty on educational         "
           "attainment is equal to zero.  Ratio 1 compares no controls to    "
           "socioeconomic controls, while ratio 2 compares no controls to    "
           "socioeconomic and health controls. Standard errors are clustered "
           "at the level of the mother.\n" + foot)

OLSf.write("\\end{footnotesize}}\\\\  \n \\bottomrule"
           "\\normalsize\\end{tabular}\\end{table}\\end{landscape} \n")

OLSf.close()


#==============================================================================
#== (5) Read in balance table, fix formatting
#==============================================================================
bali = open(bala, 'r').readlines()
balo = open(Tables+"Balance_mother."+end, 'w')

for i,line in enumerate(bali):
    if i>6:
        line = line.replace("&", dd)
        line = line.replace("\\\\", ls)
        line = line.replace("\\toprule", 
                            "\\toprule\\toprule & Non-Twin & Twin & Diff.\\\\")
        line = line.replace("mu\_1", "Family")
        line = line.replace("mu\_2", "Family")
        line = line.replace("d/d\\_se", "(Diff. SE)")
        line = line.replace("\\end{tabular}", "")    
        line = line.replace("\\end{table}", "")    
        line = line.replace("\\bottomrule", mr+mr)    

        balo.write(line)

balo.write(mc1+twid[2]+tcm[2]+mc3+
           "All variables are at the level of the mother. Education is        "
           "measured in years, mother's height in centimetres, and BMI is     "
           "weight in kilograms over height in metres squared. Wealth         "
           "quintiles are determined by DHS methodology and are based on      "
           "presence/absence of particular goods in the household. Diff. SE   "
           "is calculated using a two-tailed t-test.  Sample is identical to  "
           "that in table " + rSuS + "." + foot)
balo.write("\\end{footnotesize}}\n"+ls+br+
           "\\normalsize\\end{tabular}\\end{table} \n")

balo.close()

#==============================================================================
#== (6) Read in twin predict table, LaTeX format
#==============================================================================
ii = 1
for twintab in [twin, twiP]:
    if ii==1:
        Tname = ''
        Ttype = ''
        Tlab  = 'TWINtab:TwinDHS'
    if ii==2:
        Tname = 'Probit'
        Ttype = '(Probit)'
        Tlab  = 'TWINtab:TwinDHSProbit'

    twini = open(twintab, 'r')
    twino = open(Tables+"TwinReg"+Tname+"."+end, 'w')

    twino.write("\\begin{landscape}\\begin{table}[htpb!] \n"
                "\\caption{Probability of Giving Birth to Twins "
                + Ttype + "} \\label{" + Tlab + "}\n"
                "\\begin{center}\\begin{tabular}{lcccccc}\\toprule\\toprule\n"
                +dd+"(1)"+dd+"(2)"+dd+"(3)"+dd+"(4)"+dd+"(5)"+dd+"(6)"+ls+"\n"
                "Twin*100"+dd+"All"+dd+"\\multicolumn{2}{c}{Income}"+dd+
                "\\multicolumn{2}{c}{Time}"+dd+"Prenatal"+ls+"\n "
                "\\cmidrule(r){3-4} \\cmidrule(r){5-6} \n"
                +dd+dd+"Low inc"+dd+"Middle inc"+dd+"1990-2013"+dd+"1972-1989"
                +dd+ls+mr+"\n"
                "\\begin{footnotesize}\\end{footnotesize}"+dd+
                "\\begin{footnotesize}\\end{footnotesize}"+dd+
                "\\begin{footnotesize}\\end{footnotesize}"+dd+
                "\\begin{footnotesize}\\end{footnotesize}"+dd+
                "\\begin{footnotesize}\\end{footnotesize}"+dd+
                "\\begin{footnotesize}\\end{footnotesize}"+dd+
                "\\begin{footnotesize}\\end{footnotesize}"+ls+"\n")

    for i,line in enumerate(twini):
        if i>2:
            line = line.replace("\t",dd)
            line = line.replace("\n", ls)
            line = line.replace("\"", "")
            line = line.replace("made.\\\\", "made.")
            line = line.replace("made.&&&&&&\\\\", "made.")
            line = line.replace("antenatal", "Antenatal Visits")
            line = line.replace("prenate_doc", "Prenatal (Doctor)")
            line = line.replace("prenate_nurse", "Prenatal (Nurse)")
            line = line.replace("prenate_none", "Prenatal (None)")
            line = line.replace("Notes:",hr+hr+ 
            "\\multicolumn{7}{p{14.3cm}}{\\begin{footnotesize}\\textsc{Notes:}")
            line = line.replace("r2", dd*6+ls+"R-squared")
            line = line.replace("N&", "Observations &")
            line = re.sub(r"(?<=\d),(?=\d)",".", line)
            twino.write(line+'\n')

    twino.write(foot+"\n \\end{footnotesize}}\\\\ \\hline \\normalsize "
                "\\end{tabular}\\end{center}\\end{table}\\end{landscape} \n")
    twino.close()
    ii = ii+1

#==============================================================================
#== (7) Read in summary stats, LaTeX format
#==============================================================================
counti = open(coun, 'r')

addL = []
for i,line in enumerate(counti):
    if i<8:
        line=line.replace("(  ", "(")
        addL.append(line.replace("( ","("))
    elif i==8:
        nk = line

summi = open(summ, 'r')
summc = open(sumc, 'r')
summf = open(sumf, 'r')
summo = open(Tables+"Summary."+end, 'w')

summo.write("\\begin{table}[htpb!]\\caption{Summary Statistics} \n"
            "\\label{TWINtab:sumstats}\\begin{center}\\scalebox{0.95}{"
            "\\begin{tabular}{lccccc}\n\\toprule \\toprule \n"
            "&\\multicolumn{2}{c}{Low Income}"
            "&\\multicolumn{2}{c}{Middle Income}\\\\ \n" 
            "\\cmidrule(r){2-3} \\cmidrule(r){4-5}\n"
            "& Single & Twins & Single & Twins & All \\\\ \\midrule \n"
            "\\textsc{Fertility} & & & & & \\\\ \n")

for i,line in enumerate(summi):
    if i>2 and i%3!=2:
        line=re.sub(r"\s+", dd, line)
        line=re.sub(r"&$", ls+ls, line)

        line = line.replace("bord"           , "Birth Order"            )
        line = line.replace("fert"           , "Fertility"              )
        line = line.replace("idealnumkids"   , "Desired Family Size"    )
        line = line.replace("agemay"         , "Age"                    )
        line = line.replace("educf"          , "Education"              )
        line = line.replace("height"         , "Height"                 )
        line = line.replace("bmi"            , "BMI"                    )
        line = line.replace("underweight"    , "Pr(BMI)$<$18.5"         )
        line = line.replace("exceedfam"      , "Actual Births$>$Desired")

        line = line.replace("Age", 
        addL[4]+ addL[5]+addL[6]+ addL[7]+
        "\\textsc{Mother's Characteristics}&&&&&\\\\ Age\n")

        summo.write(line+'\n')
for i,line in enumerate(summc):
    if i>2 and i%3!=2:
        line=re.sub(r"\s+", dd, line)
        line=re.sub(r"&$", ls+ls, line)
        line = line.replace("noeduc"         , "No Education (Percent)" )
        line = line.replace("educ"           , "Education (Years)"      )
        line = line.replace("school_zsc~e"   , "Education (Z-Score)"    )

        line = line.replace("Education (Years)", 
        "\\textsc{Children's Outcomes}&&&&&\\\\ Education (Years)\n")

        summo.write(line+'\n')

for i,line in enumerate(summf):
    if i>2 and i%3!=2:
        line=re.sub(r"\s+", dd, line)
        line=re.sub(r"&$", ls+ls, line)
        line = line.replace("infantmort~y", "Infant Mortality")
        line = line.replace("childmorta~y", "Child Mortality" )

        summo.write(line+'\n')

summo.write(mr +'\n'+ addL[0] + addL[1] + addL[2] + addL[3] + mr + "\n"
            +mc1+twid[7]+tcm[7]+mc3+"Summary statistics are presented for the "
            "full estimation sample consisting of all children 18 years of    "
            "age and under born to the " +nk+ " mothers responding to any     "    
            " publicly available DHS survey. Group means are presented with   "
            "standard deviation below in parenthesis.  Education is reported  "
            "as total years attained, and Z-score presents educational        "
            "attainment relative to country and cohort (mean 0, std deviation "
            "1).  Infant mortality refers to the proportion of children who   "
            "die before 1 year of age, while child mortality refers to the    "
            "proportion who die before 5 years. Maternal height is reported in"
            " centimetres, and BMI is weight in kilograms over height in      "
            "metres squared.  For a full list of country and years of survey, "
            "see appendix table "+rCou+".")
summo.write("\\end{footnotesize}} \\\\ \\bottomrule "
            "\\end{tabular}}\\end{center}\\end{table}")

summo.close()


#==============================================================================
#== (8) Create Conley et al. table
#==============================================================================
conli = open(conl, 'r').readlines()
conlu = open(conU, 'r').readlines()
conlo = open(Tables+"Conley."+end, 'w')


conlo.write("\\begin{table}[htpb!]\\caption{`Plausibly Exogenous' Bounds} \n"
            "\\label{TWINtab:Conley}\\begin{center}\\begin{tabular}{lcccc}\n"
            "\\toprule \\toprule \n"
            "&\\multicolumn{2}{c}{UCI: $\\gamma\\in [0,2\\hat\\gamma]$}"
            "&\\multicolumn{2}{c}{LTZ: $\\gamma \\sim "
            "\mathcal{N}(\\mu_{\\hat\\gamma},\\sigma_{\\hat\\gamma})$}\\\\ \n" 
            "\\cmidrule(r){2-3} \\cmidrule(r){4-5}\n")

for i,line in enumerate(conli):
    if i<4:
        line = re.sub('\s+', dd, line) 
        line = re.sub('&$', ls+ls, line)
        line = line.replace('Plus', ' Plus')
        line = line.replace('Bound', ' Bound')
        line = line.replace('Bound\\\\', 'Bound\\\\ \\midrule')
        line = line.replace('\\midrule', 
                            '\\midrule \n \\multicolumn{5}{l}{Panel A: DHS}\\\\')
        conlo.write(line + "\n")
    if i==5:
        delta = line.replace('deltas', '')
        delta = re.sub('\s+', ', ', delta) 
        delta = re.sub(', $', '.', delta)
        delta = re.sub('^,', ' ', delta)
conlo.write('&&&& \\\\ \\midrule \\multicolumn{5}{l}{Panel B: USA (Education)}\\\\')
for i,line in enumerate(conlu):
    if i==1 or i==2 or i==3:
        line = re.sub('\s+', dd, line) 
        line = re.sub('&$', ls+ls, line)
        line = line.replace('E',' Plus')
        conlo.write(line + "\n")
conlo.write('&&&& \\\\ \\multicolumn{5}{l}{Panel B: USA (Health)}\\\\')
for i,line in enumerate(conlu):
    if i==4 or i==5 or i==6:
        line = re.sub('\s+', dd, line) 
        line = re.sub('&$', ls+ls, line)
        line = line.replace('H',' Plus')
        conlo.write(line + "\n")
    

conlo.write(mr+mc1+twid[3]+tcm[3]+mc3+
"This table presents upper and lower bounds of a 95\\% confidence interval  "
"for the effects of family size on (standardised) children's education      "
"attainment. These are estimated by the methodology of                      "
"\\citet{Conleyetal2012}  under various priors about the direct effect      "
"that being from a twin family has on educational outcomes ("+mi+ "gamma    "
+mo+"). In the UCI (union of confidence interval) approach, it is assumed   "
"the true "+mi+"gamma\\in[0,2\\hat\\gamma]"+mo+", while in the LTZ (local   "
"to zero) approach it is assumed that "+mi+"gamma\sim                       "
"\mathcal{N}(\\mu_{\\hat\\gamma},\\sigma_{\\hat\\gamma})"+mo+". The         "
"consistent estimation of $\\hat\\gamma$ and its entire distribution is     "
"discussed in appendix \\ref{TWINscn:gamma}.")

conlo.write("\\end{footnotesize}}  \n"
            "\\\\ \\bottomrule \\end{tabular}\\end{center}\\end{table} \n")


conlo.close()

#==============================================================================
#== (9) Create country list table
#==============================================================================
dhssi = open(dhss, 'r').readlines()
dhsso = open(Tables+"Countries."+end, 'w')

dhsso.write("%\\end{spacing}\\begin{spacing}{1} \n"
            "\\begin{longtable}{llccccccc}\n"
            "\\caption{Full Survey Countries and Years} \\\\ \n"
            "\\toprule\\toprule\\label{TWINtab:countries} \n"
            "& & \\multicolumn{7}{c}{Survey Year} \\\\ \\cmidrule(r){3-9} \n"
            "\\textsc{Country}&\\textsc{Income}&1&2&3&4&5&6&7\\\\ \\midrule \n")

country = "Chile"
counter=7
for i,line in enumerate(dhssi):
    countryn = re.search("\w+[-\,\'\w* ]*", line).group(0)
    countryn = countryn.replace("-"," ")
    income = re.search('Middle|Low',line).group(0)
    if countryn!= country:
        dif=7-counter
        counter = 0
        country=countryn
        if i==0:
            dhsso.write(countryn+dd+income)
        else:
            dhsso.write(dd*dif+ls+'\n'+country+dd+income)
    year = re.search("\d+", line).group(0)
    dhsso.write(dd+year)
    counter = counter + 1

dhsso.write(ls+"\n"+mr+mc1+twid[4]+tcm[4]+mc3+
"Country income status is based upon World Bank classifications described   "
"at http://data.worldbank.org/about/country-classifications and available   "
"for download at http://siteresources.worldbank.org/DATASTATISTICS/Resources"
"/OGHIST.xls (consulted 1 April, 2014). Income status varies by country and "
"time. Where a country's status changed between DHS waves only the most     "
"recent status is listed above.  Middle refers to both lower-middle and     "
"upper-middle income countries, while low refers just to those considered   "
"to be low-income economies.")

dhsso.write("\\end{footnotesize}}  \n"
            "\\\\ \\bottomrule \\end{longtable}\n"
            "%\\end{spacing}\\begin{spacing}{1.5}")


dhsso.close()

#==============================================================================
#== (10) Gender table
#==============================================================================
genfi = open(gend[0],'r').readlines
genmi = open(gend[1],'r').readlines

gendo = open(Tables+'Gender.'+end, 'w')


FB, FS, FN = plustable(gend[0],1,13,"fert",'normal',1000)
MB, MS, MN = plustable(gend[1],1,13,"fert",'normal',1000)


Ns = format(float(FN[0][0]), "n")+', '+format(float(MN[0][0]), "n")+', '
Ns = Ns + format(float(FN[0][3]),"n")+', '+format(float(MN[0][3]),"n")+', '
Ns = Ns + format(float(FN[0][8]),"n")+', '+format(float(MN[0][8]),"n")

gendo.write("\\begin{table}[htpb!]\\caption{Q-Q IV Estimates by Gender} \n"
            "\\label{TWINtab:gend}\\begin{center}\n"
            "\\begin{tabular}{lcccccccc} \\toprule \\toprule \n"
            "&\\multicolumn{4}{c}{Females}""&\\multicolumn{4}{c}{Males}\\\\ \n" 
            "\\cmidrule(r){2-5} \\cmidrule(r){6-9} \n" 
            "&Base&Socioec&Health&Obs.&Base&Socioec&Health&Obs. \\\\ \n"
            "\\midrule \n"+lineadd)

gendo.write("Two Plus "+dd+FB[0][0]+dd+FB[0][1]+dd+FB[0][2]+dd
            +format(float(FN[0][0]), "n")+dd
            +MB[0][0]+dd+MB[0][1]+dd+MB[0][2]+dd
            +format(float(MN[0][0]), "n")+ls+'\n'
            +dd+FS[0][0]+dd+FS[0][1]+dd+FS[0][2]+dd+dd
            +MS[0][0]+dd+MS[0][1]+dd+MS[0][2]+dd+ls+'\n' + lineadd +
            "Three Plus "+dd+FB[0][3]+dd+FB[0][4]+dd+FB[0][5]+dd
            +format(float(FN[0][3]), "n")+dd
            +MB[0][3]+dd+MB[0][4]+dd+MB[0][5]+dd
            +format(float(MN[0][3]), "n")+ls+'\n'
            +dd+FS[0][3]+dd+FS[0][4]+dd+FS[0][5]+dd+dd
            +MS[0][3]+dd+MS[0][4]+dd+MS[0][5]+dd+ls+'\n'+ lineadd +
            "Four Plus "+dd+FB[0][6]+dd+FB[0][7]+dd+FB[0][8]+dd
            +format(float(FN[0][8]), "n")+dd
            +MB[0][6]+dd+MB[0][7]+dd+MB[0][8]+dd
            +format(float(MN[0][8]), "n")+ls+'\n'
            +dd+FS[0][6]+dd+FS[0][7]+dd+FS[0][8]+dd+dd
            +MS[0][6]+dd+MS[0][7]+dd+MS[0][8]+dd+ls+'\n'
            +mr+mc1+twid[5]+tcm[5]+mc3+
            "Female or male refers to the gender of the index child of the    "
            "regression. All regressions include full controls including      "
            "socioeconomic and maternal health variables.  The full list of   "
            "controls are available in the notes to table "+rIVa+". Standard  "
            "errors are clustered by mother."+foot+"\n")
gendo.write("\\end{footnotesize}} \\\\ \\bottomrule \n"
            "\\end{tabular}\\end{center}\\end{table}")

gendo.close()


#==============================================================================
#== (11) IMR Test table
#==============================================================================
imrti = open(imrt, 'r').readlines()
imrto = open(Tables+"IMRtest."+end, 'w')

imrto.write("\\begin{table}[htpb!]\n"
            "\\caption{Test of hypothesis that women who bear twins have "
            "better prior health} \\label{TWINtab:IMR} \n"
            "\\begin{center}\\begin{tabular}{lccc}"
            "\\toprule \\toprule \n"
            "\\textsc{Infant Mortality (per 100 births)}"
            "& Base & +S\\&H & Observations \\\\ \\midrule \n"
            "\\begin{footnotesize}\\end{footnotesize}& \n"
            "\\begin{footnotesize}\\end{footnotesize}& \n"
            "\\begin{footnotesize}\\end{footnotesize}& \n"
            "\\begin{footnotesize}\\end{footnotesize}\\\\ \n")
for i,line in enumerate(imrti):
    if re.match("treated", line):
        index=i
    if re.match("N", line):
        ind2=i


betas = imrti[index].split()
ses   = imrti[index+1].split()
Ns    = imrti[ind2].split()

imrto.write('Treated (2+)'+hs*6+dd+betas[1]+dd+betas[3]+dd+Ns[2]+ls+'\n'
            +dd+ses[0]+dd+ses[2]+dd+ls+'\n'
            'Treated (3+)'+hs+dd+betas[4]+dd+betas[6]+dd+Ns[4]+ls+'\n'
            +dd+ses[3]+dd+ses[5]+dd+ls+'\n'
            'Treated (4+)'+dd+betas[7]+dd+betas[9]+dd+Ns[7]+ls+'\n'
            +dd+ses[6]+dd+ses[8]+dd+ls+'\n'
            'Treated (5+)'+dd+betas[10]+dd+betas[12]+dd+Ns[10]+ls+'\n'
            +dd+ses[9]+dd+ses[11]+dd+ls+
            '\n'+mr+mc1+twid[6]+tcm[6]+mc3+
            "The sample for these regressions consist of all children who    "
            "have been entirely exposed to the risk of infant mortality (ie  "
            "those over 1 year of age). Subsamples 2+, 3+, 4+ and 5+ are     "
            "generated to allow comparison of children born at similar birth "
            "orders. For a full description of these groups see the the body "
            "of the paper or notes to table "+rIVa+". Treated=1 refers to    "
            "children who are born before a twin while Treated=0 refers to   "
            "children of similar birth orders not born before a twin. Base   "
            "and S+H controls are described in table" +rIVa+"."+foot+" \n")

imrto.write("\\end{footnotesize}} \\\\ \\bottomrule \n"
            "\\end{tabular}\\end{center}\\end{table}")


#==============================================================================
#== (12) First stage table
#==============================================================================
fstao = open(Tables+"firstStage."+end, 'w')

fstao.write("\\begin{landscape}\\begin{table}[htpb!]"
            "\\caption{First Stage Results} \n"
            "\\label{TWINtab:FS}\\begin{center}"
            "\\begin{tabular}{lcccp{2mm}cccp{2mm}ccc}\n\\toprule \\toprule \n"
            "&\\multicolumn{3}{c}{2+}&&\\multicolumn{3}{c}{3+}&&"
            "\\multicolumn{3}{c}{4+}\\\\ \\cmidrule(r){2-4}\\cmidrule(r){6-8}"
            "\\cmidrule(r){10-12} \n"
            "\\textsc{Fertility}&Base&+H&+S\&H&&Base&+H&+S\&H&&Base&+H&+S\&H"
            "\\\\ \\midrule \n"
            +"\\begin{footnotesize}\\end{footnotesize}& \n"*9+
            "\\begin{footnotesize}\\end{footnotesize}\\\\ \n")

AllB = []
AllS = []
AllN = []
LowB = []
LowS = []
LowN = []
MidB = []
MidS = []
MidN = []
TwiB = []
TwiS = []
TwiN = []
AdjB = []
AdjS = []
AdjN = []

for num in ['two','three','four']:
    searcher='twin\_'+num+'\_fam'
    Asearcher='ADJtwin\_'+num+'\_fam'
    searchup=searcher+'|twin'+num
    if num=='two':
        N = 0
    elif num=='three':
        N = 4
    else:
        N = 8

    FSB, FSS, FSN    = plustable(firs, 1, 13,searcher,'normal',1000)
    FLB, FLS, FLN    = plustable(flow, 1, 13,searcher,'normal',1000)
    FMB, FMS, FMN    = plustable(fmid, 1, 13,searcher,'normal',1000)


    AllB.append(dd + FSB[0][0] + dd + FSB[0][1] + dd + FSB[0][2])
    AllS.append(dd + FSS[0][0] + dd + FSS[0][1] + dd + FSS[0][2])
    AllN.append(dd + FSN[0][N] + dd + FSN[0][N+1] + dd + FSN[0][N+2])
    LowB.append(dd + FLB[0][0] + dd + FLB[0][1] + dd + FLB[0][2])
    LowS.append(dd + FLS[0][0] + dd + FLS[0][1] + dd + FLS[0][2])
    LowN.append(dd + FLN[0][N] + dd + FLN[0][N+1] + dd + FLN[0][N+2])
    MidB.append(dd + FMB[0][0] + dd + FMB[0][1] + dd + FMB[0][2])
    MidS.append(dd + FMS[0][0] + dd + FMS[0][1] + dd + FMS[0][2])
    MidN.append(dd + FMN[0][N] + dd + FMN[0][N+1] + dd + FMN[0][N+2])



fstao.write(mc1+twid[10]+mcbf+"All"+mc2+ls+" \n"
            "Twin"+AllB[0]+dd+AllB[1]+dd+AllB[2]+ls+'\n'
            +AllS[0]+dd+AllS[1]+dd+AllS[2]+ls+'\n'+lA2+
            "Observations"+AllN[0]+dd+AllN[1]+dd+AllN[2]+ls+'\n'+lA2+

            mc1+twid[10]+mcbf+"Low-Income"+mc2+ls+" \n"
            "Twin"+LowB[0]+dd+LowB[1]+dd+LowB[2]+ls+'\n'
            +LowS[0]+dd+LowS[1]+dd+LowS[2]+ls+'\n'+lA2+
            "Observations"+LowN[0]+dd+LowN[1]+dd+LowN[2]+ls+'\n'+lA2+

            mc1+twid[10]+mcbf+"Middle-Income"+mc2+ls+" \n"
            "Twin"+MidB[0]+dd+MidB[1]+dd+MidB[2]+ls+'\n'
            +MidS[0]+dd+MidS[1]+dd+MidS[2]+ls+'\n'+lA2+
            "Observations"+MidN[0]+dd+MidN[1]+dd+MidN[2]+ls+'\n')

fstao.write('\n'+mr+mc1+twid[12]+tcm[12]+mc3+
            "Each cell represents the coefficient from the first-stage of a   "
            "two-stage regression.  The first-stage represents the effect of  "
            "twinning at parity $N$ on total fertility where $N$ is 2, 3 or 4 "
            "for 2+, 3+ and 4+ groups respectively. The 2+ group includes all "
            "first borns in families with at least 2 births, the 3+ group     "
            "includes first and second borns in families with at least 3      "
            "births, and the 4+ group includes all first to third borns in    "
            "families with at least four births.  In each regressions the     "
            "sample is made up of all children aged between 6-18 years from   "
            "families in the DHS who fulfill these birth order conditions.    "
            "Controls in each case are identical to those described in table  "
            +rIVa+".  Standard errors are clustered at the level of the       "
            "mother."+foot+" \n")
fstao.write("\\end{footnotesize}} \\\\ \\bottomrule \n"
            "\\end{tabular}\\end{center}\\end{table}\\end{landscape}")



#==============================================================================
#== (13) Gamma table
#==============================================================================
gammi = open(gamT, 'r')
gammo = open(Tables+'gamma.'+end, 'w')

gammo.write("\\begin{table}[!htbp] \\begin{center} \n"
            "\\caption{Consistent Estimates of $\\gamma$ Using a Maternal "
            "Health Shock} \n "
            "\\label{TWINtab:gamma} \n"
            "\\begin{tabular}{lcccc} \\toprule \\toprule \n"
            "&$\\frac{\\partial Educ}{\\partial Health}$ "
            "&$\\frac{\\partial Health}{\\partial Twin}$ "
            "&$\\gamma=-\\frac{\\partial Educ}{\\partial Twin}$" 
            "&$\\gamma$ (bootstrap) \\\\ \\midrule \n")


for i,line in enumerate(gammi):
    if i==3: EstA = line.split()[1]
    if i==4: SeA  = line.split()[0]
    if i==5: EstB = line.split()[1]
    if i==6: SeB  = line.split()[0]
    if i==10: obs = line.replace('\t','&')
    if i==11: rsq = line.replace('\t','&')

gammaEst = str(float(EstA[0:6])*abs(float(EstB[0:6])))[0:6]

gammo.write('Estimate &'+EstA+'&'+EstB+'&'+gammaEst+'&'+gammaEst+'\\\\ \n'
            '&'+SeA+'&'+SeA+'&&(0.0027)\\\\  \n'
            '&&&&\\\\ \n'+obs+'&&\\\\ \n'+rsq+'&&\\\\ \\midrule \n')

gammo.write('\n'+mr+mc1+twid[13]+tcm[13]+mc3+ "Regression results for         "
            "(\\ref{TWINeqn:BV1}) and (\\ref{TWINeqn:BV2}) use the 5\% sample "
            "of 1980 census data. Specifications and samples are identical to "
            "those described in \\citet{BhalotraVenkataramani2014}. The       "
            "estimate of $\gamma$ is formed by taking the product of panel A  "
            "and panel B estimates. A full description of this process, along "
            "with the non-pivotal bootstrap process to estimate the standard  "
            "error of $\\gamma$ is provided in appendix \\ref{TWINscn:gamma}, "
            "and figure \\ref{TWINfig:gammaBootsN}")

gammo.write("\\end{footnotesize}}\\\\  \n"
            "\\bottomrule\\end{tabular}\\end{center}\\end{table} \n")

gammo.close()

#==============================================================================
#== (14) NHIS Results
#==============================================================================
NHISo = open(Tables+'AllNHIS.'+end, 'w')


NHISo.write('\\begin{landscape}\\begin{table}[htpb!] \n'
            '\\caption{NHIS Estimates: Education and Health}'
            '\\label{TWINtab:NHISAll}\n'
            '\\begin{center}\\begin{tabular}{lccccccccc}\n'
            '\\toprule \\toprule\n' 
            '&\\multicolumn{3}{c}{2+}&\\multicolumn{3}{c}{3+}&'
            '\\multicolumn{3}{c}{4+}\\\\ \\cmidrule(r){2-4}'
            '\\cmidrule(r){5-7} \\cmidrule(r){8-10}\n' 
            '&Base&+H&+S\\&H&Base&+H&+S\\&H&Base&+H&+S\\&H\\\\ \\midrule\n' 
            +'\\begin{footnotesize}\\end{footnotesize}&'*9+
            '\\begin{footnotesize}\\end{footnotesize}\\\\' 
            '\\multicolumn{10}{l}{\\textbf{OLS}}\\\\')

wT = open(Results+"NHIS/OLSFertEducationZscore.xls", 'r')
for i, line in enumerate(wT):
    if i==2 or i==3:   
        line = line.replace('fert','School Z-Score')
        line = line.replace('\t', '&')
        NHISo.write(line+'\\\\ \n')
wT = open(Results+"NHIS/OLSFertexcellentHealth.xls", 'r')
for i, line in enumerate(wT):
    if i==2 or i==3:   
        line = line.replace('fert','Excellent Health')
        line = line.replace('\t', '&')
        NHISo.write(line+'\\\\ \n')

if ftype=='tex':
    NHISo.write('\\begin{footnotesize}\\end{footnotesize}&'*9+
                '\\begin{footnotesize}\\end{footnotesize}\\\\ \n' 
                '\\multicolumn{10}{l}{\\textbf{IV}}\\\\ \n') 
wT = open(Results+"NHIS/IVFertEducationZscore.xls", 'r')
for i, line in enumerate(wT):
    if i==2 or i==3:   
        line = line.replace('fert','School Z-Score')
        line = line.replace('\t', '&')
        NHISo.write(line+'\\\\ \n')
wT = open(Results+"NHIS/IVFertexcellentHealth.xls", 'r')
for i, line in enumerate(wT):
    if i==2 or i==3:   
        line = line.replace('fert','Excellent Heatlth')
        line = line.replace('\t', '&')
        NHISo.write(line+'\\\\ \n')
    if i==35:
        line    = line.replace('N','Observations')
        ObsNHIS = line.replace('\t','&')

if ftype=='tex':
    NHISo.write('\\begin{footnotesize}\\end{footnotesize}&'*9+
                '\\begin{footnotesize}\\end{footnotesize}\\\\ \n' 
                '\\multicolumn{10}{l}{\\textbf{First Stage}}\\\\ \n') 

for var in ['EducationZscore','excellentHealth']:
    wT = open(Results+"NHIS/IVFert"+var+"1.xls", 'r')
    if var=='EducationZscore': vname = 'School Z-Score'
    if var=='excellentHealth': vname = 'Excellent Health'

    for i, line in enumerate(wT):
        if i==2:   
            line = line.replace('twin_two_fam',vname)
            line1 = line.replace('\t', '&')
            line1 = line1[:-7]
        if i==34:
            line = line.replace('twin_three_fam',' ')
            line2 = line.replace('\t', '&')
            line2 = line2[4:-4]
        if i==36:
            line = line.replace('twin_four_fam',' ')
            line3 = line.replace('\t', '&')
            line3 = line3[7:]
            NHISo.write(line1+line2+line3+'\\\\ \n')
        if i==3:   
            line4 = line.replace('\t', '&')
            line4 = line4[:-7]
        if i==35:
            line5 = line.replace('\t', '&')
            line5 = line5[4:-4]
        if i==37:
            line6 = line.replace('\t', '&')
            line6 = line6[7:]
            NHISo.write(line4+'&'+line5+'&'+line6+'\\\\ \n')

NHISo.write('&&&&&&&&&\\\\\n&&&&&&&&&\\\\\n'+ObsNHIS+'\\\\ \n'
            'Joint F-test Educ (IV)'
            '&&164.5&64.7&&101.3&39.6&&38.0&7.7\\\\\n'
            'Joint F-test Health (IV)'
            '&&34469.6&163.9&&15335.6&28.4&&5276.4&17.1\\\\')

NHISo.write('\n'+mr+mc1+twid[14]+tcm[14]+mc3+
            "Each cell presents the coefficient of interest from a regression "
            "using NHIS survey data (2004-2014). Base controls include child  "
            "age FE (in months), mother's age, and mother's age at first birth" 
            " plus race dummies for child and mother. In each case the sample "
            "is made up of all children aged between 6-18 years from families "
            "in the NHIS who fulfill 2+ to 4+ requirements. Descriptive statis"
            "tics for each variable can be found in table                     "
            " \\ref{TWINtab:NHISstats}. Standard errors are clustered at the  "
            "level of the mother.")

NHISo.write("\\end{footnotesize}} \\\\ \\bottomrule \n"
            "\\end{tabular}\\end{center}\\end{table}\\end{landscape}")

NHISo.close()

#==============================================================================
#== (X) Close
#==============================================================================
print "Terminated Correctly."
