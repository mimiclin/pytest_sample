import os


cmd_list = [
    r'chcp 65001',
    r'copy .\allure-report\history\*.* .\allure-results\history',
    r'copy .\environment.properties .\allure-results',
    r'allure generate .\allure-results\ --clean -o .\allure-report',
    r'allure-combine .\allure-report\ --remove-temp-files',
    r'echo y | del .\allure-results\*.*'
]

for cmd in cmd_list:
    print(f'Execute start: {cmd}')
    os.system(cmd)
    print(f'Execute done: {cmd}')
    print(f'{"-"*20}\n')

print('Done')
