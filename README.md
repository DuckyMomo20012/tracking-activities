# Tracking Activities

A program to monitor children's computer usage.

> WARNING: This doc is updated after long time unmaintained, so maybe there is
> some parts incorrect.

## Tech stacks:

<p align="center">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="python" height="48" width="48" />
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/csharp/csharp-original.svg" alt="csharp" height="48" width="48" />
</p>

## Features:

- Children program:

  - Run in the background
  - Capture background, key loggers
  - Manage on-screen time for children (force computer shutdown)

- Parent program:
  - Manage captured pictures and send them to the Google Drive folder
    via APIs.
  - Require user to create a folder called: "**TrackingActivities**" at the root of
    Google Drive.

## Installation:

> Tested on python 3.9.6

1. Change directory:

```console
cd src/parent_program
```

2. Install environment:

```console
python -m venv .venv
```

3. Activate environment:

```console
.venv\Scripts\activate
```

4. Install libs:

```console
pip install -r requirements.txt
```

---

## How to use:

### Children Program:

> **Parent program must run first to prepare needed files!**

- Setup autostart:

  - Create **shortcut** for children's program

  ![](https://i.imgur.com/qVDBxnf.png)

  - Copy shortcut to directory: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`

  ![](https://i.imgur.com/bYxXEG5.png)

- Login into the children's program:

  - Parent password: 1234
  - Children password: 4321

### Parent Program:

> **Parent program must run first to prepare needed files!**

- Run parent program (require python and requirement libs is installed):

```console
winRun.bat
```

- The parent program will prompt you to trust the program "TrackingActivities", **accept it**.

- Parent program will require a password every time it runs, if you don't have
  password, parent program will create file: `password.txt` (of parent program)
  - Only when file `password.txt` is closed, then data is uploaded to Google Drive
    folder.

> User have to use **Notepad** to edit `password.txt` or other files.

> If you forget the password, then go to the Google Drive folder (TrackingActivities) and delete the file
> `password.txt`

- After login, login information is saved automatically, so users don't have to authenticate next
  time.

- Parent program features:

  - **View history**: Parents can view **captured pictures** and **key loggers** on both Google Drive
    and `Downloads` folder (created in children's program)

  - **Delete "Downloads" folder**: The parent can delete the entire `Downloads` to save
    storage.

  - **Logout**: The user can log out and use another account.

  - **Exit**: Exit Parent program.

  - **Edit activate.txt**: `activate.txt` timestamps, which allows children to use
    computer.

    - Only when file `activate.txt` is closed, then data is uploaded to Google Drive
      folder.

    - Timestamps symbol (for `activate.txt`):

      - `F` (from time): Start time
      - `T` (to time): End time
      - `S` (sum time):

        - Total time allowed.
        - Constraints: `0 < S <= T - F`.
        - When `S` time is run out, even `T` is not run out -> Computer still shut
          down.

      - `D` (duration time): total time till interrupt time (`I`).
      - `I` (interrupt time): interrupt time till duration time (`D`)

    - Valid timestamps:

      ```
          F06:00 T06:45
          F07:30 T11:00 D60 I20 S150
          F14:00 T17:50 D40 I10 S120
          F18:00 T19:30 S60
          F19:31 T21:30 S90
      ```

    - Constraints in brief:

      ```
        0 <= I < S
        0 < D <= S
        0 < D + I <= S
        0 < S <= T - F
        => 0 < D + I <= S <= T - F
      ```

    - If the user inputs the wrong timestamp, the user will be warned and retype.

    - Timestamps will be automatically optimized step by steps:

      1. Check format
      2. Sort lines
      3. Remove duplicate and blank lines
      4. Remove end line
      5. Check conflict, check logic

    <details>
      <summary>More timestamps examples</summary>

    ```
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
      - Format ERROR:
        asdgasdg (Totally wrong)
        F7:30 T06:30 (Missing one number)
        F007:30 T06:30 (one number redundant)
        F27:30 T06:30 (27 hours is invalid 😛)
        F07:61 T06:30 (61 minutes is invalid)
        A14:00 E17:50 J4 M10 Z120 (Wrong format!!!)
        F-7:30 T06:30 ("-" is not valid)
      - Logic ERROR:
        F07:30 T06:30 (T < F) -> ERROR
        F07:30 T09:30 D03 I58 S60 (D + I > S) -> ERROR
        F07:30 T09:30 D61 I0 S60 (D > S) -> ERROR
        F07:30 T09:30 D0 I0 S60 (D == 0) -> ERROR
        F07:30 T09:30 D1 I61 S60 (I > S or D + I > S) -> ERROR
        F07:30 T09:30 S121 (S > T - F) -> ERROR
      - Conflict ERROR (F time this line must "BIGGER" than T time previous time):
        F06:00 T06:45
        F06:00 T06:45
        (Same time) -> ERROR
        or:
        F06:00 T06:45
        F06:45 T06:52
        (F line 1 equal T line 2) -> ERROR
        or:
        F06:00 T06:45
        F06:30 T07:30
        (F line 1 smaller than T line 2) -> ERROR
    ```

    </details>
