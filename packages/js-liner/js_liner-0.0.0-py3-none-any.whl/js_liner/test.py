# javascript 1行化 [js-liner]
# 【動作確認 / 使用例】

import sys
import ezpip
js_liner = ezpip.load_develop("js_liner", "../", develop_flag = True)

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
