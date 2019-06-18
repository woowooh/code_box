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
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
    <title></title>
    <style>
        #a {{
            width: 50%;
            float: left;            
            overflow-x: scroll;
        }}
        #b {{
            width: 50%;
            padding:0;
            position:relative;
            float: left;            
            overflow-x: scroll;
        }}
        .warn {{
            border-radius: 2px;
            border: 2px solid red;
        }}
        body {{
            font-family: menlo,monospace, Tahoma,"微软雅黑","幼圆";
            font-size: 1.7vh;   
            font-weight: bold;  
            color: rgb(40, 41, 35); 
            background-color: #f6f6f6;
        }}
        .key {{
            color: rgb(163, 0, 142);
        }}
        .value {{
            color: rgb(0, 191, 77);
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
                l.append((k, 0, n + 1))
                self._recursive_dic(v, n + 1, l)
            elif isinstance(v, list):
                l.append((k, 0, n + 1)) 
                self._recursive_list(v, n + 1, l)
            else:
                l.append((k, v, 1, n + 1))      
        l.append((self.DIC_END, n))

    def _recursive_list(self, lst, n, l):
        l.append((self.LST_START, n))
        for v in lst:
            if isinstance(v, dict):         
                self._recursive_dic(v, n + 1, l)
            elif isinstance(v, list):               
                self._recursive_list(v, n + 1, l)
            else:
                l.append((v, 1, n + 1))
        l.append((self.LST_END, n))

    def _get_intersection(self):
        l1_intersection = []
        l2_intersection = []        
        for i in self.l1:
            if i not in self.l2:
                l1_intersection.append(i)
        for i in self.l2:
            if i not in self.l1:
                l2_intersection.append(i)       
        return l1_intersection, l2_intersection     

    def _HTML_from_elements(self, l, target_l):     
        dic_template = '{indent}<span class="key {cls_name}">"{key}"</span>:<span class="value {cls_name}">{value}</span>'
        lst_template = '{indent}<span class="{cls_name}">{value}</span>'
        m = self._init_HTML_space(15)
        r = ""
        for i, item in enumerate(l):    
            cls_name = ""
            if len(item) > 3:
                key = item[0]
                value = item[1]
                n = item[-1]
                if item in target_l:
                    cls_name = "warn"
                if isinstance(value, str):
                    value = '"{}"'.format(value)
                r += dic_template.format(indent=m[n], key=key, value=value, cls_name=cls_name)          
                index = i + 1
                if (index < len(l) and (l[index][0] not in self.ph_r)):
                    r += ","
                r += "<br>" 
            else:
                char = item[0]      
                typ = item[1]
                n = item[-1]                
                if char in self.ph_l:
                    if (len(r) > 0) and (r[-8] == ":"):                                             
                        r += char + "<br>"
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
                    if isinstance(char, str):
                        char = '"{}"'.format(char)                              
                    if (typ == 0):
                        char += ":"
                        cls_name = "key " + cls_name
                    else:
                        cls_name = "value " + cls_name
                    index = i + 1                   
                    r += lst_template.format(indent=m[n], value=char, cls_name=cls_name)                                            
                    if (typ == 1) and (l[index][0] not in self.ph_r):
                        r += ",<br>"
                    elif (index < len(l) and (l[index][0] in self.ph_r)):
                        r += "<br>"                                 
        return r

    def create_report(self, filename):
        r1 = self._HTML_from_elements(self.l1, self.intersection1)
        r2 = self._HTML_from_elements(self.l2, self.intersection2)  
        r = self.report_template.format(result1=r1, result2=r2)
        with open(filename + ".html", 'w') as f:
            f.write(r)
