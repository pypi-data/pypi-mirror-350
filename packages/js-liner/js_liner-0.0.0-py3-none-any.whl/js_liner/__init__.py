# javascript 1行化 [js-liner]

import re
import sys

# 括弧内の改行を除去
def rm_closed_newline(joined_code):
	s_ls = list(joined_code)	# 1文字ずつに区切る
	depth = 0
	ret_ls = []
	for s in s_ls:
		if s == "\n" and depth > 0: s = ""
		ret_ls.append(s)
		if s == "(": depth += 1
		if s == ")": depth -= 1
	return "".join(ret_ls)

# javascriptをワンライナー化する関数
def js_to_oneliner(js_code):
	# コメントの削除（// から行末まで）
	code_no_comments = re.sub(r'// .*', '', js_code)
	# 行のストリップ（前後の空白・タブを削除）
	lines = [line.strip() for line in code_no_comments.splitlines() if line.strip()]
	# 括弧内の改行を除去
	joined_code = '\n'.join(lines)
	joined_code = rm_closed_newline(joined_code)
	# 各行にセミコロンを追加
	lines = joined_code.splitlines()
	lines = [line + ';' for line in lines]
	js_code = "".join(lines)	# 改行を消す
	# セミコロンの特殊ルール (重複除去など)
	js_code = js_code.replace(";;", ";")
	js_code = js_code.replace("};", "}")
	js_code = js_code.replace("{;", "{")
	return js_code

# モジュールと関数の同一視
sys.modules[__name__] = js_to_oneliner
