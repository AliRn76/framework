import timeit

from panther_core import initialize_routing, find_endpoint as rust_find_endpoint

URLS = {
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

ENDPOINT_NOT_FOUND = (None, '')


def find_endpoint(path: str) -> tuple[int | None, str]:
    urls = URLS

    if (location := path.find('?')) != -1:
        path = path[:location]
    path = path.removesuffix('/').removeprefix('/')  # 'user/list'
    paths = path.split('/')  # ['user', 'list']
    paths_len = len(paths)

    found_path = ''
    for i, split_path in enumerate(paths):
        last_path = bool((i + 1) == paths_len)
        found = urls.get(split_path)

        # `found` is callable
        if last_path and isinstance(found, int):
            found_path += f'{split_path}/'
            return found, found_path

        # `found` is dict
        if isinstance(found, dict):
            found_path += f'{split_path}/'
            if last_path and isinstance((endpoint := found.get('')), int):
                return endpoint, found_path

            urls = found
            continue

        # `found` is None
        for key, value in urls.items():
            if not key.startswith('<'):
                continue

            elif last_path:
                if isinstance(value, int):
                    found_path += f'{key}/'
                    return value, found_path
                elif isinstance(value, dict) and '' in value:
                    found_path += f'{key}/'
                    return value[''], found_path
                else:
                    return ENDPOINT_NOT_FOUND

            elif isinstance(value, dict):
                urls = value
                found_path += f'{key}/'
                break

            else:
                return ENDPOINT_NOT_FOUND

        else:
            return ENDPOINT_NOT_FOUND

    return ENDPOINT_NOT_FOUND


PATH = 'users/1/age'


def test_python():
    # 1.3410026440396905e-06 --> 'users/'
    # 0.0000024439941626042128 --> 'users/1/age'
    find_endpoint(PATH)


def test_rust():
    #1.9080995116382837e-05 --> 'users/'        --> debug
    #3.5492994356900454e-05 --> 'users/1/age'   --> debug
    #0.0000035179982660338283 --> 'users/1/age'   --> release
    rust_find_endpoint(PATH)


def test():
    # initialize_routing(URLS)  # Just for rust

    print(f"Minimum time: {min(timeit.Timer(test_python).repeat(repeat=100, number=1))}")


test()
