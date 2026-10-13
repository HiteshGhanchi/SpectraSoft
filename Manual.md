# INSTRUCTION MANUAL

QC-E1 Ver 1.1 

DATA PROCESSING SYSTEM 

FOR 

EMISSION SPECTRAL ANALYZER 

SHIMADZU CORPORATION
ELEMENTS & SURFACE ANALYSIS EQUIPMENT DIVISION
ELEMENTS ANALYSIS EQUIPMENT PLANT
KYOTO, JAPAN 

## TABLE OF CONTENTS

1. EMISSION SPECTRAL ANALYTICAL METHOD (INTRODUCTION) 1-1
1.1 Principle 1-1
1.2 Recommendations 1-2
1.3 Preparation of an Analysis 1-4
1.4 Registration of Analytical Informations 1-7
1.5 Preliminary Operations for Quantitative Analysis 1-7
1.6 Daily Analytical Procedure 1-9
1.7 Factors of Analytical Accuracy and Error 1-10
1.8 Registration of Working Curve 1-14
1.9 Change of Sample for Recalibration 1-15
2. SYSTEM CONFIGURATION 2-1
2.1 Terms and Concepts 2-2
2.2 System Start and Stop 2-4
2.3 Basic Use of Keyboard 2-6
2.4 Program Configuration Diagram 2-12
3. ANALYTICAL DATA PROCESSING SPECIFICATIONS 3-1
4. MASTER MENU 4-1
5. CONFIGURATION INDEX OF ANALYTICAL INFORMATION 5-1
5.1 Sequence to Register Analytical Information 5-2
5.2 Preparation of Analytical Information 5-10
5.3 Registration of Analytical Group Name 5-14
5.4 Registration of Analytical Condition 5-16
5.5 Registration of Attenuator (ATT) Settings 5-20
5.6 Registration of Order of Analytical Channel and Sequence, Internal Standard Element 5-21
5.7 Registration of Drift Correction Target Value 5-24
5.8 Registration of Working Curve Coefficients, 100% Correction and Channel Skip 5-27
5.9 Registration of Matrix Element Correction Coefficients 5-32 

5.10 Registration of the Master Curve Correction Sample and Target Value .... 5-35
5.11 Registration of the Analytical Element Display and Printing Order .... 5-37
5.12 Registration of the Data Transmission Format .... 5-39
5.13 Registration of the Purity Calculation Information .... 5-41
5.14 Registration of Standard Name and Standard Value .... 5-42
5.15 Registration R Control Value .... 5-45
5.16 Registration of Special Calculation Formula .... 5-48
5.17 Analytical Information Copy .... 5-56
5.18 Registration of Element Name and Wavelength .... 5-58
5.19 Registration of Histogram Control Value .... 5-59
5.20 Registration of the Analytical Group Using Same Analytical Condition .... 5-62
6. ADJUSTMENT OF ATTENUATOR SENSITIVITY .... 6-1
7. REGRESSION CALCULATION .... 7-1
7.1 Registration of Chemical Analytical Value .... 7-3
7.2 Registration of Standard Sample .... 7-7
7.3 Calculation of Working Curve Coefficient .... 7-12
7.4 Matrix Element Correction .... 7-21
7.5 Matrix Element Correction Coefficient Calculation Type 1 (Two-Element Method) .... 7-25
7.6 Matrix Element Correction Coefficient Calculation Type 2 (Multi-Element Method) .... 7-38
8. ANALYTICAL OPERATION (CONTENT ANALYSIS) .... 8-0
8.1 Basic Operation Method .... 8-1
8.2 Analytical Procedure .... 8-4
8.3 Selection of Analytical Job .... 8-5
8.4 Setting of Operation Mode O .... 8-8
8.5 Content Analysis .... 8-14
8.6 Modification and Cancel Analytical Value .... 8-17
8.7 Three-Time Analysis .... 8-22
8.8 Master Curve Recalibration Analysis or Type Standard Analysis .... 8-24 

9. ANALYTICAL OPERATION (INSTRUMENT CORRECTION OPERATION & ANALYTICAL INTENSITY MEASUREMENT) 9-0
9.1 Basic Operation Method 9-1
9.2 Selection of Analytical Job 8-3
9.3 Setting of Operation Mode O 9-5
9.4 Two-Point Recalibration Standardization Analysis 9-8
9.5 One-Point Recalibration Standardization Analysis 9-10
9.6 INT. Two-Point for Recalibration/Analysis of Target Value for Standardization 9-12
9.7 INT. 2 for Working Curve Intensity Measurement for Working Curve Creation 9-14
9.8 INT. 2 (Drift Corrected Intensity) Post-Correction Intensity Measurement 9-16
9.9 INT. 1 (Raw Intensity) Pre-Correction Intensity Measurement 9-18
10. DATA REPORT 10-1
10.1 Data Print Out 10-3
10.2 Long Term Repeatability Check 10-10
10.3 Analytical Frequency 10-15
10.4 Stability Check 10-17
10.5 Data Modification 10-21
10.6 Histogram 10-24
11. MAINTENANCE 11-1
11.1 Waste Discharge 11-3
11.2 Manual Scanning 11-4
11.3 Lamp Test 11-7
11.4 Date and Time Setting 11-8
11.5 System Backup 11-9
11.6 Information of Maintenance 11-14
11.7 TAN (Total Number of Emission Times) Clear 11-23 

## 1. EMISSION SPECTRAL ANALYTICAL METHOD

## Introduction

1.1 Principle 

1.2 Recommendations 

1.3 Preparation of an Analysis 

1.4 Registration of Analytical Information 

1.5 Preliminary Operations for Quantitative Analysis 

1.6 Daily Analytical Procedure 

1.7 Factors of Analytical Accuracy and Error 

1.8 Registration of Working Curve 

1.9 Change of Sample for Recalibration 

## 1. EMISSION SPECTRAL ANALYTICAL METHOD (INTRODUCTION)

For several decades, Arc or Spark discharge has been used as an excitation method in emission spectrochemical analysis. An application of this method is to conduct simultaneous quantitative analysis of more than one element contained in a metal. In modern industry, it has become an indispensable method of analysis for on-line control purposes. It is used to define chemical composition with accuracy and speed, and to control melt composition within an objective range. 

Basically, the Arc/Spark spectrometer is the same as the conventional spectrograph. The only difference is the replacement of the conventional photographic plate with exit slits and photo-multiplier tubes. An electronic readout unit and a microcomputer automatically measure the spectral intensity from each element. The provided software is a fully integrated package controlling the operation of the instrument, as well as, data acquisition and analysis. 

## 1.1 Principle

The creation of an electrical (either Arc or Spark) discharge between a sample and a counterelectrode generates an emission of light. The spectra of the emitted light is characteristic of the composition of the given sample. The quantitative determination of an element is done by photoelectrically measuring the intensity of its characteristic wavelength. 

An electrical discharge from the excitation source unit excites the sample to be analyzed. 

The light given off during this process passes through the entrance slit and is focused on the concave grating. The grating disperses the light into its component wavelengths. 

The light from each preselected wavelength is gathered and converted to a photo-current by a photo-multiplier tube. The photo-current is a measure of the intensity of the spectral line. 

The intensity of the spectral line has a fixed relationship with the concentration of that element contained in the sample. For each element, a working curve is calculated by using the standard samples. The intensity of the spectral lines of the unknown sample referenced to as the 'working curve', determines the concentration of a given element in the unknown sample. (Both working curve and standard samples will be explained later) 

```txt
Temperature : 23°C + 5°C or 77°F + 8°F
Relative humidity : 40 - 70%, non-condensing environment
Any significant change in room temperature will cause a drift in the spectrometer's optical alignment. An increase in the humidity can cause a change in the dark current of the photo-multiplier tubes. Leakage of the insulating material may also occur, resulting in unstable measurements. 
```

```txt
The software QC-El described in this manual, allows the operator to:
- Control, regulate, and maintain the spectrometer
- Calibrate the instrument
- Standardize the instrument
- Analyze unknown samples
- Verify the specification of the unknown samples
- Calculate a final addition
- Establish a report following the "Statistical Process Control" guideline 
```

## 1.2 Recommendations

The Shimadzu Emission Spectrometer is a precision instrument designed to provide analyses of the highest quality. To ensure that the system operates at peak performance, we recommend that you read and understand the provider manuals before attempting to operate the instrument. 

```txt
Operating specifications:
1) Room
Proper operation of the instrument requires that room temperature and humidity remain within the specified ranges. 
```

## 2) Electrical requirements

For a spectrometer equipped with the HPSG300 source unit, the electrical requirement is: 

```txt
- One service, dedicated, three-phase (3φ), 220V AC, 30A, 50/60 Hz
A fluctuation of the supply voltage exceeding +10% changes the discharge voltage of the emission unit and will affect the analytical results.
Supply voltage stability:
1- Better than 10% = Optimum operation
2- Worse than 10% = non acceptable - We recommend the installation of a line conditioner 
```

3) Argon purity 

The discharge is performed in a closed chamber of Argon (Ar) gas. The excitation vaporization phenomenon is directly dependent on the efficiency of the electrical discharge. The purity of the argon gas used is very important to guarantee the repeatability of the discharge. The analysis of some samples containing large amount of Silicon or Aluminum may be difficult if the content of Oxygen ( $O_{2}$ ) in the Argon gas is too high. (Very distinctive "milky" burns may result from a high content of Oxygen) 

Argon requirements: 

Argon : 99.999% or more 

Oxygen : 0.0001% or less 

Nitrogen: 0.0005% or less 

Hydrogen: 0.0003% or less 

Moisture: 0.0043 mg/l or less 

4) Instrument checks 

A Shimadzu engineer will install the instrument and define all operating parameters for each application. However, before attempting to operate the instrument, it is recommended that all maintenance procedures be reviewed and understood. 

* Adjustment of the Control Gap 

Form and adjust an electrode surface at the control gap of HPSG-300 igniter (see Maintenance manual of the Source included with the Instruction manual). 

* Cleanliness of the Argon Emission Stand 

The action of the electrical discharge at the sample surface generates some dust. 

The stream of Argon eliminates a large portion of the dust. The small amount that remains will deposit in the spark chamber. Over time the accumulated dust may contaminate and damage the electrical isolation of the stand. 

(See Chapter 4, Excitation stand, Argon stand of the instruction Manual for the procedure to clean the stand) 

## * Counterelectrode

The form and the position of the counterelectrode have a direct effect on the electrical discharge. After repeated electrical discharges, the tip of the counterelectrode may become deformed. The counterelectrode must be cleaned or replaced every 300 burns. The current number of burns for the electrode is displayed on the low right side of the screen as TAN:# 

## * Maintenance status

The level of vacuum and internal temperature should be verified (section 11-8). An inappropriate level of vacuum and/or temperature will affect the optical alignment. 

(See Software manual: Maintenance section) 

## 1.3 Preparation of an Analysis

A quantitative determination by chemical analysis is an absolute method, where as emission spectrometry is a relative method. For a given element, the intensity of its characteristic spectral line is proportional to its concentration. Using this relationship, the content of an unknown sample can be determined by comparing the intensity of its spectral lines to that of a known sample. At the time of installation, a series of standard samples were analyzed. A plot of the measured intensity versus concentration is registered as the "working curve" for each element of the application. During an analysis the data system automatically compares the measured intensity of the unknown element with its working curve and the resultant concentration displayed. The results of the quantitative analysis depends on the accuracy of the elemental analysis of the standard samples. 

## 1) Standard samples

A standard sample is a material which can be used as a reference. There are several classes of standard samples, such as: 

- Homemade or in-house standards 

Samples produced internally do not have an analytical certificate. Therefore, these samples should be used with caution. 

## - Secondary standards

These standard samples are commercially available. A certificate of analysis is provided, but their traceability to a standard reference material is not guaranteed. 

- Standard reference materials 

Standard samples of this type are produced following a strict protocol. These materials are used to rule any conflict between a supplier and a customer. In the US, these standard samples are produced by NIST. Reference materials from Europe or Japan are also available. 

2. $\frac{1}{2}$ . 

1. $\frac{1}{2}$ (a) $\frac{1}{2}$ (b) $\frac{1}{2}$ (c) 

1. 2014年1月1日

(1) $\frac{1}{2}$ (2) $\frac{1}{2}$ (3) $\frac{1}{2}$ (4) $\frac{1}{2}$ (5) $\frac{1}{2}$ (6) $\frac{1}{2}$ (7) $\frac{1}{2}$ (8) $\frac{1}{2}$ (9) $\frac{1}{2}$ (10) 

1. 2017年1月1日至2018年1月1日，公司与上海浦东发展银行股份有限公司签订了《最高额保证合同》，双方均无任何关联关系。

$\therefore {a}_{1} = \frac{b}{c}$ 且 $b > 0$ ,则 $c$ 的多项式.

1.  \( \frac{1}{2} \) ,  \( \frac{1}{3} \) ,  \( \frac{1}{4} \) ,  \( \frac{1}{5} \) ,  \( \frac{1}{6} \) ,  \( \frac{1}{7} \) ,  \( \frac{1}{8} \) ,  \( \frac{1}{9} \) ,  \( \frac{1}{10} \) ,  \( \frac{1}{11} \) ,  \( \frac{1}{12} \) ,  \( \frac{1}{13} \) ,  \( \frac{1}{14} \) ,  \( \frac{1}{15} \) ,  \( \frac{1}{16} \) ,  \( \frac{1}{17} \) ,  \( \frac{1}{18} \) ,  \( \frac{1}{19} \) ,  \( \frac{1}{20} \) ,  \( \frac{1}{21} \) ,  \( \frac{1}{22} \) ,  \( \frac{1}{23} \) ,  \( \frac{1}{24} \) ,  \( \frac{1}{25} \) ,  \( \frac{1}{26} \) ,  \( \frac{1}{27} \) ,  \( \frac{1}{28} \) ,  \( \frac{1}{29} \) ,  \( \frac{1}{30} \) ,  \( \frac{1}{31} \) ,  \( \frac{1}{32} \) ,  \( \frac{1}{33} \) ,  \( \frac{1}{34} \) ,  \( \frac{1}{35} \) ,  \( \frac{1}{36} \) ,  \( \frac{1}{37} \) ,  \( \frac{1}{38} \) ,  \( \frac{1}{39} \) ,  \( \frac{1}{40} \) ,  \( \frac{1}{41} \) ,  \( \frac{1}{42} \) ,  \( \frac{1}{43} \) ,  \( \frac{1}{44} \) ,  \( \frac{1}{45} \) ,  \( \frac{1}{46} \) ,  \( \frac{1}{47} \) ,  \( \frac{1}{48} \) ,  \( \frac{1}{49} \) ,  \( \frac{1}{50} \) ,  \( \frac{1}{51} \) ,  \( \frac{1}{52} \) ,  \( \frac{1}{53} \) ,  \( \frac{1}{54} \) ,  \( \frac{1}{55} \) ,  \( \frac{1}{56} \) ,  \( \frac{1}{57} \) ,  \( \frac{1}{58} \) ,  \( \frac{1}{59} \) ,  \( \frac{1}{60} \) ,  \( \frac{1}{61} \) ,  \( \frac{1}{62} \) ,  \( \frac{1}{63} \) ,  \( \frac{1}{64} \) ,  \( \frac{1}{65} \) ,  \( \frac{1}{66} \) ,  \( \frac{1}{67} \) ,  \( \frac{1}{68} \) ,  \( \frac{1}{69} \) ,  \( \frac{1}{70} \) ,  \( \frac{1}{71} \) ,  \( \frac{1}{72} \) ,  \( \frac{1}{73} \) ,  \( \frac{1}{74} \) ,  \( \frac{1}{75} \) ,  \( \frac{1}{76} \) ,  \( \frac{1}{77} \) ,  \( \frac{1}{78} \) ,  \( \frac{1}{79} \) ,  \( \frac{1}{80} \) ,  \( \frac{1}{81} \) ,  \( \frac{1}{82} \) ,  \( \frac{1}{83} \) ,  \( \frac{1}{84} \) ,  \( \frac{1}{85} \) ,  \( \frac{1}{86} \) ,  \( \frac{1}{87} \) ,  \( \frac{1}{88} \) ,  \( \frac{1}{89} \) ,  \( \frac{1}{90} \) ,  \( \frac{1}{91} \) ,  \( \frac{1}{92} \) ,  \( \frac{1}{93} \) ,  \( \frac{1}{94} \) ,  \( \frac{1}{95} \) ,  \( \frac{1}{96} \) ,  \( \frac{1}{97} \) ,  \( \frac{1}{98} \) ,  \( \frac{1}{99} \) ,  \( \frac{20000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 

1. $\frac{1}{2}$ (1) $\frac{1}{2}$ (2) $\frac{1}{2}$ (3) $\frac{1}{2}$ 

. . . . . . . . . 

1. $a_{1}$ , $b_{1}$ , $c_{1}$ , $d_{1}$ , $e_{1}$ , $f_{1}$ , $g_{1}$ , $h_{1}$ , $i_{1}$ , $j_{1}$ , $k_{1}$ , $l_{1}$ , $m_{1}$ , $n_{1}$ , $o_{1}$ , $P_{1}$ , $Q_{1}$ , $R_{1}$ , $S_{1}$ , $T_{1}$ , $U_{1}$ , $V_{1}$ , $W_{1}$ , $X_{1}$ , $Y_{1}$ , $Z_{1}$ , $AA_{1}$ , $AB_{1}$ , $AC_{1}$ , $AD_{1}$ , $AE_{1}$ , $AF_{1}$ , $AG_{1}$ , $AH_{1}$ , $AI_{1}$ , $AJ_{1}$ , $AK_{1}$ , $AL_{1}$ , $AM_{1}$ , $AN_{1}$ , $AO_{1}$ , $AP_{1}$ , $AQ_{1}$ , $AR_{1}$ , $AS_{1}$ , $AT_{1}$ , $AU_{1}$ , $AV_{1}$ , $AW_{1}$ , $AX_{1}$ , $AY_{1}$ , $AZ_{1}$ , $BA_{1}$ , $BB_{1}$ , $BC_{1}$ , $BD_{1}$ , $BE_{1}$ , $BF_{1}$ , $BG_{1}$ , $BH_{1}$ , $BI_{1}$ , $BJ_{1}$ , $BK_{1}$ , $BL_{1}$ , $BM_{1}$ , $BN_{1}$ , $BO_{1}$ , $BP_{1}$ , $BP_{2}$ , $BP_{3}$ , $BP_{4}$ , $BP_{5}$ , $BP_{6}$ , $BP_{7}$ , $BP_{8}$ , $BP_{9}$ , $BP_{10}$ , $BP_{11}$ , $BP_{12}$ , $BP_{13}$ , $BP_{14}$ , $BP_{15}$ , $BP_{16}$ , $BP_{17}$ , $BP_{18}$ , $BP_{19}$ , $BP_{20}$ , $BP_{21}$ , $BP_{22}$ , $BP_{23}$ , $BP_{24}$ , $BP_{25}$ , $BP_{26}$ , $BP_{27}$ , $BP_{28}$ , $BP_{29}$ , $BP_{30}$ , $BP_{31}$ , $BP_{32}$ , $BP_{33}$ , $BP_{34}$ , $BP_{35}$ , $BP_{36}$ , $BP_{37}$ , $BP_{38}$ , $BP_{39}$ , $BP_{40}$ , 

2) Number of standard samples required to generate an accurate working curve 

The accuracy of a working curve depends on the number of analyzed standard samples. 

Factors that determine the number necessary are, the sample matrix, the 

analytical range required for each element, the degree of accuracy 

expected, the class and the availability of the standard samples. From a 

strictly mathematical perspective, 4 standard samples are sufficient to 

calculate a third degree polynomial working curve. However, we recommended 

that you use a minimum of 15 standard samples to accurately define the 

working curve. The chosen standard samples must span the entire analytical 

range for each element of the application. There is no maximum number. 

3) Selecting the standard samples 

Proper selection of standard samples can be difficult. Factors that determine the required standards for each application are composition, sample matrix and quality. Standard samples are expensive, but the cost should not be the determining factor. Shimadzu's applications chemists can assist you with the proper selection of standard samples for each application. Standard samples are produced in a small quantity under very strict conditions, with the best equipment available. Generally, the operating conditions used to produce the standards are different from the conditions used to manufacture a product. 

Standards produced in house may be substituted if no compatible standards are available commercially. 

4) What is a Check Sample? 

A check sample is always used to verify the proper calibration of the spectrometer. By using the standard check procedure, the quality of the analysis improves. The check standard can be a standard reference material, a secondary standard or a homemade standard. To ensure the repeatability of each analysis, the composition of the check standard must be homogeneous and very similar to the target product. 

5) What is a recalibration standard or a setting-up sample? 

The emission spectrometer is a very stable instrument, but in practice some drift in the measurement may be experienced. Possible causes of drift 

are: dust in the stand spark, variation of the temperature or humidity in 

the laboratory, or the fatigue of the Photo-multiplier tubes. The observed 

drift can be corrected by a simple recalibration. The recalibration 

procedure compares the current intensity measurement with the original 

values, and correction coefficients are calculated. Recalibration 

standards must be homogeneous and free of defects. Standards suitable for 

the procedure are available commercially at a reasonable cost. Standard reference materials or secondary standard samples are not recommended due to their high cost. 

## 1.4 Registration of Analytical Information

We recommend, at least for the first time, to take written note of the following information (see form in the User Guide): 

- Matrix 

- Element name 

- Analytical conditions (see Shimadzu application notes) 

- Standards available for the calibration of your instrument 

- Recalibration standards for the daily recalibration 

- Check standard name selected 

- Alloy specifications 

1.5 Preliminary Operations for Quantitative Analysis 

- Adjustment of Control Gap for Emission Unit (see User Guide) 

- Temperature stability of Spectrometer 

In order to stabilize a spectrometer's temperature, leave the temperature 

regulator unit and readout unit on continuously. 

- Cleaning of Emission Stand (see User Guide) 

- Registration of all the analytical information. (see Software section 5) 

Adjustment of Attenuator 

Adjust the sensitivity of the photo-multiplier tube (attenuator) so that a measurement intensity will be in the dynamic range of the readout. The adjustment of the at tenuators is described in section 6. 

- Determination of Pre-discharge time 

A spectral line intensity greatly fluctuates immediately after starting a discharge. 

Recommendations are available in the Users Guide for different matrices of standard values for the pre-discharge time. The procedure to determine this pre-discharge time is described in the User Manual. 

Adjustment of the Integration time 

The integration time is generally 4 seconds for the High speed generator (HPSG-300) and 15 seconds for the High voltage generator (HVS). 

to 32-Verify the status of the readout unit by running the electronic test (User Guide) 

- $ample preparation 

The standard samples, recalibration samples and the unknown samples must be freshly prepared. (see User Guide) 

- Verify the quality of the discharge 

With two different standards, verify the reproducibility of the discharge. 

The precision should be better than the guaranteed values (see Shimadzu Appl. notes) 

- Analysis of the sample for Recalibration 

Analyze the upper and lower setting up samples and record their intensity values. 

These values are the target values and they will be used to recalibrate the instrument in case of drift. 

- Calculation of the Working curves 

Analyze all the available standards using the mode <INT for working curve>. If the number of standards is large (greater than 25), the recalibration of the spectrometer may be necessary to correct for possible drift. After recording all intensities calculate the working curve for each element and, eventually, the inter-element correction. 

Note: After calculating the working curve, verify the accuracy of these curves. 

1.6 Daily Analytical Procedures 

1) Adjustment of Control Gap for Emission Unit 

Form and adjust an electrode surface at the control gap of the HPSG-300 igniter or rotary gap of the HVS. 

2) Cleaning of Emission Stand 

Clean inside the emission stand, as contamination deteriorates the insulation. 

3) Recalibration 

Recalibration of the instrument is required approximately every 120 minutes, due to fatigue of the photo-multiplier tube, fluctuation of the optical system, or dust build up on the spark stand. During the analysis the vapor produced by the action of the discharge may partially condense onto the surface of the condensing lens, thus decreasing the amount of light reaching the spectrometer. 

In the following cases, be sure to perform the recalibration: 

a. The precision of an analysis is dependent on the discharge state and the nature of the fatigue effect of the photomultiplier tubes. When the elapsed time since the last analysis exceeds 60 minutes the calibration must be verified with the check standard. 

If any element flags repeat the analysis. When the same element flags twice, recalibrate the instrument. 

b. When the condensing lens is cleaned or replaced. 

c. When the counter-electrode is replaced. 

d. When the outlet slit position is checked. 

$\therefore \angle 1 = \angle 2 + \angle 3 = \angle 4$ 

[Unreadable] 

$\therefore {S}_{n} = \frac{1}{2}\left( {{S}_{n} + 1}\right)$ 

$\therefore {a}_{1} = 3,{b}_{1} = 4,\cdots ,{b}_{n} = 8$ 

2. $\frac{1}{2}$ (2) 

1. $\frac{1}{2}$ (2) 

## 1.7 Factors for Analytical Accuracy and Error

## 1) Precision

Analytical precision is affected by the following: 

a. Photometric accuracy of the console units, including the photo-multiplier tubes. An electronic test (fatigue light test) is designed to check this parameter.(see User Guide) 

b. Sensitivity of the selected wavelength. (see Application Notes) 

c. Proper application of the selected wavelength. (see Application Notes) 

d. Homogeneity of samples. 

## Accuracy

Accuracy or exactness is the main goal of the analyst. The accuracy of the analysis is driven by several factors, such as: 

- the precision of the instrument, 

- the quality of the standard sample, 

- the difference in matrix composition (difference in composition of the main element), 

- the metallurgical history between the samples and standard samples (cast, chilled cast..) 

- the quality of the calibration of the instrument. The calibration includes the calculation of the working curve and the correction of the inter-element or matrix effects. There are two types of influences by the matrix elements; namely, the absorption excitation effect and the simple overlapping of spectral lines. 

## 3) Error Factors by the Instrument

Impurity of the argon gas (Ar emission stand) 

When the argon gas contains oxygen or steam, the discharge state deteriorates and the analytical results cannot be obtained as normal values. Similarly, purity of the gas will be worsened if the argon gas piping leaks or emission st and is contaminated. 

b. Mounting of the sample (Ar emission stand) 

Samples must be set on the stand to completely cover the opening to the counterelectrode. The sample forms a seal preventing air from contaminating the discharge. If air is present the accuracy of the results will be diminished. 

## c. Improper counterelectrode gap

The discharge gap must be set using the supplied gauge. Any deviation from the prescribed setting will alter the relative intensity of the spectral line, resulting in a loss of accuracy. Repeated discharges will deform the counter-electrode tip. 

The counterelectrode must be removed, cleaned or replaced, and reset with the proper gap setting. 

d. Contamination of the condensing lens (particularly for a vacuum type) 

The condenser lens serves two purposes, to focus the spectral radiation onto the grating, and to isolate the spectrometer from the spark stand. Instruments that operate under a vacuum use an oil filled pump to achieve the required vacuum. 

The low pressure atmosphere inside the spectrometer will contain a small amount of oil vapor. A scrubber inside the spectrometer and on the pump reduce this vapor to a minimum. However, over time a thin oil film will form on the inside surface of the lens. During each analysis this oil film is exposed to the spectral radiation, causing the film to darken. This reduces the amount of energy entering the spectrometer and a resulting loss in sensitivity. Therefore, the lens must be removed and cleaned after every 3000 analyses. 

## e. Vacuum level

Applications that require the determination of C,P,S or other elements that have an analytical wavelength below 200 nm must use a vacuum spectrometer. 

Oxygen absorbs energy in this range, and must be removed from the spectrometer and the stand. An improper level of vacuum will affect the sensitivity of these elements. The vacuum level in the spectrometer must be $1 \times 10^{-2}$ mm Hg (1.33 Pa) or less. 

## f. Improper outlet slit position

Changes in temperature and pressure affect the spectrometer by shifting the target spectral line and outlet slit position. The spectrometer is insulated and the temperature is controlled above ambient to minimize the effect of normal variations in room temperature. To check the alignment of the target spectral line and the exit slit, perform the manual scan procedure. 

## g. Fluctuation of the supply voltage

A fluctuation of the supply voltage that exceeds +10%, changes the discharge 0. voltage of the emission unit and causes an error to the analytical value. 

## h. Temperature and humidity

A temperature change causes the relative position of the spectrometer's outlet slit and spectral line to change. An increase in the humidity changes the dark current of the photo-multiplier tube and causes a leak in the high insulation material used for the micro current measuring circuit of the readout nit, thus making a measured value unstable. 

## 4) Error Factors by Sample

## a. Factors of the sample itself:

Sample factors that effect the accuracy and precision of an analysis are segregation, scratches, pin holes, and cracks. Very small scratches, cracks, or pin holes tend to be overlooked when the sample is polished. Monitor the dis charge trace and the intensity of the internal standard to detect problems. 

## b. Factors of sample finishing:

The sample surface must be flat and all samples including those for calibration, must have the same surface finish. Samples of cast iron, pig iron, or special steel are difficult to excite and for accurate results, the sample roughness must be the same. The samples should be polished immediately before analysis to prevent problems due to surface oxidation. 

(Note 1) If a sample's formed surface has a defect such as a scratch, bubble, or inclusion it may cause an analytical error. Select an area free of these defects to discharge. 

(Note 2) When a very thin sample is overheated in an emission process causing an analytical error, prevent the overheating by putting a large steel ingot bloom into contact. 

## 1.8 Registration of Working Curve

The quality of the sample analysis is directly dependent on the working curves. Generally, the working curves are calculated with standard reference materials. However, sometimes the metallurgical history of your samples and of the standard reference material could be different. The curve obtained with the standard reference materials are different than the curve obtained with the secondary standard samples or the homemade samples. In this case, the use of secondary samples or homemade samples (similar to your unknown samples) to calculate the working curve is recommended. 

## 1.9 Change of Sample for Recalibration

When an existing sample for recalibration becomes unusable, replace it with a new one in the following manner: 

1. With this sample for recalibration, perform a 2-point recalibration analysis. 

2. After INT.2 correction of a new calibration sample, measure a post-correction intensity in the Intensity Measurement mode. 

3. Register a measured intensity value and a sample name into the Drift Correction Target Values Registration Table. 

## 2. SYSTEM CONFIGURATION

2.1 Terms and Concepts 

2.2 System Start and Stop 

2.3 Basic Use of Keyboard 

2.4 Program Configuration Diagram 

## 2. SYSTEM CONFIGURATION

The data processing system and the included QC-El software control the operation of the spectrometer. This system provides automatic data acquisition analysis with output to the CRT and data archival. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/eb454d6903a13eb4606ec5c99df35e6f3def8a9dc32b8725b8b8cd80e9d1dbe9.jpg)


## 2.1 Terms and Concepts

This section reviews the most important terms and concepts used in the QC-El software. The operator should review the computer manual, be familiar with the layout of the keyboard and various other parts of the computer. 

## 1) Display/CRT

The QC-El software is menu driven, allowing the operator to select each operation. 

Each screen is explained in detail, in the software manual. 

## 2) <ENTER>

The operator tells the QC-El software to execute an action or to do something via the <ENTER> key. On a few occasions the Fl: Select key is used. In general, the operator will either type in some alphanumeric characters, or position the cursor/cursor box and then push the <ENTER> key to make the action final. The QC-El will then take the requested action, such as filing the alphanumeric character, or moving to a sub-menu. 

## 3) Cursor/cursor box

The Cursor is a small blinking bar () located on the CRT where data is to be entered, selected or changed. As the operator types in the appropriated characters the cursor moves to the next allowed position. <ENTER> will move the cursor to the start of the next entry field. Arrow keys will move the cursor to the next position within the present Entry Field unless it is already at the first/last position. The <ENTER>, <TAB>, SHIFT <TAP> move the cursor to the next/previous Entry Field. Use of the cursor is best learned by using it during operation of the software. 

## 4) Entry Field/Selection Field

An Entry Field is a space in a display on the CRT with a black background where the operator can input alphanumeric characters. The cursor can be moved between Entry Fields by the use of the <Arrow>, <ENTER> and <TAB> keys. 

Characters are only entered at the exact position of the cursor and cannot be shifted. The cursor can be moved within the Entry Field with the arrows keys or space bar. 

A Selection Field is an item in a menu which may be selected by the 

operator. The selection is made by moving the gray cursor box to the 

specific menu item with the arrow keys and pressing <ENTER>. A Selection 

Field, in general, cannot be modified by the operator. Many Selection 

Fields are used for presenting information to the operator. The same 

display may be present in another section of the software as an Entry 

Field where the information can be entered or modified. 

## 5) Function Keys/Soft Keys

There are two types of Function Keys or Soft keys, F1 to F10 and SHIFT F1 

to SHIFT F10. F1 to F10 (10 keys) are always shown (if the corresponding 

function is available) at the bottom of the screen. SHIFT + Fl to 

SHIFT + F10 (10 keys) are shown just above F1-F10 keys. There are a total 

of 20 soft keys. On the CRT the F1-F10 Soft keys are shown in yellow 

letters on the large blue background. The SHIFT + F1 - SHIFT + F10 Soft 

keys are shown with a light blue box around the yellow letters. 

Function Keys allow the following types of common operations to be 

performed with a single keystroke: 

Return/Move to another software section 

Start/Stop of instrument data collection 

On/Off of detector high voltage 

Print hardcopy of CRT display 

Display of help menus 

Display of analytical method or element selection screen 

Display of the job selection 

Display of data window screen 

Calculation of results 

Display of data charts 

Filing of data 

Transmission of data 

## 6) Windows

A "Window" is either a complete display on the CRT or boxes within the present CRT display that appear due to F-key commands. The "Window" will allow temporary exit from the present display to a selection field display/window or an information display/window, and then allow a direct return to the present display or a move to another software section. "Windows" are used to assist the operator in remembering information, selecting parameters or changing software sections quickly. 

## 7) Help

Many screens have on-line Help that can be accessed by pressing F5. The Help screen includes instructions on the operation of the available screen functions. 

References to the appropriate section of the manual are also included. 

## 8) ESC

The ESC or Escape key allows the operator to move backwards through the software from the present position. If the operator is using the window display, <ESC> will exit the window. Pushing <ESC> is not recommended; the use of a soft key is generally better. 

## 2.2 System Start and Stop

Turning on the Power: 

All power to the instrument should be turned on. The following procedure should be used to turn on the computer: 

1. Turn on the POWER switch of the main unit (CPU) 

2. Turn on the POWER switch of the CRT. 

3. Turn on the POWER switch of the printer. 

Turning off the Power: 

Turn off the power in the reverse order. 

(Note) Refer to the "Guide to Operations" manual and "Installation and Set-up" manual for the supplied IBM/AT compatible. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/f6cb42e0e77ff4d7bf7182bb09fbb721f2f5c56dd0ec147ac1983e1fba815a1d.jpg)



Screen 2.1 Analysis Initial Screen


```txt
Input the password and press the ENTER key.
Screen 2.2 "Analysis Initial Screen" is displayed. If the correct password is not input, the message "Pass Word incorrect" is displayed and Screen 2.2 "Analysis Initial Screen" is displayed. In this case, this applies the protection to the Analytical information and others. 
```

Explanation of Function Keys 

SHIFT + F1 (Menu) : Displays the master menu. 

SHIFT + F2 (Job) : Displays the analytical job sub-menu. 

SHIFT + F3 (Mode 0) : Displays the Operation Mode O screen. 

SHIFT + F6 (AGsele) : Displays the Analytical Group Selection screen. 

When analyzing a content, see Section 8, ANALYTICAL OPERATION 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/c9c0693b1250aee69280e6ace59ecfcc7f57af1f6e62cc662a1c88b076b93f7e.jpg)



Appearance of Keyboard



1) Typewriter keys


![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/75e8b01a78732055bc54b58cc273a0155de0a2a12855e2355cc38d1187abdefd.jpg)


The keys above are usually provided for a typewriter as well. Although some key positions are slightly different, these keys function in the same manner as those of the typewriter. 

## CAPS LOCK

Lights up the Caps Lock 

lamp on the keyboard. 

Alphabetic keys are 

inputted as uppercase 

characters. All other keys 

remain lower case. 

ENTER Inputs an item. Its method of use is described in detail at each screen. 

TAB Makes a cursor skip from one entry item to another entry item on the screen. 

SHIFT + TAB A combination of SHIFT + TAB keys provides a reverse skip. 

<table><tr><td>NumLock</td><td>/</td><td>·</td><td>-</td></tr><tr><td>7Home</td><td>8÷</td><td>9PgUp</td><td rowspan="2">+</td></tr><tr><td>4÷-</td><td>5</td><td>6→</td></tr><tr><td>1End</td><td>2÷</td><td>3PgOn</td><td rowspan="2">Enter</td></tr><tr><td colspan="2">0Ins</td><td>Del</td></tr></table>

<table><tr><td>Num</td></tr><tr><td>Lock</td></tr></table>

If this key is pressed, the keys shown above will switch the role of the cursor key/numerical key. In case of the numerical key, the NUM LOCK lamp lights up. 

** (key input Lamp/ON)** 

<table><tr><td>7</td><td>8</td><td>9</td></tr><tr><td>4</td><td>5</td><td>6</td></tr><tr><td>1</td><td>2</td><td>3</td></tr><tr><td colspan="2">0</td><td>·</td></tr></table>

** (key input Lamp/OFF)** 

<table><tr><td>Home</td><td>↑</td><td>PgUp</td></tr><tr><td>←</td><td></td><td>→</td></tr><tr><td>End</td><td>↓</td><td>PgDn</td></tr><tr><td colspan="2">Ins</td><td>Del</td></tr></table>

