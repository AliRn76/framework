import timeit

from panther_core import initialize_routing, find_endpoint

x = {
    'users': {
        '': 8,
        '1': {
            'name': 1,
            'age': 2
        },
        '<admin>': {
            'name': 3,
            'age': 4
        },
        '<user_id>': {
            'who': {
                '': 5,
                'are': 6,
                'you': 7,
            }
        }
    }
}


def test_python(d):
    a = {}
    for k, v in d.items():
        if isinstance(v, dict):
            a[k] = test_python(v)
        else:
            a[k] = v
    return a


def test():
    # test_python(x)       # 0.000004082001396454871
    initialize_routing(x)  # 0.000040165999457240105

# print(f"Minimum time: {min(timeit.Timer(test).repeat(repeat=10, number=1))}")

path = 'users/3/who'
initialize_routing(x)
endpoint = find_endpoint(path)
print(f'{endpoint=}')
