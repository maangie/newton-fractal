# Newton Fractal（ニュートン法フラクタル）

概要

このリポジトリは、ニュートン法（Newton–Raphson 法）を複素平面上で可視化したフラクタル生成プログラムです。
任意の多項式を与えると、各点がどの根に収束するかを色分けして描画します。
複素平面上の美しい境界構造（フラクタル）を楽しむことができます。

---

特徴
	•	Python（NumPy + Matplotlib + Numba）で実装
	•	多項式の係数を簡単に変更可能
	•	高速化のため JIT コンパイル（Numba）を使用
	•	簡単なパラメータ編集で、別のフラクタルも生成可能

---

使用方法

1. 環境セットアップ

このプロジェクトは uv を利用しています。
まだインストールしていない場合は：

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. 依存関係のインストール

```shell
uv sync
```

もしくは個別に：

```
uv add numpy matplotlib numba
```

3. 実行

```
uv run python main.py
```

実行後、ウィンドウにカラフルなニュートン法フラクタルが表示されます。

---

パラメータ設定（`main.py` 冒頭部分）

```python
COEFFS = np.array([1.0, 0.0, 0.0, -1.0])  # z^3 - 1
MAX_ITER = 40
EPS = 1e-8
XMIN, XMAX = -1.5, 1.5
YMIN, YMAX = -1.5, 1.5
RES = 900
```

| 変数 | 説明 |
|------|------|
| COEFFS | 多項式の係数（高次から順） |
| MAX_ITER | ニュートン法の最大反復回数 |
| EPS | 収束判定のしきい値 |
| XMIN, XMAX, YMIN, YMAX | 描画範囲 |
| RES | 出力画像の解像度 |

---

例：他の多項式で試す

| 式 | COEFFS 設定例 |
|----|----------------|
| z⁴ − 1 | `[1, 0, 0, 0, -1]` |
| z⁵ − z + 1 | `[1, 0, 0, 0, -1, 1]` |
| z³ − 2z + 2 | `[1, 0, -2, 2]` |

---

スクリーンショット例

（ここに画像を追加予定）

---

ライセンス

このプロジェクトは MIT License で公開されています。

---

作者

maangie
GitHub: https://github.com/maangie
