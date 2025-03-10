# 求人WEBアプリケーション

## 概要

この求人WEBアプリケーションは、求職者と企業をつなぐプラットフォームです。ユーザーは求人を検索し、お気に入りに登録し、応募することができます。また、企業は求人を掲載し、応募者を管理することができます。

## 主な機能

### 求職者向け機能
- ユーザー登録・ログイン機能
- プロフィール作成・編集
- 求人検索
- 求人のお気に入り登録
- 求人への応募
- 選考状況の確認
- レコメンド求人の表示
- ミッション達成によるポイント獲得

### 企業向け機能
- 企業アカウント登録・ログイン
- 企業プロフィール作成・編集
- 求人の掲載・編集・削除
- 応募者の管理と選考状況の更新

## 技術スタック

- バックエンド: Python 3.9+, Django 4.2
- データベース: PostgreSQL
- キャッシュ/非同期処理: Redis, Celery
- フロントエンド: HTML, CSS, JavaScript, Bootstrap 5

## インストール方法

### 前提条件
- Python 3.9以上
- pip (Pythonパッケージマネージャー)
- PostgreSQL
- Redis (オプション、キャッシュと非同期処理用)

### セットアップ手順

1. リポジトリをクローン

```bash
git clone https://github.com/yourusername/jobportal.git
cd jobportal
```

2. 仮想環境を作成して有効化

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

4. 環境変数の設定

`.env`ファイルをプロジェクトのルートディレクトリに作成し、以下の内容を設定します。

```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://user:password@localhost:5432/jobportal
REDIS_URL=redis://localhost:6379/0
```

5. データベースのマイグレーション

```bash
python manage.py migrate
```

6. 初期ミッションの設定

```bash
python manage.py setup_missions
```

7. 開発サーバーの起動

```bash
python manage.py runserver
```

これで、アプリケーションが http://127.0.0.1:8000/ で実行されます。

## プロジェクト構造

```
jobportal/                  # プロジェクトのルートディレクトリ
├── manage.py               # Djangoの管理コマンド用スクリプト
├── jobportal/              # プロジェクト設定フォルダ
│   ├── __init__.py
│   ├── settings.py         # プロジェクト設定ファイル
│   ├── urls.py             # プロジェクトのメインURL設定
│   ├── asgi.py             # ASGI設定
│   └── wsgi.py             # WSGI設定
├── accounts/               # ユーザーアカウント関連アプリ
├── jobs/                   # 求人情報関連アプリ
├── missions/               # ミッション関連アプリ
├── core/                   # 共通機能アプリ
├── static/                 # 静的ファイル（CSS、JS、画像など）
├── media/                  # ユーザーがアップロードするファイル
└── templates/              # 共通テンプレート
```

## 開発者向け情報

### 新しいアプリの追加方法

```bash
python manage.py startapp new_app_name
```

新しいアプリを作成したら、`jobportal/settings.py`の`INSTALLED_APPS`に追加してください。

### マイグレーションの作成

モデルを変更した後は、マイグレーションを作成して適用する必要があります。

```bash
python manage.py makemigrations
python manage.py migrate
```

### 管理者ユーザーの作成

```bash
python manage.py createsuperuser
```

作成した管理者アカウントで http://127.0.0.1:8000/admin/ にアクセスできます。

### テストの実行

```bash
python manage.py test
```

## デプロイガイド

### 本番環境の設定

1. `settings.py`を本番環境用に設定

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# セキュリティ設定
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

2. 静的ファイルの収集

```bash
python manage.py collectstatic
```

3. WSGIサーバー (例: Gunicorn) を設定

```bash
pip install gunicorn
gunicorn jobportal.wsgi:application
```

4. Webサーバー (例: Nginx) を設定してGunicornとの連携を行う

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## コントリビューション

プロジェクトへの貢献は歓迎します！バグ報告、機能リクエスト、プルリクエストなどをお願いします。

## 連絡先

質問や問題がある場合は、issueを作成するか、email@example.com までご連絡ください。
