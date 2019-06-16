import json


class JSONComparer(object):
	def __init__(self):
		self.DIC_START = "{"
		self.DIC_END = "}"
		self.LST_START = "["
		self.LST_END = "]"
		self.l1 = []
		self.l2 = []	
		self.intersection1 = []
		self.intersection2 = []
		self.ph_l = ["{", "(", "["]
		self.ph_r = ["}", ")",  "]"]
		self.report_template = """
<!DOCTYPE html>
<html>
<head>
	<title></title>
	<style>
		#a {{
			width: 50%;
			float: left;
		}}
		#b {{
			width: 50%;
			padding:0;
			position:relative;
			float: left;
		}}
		.warn {{
			background-color: rgb(232, 36, 107);
		}}
	</style>
</head>
<body>
<div id="a">
{result1}
</div>
<div id="b">
{result2}
</div>
</body>
</html>
		"""	

	def _init_HTML_space(self, n=15):
		HTML_space_map = {}
		for i in range(n):
			HTML_space_map[i] = "&ensp;&ensp;&ensp;" * i	
		return HTML_space_map

	def compare(self, JSON1, JSON2):
		try:
			j1 = json.loads(JSON1)
			j2 = json.loads(JSON2)
		except:
			print("JSON loads failed")
			return 
		self._recursive_dic(j1, 0, self.l1)
		self._recursive_dic(j2, 0, self.l2)
		self.intersection1, self.intersection2 = self._get_intersection()
		for i in self.intersection1:
			k = i[0]
			if (k in self.ph_l) or (k in self.ph_r):
				continue
			print("l1 missing ", i)
		for i in self.intersection2:
			k = i[0]
			if (k in self.ph_l) or (k in self.ph_r):
				continue
			print("l2 missing", i)

	def _recursive_dic(self, dic, n, l):
		l.append((self.DIC_START, n))
		for k, v in dic.items():
			if isinstance(v, dict):
				l.append((k, n + 1))
				self._recursive_dic(v, n + 1, l)
			elif isinstance(v, list):
				l.append((k, n + 1))	
				self._recursive_list(v, n + 1, l)
			else:
				l.append((k, v, n + 1))		
		l.append((self.DIC_END, n))

	def _recursive_list(self, lst, n, l):
		l.append((self.LST_START, n))
		for v in lst:
			if isinstance(v, dict):			
				self._recursive_dic(v, n + 1, l)
			elif isinstance(v, list):				
				self._recursive_list(v, n + 1, l)
			else:
				l.append((v, n + 1))
		l.append((self.LST_END, n))

	def _get_intersection(self):
		l1_copy = self.l1.copy()
		l2_copy = self.l2.copy()
		common_list = []
		for i in self.l1:
			if i in self.l2:
				common_list.append(i)
		for i in common_list:
			l1_copy.remove(i)
			l2_copy.remove(i)
		return l1_copy, l2_copy		

	def _HTML_from_elements(self, l, target_l):		
		dic_template = '{indent}<span class="{cls_name}">"{key}"</span>:<span class="{cls_name}">"{value}"</span>'
		lst_template = '{indent}<span class="{cls_name}">"{value}</span>"'
		m = self._init_HTML_space(15)
		r = ""
		for i, item in enumerate(l):	
			cls_name = ""
			if len(item) > 2:
				key = item[0]
				value = item[1]
				n = item[-1]
				if item in target_l:
					cls_name = "warn"
				r += dic_template.format(indent=m[n], key=key, value=value, cls_name=cls_name)			
				index = i + 1
				if (index < len(l) and (l[index][0] not in self.ph_r)):
					r += ","
				r += "<br>" 
			else:
				char = item[0]		
				n = item[-1]
				if char in self.ph_l:
					if (len(r) > 0) and (r[-5] not in self.ph_l):
						r += ":" + char + "<br>"
					else:
						r += m[n] + char + "<br>"				
				elif char in self.ph_r:
					r += m[n] + char 
					index = i + 1
					if (index < len(l) and (l[index][0] not in self.ph_r)):
						r += ","
					r += "<br>" 				
				else:
					if item in target_l:
						cls_name = "warn"								
					r += lst_template.format(indent=m[n], value=char, cls_name=cls_name)			
					index = i + 1					
					if (index < len(l) and (l[index][0] in self.ph_r)):
						r += "<br>" 				
		return r

	def create_report(self, filename):
		r1 = self._HTML_from_elements(self.l1, self.intersection1)
		r2 = self._HTML_from_elements(self.l2, self.intersection2)	
		r = self.report_template.format(result1=r1, result2=r2)
		with open(filename + ".html", 'w') as f:
			f.write(r)