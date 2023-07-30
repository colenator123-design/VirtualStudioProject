七月專題進度報告

1.已完成眼睛位置和深度檢測(使用facemash)，並藉由web socket導入unity完成鏡頭互動，隨者眼睛位置的變化，unity場景的車子會隨著移動改變。
2.在unity asset store 找相關的asset(Eg. 太空、沙漠，物件、特效、背景、人物等)，參考來源在文件中。

面臨到的挑戰:
1.除了檢測功能外，我們嘗試想要偵測眼睛轉動的位置，讓場景可以有隨著頭轉動而改變的功能，但在取得角度變化這部分遇到困難，我們有查詢相關的數學公式，但結果不是角度變化值，而是微分後的角度變化值，希望老師可以給予建議和方法。
以下是我們查詢到的方法和數學公式

get the angle of face in facemesh in python 

https://github.com/google/mediapipe/issues/1912#issuecomment-824189260

Euler Angles

https://mathworld.wolfram.com/EulerAngles.html

