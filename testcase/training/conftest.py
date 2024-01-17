import pytest


@pytest.fixture(scope="function")
def print_function_message():
    print(f'        --- Function層 開始 ---')
    yield
    print(f'        --- Function層 結束 ---')


@pytest.fixture(scope="class")
def print_class_message():
    print(f'    --- Class層 開始 ---')
    yield
    print(f'    --- Class層 結束 ---')


@pytest.fixture(scope="module", autouse=True)
def print_module_message():
    print(f'--- Module層 開始 ---')
    yield
    print(f'--- Module層 結束 ---')


@pytest.fixture()
def get_my_name():
    return f'Mimimimimimimimic!!!!!!'


@pytest.fixture()
def get_url():
    env = 'qat'
    url = f'{env}-qa.com'
    return url