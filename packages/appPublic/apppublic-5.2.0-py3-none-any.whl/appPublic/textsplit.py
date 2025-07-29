import re

def split_english_sentences(text):
    # 替换可能连在一起的句点后无空格情况，统一成 .<space>
    text = re.sub(r'([a-zA-Z])\.([A-Z])', r'\1. \2', text)

    # 不分割缩写（如 "Dr.", "U.S.A."）
    abbreviations = r"(Mr|Mrs|Ms|Dr|St|Jr|Sr|vs|i\.e|e\.g|U\.S\.A|U\.K)\."
    text = re.sub(abbreviations, lambda m: m.group(0).replace('.', '<DOT>'), text)

    # 用正则分割句子
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    # 还原缩写中的 <DOT>
    sentences = [s.replace('<DOT>', '.') for s in sentences if s.strip()]
    return sentences

def split_engish1_sentences(text):
    # 匹配以 '. ', '? ', '! ' 结尾的英文句子，保留分隔符
    sentence_endings = re.compile(r'(?<=[.!?]) +')
    sentences = sentence_endings.split(text.strip())
    return [s.strip() for s in sentences if s.strip()]

def split_text_with_dialog_preserved(text):
	# 正则匹配中英文引号对话
	text = ' '.join(text.split('\n'))
	dialog_pattern = r'([“"](.*?)[”"])'
	parts = []
	last_idx = 0

	# 先提取所有对话，保证不被切割
	for match in re.finditer(dialog_pattern, text, flags=re.DOTALL):
		start, end = match.span()

		# 前面的非对话部分按句子分割
		non_dialog = text[last_idx:start]
		sentences = re.findall(r'[^。！？!?]*[。！？!?]', non_dialog, re.MULTILINE)
		for s in sentences:
			txt = s.strip()
			if txt:
				subsentences = split_engish_sentences(txt)
				parts.extend([s.strip() for s in sentences if s.strip()])
				
		# parts.extend([s.strip() for s in sentences if s.strip()])

		# 加入整个对话
		parts.append(match.group(1).strip())

		last_idx = end

	# 处理最后一个对话之后的部分
	remaining = text[last_idx:]
	sentences = re.findall(r'[^。！？!?]*[。！？!?]', remaining, re.MULTILINE)
	parts.extend([s.strip() for s in sentences if s.strip()])

	return parts

