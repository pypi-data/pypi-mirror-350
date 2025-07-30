English description follows Japanese.

## 概要

**js\_liner** は、JavaScript のコードを「正常動作を保ったまま」ワンライナー（1行）に変換する Python ライブラリです。
他の同種ツールに比べ、信頼性とシンプルさを両立しており、煩雑な設定や冗長な機能を省き、純粋に「コードを1行にする」ことに特化しています。

## 用途
- なんとなくコードをギュッと1行にして気分を変えたいとき
- javascriptが1行じゃないと動かない環境

---

## 特徴

* ✅ JavaScript コードを動作・機能を損なわず 1 行に変換
* ✅ 複雑な関数定義や入れ子構造も対応
* ✅ シンプルなインターフェースで即使用可能
* ✅ 他ツールと比べて安定動作
* 🚫 過剰な圧縮や難読化は行わない
* ☕ なんとなく気軽に使える

---

## 使用例

```python
import js_liner

script = """
function add(
	a,	// comment
	b
){
	return a + b;
}

console.log(add(7, 1));
"""

result = js_liner(script)
print(result)	# -> function add(a,b){return a + b;}console.log(add(7, 1));
```

---

## 注意点

* 現バージョンでは、**コメントが `//` の後にスペースが無い場合、正しく動作しません。**

  * ✅ `// comment` ← OK
  * ❌ `//comment` ← NG
* コメントの扱いは今後のバージョンで改善予定です。

---

## インストール

```bash
pip install js-liner
```

---

## Overview

**js\_liner** is a Python library that converts JavaScript code into a *single line* format, while **preserving its original behavior**.
Unlike other similar tools that are often buggy or overloaded with features, this tool is minimal, reliable, and easy to use — focusing solely on converting code into a working one-liner.

## Use Cases
- When you just want to crunch your code into a single line for a change of pace
- For environments where JavaScript must run as a one-liner

---

## Features

* ✅ Converts JavaScript code into a single line without breaking functionality
* ✅ Supports nested structures and complex functions
* ✅ Easy-to-use interface — usable right away
* ✅ More stable than many alternatives
* 🚫 No minification or obfuscation
* ☕ Designed for casual and practical use

---

## Example Usage

```python
import js_liner

script = """
function add(
	a,	// comment
	b
){
	return a + b;
}

console.log(add(7, 1));
"""

result = js_liner(script)
print(result)	# -> function add(a,b){return a + b;}console.log(add(7, 1));
```

---

## Caveats

* In the current version, **comments without a space after `//` may cause issues.**

  * ✅ `// comment` ← OK
  * ❌ `//comment` ← NG
* Comment handling is planned to improve in future versions.

---

## Installation

```bash
pip install js-liner
```
