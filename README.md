## Pytest automation testing sample

### 程式碼規範
> 參照python PEP-8規範
> 
> 原文：
>> https://peps.python.org/pep-0008/
> 
> 中文版：
>> https://github.com/kernellmd/Knowledge/blob/master/Translation/PEP%208%20%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91.md

### 程式碼結構
``` python
pytest_sample
├── allure-report        -- 存放Allure report html檔 (測試報告檔名為complete.html)
├── allure-results       -- 存放測試結果暫存檔
├── configs              -- 設定檔
├── pages                -- web (or app) page objects
    ├── admin              -- admin page objects
    ├── app                -- app page objects
    ├── web                -- web page objects
├── pylib                -- 共用函式庫
├── resources            -- API測試案例參數
├── testcase             -- 測試案例(實作層)
    ├── admin              -- admin測試案例(實作層)
    ├── API                -- API測試案例(實作層)
    ├── app                -- app測試案例(實作層)
    ├── web                -- web測試案例(實作層)
├── conftest.py            -- 全域共用pytest fixture
```

### Python版本
> 未定

### 需求套件
>* allure-combine 1.0.11
>* allure-pytest 2.13.2
>* pytest 7.4.4
>* requests 2.31.0
>* selenium 4.16.0
>* airtest 1.3.3
>* pocoui 1.0.94
>* json5 0.9.14
>* pyyaml 6.0.1

### 產生可獨立開啟的 Allure report file (html)
> 1. 執行pytest測試，並將測試結果存在目錄【allure-results】
>> pytest .\testcase\API\test_user.py --alluredir=allure-results
> 
> 2. 將過去的測試結果複制到目錄【allure-results】，以產生趨勢圖 
>> copy .\allure-report\history\*.* .\allure-results\history
> 
> 3. 產生測試報告的暫存檔案
>> allure generate .\allure-results\ --clean -o .\allure-report
>
> 4. 產生可單獨開啟的測試報告，存放在目錄【allure-report】
>> allure-combine .\allure-report\ --remove-temp-files
> 
> 5. 刪除本次測試結果
>> del .\allure-results\*.*
> 
> 接下來我們就可以在目錄【allure-report】中找到這個檔案【complete.html】，開啟他就可以看到試報告

### 關於 Allure report 的小麻煩 
> 在上面的範例中，allure report的測試結果會以數個json檔的形式存放在目錄【allure-results】中，
依據官方文件中的說明，必須透過特定的指令才能開啟：
>>allure serve allure-results
> 
> 但是這個方法會起動一個allure service，且service關閉的時候就無法瀏覽測試報告，實務上不太方便使用，
因此上面的範例中採用了可獨立開啟測試報告的方法。