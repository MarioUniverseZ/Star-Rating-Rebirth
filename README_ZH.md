# SR-Rebirth-GUI
[English][README.md]
這是從[sunnyxxy的repo](https://github.com/sunnyxxy/Star-Rating-Rebirth) fork出的GUI版本 (演算法版本使用2025-03-04)<br>
(UI版面參考了[Mapset Verifier](https://github.com/Naxesss/MapsetVerifier)和[Huggy的Spread Wizard](https://github.com/sinanates17/Huggeds-Mania-Spread-Wizard))
![image](https://github.com/user-attachments/assets/f44d8f69-26ad-42ee-afe9-509217eb5ef0)

## 注意
- 初次使用時，會先要求提供osu!的路徑

## 開發 (限Windows)
1. Clone repo
    ```
    git clone https://github.com/MarioUniverseZ/SR-Rebirth-GUI.git
    ```
2. 安裝[Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
3. 把`TorusNotched-Regular.ttf` 放到`Window/font` (我不提供字型檔)
4. 安裝專案依賴項
    ```
    poetry install
    ```
5. 執行/偵錯`main.py`

## 貢獻
[Issue](https://github.com/MarioUniverseZ/SR-Rebirth-GUI/issues) | [PR](https://github.com/MarioUniverseZ/SR-Rebirth-GUI/pulls)

## GUI流程圖
![image](https://github.com/user-attachments/assets/8106c9dc-9f01-4c05-b039-075be128466b)

## 未來規劃
- [ ] 修正問題
- [ ] 更潮的外觀 (可能會用PyQt重寫)
- [x] 一次計算多個圖
- [x] 切換DT或HT
- [x] 遷移pip環境至poetry