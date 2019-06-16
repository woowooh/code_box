import json


global_l = []
def dic_compare(a, b, n=0):
    common_key_list = []
    a_copy = a.copy()
    b_copy = b.copy()
    for k, v in a.items():        
        for k2, v2 in b.items():
            if (k == k2):
                common_key_list.append(k)                
                break
    for k in common_key_list:
        del a_copy[k]
        del b_copy[k]
    for k in a_copy.keys():
        global_l.append((k, n + 1))
    for k in b_copy.keys():
        global_l.append((k, n + 1))
    for k in common_key_list:        
        if a[k] != b[k]:
            if (isinstance(a[k], dict) and isinstance(b[k], dict)):
                dic_compare(a[k], b[k], n + 1)
            elif ((isinstance(a[k], list) and isinstance(b[k], list))):
                list_compare(a[k], b[k])
            else:
                global_l.append((k, n + 1))


def list_compare(a, b, n=0):
    common_list = []
    a_copy = a.copy()
    b_copy = b.copy()
    for v1 in a:
        find_k = False
        for v2 in b:
            if (v1 == v2):
                common_key_list.append(v1)                
                break
    for val in common_list:
        a_copy.remove(val)
        b_copy.remove(val)
    for k in a_copy:
        global_l.append((k, n + 1))
    for k in b_copy:
        global_l.append((k, n + 1))

s = '{"responseCode":200,"message":[],"data":{"incidents":{"isDistribute":false,"deviceType":"笔记本","hostname":"mac的MacBook Air","corporateType":"公司内部","operationSystem":"macOS 10.13 (17A365)","dmDeviceName":"bogon","sourceTrs":"0","riskLevel":"","details":"http://172.22.70.119/post.php ","channelType":"HTTP","workModeType":"阻断","sourceName":"mac的MacBook Air\\mac","destinationNames":"172.22.70.119","sourceGroups":"","sourceIp":"172.21.21.45","destinationIps":"172.22.70.119","sourceManagers":"","destinationCountries":"","destinationCities":"","destinationLocations":"","riskLevelExport":"","transactionId":"94ef9f37-65be-42fe-929e-cc3180566422","statusType":"新","actionType":"阻止","serialId":1,"detectTime":"2019-05-08 16:15:52","maxMatches":1,"transactionSize":"1 KB","severityType":"信息","breachContents":"","incidentTime":"2019-05-08 16:15:37","detectAgent":"Endpoint(mac的MacBook Air)","analyzeAgent":"Content Analysis Engine(mac的MacBook Air)","isIndent":false,"policyNames":"test1","ignoreStatus":"未忽略","policyGroupNames":"默认策略组","totalMatches":1,"statusTypeId":1,"actionTypeId":2,"severityTypeId":4,"displayHtml":true,"source":{"userReportName":"logonName","logonName":"mac的MacBook Air\\mac","ipAddress":"172.21.21.45","hostname":"mac的MacBook Air","displayName":"mac的MacBook Air\\mac"},"destinations":[{"directionType":"出向","actionType":"","url":"http://172.22.70.119/post.php ","ipAddress":"172.22.70.119","displayName":"172.22.70.119"}],"matchedPolicies":[{"policyName":"test1","policyUuid":"59cfa904-2d6b-48a7-a237-20203e0bbad7","matches":1,"isTrickle":false,"isVisible":true,"policyGroupName":"默认策略组","matchedRules":[{"ruleName":"1","matchedConditions":[{"matchedElements":[{"elementType":"关键字","elementTypeId":5,"elementUuid":"4680e64d6ecc2cb0e70261e9f5cc4343","matches":"1","elementName":"特别搜索","matchedContents":[{"locationType":"表单数据","matches":1,"contentSize":"12 B","compoundTexts":["特别搜索"],"fileLayer":0,"locationTypeId":19}]}]}]}]}],"histories":[{"description":"事件被记录","historyTime":"2019-05-08 16:15:37","adminName":"system"}]}}}'
s2 = '{"data":{"incidents":{"isDistribute":false,"hostname":"mac的MacBook Air","corporateType":"公司内部","operationSystem":"macOS 10.13 (17A365)","dmDeviceName":"bogon","sourceTrs":"0","riskLevel":"","details":"http://172.22.70.119/post.php ","channelType":"HTTP","workModeType":"阻断","sourceName":"mac的MacBook Air\\mac","destinationNames":"172.22.70.119","sourceGroups":"","sourceIp":"172.21.21.45","destinationIps":"172.22.70.119","sourceManagers":"","destinationCountries":"","destinationCities":"","destinationLocations":"","riskLevelExport":"","transactionId":"94ef9f37-65be-42fe-929e-cc3180566422","statusType":"新","actionType":"阻止","serialId":1,"detectTime":"2019-05-08 16:15:52","maxMatches":1,"transactionSize":"1 KB","severityType":"信息","breachContents":"","incidentTime":"2019-05-08 16:15:37","detectAgent":"Endpoint(mac的MacBook Air)","analyzeAgent":"Content Analysis Engine(mac的MacBook Air)","isIndent":false,"policyNames":"test1","ignoreStatus":"未忽略","policyGroupNames":"默认策略组","totalMatches":1,"statusTypeId":1,"actionTypeId":2,"severityTypeId":4,"displayHtml":true,"source":{"userReportName":"logonName","logonName":"mac的MacBook Air\\mac","ipAddress":"172.21.21.45","hostname":"mac的MacBook Air","displayName":"mac的MacBook Air\\mac"},"destinations":[{"directionType":"出向","actionType":"","url":"http://172.22.70.119/post.php ","ipAddress":"172.22.70.119","displayName":"172.22.70.119"}],"matchedPolicies":[{"policyName":"test1","policyUuid":"59cfa904-2d6b-48a7-a237-20203e0bbad7","matches":1,"isTrickle":false,"isVisible":true,"policyGroupName":"默认策略组","matchedRules":[{"ruleName":"1","matchedConditions":[{"matchedElements":[{"elementType":"关键字","elementTypeId":5,"elementUuid":"4680e64d6ecc2cb0e70261e9f5cc4343","matches":"1","elementName":"特别搜索","matchedContents":[{"locationType":"表单数据","matches":1,"contentSize":"12 B","compoundTexts":["特别搜索"],"fileLayer":0,"locationTypeId":19}]}]}]}]}],"histories":[{"description":"事件被记录","historyTime":"2019-05-08 16:15:37"}]}}}'
s = s.replace("\\", "\\\\")
s2 = s2.replace("\\", "\\\\")

dic = json.loads(s)
dic2 = json.loads(s2)

dic_compare(dic, dic2)
print(global_l)
