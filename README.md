<div align="center">

  <h1>Tracking Activities</h1>

  <p>
    A program to monitor children's computer usage
  </p>

<!-- Badges -->
<p>
  <a href="https://github.com/DuckyMomo20012/tracking-activities/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/DuckyMomo20012/tracking-activities" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/DuckyMomo20012/tracking-activities" alt="last update" />
  </a>
  <a href="https://github.com/DuckyMomo20012/tracking-activities/network/members">
    <img src="https://img.shields.io/github/forks/DuckyMomo20012/tracking-activities" alt="forks" />
  </a>
  <a href="https://github.com/DuckyMomo20012/tracking-activities/stargazers">
    <img src="https://img.shields.io/github/stars/DuckyMomo20012/tracking-activities" alt="stars" />
  </a>
  <a href="https://github.com/DuckyMomo20012/tracking-activities/issues/">
    <img src="https://img.shields.io/github/issues/DuckyMomo20012/tracking-activities" alt="open issues" />
  </a>
  <a href="https://github.com/DuckyMomo20012/tracking-activities/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/DuckyMomo20012/tracking-activities.svg" alt="license" />
  </a>
</p>

<h4>
    <a href="https://github.com/DuckyMomo20012/tracking-activities/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/DuckyMomo20012/tracking-activities">Documentation</a>
  <span> · </span>
    <a href="https://github.com/DuckyMomo20012/tracking-activities/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/DuckyMomo20012/tracking-activities/issues/">Request Feature</a>
  </h4>
</div>

<br />

<!-- Table of Contents -->

# :notebook_with_decorative_cover: Table of Contents

- [About the Project](#star2-about-the-project)
  - [Tech Stack](#space_invader-tech-stack)
  - [Features](#dart-features)
- [Getting Started](#toolbox-getting-started)
  - [Prerequisites](#bangbang-prerequisites)
  - [Run Locally](#running-run-locally)
- [Usage](#eyes-usage)
  - [Children Program](#baby-children-program)
  - [Parent Program](#adult-parent-program)
- [Contributing](#wave-contributing)
  - [Code of Conduct](#scroll-code-of-conduct)
- [FAQ](#grey_question-faq)
- [License](#warning-license)
- [Contact](#handshake-contact)
- [Acknowledgements](#gem-acknowledgements)

<!-- About the Project -->

## :star2: About the Project

<!-- TechStack -->

### :space_invader: Tech Stack

<details>
  <summary>Client</summary>
  <ul>
    <li>Python</li>
    <li>C#</li>
  </ul>
</details>

<!-- Features -->

### :dart: Features

> WARNING: This doc is updated after long time unmaintained, so maybe there is
> some parts incorrect.

- **Children program:**

  - Run in the background.
  - Capture background, key loggers.
  - Manage on-screen time for children (force computer shutdown).

- **Parent program:**
  - Manage captured pictures and send them to the Google Drive folder
    via APIs.
  - Require user to create a folder called: "**TrackingActivities**" at the root of
    Google Drive.

<!-- Getting Started -->

## :toolbox: Getting Started

<!-- Prerequisites -->

### :bangbang: Prerequisites

- Python: `>= 3.9`.

- Operating system: `Windows`.

  > **NOTE**: This app only supports `Windows`. Currently not supporting `Linux` and `macOS`.

<!-- Run Locally -->

### :running: Run Locally

Clone the project:

```console
git clone https://github.com/DuckyMomo20012/tracking-activities.git
```

Go to the project directory:

```console
cd tracking-activities
```

Change directory to `parent_program` folder:

```console
cd src/parent_program
```

Create virtual environment:

```console
python -m venv .venv
```

Activate environment:

```console
.venv\Scripts\activate
```

<!-- Usage -->

## :eyes: Usage

> WARNING: This doc is updated after long time unmaintained, so maybe there is
> some parts incorrect.

### :baby: Children Program:

> **Parent program must run first to prepare needed files!**

- Setup autostart:

  - Create **shortcut** for children's program

    ![shortcut](https://i.imgur.com/qVDBxnf.png)

  - Copy shortcut to directory: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`

    ![copy directory](https://i.imgur.com/bYxXEG5.png)

- Login into the children's program:

  - Parent password: `1234`
  - Children password: `4321`

### :adult: Parent Program:

> NOTE: **Parent program must run first to prepare needed files!**

- Run parent program (require python and requirement libs is installed):

  ```console
  winRun.bat
  ```

- The parent program will prompt you to trust the program "TrackingActivities",
  please **accept it**.

- Parent program will require a password every time it runs, if you don't have
  password, parent program will create file: `password.txt` (of parent program)

  - Only when file `password.txt` is closed, then data is uploaded to Google
    Drive folder.

    > NOTE: User have to use **Notepad** to edit `password.txt` or other files.

  > If you forget the password, then go to the Google Drive folder
  > (TrackingActivities) and delete the file `password.txt`.

- After login, login information is saved automatically, so users don't have to
  authenticate next time.

- Parent program features:

  - **View history**: Parents can view **captured pictures** and **key loggers**
    on both Google Drive and `Downloads` folder (created in children's program).

  - **Delete "Downloads" folder**: The parent can delete the entire `Downloads`
    to save storage.

  - **Logout**: The user can log out and use another account.

  - **Exit**: Exit Parent program.

  - **Edit activate.txt**: `activate.txt` timestamps, which allows children to
    use computer.

    - Only when file `activate.txt` is closed, then data is uploaded to Google
      Drive folder.

    - Timestamps symbol (for `activate.txt`):

      - `F` (from time): Start time
      - `T` (to time): End time
      - `S` (sum time):

        - Total time allowed.
        - Constraints: `0 < S <= T - F`.
        - When `S` time is run out, even `T` is not run out -> Computer still
          shut down.

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

<!-- Contributing -->

## :wave: Contributing

<a href="https://github.com/DuckyMomo20012/tracking-activities/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=DuckyMomo20012/tracking-activities" />
</a>

Contributions are always welcome!

<!-- Code of Conduct -->

### :scroll: Code of Conduct

Please read the [Code of Conduct](https://github.com/DuckyMomo20012/tracking-activities/blob/main/CODE_OF_CONDUCT.md).

<!-- FAQ -->

## :grey_question: FAQ

- Is this project still maintained?

  - No, but I will only update documentation.

- Are you planning to support Linux and macOS in the future?

  - No, we are not adding support for Linux and macOS any time soon (and most
    likely never).

<!-- License -->

## :warning: License

Distributed under MIT license. See
[LICENSE](https://github.com/DuckyMomo20012/tracking-activities/blob/main/LICENSE)
for more information.

<!-- Contact -->

## :handshake: Contact

Duong Vinh - [@duckymomo20012](https://twitter.com/duckymomo20012) - tienvinh.duong4@gmail.com

Project Link: [https://github.com/DuckyMomo20012/tracking-activities](https://github.com/DuckyMomo20012/tracking-activities).

<!-- Acknowledgments -->

## :gem: Acknowledgements

Here are useful resources and libraries that we have used in our projects:

- [Awesome Readme Template](https://github.com/Louis3797/awesome-readme-template):
  A detailed template to bootstrap your README file quickly.