(Note) At a lamp-OFF time, a combination of the SHIFT + Numerical Keys provides the same function as at a lamp-ON time. 

## 3) ESC Key

ESC Quits a job currently done. Its method of use is described in detail at each screen. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/174b19e9bfaed5cd0fd82c1e4e9c61214503cc9c3826b99378e7fd69e0324768.jpg)


How to Use the Function Keys F1 through F10 

These function keys provide functions corresponding to each key number displayed at the bottom of each screen. 

How to Use SHIFT + Fl through Fl0 

These key combinations provide functions corresponding to each key number displayed in the second row from the bottom of each screen. Their method of use is described in detail at each screen. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/560ade36b091fb7f8be8fb808ee279cb548535e079d458b72861aae1d581ab41.jpg)


You can reset the system by pressing the DEL key together with CTRL and ALT keys. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/d95086070a82383d74b2bf31f42da69660483bd732ac21497bdd33df7197a335.jpg)



Program Configuration Diagram


3. ANALYTICAL DATA PROCESSING SPECIFICATIONS 

## 3. ANALYTICAL DATA PROCESSING SPECIFICATIONS

Number of: 

1) Elements measured 45 

2) Elements simultaneously processed 32 

3) Analytical condition groups 20 

4) Analytical groups 100 (20 × S) 

5) Working curve groups 5 

6) Standard groups 500 

There are 20 analytical condition groups. For each analytical condition, 

20 analytical groups with 10 working curves groups could be registered. 

Method: 

1) Intensity versus concentration 

2) Internal standard method 

The method can be optionally specified per element 

Working Curve processing: 

1) 3200 working curves (32 elements × 100 working curve groups) 

2) 1st, 2nd and 3rd polynomial equation 

C : Concentration 

Idc : Intensity after drift correction 

3) Channel skip per working curve 

Corrections: 

1) 100% correction per working curve group 

2) Matrix element corrections 

- Correction additive (overlap) (L) 

$$
C _ {e 1} = C _ {0} + a _ {2} C _ {e 1 2} + a _ {2} C _ {e 1 3} + \dots .
$$

$C_{el}$ Element Concentration 

$C_{0}$ Concentration before matrix correction 

$C_{el2}, C_{el3}, \ldots$ Concentration of the interferant element 

$$
a _ {1}, a _ {2}, \dots .
$$

- Matrix effect (multiplying correction) (D) 

$$
C _ {e l} = C _ {0} (1 + a _ {2} C _ {e l 2} + a _ {2} C _ {e l 3} + \dots)
$$

$C_{el}$ Element Concentration 

$C_{0}$ Concentration before matrix correction 

$C_{el2}, C_{el3}, \ldots$ Concentration of the interferant element 

$$
a _ {1}, a _ {2}, \dots .
$$

The total number of corrections per element is limited at 8 

3) Master curve correction 

$$
C = C o + A C \quad o r \quad C = C o \times M C
$$

Depending on the range set, the additive or multiplying coefficient is applied. 

Statistics 

1) R control per analytical condition group 

$$
R \leq a C ^ {2} + b C + d
$$

C : Average concentration 

2) Reproducibility tests 

Applied on a maximum of 21 measurements. 

- Average value 

- Maximum value - Minimum value 

- Standard deviation value calculation 

$$
\alpha = \sqrt {\frac {\sum (X n - X o) ^ {2}}{n - 1}}
$$

Xn: Every analytical value 

n : Number of measurements 

Xo: Average measurement 

- Coefficient of Variation or Relative Standard Deviation 

$$
\mathrm{CV} = \frac {\alpha}{\mathrm{XO}} \times 1 0 0
$$

α : Standard Deviation 

Xo: Average concentration 

Printed transmission information 

- Printing order 

- Number of printing characters 

- Number of decimal digits 

- Number of magnifications 

Specified per analytical group 

Analytical result processing information 

Per analytical group 

- Displaying and printing of each analytical value (one-time analysis) 

- Printing of display of each analytical value and average value 

- Displaying and printing of each analytical value, average value, standard deviation and coefficient of variation 

- Printing directed by an operator 

Report preparation 

- per analytical group 

- per standard group 

- per sample name 

Control chart 

- per standard group 

- per sample name 

Sensitivity adjustment 

- Adjustment of each channel per analytical group 

Waste discharge 

Manual scanning 

Date setting 

System backup 

4. MASTER MENU 

## 4. MASTER MENU

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/b7b8421115819bfa19c954b04ac6dc9420ce93b579a0f524da4db370a90a61b7.jpg)



FIGURE 2: Master Menu Display Example


Pressing the SHIFT + Fl (Menu) keys together displays the master menu. Select a desired job with the key ↑ or ↓, and press the ENTER key. You are taken to each Job screen. 

1. Analytical information ..... Registers analytical information 

2. Attenuator adjustment ..... Adjusts attenuator sensitivity 

3. Regression calculation ..... Registers a chemical analytical value and standard sample, creates a working curve and calculates a matrix element correction coefficient. 

4. Analysis . . . . . . . . . . . . . . Performs an analysis 

5. Report of results ..... Prepares a report 

6. Maintenance ..... Performs various kinds of maintenance. 

## 5. CONFIGURATION INDEX OF ANALYTICAL INFORMATION

## Introduction

5.1 Sequence to Register Analytical Information 

5.2 Preparation of Analytical Information 

5.3 Registration of Analytical Group Name 

5.4 Registration of Analytical Conditions 

5.5 Registration of Attenuator (ATT) Settings 

5.6 Registration of Order of Analytical Channel and Sequence, Internal Standard Element 

5.7 Registration of Drift Correction Target Value 

5.8 Registration of Working Curve Coefficients, 100% Correction and Channel Skip 

5.9 Registration of Matrix Element Correction Coefficients 

5.10 Registration of the Master Curve Correction Sample and Target Value 

5.11 Registration of the Analytical Element Display and Printing Order 

5.12 Registration of the Data Transmission Format 

5.13 Registration of the Purity Calculation Information 

5.14 Registration of Standard Name and Standard Value 

5.15 Registration R Control Value 

5.16 Registration of Special Calculation Formula 

5.17 Analytical Information Copy 

5.18 Registration of Element Name and Wavelength 

5.19 Registration of Histogram Control Value 

5.20 Registration of the Analytical Group Using Same Analytical Condition 

## 5. CONFIGURATION INDEX OF ANALYTICAL INFORMATION

## Introduction

Shimadzu's integrated software package allows the registration of 20 different sets of Analytical Conditions. Each set can consist of 20 unique Analytical Groups plus its respective working curve. 

Normally the Analytical Conditions are based upon the sample matrix, such as steel, cast iron, aluminum alloys, copper alloys, etc... With the same analytical conditions several alloys may be analyzed, but their analytical group names and working curves are different. Therefore, the software permits the optimum analytical conditions and working curve for each analytical object to be defined. 

<table><tr><td>Analytical group</td><td></td><td>Analytical condition</td><td>Working curve group</td><td>Analytical group name (8 characters)</td></tr><tr><td></td><td></td><td>A. CON</td><td>W. GRP</td><td>AG - No Name</td></tr><tr><td rowspan="21">Up to 100 groups</td><td>1</td><td>1</td><td>1</td><td>FC</td></tr><tr><td>2</td><td></td><td>2</td><td>FCD</td></tr><tr><td>3</td><td></td><td>3</td><td>FCDN</td></tr><tr><td>.</td><td></td><td>.</td><td></td></tr><tr><td>.</td><td></td><td>5</td><td></td></tr><tr><td>5</td><td></td><td></td><td></td></tr><tr><td>6</td><td>2</td><td>1</td><td>C Steel1</td></tr><tr><td>7</td><td></td><td>2</td><td>C Steel2</td></tr><tr><td>8</td><td></td><td>3</td><td>C Steel3</td></tr><tr><td>.</td><td></td><td>.</td><td></td></tr><tr><td>.</td><td></td><td>.</td><td></td></tr><tr><td>.</td><td></td><td>.</td><td></td></tr><tr><td>10</td><td></td><td>5</td><td></td></tr><tr><td>11</td><td>3</td><td>1</td><td>SUS</td></tr><tr><td>.</td><td></td><td>.</td><td></td></tr><tr><td>.</td><td></td><td>.</td><td></td></tr><tr><td>15</td><td></td><td>5</td><td></td></tr><tr><td>.</td><td></td><td>.</td><td></td></tr><tr><td>.</td><td></td><td>.</td><td></td></tr><tr><td>.</td><td></td><td>.</td><td></td></tr><tr><td>100</td><td></td><td>.</td><td></td></tr></table>

## 5.1 Registration Order of Analytical Information

Analytical information is registered per group. This section describes the method sequentially. As part of the initial configuration of your instrument Shimadzu registered the element name with its corresponding integrator number (ITG) and analytical wavelength in the <Element name and wavelength> table. 

This table should not be modified without the direction from Shimadzu's Optical Emission personnel! 

## 1) Selecting the analytical condition

Assign an analytical condition group (A.CON) per main component or steel type. 

<table><tr><td>A. CON</td><td>ANALYTICAL OBJECT</td></tr><tr><td>1</td><td>Cast iron</td></tr><tr><td>2</td><td>Low alloy steel</td></tr><tr><td>3</td><td>Stainless steel</td></tr><tr><td>4</td><td>Special steel</td></tr><tr><td>5</td><td>Aluminum alloy</td></tr><tr><td>6</td><td>Copper alloy</td></tr><tr><td>.</td><td></td></tr><tr><td>.</td><td></td></tr><tr><td>.</td><td></td></tr><tr><td>20</td><td></td></tr></table>

2) Registering the analytical group name (See 5.3) 

In the <Name of analytical group> table, register an analytical group name (8 characters). 

## 3) Registering the analytical group condition (See 5.4)

In the <Analytical condition> table, register the analytical conditions such as a source condition, integrating time and so on. 

4) Registering the measuring condition and internal standard element (See 5.5) 

In the <Sequence, internal standard element number & attenuator> table, register an analytical sequence, and an internal standard element number when internal standard analysis is used. 

The attenuator is automatically filed by making the attenuator adjustment outline in Step 7. 

5) Registering the analytical element (See 5.6) 

In the <Order of analytical channel> table, register an analytical element order. (Take the channel skip into account when an analytical range is wide). 

6) Entrance slit adjustment (11.2) 

To prevent any error caused by a drift in temperature, the optical alignment of the spectrometer must be verified. Set the scanning dial to the spectral peak value. The manual scanning operation is described in 11.2. 

7) Setting the attenuator (See Section 6) 

In the <Attenuator adjustment> mode, determine an attenuator setting for the element measured. For an on-screen intensity value use the following table as a reference. 

<table><tr><td>Emission unit</td><td>Display scale</td><td>Graduation</td><td>Intergration time</td><td>INT l value (without internal standard)</td></tr><tr><td>HPSG</td><td><eq>\times 2</eq></td><td>6 - 7</td><td>4 sec</td><td>0.5 - 0.6</td></tr><tr><td>HVS</td><td><eq>\times 5</eq></td><td>4 - 5</td><td>15 sec</td><td>0.5 - 0.6</td></tr></table>

For a given element, adjust the attenuator to read an intensity value lower than the internal standard intensity value. A high content sample of the desired analytical range should be used to adjust the attenuator. 

A pre-correction intensity of 0.8 or more with no internal standard element specified, overflows. Normally, use within a range of 0.5 to 0.6. 

8) Measuring the pre-correction intensity (See 9.9) 

Entering the information 1 through 7 enables measurement of the pre-correction intensity. The setting-up samples are measured in the <INT 1. (Raw intensity)> mode. The measured intensity could be recorded in the calibration table target values and working curve coefficient calculations. (However, it is automatically filed by performing the operation in sections 10 or 13). 

In the <Sample number target & coefficient for drift correction> table, register sample names for recalibration. A sample for recalibration or setting-up standards mentioned here refers to a uniform sample which is free from forming segregation and crystal segregation and whose measured intensity can cover a working curve range. (You may use a sample whose chemical analytical value is not certified). 

Usually the recommended number of samples for recalibration is 3 to 6. The setting-up standards are selected to recalibrate the instrument at high and low content for each element. The following is an example of setting-up standards provided by Shimadzu. 

<table><tr><td></td><td>C</td><td>Si</td><td>Mn</td><td>P</td><td>S</td><td>Ni</td><td>Cr</td><td>...</td></tr><tr><td>ST - A</td><td>(1.01)</td><td>(0.06)</td><td>(0.04)</td><td>(0.001)</td><td>(0.001)</td><td>(4.00)</td><td>(0.01)</td><td>...</td></tr><tr><td>ST - B</td><td>(0.009)</td><td>(0.64)</td><td>(0.50)</td><td>(0.034)</td><td>(0.003)</td><td>(0.51)</td><td>(4.04)</td><td>...</td></tr><tr><td>ST - C</td><td>(0.004)</td><td>(0.01)</td><td>(2.04)</td><td>(0.006)</td><td>(0.043)</td><td>(0.03)</td><td>(0.52)</td><td>...</td></tr></table>

Register the appropriate setting-up standard names in the items H, L and K of the Information table. For each standard, only one character is available. 

$$
(\mathrm{ST} - \mathrm{A} = \mathrm{A} / \mathrm{ST} - \mathrm{B} = \mathrm{B} / \mathrm{ST} - \mathrm{C} = \mathrm{C})
$$

<table><tr><td></td><td>C</td><td>Si</td><td>Mn</td><td>P</td><td>S</td><td>Ni</td><td>Cr</td><td>...</td></tr><tr><td>H</td><td>A</td><td>B</td><td>C</td><td>B</td><td>C</td><td>A</td><td>B</td><td>...</td></tr><tr><td>L</td><td>C</td><td>C</td><td>A</td><td>A</td><td>A</td><td>C</td><td>A</td><td>...</td></tr><tr><td>K</td><td>A</td><td>B</td><td>C</td><td>B</td><td>C</td><td>A</td><td>B</td><td>...</td></tr></table>

Example of Standardization Sample Name Registration 

It is also possible to manually input the pre-correction intensity measured values of number 8 for the H, L, and K target value items of the Information Table. 

However, they are automatically filed by performing the analytical operation in number 10. 

10) Registering the target value for calibration (See 9.6) 

In the <Analysis> <INT. 2 for target> mode, specify an analytical group and analyze the sample for recalibration registered in number 9. 

The pre-correction intensity analyzed is automatically filed in the target value item (H, L, K) of the Drift Correction Target Value Registration Table shown in section 5.7. 

11) Two-point recalibration (See 9.4) 

In the <Analysis> <Two-point recalibration> mode, perform the 2-point recalibration analysis. Analyze all samples for recalibration registered in the analytical group and calculate correction coefficients "alpha" and "beta". 

The alpha and beta values obtained are automatically filed into the items alpha and beta of the Drift Correction Target Value Registration table shown in 5.7. 

12) Measuring the post-correction intensity (See 9.8) 

A post-correction intensity can be measured in the <Analysis> <INT. 2 (Drift corrected intensity)> mode. 

The post-correction intensity can be used for working curve coefficient calculations. (It is automatically filed by performing the operation mentioned in number 15). 

13) Registering the working curve standard samples (See 7.1) 

In the <Regression calculation> <Chemical content> mode, register the chemical composition of each standard sample available to calculate the working curve. 

Note : If the 100% correction is going to be used, the chemical composition should be converted to the virtual composition. The virtual composition is determined by calculating the ratio of each element to the main component. 

Example: For a steel type where content of a main component element changes by 5% or more, use a 100% correction method. In this case, the content to be input in the <Chemical content> mode should be converted into a relative content of measured element content/main component element content. (Although this method is effective for alloys of iron, nickel, etc. it is not so much recommended for those of copper and aluminum). 

14) Registering to the analytical group for the working curve standard sample name (See 7.2) 

In the <Regression calculation> <Sample entry> mode, register the standard samples for each analytical group. The software creates a file for each sample, its composition, and its measured intensity (collected during the analysis in <INT for working curve> mode). 

15) Measuring the working curve standard sample intensity (See 9.7) 

Measure a curve standard sample in the <Analysis> <INT 2 for working curve> mode. 

Analyze the standard samples registered in the Sample Entry (step 14). 

When the number of samples to be analyzed is large, it is recommended that the two point-recalibration be repeated halfway through analyzing the samples. 

16) Calculating the working curve coefficient (See 7.3) 

Calculate the working curve coefficients in the <Regression calculation>
<Working curve making> mode. 

17) Registering the working curve coefficient (See 5.8) 

The working curve coefficients obtained in number 16 are automatically filed into the <Coefficient of working curve, normalization to 100% channel skip> table. 

Manually input information for 100% correction and channel skip. 

18) Calculating the matrix element correction coefficient 

(See 7.4 through 7.6) 

Calculate the correction coefficients for matrix elements in the <Regression calculation> <Matrix coefficient> mode. 

After calculation, the correction coefficients are automatically filed into the <Coefficient of matrix correction> table. The coefficients are determined by multiple regression calculations. The calculation is possible only if the number of standard samples is large enough. (For one interference calculation 15 standard samples are the minimum recommended number). 

19) Registering the master curve correction sample and target value (See 5.10) 

Register a master curve correction sample name and a target value. 

20) Registering the printing order (See 5.11) 

Register in the <Display & printout format> table the information for the printing order and transmission order, number of decimal digits, number of effective digits, exponent display, etc. of the analytical results. 

21) Registering the purity calculation (See 5.12) 

Calculate a main component element's content (purity), such as aluminum and register in the <Purity calculation> table to print. 

22) Registering the product standard value (See 5.13) 

Register a product standard name and its standard value in the <Standard information> table. It checks whether a result of content analysis is within a preregistered product standard range. 

23) Registering the variance check (R control) control width (See 5.14) 

In the <Coefficient of equation for variance check> table, register a variance control width for analytical values at a multiple analysis time. 

24) Registering the special calculation formula (See 5.15) 

Register a special calculation formula in the <Information for calculation of physical constant> table. For example, input in this table the calculation formula which calculates as carbon equivalents (CE values) the values of carbon (C) and silicon (Si) which has the most effect in a cast iron material. In the Analytical Element Registration table shown in number 6, affix a virtual integrator number for this calculation formula after an analytical element. 

25) Copying the analytical information (Section 5.16) 

Selecting <Copy from different analytical group> provides a method of copying all analytical conditions and information from one group to another. 

Note: When you copy between different analytical condition groups, all analytical conditions are copied. 

26) This system can be run in an optimum condition by inputting the analytical information nos. 1 through 25. 

Function keys commonly used in an analytical information registration area as follows: 

F 1 (Select) : Selects an analytical group name AG-No. 

F 2 (Next) : Displays the next analytical Information screen. 

F 3 (Pre.) : Displays the previous Analytical Information screen. 

F 4 (Print) : Prints a screen. 

F 5 (Help) : Press this key, if there is anything unclear on the Information screen. 

F 6 (Ele) : Displays a list of analytical element for the selected group. Press the ESC key to remove the element window. 

F 9 (Init) : Returns to the Analysis Mode screen. 

F10 (Sub-menu) : Turns to the Analytical Information Sub-menu screen
Figure 3. 

SHIFT + Fl (Menu): Displays the Master Menu screen. 

(Note 1) During the setting of any analytical information file on the Display screen, the use of function keys being displayed (except F4 (Print) and F5 (Help)) will validate the screen information. 

(Note 2) To set an information, move the cursor to an entry item with the keys ENTER, ↑, ↓, +, →, or TAB and input it. 

↑ (+) : Moves the cursor upward (downward) by one position from a current one. When a current cursor position is at the top (bottom), the cursor does not move. 

← (→) : Moves the cursor the left (right) by one position from a current one. 

TAB : Moves the cursor from a current entry item to the immediate right one. 

SHIFT + TAB: Provides a reverse function of the TAB key. 

(Note 3) When inputting a numerical value, do not leave a space between numbers.
Example: 100.0 (acceptable) 12 3 (unacceptable) 

(Note 4) A buzzer sounds when an unavailable key is pressed. 

(Note 5) When information entered is erroneous, an error message "Data Error" is displayed when the function key is pressed, and the cursor is moved to an erroneous entry position. Correct the information and press the function key again. 

(Note 6) Only the function keys displayed at the bottom of the screen are effective. 

## 5.2 Preparation of Analytical Information

Select the <Analytical information> mode from the Master Menu (FIGURE 2) with the key ↑ or ↓, and press the ENTER key. The Analytical Information Sub-menu screen is displayed. Move the highlighted cursor bar with the key ↑ or ↓ to the menu item and press ENTER to select. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/dc3c841cd7a84280acd87315202063b1736d1be43fafefa01ba369cf9f1e7d19.jpg)



FIGURE 3: Example of Analytical Information Sub-menu Display


When you select: 

<Information for INT. 1> (JOB No. 5) 

Opens the specific file to read, input or modify the analytical information for the analysis in Raw intensity mode. This analysis mode is called "JOB 5" (INT.1(Raw intensity without any correction)). 

<Information for INT. 2> (JOB No. 2, 3, 6, 7, 8) 

Opens the specific files to read, input or modify the analytical information forthe analysis in mode 2, 3, 6, 7 and 8. The analysis mode 2, 3, 6, 7 and 8 are defined as following: 

2. 1-point recalibration 

3. 2-point recalibration 

6. INT. 2 (Drift corrected intensity) 

7. INT. 2 for working curve 

8. INT. 2 for target 

<Information for cont> (JOB No. 4, x, y) 

Opens the specific files to read, input or modify the analytical information for the analysis in mode 4, X and Y. The analytical mode 4, X and Y are defined as following: 

4. Master curve calibration 

X. Content 

Y. Special 3 times analysis 

## <Standard information>

Opens the specific file to read, input or modify the specifications and names of your products. It is possible to register 500 product names (called standard names) and product specifications (called standard values). 

<Coefficient of equation for variance check> 

Opens the specific file to read, input or modify the R control width for multiple analyses per analytical condition. 

<Information for calculation of physical constant> 

Opens a specific file to read, create or modify a special calculation formula. 

This formula is registered in a virtual integrator number. 

<Copy from different analytical group> 

Opens a specific file which contains the instruction to copy element name and wavelength from one analytical group to another. 

## <Element name and wavelength>

Opens the specific file to read, input or modify the name and wavelength of the element. 

Each element is assigned to a specific integrator (ITG-No.) or. The element name, integrator and wavelength are set by Shimadzu and are not be modified without approval of the OES service department. 

## <Histogram information>

Opens the specific file to read, input or modify the Histogram Control Value. 

<Analytical group using same analytical condition> 

Opens the specific file to read, input or modify the Number Analytical Condition Group. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/6bd444c5904f7e3bf1a77766544f25441e326d3e6d094182d3edd1df18b90d96.jpg)



Information Screen displayed next when each of function keys F1, F2, F3, and F10 is pressed at the Analytical Information display screen.


## 5.3 Registration of Analytical Group Name

After selecting an analysis mode (<Information for INT. 1, INT. 2 or cont>) from the Analytical Information Screen (Figure 3), the Analytical Group Name Registration Screen will be displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/ddd6d782ae2e1205e96d1330fc3eb7676c236030211c422e1e398929fdbc6532.jpg)


FIGURE 4: Input Example of Analytical Group Name Registration Screen 

AG-No. : Analytical group number (No. 1 to 100) 

A. CON : Analytical condition group number (No. 1 to 20) 

W. GRP.: Working curve group number (No. 1 to 5) 

A. CON and W. GRP are assigned to each AG-No. 

NAME : Register an analytical group name. (Within 8 characters) 

Explanation of Function Keys 

F1 (Select): Selects the highlighted analytical group AG-No. 

<Operation Method> 

Registration of a new Analytical Group Number 

1) Select the analytical condition (A.CON 1 to 20) 

Use PgDown, PgUp and the arrows keys to select the condition. 

2) Select the Analytical Group Number (AG-No) with the arrows keys 

3) To register a new group name, select the Analytical Condition, move the cursor to the next available blank entry position and type in the new name. 

4) Move the cursor to the desired group name and condition and select by pressing the Fl key. 

(Note) If an analytical group name is changed halfway through an analysis, preceding and following data cannot be used for data editing in report preparation and X-R control. 

## 5.4 Registration of Analytical Condition

After selecting an analytical group from the Analytical Group Name Registration screen, the Analytical Condition Registration screen will be displayed. 

```txt
Analytical Information Date 04-01-93 Time 16:12
(1) Analytical Conditions A.CON = 4
Ar Flush(x0.1sec) = 30 Source No.
Sequence 1 2 3 0: Lamp
Source 2 1 3 1: Normal spark
Preburn Time 30 10 10 x0.1sec 2: Special combined
Integ. Time 0 30 30 x0.1sec 3: Combined spark
Cleaning 6 4: Oscillation spark
Source 6 7: Arclike combined
Cleaning Time 4 x0.1sec 5: Cleaning sparl
1:Menu 8: 9:
2:Next 3:Pre. 4:Print 5:Help 9:Init 10:Submenu 
```

FIGURE 5: Input Example of Analytical Condition Registration Screen (Input Example of Low Alloy Steel) 

AIR FLUSH : Time required to flush the discharge chamber (Ar stand) with argon gas. 

Source : Set the electrical discharge conditions for each sequence by selecting the appropriate source number. Source number and corresponding spark type is displayed on the right hand side of the screen. 

Preburn Time : Set a preburn time for each of the sequences SEQ1 through SEQ3. (Preburn times are set to reduce the effect of the sample metallurgical hysteresis). 

Integ. Time : Set a measuring time for each of the sequences SEQ1 through SEQ3. 

Cleaning Source: Set the source condition to cleaning spark option. 

Cleaning Time : Set a discharge time for cleaning the tip of the counterelectrode. 

Pressing the ENTER key validates an input and moves the cursor to an entry item. 

Pressing the function key F2 (Next) changes to the next screen in the sequence and F3 (Pre.) return to the previous screen. 

<Source conditions> 

Normal Spark (HPSG-300) 

Emission condition for most analysis 

Combined Spark (HPSG-300) 

Used for the analysis of low levels of P, S, Pb, Sb, etc. (generally in the range of 50 ppm) 

Oscillation Spark (HPSG-300) 

Used for analyzing Si, etc.. contained in unwhitened gray cast iron.
Carbon contained in cast iron cannot be analyzed because a C electrode is used as a counterelectrode. 

High Power Spark (HPSG) 

In analyzing carbon contained in steel, there will be a difference in the analytical value due to the thermal hysteresis of a sample. The effect of thermal hysteresis is reduced by approximating an analytical surface layer to a quick-cooled texture through preburn for a constant time by a high power spark. 

Cleaning Spark (HPSG-300) 

During an analysis a portion of the vaporized sample may deposit on the counter electrode. By reversing the polarity of the discharge during the cleaning cycle, these deposited samples will vaporize. 

High Voltage Spark (HVS) 

Used for analyzing aluminum alloy, magnesium alloy, etc. 

## <Analytical sequence>

The analysis of most elements only require the use of Sequence 1. Some matrices may require the use of Seq. 2 and Seq 3, to optimize the analyses. Each sequence initiates sequentially. At the end of the analysis the counter electrode is cleaned and the data is displayed on the screen. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/5d2593f6dfbeb4d287d64b90543f5db5d871ce82ba5dbfca586ad652d2a1fe2b.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/bd04efc8dff1ed175a39241972f5e8c193f77be8e7a2fe9907703964fed1b0d1.jpg)



FIGURE 6: Input Example for Aluminum Analysis


## 5.5 Registration of Attenuator (ATT) Settings

From the Analytical Condition Registration screen, pressing the F2 (Next) key displays the Measuring Condition (SEQ), Internal Standard Element (ISE) and Attenuator (ATT) Registration screen. 

```batch
Analytical Information Date 04-01-93 Time 16:14
(2) Attenuator Settings A.CON = 6
ITG ELE WL ATT ITG ELE WL ATT
1 FE1 271.4 15 15 SN 189.9 27
2 FE2 287.2 0 16 NB 319.5 32
3 C 193.0 18 17 B 182.5 35
4 SI 212.4 33 18 PB 405.7 35
5 MN 293.3 20 19 CO 258.0 27
6 P 178.3 34 20 W 220.4 39
7 S 180.7 31 21 0
8 CU 224.2 26 22 0
9 NI 231.6 17 23 0
10 CR 267.7 15 24 0
11 MO 202.0 21 25 0
12 AL 394.4 37 26 0
13 V 311.0 23 27 0
14 TI 337.2 23 28 0
1:Menu
2:Next 3:Pre. 4:Print 5:Help 9:Init 10:Submenu 
```

FIGURE 5.4: Input Example of Attenuator (ATT) Registration Screen. 

ITG: Integrator Number for the readout unit (channel 1 to 45). 

ELE: Element name and wavelength for each integrator 

AT : Setting of the sensitivity of a measured element detector.
Automatically filed upon attenuator adjustment. This screen also allows manual input. Set within a range of 0 to 63. 

The cursor can be moved to an entry item with the arrow keys or moved sequentially by pressing ENTER. 

When you want to input ITG Number 29 to 45, press the PgUp key. After inputting the information, press the F2 (Next) key. You are then taken to the Analytical Element Registration screen (Section 5.6). 

## 5.6 Registration of Order of Analytical Channel and Sequence, Internal Standard Element

From the Attenuator Settings Registration screen, pressing the F2 (Next) key displays the Order of Analytical Channel and Sequence (SEQ), Internal Standard Element (ISE) Registration screen. 

In the column labeled ITG enter the integrator number and the corresponding element name (ELE) will automatically be displayed. Press the F6 (key) to display the element list and integrator numbers. The column labeled NAME allows the user to enter the format of the element name to be used throughout the method. The software is case sensitive, therefore FE1 is different from Fe1. A maximum of 32 elements can be entered, but those that are internal standards must be the first elements of the list. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/e58d8de155e821e93418924d75434752e2e8f4f5a958da90298110f0e606b230.jpg)


FIGURE 5.5: Input Example of Analytical Element Registration Screen 

ITG : Input an integrator for AR-No. 1 to 45 or virtual integrator Number 57 to 61 set in special calculation information. 

ELE : Displays an element name corresponding to ITG.(cannot be modified) 

NAME : Input an element name to AR-No. less than 5 characters. (Input the same name in case of channel skip). 

ISE : Select whether to use the internal standard method, and set internal standard elements when using the internal standard method. 

ISE = 0 : Set a constant-time integrating method. (Analyze the internal standard elements through constant-time intergral). 

ISE 1 to 45: Set an integrator number for the internal standard element. 

W - No. : When you analyze with using the element informations (① ~ ④ below) registered in differential AR-No., you input the AR-No.. 

① Calibration coefficient information 

② Matrix correction information 

③ 100% correction information 

④ Master-curve correction information 

When you don't use the differential AR-No. information, you input "0" in it. 

The cursor can be moved to an entry item with the arrow keys or moved sequentially by pressing ENTER. 

When you want to input ITG Number 29 to 45, press the PgUp key. After inputting the information, press the F2 (Next) key. You are then taken to the Analytical Element Registration screen (Section 5.6). 

FIGURE 5.5.1: Analytical Screen Registration and Element Name Window Display Example 

(Note 1) When performing a channel skip with two analytical wavelengths, input two wavelengths continuously. (see section 5-8) 

(Note 2) When performing a channel skip with one analytical wavelength, input the same ITG-No.continuously and distinguish with AR-No. (see section 5-8) 

(Note 3) Since the element names registered in this table serve as key codes for standard checks, X-R control and accuracy control, unify the element names registered. 

(Note 4) If an analytical element order is altered halfway through an analysis, preceding and following data cannot be used for data editing in report preparation and X-R control. 

Pressing the ENTER key validates the input and moves the cursor to an entry item (ITG,Name). When you do not know the ITG-No. and element names, press the F6 (Elem) key. 

The screen displays the ITG-No. and the window corresponding to the integrator element names. When you want to delete the Window screen, press the ESC key. 

After inputting information, press the F2 (Next) key. You are then taken to the Drift Correction Reference Value Registration screen (Section 5.7). 

## 5.7 Registration of Drift Correction Target Value

The Drift Correction Target Value screen is displayed by pressing F2 (Next) key from the Registration of the Analytical Elements screen. This table contains information necessary to perform the recalibration and Drift Correction Calculation for the analytical group. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/0e5b55c0a661b95f6fa46f7bf352bb59769f49ae7ee84dd740f1fcbcfbffb501.jpg)



FIGURE 5.6: Input Example of Drift Correction Reference Value Registration Screen


Sample Number 

H: Input the name of a high-content sample for the 2-point recalibration.
(1 character) 

L: Input the name of a low-content sample for the 2-point recalibration.
(1 character) 

K: Input the name of a sample for the 1-point recalibration. (1 character) 

Target 

H: Input the target intensity of a high-content sample for 2-point recalibration. 

L: Input the target intensity of a low-content sample for 2-point recalibration. 

K: Input the target intensity of a sample for the l-point recalibration. 

After the sample names for recalibration are registered, analysis in the <INT. 

2 for target> mode will automatically file the measured intensity values for each target item. 

Recalibration of the spectrometer compares the current intensity reading with those obtained during the initial setup procedures and drift correction coefficients are calculated. 

The correction coefficients are calculated as follows: 

$H_{Target}$ : High-content standard sample target intensity value 

$I_{H}$ : High-content standard sample measured intensity value 

$L_{Target}$ : Low-content standard sample target intensity value 

$I_{L}$ : Low-content standard sample measured intensity value 

<Two-point recalibration correction coefficients> 

$$
\mathrm{H} _ {\text { Target }} = (\alpha \times I _ {H}) + \beta
$$

$$
L _ {T a r g e t} = (\alpha \times I _ {L}) + \beta
$$

$$
\alpha = \frac {H _ {\text { Target }} - L _ {\text { Target }}}{I _ {H} - I _ {L}}
$$

$$
\beta = H _ {T a r g e t} - (\alpha \times I _ {H})
$$

At this time, the k value for l-point calibration is 1.0. 

<One-point recalibration correction coefficients> 

$$
\mathrm{H} _ {\text { Target }} = k ((\alpha \times I) + \beta)
$$

$$
k = \frac {H _ {\text { Target }}}{((\alpha \times I _ {H}) + \beta)}
$$

After the two-point recalibration, the new alpha and beta values are calculated and the post-correction intensity can be obtained by the following equation; 

$$
I _ {D C} = \alpha I + \beta
$$

After the one-point recalibration, the new k values are calculated and post-correction intensity can be obtained by the following equation; 

$$
I _ {D C} = k (\alpha I + \beta)
$$

$I_{DC}$ : post-correction intensity 

I : pre-correction intensity 

(Note) When using the Internal Standard Method for the internal standard element, set standard sample name items (H, L, K) to *, target value to 0, α to 1.0, β to 0.0, and the k item to 1.0. 

5.8 Registration of Working Curve Coefficient, 100% Correction and Channel Skip 

The Working Curve Coefficient, 100% Correction and Channel Skip Registration screen is displayed by pressing the F2 key (Next) from the Drift Correction Target Value Registration screen. 

This screen displays the working curve coefficients, 100% correction, and channel skip information. 

<table><tr><td colspan="8">Date 04-01-93 Time 16:17</td></tr><tr><td colspan="8">Working Curve Coefficients, Normalization to 100% &amp; Channel Skip</td></tr><tr><td></td><td></td><td></td><td></td><td colspan="4">A.CON = 6 W.GRP = 1</td></tr><tr><td>AR-No.</td><td>NAME</td><td>a</td><td>b</td><td>c</td><td>d</td><td>Y/N</td><td>SKIP POINT</td></tr><tr><td>1</td><td>Fe</td><td>.000000000</td><td>.000000000</td><td>1.00000000</td><td>.000000000</td><td>I</td><td>.00000</td></tr><tr><td>2</td><td>C</td><td>.000000000</td><td>.000037204</td><td>.010455192</td><td>-.07728757</td><td>Y</td><td>.00000</td></tr><tr><td>3</td><td>Si</td><td>.000000000</td><td>.000001026</td><td>.014157231</td><td>-.09831648</td><td>Y</td><td>.00000</td></tr><tr><td>4</td><td>Mn</td><td>.000000000</td><td>.000099265</td><td>.021218607</td><td>-.07058757</td><td>Y</td><td>.00000</td></tr><tr><td>5</td><td>P</td><td>.000000000</td><td>.000000000</td><td>.001629505</td><td>-.04153815</td><td>Y</td><td>.00000</td></tr><tr><td>6</td><td>S</td><td>.000000000</td><td>.000000000</td><td>.000973307</td><td>-.01248745</td><td>Y</td><td>.00000</td></tr><tr><td>7</td><td>Cu</td><td>.000000000</td><td>.000084588</td><td>.008716023</td><td>-.06389780</td><td>Y</td><td>.00000</td></tr><tr><td>8</td><td>Ni</td><td>.000000000</td><td>.000895760</td><td>.017342154</td><td>-.07112108</td><td>Y</td><td>.00000</td></tr><tr><td>9</td><td>Cr</td><td>.000000000</td><td>.000585646</td><td>.013221181</td><td>-.03783195</td><td>Y</td><td>.00000</td></tr><tr><td>10</td><td>Mo</td><td>.000000000</td><td>.000107758</td><td>.012075054</td><td>-.07680739</td><td>Y</td><td>.00000</td></tr><tr><td>11</td><td>Al</td><td>.000000000</td><td>.000000000</td><td>.001992400</td><td>-.02804000</td><td>Y</td><td>.00000</td></tr><tr><td>12</td><td>V</td><td>.000000000</td><td>.000019321</td><td>.006282317</td><td>-.03905830</td><td>Y</td><td>.00000</td></tr><tr><td>13</td><td>Ti</td><td>.000000000</td><td>.000009744</td><td>.002702906</td><td>-.00848646</td><td>Y</td><td>.00000</td></tr><tr><td>14</td><td>Sn</td><td>.000000000</td><td>.000000000</td><td>.002208242</td><td>-.02800413</td><td>Y</td><td>.00000</td></tr><tr><td>15</td><td>Nb</td><td>.000000000</td><td>.000000000</td><td>.003046737</td><td>-.05785630</td><td>Y</td><td>.00000</td></tr><tr><td>16</td><td>B</td><td>.000000000</td><td>.000000000</td><td>.000260867</td><td>-.01025638</td><td>Y</td><td>.00000</td></tr></table>

