import json
import uuid


def read_json(p):
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
        return json.loads(c)


def init_space_map():
    space = "&ensp;&ensp;&ensp;"
    m = {}
    for i in range(30):
        m[i] = space * i
    return m


space_map = init_space_map()


def record_recursive_dict(d, storage, level, index):
    if index is None:
        index = 0
    storage.append(("symbol", level, "{", index))
    level += 1
    for k, v in d.items():
        storage.append(("key", level, f"{k}", index))
        if isinstance(v, list):
            record_recursive_list(v, storage, level, index)
        elif isinstance(v, dict):
            record_recursive_dict(v, storage, level, index)
        elif isinstance(v, int):
            storage.append(("value", level, f"{str(v)}", index))
        elif isinstance(v, str):
            storage.append(("value", level, f"'{v}'", index))
    storage.append(("symbol", level - 1, "}", index))


def record_recursive_list(lst, storage, level, index):
    if index is None:
        index = 0
    storage.append(("symbol", level, "[", index))
    level += 1
    for i, e in enumerate(lst):
        if isinstance(e, list):
            record_recursive_list(e, storage, level, f"{index}:{i}")
        elif isinstance(e, dict):
            record_recursive_dict(e, storage, level, f"{index}:{i}")
        elif isinstance(e, int):
            storage.append(("value", level, f"{e}", index))
        elif isinstance(e, str):
            storage.append(("value", level, f"'{e}'", index))
    storage.append(("symbol", level - 1, "]", index))


def get_anti_intersection(set1, set2):
    anti1 = set1 - set2
    anti2 = set2 - set1
    return list(anti1), list(anti2)


def html_styled_diff(line, t1):
    template_key = '{indent}<span class="{cls_name}">"{value}":</span>{br}'
    template_value = '{indent}<span class="{cls_name}">{value}</span>{br}'
    default_left = '{indent}<span onClick="hide(\'{_uuid}\')">+</span><span id="{_uuid}" class="{cls_name}" data-type="object">{value}{br}'
    default_right = '{indent}{value}</span>{br}'
    cls_name = " "
    value = ""
    _uuid = f"a{str(uuid.uuid4())}"
    indent = space_map[line[0]]
    if line[1][0] == "key":
        cls_name = "key"
        template = template_key
    elif line[1][0] == "value":
        cls_name = "value"
        template = template_value
    else:
        cls_name = "default"
        if line[1][2] in ["{", "["]:
            template = default_left
        if line[1][2] in ["}", "]"]:
            template = default_right
    value = line[1][2]
    if line[1] in t1:
        cls_name += " warn"
    br = line[2]
    if "," in br:
        br = f'<span class="default comma">{br.replace("<br>", "")}</span><br>'
    return template.format(**locals())


def html_from_diff(l, anti):
    q = []
    r = []
    prev = None
    next = None
    length_l = len(l)
    for i, e in enumerate(l):
        indent = e[1]
        line = (indent,e, "<br>")
        if e[2] in ["{", "["]:
            if prev and prev[0] == "key":
                line = (0, e, "<br>")
            q.append(e[2])
        else:
            if i + 1 < length_l:
                next = l[i + 1]
                if e[0] == "symbol" and e[2] in ["}", "]"]:
                    if next[0] == "symbol" and next[2] not in ["]", "}"]:
                        if len(q) > 0:
                            line = (indent, e, ",<br>")
                if e[0] == "key":
                    if next[0] == "value":
                        line = (indent, e, "")
                    if next[0] == "symbol":
                        line = (indent, e, "")
                if e[0] == "value":
                    if prev[0] == "key":
                        line = (0, e, "<br>")
                    if next[0] == "value":
                        line = (indent, e, ",<br>")
                    if next[0] == "key":
                        line = (0, e, ",<br>")
        line = html_styled_diff(line, anti)
        r.append(line)
        prev = e
        if e[2] in ["}", "]"]:
            q.pop()
    return "".join(r)


def create_result(r1, r2):
    report_template = """
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
                pappending:0;
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
                font-family: menlo,monospace, Tahoma,"微软雅黑","幼圆";
                font-size: 1.7vh;   
                font-weight: bold;  
                color: rgb(163, 0, 142);
                background-color: #f6f6f6;
            }}
            .value {{
                font-family: menlo,monospace, Tahoma,"微软雅黑","幼圆";
                font-size: 1.7vh;   
                font-weight: bold;  
                color: rgb(0, 191, 77);
                background-color: #f6f6f6;
            }}
            .default {{
                color: #4A5560;
                font-weight: normal;  
            }}
            .comma {{
                color: #4A5560;
                font-weight: normal;  
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
    <script>
        var storage = {{}}

        function hide(_uuid) {{
            if (_uuid in storage) {{
                var e = storage[_uuid]        
            }} else {{
                var e = document.querySelector(`#${{_uuid}}`)
            }}
            e.style.display = e.style.display === "" ? "none": ""
        }}
    </script>
    </body>
    </html>
            """
    r = report_template.format(result1=r1, result2=r2)
    with open("diff.html", 'w', encoding='utf-8') as f:
        f.write(r)


def compare_json():
    j1 = read_json("./j1.json")
    j2 = read_json("./j2.json")
    l1 = []
    l2 = []

    if isinstance(j1, dict):
        record_recursive_dict(j1, l1, 0, None)
        record_recursive_dict(j2, l2, 0, None)
    else:
        record_recursive_list(j1, l1, 0, None)
        record_recursive_list(j2, l2, 0, None)

    t1, t2 = get_anti_intersection(set(l1), set(l2))
    print(f"diff t1 is ,", t1)
    print(f"diff t2 is ,", t2)
    diff_a = html_from_diff(l1, t1)
    diff_b = html_from_diff(l2, t2)
    create_result(diff_a, diff_b)


compare_json()


