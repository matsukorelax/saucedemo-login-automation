# Selenium Login Test (SauceDemo)

## ✅ 概要
Selenium + pytest を使ったログイン機能の自動テスト。  
正常系・異常系を網羅し、ログ出力＆スクリーンショットで状況確認可能。

## 📋 テスト内容
- `test_login_flow`: 正常なログイン
- `test_login_invalid_name`: 間違ったユーザー名
- `test_login_invalid_pass`: 間違ったパスワード
- `test_login_empty_fields`: 空欄ログイン

## ▶️ 実行方法
```bash
pytest -s test_login.py

🔍 必要環境
Python 3.10+

Chromeブラウザ

pip install -r requirements.txt

---

### 📦 2. `requirements.txt`
```txt
selenium
pytest
webdriver-manager