FIGURE 11: Input Example of Working Curve Coefficient, etc. Registration Screen 

NAME : Displays an analytical element name. 

a, b, c, d : Working curve coefficients. (a, b, c, and d are automatically filed by a working curve coefficient calculation program). 

Y/N : Set whether to perform 100% correction. 

Y : Element requiring 100% correction 

N : Element not requiring 100% correction 

I : Internal standard element 

When setting a channel skip, enter Y for both low and high content. 

SKIP : A SKIP element must have two available analytical wavelengths, one for low content and another for high content. The Skip mark, +, must be entered for the low content range and the next element must be the high content. Both entries of the element must have exactly the same name. 

POINT : Set a skip point in 6 digits including a decimal point. 

Pressing the ENTER key validates an input and moves the cursor to the next entry item (a, b, c, d, Y/N, SKIP, POINT). When you want to input information for AR No. 16 to 32, press the PgUp key. After inputting information, press the F2 (Next) key. The Matrix Element Correction Coefficient Registration screen appears (Section 5.9). 

1) Working Curve Coefficient 

Working curve coefficients a, b, c, and d refer to coefficients of the following content conversion formula: 

C = aI $^{3}$ DC + bI $^{2}$ DC + cI $_{DC}$ + d 

The concentration of a given element (C) can be calculated by substituting the post-drift corrected intensity ( $I_{DC}$ ) in the above equation. The coefficients (a,b,c) are calculated upon creation of a working curve and automatically filed. They can also be manually inputted. 

(Note 1) For internal standard elements which do not require content conversion, manually input a = 0; b = 0; c = 1 and d = 0. 

(Note 2) In practice, it may be observed that the working curve obtained with the reference material and the working curve obtained with homemade samples are different. This difference can be explained by the fact that the homemade samples integrate all the factors which can affect the quality of the standard samples. Therefore, it is often recommended to use the homemade standard samples if the number of homemade standard samples are large enough to calculate a good working curve. 

The internal standard corrects for any instability in the discharge or for small differences in the emission resulting from a difference in the matrix. The correction is only possible if the concentration of the internal standard in the standard samples and the analyzed samples is constant. When the concentration of the internal standard varies more than 5 % , use the 100% Correction method. 

This method calculates for each element the intensity ratio using the virtual concentration. The virtual concentration is determined by dividing the concentration of the element by the concentration of the internal standard and multiplying by 100. The concentration of a given element is calculated as follows: 

① Preparation for obtaining the working curve coefficients 

a. Calculate the content of the main component element out of the chemical analytical value table for standard samples. 

$$
C _ {B E} = 1 0 0 - \left(\Sigma C _ {E L} + \Sigma C _ {M C}\right)
$$

$C_{BE}$ : Concentration of the main element (or Internal Standard) 

$C_{EL}$ : Element concentration 

$C_{MC}$ : Concentration of correction not required element 

b. Calculate the virtual content of each element. (called also 100% corrected content) 

Virtual concentration = $\frac{C_{EL}}{\frac{C_{BE}}{100}}$ 

c. Register the virtual concentration (100% corrected content) in the chemical analytical value registration table to obtain working curve coefficients. If you register Y in "Auto-Calculation Chemical Analytical Value for 100% Connection (See SETUP GUIDE)" the Virtual concentration is calculated automatically. For an element which does not require 100% correction, register a chemical analytical value to obtain working curve coefficients. 

A calculation procedure is as follows: 

$$
C _ {B E} + \Sigma C _ {E L} + \Sigma C _ {M C} = 1 0 0
$$

$C_{BE}$ : Concentration of internal standard (concentration of a main component element) 

$C_{EL}$ : Concentration of a target element for internal standard element correction 

$C_{MC}$ : Concentration of a correction not required element 

From the formula above, the content of the main component element of the sample measured can be obtained as follows: 

$$
C _ {B E} + \Sigma C _ {E L} = 1 0 0 - \Sigma C _ {M C} \quad \text { or } \quad C _ {B E} (1 + \Sigma C _ {E L}) = 1 0 0 - \Sigma C _ {M C}
$$

$$
\frac {C _ {B E}}{1 0 0} = \frac {1 0 0 - \Sigma C _ {M C}}{1 0 0 + \Sigma \frac {C _ {E L}}{\frac {C _ {B E}}{1 0 0}}}.
$$

The corrected concentration ( $C_{N0}$ ) of a given element is: 

$C_{NO} = \frac{C_{BE}}{100} \cdot \frac{C_{EL}}{\frac{C_{BE}}{100}} <----$ Value obtained from the working curve
The content of the main component element of the analytical sample 

Therefore, 

$$
\frac {C _ {B E}}{1 0 0} = \frac {1 0 0 - \Sigma C _ {M C}}{1 0 0 + \Sigma \frac {C _ {E L}}{\frac {C _ {B E}}{1 0 0}}} \cdot \frac {C _ {E L}}{\frac {C _ {B E}}{1 0 0}}
$$

Channel skip is used when the working curve is divided into low-content and high-content ones, or when there are two analytical wavelengths. Input in the item POINT the content when dividing the working curve, and "+" in the item SKIP of the element with a low range of use. 

** (Insert graph drawing)** 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/320171fb4fb132707979037961f6b995c79171a79636c051d87f1deb1172f198.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/53c597e0b4e636b2d82721387d02d10da9d3e7c9248d8893bdc3c89b62281c71.jpg)


① Cr low-content working curve 

② Cr high-content working curve 

When dividing the working curve with 1 analytical wavelength. 

When there are 2 analytical wavelengths. 

## 5.9 Registration of the Matrix Element Correction Coefficient

From the Working Curve Coefficient screen, pressing the F2 (Next) key displays the Matrix Element Correction Coefficient Registration screen. 

In this table, input the name of the element requiring correction and the coefficients. 

```txt
Analytical Information Date 04-01-93 Time 16:18
(6) Matrix Correction Coefficients A.CON = 6 W.GRP = 1
AR-No. NAME D/L AR-No. NAME COEFF. D/L AR-No. NAME COEFF.
5 P 1 L 8 Ni -.00110000 2 L 9 Cr -.00036000
3 L 10 Mo -.00990000 4
5
7
6 S 1 L 4 Mn -.00100000 2
3
5
7
7 Cu 1 L 8 Ni -.00350000 2
3
5
7
8 Ni 1
3
5
7
D or L D or L
Correction equation C=Co(1+Δdj*Cj)+Δlj*Cj
1:Menu 2:Next 3:Pre. 5:Help 6:Elem 9:Init 10:Submenu 
```


FIGURE 5.8: Input Example of Matrix Correction Registration Screen


D/L : Input a type of matrix element correction formula. 

L : Correction element is an overlapping type. 

D : Correction element is an absorption excitation type. 

AR-No. : Input the Ar-No. of a correction element. 

NAME : Displays an element name corresponding to the AR-No. 

COEFF : Input a matrix element correction coefficient. The coefficient is filed after calculating the matrix element correction coefficient. 

Pressing the ENTER key validates the input and moves the cursor to the next entry item (D/L, AR-No., COEFF). 

One screen displays information for 4 elements. Press the PgUp or PgDn key to view other elements. 

Press F6 (ELE) to display a list of the elements and the AR-No. To remove the window press ESC key. After inputting the information, press the F2 (Next) key. The Master Curve correction Sample and Target Value Registration screen then appears. (Section 5.10). 

The matrix element correction can only be used to correct for an obvious interference. 

The determination of the interelement effects must be done carefully, and the number of standards large enough to maintain the precision. The use of unnecessary correction affects the accuracy and the precision of the analysis. 

After the correction coefficients are registered, all subsequent results will be calculated with the proper coefficients. 

In Optical Emission Spectroscopy, the major effects of matrix elements observed are : 

① When an element is absorbed or excited by another element. (Mn/S in Steel) 

Note: An inappropriate discharge may increase the phenomena 

② When the spectrums of two elements overlap. The wavelength of the given element is interfered by a close wavelength of another element. The resolution of the spectrometer is not sufficient enough to separate the two wavelengths. 

Generally, number ① is called absorption excitation correction, and number ② is referred to as overlapping correction. Overlapping correction is more general for the emission spectral instrument. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/852461d2440057795c87b14c5baf33f30ebc84782cbd29f4ded8491612519568.jpg)


C : Post-correction content of a quantitative element 

$C_{0}$ : Pre-correction content of a quantitative element 

$C_{i}$ : Measured content of a correction element 

$d_{j}$ : Absorption excitation correction coefficient 

$\ell_{j}$ : Overlapping correction coefficient 

## (Note 1) Caution for channel skip

On a channel skip, the calculation of the correction coefficient should be performed separately on each section of the working curve. If the channel skip is performed on the analytical range of the same wavelength, the calculated coefficient may be identical for both section of the working curve. 

(Note 2) When registering two or more matrix elements, register them continuously. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/5fe88fd5d413606aecb737084937280c3723193cb74fc6856590e46d255eedb6.jpg)


FIGURE 5.8.1: Input Example of Matrix Element Correction Coefficient When Performing Channel Skip and Display Example of Element Name Window 

5.10 Registration of the Master Curve Correction Sample and Target Value From the Matrix Element Correction Coefficient Registration screen, pressing the F2 (Next) key displays the Master Curve Correction Sample and Target Value Registration screen. 

```csv
Analytical Information Date 04-01-93 Time 16:20
(7) Master Curve Correction (Sample No., Target, Range & Coefficient)
A.CON = 6 W.GRP= 1
AR-No. NAME SPL TARGET D1 D2 AC MC
1 Fe .00000 .00000 .00000 .00000 1.0000 Co: Result
2 C .00000 .00000 .00000 .00000 1.0000 SPL: Sample No.
3 Si .00000 .00000 .00000 .00000 1.0000 TARGET: Ct
4 Mn .00000 .00000 .00000 .00000 1.0000 Target content of
5 P .00000 .00000 .00000 .00000 1.0000 specified sample
6 S .00000 .00000 .00000 .00000 1.0000
7 Cu .00000 .00000 .00000 .00000 1.0000 Correction Condition
8 Ni .00000 .00000 .00000 .00000 1.0000 1.Ct-D1<Co<CT+D1
9 Cr .00000 .00000 .00000 .00000 1.0000 MC=1.0 AC=O.
10 Mo .00000 .00000 .00000 .00000 1.000C 2.Ct-D2<Co<CT-D1
11 Al .0.ooooo .ooooo .ooooo 1.ooooo Mc=Ct/Co
12 V .ooooo .ooooo .ooooo .ooooo 1.ooooo Ct+D1<Co<CT+D2
13 Ti .ooooo .ooooo .ooooo .ooooo 1.ooooo AC=Ct-Co
14 Sn .ooooo .ooooo .ooooo .ooooo 1.ooooo 3.Ct-D2>Co,Co>CT+D2
15 Nb .ooooo .ooooo .ooooo .ooooo 1.ooooo 'Error' display
16 B .ooooo .ooooo .ooooo .ooooo 1.ooooo
D1: Correction Limits (Not Required) D2: Correction Limits (Required)
1:Menu
2:Next 3:Pre. 4:Print 5:Help 9:Init 1O:Submenu 
```

FIGURE 5.9: Input Example of Master Curve Correction Sample and Target Value Registration 

```txt
NAME : Displays an analytical element name.
SPL : Input a master curve correcting sample name. (1 character)
TARGET: Input a target value in 6 digits, including a decimal point
D1 : Input a lower limit control width in 6 digits, including a decimal point
D2 : Input an upper limit control width having 6 digits, including a decimal point
AC : Set a master curve coefficient for AC using 6 digits, including a decimal point
MC : Set a master curve coefficient for MC using 6 digits, including a decimal point and a sign 
```

AC and MC are filed by performing a master curve correction analysis. Pressing the ENTER key moves the cursor to an entry item (SPL, TARGET, D1, D2, AC, MC). 

When inputting the information, press the F2 (Next) key. Section 5.11, "Analytical Element Display and Printing Order Registration" screen, appears. 

Master curve correction is also referred to as "y" correction. It corrects a difference between the content analyzed with a created working curve and a chemical analytical value. 

<table><tr><td>(-) Side</td><td>C+</td><td>(+) Side</td></tr><tr><td></td><td>D1</td><td>D1</td></tr><tr><td></td><td>D2</td><td>D2</td></tr></table>

$C_{t}$ : TARGET content 

$C_{0}$ : Quantitative value from the working curve
(Sample with a known curve) 

$D_{1}$ : Lower limit control width 

$D_{2}$ : Upper limit control width
(Correction required content range) 

Calculation formula for the correction coefficients AC and MC 

1) If a value of $C_{0}$ is in a range of $C_{t} - D_{1} \leq C_{0} \leq C_{t} + D_{1}$ , there are no correction MC = 1 and AC = 0. 

2) If a value of $C_0$ is in a range of $C_t - D_2 \leq C_0 \leq C_t - D_1$ or $C_t + D_1 \leq C_0 < C_t + D_2$ , the correction coefficients are calculated as follows; 

$$
\mathrm{MC} = \mathrm{C} _ {\mathrm{t}} / \mathrm{C} _ {0} \text { and } \mathrm{AC} = \mathrm{C} _ {\mathrm{t}} - \mathrm{C} _ {0}.
$$

3) If a value of $C_0$ is in a range of $C_0 < C_t - D_2$ or $C_0 > C_t + D_2$ , the coefficients are not calculated and the message, <Error display!>, is displayed. The value of the previous calculation are used in analysis. 

Master curve correction analysis 

When making an analysis in master curve correction, the content of an analyticalvalue is calculated by the following formulas and printed. 

When a quantitative value C, upon analysis of an unknown sample, is found to be: 

1) $C > C_{t}$ then $C_{AC}$ is calculated as $C_{AC} = C + AC$ and printed. 

2) $C > C_t$ then $C_{MC}$ is calculated as $C_{MC} = C \times MC$ and printed. 

5.11 Registration of the Analytical Element Display and Printing Order
From the Master Curve Correction Sample and Target Value Registration screen, pressing the F2 (Next) key displays the Analytical Element Display and Printing Order Registration screen. 

This table contains the information for the CRT display and printer format. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/c13b8c24f9273661bee730c14e58a68e527a222084d708d662498188bd5620e5.jpg)



FIGURE 5.10: Input Example of Analytical Element Display and Printing Registration Screen


## NAME : Analytical element name

ORDER: When outputting the element list to the printer, the order of the elements are set with this list. Element with an order value of 0 will not be sent to the printer. When using the channel skip procedure for an element, both entries must have the same order value. 

FIG. : Input the number of display and printing characters for the content. 

DECI : Input the number of digits beyond the decimal point. 

MAGN.: Enter the value for the exponent, for which 10 is to be its base, to be used as a multiplier. For example, if the value of 4 is entered, and the analysis value is 0.0021%, the display will be 21.0 (104 * 0.0021%). 

Pressing the ENTER key moves the cursor to an entry item (ORDER, FIG., DECI., MAGN.). 

After inputting the required information, press the F2 (Next) key. The screen changes to the Purity Calculation Information Registration screen (Section 5.12). 

(Note 1) The value input in FIG-15 specifies the number of digits excluding a decimal point. Only 0 through 6 can be inputted. 

(Note 2) When 0 is specified in FIG., a 6-digit floating decimal point display results. At this time, you cannot input a value other than 0 in DECI. 

(Note 3) The value specified in DECI is the number of decimal places displayed.
However, when 0 is specified, the value input in FIG. becomes meaningless and an integer display is specified. 

(Note 4) For MAGN., specify within a range which does not exceed the number of digits specified in FIG. and DECI. 

Example: When analytical value is .12345 

Fig. Deci. Magn. Data Display
(Note 2) 0 0 0 .12345
(Note 3) 3 3 0 .123
(Note 3) 4 0 2 12
(Note 4) 4 2 2 12.34
(Note 4) 4 2 3 **** (display exceeding the number of digits)
(Display data is 123.4, exceeding the number of digits) 

(Note 5) If an analytical order is altered halfway through an analysis, preceding and following data cannot be used for editing data for report preparation and X-R control. 

## 5.12 Registration of the Data Transmission Format

From the Analytical Element Display and Printing Order Registration screen, pressing the F2 (Next) key displays the Data Transmission Format Registration screen. 

This table contains the information for the CRT display and printer format. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/fcec81bbcd00566ee9de06b0c17aa25cce5586fb85252c763610d3fd2f0c6db4.jpg)



FIGURE 5.11: Input Example of Data Transmission Format Printing Registration Screen


## NAME : Analytical element name

ORDER: When the element list to the Upper computer the order of the elements are set with this list. Element with an order value of 0 will not be sent to the Upper computer When using the channel skip procedure for an element, both entries must have the same order value. 

FIG. : Input the number of transmitting characters for the content. 

DECI : Input the number of digits beyond the decimal point. 

MAGN.: Enter the value for the exponent, for which 10 is to be its base, to be used as a multiplier. For example, if the value of 4 is entered, and the analysis value is 0.0021%, the transmitting value will be 21.0 (104 * 0.0021%). 

Pressing the ENTER key moves the cursor to an entry item (ORDER, FIG., DECI., MAGN.). 

After inputting the required information, press the F2 (Next) key. The screen changes to the Purity Calculation Information Registration screen (Section 5.12). 

(Note 1) The value input in FIG specifies the number of digits excluding a decimal point. Only 0 through 6 can be inputted. 

(Note 2) When 0 is specified in FIG., a 6-digit floating decimal point transmit results. At this time, you cannot input a value other than 0 in DECI. 

(Note 3) The value specified in DECI is the number of decimal places transmitted.
However, when 0 is specified, the value input in FIG. becomes meaningless and an integer transmission is specified. 

(Note 4) For MAGN., specify within a range which does not exceed the number of digits specified in FIG. and DECI. 

Example: When analytical value is .12345 

<table><tr><td></td><td>Fig.</td><td>Deci.</td><td>Magn.</td><td>Data Transmit</td></tr><tr><td>(Note 2)</td><td>0</td><td>0</td><td>0</td><td>.12345</td></tr><tr><td>(Note 3)</td><td>3</td><td>3</td><td>0</td><td>.123</td></tr><tr><td>(Note 3)</td><td>4</td><td>0</td><td>2</td><td>12</td></tr><tr><td>(Note 4)</td><td>4</td><td>2</td><td>2</td><td>12.34</td></tr><tr><td>(Note 4)</td><td>4</td><td>2</td><td>3</td><td>**** (data exceeding the number of digits)</td></tr></table>

(data is 123.4, exceeding the number of digits) 

## 5.13 Registration of the Purity Calculation Information

On the Data Transmission Format Registration screen, pressing the F2 (Next) key displays the Purity Calculation Information Registration screen. 

```txt
Analytical Information Date 04-01-93 Time 17:03
(10) Purity Calculation A.CON = 1 W.GRP = 1
AR-No. NAME +/- AR-No. NAME +/- Calculation Y/N = N
1 Fe2 17
2 C 18
3 Si 19 Calculation Equation
4 Mn 20
5 P 21 Cb: Content of '+' specified ele-
ment(base element)
6 S 22 Ce: Content of '-' specified ele-
ment
7 V 23
8 Cu 24
9 Ni 25
10 Cr 26 space: ' No Selection
11 Nb 27
12 Al 28
13 Sn 29 Cb=100-(Ge1+Ce2+ )
14 Mo 30
15 31
16 32
+ or - + or -
1:Menu + or -
2:Next 3:Pre. 4:Print 5:Help 9:Init 10:Submenu 
```


FIGURE 5.12: Input Example of Purity Calculation Information


Registration Screen 

```txt
Calculation Y/N: Specify whether to calculate purity.
+/-: Specify an element to be calculated as :
+ : Input to a main component element.
- : Input to an element used for purity calculation.
_ : Input to an element not used for purity calculation.

Purity calculation is to calculate the content of main components, subtracting a quantitative value of impurity elements from 100%.

<Calculation Formula>
100% = C_b + C_e    C_b: Content of main component elements
C_e: Quantitative value of impurity elements
∴ C_b = 100 - ΣC_e

(Note 1) Input ORDER number for the main component elements in the Analytical Element Display and Printing Order Registration Table (Section 5.11).

(Note 2) Enter _ for a virtual element in a special calculation formula. 
```

## 5.14 Registration of Standard Name and Standard Value

1) Registering the standard name (or product names) 

From the Analytical Information Sub-menu FIGURE 3, select the <Standard Information> mode with the key ↑ or ↓, and press the ENTER key. The Standard Name Registration screen is displayed. 

In this table, register standard names and ST-Nos. to be judged upon analysis and select the standard names when registering standard values. Up to 500 standard names can be registered. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/0147124c6ae08480628a12d82f83ee040e5d88b4769c48100fa0315fe85e250f.jpg)



FIGURE 5.13: Input Example of Standard Name Registration Screen


ST-No.: Standard name (or Product name) Number (up to 500 names) 

NAME : Register the standard name (or Product name) within 10 characters. 

Since the cursor is moved by pressing the ENTER, TAB, ↑, ↓, ←, → input the standard name and press the ENTER key. Only 40 standard names can be displayed on one screen. When you want to input to other ST-Nos., change the screen with the PgUp or PgDn key. 

When you want to register a standard name, move the cursor to the standard name where you want to input it, and press the Fl (Select) key. The Standard Check Standard Value (or Product Specifications) Registration FIGURE 18 appears. 

## 2) Registering the Standard Values (or Product Specifications)

On the Standard Name Registration screen, select the standard name and press the Fl (Select) key. The Standard Value Registration screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/bfe50c68504fd74d952e8f6122a86f0b64e0ce71aa24c780f08803381d94c37a.jpg)


FIGURE 5.14: Input Example of Standard Check Reference Value Registration Screen 

NAME : Input an element name (5 characters). 

UPPER: Input an upper-limit standard value in 6 digits, including a decimal point. 

LOWER: Input a lower-limit standard value in 6 digits, including a decimal point. 

TRACE: Input a trace value in 6 digits, including a decimal point. 

When an analytical value is over the upper-limit standard value (UPPER), H is printed after an average value. 

When the analytical value is below the lower-limit standard value (LOWER), L is printed after an average value. 

When the analytical value is below the lower-limit standard value and (TRACE), the average value is printed as Tr. 

Pressing the ENTER key validates an input value and moves the cursor to the next entry item (ELEMENT, UPPER, LOWER, TRACE). Input information required. 

After inputting the information, press F2 (Next). The Standard Name Registration FIGURE 5.13 then appears. 

(Note) In the table (Figure 5.14), register the same element names as those registered in Section 5.6 Registration of Analytical Element. 

## 5.15 Registration R Control Value

## 1) Selecting the R Control Group

On the Analytical Information Sub-menu Screen, select the <Coefficient of equation for variance check> mode with the key $\uparrow$ or $\downarrow$ and press the ENTER key. The R Control Group Selection screen is displayed. In this table, select an R control value registration group. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/3aa4a1c61737f2c286d11b0fc03f2fae92bd2795bf993983cd07e6f80c5f3428.jpg)



FIGURE 5.15: R Control Group Selection Screen


Using the keys $\uparrow$ , $\downarrow$ and $\leftarrow$ and $\rightarrow$ , select the R control value registration group and press the F1 (Select) key. The R Control Value Registration FIGURE 5.16 is displayed. 

Only 20 groups in one screen can be displayed. When you want to select other groups, select the screen with the PgUp or PgDn key. 

(Note) There is the R Control Value Registration Table for each analytical condition group (10 groups). 

## 2) Registering the R Control Value

If you select a group in the R Control Group Selection screen, the R Control Value Registration screen will be displayed. In this table, set a value to R-controlled for each of the analytical condition groups (20 groups) in terms of quadratic equation. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/77dfd62df643d1661debb3f61b22f9b4e4d894a3e2ddb1047b116c9bf8d707d4.jpg)



FIGURE 5.16: Input Example of R Control Value Registration Screen


## ELE : Integrator element name

A.B.C.: A coefficient for R control value calculation formula can be input up to 8 digits, including a decimal point. 

Pressing the ENTER key moves the cursor to an entry item (A.B.C.). Input information required. After inputting information, press the F2 (Next) key. The R Control Group Selection FIGURE 5.15 is displayed. 

It has R control information per analytical condition group and analytical element. 

If R control is performed at the same rate of control width in low content and high content ranges, control in the low content range will become more severe than that in the high content range. In order to perform equivalent control in all content ranges, plot R versus the content in approximate of quadratic equation as shown in the figure below and judge it acceptable if R of an analytical result is within an oblique line part. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/fc731cc98d73eeb01f85b33de5a93e8765a1f9954fe76d81e6a64c3d1955d804.jpg)


Content % 

The control value, R, is obtained as follows: 

$R = AC^{2}_{0} + BC_{0} + C$ $C_{0}$ : Average value of multiple analyses 

For a judgement of R control: 

$$
C _ {\min} - C _ {\max} > R
$$

$C_{max}$ : Maximum value of multiple analysis 

$C_{min}$ : Minimum value of multiple analysis 

In this case, R is printed after an analytical value because it is beyond R control. 

## 5.16 Registration of Special Calculation Formula

1) Selecting the Special Calculation Formula Group 

On the Analytical Information Sub-menu FIGURE 5.1, select the <Information for calculation of physical constant> mode with the key ↑ or ↓ and press the ENTER key. The Special Calculation Formula Group Selection screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/d04d41d82ba0fa90e1d050f1c71b16f537b7752c81fd65c564505b144aae983c.jpg)



FIGURE 5.17: Special Calculation Formula Group Selection Screen


Select a special calculation formula group with the key $\uparrow$ , $\downarrow$ , $\uparrow$ , or $\rightarrow$ and press the Fl (Select) key. The Special Calculation Formula Registration (FIGURE 5.17) is displayed. 

Only 20 groups can be displayed in one screen. When you want to select other groups, select with the PgUp or PgDn key. 

(Note) You can register 5 special calculation formulas per analytical group (500 formulas total). They cannot be shared among different analytical groups. 

2) Registering the Special Calculation Formula
The Special Calculation Formula Registration screen is displayed by selecting a group on the Special Calculation Formula Group Selection screen. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/04d384897691ad4c1b6d889aac05b898ae9d95910a52ee487f52233a8f951326.jpg)



FIGURE 5.18: Special Calculation Formula Registration Screen (Initial Screen)


$$
\mathbf {A G - N O}.
$$

$$
\text { Exp. } = 1 - 5
$$

: Analytical group 

: Special calculation formula registration group 500 formulas for 100 analytical group, with 5 formulas per analytical group. 

Assigned for each analytical group. 

Exp. ( ) : Indicates the special calculation formula Number created and a formula area.
(For the area display area, a total of coefficients, element names and operators is up to 16, or the number of input characters is within 64). 

Imaginary integrator: Virtual integrator 

ITG : Virtual integrator Number 57-61 (ITG No. to be registered in the Analytical Element Registration Table (Section 5.6)) 

NAME : Virtual integrator name (5 characters) 

Exp. No. : Special calculation formula registration number 

ORDER/NAME : Displays the order number registered in the Analytical Element Display and Printing Order Registration Table (Section 5.11) and the element name 

Message area : Entry area for the virtual integrator name and creation of the special calculation formula. 

Additional Explanation of Function Keys 

F2 (Next) : Changes to the Special Calculation Formula Group Selection screen 5.16 

F6 (Exp) : Displays the Special Calculation Formula Section screen. When you want to delete it, press the ESC key. 

F7 (Reset): Clears the special calculation formula for the item "Exp. ( )" 

F8 (Set) : Registers the virtual integrator name "NAME" 

Explanation of Special Calculation Formula 

For example, there are carbon equivalent values (CE values, the carbon (C) and silicon (Si)), that affect a material of cast iron the most. These CE values are calculated and printed after completing an analysis. 

This table registers various calculation formulas, such as a carbon equivalent calculation formula into virtual integrator numbers and allows them to be called in the Analytical Element Registration Table (Section 5.6). 

A calculation formula is: 

$$
\mathrm{X} = \sum_ {n = 1} ^ {1 6} \mathrm{Ki} \quad \mathrm{Ci} + \mathrm{Ko}
$$

Ki: Coefficient to an analytical element 

Ci: Analytical element 

$K_{0}$ : Fixed constant 

This example is described with the carbon equivalent (CE value) of cast iron. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/b216be60b831b26afc02db2a45412ca98ce94854e265adcbcfc0bf8ccdb1bf54.jpg)


The following describes a procedure for registering the above formula: 

<Operating Methods> 

I) Registering the Virtual Integrator Name 

① Press the F8 (Set) key in FIGURE 22, Initial screen. <Message> are is made ready for accepting an entry of virtual integrator name. 

② Enter the virtual integrator name (5 characters) corresponding to ITG No. and press the ENTER key. 

③ The virtual integrator name entered is set in the item Imaginary integrator Name. 

④ Special calculation formula Exp. (No.) changes to the next number. When you want to enter another virtual integrator name in the same manner, press the F8 (Set) key and repeat the steps 1 through 3. 

⑤ When you want to alter an already registered virtual integrator name, press F6 (Exp.) key to display the <Exp. table> window. Next, using the key ↑ or ↓, move the cursor to the item EXP. () and press the ENTER key. The rest of the operation is the same as step 1. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/b6448a860fe1f185ee12d2649d2c1aeb43fd3d96be244d44767f0379c6f2cef6.jpg)



FIGURE 23: Registration of Special Calculation Formula and Virtual Integrator Name


II) Registering the Special Calculation Formula 

① After the virtual integrator name is registered, press the F6 (Exp.) key. The <Exp. table> window is displayed on the lower side of the screen. 

② Using the key $\uparrow$ or $\downarrow$ , move the cursor to the Exp. (No.) item to be entered, and press the ENTER key. 

③ The <Message area> item is made ready for accepting an entry of special calculation formula. 

<table><tr><td>Sign desired to be entered</td><td>Sign entered</td><td>Message displayed in Message Area</td></tr><tr><td>1</td><td>— ENTER</td><td>1st Coefficient</td></tr><tr><td>C</td><td>1 ENTER</td><td>1st Order</td></tr><tr><td>+</td><td>+ ENTER</td><td>2nd Operator</td></tr><tr><td>1/3</td><td>1/3 ENTER</td><td>2nd Coefficient</td></tr><tr><td>Si</td><td>2 ENTER</td><td>2nd Order</td></tr><tr><td>+</td><td>+ ENTER</td><td>3rd Operator</td></tr><tr><td>1/4</td><td>1/4 ENTER</td><td>3rd Order</td></tr></table>

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/bbe93a6afe727a2a4ad125bb3088803a3802b0728122e3d4fa72a5946a0e4448.jpg)



FIGURE 5.20: Registration of Special Calculation Formula


⑤ When you want to enter a calculation formula to another integrator, press the F6 (Exp.) key to display the <Exp. table> window. Then, using the key ↑ or ↓, select a virtual integrator number and press the ENTER key. 

⑥ The selected virtual integrator is made ready for accepting an entry of calculation formula. 

⑦ Perform the same operation as outlined in Step 4. 

III) Checking the Special Calculation Entry State 

If you press the TAB or SHIFT + TAB (or $\leftarrow / \rightarrow$ ) when the item <Message area> is ready for accepting a calculation formula, the cursor will move to the coefficient item, Order item, and Operator item of Exp. (No.). The contents of a relevant item are displayed at the <Message area> item. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/cdae871ab876b7ad4a3b07b896134c9f2bbee44eb730e562edc4578465321dcb.jpg)



FIGURE 5.21: Display Example of Special Calculation Formula


IV) Checking the Special Calculation Formula Registration State 

When you want to check a special calculation formula registration state, press the F6 (Exp.) key. The Exp. table window is displayed at the lower part of the screen. When deleting the window, press the ESC key. 

## V) Altering the Special Calculation Formula

When altering part of the registered calculation formulas, press the F6 (Exp.) key, to display the <Exp. table> window, and then select the calculation formula to be altered using the key $\uparrow$ or $\downarrow$ . Next, using TAB, SHIFT + TAB (or $\leftarrow$ $\rightarrow$ key), move the cursor to the entry item to be altered and change its contents. 

(Note) When you want to delete all or part of the registered calculation formulas, press the F7 (Reset) key to delete all the calculation formulas and then enter again. 

VI) Precautions for Registering the Special Calculation Formula 

① A calculation formula can contain up to 64 characters, with a maximum of 16 coefficients. 

② A fixed constant should be entered at the end of the calculation formula. 

③ The coefficient, element name, operator and fixed constant should be entered with no space among them. 

④ A virtual integrator name should be entered continuously. 

⑤ When only the virtual integrator name has been registered and no calculation formula has been registered, do not press SHIFT + F1 (Menu), F2 (Next), F9 (Init) or F10 (Sub-menu). 

⑥ Do not enter a virtual integrator element in the calculation formula. 

⑦ When you want to use the special calculation formula in other analytical groups, register it separately. 

## 5.17 Analytical Information Copy

On the Analytical Information Sub-menu FIGURE 5.1, select the <Copy from different analytical group> mode with the key ↑ or ↓ and press the ENTER key. The Analytical Information Copy screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/f6eb5db7f166a45d71e528a93af559ca07676d220fd507c125d85836f9cededd.jpg)



FIGURE 5.22: Display Example of Analytical Information Copy


AG-No.: Analytical group number 

NAME : Analytical group name 

Additional Explanation of Function Keys 

Fl (Select): Selects a copy source and a copy destination for an analytical group 

F7 (Copy) : Executes copying of analytical information 

## <Operating Method>

1) Select an analytical group, using the keys PgUp, PgDn, TAB, ↑, ↓, ←, +. 

2) Move the cursor to the item Group Name of the copy source. 

3) Press the Fl (Select) key. A group name is displayed at the item Source on the screen. 

4) On the upper right part of the screen. <Select destination> is displayed. Next, move the cursor to the item Group Name of the copy destination and enter a group name. 

5) With the cursor placed at the item Group Name of the copy destination, press the Fl (Select) key. On the upper right part of the screen, "Press F7 (Copy) !" is displayed. 

6) Press the F7 (Copy) key. Copying of analytical information starts. 

7) When you want to successively copy to another analytical group, repeat Steps 2 through 7. 

8) After copying is completed press SHIFT + Fl (Menu), F9 (Init) or Fl0 (Sub-menu). 

## 5.18 Registration of Element Name and Wavelength

From the Analytical Information Sub-menu screen, select the <Element name and Wavelength> mode with ↑ or ↓ and press the ENTER key. The Element Name and Wavelength Registration screen is displayed. 

Shimadzu will enter the element name and the wavelength during the initial configuration of the system. Do not enter or change any information on this screen. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/5d5e87a9deeccea7a5db2f4e678cdf3012f7e160ff885fe842c737915cef629b.jpg)


ITG: Displays integrator Number 1 ~ 45. 

ELE: Enter an element name within 5 characters.
(Do not enter the same name.) 

WL : Enter a wavelength within 6 digits, including a decimal point.
(unit: nm) 

## 5.19 Registration of Histogram Control Value

## 1) Registration of Histogram Control Group Name

Select the <Histogram control value registration> mode on the analytical information sub-menu screen using ↑ or ↓ and press ENTER key. The analytical group selection screen is then displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/02bba8389b4a9836dd8adcd5601f02c6965148bc802aa5f272477b240c3952c8.jpg)



FIGURE 5.24: Analytical Group Selection Screen


Select the group name under which histogram control values are to be registered using $\uparrow$ , $\downarrow$ , $\leftarrow$ , and $\rightarrow$ keys. Press F1 (Select) key. 

The histogram control value registration screen (2) is then displayed. 

Only 20 groups are displayed on a single screen at a time. To display any other group, select an appropriate screen using PgUp or PgDn key. 

(Note) The histogram control value registration table is provided for each analytical condition group (10 groups). 

AG-No. : Analytical condition group No. (1 to 100 groups) 

A. CON : Analytical condition group No. (1 to 10 groups) 

W. CRP : Calibration curve group No. (1 to 100 groups) 

Group name: Analytical group name (Displayed here is an analytical group name registered on the analytical group name registration screen.) 

2) Registration of Histogram Control Value 

Specify a desired group name on the analytical group selection screen. The histogram control value registration screen is then displayed. 

In this table, set control values and class mark with which a histogram is created for each analytical group (10 groups). 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/0c293700f90a3786a7df2f3569abb5c62cac57a56c6f3e4086db6f97b805614e.jpg)



FIGURE 5.25: Entry Example of Histogram Control Value Registration Screen


Upper limit: Enter the upper limit of a histogram. Up to eight digits including a decimal point are accepted. 

Lower limit: Enter the lower limit of a histogram. Up to eight digits including a decimal point are accepted. 

Class mark : Enter the class mark (number of partitions) between the lower and upper limits of a histogram. Up to 15 can be entered. 

The control width between the lower and upper limits is divided by the class mark. Each partition is used as one class when a histogram is created. 

After entering the above information, press F2 (Next) key. The system then returns to the analytical group selection screen. 

