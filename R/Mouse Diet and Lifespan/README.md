# Description

This folder includes statistical analyis and modelling of a publically-available dataset that was included within a Nature article from October 2024: 
> Francesco _et al._ (2024) "Dietary restriction impacts health and lifespan of genetically diverse mice" _Nature_ **634**, 684–692. doi: 10.1038/s41586-024-08026-3

The datasets includes statistics on the life- and healthspan of genetically outbred female mice. The cohort (_n_ = 960) was equally divided into five separate intervention groups (_n_ = 192 each): _Ad libitum_ (AL), 1-day fasting (1D), 2-day fast (2D), 20% caloric restriction wrt AL group (20%), 40% caloric restriction wrt AL group (40%).

# Files

## Reporting
* 2421232_report.pdf = Writeup of the results and statistical analyses
* analysis_code.md = R markdown code used in the analysis

## Datasets
2 CSV files

### AnimalData_Processed_20230712.csv
CSV file with 18 columns:
* MouseID - individual Mouse ID
* Generation - Generation of mice (G22 - G28)
* Cohort - Cohort per generation e.g which week the interventions were conducted G28 Week 1
* JobGroup - Day of cohort intervention
* BWDay - Date of body weight measurement
* HID
* LHID
* Diet - Diet regimen
* EN
* Coat - Coat colour
* Status
* DOB - Date of Birth
* DOE - Date
* COE
* SurvDays
* Died
* AnimalComments	
* CAST

### WeeklyBW_Processed_20230712.csv
CSV with 14 columns. Information derived from author-provided ReadMe:
* MouseID			Unique identifier for each mouse in form of "DO" (indicating the mice are diversity outbred mice), '-', 'XX' (indicating the diet group of the mice), '-', '####' (unique numeric code for each mouse)
* BWDay			The day of the week on which the weekly BW was usually recorded (calculated from raw weekly BW data)
* AgeInDays		The age (in days) of the mouse at the time of the assay
* BW_LOESS		The smoothed BW (grams) of the mouse. The BWs were smoothed using a LOESS algorithm in R, see the data processing script for details. Importantly, the BWs collected before 6 months of age were smoothed without using BW data collected after 6 months of age so that there would be no way for the diet interventions to affect smoothed BWs before the start of the intervention.
* BW_Raw			The raw BW (grams) of the mouse (identical to the "BW" column in the raw data file, FROZEN_BW_DATA).
* BW_LagMean		The mean (grams) of raw BWs measured within one month previous to the collected date
* BW_LagVar		The variance (grams squared) of raw BWs measured within one month previous to the collected date
* BW_LagSlope		The relative change (percent change per month) (ln[raw BW] ~ age) in BW over the previous month
* BW_LagResidMSE		The mean squared error of the residuals of the regression of natural-log raw BW onto age over the past month
* LagN			The number of BWs recorded in the past month (the number of records used to calculate the lag statistics above)
* DateCollect		The date of collection
* Tech			The technician who performed the assay (coded as letters to ensure anonymity of the techinicians)
* DaysSinceFast		The number of days between when the mouse was last fasted and the time of the assay (zeroes indicate done during time of fast or the day the food was returned [mice are generally fed between 12-2 pm and phenotyped between 8 am and 12pm], NA for ad libitum mice because they never experience a fast)
* Comments		Batch comments refer to an entire assay batch, sample comments refer to an individual sample within the batch
