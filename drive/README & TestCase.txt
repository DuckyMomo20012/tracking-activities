- Nếu chưa có python thì chạy file "installPython.bat"
- Để chạy chương trình thì chạy file "parent_program.py"
- Để uninstall python thì chạy file "uninstallPython.bat"
FORMAT:
F<h1:m1> T<h2:m2>
or
F<h1:m1> T<h2:m2>S<mS>
or
F<h1:m1> T<h2:m2>|D<mD> I<mI>|S<mS>
FORMULA:
0 <= I < S
0 < D <= S
0 < D + I <= S
0 < S <= T - F
=> 0 < D + I <= S <= T - F
OPTIMAL:
IF D == "" AND I == "" AND S == T - F: 
Optimize from: F07:30 T09:30 D60 I0 S60 -> to: F07:30 T09:30 S60
IF D != "" AND I != "" AND D == S AND I == 0:
Optimize from: F07:30 T09:30 S120 -> to: F07:30 T09:30
VALID EXAMPLE:
F06:00 T06:45
F07:30 T11:00 D60 I20 S150
F14:00 T17:50 D40 I10 S120
F18:00 T19:30 S60
F19:31 T21:30 S90
ERROR:
+Format ERROR:
asdgasdg (Totally wrong)
F7:30 T06:30 (Missing one number)
F007:30 T06:30 (one number redundant)
F27:30 T06:30 (27 hours is invalid 😛)
F07:61 T06:30 (61 minutes is invalid)
A14:00 E17:50 J4 M10 Z120 (Wrong format!!!)
F-7:30 T06:30 ("-" is not valid)
+Logic ERROR:
F07:30 T06:30 (T < F)->ERROR
F07:30 T09:30 D03 I58 S60 (D + I > S)->ERROR
F07:30 T09:30 D61 I0 S60 (D > S)->ERROR
F07:30 T09:30 D0 I0 S60 (D == 0)->ERROR
F07:30 T09:30 D1 I61 S60 (I > S or D + I > S)->ERROR
F07:30 T09:30 S121 (S > T - F)->ERROR
+Conflict ERROR (F time this line must "BIGGER" than T time previous time):
F06:00 T06:45
F06:00 T06:45
(Same time)->ERROR
or:
F06:00 T06:45
F06:45 T06:52
(F line 1 equal T line 2)->ERROR
or:
F06:00 T06:45
F06:30 T07:30
(F line 1 smaller than T line 2)->ERROR