From the Analytical Information Sub-menu FIGURE 3, select the <Analytical group using same analytical group> mode with the key ↑ or ↓ ,and press the ENTER key. The recalibration group Registration screen is displayed. 

In this table, register number of analytical condition group (A.CON) you want to use its recalibration correction coefficients for other A. CON. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/1738abb933cc5f3812f3de382c01ed82b8d5a2f60ba2b5f2084dfeb017f49742.jpg)



FIGURE 5.26: Input Example of Analytical Group Using Same Analytical Condition Group Screen


A. CON. : Destination of recalibration convection coefficients. 

USED A. CON: Number of A. CON you want to use its recalibration correction coefficients. 

In USED A. CON area, if you register the number of A. CON. you want to use, its recalibration correction coefficients is used for the A. CON in A. CON area. 

(Note) A. CON and USED A. CON must have same analytical element. 

6. ADJUSTMENT OF ATTENUATOR SENSITIVITY 

## 6. ADJUSTMENT OF ATTENUATOR SENSITIVITY

On the Master Menu screen, move the cursor to the <Attenuator adjustment> mode with the key ↑ or ↓ and press the ENTER key. The Attenuator Sensitivity Adjustment screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/a151bd4c552fe79329bc1fb9a89fd91d381b4eb294de58b6d90278d1fab6d11f.jpg)


FIGURE 6.1: Display Example of Attenuator Sensitivity Adjustment Screen 

AG-No : Enter the name of the analytical group. 

Element : Enter the name of the element requiring adjustment. The name must be entered exactly as it appears in the <Element Name and Wavelength Table> (see section 5.17 Registration of Element Name and Wavelength). 

ATT : Displays the filed attenuator value. 

Scale : The scale value is a multiplier that extend the range of the graph. The scale range is 1 through 9 and 0, with 0 being 10 times. 

Sequence : Displays the sequence Number registered for the analytical element of the selected analytical group. 

Source No: Displays the source Number registered for the analytical element of the selected analytical group. 

Explanation of Function Keys 

Fl (Start): Starts the emission 

F2 (Stop) : Stops the emission 

F3 (Pause): Stops the emission, the next start command (F1) resets the display. 

F4 (Copy) : Outputs the screen to the printer. 

F5 (Help) : Displays the Help screen. To return to the attenuator adjustment screen, press the ESC key. 

F7 (Reset): Clear the display 

F8 (-HV) : Turns on/off -HV 

SHIFT + Fl: Displays the Master Menu screen (Menu) 

## <Operating Method>

1) Press the F8 (-HV) key to turn on -HV. When the high voltage is activated the -HV screen item will be highlighted. 

2) Enter the analytical group name AG-No and press the ENTER key. 

3) The cursor moves to the element name after AG-No has been entered. Enter the element name exactly as it appears in the Element name and Wavelength table. After pressing enter the cursor moves to the ATT item and displays the current value, the sequence number and the source number. 

4) Move the cursor to the item Scale with the key and enter Scale 0 ~ 9. 

<table><tr><td>Emission Unit</td><td>Scale</td><td>Graduation</td><td>Integrating Time</td><td>(Constant-time Integral)</td></tr><tr><td>HPSG-300</td><td>×2</td><td>6 ~ 7</td><td>4 sec.</td><td>0.5 ~ 0.6</td></tr><tr><td>HVS</td><td>×5</td><td>4 ~ 5</td><td>15 sec.</td><td>0.5 ~ 0.6</td></tr></table>

5) Select the working curve standard sample with the highest content for the element entered in step 3. 

6) Set the sample onto the emission stand, and press Fl to start the emission. 

The screen displays an intensity for the current ATT value. 

7) Move the cursor to the item ATT, and adjust the intensity level with the key $\uparrow$ or $\downarrow$ . 

The key $\downarrow$ decreases the ATT value by 1, and $\uparrow$ increases it by 1. When the intensity value is correctly set press F2 to stop. 

8) To adjust the sensitivity of different element, move the cursor to the Element item and enter the analytical element name. Do the same operation as in Step 7. 

(If Source Number varies from one element to another, emission will be temporarily interrupted). 

9) When an intensity display comes to the bottom of the screen, the emission automatically stops. 

10) Pressing the F7 key (Reset) erases the display. If you press the F1 key (Start) to start an emission without pressing F7 (Reset), the a display will be overlapped. 

11) When you want to adjust attenuator sensitivity for another analytical group, press SHIFT + TAB to move the cursor to the entry item Ag-No. 

After completing adjustment, press F9 (Init) or SHIFT + F1 (Menu) to return to the Analysis mode. 

(Note 1) Before processing in this mode, be sure to register the analytical information of <Information INT. l>. 

(Note 2) Values for the items Element, Scale and ATT can be altered even during emission. 

(Note 3) The set ATT value is automatically filed by pressing any function key other than F4 (Copy) and F5 (Help). 

(Note 4) For the items Sequence and Source for each element, those registered in the analytical Information Table are displayed. Be careful not to cause overflowing because analytical sensitivity differs depending on a Source condition. 

7. REGRESSION CALCULATION 

7. REGRESSION CALCULATION 

Registration of Standard Sample 

Calculation of Working Curve Coefficient 

Matrix Element Correction Coefficient Calculation 

## 7. REGRESSION CALCULATION

7.1 Registration of Chemical Analytical Value 

7.2 Registration of Standard Sample 

7.3 Calculation of Working Curve Coefficient 

7.4 Matrix Element Correction 

7.5 Matrix Element Correction Coefficient Calculation Type 1 (Two-Element Method). 

7.6 Matrix Element Correction Coefficient Calculation Type 2 (Multi-Element Method) 

## Note

Calculation of coefficient is described with Mn (290.0547 nm) contained in stainless steel. 

According to the Wavelength Table, the wavelength of Mn (290.0547 nm) is approximated by those of W (290.0807 nm), Mo (290.0795 nm), Nb (290.0675 nm) and Cr (290.0265 nm). 

Within a range of a group of analyzed samples, the concentration of Cr is important and the Mn measurement may be affected. A matrix element correction must be calculated. 

## 7. REGRESSION CALCULATION

On the Master Menu screen, select the <Regression calculation> mode with the key ↑ or ↓ and press the ENTER key. The Regression Calculation Sub-menu screen is displayed. After selecting a target item by using the ↑ and ↓, pressing the ENTER key takes you to the selected screen. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/dffccda9e50449e861d7db255ac7d3210251ef2dd079062f283a96f6076c65e7.jpg)



FIGURE 7.1: Coefficient Calculation Sub-menu Screen


## 1. Working curve making

Creates a working curve and calculates working curve coefficients (a, b, c, d). 

## 2. Matrix coefficient

Calculates matrix element correction coefficients. 

TYPE 1: Calculates matrix element correction coefficients by the two-element method. 

TYPE 2: Calculates matrix element correction coefficients by the multi-element method. 

## 3. Information

Registers standard samples. 

Chemical content: Register chemical content for standard samples. 

Sample entry : Register the sample names registered in the item "Chemical content" for each analytical group (Ag-No.). 

(Note 1) This instruction manual describes in the following order: 

1. Information 

2. Working curve making 

3. Matrix coefficient 

(Note 2) Selection of "Chemical content" and "Sample entry" of the <Information> mode: 

Using ↑ or ↓, move the cursor to the <Information> mode and press 

the ENTER key. The cursor moves to the item "Chemical content". 

Using ↑ or ↓ , select "Chemical content" or "Sample entry" and press 

the ENTRY key. It is changed to the selected mode. 

(Note 3) Selection of "TYPE 1" and "TYPE 2" of the <Matrix coefficient> mode: 

Using $\uparrow$ or $\downarrow$ , move the cursor to the <Matrix coefficient> mode and press the ENTER key. The cursor moves to the item "TYPE 1". Using $\leftarrow$ or $\rightarrow$ , select "TYPE 1" or "TYPE 2" and press the ENTER key. It is changed to the selected mode. 

## 7.1 Registration of Chemical Analytical Value

On the Coefficient Calculation Sub-menu screen, select the item "Chemical content" of the <Information> mode and press the ENTER key. The Chemical Analytical Value Registration screen is displayed. In this table, for each standard samples you can enter names and chemical content values of up to 1,000 standard samples. 

Each displayed screen contents 8 standard samples. (If some standard samples have been registered, the last registered table is displayed). 

<table><tr><td colspan="6">Chemical Content Table</td><td colspan="3">Date 04-01-93 Time 18:02</td></tr><tr><td></td><td></td><td></td><td colspan="3">ST05-2</td><td></td><td></td><td></td></tr><tr><td>ELE.</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td></tr><tr><td>FE1</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td></tr><tr><td>FE2</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td></tr><tr><td>C</td><td>.00270</td><td>.09900</td><td>.14500</td><td>.19000</td><td>.24000</td><td>.36000</td><td>.51000</td><td>.66000</td></tr><tr><td>SI</td><td>.00400</td><td>.59000</td><td>.41000</td><td>.08200</td><td>.26000</td><td>.35000</td><td>.32000</td><td>.16000</td></tr><tr><td>MN</td><td>.02000</td><td>.17000</td><td>.75000</td><td>1.9700</td><td>1.6100</td><td>1.3000</td><td>1.0400</td><td>.54000</td></tr><tr><td>P</td><td>.00360</td><td>.00400</td><td>.00800</td><td>.01500</td><td>.00000</td><td>.00170</td><td>.02600</td><td>.02000</td></tr><tr><td>S</td><td>.00200</td><td>.00000</td><td>.00000</td><td>.00800</td><td>.01500</td><td>.04300</td><td>.04000</td><td>.02800</td></tr><tr><td>CU</td><td>.00100</td><td>.40000</td><td>.03100</td><td>.00000</td><td>.30000</td><td>.05300</td><td>.10000</td><td>.16000</td></tr><tr><td>NI1</td><td>.00200</td><td>.07000</td><td>.66000</td><td>.11000</td><td>.38000</td><td>.48000</td><td>.19000</td><td>.29000</td></tr><tr><td>NI2</td><td>.00700</td><td>.05000</td><td>.10000</td><td>.48000</td><td>.91000</td><td>1.4700</td><td>2.0300</td><td>2.4800</td></tr><tr><td>CR</td><td>.00500</td><td>3.9000</td><td>3.2600</td><td>2.5400</td><td>2.0500</td><td>1.5200</td><td>1.0500</td><td>.52000</td></tr><tr><td>MO</td><td>.00100</td><td>.09100</td><td>.06500</td><td>.02100</td><td>.04800</td><td>.01600</td><td>.00000</td><td>.00000</td></tr><tr><td>MG</td><td>.00200</td><td>.00000</td><td>.01800</td><td>.09000</td><td>.05300</td><td>.02700</td><td>.04500</td><td>.07900</td></tr><tr><td>TI</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td></tr><tr><td>SN</td><td>.00100</td><td>.06500</td><td>.04400</td><td>.02200</td><td>.01100</td><td>.00000</td><td>.00000</td><td>.00000</td></tr><tr><td>NB</td><td>.00100</td><td>.49000</td><td>.40000</td><td>.30000</td><td>.09900</td><td>.19000</td><td>.60000</td><td>.98000</td></tr><tr><td>B</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td></tr><tr><td>PB</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td></tr><tr><td>CO</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td><td>.00000</td></tr></table>


FIGURE 7.2 Input Example of Chemical Analytical Value Registration


Sample Name: Displays the sample name where the cursor is located. (Can be entered within 10 characters) 

ELE : Displays an integrator element name. 

No. : Registration number (1 ~ 1000) 

## Example of Function Keys

F 5 (Help) : Displays the Help screen. When you want to erase the Help screen, press the ESC key. 

F 8 (Index) : Displays the Index window for registered sample names. When you want to erase the Index window, press the ESC key. 

F 9 (Init) : Returns to the Analytical mode. 

F10 (Sub-menu) : Returns to the Coefficient Calculation Sub-menu screen. 

SHIFT + Fl (Menu) : Displays the Master Menu screen. 

## Cursor Move on the Registration Screen

The cursor is vertically moved with the keys $\uparrow$ , $\downarrow$ and ENTER by one position. (However, when the cursor has moved to the last one of registered element names, it returns to the first one). 

The cursor is horizontally moved with the keys +, + and TAB keys by one sample. (However, when the cursor is located at the right (or left) end of the screen, it moves to the next screen). 

## <Operating Method>

1. Select <Information> then <Chemical content>, the last group of registered samples is displayed. 

2. Enter a sample name within 10 characters and press the ENTER key. The cursor moves to a chemical analytical value entry area. 

3. For each element, enter a chemical analytical value. 

4. After entering all contents, move the cursor to the sample name with the key ↑. 

5. Using the TAB key, move the cursor to the next sample name entry item and take the Steps 2 through 4. 

6. When you want to alter the sample name and content, move the cursor to the sample name to be altered, using the TAB key. 

(Note 1) Register sample names continuously. 

(Note 2) A sample name cannot be used several time. 

(Note 3) For each sample Number, a file containing sample name, chemical analytical value and measured intensity is created. 

When calculating coefficients, the chemical analytical value and intensity can be called with the sample name as a code. Do not change a relationship between the sample Number and sample name halfway through. 

On the chemical analytical value registration screen, the Index Table Screen is displayed by pressing F8 (Index). 60 registered sample names are displayed on the screen as follows: 

<table><tr><td colspan="8">Chemical content table Date 09-09-91 Time 19:05</td></tr><tr><td>ELE</td><td>1</td><td>2</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>FE1</td><td>.00000</td><td>.00000</td><td colspan="5">INDEX TABLE&gt;</td></tr><tr><td>FE2</td><td>.00000</td><td>.00000</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>NAME</td></tr><tr><td>C</td><td>.00000</td><td>.00000</td><td>1</td><td>FXS-MN-1</td><td>21</td><td>SS468-S</td><td></td></tr><tr><td>SI</td><td>.00000</td><td>.00000</td><td>2</td><td>FXS-MN-2</td><td>22</td><td>SS61-S</td><td></td></tr><tr><td>MN</td><td>.20045</td><td>.49256</td><td>3</td><td>FXS-MN-3</td><td>23</td><td>SS62-S</td><td></td></tr><tr><td>P</td><td>.00000</td><td>.00000</td><td>4</td><td>FXS-MN-4</td><td>24</td><td>SS63-S</td><td></td></tr><tr><td>S</td><td>.00000</td><td>.00000</td><td>5</td><td>STO1-1-S</td><td>25</td><td>SS64-S</td><td></td></tr><tr><td>CU</td><td>.00000</td><td>.00000</td><td>6</td><td>ST21-1-S</td><td>26</td><td>SS65-S</td><td></td></tr><tr><td>NI1</td><td>.00000</td><td>.00000</td><td>7</td><td>ST22-1-S</td><td>27</td><td>SS66-S</td><td></td></tr><tr><td>NI2</td><td>.00000</td><td>.00000</td><td>8</td><td>ST23-1-S</td><td>28</td><td>SS67-S</td><td></td></tr><tr><td>CR</td><td>.00000</td><td>.00000</td><td>9</td><td>ST24-1-S</td><td>29</td><td>SS68-S</td><td></td></tr><tr><td>MO</td><td>.00000</td><td>.00000</td><td>10</td><td>ST25-1-S</td><td>30</td><td>STO1-1</td><td></td></tr><tr><td>MG</td><td>.00000</td><td>.00000</td><td>11</td><td>ST26-1-S</td><td>31</td><td>STO2-1</td><td></td></tr><tr><td>TI</td><td>.00000</td><td>.00000</td><td>12</td><td>ST27-1-S</td><td>32</td><td>STO3-1</td><td></td></tr><tr><td>V</td><td>.00000</td><td>.00000</td><td>13</td><td>ST28-1-S</td><td>33</td><td>STO4-1</td><td></td></tr><tr><td>SN</td><td>.00000</td><td>.00000</td><td>14</td><td>SS461-S</td><td>34</td><td>STO5-1</td><td></td></tr><tr><td>AL</td><td>.00000</td><td>.00000</td><td>15</td><td>SS46S-S</td><td>35</td><td>STO6-1</td><td></td></tr><tr><td></td><td>.00000</td><td>.00000</td><td>16</td><td>SS463-S</td><td>36</td><td>STO7-1</td><td></td></tr><tr><td></td><td>.00000</td><td>.00000</td><td>17</td><td>SS464-S</td><td>37</td><td>STO8-1</td><td></td></tr><tr><td></td><td></td><td></td><td>18</td><td>SS46S-S</td><td>38</td><td>STO9-1</td><td></td></tr><tr><td></td><td></td><td></td><td>19</td><td>SS466-S</td><td>39</td><td>ST10-1</td><td></td></tr><tr><td></td><td></td><td></td><td>20</td><td>SS467-S</td><td></td><td></td><td></td></tr></table>


FIGURE 7.3: Input Example of Index Table Screen


## <Operation Method>

1. A screen display for 60 preceding/following standard sample names can be changed by using the PgUp and PgDn keys. 

2. With the HOME and END keys, the first and last sample table names of registered samples are displayed. 

3. To display the chemical analytical values of a registered sample, move the cursor to that sample and press the Enter or F8 (Index) key. The Index Window screen disappears and the cursor moves to the specified sample name. 

## 7.2 Registration of Standard Sample

On the Coefficient Calculation Sub-menu screen, select the item "Sample entry" of the <Information> mode and press the ENTRY key. The Standard Sample Registration screen is displayed. In this table, you can register or alter 100 standard samples per analytical group (AG-No.). 

<table><tr><td colspan="6">Regression Calculation Sample NameAG-No.=Lowalloy</td><td colspan="3">Date 04-01-93 Time 18:03</td></tr><tr><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td></tr><tr><td>1</td><td></td><td>21</td><td></td><td>41</td><td></td><td>61</td><td></td><td>81</td></tr><tr><td>2</td><td></td><td>22</td><td></td><td>42</td><td></td><td>62</td><td></td><td>82</td></tr><tr><td>3</td><td></td><td>23</td><td></td><td>43</td><td></td><td>63</td><td></td><td>83</td></tr><tr><td>4</td><td></td><td>24</td><td></td><td>44</td><td></td><td>64</td><td></td><td>84</td></tr><tr><td>5</td><td></td><td>25</td><td></td><td>45</td><td></td><td>65</td><td></td><td>85</td></tr><tr><td>6</td><td></td><td>26</td><td></td><td>46</td><td></td><td>66</td><td></td><td>86</td></tr><tr><td>7</td><td></td><td>27</td><td></td><td>47</td><td></td><td>67</td><td></td><td>87</td></tr><tr><td>8</td><td></td><td>28</td><td></td><td>48</td><td></td><td>68</td><td></td><td>88</td></tr><tr><td>9</td><td></td><td>29</td><td></td><td>49</td><td></td><td>69</td><td></td><td>89</td></tr><tr><td>10</td><td></td><td>30</td><td></td><td>50</td><td></td><td>70</td><td></td><td>90</td></tr><tr><td>11</td><td></td><td>31</td><td></td><td>51</td><td></td><td>71</td><td></td><td>91</td></tr><tr><td>12</td><td></td><td>32</td><td></td><td>52</td><td></td><td>72</td><td></td><td>92</td></tr><tr><td>13</td><td></td><td>33</td><td></td><td>53</td><td></td><td>73</td><td></td><td>93</td></tr><tr><td>14</td><td></td><td>34</td><td></td><td>54</td><td></td><td>74</td><td></td><td>94</td></tr><tr><td>15</td><td></td><td>35</td><td></td><td>55</td><td></td><td>75</td><td></td><td>95</td></tr><tr><td>16</td><td></td><td>36</td><td></td><td>56</td><td></td><td>76</td><td></td><td>96</td></tr><tr><td>17</td><td></td><td>37</td><td></td><td>57</td><td></td><td>77</td><td></td><td>97</td></tr><tr><td>18</td><td></td><td>38</td><td></td><td>58</td><td></td><td>78</td><td></td><td>98</td></tr><tr><td>19</td><td></td><td>39</td><td></td><td>59</td><td></td><td>79</td><td></td><td>99</td></tr><tr><td>20</td><td></td><td>40</td><td></td><td>60</td><td></td><td>80</td><td></td><td>100</td></tr><tr><td colspan="9">1:Menu 3:Delete</td></tr><tr><td colspan="7">1:Analys 5:Help</td><td colspan="2">8:Table 9:Init 10:Submenu</td></tr></table>


FIGURE 7.4: Standard Sample Registration Initial Screen


AG-NO: Enter an analytical group name. 

NAME : Enter the sample name registered in the Chemical Analytical Value Registration Table. 

## Explanation of Function Keys

F 1 (Analys) : Returns to the Analysis mode. 

F 4 (Print) : Copies the screen. 

F 3 (Series) : Used when collectively moving a group of samples on the Sample-Name Selection screen. 

F 5 (Help) : Displays the Help screen. When you want to erase the Help screen, press the ESC key. 

F 6 (AG select) : Displays the Analytical Group (AG-No.) Selection screen. 

F 8 (Table) : Displays the Standard Sample Name Selection screen. 

F 9 (Init) : Returns to the Analysis Mode screen. 

F10 (Sub-menu) : Returns to the Coefficient Calculation Sub-menu screen. 

SHIFT + Fl (Menu) : Displays the Master Menu screen. 

SHIFT + F3 (Delete): Deletes the sample names on the screen. (A sample group after a cursor-indicated sample name is deleted). 

<Operating Method> 

1) Entering an analytical group name in the entry item AG-No. 

There are two ways for entering AG-No.: 

a. Enter Ag-No. and press the ENTER key. 

b. Press F6 (AG select) key to display the Ag-No. Selection screen. If you select Ag-No. with ↑ or ↓ and press the ENTER key, the Standard Sample Registration screen for the specified AG-No. will be displayed. 

<table><tr><td colspan="6">Regression Calculation Sample NameAG-No.=Lowalloy</td><td colspan="3">Date 04-01-93 Time 18:07</td></tr><tr><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>NAME</td></tr><tr><td>1</td><td>ST01-2</td><td>21</td><td></td><td>41</td><td></td><td>61</td><td></td><td>81</td></tr><tr><td>2</td><td>ST02-2</td><td>22</td><td></td><td>42</td><td></td><td>62</td><td></td><td>82</td></tr><tr><td>3</td><td>ST03-2</td><td>23</td><td></td><td>43</td><td></td><td>63</td><td></td><td>83</td></tr><tr><td>4</td><td>ST04-2</td><td>24</td><td></td><td>44</td><td></td><td>64</td><td></td><td>84</td></tr><tr><td>5</td><td>ST05-2</td><td>25</td><td></td><td>45</td><td></td><td>65</td><td></td><td>85</td></tr><tr><td>6</td><td>ST06-2</td><td>26</td><td></td><td>46</td><td></td><td>66</td><td></td><td>86</td></tr><tr><td>7</td><td>ST07-2</td><td>27</td><td></td><td>47</td><td></td><td>67</td><td></td><td>87</td></tr><tr><td>8</td><td>ST08-2</td><td>28</td><td></td><td>48</td><td></td><td>68</td><td></td><td>88</td></tr><tr><td>9</td><td>ST09-2</td><td>29</td><td></td><td>49</td><td></td><td>69</td><td></td><td>89</td></tr><tr><td>10</td><td>ST10-2</td><td>30</td><td></td><td>50</td><td></td><td>70</td><td></td><td>90</td></tr><tr><td>11</td><td></td><td>31</td><td></td><td>51</td><td></td><td>71</td><td></td><td>91</td></tr><tr><td>12</td><td></td><td>32</td><td></td><td>52</td><td></td><td>72</td><td></td><td>92</td></tr><tr><td>13</td><td></td><td>33</td><td></td><td>53</td><td></td><td>73</td><td></td><td>93</td></tr><tr><td>14</td><td></td><td>34</td><td></td><td>54</td><td></td><td>74</td><td></td><td>94</td></tr><tr><td>15</td><td></td><td>35</td><td></td><td>55</td><td></td><td>75</td><td></td><td>95</td></tr><tr><td>16</td><td></td><td>36</td><td></td><td>56</td><td></td><td>76</td><td></td><td>96</td></tr><tr><td>17</td><td></td><td>37</td><td></td><td>57</td><td></td><td>77</td><td></td><td>97</td></tr><tr><td>18</td><td></td><td>38</td><td></td><td>58</td><td></td><td>78</td><td></td><td>98</td></tr><tr><td>19</td><td></td><td>39</td><td></td><td>59</td><td></td><td>79</td><td></td><td>99</td></tr><tr><td>20</td><td></td><td>40</td><td></td><td>60</td><td></td><td>80</td><td></td><td>100</td></tr><tr><td colspan="9">1:Menu 3:Delete</td></tr><tr><td colspan="9">1:Analys 5:Help 8:Table 9:Init 10:Submenu</td></tr></table>

## FIGURE 7.5: Input Example of Ag-No. Selection Screen

2) When the AG-No. is entered, the standard sample names registered in that Ag-No. are displayed and the system waits for a standard sample name to be entered at the entry item next to the last registered sample. (The cursor can moved only within a frame currently entered). 

<table><tr><td colspan="6">Sample for regression calculationAG-No. = SUS 1</td><td colspan="4">Date 09-10-91 Time 09:12</td></tr><tr><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td></tr><tr><td>1</td><td>FXS-MN-1</td><td>21</td><td>SS468-S</td><td>41</td><td></td><td>61</td><td></td><td>81</td><td></td></tr><tr><td>2</td><td>FXS-MN-2</td><td>22</td><td></td><td>42</td><td></td><td>62</td><td></td><td>82</td><td></td></tr><tr><td>3</td><td>FXS-MN-3</td><td>23</td><td></td><td>43</td><td></td><td>63</td><td></td><td>83</td><td></td></tr><tr><td>4</td><td>FXS-MN-4</td><td>24</td><td></td><td>44</td><td></td><td>64</td><td></td><td>84</td><td></td></tr><tr><td>5</td><td>STO1-1-S</td><td>25</td><td></td><td>45</td><td></td><td>65</td><td></td><td>85</td><td></td></tr><tr><td>6</td><td>ST21-1-S</td><td>26</td><td></td><td>46</td><td></td><td>66</td><td></td><td>86</td><td></td></tr><tr><td>7</td><td>ST22-1-S</td><td>27</td><td></td><td>47</td><td></td><td>67</td><td></td><td>87</td><td></td></tr><tr><td>8</td><td>ST23-1-S</td><td>28</td><td></td><td>48</td><td></td><td>68</td><td></td><td>88</td><td></td></tr><tr><td>9</td><td>ST24-1-S</td><td>29</td><td></td><td>49</td><td></td><td>69</td><td></td><td>89</td><td></td></tr><tr><td>10</td><td>ST25-1-S</td><td>30</td><td></td><td>50</td><td></td><td>70</td><td></td><td>90</td><td></td></tr><tr><td>11</td><td>ST26-1-S</td><td>31</td><td></td><td>51</td><td></td><td>71</td><td></td><td>91</td><td></td></tr><tr><td>12</td><td>ST27-1-S</td><td>32</td><td></td><td>52</td><td></td><td>72</td><td></td><td>92</td><td></td></tr><tr><td>13</td><td>ST28-1-S</td><td>33</td><td></td><td>53</td><td></td><td>73</td><td></td><td>93</td><td></td></tr><tr><td>14</td><td>SS461-S</td><td>34</td><td></td><td>54</td><td></td><td>74</td><td></td><td>94</td><td></td></tr><tr><td>15</td><td>SS462-S</td><td>35</td><td></td><td>55</td><td></td><td>75</td><td></td><td>95</td><td></td></tr><tr><td>16</td><td>SS463-S</td><td>36</td><td></td><td>56</td><td></td><td>76</td><td></td><td>96</td><td></td></tr><tr><td>17</td><td>SS464-S</td><td>37</td><td></td><td>57</td><td></td><td>77</td><td></td><td>97</td><td></td></tr><tr><td>18</td><td>SS465-S</td><td>38</td><td></td><td>57</td><td></td><td>78</td><td></td><td>98</td><td></td></tr><tr><td>19</td><td>SS466-S</td><td>39</td><td></td><td>59</td><td></td><td>79</td><td></td><td>99</td><td></td></tr><tr><td>20</td><td>SS467-S</td><td>40</td><td></td><td>60</td><td></td><td>80</td><td></td><td>100</td><td></td></tr><tr><td colspan="10">1:Menu 3:Delete1:Analys 4:Print 5:Help 8:Table 9:Init 10:Submenu</td></tr></table>


FIGURE 7.6: Input Example of Standard Sample Registration Screen


3) To register or alter a standard sample name, there are three ways available: 

a. Using the keys TAB, ↑, and ↓, move the cursor to the point where you want to register or alter, enter a standard sample name and press the ENTER key. 

b. Using the keys ↑, ↓, and TAB, move the cursor to the point where you want to register or alter, and press the F8 (Table) key. The <SAMPLE NAME TABLE> Window screen is displayed. (At this time, a cursor color is changed from blue to green). Set the cursor to the sample you want to register using the keys ↑, ↓, PgUp and PgDn and press the Enter key. A background color for that sample this turned into red. 

By pressing the F8 (Table) key, move the sample, whose background color is red, to the cursor (green) on the Standard Sample Registration screen. 

c. When collectively registering a group of multiple samples, move the cursor to the entry item next to the last registered sample and press the F8 (Table) key. 

The <SAMPLE NAME TABLE> Window screen is displayed. Move the cursor to the top of the sample group you want to register and press the F3 (Series) key. The cursor color is turned into red. 

Using the $\downarrow$ key, move the cursor to the end of the sample group you want to select and press the ENTER key. The background of all the sample groups specified are turned to red. (If you move the cursor to an already red-colored sample with $\uparrow$ or $\downarrow$ and press the F3 (Series) key, it will be returned to blue). 

Pressing F8 (Table) moves a group of samples, whose background color is red to the Registration screen. 

<table><tr><td colspan="8">Sample for regression calculation Date 09-10-91 Time 09:12AG-No. = SUS 1</td></tr><tr><td></td><td></td><td></td><td></td><td colspan="4">----&lt;SAMPLE NAME TABLE&gt;----</td></tr><tr><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td></tr><tr><td>1</td><td>FXS-MN-1</td><td>21</td><td>SS468-S</td><td>1</td><td>FXS-MN-1</td><td>21</td><td>SS468-</td></tr><tr><td>2</td><td>FXS-MN-2</td><td>22</td><td>SS61-S</td><td>2</td><td>FXS-MN-2</td><td>22</td><td>SS61-S</td></tr><tr><td>3</td><td>FXS-MN-3</td><td>23</td><td>SS62-S</td><td>3</td><td>FXS-MN-3</td><td>23</td><td>SS62-S</td></tr><tr><td>4</td><td>FXS-MN-4</td><td>24</td><td>SS63-S</td><td>4</td><td>FXS-MN-4</td><td>24</td><td>SS63-S</td></tr><tr><td>5</td><td>STO1-1-S</td><td>25</td><td>SS64-S</td><td>5</td><td>STO1-1-S</td><td>25</td><td>SS64-S</td></tr><tr><td>6</td><td>ST21-1-S</td><td>26</td><td>SS65-S</td><td>6</td><td>ST21-1-S</td><td>26</td><td>SS65-S</td></tr><tr><td>7</td><td>ST22-1-S</td><td>27</td><td>SS66-S</td><td>7</td><td>ST22-1-S</td><td>27</td><td>SS66-S</td></tr><tr><td>8</td><td>ST23-1-S</td><td>28</td><td>SS67-S</td><td>8</td><td>ST23-1-S</td><td>28</td><td>SS67-S</td></tr><tr><td>9</td><td>ST24-1-S</td><td>29</td><td>SS68-S</td><td>9</td><td>ST24-1-S</td><td>29</td><td>SS68-S</td></tr><tr><td>10</td><td>ST25-1-S</td><td>30</td><td></td><td>10</td><td>ST25-1-S</td><td>30</td><td>STO1-</td></tr><tr><td>11</td><td>ST26-1-S</td><td>31</td><td></td><td>11</td><td>ST26-1-S</td><td>31</td><td>STO2-1</td></tr><tr><td>12</td><td>ST27-1-S</td><td>32</td><td></td><td>12</td><td>ST27-1-S</td><td>32</td><td>STO3-1</td></tr><tr><td>13</td><td>ST28-1-S</td><td>33</td><td></td><td>13</td><td>ST28-1-S</td><td>33</td><td>STO4-1</td></tr><tr><td>14</td><td>SS461-S</td><td>34</td><td></td><td>14</td><td>SS461-S</td><td>34</td><td>STO5-1</td></tr><tr><td>15</td><td>SS462-S</td><td>35</td><td></td><td>15</td><td>SS462-S</td><td>35</td><td>STO6-1</td></tr><tr><td>16</td><td>SS463-S</td><td>36</td><td></td><td>16</td><td>SS463-S</td><td>36</td><td>STO7-1</td></tr><tr><td>17</td><td>SS464-S</td><td>37</td><td></td><td>17</td><td>SS464-S</td><td>37</td><td>STO8-1</td></tr><tr><td>18</td><td>SS465-S</td><td>38</td><td></td><td>18</td><td>SS465-S</td><td>38</td><td>STO9-1</td></tr><tr><td>19</td><td>SS466-S</td><td>39</td><td></td><td>19</td><td>SS466-S</td><td>39</td><td>ST10-1</td></tr><tr><td>20</td><td>SS467-S</td><td>40</td><td></td><td>20</td><td>SS467-S</td><td></td><td></td></tr></table>


FIGURE 7.7: Display Example of Sample Name Table Window


4. Deleting the Standard Sample Name 

When deleting an already registered sample, move the cursor to the top sample name to be deleted and press the SHIFT + F3 (Delete) keys. This deletes all sample names subsequent to the specified sample. 

5. Measuring the Post-correction Intensity of the Working Curve Standard Sample 

After registering the standard sample in the analytical group, press the Fl (Analys) key. It returns to the last selected Analysis mode. 

## 7.3 Calculation of Working Curve Coefficient

On the Regression Calculation Sub-menu screen, select the <Working curve making> mode with the key ↑ or ↓. The Working Curve Making screen is displayed. 

This screen draws the working curve of each element per analytical group in linear, quadratic and cubic equations, and displays working curve coefficients a, b, c, and d and standard deviation S.D. Select and register an optimum working curve for each element. 

$I_{DC}$ : Post-correction intensity value C: Content 

$$
C = a I _ {D C} ^ {3} + b I _ {D C} ^ {2} + c I _ {D C} + d
$$

AG-No. entered last in the analytical processing is displayed as the initial Ag-No., and for elements, those for AR-No. 1 are displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/d8ffd8295e360b17fa236ca7617a9509b52a0d68d18c7c5972835e2ba5fd7db9.jpg)



FIGURE 7.8: Display Example of Working Curve Making Initial Screen


AG-No.: Analytical group name 

INTE : Post-correction intensity (graph displayed with exponent) 

CONT : Chemical analytical value or 100% correction content (graph displayed with exponent) 

## Explanation of Function Keys

F 2 (Next) : Displays the element next to currently displayed one. 

F 3 (Pre.) : Displays the element proceeding currently displayed one. 

F 4 (Copy) : Copies the screen. 

F 5 (Help) : Displays the Help screen. When you want to erase the Help screen, press the ESC key. 

F 6 (Elem) : Displays the ELEMENT selection window of a specified analytical group (Ag-No.) When erasing it, press the ESC key. 

F 7 (Reset) : Press this key when altering the analytical group (Ag-No.) 

F 7 (AG sel) : While F7 (Reset) is displayed, pressing F7 switches to the F7 (AG sel) mode and the Analytical Group (AG-No.) Selection screen is displayed. 

F 8 (Data) : Displays the sample name and content of the analytical element currently processed and the intensity data window. When erasing them, press the ESC key. 

F 9 (Init) : Returns to the Analysis Mode screen. 

F10 (Sub-menu) : Returns to the Coefficient Calculation Sub-menu FIGURE 7.1. 

SHIFT + F1 (Menu) : Displays the Master Menu screen. 

SHIFT + F3 (Delete): Deletes the sample names on the screen. (A sample group after a cursor-indicated sample name is deleted). 

(Note) In this mode the ENTER key is used to calculate working curve coefficients and to register them into the Working Curve Coefficients Table. 

## 2. Selecting the Analytical Group (AG-No.)

To select AG-No., press the F7 (Reset) key. The cursor moves to the AG-No. entry item. Enter an AG-No. name and press the ENTER key. Alternatively, press the F7 (AG sel) key to display the Analytical Group Selection screen. Move the cursor to the Ag-No. item to be set with ↑ or ↓ on the Selection screen and press the ENTER key. It is changed to the Working Curve Coefficient Calculation screen for set Ag-No. 

