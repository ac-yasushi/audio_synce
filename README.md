# audio_synce
やりたいこと

+ 波形から音声を合成する関数の制作。
+ 音波の録音からwavファイル形式に持ってくる。
+ wavファイルを周波数特性に変換して波形合成
+ 最初の関数から音を作成
+ 周波数特性から音程を判断して出力

実装形式

1. 録音→FFT→波形クラス
2. 波形→音声、波形→音程出力クラス
3. 1,2をモジュール化してプログラム作成
