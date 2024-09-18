import json
import uuid
import os


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


def record_recursive_dict(d, storage, level, prefix=""):
    storage.append(("symbol", level, "{", prefix))
    level += 1
    for k, v in d.items():
        storage.append(("key", level, k, prefix))
        if isinstance(v, list):
            record_recursive_list(v, storage, level, prefix=f"{prefix}{k}.")
        elif isinstance(v, dict):
            record_recursive_dict(v, storage, level, prefix=f"{prefix}{k}.")
        elif isinstance(v, int) or isinstance(v, float):
            storage.append(("value", level, f"{str(v)}", f"{prefix}{k}."))
        elif isinstance(v, str):
            storage.append(("value", level, f"'{v}'", f"{prefix}{k}."))
        elif v is None:
            storage.append(("value", level, None, f"{prefix}{k}."))
    storage.append(("symbol", level - 1, "}", prefix))


def record_recursive_list(lst, storage, level, prefix=""):
    storage.append(("symbol", level, "[", prefix))
    level += 1
    for i, e in enumerate(lst):
        if isinstance(e, list):
            record_recursive_list(e, storage, level,  prefix=f"{prefix}[{i}]")
        elif isinstance(e, dict):
            record_recursive_dict(e, storage, level, prefix=f"{prefix}[{i}]")
        elif isinstance(e, int) or isinstance(e, float):
            storage.append(("value", level, f"{e}", f"{prefix}[{i}]"))
        elif isinstance(e, str):
            storage.append(("value", level, f"'{e}'", f"{prefix}[{i}]"))
        elif e is None:
            storage.append(("value", level, None, f"{prefix}[{i}]"))
    storage.append(("symbol", level - 1, "]", prefix))


def get_exclusion(set1, set2):
    anti1 = set1 - set2
    anti2 = set2 - set1
    return list(anti1), list(anti2)


def html_styled_diff(line, t1):
    template_key = '{indent}<span class="{cls_name}">"{value}":</span>{br}'
    template_value = '{indent}<span class="{cls_name}">{value}</span>{br}'
    default_left = '{indent}<span onClick="hide(\'{_uuid}\')">+</span><span id="{_uuid}" class="{cls_name}" data-type="object">{value}{br}'
    default_right = '{indent}{value}</span>{br}'
    cls_name = " "
    value = line[1][2]
    _uuid = f"a{str(uuid.uuid4())}"
    indent = space_map[line[0]]
    if line[1][0] == "key":
        cls_name = "key"
        template = template_key
        if line[1] in t1:
            cls_name += " warn"
    elif line[1][0] == "value":
        cls_name = "value"
        template = template_value
        if line[1] in t1:
            cls_name += " warn"
    else:
        cls_name = "default"
        if line[1][2] in ["{", "["]:
            template = default_left
        if line[1][2] in ["}", "]"]:
            template = default_right
    if line[1] in t1:
        t1.remove(line[1])
    br = line[2]
    if "," in br:
        br = f'<span class="default comma">{br.replace("<br>", "")}</span><br>'
    return template.format(**locals())


def html_from_diff(l, exclusion):
    r = []
    prev = None
    length_l = len(l)
    for i, e in enumerate(l):
        indent = e[1]
        br = "<br>"
        if i + 1 < length_l:
            next = l[i + 1]
            if e[0] == "symbol":
                if prev and prev[0] == "key":
                    indent = 0
                    br = "<br>"
                if e[2] in e[2] in ["}", "]"] and next[2] not in ["}", "]"]:
                    indent = e[1]
                    br = ",<br>"
            elif e[0] == "key":
                indent = e[1]
                br = ""
            elif e[0] == "value":
                if prev[0] == "key":
                    indent = 0
                    br = "<br>"
                if next[0] == "value":
                    indent = e[1]
                    br = ",<br>"
                if next[0] == "key":
                    indent = 0
                    br = ",<br>"
        line = (indent, e, br)
        line = html_styled_diff(line, exclusion)
        r.append(line)
        prev = e
    return "".join(r)


def create_result(r1, r2, filename):
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
        <div>old</div>
        {result1}
    </div>
    <div id="b">
        <div>new</div>
        {result2}
    </div>
    <script>
        var storage = {{}}

        function hide(_uuid) {{
            if (_uuid in storage) {{
                var e = storage[_uuid]  
            }} else {{
                var e = document.querySelector(`#${{_uuid}}`)
                storage[_uuid] = e
            }}
            e.style.display = e.style.display === "" ? "none": ""
        }}
    </script>
    </body>
    </html>
            """
    r = report_template.format(result1=r1, result2=r2)
    sep = os.path.sep
    with open(f"{filename}.html".strip(sep), 'w', encoding='utf-8') as f:
        f.write(r)


def compare_json(j1=None, j2=None, filename=""):
    j1 = j1 or read_json("./old.json")
    j2 = j2 or read_json("./new.json")
    l1 = []
    l2 = []
    if not (isinstance(j1, type(j2))):
        raise Exception("compare json type not equal")
    if isinstance(j1, dict):
        record_recursive_dict(j1, l1, 0)
        record_recursive_dict(j2, l2, 0)
    else:
        record_recursive_list(j1, l1, 0)
        record_recursive_list(j2, l2, 0)

    e1, e2 = get_exclusion(set(l1), set(l2))
    print(f"diff t1 is ,", e1)
    print(f"diff t2 is ,", e2)
    diff_a = html_from_diff(l1, e1)
    diff_b = html_from_diff(l2, e2)
    create_result(diff_a, diff_b, filename)


def compare_result(j1=None, j2=None):
    j1 = j1 or read_json("./old.json")
    j2 = j2 or read_json("./new.json")
    l1 = []
    l2 = []

    if isinstance(j1, dict):
        record_recursive_dict(j1, l1, 0)
        record_recursive_dict(j2, l2, 0)
    else:
        record_recursive_list(j1, l1, 0)
        record_recursive_list(j2, l2, 0)
    e1, e2 = get_exclusion(set(l1), set(l2))
    assert e1 == [], e1
    assert e2 == [], e2


if __name__ == "__main__":
    compare_json(filename="diff")