<table><tr><td colspan="6">Sample for regression calculationAG-No. = SUS 1</td><td colspan="4">Date 09-10-91 Time 09:12</td></tr><tr><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td></tr><tr><td>1</td><td>FC 1</td><td>21</td><td>High Mnl</td><td>41</td><td>Tool 1</td><td>61</td><td></td><td>81</td><td></td></tr><tr><td>2</td><td>FC 2</td><td>22</td><td>13Cr Ste</td><td>42</td><td>Tool 2</td><td>62</td><td></td><td>82</td><td></td></tr><tr><td>3</td><td>FCD 1</td><td>23</td><td></td><td>43</td><td></td><td>63</td><td></td><td>83</td><td></td></tr><tr><td>4</td><td>FCD 2</td><td>24</td><td></td><td>44</td><td></td><td>64</td><td></td><td>84</td><td></td></tr><tr><td>5</td><td></td><td>25</td><td></td><td>45</td><td></td><td>65</td><td></td><td>85</td><td></td></tr><tr><td>6</td><td></td><td>26</td><td></td><td>46</td><td></td><td>66</td><td></td><td>86</td><td></td></tr><tr><td>7</td><td></td><td>27</td><td></td><td>47</td><td></td><td>67</td><td></td><td>87</td><td></td></tr><tr><td>8</td><td></td><td>28</td><td></td><td>48</td><td></td><td>68</td><td></td><td>88</td><td></td></tr><tr><td>9</td><td></td><td>29</td><td></td><td>49</td><td></td><td>69</td><td></td><td>89</td><td></td></tr><tr><td>10</td><td></td><td>30</td><td></td><td>50</td><td></td><td>70</td><td></td><td>90</td><td></td></tr><tr><td colspan="2">11 C Steel1</td><td>31</td><td>SUS 1</td><td>51</td><td>Pur Al</td><td>71</td><td></td><td>91</td><td></td></tr><tr><td colspan="2">12 C Steel2</td><td>32</td><td>SUS 2</td><td>52</td><td></td><td>72</td><td></td><td>92</td><td></td></tr><tr><td colspan="2">13 C Steel3</td><td>33</td><td>SUS 3</td><td>53</td><td></td><td>73</td><td></td><td>93</td><td></td></tr><tr><td>14</td><td></td><td>34</td><td></td><td>54</td><td></td><td>74</td><td></td><td>94</td><td></td></tr><tr><td>15</td><td></td><td>35</td><td></td><td>55</td><td></td><td>75</td><td></td><td>95</td><td></td></tr><tr><td>16</td><td></td><td>36</td><td></td><td>56</td><td></td><td>76</td><td></td><td>96</td><td></td></tr><tr><td>17</td><td></td><td>37</td><td></td><td>57</td><td></td><td>77</td><td></td><td>97</td><td></td></tr><tr><td>18</td><td></td><td>38</td><td></td><td>57</td><td></td><td>78</td><td></td><td>98</td><td></td></tr><tr><td>19</td><td></td><td>39</td><td></td><td>59</td><td></td><td>79</td><td></td><td>99</td><td></td></tr><tr><td>20</td><td></td><td>40</td><td></td><td>60</td><td></td><td>80</td><td></td><td>100</td><td></td></tr><tr><td colspan="10">1:Menu Please select AG-No. by using arrow key and press.1:Analys 4:Print 5:Help 8:Table 9:Init 10:Submenu</td></tr></table>


FIGURE 7.9: Display Example of Analytical Group (Ag-No.) Selection Screen


## 3. Selecting the Element Name

An element preceding/following the currently displayed one is displayed by pressing F3 (Pre.) or F2 (Next), respectively. (The order of element names registered in the Analytical Element Registration Table (Section 5.6)). 

Alternatively, the <Element Table> is displayed on the screen by pressing the F6 (Elem) key. Using ↑ and ↓, move the cursor to the element name item to be selected and press the ENTER key. The Working Curve Calculation screen for the specified element names are displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/2ff2ca10b80105e3a4ffe7b43b53504e67db35f7edc64deccf4a2a1b4fb75998.jpg)



FIGURE 7.10: Display Example of Element Name Selection Screen


## 4. Calculating the Working Curve Coefficient

When the Ag-No. and element names are established, data is displayed with a red mark "O", and linear, quadratic and cubic working curves calculated in the method of least squares are displayed. The linear equation is displayed in green, the quadratic equation is displayed in light blue (cyan blue) and the cubic equation is displayed in pink (magenta), respectively. Displayed then, are working curve coefficients a, b, c, d and the standard deviation S.D. 

The maximum intensity of data entered to the axis of ordinates is displayed with an exponent and the maximum content of data entered to the axis of abscissas is also displayed with an exponent. 

$$
S. D. = \sqrt {\frac {\sum R ^ {2}}{n - 1}} \quad R = C i = \widehat {C} i
$$

Ci : Chemical content 

Ci : Analytical result from working curve 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/5437d06cadd77a3b7f458ce7ff96487773b3fe09ed9da79a0bf7f1a50fca5c09.jpg)



FIGURE 7.11: Display Example of Working Curve Coefficient Calculation Screen


## 5. Displaying/Altering the Data Window

On the Working Curve Creating screen, pressing the F8 (Data) key displays the DATA window where minimum content data is displayed. 

The data being displayed in the window is indicated with a yellow " " mark on the graph. Using the key $\uparrow(\downarrow)$ , display the data in the window in a descending (ascending) order of content. 

The FLAG mark and intensity value, which are the data being displayed in the window, are changeable. Move the cursor to the item to be change with $\leftarrow / \rightarrow$ or TAB and change. The characters which can be entered in the item "FLAG" are $\sim$ , --, *, and /. They are classified as shown in the table below: 

<table><tr><td>FLAG Mark</td><td>Working Curve Coefficient Calculation</td><td colspan="2">Matrix Element Correction Coefficient Calculation</td><td>Screen Display</td></tr><tr><td></td><td>Provided</td><td>Provided</td><td>Red &quot;○&quot;</td><td></td></tr><tr><td>--</td><td>Unprovided</td><td>Provided</td><td>Red &quot;x&quot;</td><td></td></tr><tr><td>*</td><td>Unprovided</td><td>Unprovided</td><td>Unprovided</td><td></td></tr><tr><td>/</td><td>Provided</td><td>Unprovided</td><td>Red &quot;○&quot;</td><td></td></tr></table>

(Note 1) The FLAG mark can be entered only in the Working Curve Coefficient Calculation Table. When entering the FLAG mark in the Matrix Element Correction Coefficient Calculation Table, you return the system to this table, enter FLAG in it and obtain the standard deviation and compare it. 

(Note 2) When obtaining the working curve coefficient through the matrix element correction coefficient calculation TYPE 1 (two-element method), enter U for the two-element sample or the sample less affected by matrix elements. For the other samples, enter a -- mark. 

(Note 3) When * or / has been set for an element to be corrected in the matrix element correction coefficient calculation, the chemical content of the correction element of that sample is not included in the matrix element correction coefficient calculation. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/13ae0cc9134c84da7f3b452ec6bebdb9d1403a1f334a5d9eb7eaa50ee2ade521.jpg)


(Note 4) When the intensity value entered is -0.1 (initial value), it is not used for working curve coefficient calculations and matrix element correction coefficient calculations. 

If you press the ENTER key after setting the FLAG mark in the item FLAG, the working curve coefficients and standard deviation will be recalculated and displayed on the screen. Pressing the F8 (Data) or ESC key returns to the Working Curve Coefficient Calculation FIGURE 7.11 

FIGURE 7.12: Data Window Display Example 

No. : Standard sample No. NAME: Standard sample name 

FLAG: FLAG mark 

INTE: Intensity value 

CONT: Chemical analytical value or 100% correction content 

Explanation of Function Keys 

Fl (Look): Displays the Data Table 

## 6. Displaying the Data Table

While the Data window is displayed, pressing the Fl (Look) key displays the Data Tables List. 

Forty (40) working curve creating data are displayed on the screen. Using $\uparrow$ and $\downarrow$ , scroll data to be scrolled. Move the cursor to that data item using the $\leftarrow$ or $\rightarrow$ key and alter the FLAG mark and intensity value. 

After altering, pressing the Fl (Look) or ESC key returns back to the Data Window screen. The working curve coefficient and standard deviation are recalculated and displayed. This table also allows the entering of the FLAG marks "--", "--", "*", and "/" for the item FLAG. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/570c5ca151423e884adda93bcb09f4745be20816d6ec39529d43075a823b440c.jpg)


FIGURE 7.13: R. VAL: Difference between Analytical Value Obtained from Working Curve and Chemical Analytical Value 

7. Selecting and Registering the Working Curve 

On the Working Curve Coefficient Calculation FIGURE 7.11, move the cursor to the Linear, Quadratic or Cubic item with $\uparrow$ or $\downarrow$ to select the working curve and press the ENTER key. 

"F" is displayed after a degree and the coefficients obtained are registered in the Working Curve Coefficient Registration Table. After registration, only a selected working curve is displayed. Copy the screen with the F4 (Copy) key, or obtain the coefficients of the next element with the F2 (Next) or F3 (Pre.) key. 

Since the intensity and chemical analytical values are filed per sample Number, you can also calculate working curve coefficients in other analytical groups (within the same analytical condition group). 

(Note) If working curve coefficients are registered with matrix element correction coefficients registered in the Matrix Element Correction Coefficient Registration Table of the analytical information, the matrix element correction coefficients will be cleared to 0.0. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/98d39391da100e04746b4b6beff84653938093adfcd7fe6c1e90fe3aecebbc6c.jpg)



FIGURE 7.14: Display Example of Working Curve Selection Screen


## 7.4 Matrix Element Correction

## 1) Outline

The emission spectrometry is based on the assumption that the emission of light measured is directly proportional to the mean composition of the sample. In fact, this assumption is not always perfectly correct. Intensity changes of the analytical line can be observed in the presence of one or more "interfering" element in the sample. The origin of these effects may be related to: 

a) Absorption excitation effects as the 

- Change of the inclusion form of the analyzed element in the sample 

- Change of the solidification form (related to the cooling rate of the sample) 

- Change of the melting point due to the presence of a particular element. 

- Change of the thermal conductivity due to a difference of composition. 

b) Analytical spectral line overlapping effect 

Since spectra are very approximate as Cr (290.03 nm) to Mn (290.02 nm), if Cr coexists in the sample, part of Cr is also measured together with Mn and the content of Mn apparently increases. The error caused by measuring part of an approximate spectral line together with a target spectral line is called a spectral line overlapping effect. 

(For approximate spectral line, see the Wavelength Table) 

## 2) Applied correction formulas

Formulas applied to calculate the Correction Coefficients and the Reference Working Curve are: 

Estimate reference value 

$$
C ^ {\prime} = \frac {C _ {i} ^ {\prime} - \Sigma \ell_ {j} C _ {j} ^ {\prime}}{1 + \Sigma d _ {j} C _ {j} ^ {\prime}}\tag{1}
$$

$$
C ^ {\prime} = a I _ {D C} ^ {3} + b I _ {D C} ^ {2} + c I _ {D C} + d\tag{2}
$$

C' : Estimated reference value of element to be corrected 

$C_{i}'$ : Content of element to be corrected 

Cj': Content of matrix element 

$\ell_{j}$ : Overlapping matrix coefficient 

$d_{j}$ : Absorption excitation correction coefficient 

$I_{DC}$ : Measured intensity of element to be corrected 

Formulas applied to calculate the content of an element: 

With the measured intensity ( $I_{x}$ ) applying the reference working curve 

coefficient calculate the uncorrected content $C_{0}$ : 

$$
C _ {0} = a I _ {x} ^ {3} + b I _ {x} ^ {2} + c I _ {x} + d
$$

Then applying the matrix correction coefficient calculate the content C. 

$$
C = C _ {0} (1 + \varepsilon d _ {j} C _ {j}) + \varepsilon l _ {j} C _ {j}\tag{3}
$$

C : Corrected content of quantitative element 

$C_{0}$ : Uncorrected content of quantitative element 

$C_{i}$ : Measured content of matrix element 

$I_{x}$ : Measured intensity of quantitative element 

3) Matrix element correction TYPE 1 (two-element method) 

A reference working curve is calculated using two elements standard 

samples or the less affected standard samples (whose low content). This 

curve is registered as a working curve of this element. Then the 

correction coefficients are calculated using a multiple regression 

calculation. 

(Two-element standard sample: Japan steel Association's FXS series and 

BRAMMER-made IRON BASE BINARY series are available on the market). 

4) Matrix element correction TYPE 2 (multi-element method) 

The reference working curve coefficients (a, b, c and d in the formula 2) 

and correction coefficients ( $\ell_{i}$ and $d_{j}$ in the formula 1) are obtained 

using a multiple regression calculation. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/087e1ff1fe3664215168e1baf45e24997dd27b5a789489abb601e33afb8ced33.jpg)



Multi-element method


![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/8a06b8502f4bc649da09eba9879cd62c9f0b77139ff348a00fc9e227b626b893.jpg)



This program displays the content $C_{i}'$ of an element to be corrected as CONT and the corrected content C of a quantitative element as CAL. CONT and assumes $C_{i}' - C = R$ . VALUE


5) Precautions for calculating the matrix element correction coefficients 

a. When the main component content fluctuates by 5% or more, enter as content (in the Chemical Analytical Value Registration Table) 100% corrected content. 

b. To improve the exactness of correction coefficients, use standard samples, whose chemical analytical values are reliable, and use as many as 10 to 6 times more than the sum (m + k) of the correction coefficients (k) and the degree of the working curve used (m). 

c. The use of the calculated correction coefficients is limited in a range of entered data. In order to analyze an unknown sample, it is necessary to check the validity of the calculated coefficient, therefore a chemical analysis should be performed. 

d. Generally the calculated corrections are good if the calculated coefficient obtain with TYPE 1 and TYPE 2 are similar. (Due to a difference in calculating methods, a standard deviation value for TYPE 2 is smaller). 

e. To check the origin of the working curve, analyze pure iron (or pure copper, aluminum) under the same conditions. Since pure iron (or pure matrix element) is not affected by matrix elements. its analytical result must approach to 0. If it doesn't, review the correction coefficients. 

f. In emission spectrometry, a matrix element correction should not exceed 10% of chemical analytical values. If the correction exceeds 10%, it is recommended to verify and recalculate the coefficient without the higher affected standard samples. 

g. When using a channel skip, set the correction element separately on each side and calculate matrix element correction coefficients. However, when coefficients are identical manually enter in the Matrix Element Correction Coefficient Registration Table. 

h. For a general matrix element correction method, see the Japan Industrial Standards "Emission Spectral Analytical Methods for Gl253 Iron and Steel by Photoelectric Photometry" or USA's "ASTM E-158". 

i. To prevent any miscalculation, verify on Wavelength Table, on JIS or ASTM if the calculated effects is justified. A blind calculation may apparently improve your curve but the analysis of an unknown sample may be not accurate. 

7.5 Matrix Element Correction Coefficient Calculation Type 1
(Two-Element Method)

In working curve coefficient calculation, enter ~ in the item FLAG of the two-element standard samples or the less affected standard samples by matrix elements. and "-" for the other samples. With the sample for which - has been entered, obtain the reference working curve. Enter ~ at least for two samples or the calculation will not be possible.

Select <Matrix coefficient> <TYPE 1> on the Coefficient Calculation Sub-menu screen. The Matrix Element Correction Constant Calculation screen is displayed. If this program is selected in an initial state (when the computer is turned on), the Analytical Group (AG-No.) Selection screen will be displayed. Using ↑ or ↓, select an analytical group and press the ENTER key.

If this program is selected from Working Curve Making through the Coefficient Calculation Sub-menu FIGURE 7.1, the FIGURE 7.25 will be displayed. For AG-No. and element to be corrected, those last set upon working curve creation are displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/e696367decbf2037deb7cd0ef2bb93f73b2fea0b16e3913a9f610b076c80c9be.jpg)



FIGURE 7.15: Input Example of Matrix Element Correction Constant Calculation Registration Screen


## Explanation of Function Keys

F 3 (Cal) : Calculates correction coefficients. 

F 5 (Help) : Displays the Help screen. To erase it, press the ESC key. 

F 6 (Elem) : Displays the Analytical Element (AR-No.) Window screen for a selected AG-No. to erase it, press the ESC key. (The Window screen cannot be selected). 

F 7 (AG sel) : Displays the Analytical Group (Ag-No.) Selection screen. The selection of different AG-No may be performed using the cursor and the ENTER key. 

F 7 (Reset) : When the cursor is located at the matrix element entry item, the key F7 has a different meaning. Pressing F7 will reset the matrix element entry and the cursor returns to the corrected element entry. 

F 8 (Data) : Displays the Data screen (sample name, content intensity) for the analytical element where the cursor is located. To erase, press the ESC key. (No entry is allowed to the screen). 

F 9 (Init) : Returns to the Analysis Mode screen. 

F10 (Sub-menu) : Returns to the Regression Calculation Sub-menu screen. 

SHIFT + Fl (Menu) : Displays the Master Menu screen. 

1) Selecting the analytical group (Ag-No.)
Press the F7 (AG sel) key on the Matrix Element Correction Coefficient Calculation Registration FIGURE 7.25. The Ag-No. Selection screen is displayed.
Select Ag-No. with ↑ or ↓ and press ENTER. The Matrix Element Correction screen for the selected Ag-No is displayed with the first analytical element preselected. 

<table><tr><td colspan="6">Working curve makingAG-No. = SUS 1</td><td colspan="4">Date 09-10-91 Time 09:12</td></tr><tr><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td></tr><tr><td>1</td><td>FC 1</td><td>21</td><td>High Mnl</td><td>41</td><td>Tool 1</td><td>61</td><td></td><td>81</td><td></td></tr><tr><td>2</td><td>FC 2</td><td>22</td><td>13Cr Ste</td><td>42</td><td>Tool 2</td><td>62</td><td></td><td>82</td><td></td></tr><tr><td>3</td><td>FCD 1</td><td>23</td><td></td><td>43</td><td></td><td>63</td><td></td><td>83</td><td></td></tr><tr><td>4</td><td>FCD 2</td><td>24</td><td></td><td>44</td><td></td><td>64</td><td></td><td>84</td><td></td></tr><tr><td>5</td><td></td><td>25</td><td></td><td>45</td><td></td><td>65</td><td></td><td>85</td><td></td></tr><tr><td>6</td><td></td><td>26</td><td></td><td>46</td><td></td><td>66</td><td></td><td>86</td><td></td></tr><tr><td>7</td><td></td><td>27</td><td></td><td>47</td><td></td><td>67</td><td></td><td>87</td><td></td></tr><tr><td>8</td><td></td><td>28</td><td></td><td>48</td><td></td><td>68</td><td></td><td>88</td><td></td></tr><tr><td>9</td><td></td><td>29</td><td></td><td>49</td><td></td><td>69</td><td></td><td>89</td><td></td></tr><tr><td>10</td><td></td><td>30</td><td></td><td>50</td><td></td><td>70</td><td></td><td>90</td><td></td></tr><tr><td>11 C Steel1</td><td>31</td><td>SUS 1</td><td>51</td><td>Pur Al</td><td>71</td><td></td><td>91</td><td></td><td></td></tr><tr><td>12 C Steel2</td><td>32</td><td>SUS 2</td><td>52</td><td></td><td>72</td><td></td><td>92</td><td></td><td></td></tr><tr><td>13 C Steel3</td><td>33</td><td>SUS 3</td><td>53</td><td></td><td>73</td><td></td><td>93</td><td></td><td></td></tr><tr><td>14</td><td></td><td>34</td><td></td><td>54</td><td></td><td>74</td><td></td><td>94</td><td></td></tr><tr><td>15</td><td></td><td>35</td><td></td><td>55</td><td></td><td>75</td><td></td><td>95</td><td></td></tr><tr><td>16</td><td></td><td>36</td><td></td><td>56</td><td></td><td>76</td><td></td><td>96</td><td></td></tr><tr><td>17</td><td></td><td>37</td><td></td><td>57</td><td></td><td>77</td><td></td><td>97</td><td></td></tr><tr><td>18</td><td></td><td>38</td><td></td><td>57</td><td></td><td>78</td><td></td><td>98</td><td></td></tr><tr><td>19</td><td></td><td>39</td><td></td><td>59</td><td></td><td>79</td><td></td><td>99</td><td></td></tr><tr><td>20</td><td></td><td>40</td><td></td><td>60</td><td></td><td>80</td><td></td><td>100</td><td></td></tr><tr><td colspan="10">Please select AG-No. by using arrow key and press.</td></tr><tr><td colspan="10">1:Menu 3:Delete</td></tr><tr><td colspan="10">1:Analys 4:Print, 5:Help 8:Table 9:Init 10:Submenu</td></tr></table>


FIGURE 7.16: Display Example of AG-No. Selection Screen


2) Displaying the analytical element (AR-No.)
Press the F6 (Elem) key on the Matrix Element Correction Coefficient Calculation screen. The <Element table> Window screen is displayed. When you want to erase the Window screen, press the ESC key. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/f48d22fac1e9d5e86955a1ac883a99d5ac2c3259eee23eb6d1ffd8c44ee901c7.jpg)



FIGURE 7.17: Display Example of Analytical Element AR-No. Screen


## 3) Displaying the data table

If you press the F8 (Data) key when the cursor is located at the entry item for the element to be corrected or matrix element, the Data Table screen will be displayed. Press the ESC key to erase it. 

<table><tr><td colspan="9">Data table for working curve AG-No. = 31 SUS 1 Date 09-11-91 Time 15:50</td></tr><tr><td colspan="9">&lt; Cr &gt; A.CON = 4 W.GRP = 1</td></tr><tr><td>No.</td><td>NAME</td><td>FLAG</td><td>CONT.</td><td>INTE.</td><td>No.</td><td>NAME</td><td>FLAG</td><td>CONTE. INTE.</td></tr><tr><td>1</td><td>FXS-MN-1</td><td>-</td><td>.00000</td><td>-1.000</td><td>51</td><td></td><td></td><td></td></tr><tr><td>2</td><td>FXS-MN-2</td><td>-</td><td>.00000</td><td>-1.000</td><td>52</td><td></td><td></td><td></td></tr><tr><td>3</td><td>FXS-MN-3</td><td>-</td><td>.00000</td><td>-1.000</td><td>53</td><td></td><td></td><td></td></tr><tr><td>4</td><td>FXS-MN-4</td><td>-</td><td>.00000</td><td>-1.000</td><td>54</td><td></td><td></td><td></td></tr><tr><td>5</td><td>STO1-1-S</td><td></td><td>.01600</td><td>1.6824</td><td>55</td><td></td><td></td><td></td></tr><tr><td>6</td><td>ST21-1-S</td><td></td><td>39.392</td><td>148.70</td><td>56</td><td></td><td></td><td></td></tr><tr><td>7</td><td>ST22-1-S</td><td></td><td>49.870</td><td>186.24</td><td>57</td><td></td><td></td><td></td></tr><tr><td>8</td><td>ST23-1-S</td><td></td><td>35.275</td><td>140.64</td><td>58</td><td></td><td></td><td></td></tr><tr><td>9</td><td>ST24-1-S</td><td></td><td>32.665</td><td>134.68</td><td>59</td><td></td><td></td><td></td></tr><tr><td>10</td><td>ST25-1-S</td><td></td><td>26.492</td><td>113.57</td><td>60</td><td></td><td></td><td></td></tr><tr><td>11</td><td>ST26-1-S</td><td></td><td>26.898</td><td>116.45</td><td>61</td><td></td><td></td><td></td></tr><tr><td>12</td><td>ST27-1-S</td><td></td><td>20.305</td><td>94.415</td><td>62</td><td></td><td></td><td></td></tr><tr><td>13</td><td>ST28-1-S</td><td></td><td>9.0150</td><td>49.428</td><td>63</td><td></td><td></td><td></td></tr><tr><td>14</td><td>SS461-S</td><td></td><td>19.629</td><td>92.103</td><td>64</td><td></td><td></td><td></td></tr><tr><td>15</td><td>SS462-S</td><td></td><td>16.741</td><td>80.944</td><td>65</td><td></td><td></td><td></td></tr><tr><td>16</td><td>22463-S</td><td></td><td>25.902</td><td>112.60</td><td>66</td><td></td><td></td><td></td></tr><tr><td>17</td><td>22464-S</td><td></td><td>49.561</td><td>183.63</td><td>67</td><td></td><td></td><td></td></tr><tr><td>18</td><td>SS465-S</td><td></td><td>25.347</td><td>110.63</td><td>68</td><td></td><td></td><td></td></tr><tr><td>19</td><td>SS466-S</td><td></td><td>25.084</td><td>109.80</td><td>69</td><td></td><td></td><td></td></tr><tr><td>20</td><td>SS467-S</td><td></td><td>25.529</td><td>111.34</td><td>70</td><td></td><td></td><td></td></tr><tr><td colspan="9">1:Menu Please make data for working table by using arrow key and</td></tr></table>

## FIGURE 7.18: Display Example of Data Table Screen

Scroll the display screen, using the key $\uparrow$ or $\downarrow$ . With the HOME (END) key, display the top (end) of the data displayed. 

## <Operating Method>

1. Enter a corrected element name in the corrected element entry item and press the ENTER key. The cursor moves into a matrix element entry area. 

2. When the element to be corrected and matrix element have been registered in the Matrix Element Correction Coefficient Registration Table of Analytical Information, their contents are displayed. 

a) When you want to alter the matrix element, enter a matrix element correction formula type (L or D) and press the ENTER key. The cursor moves to the matrix element entry item. 

Enter a matrix element Number and press the ENTER key. The cursor moves to the next matrix element entry item. Then, operate in the same manner. 

b) When you want to erase the matrix element currently displayed, erase it from its end. 

Enter ~ in the item D/L and press the ENTER key. Then, the data in the matrix element is erased. 

3. When newly registering the element to be corrected: 

Enter the matrix element correction formula type (L or D) and press the ENTER key. 

The cursor moves to the corrected element entry zone. Enter an element Number to be corrected and press the ENTER key. The cursor moves to the next correction element zone. Then, operate in the same manner. 


4. After completing (2) or (3), press the F3 (Cal) key. Matrix coefficients are calculated and (Disp. 1) is displayed.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/4bcb03f9141fcbf625be2ca8753ff8cbcf2eb912672afa4ba52cd1a1825f1940.jpg)



FIGURE 7.19: (Disp.1) Each Mode Selection Screen after Correction Coefficient Calculation


## Explanation of Function Keys

F 2 (File) : Registers the correction constants displayed in Disp. 5 and Disp. 6 into the Matrix Element Correction Coefficient Registration Table of Analytical Information. 

F 4 (Print/Copy) : Copies the screen. 

F 7 (Reset) : Returns to the Matrix Element Correction Coefficient Registration screen. 

F 8 (Data) : Displays in the Window the sample name for the analytical element currently processed. To erase, press the ESC key. 

SHIFT + F3 (Disp. 1): Displays the screen after completing correction coefficient calculation. 

SHIFT + F4 (Disp. 2): Displays the Pre-correction Working Curve FIGURE 7.20. 

SHIFT + F5 (Disp. 3): Displays the Pre-correction Working Curve FIGURE 7.21. 

SHIFT + F6 (Disp. 4): Displays the FIGURE 7.22 with chemical analytical values (or 100% corrected contents) on the axis of abscissas and corrected contents on the axis of ordinates. 

SHIFT + F7 (Disp. 5): Displays the Correction Coefficient Display FIGURE 7.23. 

SHIFT + F8 (Disp. 6): Displays the FIGURE 7.22 with chemical analytical values (or 100% corrected contents), corrected contents and R. VAL. 

The FIGURES 7.17 through 7.24 show display examples of modes for each combination of function keys SHIFT + F3 (Disp. 1) through SHIFT + F8 (Disp. 6). (TYPE 1 and Disp., mode are displayed on the upper part of each screen). When matrix element correction coefficients are determined, press the F2 (File) key on the Disp. 5 or Disp. 6 screen. Matrix Element Correction Coefficient Registration Table of Analytical Information. 

When calculating the matrix element correction coefficients for other elements, press the F7 (Reset) key on the Disp. 1 screen. It is then changed to the Matrix Element Correction Coefficient Calculation Registration FIGURE 7.25. 

(Note 1) When you want to exclude particular samples from matrix element correction coefficient calculation, enter the FLAG mark "*" in the item FLAG in the Working Curve Coefficient Calculation mode (Section 7.3). Perform the matrix element correction coefficient calculation in the same manner again. 

(Note 2) On the Disp. 3 or Disp. 4 screen, pressing the F8 (Data) key displays sample names on the screen. By using the key + (↓), the sample names are displayed in an ascending (descending) order of content. On the graph, they are displayed in green. 

For Disp. 3, pre-correction ones are displayed with ted "X" and "○" marks, and post-correction ones are with a yellow "□" mark. 

(Note 3) In the Disp. 5 or Disp. 6 Screen mode, pressing the F4 (Print/Copy) key prints PRINT Example 7.2. 

(Note 4) The calculation formula displayed on the Matrix Element Correction Coefficient Calculation FIGURE 7.25 is intended for obtaining a corrected content. 

$$
C = C _ {i} \underline {{(1 + \Sigma d _ {j} C _ {j})}} + \underline {{\Sigma \ell_ {j} C _ {j}}}
$$

(Absorption Excitation) (Overlapping Effect Item) 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/539029dab6bc803d9dcd5cf69881b989bd6d3139f8661f6a80ac167140998f87.jpg)



FIGURE 7.20: (Disp. 2) Display Example of Pre-correction Working Curve Screen



This screen displays the working curve obtained with a two-element standard sample.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/42b47600a2a0d23c814813bcef8763646df1ad39adfb91f8b47066d660efc902.jpg)



FIGURE 7.21: (Disp.3) Display Example of Post-correction Working Curve Screen (Reference Working Curve)


On this screen, "O" and "X" indicate pre-correction, and "☐" indicates post-correction. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/915a802470d925070e43334f4520ae3ddc40405a9e45974dbf4276a6997d73a9.jpg)



FIGURE 7.22: (Disp. 4) Display Example of Chemical Analytical Values vs. Post-correction Content Values


This screen is plotted with chemical analytical values on the axis of abscissas and post-correction content values on the axis of ordinates. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/bdf210c39bccda30ff72830da695836e4bd37d65ed02641d43c96c73feb04df5.jpg)



FIGURE 7.23: (Disp. 5) Display Example of Correction Coefficients


This screen displays matrix element correction coefficients matrix element names. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/38bb303ed5b07b8463edc7a34b0d2205f7dfa5baa25206c172c292931efd6e91.jpg)


## FIGURE 7.24: (Disp. 6) Display Example of Corrected Values

NAME : Sample name FLAG: Flag mark 

CONT : Chemical analytical value or 100% corrected content 

INTE : Measured intensity 

CAL. CONT : Corrected content 

R. VALUE : Displays difference between CONT and CAL. CONT. 

S.D. : Displays a standard deviation for R. VALUE. 

If the key ↑ or ↓ is pressed, the screen will scroll to display 

data. Pressing the HOME (END) key displays the top (last) data on the screen. 

$$
S. D. = \sqrt {\frac {\Sigma R ^ {2}}{n - 1}}
$$

<table><tr><td colspan="6">Calculation matrix coefficient Type 1 DAT</td></tr><tr><td colspan="6">&lt; Si : 212.4 / FE1 : 271.4 &gt; AG-No:= 1 LowAlloy</td></tr><tr><td></td><td>1 Cu</td><td>L</td><td>.0167618333</td><td></td><td></td></tr><tr><td></td><td>2 Mo</td><td>L</td><td>-.008048414</td><td></td><td></td></tr><tr><td>a</td><td>b</td><td>c</td><td>d</td><td>S.D</td><td></td></tr><tr><td>.000000000</td><td>.000004784</td><td>.013151460</td><td>-.09194813</td><td>.00563</td><td></td></tr><tr><td>NAME</td><td>FLAG CONT.</td><td>INTE.</td><td>CAL.CONT.</td><td>R.VALUE</td><td></td></tr><tr><td>1 ST01-5*</td><td>.00606</td><td>6.8616</td><td>-.00147</td><td>.007534</td><td></td></tr><tr><td>2 ST02-5*</td><td>.65599</td><td>56.132</td><td>.658503</td><td>-.00252</td><td></td></tr><tr><td>3 ST03-5*</td><td>.47427</td><td>41.909</td><td>.476703</td><td>-.00243</td><td></td></tr><tr><td>4 ST04-5*</td><td>.09382</td><td>14.700</td><td>.102011</td><td>-.00819</td><td></td></tr><tr><td>5 ST05-5*</td><td>.29199</td><td>29.539</td><td>.301026</td><td>-.00904</td><td></td></tr><tr><td>6 ST06-5*</td><td>.43006</td><td>38.178</td><td>.424533</td><td>.005524</td><td></td></tr><tr><td>7 ST07-5*</td><td>.37715</td><td>35.452</td><td>.379041</td><td>-.00189</td><td></td></tr><tr><td>8 ST08-5*</td><td>.22305</td><td>23.900</td><td>.222048</td><td>.001007</td><td></td></tr><tr><td>9 ST09-5*</td><td>.27550</td><td>27.582</td><td>.270007</td><td>.005496</td><td></td></tr><tr><td>10 ST10-5*</td><td>.24050</td><td>25.074</td><td>.241899</td><td>-.00140</td><td></td></tr></table>

PRINT Example 7.1: This is a printout example of correction coefficients and corrected values. 

In the Disp. 5 or Disp. 6 mode, pressing the F4 (Print) key prints corrected coefficients and corrected data to the printer. 

7.6 Matrix Element Correction Coefficient Calculation Type 2 (Multi-Element Method) 

On the Coefficient Calculation Sub-menu screen, select <Matrix Coefficient>
<TYPE 2>. The Matrix Element Correction Coefficient Calculation screen is displayed. 

If this program is selected in an initial state (when the computer is turned on), the Analytical Group (AG-No.) Selection screen will be displayed. Using $\uparrow$ or $\downarrow$ , select an analytical group and press the ENTER key. The screen is displayed. 

If this program is selected from Working Curve Making through the Coefficient Calculation Sub-menu FIGURE 7.1, the FIGURE 7.25 will be displayed. 

For AG-No. and element to be corrected, those last set upon working curve creation are displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/cc9901ff06debd01472d5032130b2c36a8a3599abea4deb28b7f9da6482f3e51.jpg)



FIGURE 7.25: Input Example of Matrix Element Correction Coefficient Calculation Registration Screen


Explanation of Function Keys 

F3 (Cal) : Calculates correction coefficients. 

F5 (Help): Displays the Help screen. To erase, press the ESC key. 

F 6 (Elem) : Displays the Analytical Element (AR-No.) Window screen for the selected. AG-No. To erase it, press the ESC key. (The screen cannot be selected). 

F 7 (AG sel) : Displays the Analytical Group (Ag-No.) Selection screen when the cursor is located at the correction element entry item. 

F 7 (Reset) : If the cursor is located at the correction element entry item, press this key when altering a name of the element to be corrected. 

F 8 (Data) : Displays the Data (sample name, content, and intensity) for the analytical element where the cursor is located. To erase, press the ESC key. (No entry is allowed to screen). 

F 9 (Init) : Returns to the Analytical Mode screen. 

F10 (Sub-menu) : Returns to the Coefficient Calculation Sub-menu FIGURE 7.1. 

SHIFT + Fl (Menu) : Displays the Master Menu screen. 

## 1) Selecting the analytical group (AG-No.)

Press the F7 (AG sel) key on the Matrix Element Correction Coefficient Calculation Registration FIGURE 7.25. The AG-No. Selection screen is displayed. 

Using ↑ or ↓, select AG-No. and press the ENTER key. The Matrix Element Correction Screen for the selected AG-No. is displayed. 

<table><tr><td colspan="6">Working curve makingAG-No. = SUS 1</td><td colspan="4">Date 09-10-91 Time 09:12</td></tr><tr><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td><td>No.</td><td>NAME</td></tr><tr><td>1</td><td>FC 1</td><td>21</td><td>High Mnl</td><td>41</td><td>Tool 1</td><td>61</td><td></td><td>81</td><td></td></tr><tr><td>2</td><td>FC 2</td><td>22</td><td>13Cr Ste</td><td>42</td><td>Tool 2</td><td>62</td><td></td><td>82</td><td></td></tr><tr><td>3</td><td>FCD 1</td><td>23</td><td></td><td>43</td><td></td><td>63</td><td></td><td>83</td><td></td></tr><tr><td>4</td><td>FCD 2</td><td>24</td><td></td><td>44</td><td></td><td>64</td><td></td><td>84</td><td></td></tr><tr><td>5</td><td></td><td>25</td><td></td><td>45</td><td></td><td>65</td><td></td><td>85</td><td></td></tr><tr><td>6</td><td></td><td>26</td><td></td><td>46</td><td></td><td>66</td><td></td><td>86</td><td></td></tr><tr><td>7</td><td></td><td>27</td><td></td><td>47</td><td></td><td>67</td><td></td><td>87</td><td></td></tr><tr><td>8</td><td></td><td>28</td><td></td><td>48</td><td></td><td>68</td><td></td><td>88</td><td></td></tr><tr><td>9</td><td></td><td>29</td><td></td><td>49</td><td></td><td>69</td><td></td><td>89</td><td></td></tr><tr><td>10</td><td></td><td>30</td><td></td><td>50</td><td></td><td>70</td><td></td><td>90</td><td></td></tr><tr><td>11</td><td>C Steel1</td><td>31</td><td>SUS 1</td><td>51</td><td>Pur Al</td><td>71</td><td></td><td>91</td><td></td></tr><tr><td>12</td><td>C Steel2</td><td>32</td><td>SUS 2</td><td>52</td><td></td><td>72</td><td></td><td>92</td><td></td></tr><tr><td>13</td><td>C Steel3</td><td>33</td><td>SUS 3</td><td>53</td><td></td><td>73</td><td></td><td>93</td><td></td></tr><tr><td>14</td><td></td><td>34</td><td></td><td>54</td><td></td><td>74</td><td></td><td>94</td><td></td></tr><tr><td>15</td><td></td><td>35</td><td></td><td>55</td><td></td><td>75</td><td></td><td>95</td><td></td></tr><tr><td>16</td><td></td><td>36</td><td></td><td>56</td><td></td><td>76</td><td></td><td>96</td><td></td></tr><tr><td>17</td><td></td><td>37</td><td></td><td>57</td><td></td><td>77</td><td></td><td>97</td><td></td></tr><tr><td>18</td><td></td><td>38</td><td></td><td>57</td><td></td><td>78</td><td></td><td>98</td><td></td></tr><tr><td>19</td><td></td><td>39</td><td></td><td>59</td><td></td><td>79</td><td></td><td>99</td><td></td></tr><tr><td>20</td><td></td><td>40</td><td></td><td>60</td><td></td><td>80</td><td></td><td>100</td><td></td></tr><tr><td colspan="10">Please select AG-No. by using arrow key and press.</td></tr><tr><td colspan="10">1:Menu 3:Delete1:Analys 4:Print 5:Help 8:Table 9:Init 10:Submenu</td></tr></table>


