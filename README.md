# DAQino
DAQino is a data aquisition system made using Arduino and Python. The system is capable of:
- aquire analog signal from 392 S/s (2,55 ms) up to 6,6 kS/s (150 us) from one port at a time.
- control PWM from one port at a time.
- do step response test.
- run script to automate tests.

![Not posissible to load image.](https://github.com/c-mmonteiro/DAQino/blob/main/Capturar.PNG)

All the samples measured will be shown at the graphic and it can be save on a log file, if configured.

-----------------------------
**HOW TO USE:**
You can run the .exe or the Python Script.

Run .exe:

1. Download DAQino.exe, ifc.png and folder DAQ
2. Program Arduino with the firmware on DAQ folder.
3. Run DAQino.exe

Run Script:

1. Download all files.
2. Program Arduino with the firmware on DAQ folder.
3. Install all requirements.

    Run: pip install -r requirements.txt

4. Run main.py file.
------------------------------
**SCRIPT FILE:**

The script will use the CSV standard, that is, it will divide your information with the ‘;’ character. In the first line it will have the title of each of the columns (which will be ignored by the program) following the sequence shown below. The subsequent lines will be the values ​​to be executed.

-	Teste Number (will be the end of the file name)
-	Test Type 
    *    ‘m’ for measure
    *	‘d’ for step response
    *	‘p’ for PWM drive
    *	‘e’ for waiting time
-	AD Port
-	Aquisition Period (in us from 150 to 2550 with step of 10 us)
-	Number of Samples (0 a 767)
-	PWM Port
-	Duty Cycle before step (used only on step response, 0 to 255)
-	Waiting time before step (s)
-	Duty Cycle after step (0 a 255)
-	Step Dalay (in samples, from 0 to 255)
-	Save data (0 oe 1).

Example:

Num;Type;AD Port;Period;Samples;PWM Port;DC pre;Waiting Time;DC;Delay;Save<br/>
1;m;0;150;750;6;0;0;0;0;1<br/>
2;p;0;150;750;6;0;0;150;0;0<br/>
3;e;0;150;750;6;0;3;0;0;0<br/>
4;d;0;150;750;6;50;10;200;0;1<br/>
5;a;0;150;750;6;50;1;200;0;1<br/>
6;d;0;150;750;6;50;1;150;100;1<br/>

------------------------------
**LOG FILE:**

The measurement log files will be a list with each value on one line. The sequence of this list follows the sequence shown below.

Period<br/>
sample_number<br/>
Type (Measurement (M) or step response (D))<br/>
Initial PWM(Duty Cycle)<br/>
Final PWM(Duty Cycle)<br/>
Sample 0<br/>
Sample 1<br/>
....







