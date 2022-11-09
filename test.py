import json

a = '{"a" : "b", "c" : "d"}'
employee_string = '{"first_name": "Michael", "last_name": "Rodgers", "department": "Marketing"}'

b = json.loads(a)

print(b.get('lebra'))