FIGURE 7.26: Display Example of AG-No. Selection Screen


2) Display the analytical element (AR-No.)
Press the F6 (Elem) key on the Matrix Element Correction Coefficient Calculation Registration screen. The <Element table> Window screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/ad86cf53915d7b1a72104da5147c50502ccc287d3aa29e08f12e933d636adbdf.jpg)



FIGURE 7.27: Display Example of Analytical Element AR-No. Screen


## 3) Display the data table

If you press the F8 (Data) key when the cursor is located at the entry item for the element to be corrected or correction element, the Data Table screen will be displayed. To erase it, press the ESC key. 

<table><tr><td colspan="9">Data table for working curve AG-No. = 31 SUS 1 Date 09-11-91 Time 15:50</td></tr><tr><td colspan="9">&lt; Cr &gt; A.CON = 4 W.GRP = 1</td></tr><tr><td>No.</td><td>NAME</td><td>FLAG</td><td>CONT.</td><td>INTE.</td><td>No.</td><td>NAME</td><td>FLAG</td><td>CONTE. INTE.</td></tr><tr><td>1</td><td>STO1-1-S</td><td>.01600</td><td>1.6824</td><td>5 51</td><td></td><td></td><td></td><td></td></tr><tr><td>2</td><td>ST21-1-S</td><td>39.392</td><td>148.70</td><td>5 52</td><td></td><td></td><td></td><td></td></tr><tr><td>3</td><td>ST22-1-S</td><td>49.870</td><td>186.24</td><td>5 53</td><td></td><td></td><td></td><td></td></tr><tr><td>4</td><td>ST23-1-S</td><td>35.275</td><td>140.64</td><td>5 54</td><td></td><td></td><td></td><td></td></tr><tr><td>5</td><td>ST24-1-S</td><td>32.665</td><td>134.68</td><td>5 55</td><td></td><td></td><td></td><td></td></tr><tr><td>6</td><td>ST25-1-S</td><td>26.492</td><td>113.57</td><td>5 56</td><td></td><td></td><td></td><td></td></tr><tr><td>7</td><td>ST26-1-S</td><td>26.898</td><td>116.45</td><td>5 57</td><td></td><td></td><td></td><td></td></tr><tr><td>8</td><td>ST27-1-S</td><td>20.305</td><td>94.415</td><td>5 58</td><td></td><td></td><td></td><td></td></tr><tr><td>9</td><td>ST28-1-S</td><td>9.0150</td><td>49.428</td><td>5 59</td><td></td><td></td><td></td><td></td></tr><tr><td>10</td><td>SS461-S</td><td>19.629</td><td>92.103</td><td>6 60</td><td></td><td></td><td></td><td></td></tr><tr><td>11</td><td>SS462-S</td><td>16.741</td><td>80.944</td><td>6 61</td><td></td><td></td><td></td><td></td></tr><tr><td>12</td><td>22463-S</td><td>25.902</td><td>112.60</td><td>6 62</td><td></td><td></td><td></td><td></td></tr><tr><td>13</td><td>22464-S</td><td>49.561</td><td>183.63</td><td>6 63</td><td></td><td></td><td></td><td></td></tr><tr><td>14</td><td>SS465-S</td><td>25.347</td><td>110.63</td><td>6 64</td><td></td><td></td><td></td><td></td></tr><tr><td>15</td><td>SS466-S</td><td>25.084</td><td>109.80</td><td>6 65</td><td></td><td></td><td></td><td></td></tr><tr><td>16</td><td>SS467-S</td><td>25.529</td><td>111.34</td><td>6 66</td><td></td><td></td><td></td><td></td></tr><tr><td>17</td><td>SS468-S</td><td>25.718</td><td>111.07</td><td>6 67</td><td></td><td></td><td></td><td></td></tr><tr><td>18</td><td>SS61-S</td><td>19.721</td><td>115.07</td><td>6 68</td><td></td><td></td><td></td><td></td></tr><tr><td>19</td><td>SS62-S</td><td>17.426</td><td>83.146</td><td>6 69</td><td></td><td></td><td></td><td></td></tr><tr><td>20</td><td>SS63-S</td><td>26.604</td><td>114.52</td><td>7 70</td><td></td><td></td><td></td><td></td></tr><tr><td colspan="9">1:Menu Please make data for working table by using arrow key and</td></tr><tr><td colspan="4"></td><td colspan="5">8:Data 9:Init 10:Submenu</td></tr></table>


FIGURE 7.28: Display Example of Data Table Screen


The screen is scrolled by using $\uparrow$ or $\downarrow$ . With the HOME (END) key, display the top (end) of the data displayed. 

## <Operating Method>

1. Enter a name of the element to be corrected in the corrected element entry item and press the ENTER key. The cursor moves into a correction element entry area. 

2. When the element to be corrected and correction elements have been registered in the Matrix Element Correction Coefficient Calculation Registration Table, their contents are displayed. 

a) To alter the correction element, enter a matrix element correction formula type (L or D) and press the ENTER key. The cursor moves to the correction element Number and press the ENTER key. Then the data for the correction element is erased. 

b) To erase the correction element currently displayed, erase it from is end. Enter - in the D/L entry area and press the ENTER key. Then the data for the correction element are erased. 

3. When newly registering the element to be corrected, enter the matrix element correction formula type (L or D) and press ENTER. The cursor moves to the corrected element entry area. 

Enter an element Number, to be corrected and press the ENTER key. The cursor moves to the next correction element entry area. Then operate in the same manner. 

4. After completing (2) or (3), press the F3 (Cal) key. Matrix element correction coefficients are calculated and Disp. 1 is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/0014f390f1f385f6cdba7faaa19769f35b215c107df4d35039189bce3a2208e5.jpg)



FIGURE 7.29: (Disp. 1) Each Mode Selection Screen after Correction Coefficient Calculation


## Explanation of Function Keys

F 2 (File) : Registers the correction coefficients and reference working curve coefficients displayed on the Disp. 5 or Disp. 6 into the Matrix Element Correction Coefficient Calculation Registration Table and Working Curve Coefficient Registration Table of Analytical Information. 

F 4 (Print/Copy) : Copies the screen. 

F 7 (Reset) : Returns to the Matrix Element Correction Coefficient Calculation Registration screen. 

F 8 (Data) : Displays in the window, the sample name for the analytical element currently processed. To erase, press the ESC key. 

SHIFT + F3 (Disp. 1): Displays the screen after completing correction coefficient calculation (FIGURE 7.29). 

SHIFT + F4 (Disp. 2): Displays the Pre-correction Working Curve (FIGURE 7.30). 

SHIFT + F5 (Disp. 3): Displays the Pre-correction Working Curve (FIGURE 7.31). 

SHIFT + F6 (Disp. 4): Displays the screen with chemical analytical values (or 100% corrected contents) on the axis of abscissas and corrected contents on the axis of ordinates (FIGURE 7.32). 

SHIFT + F7 (Disp. 5): Displays the Correction Coefficient Display Screen in FIGURE 7.23. 

SHIFT + F8 (Disp. 6): Displays the screen for chemical analytical values (or 100% corrected contents) corrected contents and their difference. 

The FIGURES 7.29 through 7.34 show displayed examples of modes for each combination of function keys SHIFT + F5 (Disp. 1) through SHIFT + F8 (Disp. 6). (TYPE 2 and Disp. modes are displayed on the upper part of each screen). When matrix element correction coefficients are determined, press the F2 (File) key. The correction coefficients and reference working curve coefficients obtained are registered into the Matrix Element Correction Coefficient Calculation Registration Table and Working Curve Coefficient Registration Table of Analytical Information. 

When calculating the matrix element correction coefficients for other elements, press the F7 (Reset) key on the Disp. 1 screen. It is changed to the Matrix Element Correction Coefficient Calculation Registration Table. 

(Note 1) When you want to exclude particular elements from the matrix element correction coefficient calculation, enter the FLAG mark "*" in the item FLAG in the Working Curve Coefficient Calculation mode (Section 7.3). Perform the matrix element correction coefficient calculation again in the same manner. 

(Note 2) On the Disp. 3 or Disp. 4 screen, pressing the F8 (Data) key displays sample names on the screen. By using the key ↑ (↓), the sample names are displayed in an ascending (descending) order of content. On the graph, they are displayed in green. For Disp. 3, pre-correction names are displayed with red "X" and "O" marks, and post-correction names with a yellow " " mark. 

(Note 3) In the Disp. 5 or Disp. 6 mode, pressing the F4 (Print) key prints PRINT Example 7.1. 

(Note 4) The calculation formula displayed on the Matrix Element Correction Coefficient Calculation FIGURE 7.25 is intended for obtaining a corrected content. 

C = C_i $\frac{(1 + \Sigma d_j C_j)}{D\ Item} + \frac{\Sigma \ell_j C_j}{L\ Item}$ (Absorption (Overlapping Effect Item) Excitation Item) 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/dd9e5dea2808cc1163bb611fd3227b8aeb48c18f858ceb9e1f3ad8778aea865c.jpg)



FIGURE 7.30: (Disp. 2) Display Example of Pre-correction Working Curve Screen



This screen displays the pre-correction working curve obtained out of analytical values and measured intensity through multiple regression calculation.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/63c50149c965e04b4a93be04e76c6224d3f6dd570e5806df4538bc5121074f3a.jpg)



FIGURE 7.31: (Disp. 3) Display Example of Post-correction Working Curve (Reference Working Curve)



On the screen, "O" and "X" indicate pre-correction, and "☐" indicates post-correction.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/2a0a8f00c925f19b4ae8bb246c969d01129de2bb5b48b5e676d020d9d9b12403.jpg)



FIGURE 7.32: (Disp. 4) Display Example of Chemical Analytical Values (100% Corrected Contents) vs. Post-correction Content Values


This screen is plotted with chemical analytical values (or 100% corrected contents) on the axis of abscissas and post-correction content values on the axis of ordinates. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/0416200754c94655afb07ebb9b3049f7eb153f6029f4487f83fbe36cb2d94ed5.jpg)



FIGURE 7.33: (Disp. 5) Display Example of Correction Coefficients


This screen displays matrix element correction coefficients and correction element names. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/aab163c06fa69388fb0feccd8ae09fe843326e7ec47f858d1e6082800db6e377.jpg)


FIGURE 7.34: (Disp. 6) Display Example of Corrected Values 

NAME : Sample name FLAG: Flag mark 

CONT : Chemical analytical value or 100% corrected content 

INTE : Measured intensity 

CAL. CONT : Corrected content (Content corrected with correction coefficients and an uncorrected content value calculated from an obtained reference working curve). 

R. VALUE : Displays a difference between CONT and CAL. CONT 

S.D. : Displays a standard deviation for R. VALUE. 

If the key $\uparrow$ or $\downarrow$ is pressed, the screen will be scrolled to display data. Pressing the HOME (END) key displays the top (last) data on the screen. 

$$
S. D. = \sqrt {\frac {\Sigma R ^ {2}}{n - 1}}
$$

<table><tr><td colspan="6">Calculation matrix coefficient Type 2 DATE 03-26-93</td></tr><tr><td colspan="6">&lt; Si : 212.4 / FE1 : 271.4 &gt; AG-No:= 1 LowAlloy</td></tr><tr><td></td><td>1 Cu</td><td>L</td><td>.0247002587</td><td></td><td></td></tr><tr><td></td><td>2 Mo</td><td>L</td><td>-.004825142</td><td></td><td></td></tr><tr><td>a</td><td>b</td><td>c</td><td>d</td><td>S.D</td><td></td></tr><tr><td>.000000000</td><td>.000012245</td><td>.012545108</td><td>-.08570623</td><td>.00508</td><td></td></tr><tr><td>NAME</td><td>FLAG CONT.</td><td>INTE.</td><td>CAL.CONT.</td><td>R.VALUE</td><td></td></tr><tr><td>1 ST01-5*</td><td>.00606</td><td>6.8616</td><td>.000970</td><td>.005090</td><td></td></tr><tr><td>2 ST02-5*</td><td>.65599</td><td>56.132</td><td>.656761</td><td>-.00078</td><td></td></tr><tr><td>3 ST03-5*</td><td>.47427</td><td>41.909</td><td>.477934</td><td>-.00366</td><td></td></tr><tr><td>4 ST04-5*</td><td>.09382</td><td>14.700</td><td>.103013</td><td>-.00919</td><td></td></tr><tr><td>5 ST05-5*</td><td>.29199</td><td>29.539</td><td>.296730</td><td>-.00474</td><td></td></tr><tr><td>6 ST06-5*</td><td>.43006</td><td>38.178</td><td>.423438</td><td>.006620</td><td></td></tr><tr><td>7 ST07-5*</td><td>.37715</td><td>35.452</td><td>.377073</td><td>.000076</td><td></td></tr><tr><td>8 ST08-5*</td><td>.22305</td><td>23.900</td><td>.224449</td><td>-.00139</td><td></td></tr><tr><td>9 ST09-5*</td><td>.27550</td><td>27.582</td><td>.269505</td><td>.005998</td><td></td></tr><tr><td>10 ST10-5*</td><td>.24050</td><td>25.074</td><td>.238520</td><td>.001981</td><td></td></tr></table>

PRINT EXAMPLE 7.2: This is a printout example of correction coefficients and corrected values. 

In the Disp. 5 or Disp. 6 mode, pressing the F4 (Print) key prints correction coefficients and corrected data to the printer. 

## 8. ANALYTICAL OPERATION CONTENT ANALYSIS

8.1 Basic Operation Method 

8.2 Analytical Procedure 

8.3 Selection of Analytical Job 

8.4 Setting of Operation Mode 0 

8.5 Content Analysis 

8.6 Modification and Cancel Analytical Value 

8.7 Three-times Analysis 

8.8 Master Curve Recalibration Analysis or Type Standard Analysis 

## 8.1 Basic Operation Method

1) Entering the required information 

a. With +, + and ENTER, move the cursor to an entry item. Type the data then press the ENTER key. The contents are entered. 

b. When entering a numerical value do not leave a space between numbers.
When leaving a space, use the - key. 

c. The information required is dependent on the JOB selected. (see section 8.3). 

2) Explanation of Function Keys for Analytical Operation 

Fl (Start) : Starts photometry. 

F2 (Stop) : Stops photometry. 

F3 (Cal) : Calculates values $\alpha$ , $\beta$ , k in Analytical Jobs 2 and 3 and those MC and AC in Analytical Job 4. 

F4 (Print) : Prints analytical results. 

F5 (File) : Files analytical results. (Displayed in the MANUAL mode). 

F6 (Trans) : Transmits analytical results to the host computer. 

F7 (Reset) : Erases from the screen the data halfway into the multiple analysis. 

F8 (-HV) : Turns -HV on/off to the readout unit. (A background color is switched to white when -HV is turned on). 

SHIFT + F1 (Menu) : Displays the Master Menu screen. To erase, press the ESC key. 

SHIFT + F2 (Job) : Displays the Job Menu Selection screen. To erase, press ESC key. 

SHIFT + F3 (Mode O) : Displays Printout/Screen Display Format Entry screen. 0 To erase, press the F9 (Init) key. 

SHIFT + F6 (AG sel) : Displays the Analytical Group Selection screen on the Content Analysis Mode screen. 

(Note 1) When a function key F1 through F10 is pressed the background of the selection is highlighted. 

(Note 2) When the -HV of the readout unit is turned off before or during an analysis, an error message "Measurement Error" is displayed. (When the measured value of the internal standard element AR-No. 1 is 0.02 or less, an automatic check is made on HV status). 

3) Analytical Value Flags 

I) When an analytical value is over the required range, it is indicated by "!!!!!" in red. 

II) The calculation is disabled when the values for 'FIG' and 'DECI', as seen on the 'Printout Format Entry Table' (see section 5.11 pg 77), are incorrect. This is indicated by "******". 

III) When an overflow occurs after an intensity value is converted to content it is indicated by "?????". 

IV) Display and printout when R control or standard checks in content analysis or three-time analysis is out of range, and when R control in the master curve recalibration analysis is out of range. 

a. When variance check (R control) is out of tolerance 

The average value is displayed in red on the screen and a R is printed after the average value on the printer. 

b. When product standard check is out of tolerance (Check the standard against the product standard registration information). 

When beyond the lower-limit standard 

The screen displays L in blue after the average value. L is printed after the average value on the printer. 

When beyond the upper-limit standard 

The screen displays H in blue after the average value. H is printed after the average value on the printer. 

When beyond the trace standard 

The screen displays the average value as "Tr". On the printer, the average value is printed as "Tr". 

(Note) The Tr standard is effective only when beyond the lower-limit standard. 

c. When both variance check and standard check are out of tolerance 

The screen displays the average value in red, followed by H, L. On the printer, R, H and L are printed in that order as "Tr". 

4) Scrolling the Analysis Screen 

During a multiple analysis data may scroll off the screen. To view the data place the cursor at the item AG-NO and press TAB to scroll right or shift-tab to scroll left. 

To display these erased data, press TAB, or SHIFT + TAB. (Effective only when cursor is located at the item Ag-No.). 

5) Number of Emission Times 

TAN: Displays the total number of emission times. 

AN : Displays the number of emission times after waste discharge. 

6) Registering the Product Standard Check Name 

Enter the standard name from the Product Standard Registration Table (Section 5.13) into the entry item ST-No. 

(Note) When the analytical elements displayed on the screen and the registered elements for the product standard do not match each other, unmatched elements are displayed on the lower part of the screen. 

8.2 Analytical Procedures 

This section describes a general pattern of daily analytical procedures. When actually using, prepare a procedural document based on the following: 

1) Setting the Scanning dial (See 11.2) 

Select the <Manual scanning> mode from the <Maintenance> menu. Set a 

scanning sample onto the emission stand and start emission. Calculate the 

peak position and set the scanning dial to the peak position. (This is not 

required to be done daily when temperature inside the spectrometer is 

stable) 

2) Cleaning the Electrode (Waste Discharge) (See 11.1) 

Select the <Waste discharge> mode from the <Maintenance> menu. Set a cleaning sample onto the emission stand and start emission. The burn sequence will be repeated 5 times and the number of analyses AN will be reset to 0 (zero). 

3) Two-Point Recalibration (See 9.4) 

Select the <Two-point recalibration> mode from the <Analysis> menu. Perform the two-point recalibration with the registered calibration sample. 

4) One-Point Recalibration (See 9.5) (not required if two point recalibration 

is being used) 

Select the <One-point recalibration> mode from the <Analysis> menu. 

Perform the one-point recalibration with the registered calibration 

sample. 

5) Master Curve Corrections (See 8.8) (or Type Standard Calibration) 

If the used Analytical group has been set with a master curve correction, 

select the <Master curve recalibration> mode from the <Analysis> menu. 

Perform the master curve correction with a master curve recalibration 

sample. (Note: After one-point or two-point calibration, be sure to 

perform master curve recalibration correction). 

6) Content Analysis (See 8.5 and 8.7) 

Select the <CONT> or <Special 3 times analysis> mode from the <Analysis> menu and perform a content analysis. 

## 8.3 Selection of Analytical Job

If you press SHIFT + F2 (Job) on the Master Menu Screen 4.1, the Analytical Job Selection Menu screen will be displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/459ac42c5a9b4704cfbbaeb7f871ede6f3e4d13703b755af417355a4c17d6906.jpg)



FIGURE 8.1: Analytical Job Selection Menu Screen


Each job is selected by moving the cursor with the $\uparrow$ or $\downarrow$ arrow keys, and pressing ENTER. 

<2, l-point recalibration> One-point recalibration analysis. (See 9.5) Analysis mode to calculate the drift correction coefficient K. 

<3, 2-point recalibration> Two-point calibration analysis. (See 9.4) Analysis mode to calculate the drift correction coefficients $\alpha$ and $\beta$ . 

<4, Master curve recalibration> 

Master curve correction recalibration analysis. 

<5, INT. 1 (Raw intensity)> Pre-correction intensity analysis. (See 9.9) 

Analysis expressed in intensity before drift correction. 

<6, INT. 2 (Drift Corrected Intensity)> Post-correction intensity analysis. (See 9.8) 

Analysis of an intensity value for which pre-correction intensity has been corrected with drift correction coefficients obtained through <l-point or 2-point recalibration> analysis. 

<7, INT. 2 for Working Curve> Intensity analysis for the working curve calculation. (See 9.7) 

Analysis of a post-correction intensity used for calculating working curve coefficients and matrix element correction coefficients. 

<8, INT. 2 for Target> One or two Recalibration reference value analysis. (See 9.6) 

Used to automatically register reference values into the Drift Correction Coefficients Registration Table of Analytical Information. 

<X, CONT> Unknown sample quantitative analysis. 

<Y, Special 3-time analysis> 3-Time content analysis. 

In the Three-time Analysis mode a third analysis is requested when the variance limit is exceeded in the first two measurements. Then, calculates the average value for each element, using data with the minimum variance. However, when the variance limits are exceeded for the three times analysis, a three-time analysis error is recorded. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/dbe3fafc895f1fe967abfd527a989921af4afa478ce19843a98163794abdaab8.jpg)



Content Analysis Flow


## 8.4 Setting of Operation Mode O

Pressing SHIFT + F3 (Mode O) on the Analysis FIGURE 4.1 will display the Mode O menu. 

When this mode has already been previously used, the last used values are displayed in respective areas. The cursor is always displayed at the D(Display mode). Select the mode you want using the ↑ or ↓ arrow key and pressing ENTER. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/a733c362a23440ed386e1c6925a415bf5433a1964fe5dbbcd15236140ed18092.jpg)



FIGURE 8.2: Operation Mode 0 Selection Screen


For modes D, P and N, their values are active for all analytical jobs. For modes T, F, and I, their values are active for content analysis only. 

## 1) "D" (Display Mode)

Provides the option for displaying analytical results on the screen as either <1: Each Result> or <2: (1) + R + S.D. + CV>. Pressing ENTER when the cursor is blinking at D will advance the cursor to option 1. Select either option using the ↑ or ↓ key, and press ENTER. 

The selected mode is entered in the item "Display Mode" in the lower part of the screen. 

$$
R = X \max - X \min
$$

R : Variance of multiple analytical value 

S.D.: Standard deviation 

Xmax: Maximum value 

Xmin: Minimum value in many times analysis 

$$
S. D. = \sqrt {\frac {\sum (X _ {i} - X) ^ {2}}{n - 1}}
$$

X : Average value in many times analysis 

C.V.: Coefficient of variation or relative standard deviation 

CV = $\frac{S.D.}{X} \times 100 [\%]$ 

2) "P" (Print Mode) 

Selects the mode for printing analytical results on the printer. Press the ENTER key, select either <M: Print by ...> or <A: Auto-print...> with the key ↑ or ↓, and press the ENTER key. Next, using ↑, ↓, ← and →, select one of <l: AVE> through <5: INT. l +...> and press the ENTER key. 

The specified mode is entered in the item "Print Mode" in the lower part of the screen. 

M: Manual print pressing the F4 (Print) key after completing an analysis. 

A: Auto-print 

Data is printed automatically after completion of an analysis. 

1: AVE 

Prints only the average value for a multiple burn analysis. 

2: Each result + AVE 

Prints each result and the average value for a multiple burn analysis. 

3: AVE + R + S.D. + CV 

Prints the average value R, S.D. and CV for a multiple burn analysis 

4: Each result + 3 

Prints each analytical value, the average value, R, S.D. and CV for a multiple burn analysis 

5: INT1 + INT2 + CONT (Only Cont & Special 3 times) 

In the contamination analysis and three times analysis, when the Print mode is the Auto-print, pre-correction intensity, post-correction intensity and inclusion rate are printed out. The contamination rate of each correction stages (per-correction, post-correction of matrix element, post-correction of star curve, pure calculation) also are printed out. 

## 3) "N" (Number of Analyses)

The number of burns for a multiple burn analysis can be specified up to 21 times. 

Pressing the ENTER key displays "JOB N: [Z]" beside the Ag-No. on the lower part of the screen. After entering the number of burns, press the ENTER key. The number of burns entered is placed in the item N in the lower part of the screen. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/990db6184376f2efdb103010899d450fd3775e942c0f9c74abf7a6a496efb956.jpg)


```txt
Operation Mode 0 Date 04-01-93 Time 18:14
D(Display mode) 1:Each result+AVE 2:(1)+R+STD+CV
P(Print Mode) M: Manual-print A: Auto-print
1: Ave 2: Each result+Ave
3: Ave+R+STD+CV 4: Each result+(3)
5: Int.1 + Int.2 (+ Cont(not corrected)+Matrix after+
Master curve after+pure cal after) + Cont.
N(No. of analysis) max.21
T(Computer trans.) M: Manual A: Auto
1 *
T(Printer trans.) M: Manual S: Semi-auto A: Auto
1 2 * 3 * 4
F(File mode) M: Manual-file A: Auto-file
I(Sample index set) consists of each characters. Make index at pleasure
HIGH STRENGTH STEEL [A]223
Display:1 Print:M2 Trans.-C:M Trans.-P:M File:M N: 2 AN: 36 TAN:3163
AG-NO.:[STEEL ] JOB N:[ 2]
9:Init 
```


FIGURE 8.3: Input Example of Number of Analysis


(Note) The number of burns cannot be altered once an analysis has begun. 

4) "T" (Mode of transmission to host computer) (For content analysis) 

A) Select either AUTO or MENU mode for transmitting analytical results to the host computer. 

Select either <M: Manual ...> or <A: Auto...> with the key ↑ or ↓, and press the ENTER key. 

<M: Trans by function key after multiple analysis> 

Analytical results are transmitted by pressing the F6 (Trans) key after completing an analysis. 

## <A: Auto-transmit after multiple analysis>

Analytical results are automatically transmitted after completing an analysis. 

## B) Select the destination for transmitting

Select number of destination computer (1, 2, 3, 4 or 5) with the key + or + and press the - key and press the ENTER key. 

Mote 

The destination computer 2 through 5 is optional. The standard QC-El has transmitting to only one computer. 

"T" (Mode of transmission to furnace printer) (For content analysis)
This function is optional. 

## 6) "F" (File Mode) (Upon content analysis)

Select either AUTO or MENU mode for filing analytical results. Press the ENTER key, select either <M: Manual ...> or <A: Auto ...> with the key ↑ or ↓ and press the ENTER key. A specified mode is put in the item File mode on the lower part of the screen. 

## <M: Manual filing>

Analytical results are filed by pressing F5 (File) after completing an analysis. 

## <A : Auto-File after multiple analysis>

Analytical results are automatically filed after completing an analysis. 

```txt
6) "I" (Sample Index Set) (For content analysis)
Set an entry frame within which an operator enters upon content analysis.
Pressing the ENTER key displays JOB I: [ ]: beside the AG-No. in the lower part of the screen 
```

```txt
Operation Mode 0 Date 04-01-93 Time 18:15
D(Display mode) 1:Each result+AVE 2:(1)+R+STD+CV
P(Print Mode) M: Manual-print A: Auto-print
1: Ave 2: Each result+Ave
3: Ave+R+STD+CV 4: Each result+(3)
5: Int.1 + Int.2 (+ Cont(not corrected)+Matrix after+
Master curve after+pure cal after) + Cont.
N(No. of analysis) max.21
T(Computer trans.) M: Manual A: Auto
1 *
T(Printer trans.) M: Manual S: Semi-auto A: Auto
1 2 * 3 * 4
F(File mode) M: Manual-file A: Auto-file
I(Sample index set) consists of each characters. Make index at pleasure
HIGH STRENGTH STEEL [A1223]
Display:1 Print:M2 Trans.-C:M Trans.-P:M File:M N: 2 AN: 36 TAN:3163
AG-NO.:[STEEL] JOB I:[HIGH STRENGTH STEEL [A1223]]
9:Init 
```

## FIGURE 8.4: Input Example of Sample Index

① To enter all 36 characters of the item Index upon analysis: 

Set "JOB: [ ]" and press the ENTER key. At this time, enter 36 characters worth of index between [ and]. 

② To enter a common sample name and a free index name in the item Index upon analysis: 

```txt
Set "JOB: [ SAMPLE NO. [ ] ]" and press the ENTER key. At this time, enter a common sample name for the Sample No. and an arbitrary index between [and]. 
```

③ To enter a common sample name and free index name in the item Index and display a 4-digit serial number upon analysis: 

Set "JOB: [ SAMPLE NO. [ ] < > ]" and press the ENTER key.
A counting up number is displayed between < and > per analytical sample. 

To erase it, clear to ")". When successively setting another analytical group, press the ESC key. The cursor moves to the item AG-No. When terminating registration, press the F9 (Init) key. The Analytical Mode screen appears. 

(Note) To prepare a daily report per sample index, the code within the brackets ([ ] ) becomes a keyword. 

## 8.5 Content Analysis

On the Analytical Job Selection Menu FIGURE 8.1, select the <X, CONT> mode with ↑ or ↓ and press the ENTER key. The Content Analysis screen is displayed. Content Analysis is a quantitative analysis of an unknown sample. 

## <Operating Method>

1. Enter an analytical group AG-No. name and press the ENTER key. Alternatively, display the Analytical Group Selection screen by pressing SHIFT + F6 (AG sel). Move the cursor to the analytical group name you want to analyze using $\uparrow$ , $\downarrow$ , $\leftarrow$ and $\rightarrow$ , and press the ENTER key. The specified analytical group is displayed in the Ag-No position and the cursor moves to the St-No position. 

2. Enter in the St-No position, a standard name from the Product Standard Check Registration Table and press the ENTER key. The cursor moves to the Index position. 

3. Enter the sample name in the Index position and press the ENTER key. The cursor moves to the AG-No position. 

4. Place the sample for analysis on the emission stand. 

5. Press the Fl (Start) key to begin the analysis. 

6. When the multi-burn is completed, analytical results are displayed on the CRT and printed on the printer. 

(Note 1) Transmitting the results to a remote computer 

When the Trans Mode is "A" (AUTO), results are transmitted after completing the analysis. When the Mode is "M" (MANUAL), they are transmitted by pressing F6 (Trans). 

(Note 2) Filing the results 

When the File Mode is "A" (AUTO), results are filed automatically after completing analysis. When the Mode is "M" (MANUAL), they are filed by pressing F5 (File). 

(Note 3) Number of data filed 

The data file can store a maximum of 10,000 records. When the number of records reaches 9,990 the message "File Full" is displayed. Use the <Maintenance> <Backup> mode to save the contents of the QCR directory to floppy disks. (Section 11.5). 

After the QCR directory backup is complete, the file must be reinitialized by restoring the directory using the original set of disks supplied with the spectrometer. 

Warning: When the data file is full, the new data overwrite the old data. 

(Note 4) For out of tolerance R control or out of tolerance product standard check, see 8.1 "Basic Using Method". 

(Note 5) When no product standard name or sample name has been specified during data acquisition, daily report preparation or X-R control cannot be done. 

(Note 6) The analyzed results can be modified by pressing the SHIFT + F8 (Modify) after completing of a multiple burn analysis. The analyzed results can also be cancelled by pressing the SHIFT + F7 (Cancel) keys on computer analysis. 

(Note 7) When the analytical element name displayed on the screen does not match the element name in the Standard Registration Table, the message "Undefined" and the element name are displayed in the lower part of the screen. 

(Note 8) If the order of analytical group names (AG-No.) or analytical elements is altered then the preceding and following data cannot be used for daily report preparation or X-R control. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/bebacdda7765a5b54f264d49059b82ea3a21d250d6ac4f1d0f68a57c6a4a7523.jpg)



FIGURE 8.5: Display Example of Content Analysis


8.6 Modicification and Cancel of Analytical Value 

8.6.1 Modification of Analytical Value 

The <Modify mode> screen is displayed by pressing SHIFT + F8 (Modify) after completing the data processing of a quantitative analysis. The data change item "Job M: NAME [ ] DATA [ ]" is displayed in the lower part of the screen. When using this mode, set the Transmission and File modes to MANUAL. 

Modify Mode is used to change the average value of an analysis. 

## <Operation Method>

1. Enter an analytical element name in NAME and press the ENTER key. The cursor moves to DATA. 

2. Enter in DATA the new average value and press the ENTER key. 

3. The average value (AVE) of the actual analysis is replaced by the data entered on the screen. 

4. If there are other elements you want to change, repeat steps 1) to 3). 

5. After all changes are completed, press F9 (Init). The Analysis Mode screen appears. 

6. To print the new results, press F4 (Print). 

7. The modified average values are followed by the mark "*". 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/67075bc170cf69d86d52282219f7d9d69bef5890d2edf8f54de276c3e3ffcfe6.jpg)



FIGURE 8.6: Display of Modify Mode Entry Item


## 8.6.2 Cancel of Analytical Value

The cancel screen is displayed by pressing the SHIFT + F7 (Cancel) key on the analytical screen in the multi-time analysis mode. The cancel number selection window is also displayed. 

Data can be cancelled during the analysis or after completion of the analysis. 

## <Reanalysis>

## <Operation Method>

1. Select a data number to be reanalyzed with the $\leftarrow$ or $\rightarrow$ key and press the ENTER key. 

2. The mark "*" is put under the specified number and on the left side of the "number of analysis" item, respectively. If the ENTER key is pressed again, this mode will be cancelled and the mark "*" will also disappear. 

The reanalysis can be specified within the range of "the number of analysis completed so far - 1". 

3. Press the ESC key and terminate this setting. 

(Note) When analytical data overflows the screen, scroll the analytical data to the left or to the right on the screen by pressing the TAB key or SHIFT + TAB keys. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/71bcc1420e185cbe42153b4eb8dc2132d2846f5e0253a9371a8272bb432f3cf4.jpg)



FIGURE 8.7: Example of Data Cancel Window


4. When the analysis is made after completion of the cancel setting, any cancel-specified analytical value will be replaced by the new result obtained from this reanalysis. 

5. the mark "*" put on the result of the reanalysis disappears. 

6 Even after completion of the specified analysis, the reanalysis can be continued until the forced termination is enforced. 

1. Select the forced averaging in the window on the screen 8.7 and press the ENTER key. The data obtained so far is then averaged and the analysis is terminated. 

This averaging process is performed with the cancel-specified data number neglected. 

2. Once the forced averaging is executed, no reanalysis can be made. 

3. The figures below show screen display and printout examples where the analysis is terminated with the forced averaging. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/17514db09df08d080b35bfd850c71ec16ce1a9577ffa60f2cc4a88a76f6a4b6a.jpg)



FIGURE 8.8: Screen Display Example with Forced Averaging Termination


## 8.7 Three-Time Analysis

On the Analytical Job Selection Menu FIGURE 8.1, select the <Special 3 times analysis> mode with ↑ or ↓ key and press the ENTER key. The Three-Time Analysis screen is displayed. 

Three-time analysis mode, requests a third analysis when the variance limit is exceeded in two first measurement. Then, calculates the average value for each element, using data with the minimum variance. However, when the variance limits is exceeded for the three times analysis, a three-time analysis error is recorded and an R is printed after the average value. 

## <Operating Method>

1. Enter an analytical group AG-No. name and press ENTER. Alternatively, press SHIFT + F6 (AG sel) to display the Analytical Group Selection screen. Move the cursor with the keys ↑, ↓, + and → to the analytical group to analyzed and press ENTER. The specified analytical group name is displayed in the AG-No position. 

The cursor moves to the ST-No position. 

2. Enter in the ST-No. position a standard name from the Product Standard Check Registration Table and press ENTER. The cursor moves to the Index position. 

3. Enter a sample name in the Index item and press ENTER. The cursor moves to the item Ag-No position. 

4. Place the unknown sample on the emission stand. 

5. Press Fl (Start) to start the analysis. 

6. Reposition the sample before the second measurement and press Fl (start) again. 

After the data have been processed, if there is an element out of R tolerance, the average is displayed in red and the message "no good" appears in the upper part of the screen. 

7. Reposition the sample again and press F1 (Start) to start the third analysis. An average value will now be calculated using the best two values (lowest variance) of the three values set. The results will be displayed on the screen and printed. 

(Note) After completing a two burn analysis, if you want to end the analysis with the R value out of tolerance, press F3 (Cal). 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/80a0917fa37e37057dfe160a1183e0011c9a1c3a6c5af36e5c3521d246dcc7cf.jpg)



FIGURE 8.10: Display Example of Three-time Analysis


8.8 Master Curve Recalibration Analysis or Type Standard Analysis 

On the Analytical Job Selection Menu FIGURE 8.1, select the Master Curve Recalibration mode with ↑ or ↓ and press ENTER. The Master Curve Recalibration Analysis screen is displayed. The correction coefficients MC and AC are determined using the working curve and a known standard sample. 

The correction coefficients MC and AC obtained are filed into the Master Curve Correction Sample and Target Value Registration Table. The same analytical results as chemical analytical values are obtained by correcting the working curve converted contents with MC and AC. 

## <Operating Method>

1. Enter an analytical group AG-No. name and press ENTER. The cursor moves to the Sample No position 

