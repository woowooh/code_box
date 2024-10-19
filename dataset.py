import copy


class Dataset:
    
    def input_digit(self):
        d = [
            -1,
             0,
             1,
        ]
        return d

    def input_str(self):
        d = [
            "",
            "~!@#''\"$%^&*(self)_+={}|\\w\n\t<,.>/?`-_",
            "~@#￥%……&*（）———+=‘；“：「」【】，。、？|",
            " ",
        ]
        return d
    
    def input_timestamp(self):
        d = [
            "2023-10-01 12:00:00",
            "2023-12-31 23:59:59",
            "2100-12-31 23:59:59",
            "2023-02-30 12:00:00",
        ]
        return d

    def input_timestamp_int(self):
        d = [
            1696948800,
            1893456123,
        ]
        return d
    
    def input_bool(self):
        d = [
            True,
            False,
            "true",
            "false",
            1,
            0,
        ]
        return d
    
    def input_xss(self):
        d = [
            "<script>alert('XSS');</script>",
            "\"><script>alert('XSS');</script>",
            "'><script>alert('XSS');</script>",
            "\"><img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=",
            "&lt;script&gt;alert('XSS')&lt;/script&gt;",
            "&#60;script&#62;alert('XSS')&#60;/script&#62;",
        ]
        return d
    
    def input_long(self):
        d = [
            -2147483648,
             2147483647,
             2147483648,
             -2147483649,
        ]
        return d
    
    def input_float(self):
        d = [
            0.0,
            1.0,
            1.1,
            1.0001,
            -1.0,
            -1.1,
            0.01,
            3.4028235E+38,
            -3.4028235E+38,
            3.4028236E+38,
            -3.4028236E+38,
        ]
        return d

    def input_long_char(self):
        s = "这个测试" * 1000
        d = [
            s,
        ]
        return d

    def input_emoji(self):
        d = [
            "😀",
        ]
        return d

    def input_inject(self):
        d = [
            "' OR '1'='1",
            "'; SELECT * FROM users; --",
            "' AND 1=1 --",
            "' AND 1=0 --",
            "' UNION SELECT null, username, password FROM users --",
        ]
        return d

    def input_forbidden(self):
        d = [
            "毒品",
            "涉黄",
            "赌场",
        ]
        return d

    def get_all_input(self, target=None):
        attribute_n_methods = dir(self)
        if target:
            attribute_n_methods = target
        r = []
        for am in attribute_n_methods:
            if am.startswith("input_"):
                method = getattr(self, am, None)
                if callable(method):
                    d = method()
                    r.extend(d)
        return r

    def replace_and_post_args(self, d: dict, action):
        for k, v in d.items():
            if isinstance(v, list):
                self.recursive_list(k, v, action, d)
            elif isinstance(v, dict):
                self.recursive_dict(k, v, action, d)
            else:
                for arg in self.get_all_input():
                    old = v
                    d[k] = arg
                    action(d)
                    d[k] = old

    def recursive_dict(self, prev_key, d, action, source_d):
        for k, v in d.items():
            if isinstance(v, list):
                self.recursive_list(k, v, action, source_d)
            elif isinstance(v, dict):
                self.recursive_dict(k, v, action, source_d)
            else:
                for arg in self.get_all_input():
                    old = v
                    d[k] = arg
                    action(source_d)
                    d[k] = old

    def recursive_list(self, prev_key, l, action, source_d):
        for i, v in enumerate(l):
            if isinstance(v, list):
                self.recursive_list(prev_key, v, action, source_d)
            elif isinstance(v, dict):
                self.recursive_dict(prev_key, v, action, source_d)
            else:
                for arg in self.get_all_input():
                    old = v
                    l[i] = arg
                    action(source_d)
                    l[i] = old


def _main():
    e = Dataset()
    t = {"a": "b", "重叠": [1, 2, 3], "dict": {"fff": "ccc"}}
    e.replace_and_post_args(t, print)


_main()