# SR-Rebirth-GUI
[中文](README_ZH.md)<br>
forked from [sunnyxxy's repo](https://github.com/sunnyxxy/Star-Rating-Rebirth)(2025-03-04 version)<br>
(Yes, this UI design comes from [Mapset Verifier](https://github.com/Naxesss/MapsetVerifier) and [Huggy's Spread Wizard](https://github.com/sinanates17/Huggeds-Mania-Spread-Wizard))
![image](https://github.com/user-attachments/assets/f44d8f69-26ad-42ee-afe9-509217eb5ef0)

## Notes
- You will be asked for your beatmap directory for the first time when you run the program (see [GUI Flowchart](#gui-flowchart) below)

## Development(Windows Only)
1. Clone this repo
    ```
    git clone --branch GUI-Tkinter https://github.com/MarioUniverseZ/SR-Rebirth-GUI.git
    ```
2. Install [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
3. Get `TorusNotched-Regular.ttf` and put it in `Window/font` (I don't provide one though)
4. Install dependencies
    ```
    poetry install
    ```
5. run/debug main.py

## Contribute
[Issue](https://github.com/MarioUniverseZ/SR-Rebirth-GUI/issues) | [PR](https://github.com/MarioUniverseZ/SR-Rebirth-GUI/pulls)

## GUI Flowchart
![image](/img/gui-flowchart.png)

## Future Plan
- [ ] Fix issues
- [ ] Better decoration (maybe rewrite with PyQt)
- [x] Multi-calculate SR at once
- [x] Toggle Double Time or Half Time
- [x] Migrate pip environment to poetry