2. Enter the master curve correction sample name from the Master Curve Correction Sample and Target Value Registration Table, and press ENTER. The cursor moves to the Index position. 

3. Enter any desired characters in the item Index and press ENTER. The cursor moves to the Sample Number position. 

4. Place the correction sample on the emission stand. 

5. Press Fl (Start) to start the analysis. 

6. Analytical values displayed are those of the elements which match the selected sample name. 

7. After an N-burn analysis is completed, the average value is displayed and printed.
The message "Set next Sample" is displayed on the screen. 

8. Similarly, analyze all correction samples registered in the Master Curve Correction Target Value Registration Table. 

9. Press F3 (Cal) after completing each analysis. MC and AC values are calculated, displayed and printed. (For a master curve correction calculation formula, see the item Master Curve Correction Sample and Target Value Registration of Analytical Information). 

10. When calibrating another analytical group, move the cursor to the item Ag-No. using the key +. 

11. After completing the master curve correction recalibration, press F9 (Init). The Analytical Mode screen is displayed. 

(Note 1) If you press the F3 (Cal) key in the middle of the recalibration, AC and MC values are calculated only for the element displayed in the item AVE. The other elements display previous values. 

(Note 2) When the average value is out of standard value ranges of D1 to D2 of the Master Curve Correction Sample and Target Value Registration Table, the average value is displayed in pink and a message "Range Over!!" is displayed in the upper part of the screen. (MC and AC remain at the previous values). 

(Note 3) After performing one-point or two-point calibration analysis, be sure to recalibrate all type standard (or master curve correction) you will be using. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/054a16b4d5c0db5df47b22ccd2f6709616b9550c8a2b3093ba4c4718c594fbac.jpg)



FIGURE 8.11: Display Example of Master Curve Recalibration Analysis


9. ANALYTICAL OPERATION
INSTRUMENT CORRECTION OPERATION & ANALYTICAL INTENSITY MEASUREMENT 

9.1 Basic Operation Method 

9.2 Selection of Analytical Job 

9.3 Setting of Operation Mode 0 

9.4 Two-Point Recalibration Standardization Analysis 

9.5 One-Point Recalibration Standardization Analysis 

9.6 INT. Two-Point for Registration/Analysis of Target Value for Standardization 

9.7 INT Two for Working Curve Intensity Measurement for Working Curve Preparation 

9.8 INT. Two (Drift Corrected Intensity) Post-Correction Intensity Measurement 

9.9 INT. One (Raw Intensity)
Pre-Correction Intensity Measurement 

## 9.1 Basic Operation Method

1) Entering the Data 

a. Using ←, → and ENTER keys, move cursor to an entry item. After entering data, press ENTER. Its contents are displayed. 

b. When entering a numerical value, do not leave a space between numbers.
When leaving a space, use the $\sim$ key. 

c. When data entered is erroneous, an error message is displayed upon pressing the ENTER key. After correcting data, press ENTER again. 

2) Explanation of Function Keys for Analytical Operation 

Fl (Start) : Starts photometry. 

F2 (Stop) : Stops photometry. 

F3 (Cal) : Calculates values $\alpha$ , $\beta$ , k in Analytical Jobs 2 and 3 and those MC and AC in Analytical Jobs 2 and 3. 

F4 (Print) : Prints analytical results. 

F7 (Reset) : Erases from the screen the data halfway into the multiple analysis. 

F8 (-HV) : Turns -HV on/off to the readout unit. (A background color is switched to white when -HV is turned on). 

F10 (Curve) : Effective only for Job 7. Changes to the Coefficient Calculation screen. 

SHIFT + Fl (Menu): Displays the Master Menu screen. To erase, press the ESC key. 

SHIFT + F2 (Job) : Displays the Job Menu Selection screen. To erase, press ESC key. 

(Note 1) When one of the function keys F1 through F10 are pressed while processing is currently under way, a background color is switched to white. 

(Note 2) When -HV of the readout unit is turned off or abnormally occurs halfway through an analysis, an error message "Measurement Error" is displayed. (If the integral value of internal standard element AR-No. 1 comes to 0.02 or less, a check function will work). 

## 3) Displaying the Analytical Value Mark

"!!!!!" is displayed in red when an analytical value overflows. When analytical information is erroneous and is impossible to calculate, "*****" is displayed. 

4) Calculating the Measured Intensity 

① Pre-Correction Intensity I 

I = $\frac{Intensity of measured element}{Intensity of internal standard element} \times 100$ 

(Note) The intensity of the internal standard element and measured element overflows at 0.8 or more). 

② Post-Correction Intensity $I_{DC}$ 

$I_{DC}=k(\alpha I+\beta)$ 

k, $\alpha$ , $\beta$ : Drift correction constants 

5) Variance Check in Intensity analysis (R Control) 

R control is checked using a value of R/average rather than through the quadratic equation control. 

a. When R control is out of range by 3% to less than 6%, the screen displays an average value in blue. To the printer, r is printed after the average value. 

b. When R control is out of range by 6% or more, the screen displays an average value in red. To the printer, R is printed after the average value. 

6) Scrolling the Analysis Screen 

When more data than is displayed on the screen is analyzed in a multiple analysis, beginning analytical values are erased from the screen. To display the erased data, press TAB or SHIFT + TAB. 

7) Number of Emission Times 

TAN: Displays the total number of emission times. 

AN : Displays the number of emission times since waste discharge. 

## 9.2 Selection of Analytical Job

To view the Analytical Job Selection Menu from the Master Menu FIGURE 2, press SHIFT+ F2 (Job). 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/30e73d6d918f740e7cd68772d65542db19d4096bb65a083a1f7b9e8db632e1d4.jpg)



FIGURE 9.1: Analytical Job Selection Menu Screen


Each job is selected by moving the cursor with the↑ or ↓ arrow key and pressing ENTER. 

<2, l-point recalibration> One-point calibration standardization analysis. Analysis mode for obtaining a value of the drift correction coefficient k. 

<3, 2-point recalibration> Two-point calibration standardization analysis. Analysis mode for obtaining values of the drift correction coefficient $\alpha$ and $\beta$ . 

<4, Master curve recalibration> Master curve correction standardization analysis. (See 8.8) 

Analysis mode for obtaining values of the master curve correction coefficients AC and AC and MC. Be sure to do this after <l-point or 2-point recalibration> standardization analysis. 

<5, INT. 1 (Raw intensity)> Pre-Correction intensity analysis. 

Analysis of an intensity value which has not been corrected by drift correction. 

<6, INT. 2 (Drift corrected intensity)> Post-Correction intensity analysis. Analysis of an intensity value for which pre-correction intensity has been corrected with drift correction coefficients obtained through l-point or 2-pointre calibration analysis. 

<7, INT. 2 for Working Curve> 

Creating working curves and Matrix Element Correction coefficients. 

<8, INT. 2 for target> Calibration target value analysis.
Used for automatically registering target values for the Drift Correction
Coefficient Registration Table of Analytical Information. 

<X, Cont> Content analysis. 

Analysis of a content. 

<Y, Special 3-time analysis> Three-time content analysis 

Three-time analysis performs the third analysis when a variance check is out of range in two times of analysis. It obtains an average value per element using data with a minimum variance. However, when the content is out of variance check range for three times running, a three-time analysis error results. 

## 9.3 Setting of Operation Mode O

Pressing SHIFT + F3 (Mode O) on the Analysis screen will display the Mode O Setting screen. 

When a mode has been set. its state is displayed in respective display areas. Since the cursor is displayed at a position of D (Display mode), select the mode you want to set using the $\uparrow$ or $\downarrow$ and press ENTER. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/609f0bcbe8eb521b93986a6e63835b9fe4d8a6ab242d68c0d20476a1e0f19449.jpg)



FIGURE 9.2: Operation Mode O Selection Screen


## 1) "D" (Display Mode)

Set a mode for displaying analytical results on the screen by pressing the ENTER key, selecting either <1: Each Result> or <2: (1) + R + S.D. + CV> with the key + or + and pressing the ENTER key again. 

A specified mode is entered in the item "Display Mode" on the lower part of the screen. 

$$
R = X \max - X \min
$$

Standard deviation S.D. 

$$
= \sqrt {\frac {\sum (X _ {i} - X) ^ {2}}{n - 1}}
$$

Xmax: Maximum value in a multiple analysis. 

Xmin: Minimum value in a multiple analysis. 

$\bar{X}$ : Average value in a multiple analysis. 

Coefficient of variation 

$X_{i}$ : Each analytical value 

$$
\mathrm{CV} = \frac {\mathrm{S.D.}}{\mathrm{X}} \times 1 0 0 [ \% ]
$$

## 2) "P" (Print Mode)

Set a mode for printing analytical results to the output of printer. Press the ENTER key, select either <M: Print by ...> or <A: Auto-print...> with the key ↑ or ↓, and press the ENTER key. Next, using ↑, ↓, + and →, select one of <l: AVE> through <5: INT. l + ...> and press the ENTER key. 

A specified mode is entered in the item "Print Mode" on the lower part of the screen. 

M: Print by Function Key after many times analysis
Printed by pressing the F4 (Print) key after completing an analysis. 

A: Auto-print after time analysis
Printed automatically after completing an analysis. 

1: AVE
Prints only an average values for a multiple analysis. 

For a multiple analysis this option prints the values for each analysis and the corresponding average. 

3: AVE + R + S.D. + CV 

Prints an average value R, S.D. and CV for a multiple analysis 

## 3) "N" (Number of Analysis)

The number of analyses for a multiple analysis can be specified up to 21 times. 

Pressing the ENTER key displays "JOB N: [ ]" beside the Ag-No. on the lower part of the screen. After entering the number of analyses, press the ENTER key. 

The number of analyses entered is placed in the item N on the lower part of the screen. 

## 4) T (Transmission), F (File) and I (Index)

Cannot be set. 

## 9.4 Two-Point Recalibration Standardization Analysis

After the two-point recalibration procedure is completed press F3 to calculate the new values of $\alpha$ and $\beta$ . The coefficients correct the current measured intensity values to the registered target values. 

The new correction coefficient values $\alpha$ and $\beta$ are automatically filled into the correction Target Value Registration Table. Periodically repeating the two point recalibration, and obtaining new values for $\alpha$ and $\beta$ can maintain optimum operating conditions. 

## <Operating Method>

1. Enter an analytical group AG-No. name and press ENTER. The cursor moves to the item Sample Number. 

2. Enter the standardization sample names registered in the items "H" and "L" of the Drift Correction Target Value Registration Table and press ENTER. The cursor moves to the item Index. 

3. Enter any desired characters in the item Index and press ENTER. The cursor moves to the item Sample Number. 

4. Set onto the emission stand, the correction sample set in the item Sample Number. 

5. Press Fl (Start) to start an analysis. 

6. Analytical values displayed are only those of elements which match a registered sample name. 

7. When a sample surface to be analyzed is changed and N-time measurement is complete, an average value is displayed per element in the item "H" for a high-content standardization sample and in "L" for a low-content standardization sample, respectively and sent to the printer. A message "Set next Sample" is displayed on the screen. 

8. At the same time, analyze all standardization samples registered in the Drift Correction Target Value Registration Table. 

9. After completing an analysis, press F3 (Cal). The $\alpha$ and $\beta$ values are calculated, displayed on the screen and printed to the printer. At this time, a value of k is 1.0. 

10. To standardize another analytical group, move the cursor to the item AG-No. with key. 

11. After completing the two-point calibration standardization analysis, press F9 (Init) and the Analysis Mode screen will be displayed. 

(Note 1) If the F3 (Cal) key is pressed halfway through a standardization analysis, the alpha and beta values will be obtained with only the elements displayed in both items "H" and "L". The other elements will display previous values. 

(Note 2) When correcting the master curve, perform a master curve standardization analysis after the two-point recalibration. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/86b2082e6527b7d4faf089faca2808567c142b71e87b6f41289432bec81458ce.jpg)



FIGURE 9.3: Display Example of Two-Point Recalibration Standardization Analysis


## 9.5 One Point Recalibration Standardization Analysis

On the Analytical Job Selection Menu (FIGURE 9.1), select the <l-point recalibration> mode with + or + and press ENTER. The One-Point Recalibration Standardization Analysis screen is displayed. One-point calibration standardization obtains a correction coefficient of k from the registered target values and measured values upon standardization analysis. 

The obtained value for k is automatically filed into the Drift Correction Target Value Registration Table. The analyzer can be kept in an optimum condition by periodically obtaining the correction coefficient, k. 

## <Operating Method>

1. Enter an analytical group (AG-No.) name and press ENTER. The cursor moves to the item Sample Number. 

2. Enter the standardization sample names registered in the item "K" of the Drift Correction Target Value Registration Table and press ENTER. The cursor moves to the item Index. 

3. Enter any desired characters in the item Index and press ENTER. The cursor moves to the item Sample Number. 

4. Set onto the emission stand, the correction sample set in the item Sample Number. 

5. Press Fl (Start) to start an analysis. 

6. Analytical values displayed are only those of elements which match a registered sample name. 

7. When a sample surface to be analyzed is changed and N-time measurement is complete, an average value is displayed per element in the item "k" and sent to the printer. A message "Set next Sample" is displayed on the screen. 

8. At the same time, analyze all standardization samples registered in the Drift Correction Target Value Registration Table. 

9. After completing an analysis, press F3 (Cal). The k value is calculated, displayed on the screen and sent to the printer. At this time, up-to-date values are displayed for $\alpha$ and $\beta$ . 

10. To standardize another analytical group, move the cursor to the next AG-No. item using the + key. 

11. After completing the one-point calibration standardization analysis, press F9 (Init) and the Analysis Mode screen will be displayed. 

(Note 1) If the F3 (Cal) key is pressed halfway through a standardization analysis, the kvalue will be obtained with only the elements displayed in both items "k". The other elements will display previous values. 

(Note 2) Perform the drift correction with the Two-Point Recalibration Standardization analysis after the One-Point Recalibration Standardization. 

(Note 3) When correcting the master curve, perform a master curve standardization analysis after the One-Point Recalibration Standardization. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/82eed52ad2aa44e2f9756609ce00c9264eea77a79b09ca543d9977886c32f2f3.jpg)



FIGURE 9.4: Display Example of One-Point Recalibration Standardization Analysis


9.6 INT 2-Point for Recalibration/Analysis of Target Value for Standardization 

On the Analytical Job Selection Menu FIGURE 9.1, select the <INT.2 for point target> mode with ↑ or ↓ and press ENTER. The Standardization Target Value Registration/Analysis screen is displayed. 

Standardization target value registration analysis automatically registers into the Drift Correction Target Value Registration Table target values which serve as targets for a one-point and two-point recalibration standardization. 

## <Operating Method>

1. Enter an analytical group (AG-No.) name and press ENTER. The cursor moves to the item Sample No. 

2. Enter the sample names registered in the items "H", "L" and "K" of the Drift Correction Target Value Registration Table and pres ENTER. The cursor moves to the item Index. 

3. Enter any desired characters in the item Index and press ENTER. The cursor moves to the item Sample No. 

4. Set onto the emission stand, the standardization sample set in the item Sample No. 

5. Press Fl (Start) to start an analysis. 

6. Analytical values displayed are only those of elements which match a registered sample name. 

7. When a sample surface to be analyzed is changed and N-time measurement is complete, analytical results are displayed on the screen. Measured values of elements not registered are also sent to the printer. 

8. A message "File Completed" is displayed on the screen and analytical results 9 AVE) are filed in the "H", "L" and "K" intensity items of the Drift Correction Target Value Registration Table. 

9. Similarly, analyze the standardization samples registered in the Drift Correction Target Value Registration Table. 

10. When analyzing the standardization samples of another group, move the cursor to the item "Ag-No." with +. 

(Note 1) Entering an unregistered sample name (i.e. sample name is not found in the Standardization Target Value Registration Table) in the item 'Sample number' will cause the error message, "Data Error!", to be displayed. 

(Note 2) When a measured value is abnormal, enter the same sample name and measure again. An abnormal value is replaced by a newly measured value. 

(Note 3) When data is filed in the items "H", "L" and "K", an element's color on the screen is changed. 

. When filed in both items "H" and "L", element names are blue.
. When filed in all items "H", "L" and "K", element names are red. 

(Note 4) When changing the standardization sample, manually input a sample name and a measured intensity in the Drift Correction Target Value Registration Table. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/dee35b15-f4e4-4bf5-8ddf-08268857acbb/297e7f7d7ca420a4e9c48ed2eedf859e9a9f1442e9832bcd69eeeef2fc82705d.jpg)



FIGURE 9.5: Display Example of Standardization Target Value Registration Analysis


9.7 INT. 2 for Working Curve Intensity Measurement for Working Curve Creation
Intensity values obtained with this selection are used to complete the working curve and matrix element correction coefficients. Register the sample names in the Standard Sample Registration Table (Section 7.2) of the Coefficient Calculation Program. All intensities measured are post-correction intensities, and if numerous samples are used to generate the curves it is recommended that the two-point recalibration be performed every 30 minutes to correct for any drift of equipment. 

## <Operating Method>

1. Enter an analytical group (Ag-No.) name and press ENTER. The cursor moves to the item Sample Number. 

2. Enter the working curve standard sample names registered in the Standardization Sample Registration Table of the Coefficient Calculation Program and press ENTER. 

3. Enter any desired characters in the item Index and press ENTER. The cursor moves to the item Sample Number. 

4. Set onto the emission stand, the standardization sample set in the item Sample No. 

5. Press Fl (Start) to start an analysis. 

6. When a sample surface to be analyzed is changed and N-time measurement is complete, analytical results are displayed on the screen and sent to the printer. 

7. A message "File Completed" is displayed on the screen and analytical results (AVE) are filed in the Sample Name Table. 

8. Similarly, analyze the working curve standard samples registered in the Standard Sample Name Registration Table. 

9. After measuring the registered working curve standard samples, press F10 (Curve).
You are taken to the 'Coefficient Calculation Sub-menu' (FIGURE 29). Obtain the working curve coefficients and matrix element correction coefficients mentioned in Section 7. 

9.7 INT. 2 for Working Curve Intensity Measurement for Working Curve Creation
Intensity values obtained with this selection are used to complete the working curve and matrix element correction coefficients. Register the sample names in the Standard Sample Registration Table (Section 7.2) of the Coefficient Calculation Program. All intensities measured are post-correction intensities, and if numerous samples are used to generate the curves it is recommended that the two-point recalibration be performed every 30 minutes to correct for any drift of equipment. 

## <Operating Method>

1. Enter an analytical group (Ag-No.) name and press ENTER. The cursor moves to the item Sample Number. 

2. Enter the working curve standard sample names registered in the Standardization Sample Registration Table of the Coefficient Calculation Program and press ENTER. 

3. Enter any desired characters in the item Index and press ENTER. The cursor moves to the item Sample Number. 

4. Set onto the emission stand, the standardization sample set in the item Sample No. 

5. Press Fl (Start) to start an analysis. 

6. When a sample surface to be analyzed is changed and N-time measurement is complete, analytical results are displayed on the screen and sent to the printer. 

7. A message "File Completed" is displayed on the screen and analytical results (AVE) are filed in the Sample Name Table. 

8. Similarly, analyze the working curve standard samples registered in the Standard Sample Name Registration Table. 

9. After measuring the registered working curve standard samples, press F10 (Curve).
You are taken to the 'Coefficient Calculation Sub-menu' (FIGURE 29). Obtain the working curve coefficients and matrix element correction coefficients mentioned in Section 7. 

(Note 1) If you enter in the item "Sample Number" the sample name unregistered in the Standard Sample Name Registration Table, a message "Data Error!" will be displayed. 

(Note 2) When a measured value is abnormal, enter the same sample name and measure again. An abnormal value is replaced by a newly measured value. 

(Note 3) When there are many working curve standard samples, perform the two-point recalibration standardization during an analysis. (A drift of the equipment is corrected). 

(Note 4) When one analytical group has 100 or more working curve standard samples, measure similarly with another group of identical analytical conditions. Data measured with the analytical group within identical analytical conditions can be shared. (To measure with another analytical group, move the cursor to the item "Ag-No." with the + key. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/bdaa5799ba835c2fb41e4bde51229f991e8b7e672fd7cd9ac4d9b7823c4cef44.jpg)



FIGURE 9.6: Display Example of Working Curve Creating Intensity Measurement


9.8 INT.2 (Drift Corrected Intensity) Post-Correction Intensity Measurement 

On the Analytical Job Selection Menu (FIGURE 9.1), select the <INT.2 (Drift Corrected Intensity)> mode with ↑ or ↓ and press ENTER. The Post-Correction Intensity Measurement screen is displayed. 

Post-correction intensity is obtained by correcting the pre-correction intensity with calibration correction coefficients ( $\alpha$ , $\beta$ , and k values). 

$$
I _ {D C} = k (\alpha I + \beta)
$$

$$
I: \quad \text { Pre - correction   intensity }
$$

This can also be used as an intensity for a working curve coefficient calculation. 

When converting the standardization sample, measure target values in this mode after performing drift correction in the Two-point Recalibration Standardization Analysis mode. 

## <Operating Method>

1. Enter an analytical group (Ag-No.) name and press ENTER. The cursor moves to the item Sample Number. 

2. Enter any desired sample name in the item Index and press ENTER. The cursor moves to the item "Ag-No." 

3. Set a sample to be measured onto the emission stand. 

4. Press Fl (Start). Analytical values are displayed on the screen. 

5. When a sample surface to be analyzed is changed and N-time measurement is completed, an average value is displayed on the screen and sent to the printer. 

6. When analyzing with a sample name change, move the cursor to the item "Index" and perform the same operation. 

7. When analyzing with an analytical group changed, move the cursor to the item "Ag-No." and perform the same operation. 

When a standardization sample currently used is becoming too thin for use and you want to change it to another, follow these procedures: 

① Perform a two-point recalibration standardization with the standardization sample currently being used. 

② Measure in this mode the standardization sample to be changed and obtain a post-correction intensity. 

③ Register the obtain post-correction intensity and a sample name in the Drift Correction Reference Value Registration Table. 

④ Alternatively, measure in the <INT.2 for target> Analysis mode. (When the sample name is changed at this time, change also the sample names registered in the Drift Correction Target Value Registration Table). 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/24e00b895894dd2c75a4494fdc9d256c196fa99619a12ad6467fccb651369fe0.jpg)



FIGURE 9.7: Display Example of Post-Correction Intensity


9.9 INT.1 (Raw Intensity) Pre-Correction Intensity Measurement 

On the Analytical Job Selection Menu (FIGURE 9.1), select the <INT.1 (Raw intensity)> mode with ↑ or ↓ and press ENTER. The Post-correction Intensity Measurement screen is displayed. 

Pre-correction intensity is an A/D converted value integrated by the integrator of the readout unit. It is generally called a raw intensity and used experimentally. 

## <Operating Method>

1. Enter an analytical group (Ag-No.) name and press ENTER. The cursor moves to the item Sample Number. 

2. Enter any desired sample name in the item Index and press ENTER. The cursor moves to the item "Ag-No." 

3. Set a sample to be measured onto the emission stand. 

4. Press Fl (Start). Analytical values are displayed on the screen. 

5. When a sample surface to be analyzed is changed and N-time measurement is completed, an average value is displayed on the screen and sent to the printer. 

6. When analyzing with a sample name change, move the cursor to the item "Index" and perform the same operation. 

7. When analyzing with an analytical group changed, move the cursor to the item "Ag-No." and perform the same operation. 

(Note) The measured intensity I of the measured element is calculated as follows: 

I = $\frac{Intensity of measured element}{Intensity of internal standard element} \times 100$ 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/a6246e253fcfc20c8215d38039b638a8dbcfc7103e8df1dc9e029f11ee758906.jpg)



FIGURE 9.8: Display Example of Pre-Correction Intensity Measurement


## 10. DATA REPORT

10.1 Data Print Out 

10.2 Long Term Repeatability Check 

10.3 Analytical Frequency 

10.4 Stability Check 

10.5 Data Modification 

10.6 Histogram 

## 10. DATA REPORT

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/0976e3e3505d806fbbd28b29331371eedc323d06a259c0cf691d815ca5a21353.jpg)



FIGURE 10.1: Daily Report Menu Screen


## Explanation of Function Keys

F 4 (Print) : Copies the screen. 

F 5 (Help) : Displays the Help screen. To erase, press ESC. 

F 9 (Init) : Returns to the Analysis Mode screen. 

F10 (Sub-menu) : Returns to the Report Sub-menu FIGURE 10.1. 

SHIFT + Fl (Menu) : Displays the Main Menu screen. 

(Note 1) One day processed in this program refers to a span of 24 hours from 7:00 a.m. to 7:00 a.m. the next day. 

Data print out 

Prepares a daily report per analytical group, ST-No. (standard name) and sample index. 

Long term check of repeatability 

Prepares and X-R control chart per standard name (St-No.). 

## A analyzing frequency

Totalizes the number of analysis times. 

Stability check 

Controls accuracy of analytical instruments. 

Data modification 

Modifies data. 

Histogram 

Creates Histogram 

10.1 Data Print Out 

Using the key $\uparrow$ or $\downarrow$ , select the <Data print out> mode on the Report Sub-menu screen. The Daily Report Preparation screen is displayed. 

This program prepares a daily report per 1) analytical group AG-No., 2) product standard name ST-No. and 3) Sample index and prints to the printer. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/bc6f4a2abca5e2d6cb7cd32d0b5191cf22af2bb52f4332c1217907ff323b34e6.jpg)



FIGURE 10.2: Daily Report Preparation Mode Selection Screen


Explanation of Function Keys 

F7 (Reset): Returns to the Daily Report preparation Mode Selection Screen. 

## 10.1.1 Preparing the Daily Report per Analytical Group (Ag-No)

On the Daily Report Preparation Mode Selection screen, select the <Analytical group> mode with the key ↑ or ↓ and press ENTER key. The Analytical Group Daily Report Preparation screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/99e91d8538c38ba3f1bf981500de4862299d3587d50083ec3825de209707b7d1.jpg)



FIGURE 10.3: Input Example of Analytical Group Setting Screen


## <Operating Method>

1. The screen displays a message "Please type Ag-No. and press <Enter>" Enter an AG-No. name on which you prepare a daily report and press the ENTER key. The cursor moves to the item "Period". 

2. In the item "Period", enter start and end dates of the daily report preparation in the form of "Month/Day/Year-Month/Day/Year" and press ENTER. 

3. The screen displays a message "Press F4 (Print) to start print out". Press F4 (Print). 

4. All data on the analytical group and period specified are printed to the printer. 

5. To stop printing halfway, press the ESC key. 

(Note 1) Unless the input AG-No. data exist or the input AG-No. is registered in analytical information, the message "Date error!" appears. 

(Note 2) Enter the only start date in the item "Period" and press the F4 (Print) or F6 (Trans) key, and the only data of specified date is printed out or transmitted. 

(Note 3) Unless the input period data exist in the item "Period", the message "No data in the period!" appears. 

10.1.2 Preparing the Daily Report Per Standard Name 

On the Daily Report Preparation Mode Selection screen, select the <Standard No.> mode with the key ↑ or ↓ and press the ENTER key. The Standard Name Daily Report Preparation screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/f26c21472c7b96413f8d5274beadef80943c2b54b36904a3cd77efeb5055d35b.jpg)



FIGURE 10.4: Input Example of Standard Name Setting Screen


## <Operating Method>

1. The screen displays a message "Please type ST-No. and press <Enter>" Enter an ST-No. name on which you prepare a daily report and press the ENTER key. The cursor moves to the item "Period". 

2. In the item "Period", enter start and end dates of the daily report preparation in the form of "Month/Day/Year-Month/Day/Year" and press ENTER. 

3. The screen displays a message "Press F4 (Print) to start print out". Press F4 (Print). 

4. All data on the analytical group and period specified are printed to the printer. 

5. To stop printing halfway, press the ESC key. 

(Note 1) Unless the input ST-No. data exist or the input ST-No. is registered in the Analytical information, the message "Data error!" appears. 

(Note 2) Enter the only start date in the item "Period" and press the F4 (Print) or F6 (Trans) key, and the only data of specified date is printed out and transmitted. 

(Note 3) Unless the input period data exist in the item "Period", the message "No data in the period!" appears. 

## 10.1.3 Perparing the Daily Report Per Sample Index

On the Daily Report Preparation Mode Selection screen, select the <Sample Index> mode with the key ↑ or ↓ and press ENTER key. The Sample Index Daily Report Preparation screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/17d840aa67e328550c94362d6708e9088e7d0719eacb5f6d35b69ed74e1fc383.jpg)



FIGURE 10.5: Input Example of Sample Index Setting Screen


## <Operating Method>

1. The screen displays a message "Please type Sample Index and press <Enter>" Enter the sample index name on which you prepare a daily report and press the ENTER key. The cursor moves to the item "Period". 

2. In the item "Period", enter start and end dates of the daily report preparation in the form of "Month/Day/Year-Month/Day/Year" and press ENTER. 

3. The screen displays a message "Press F4 (Print) to start print out". Press F4 (Print). 

4. All data on the analytical group and period specified are printed to the printer. 

5. To stop printing halfway, press the ESC key. 

(Note 1) Unless the input Sample Index data exist, the message "Date error!" appears. 

(Note 2) Enter the only start date in the item "Period" and press the F4 (Print) or F6 (Trans) key, and the only data of specified date is printed out or transmitted. 

(Note 3) Unless the input period data exist in the item Period, the message "No data in the period!" appears. 

(Note 4) The "?" mark of the input item in Sample Index makes all characters the retrieval objects. 

For example, to retrieve the first letter of Sample Index or "A" sample, set [A??? ... ?]. 

If you input nothing, all data is the retrieval object. 

## 10.2 Long Term Repeatability Check

On the Report Sub-menu screen, select the <Long-term check of repeatability> mode with the key ↑ or ↓ and press the ENTER key. The X-R control screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/95665cd7208f97ba902fa3e9708154223e9002f05a2ab6303ffb6eaeca3055ba.jpg)



FIGURE 10.6: Input Example of X-R Control Setting Screen


ST-No. : Enter a product standard name 

Period : Enter a plotting period 

AG-No. : Enter an analytical group name 

Ele : Enter an element name for which plotting is to be done. 

## Explanation of Function Keys

Fl (Graph) : Displays the X-R control chart for a set element. 

F6 (Elem) : Displays the element window. 

## <Operating Method>

1. The screen displays a message "Please type ST-No. and press <Enter>." Enter the sample index name on which you prepare a daily report and press the ENTER key. The cursor moves to the item "Period". 

2. In the item "Period", enter start and end dates of the X-R control in the form of "Month/Day/Year-Month/Day/Year" and press ENTER. The cursor moves to the item "AG-No.". 

3. Enter in the item "AG-No." the analytical group name for which X-R control is to be done and press ENTER. The cursor moves to the item "ELE". 

4. Enter in the item "ELE" the element name for which the X-R control is to be plotted and press ENTER. 

5. The screen displays a message "Press Fl to graph the data". Press Fl (Graph) 

6. The X-R control charge for the specified element is displayed on the screen. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/17cf0259bf214159ac0a3e087c0b5817fd9885f58045e287a38324f2b5b2b39c.jpg)



FIGURE 10.7: Display Example of X-R Control Chart


Content : X-R control chart 

Upper/Lower : Standard limits registered in the Standard Value Registration Section 5.13. 

R : Variance chart for multiple analysis 

Max : Maximum analytical and variance values and the date when the X-R control chart is prepared 

Min : Minimum analytical and variance values and the date when the X-R control chart is prepared 

Av : Average value of analytical values and variance when the X-R control chart is prepared. 

Additional Explanation of Function Keys 

F 7 (Reset): Returns to the X-R Control Setting screen. 

F 8 (Data) : Displays the data window. 

F10 (Print): Prints out the data out of spec. 

7. To copy the screen to the printer, press F4 (Print/Copy). 

8. To check the data at each display position of the X-R control chart, press F8 (Data). 

9. A sample name/analytical data window is displayed on the screen. The 

data specified is displayed in the X-R control chart as a red " " mark. 

10. To check the data of other samples, press the + or → . 

The displayed data is changed in a file order. 

11. To erase window data, press F8 (Data) again. 

12. To change the period or element name in the X-R control, press F7 

(Reset). The X-R Control Setting FIGURE 10.6 is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/14118bda7f7715ae0c23447f1a3f87a59d13168d2edc6aca5b729ee5197ee3ba.jpg)



FIGURE 10.7.1: $\overline{\mathbf{X}}$ -R Control Chart and Display Example of Data Window


(Note 1) Unless the input ST-No. data exist or the input ST-No. is registered in the Analytical information, the message "Data error!" appears. 

(Note 2) Unless the Input period data exist in the item "Period", the message "No data in the period!" appears. 

(Note 3) Enter the only start date in the item "Period", and the X-R control chart of specified date is created. 

(Note 4) Unless the input AG-No. data exist or the input AG-No. is registered in Analytical information, the message "Date error!" appears. 

(Note 5) If the retrieval data are over than 561 cases, the message "Data over flow. Please reset shorter period. Press F7" as a control chart appears on the display screen. 

(Note 6) When the only one retrieval datum exists, the message "No data!" appears on the display screen. 


10.3 Analytical Frequency



On the Report Sub-menu screen, select the <Analytical Frequency> mode with the key ↑ or ↓ and press ENTER. The Analytical Frequency Totalization screen is displayed.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/953f9a2315106b206c807bc089bec55cd9b19f2f0c068a6b9cdb8370166005b0.jpg)



FIGURE 10.8: Display Example of Analytical Frequency Totalization Setting Screen


Period : Enter a period during which analytical frequency data are to be totalized. 

## <Operating Method>

1. In the item "Period", enter start and end dates of analytical frequency data totalization in the format of "Month/Day/Year-Month/Day/Year" and press ENTER. 

2. After the message "Press F4 (Print) to start print out" is displayed on the screen, press F4 (Print). 

3. Data on the specified period are totalized and printed to the printer. 

(Note) When only the start date of totalization is entered, the data on the entered date only is totalized. 

10.4 Stability Check 

On the Report Sub-menu FIGURE 10.1, select the <Stability Check> mode with the key ↑ or ↓ and press ENTER. The Stability Check screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/a173f0e44aabad9410ac0f9766e1ce0ae2c374a65f08f99d0513cf164faf7b8e.jpg)



FIGURE 10.9: Input Example of Stability Check Setting Screen


Index : Enter a sample index. 

Period : Set a period during which accuracy control is to be tabulated. 

Ele : Enter an element name to be displayed in the stability check chart. 

Additional Explanation of Function Keys 

F3 (AG sel): Displays the analytical group selection screen. 

F6 (Elem) : Displays the element window. 

<Operating Method> 

1. After the message "Please type index and press <ENTER>" is displayed on the screen, enter the sample name for which stability check is to be done, and press ENTER. 

The cursor moves to the item "Period". 

2. In the item "Period", enter start and end dates of the stability check chart preparation in the format of "Month/Day/Year-Month/Day/Year" and press ENTER. 

3. Press the F3 (AG sel). Select an analytical group for which accuracy control is to be performed using $\uparrow$ or $\downarrow$ key and press the ESC key. To erase it, press the ESC key. 

4. Enter in the item "ELE" the element name for which the stability check is to be done and press ENTER. To display the Window screen for the element name entered, press F6 (Elem). 

To erase, press the ESC key. Element names are displayed in a registration order in the Analytical Element Display and Printing Order Registration Table (Section 5.11) of the Analytical Information. 

5. After the message "Press F1 to graph the data" is displayed on the screen, press F1 (Graph). 

6. The stability check chart for the set element is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/75c513e410ffae448a2ef973f3db9858c651538ca852053143439f429166eb63.jpg)



FIGURE 10.10: Display Example of Stability Check Chart


Content: Stability check chart 

R : Variance chart upon multiple analysis 

Max : Maximum analytical value and variance value and the date when the stability check chart is prepared 

Min : Minimum analytical value and variance value and the date when the stability check chart is prepared 

AV : Average value of analytical value and variance when the stability check chart is prepared 

## Explanation of Function Keys

F7 (Reset): Returns to the Stability Check Setting FIGURE 10.9. 

F8 (Data) : Displays the data window. To erase, press F8 and ESC. 

7. To copy the screen to the printer, press F4 (Copy). 

8. To check the data at each display position of the stability check chart, press F8 (Data). 

9. To check other data, press or . The data is changed in a file order. 

10. To change the accuracy control input conditions, press F7 (Reset). This 

returns you to the Stability Check Setting Screen. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/3727c5fd4ed007d6fae361d7bddbb740ea398199bc0d77533488b3c3837d1ab4.jpg)


FIGURE 10.10.1: Accuracy Control Chart and Data Window (Note 1) Unless the input Index data exist in the specified period, the message "No data in the period" appears. 

(Note 2) The "?" mark of the input item in Sample Index makes all characters the retrieval objects. 

For example, to retrieve the first letter of Sample Index or "A" sample, set [A??? ... ?]. 

If you input nothing, all data is the retrieval object. 

(Note 3) If the data extend into the plural AG-No. (Analytical Groups) and the AG-No. is not specified, the data which belongs to the first retrieved data is the retrieval object. 

(Note 4) Enter the only start date in the item "Period", and the X-R control chart of specified date is created. 

(Note 5) If the retrieval data are over than 561 cases, the message "Data over flow. Please reset shorter period. Press F7" as a control chart appears on the display screen. 

(Note 6) When the only one retrieval datum exists, the message "No data!" appears on the display screen. 

## 10.5 Data Modification

On the Report Sub-menu screen 10.1, select the <Modify data> mode with ↑ or ↓ key and press √key. The data modification selection screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/08a761ed4e26e08817c10ad542d7af70f34c25bb1c2499679e267e023e061495.jpg)



FIGURE 10.11: Input Example of Modification Data Selection Screen


## Explanation of Function Keys

<table><tr><td>F 2 (Search)</td><td>: Moves to the entry screen for a data No. to be searched.</td></tr><tr><td>F 5 (Help)</td><td>: Displays the help screen.</td></tr><tr><td>F 8 (Modify)</td><td>: Displays the data to be modified and moves to the modification screen.</td></tr><tr><td>F 9 (Init)</td><td>: Returns to the analytical mode screen.</td></tr><tr><td>F10 (Sub-menu)</td><td>: Returns to the report sub-menu screen.</td></tr><tr><td>Shift + F1 (Menu)</td><td>: Returns to the main menu.</td></tr><tr><td>Shift + F2 (All del)</td><td>: All data is deleted.</td></tr></table>

1. Move the cursor to the data to be modified with $\uparrow$ or $\downarrow$ key. 

2. Press the ↘ here. The background color of the sample turns red. 

3. When the background color is red, press the function key F8 (Modify). 

4. The modification screen for the analytical data of the specified No. is then displayed. 

5. Move the cursor to the item to be modified with $\uparrow$ , $\downarrow$ , $\leftarrow$ , or $\rightarrow$ and make a modification with the $\swarrow$ key. 

6. Pressing the function key Fl (Reset) allows the modification data selection screen to be returned. Continue the modification here. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/3f8c138fd37f2f16392bc2916dcc2e8e47446df3d8e1e720b527030e55537a34.jpg)



FIGURE 10.12: Data Modification Screen


(Note 1) The data here is displayed using a floating point regardless of the number of digits specified for analytical information. 

(Note 2) In FLG, the out-of-standard marks H and L, and overflow and skip marks are displayed. 

H: Out of upper limit standard 

L: Out of lower limit standard 

T: Out of trace standard 

S: Channel skipped data 

!: Overflow 

?: Data out of calculation of matrix element correction coefficient 

R: Out of R-check 

To display the Histogram parameter setting screen, Select the <Histogram> mode on the Report sub-menu using the ↑ or ↓ key and press the ENTER key. 

```txt
Histogram Date 04-01-93 Time 14:48
ST-No. SCM
Period 7 /1 /1992~7 /31/1992 < mm/dd/yy >
AG-No. STEEL
Index HIGH STRENGTH STEEL?????????????
Ele C
Press F1(Graph) to graph the data.
1:Menu
1:Graph 9:Init 10:Submenu 
```

FIGURE 10.13 Display Example of Histogram Parameter Setting Screen 

ST-No : Enter the product specification name. 

Period : Enter the period to create the Histogram. 

AG-No : Enter the analytical group name. 

Index : Enter the sample index. 

Ele : Enter the element name to create the Histogram. 

N= 246 AV=.37269
R=.07485 CP=.82129
S=.01218 CPK=.74760
U=.40000 OVER 3
L=.34000 UNDER 4
(1) - .34245[.33871] 5
(2) - .34994[.34620] 3
(3) - .35742[.35368] 13
(4) - .36491[.36117] 41
(5) - .37239[.36865] 52
(6) - .37988[.37614] 76
(7) - .38736[.38362] 27
(8) - .39485[.39111] 19
(9) - .40233[.39859] 8
(10) - .40982[.40608] 2 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/1c910035818cb6616d382d8cd6d784de3b762b6233206e98264ed261e52077fe.jpg)


## FIGURE 10.14: Display Example of Histogram

8. Average, R value, Standard Deviation, CP value and CPK value are displayed with the histogram according to 7. 

$$
\mathrm{AV} = \frac {\sum_ {i = 1} ^ {N} X _ {i}}{N}
$$

N : Number of data 

$$
R = M a x - M i n
$$

AV : Average of analytical value 

R : R value 

S : Standard deviation 

$$
S = \sqrt {\frac {\sum_ {i = 1} ^ {N} (X - X i) ^ {2}}{N - 1}}
$$

CP : CP value 

CPK: CPK value 

$$
C P = \frac {U - L}{6 \times S}
$$

Xi : Each analytical value 

$$
C P K = \frac {U - A V}{3 \times S} (0 <   U - A V <   A V - L)
$$

Max: Maximum analytical value 

Min: Minimum analytical value 

U : Controlled upper limit
(Specification upper limit or Upper limit to controlled upper value) 

$$
C P K = \frac {A V - L}{3 \times S} (0 <   A V - L <   U - A V)
$$

L : Controlled lower limit
(Specification lower limit or
L) Controlled lower limit of the
histogram) 

$$
\mathrm{CPK} = 0
$$

$$
(A V <   L \text { or } U <   A V)
$$

Double dot line is displayed on the position of the average $\pm n\sigma$ on the histogram display screen. 

n: Coefficient (1 ~ 9, default is 2) 

σ: Standard deviation 

Refer to "QC-El INSTALLATION MANUAL" to modify the coefficient "n". 

Additional Explanation of Function Keys 

F7 (Reset): Returns to the histogram parameter setting screen. 

9. To modify the parameter to create the histogram, press the F7 (Reset) key. 

Return to histogram parameter setting screen. 

10. Press the F4 (Copy) key to copy a screen. Print out the screen. 

(Note 1) Unless the input ST-No. data exist or the input ST-No. is registered in the Analytical information, the message "Data error!" appears. 

(Note 2) Unless the input period data exist in the item "Period", the message "No data in the period!" appears. 

(Note 3) When enter the only start date in the item "Period", the histogram is created with the specified date data. 

(Note 4) Unless the input AG-No. data exist or the input AG-No. is registered in the Analytical information, the message "Data error!" appears. 

(Note 5) Unless the input Index data exist in the specified period, the message "No data in the period!" appears. 

Note 6) The "?" mark of the input item in Index makes all characters the retrieval objects. For example, to retrieve the all data beginning with A, of sample name enter [A??? ... ?]. 

If you input nothing, all data is the retrieval object. 

(Note 7) In the control upper limit and control lower limit, if the ST-No. is input, a control upper limit and lower limit of the specification check information are used. On the contrary, if not, a control upper limit and lower limit are used. 

Additional Explanation of Function Keys 

Fl (Graph) : Displays the histogram of the set element. 

F3 (AG sel): Displays the AG-No. (Analytical Group) selection screen. 

F6 (Elem) : Displays the element name window. 

## <Operation Method>

1. While the message "Please type Index and press <ENTER> is being displayed, enter the product specification name and press the ENTER key. Unless you input the product specification name at the retrieval item, you press the only ENTER key. 

The cursor moves to the Period item. 

2. Input the each "Month/Date/Year" of the start date and end date to create the histogram in the Period item. 

(Ex.) To print out the data from 1/1/1993 to 1/31/1993, press the key as follows. 

1 ENTER 1 ENTER 9 3 ENTER 1 ENTER 3 1 ENTER 9 3 ENTER
The cursor moves to the AG-No. item. 

3. Input the Analytical group name to display the histogram on AG-No. item and press the ENTER key. 

Pressing F3 (AG sel) key displays the AG-No. table. Move the cursor to the AG-No. to select and press the ENTER key, and the setting screen appears and the selected AG-No. is displayed. 

The cursor moves to Index item. 

4. Input the sample name in Index item and press the ENTER key. 

5. Input the element name to display the histogram in Ele item and press the ENTER key. 

The element name window is displayed by pressing the F6 (Elem) key. Press the ESC key to clear the window. 

6. After the message "Press Fl to graph the data" is displayed on the screen, press the Fl (Graph) key. 

7. The histogram you set an element is displayed according to 6 above. 

8. The horizontal width of histogram is decided by the control upper limit or the maximum of data and the control lower limit or the minimum of data. 

## 11. MAINTENANCE

11.1 Waste Discharge 

11.2 Manual Scanning 

11.3 Lamp Test 

11.4 Date and Time Setting 

11.5 System Backup 

11.6 Information of Maintenance 

11.7 TAN (Total No. of Emission Times) Clear 

## 11. MAINTENANCE

On the Master Menu screen, select the <Maintenance> mode with the ↑ or ↓ and press the ENTER key. The Maintenance Sub-menu screen is displayed. With the key ↑ or ↓ ,select desired item and press the ENTER key. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/3e90938cf486a4886dad7dbc63927418018a09e28ec807aae3e7f279445f2e44.jpg)



FIGURE 11.1 Maintenance Sub-menu Screen


Explanation of Function Keys Commonly used for Maintenance 

Fl (Start) : Starts photometry. 

F4 (Print) : Copies the screen. 

F8 (-HV) : Turns -HV on/off. 

F9 (Init) : Returns to the Maintenance Sub-menu Screen 11.1. 

SHIFT + Fl (Menu) : Displays the Main Menu screen. 

Contents of Maintenance Mode 

Waste discharge ..... Performs a waste discharge to clean the electrode. 

Manual scanning .... Adjusts the inlet slit. Set a scanning dial position to a spectral peak position. 

Lamp test ....Performs a lamp test and used for checking the photometric system (photomultiplier, -HV, ITG). 

Date & Time .... Sets a date and time. 

System backup .... Backup and saves the system. 

## Information of maintenance

Sets the information used for waste discharge, lamp test and manual scanning, as well as that for the emission source. 

TAN clear ....Clears the total No. of emission times TAN to 0. 

Temperature/Voltage/Degree of vacuum
...... Displays the temperature, voltage and degree of vacuum in the spectrometer. 

## 11.1 Waste Discharge

Select the <Waste discharge> mode on the Maintenance Sub-menu screen. The Waste Discharge screen is displayed. 

Waste discharge is a discharge to stabilize emission when setting a new electrode (including a reformed one) to the emission stand. 

This operation causes AN on the right side of the analysis screen to be cleared to 0. 

For emission conditions of waste discharge, enter in the Waste Discharge Information Table of Section 11.6 Analytical Information for Maintenance. 

<Operation Method> 

1. Set onto the emission stand a sample for waste discharge. 

2. Press the Fl (Start) to start emission. 

3. Waste discharge ends upon its 5th emission. 

4. A message "Waste Discharge End!!" is displayed on the screen. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/45d7c87a0592b9cbabb8bb08dbd8c972c0910adc03da8df936999234aad794ab.jpg)



FIGURE 11.2: Waste discharge Screen


## 11.2 Manual Scanning

Select the <Manual scanning> mode on the Maintenance Sub-menu screen. The Manual Scanning screen is displayed. 

In the item "Element", the top element name of ITG-No. of the spectrometer is displayed. 

When a temperature inside the spectrometer changes, a spectral peak position also changes. Manual scanning means to set the spectral peak position with the scanning dial. 

Attenuator sensitivity adjustment for lamp test is also provided. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/381963235f4b5fcf7bac490da668e048ddd06008f0e0fb7bd6d865b820630942.jpg)



FIGURE 11.3: Display Example of Manual Scanning Screen


Element: Element name for ITG-No. 

ATT : Attenuator value.
Displays a filed attenuator value. If the attenuator value is altered, a registered value will be also altered. 

Scale : Intensity value display scale (the Key → moves the cursor). A display scale can be altered by entering one of values 1 through 9 or 0 ("0" for 10 times). 

Explanation of Function Keys 

Fl (Start) : Starts emission. 

F2 (Stop) : Stops emission. 

F3 (Pause) : Waits for an entry with emission turned on and nothing displayed. 

F4 (Copy) : Copies the screen. 

F6 (Mark) : Displays a yellow "O" mark at a current profile intensity. 

F7 (Reset) : Erases the profile curve on the screen. 

F8 (-HV) : Turns on/off -HV. 

(Note) Pressing the function key turns its background color into white. 

## 11.2.1 Manual Scanning Operating Method

1) Set a profile sample onto the emission stand. 

2) If the F1 (Start) key is pressed and emission starts, intensities for elements displayed will be displayed. 

3) Alter the ATT value so that a profile intensity will be set to the 8th graduation. 

4) Shift the scanning dial value of the spectrometer by about 30 graduations in a decremental direction from a current peak position to eliminate backlash, and set to the peak position minus 15 graduations. 

5) About 1 second later, move the dial by 5 graduations in an incremental direction. When the intensity is relatively stabilized, press the F6 (Mark) key. 

A yellow "O" mark is displayed at a profile intensity value. Then, move the scanning dial by 5 graduations in the incremental direction. 

6) Repeat the step 5) above (by 15 graduations in the incremental direction from an initial peak position). 

7) Press the F2 (Stop) key to stop emission. (A result as in Screen 11.3 is obtained.) 

8) Calculate a peak position out of the profile curve displayed on the screen. (Calculate in the method as described in a figure, not with a peak point of the curve.) 

Peak position : $\frac{512 + 505}{2} = 508.5$ 

9) Finally, adjust the dial to a calculation result.
When this is done, move the dial in one direction from a lower graduation to a higher graduation in order to eliminate backlash. 

11.2.2 Sensitivity Adjustment for Lamp Test 

1) Copy the contents of the Manual Scanning Information Table of Maintenance Information, Section 11.6 and clear a source condition to "0" (Zero) (Lamp test). 

2) By pressing the F7 (Copy) key on the Lamp Test/ISE/ATT Information FIGURE 11.11 of Maintenance Information, file and copy the ATT values of the table into the Manual Scanning Information Table. (The ATT value of the Manual Scanning Information Table is set for a lamp test.) 

3) Select the <Manual scanning> mode from the Maintenance Sub-menu FIGURE 11.1 and set the ATT value for a lamp test. 

4) Using the key →, move the cursor to the item "Scale" and set Scale (×10). 

5) Enter an ITG-No. name in the item "Element" and press the ENTER key. The ATT values filed are displayed. 

6) Press the Fl (Start) key. 

The screen displays an intensity at a time when the lamp is lit up. 

7) Enter the ATT value so that a screen graduation will be the 8th one. 

8) Enter other ITG-Nos., repeat the steps 5) to 7) and determine the ATT values of all ITGs. 

9) Press the F10 (Sub-menu) key to display the Maintenance Sub-menu Screen 11.1, and then, display the Manual Scanning Information Table of Maintenance Information. 

10) Press the F7 (Copy) key on the Manual Scanning Information Registration FIGURE 11.9. The ATT values displayed are filled in the Lamp Test/ISE/ATT Information Registration Table (FIGURE 11.11). 

11) Manually enter the contents of the screen copied in the step 1) into the Manual Scanning Information Table. 

AVE R STD CV
Fe1 89.277 .11605 .03782 .04236
Fe2 112.01 .14566 .04746 .04237
C 89.967 .12140 .03711 .04125
Si 91.754 .20221 .07366 .08028
Mn 101.22 .21120 .05436 .05370
P 90.938 .20162 .07239 .07960
S 104.62 .21694 .08185 .07824
Cu 99.381 .25000 .08053 .08103
Ni1 106.48 .22009 .07053 .06624
Ni2 97.226 .20819 .06449 .06633
Cr 108.36 .13956 .05185 .04785
Mo 99.975 .25098 .06887 .06888
Mg 103.10 .21307 .07910 .07672
Ti 96.799 .12428 .03948 .04079
V 108.43 .17433 .05113 .04716
Sn 108.75 .17838 .06274 .05769 

Display:2 Print:A4 Trans.-C: Trans.-P: File:M N:10 AN:680 TAN:2866
AG-No.:[LAMPTEST] [ ] 1:Menu 8:-HV 9:Init 10:Submenu
1:Start 

## FIGURE 11.4: Display Example of Lamp Test

## Explanation of Function Keys

Fl (Start) : Starts the lamp test. 

F2 (Stop) : Stops the lamp test. 

: Erases a lamp test measured value. 

F8 (-HV) 

: Turns on/off -HV. (When turned on, a background color is turned into white.) 

The photometric system (photomultiplier, -HV, ITG, etc.) is diagnosed by conducting the lamp test. Set the Lamp test mode, and 2 hours later after turning on -HV, press the F1 (Start) key. After completing 10 times of measurement, results of an average value, R, S. D and CV are displayed and printed. It is normal if a value of CV at this time is 0.1 or less. (Excluding photomultipliers other than R300 and R306) 

## 11.4 Date and Time Setting

Select the <Date & Time> mode on the Maintenance Sub-menu FIGURE 11.1. The Date and Time Setting screen is displayed. 

For example, when you set May 8, 1992, 1:25:05 p.m., enter: 

<table><tr><td>Date</td><td>05</td><td>-08</td><td>-92</td></tr><tr><td>Time</td><td>13 :</td><td>25 :</td><td>05</td></tr></table>

(Note) When a month or day is 1-digit value, prefix it with 0 and enter as 2 characters. 

## 11.5 System Backup

Select the <System backup> mode on the Maintenance Sub-menu FIGURE 11.4. Then the System backup screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/6f56d75f00497bec15403f75b44f008bf451c51679785fa459d3af758106ecde.jpg)



FIGURE 11.4: System Backup Initial Screen



Using the key $\uparrow$ or $\downarrow$ , select mode and press the ENTER key.



Load system from FDD to FXD : Copies information from a floppy sheet (FDD) to a fixed disk (FXD).



Save system from FXD to FDD : Copies information from a fixed disk (FXD) to a floppy sheet (FDD).



Formatting FDD : Initializes a new floppy disk.



This system has 6 directories, for each of which load and save actions are allowed.


<table><tr><td>Directory Name</td><td>Content</td><td>Sheet No.</td></tr><tr><td>EXE/*.EXE</td><td>QC-E1 system program</td><td>01</td></tr><tr><td>DSP/DSP*.DAT</td><td>Displaying screen information</td><td>01</td></tr><tr><td>ACH/HLP*.DAT</td><td>Help display information</td><td>01</td></tr><tr><td>QCD</td><td>QC-E1 analytical information</td><td>Sheet Nos. vary depending on volume of file.</td></tr><tr><td>QCR</td><td>Data of analytical results daily report</td><td>Sheet Nos. vary depending on volume of file.</td></tr></table>

## 1) Save System

The following is a description of Save mode operation (from the fixed disk (FXD) to the floppy sheet (FDD)). 

① Select the <Save system from FXD to FDD> mode with the key ↑ or ↓ and press the ENTER key.
Then the cursor moves to the DIRECTORY NAME SELECT area. 

② Move the cursor to the directory name to be selected with the key ↑ or ↓ and then press the ENTER key. 

③ Enter the F1 (Execute) key. 

Then the Save system is activated with the following message display appearing on the screen. 

QC-E1 data backup process
Freeze the help files and copy to the floppy sheet. 

Completion of freezing.
Copy to the floppy sheet (s). 

Copy from \hlp. lzh to a:\hlp. lzh insert backup disk 01 in drive A: Strike any key when ready 

④ Following the instruction displayed on the screen, set the backup sheet No. 01 on the floppy drive. 

⑤ After setting the floppy sheet, press the ENTER key.
This will cause data of FXD to be copied on FDD.
(Lamp of the floppy drive sheet goes on. Never attempt to take out the sheet while the lamp is ON.) 

⑥ When copying of sheet ends, a message appears on the screen. Following messages displayed on the screen, repeat above procedures ④ ~ ⑤ for floppy sheets in the order of their numbers. 

Insert backup disk 02 in drive A: Strike any key when ready 

⑦ When saving of all sheets of the selected directory name is completed, display changes to 11.4: 

⑧ Move the cursor to another directory name and repeat procedures ①
~ ⑦ above. 

(Note 1) Be sure to store floppy sheets putting serial Nos., and 

(Note 2) Be sure to set in the floppy drive the floppy sheet whose number is shown on the display. 

(Note 3) Be sure to perform saving from No. 01 of each directory name as no saving from other No. than 001 is permitted. 

## 2) Load System

（2）在 $x$ 轴上的方程中，当 $x \in \mathbb{Z}$ 时，当 $x \in \mathbb{Z}$ ，则

Operation for floppy sheet (FDD) to fixed disk (FXD) in the load mode is same as for the Save mode. 

Because of the system configuration, be sure to load sheets in the order of Sheet Nos. 

order of Sheet Nos. 

1. 2017年，公司与上海浦东发展银行股份有限公司签订了《最高额保证合同》，约定在2018年1月1日、2018年1月2日、2018年1月3日、2018年1月4日、2018年1月5日、2018年1月6日、2018年1月7日、2018年1月8日、2018年1月9日、2018年1月10日、2018年1月11日、2018年1月12日、2018年1月13日、2018年1月14日、2018年1月15日、2018年1月16日、2018年1月17日、2018年1月18日、2018年1月19日、2018年1月20日、2018年1月21日、2018年1月22日、2018年1月23日、2018年1月24日、2018年1月25日、2018年1月26日、2018年1月27日、2018年1月28日、2018年1月29日、2018年1月30日、2018年1月31日、2018年1月32日、2018年1月33日、2018年1月34日、2018年1月35日、2018年1月36日、2018年1月37日、2018年1月38日、2018年1月39日、2018年1月40日、2018年1月41日、2018年1月42日、2018年1月43日、2018年1月44日、2018年1月45日、2018年1月46日、2018年1月47日、2018年1月48日、2018年1月49日、2018年1月50日、2018年1月51日、2018年1月52日、2018年1月53日、2018年1月54日、2018年1月55日、2018年1月56日、2018年1月57日、2018年1月58日、2018年1月59日、2018年1月60日、2018年1月61日、2018年1月62日、2018年1月63日、2018年1月64日、2018年1月65日、2018年1月66日、2018年1月67日、2018年1月68日、2018年1月69日、2018年1月70日、2018年1月71日、2018年1月72日、2018年1月73日、2018年1月74日、2018年1月75日、2018年1月76日、2018年1月77日、2018年1月78日、2018年1月79日、2018年1月80日、

（1）在 $x$ 轴上，当 $y$ 为正方形，且 $\xi = y$ 的值为 $0.25$ , 则 $\xi = 0.25$ .

① To initialize a new floppy sheet, select the Formatting Mode with ↑, ↓ keys and then enter ENTER key. 

② Then the initialization system is activated with the following display appearing on the screen. 

QC-E1 format process 

Initialization a floppy sheet.
WARNING! Files in the floppy sheet will be erased. 

Insert new diskette for drive A: and press ENTER when ready ... 

③ Set the floppy sheet to be initialized in the floppy drive. 

④ After setting the floppy sheet properly, press the ENTER key. Then, the red lamp on the floppy drive goes on and initialization starts. (Never attempt to take out the sheet while the lamp is ON). 

⑤ Upon completion of initialization of each sheet, a message appears on the screen. To continue initialization, enter Y and then press the key ENTER and repeat procedures ③ ~ ⑤ above. 

⑥ Upon completion of all initialization, enter N and press the ENTER key. 

<Backup or resave the analytical information in each analytical condition group> 

1) When the resave (FDD + FXD) mode or backup (FDD + FXD) mode is selected, the cursor moves to the directry select area. Select "¥QCD2¥*.*: Specification A. Con file" using the ↑ or ↓ key, and press the ENTER key. 

2) When the backup lights up in red, press the key.
Analytical condition group (A. Con) selection screen appears. 

<table><tr><td colspan="9">Date 03-26-93 Time 18:54A.Con.No.=1</td></tr><tr><td>AG-No.</td><td>NAME</td><td>AG-No.</td><td>NAME</td><td>AG-No.</td><td>NAME</td><td>AG-No.</td><td>NAME</td><td>AG-No.</td></tr><tr><td>1</td><td>LowAlloy</td><td>21</td><td></td><td>41</td><td></td><td>61</td><td></td><td>81</td></tr><tr><td>2</td><td></td><td>22</td><td></td><td>42</td><td></td><td>62</td><td></td><td>82</td></tr><tr><td>3</td><td></td><td>23</td><td></td><td>43</td><td></td><td>63</td><td></td><td>83</td></tr><tr><td>4</td><td></td><td>24</td><td></td><td>44</td><td></td><td>64</td><td></td><td>84</td></tr><tr><td>5</td><td></td><td>25</td><td></td><td>45</td><td></td><td>65</td><td></td><td>85</td></tr><tr><td>6</td><td>STEEL</td><td>26</td><td></td><td>46</td><td></td><td>66</td><td></td><td>86</td></tr><tr><td>7</td><td></td><td>27</td><td></td><td>47</td><td></td><td>67</td><td></td><td>87</td></tr><tr><td>8</td><td></td><td>28</td><td></td><td>48</td><td></td><td>68</td><td></td><td>88</td></tr><tr><td>9</td><td></td><td>29</td><td></td><td>49</td><td></td><td>69</td><td></td><td>89</td></tr><tr><td>10</td><td></td><td>30</td><td></td><td>50</td><td></td><td>70</td><td></td><td>90</td></tr><tr><td>11</td><td>FC CAST</td><td>31</td><td></td><td>51</td><td></td><td>71</td><td></td><td>91 SIMA</td></tr><tr><td>12</td><td></td><td>32</td><td></td><td>52</td><td></td><td>72</td><td></td><td>92</td></tr><tr><td>13</td><td></td><td>33</td><td></td><td>53</td><td></td><td>73</td><td></td><td>93</td></tr><tr><td>14</td><td></td><td>34</td><td></td><td>54</td><td></td><td>74</td><td></td><td>94</td></tr><tr><td>15</td><td></td><td>35</td><td></td><td>55</td><td></td><td>75</td><td></td><td>95</td></tr><tr><td>16</td><td>FCD CAST</td><td>36</td><td></td><td>56</td><td></td><td>76</td><td></td><td>96 SBC</td></tr><tr><td>17</td><td></td><td>37</td><td></td><td>57</td><td></td><td>77</td><td></td><td>97</td></tr><tr><td>18</td><td></td><td>38</td><td></td><td>58</td><td></td><td>78</td><td></td><td>98</td></tr><tr><td>19</td><td></td><td>39</td><td></td><td>59</td><td></td><td>79</td><td></td><td>99</td></tr><tr><td>20</td><td></td><td>40</td><td></td><td>60</td><td></td><td>80</td><td></td><td>100</td></tr><tr><td colspan="9">Please select A.Con No. by using arrow key and press</td></tr></table>

FIGURE 11.5: Analytical Condition Group (A. Con)
Selection Screen Display 

Select the A. Con No. using the arrow keys and press the ENTER key.
When resave (FDD → FXD): 

The message "Replace existing A. Con No. ? (Y/N)" is displayed. (This message is erased by pressing the ENTER or ESC key, and return to A. Con. No. selection mode). 

An information is registered in specified analytical condition group by pressing "Y" key and ENTER key in order. 

When backup (FXD → FDD): 

If any Analytical Group Name (AG-Name) is registered in the selected A. Con No., the information of the specified condition group is backupped. If the Analytical Group is pre-registered in the specified condition group, the "Data error!" appears. 

## 11.6 Information of Maintenance

Analytical Information for Maintenance 

Select the <Information of Maintenance> mode on the Maintenance Sub-menu FIGURE 11.1. The Analytical Information for Maintenance screen is displayed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/27bec0100a90d91fb728caf28f4a56d1b7a913098bbed5aa677562c2f7ac49aa.jpg)



FIGURE 11.7: Example of Analytical Information for Maintenance Screen


This information sets; 

1) Waste discharge analytical information 

2) Manual scanning analytical information 

3) Lamp test analytical information 

4) Source code 

With ↑ or ↓, move the cursor to the mode you want to select, and press the ENTER key. 

Ar Flush(X0.1sec) = 30 

Sequence 1
Source 1
Preburn Time 70 x0.1sec
Integ Time 40 x0.1sec 

Cleaning
Source 5
Cleaning Time 2 x0.1sec 

1:Menu 4:Print 

Source No.
0 : Fatigue lamp
1 : Normal spark
2 : High power spark
3 : Combined spark
4 : Oscillation spark
5 : Cleaning spark
6 :
7 :
8 :
9 : 

# FIGURE 11.8: Input Example of Waste Discharge Information Registration Screen

Ar Flush : Set an argon flush time. 

Source : Set a source code for waste discharge. 

Preburn Time : Set a preburn time for waste discharge. 

Integ. Time : Set an integrating time for waste discharge. 

Cleaning Source: Set a source code for cleaning. 

Cleaning Time : Set a cleaning time. 

```txt
2). Information of Manual Scanning
When selected on the Analytical Information for Maintenance screen, the Manual Scanning Information screen is displayed.
What are of either and very close to good? If you have an analytical
subject to the subject is a result of the results to the
yes non-chemical laboratory exit or very much good results. 
```

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/013191c0ed773994356252e24cc2a5c2e17fccd711cf0816ab173644c8b6b1a3.jpg)



FIGURE 11.9: Input Example of Manual Scanning Information Registration Screen


Source: Set a source code for manual scanning. 

ITG : Integrator No. 

ELE : Element name. 

ATT : Set an attenuator value. Although it is filed from the Manual Scanning FIGURE 11.3, it can be also manually entered. 

With this table. determine an emission source for manual scanning. The ATT value is automatically filed from the Manual Scanning FIGURE 11.3. 

When determining the ATT value for the lamp test, do so in the <Manual scanning> mode and press the F7 (Copy) to file from this table to the Lamp Test/ISE/ATT Information Registration Table. 

Pressing the ESC key returns you to the Analytical Information for Maintenance FIGURE 11.7. 

<table><tr><td colspan="2">1984年6月7日</td><td colspan="2">2005年6月23日</td><td colspan="2">2006年6月23日</td><td colspan="2">2007年6月23日</td></tr><tr><td>单位</td><td>合计</td><td>金额</td><td>占比</td><td>金额</td><td>占比</td><td>金额</td><td>占比</td></tr><tr><td>中国</td><td>1,000</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td></tr><tr><td>美国</td><td>1,000</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td></tr><tr><td>德国</td><td>1,000</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td></tr><tr><td>法国</td><td>1,000</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td></tr><tr><td>日本</td><td>1,000</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td></tr><tr><td>韩国</td><td>1,000</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td></tr><tr><td>印度</td><td>1,000</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td></tr><tr><td>泰国</td><td>1,000</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td></tr><tr><td>其他</td><td>1,000</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td><td>1,000</td><td>100%</td></tr></table>

# 1. 2017年，公司与上海浦东发展银行股份有限公司签订了《关于使用部分闲置募集资金进行现金管理的协议》。

[1] 2017年，美国国家航空航天局（NASA）与俄罗斯国家航空航天局（NASA）签署《关于加强和改进航天工程的批复》。

61. 2023年1月1日

$\therefore f(x) = 1$ $\therefore f(x) = 2$ $\therefore f(x) = 3$ $\therefore f(x) = 4$ $\therefore f(x) = 5$ $\therefore f(x) = 6$ $\therefore f(x) = 7$ $\therefore f(x) = 8$ $\therefore f(x) = 9$ $\therefore f(x) = 10$ 

$\frac{1}{2}$ $\frac{1}{2}$ $\frac{1}{2}$ $\frac{1}{2}$ $\frac{1}{2}$ $\frac{1}{2}$ $\frac{1}{2}$ $\frac{1}{2}$ $\frac{1}{2}$ 

(2) $\frac{1}{2}$ (3) $\frac{1}{2}$ (4) $\frac{1}{2}$ (5) $\frac{1}{2}$ (6) $\frac{1}{2}$ (7) $\frac{1}{2}$ (8) $\frac{1}{2}$ (9) $\frac{1}{2}$ (10) $\frac{1}{2}$ (11) $\frac{1}{2}$ (12) $\frac{1}{2}$ (13) $\frac{1}{2}$ (14) $\frac{1}{2}$ (15) $\frac{1}{2}$ (16) $\frac{1}{2}$ (17) $\frac{1}{2}$ (18) $\frac{1}{2}$ (19) $\frac{1}{2}$ (20) 

<table><tr><td colspan="7">1:Menu
2:Next 3:Print 4:Init 5:Submenu</td></tr><tr><td colspan="7">Source No.</td></tr><tr><td colspan="7">0: Fatigue lamp</td></tr><tr><td colspan="7">1: Normal spark</td></tr><tr><td colspan="7">2: High power spark</td></tr><tr><td colspan="7">3: Combined spark</td></tr><tr><td colspan="7">4: Oscillation spark</td></tr><tr><td colspan="7">5: Cleaning spark</td></tr><tr><td colspan="7">6:</td></tr><tr><td colspan="7">7:</td></tr><tr><td colspan="7">8:</td></tr><tr><td colspan="7">9:</td></tr></table>

## FIGURE 11.10 Input Example of Lamp Test Analytical Condition

Registration Screen 

Source : Set a source code for the lamp test. 

Preburn Time : Set a preburn time for the lamp test. 

Integ. Time : Set an integrating time for the lamp test. 

## Function Keys

F2 (Next): Displays the Lamp Test/Internal Standard Element Attenuator Registration screen.
The lamp Test/Internal Standard Element (ISE)/Attenuator (ATT) Registration screen is displayed by pressing F2 (Next) on the Lamp Test Analytical Condition Registration FIGURE 11.10. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/534c3e4934eea5c60c78fde8b0347c7e5fb1af512b258e71b65c74838b2c04b2.jpg)


1. 2017年，公司与上海浦东发展银行股份有限公司签订了《关于使用部分闲置募集资金进行现金管理的协议》。

FIGURE 11.11: Input Example of Lamp Test/ISE/ATT Registration Screen 

ITG : Integrator No. 

ELE : Element name 

SEQ : Measurement sequence 

ISE : Select whether or not the internal standard method is to be used, and set internal standard elements when it is used.
0 : Constant-time integral 

```txt
Function Keys
F2 (Next): Takes to the Lamp Test Analytical Element Registration screen.
F3 (Pre) : Returns to the Lamp Test Analytical Condition Registration screen.
F7 (Copy) : Copies the attenuator values displayed on the screen to the Manual Scanning Information Registration screen 11.9. 
```

The Lamp Test Analytical Element Registration screen is displayed by pressing F2 (Next) on the Lamp Test SEQ/ISE/ATT Registration screen. 

```txt
Lamp Test Information Date 04-01-93 Time 19:24
(3) Order of Analytical Channel
AR-NO. ITG ELE NAME AR-NO. ITG ELE NAME AR-NO. ITG ELE NAME
1 1 FE1 Fe1 17 17 B B
2 2 FE2 Fe2 18 18 PB Pb
3 3 C C 19 19 CO Co
4 4 SI Si 20 20 W W
5 5 MN Mn 21
6 6 P P 22
7 7 S S 23
8 8 CU CU 24
9 9 NI Ni 25
10 10 CR Cr 26
11 11 MO Mo 27
12 12 AL Al 28
13 13 V V 29
14 14 TI Tt 30
15 15 SN Sn 31
16 16 NB Nb 32
1:Menu unmed: 2:01:01:01
3:Pre. 4:Print
9:Init 10:Submenu 
```

FIGURE 11.12: Input Example of Lamp Test Analytical Element Information Registration Screen 

```txt
AR-No. : Analytical element No. into some functions and analysis
ITG : Set an integrator No. to the number of elements
ELE : Displays an element name
NAME : Set an analytical element name. 
```

```txt
FIGURE 11.13: Input Example of Source Code Information Registration Screen
Jewels (Jewels) test used to use a sugar (Sugal) (Sugal)
Kesip2 no-treatyzed jolvaticini
No. : Source No.
SOURCE : Set a source code with a hexadicimal number : 04-54
STAND : Set a selection of the emission-stand I or IIa : 071
COMMENT: Set a comment. - was therele as evalise: 04
..emark fromels leotvism as rea : 2840 
```

```txt
Function Keys

F3 (Pre): Returns to the Lamp Test/ISE/ATT Registration screen. (yes) 50
Register element names to be printed upon the lamp test.
4) Information of Source Code

When selected on the Analytical Information for Maintenance screen, the Source Code Information Registration screen is displayed. 
```

```txt
Source Code Table
Date 03-26-93 Time 18:49
No. SOURCE STAND -COMMENT
0 0 1 Fatigue lamp 9 2 1 5 1 2 3 4 5
1 9 1 Normal spark 10 3 2 1 5 2 3 4 5
2 A 1 High power spark 11 3 2 1 5 2 3 4 5
3 8 1 Combined spark 12 4 3 2 1 5 2 3 4
4 F 1 Oscillation spark
5 C 1 Cleaning spark
6 0 1
7 0 1
8 0 1
9 0 1
1:Menu
4:Print
9:Init 10:Submenu 
```

```txt
2016.04.10 19:30
B. 19:30 
```

(Note) The FIGURE 11.13 shows an input example when the emission unit is provided with low-pressure-spark HPSG-300 and high-pressure-spark HVS. When the emission unit is changed, the source code is also changed. Do not change it because it has been set upon shipment from our factory. 

neose basic MAT in algmax yisjatic .M.11 3627 

As a component, and a total of the largest one's velocity, the power of the external work is not to be driven by the best time since 1973. 

11.7 TAN (Total No. of Emission Times) Clear
at time date and new schedule must be added to the main screen (8:56)
When selected in the Maintenance Sub-menu, the TAN Clear screen appears.
TAN: Total No. of emission times. Cleared when the condensing lens of the
oisin or emission stand is replaced or reproduced.
When a long time is expected if obtained it would be used.
When it may be cleared, press Y. 

TAN displayed on the lower right part of the Analytical Mode screen is set to 0 (Zero). 

(Note) Returns from 9999 to 0. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-09-30/7aa37dce-54b0-4cc7-9d58-d88f5247b0db/ceb64ffcf5f394c5d2749830f36f262194cd7d2d1182694ce5041a6716cead98.jpg)



FIGURE 11.14: Display Example of TAN Clear Screen


## 11.8 Temperature, Voltage and Vacuum Degree Display

The vacuum degree, voltage and temperature inside the spectrometer are displayed. It is normal when a needle is within a green range. 