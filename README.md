# youtube-multitool
てすとなう

## 概要
- 複数アカウントで自分のライブにコメント送信
- コメント順序やテストモード設定可能
- プロキシ経由通信もオプションで対応

## ファイル構成
- main.py         : メインスクリプト（全機能統合）
- accounts.json   : アカウント情報（OAuthトークン）
- comments.txt    : コメントリスト
- config.json     : 設定ファイル
- comment_log.txt : ログ（自動生成）

## 設定例
- config.json の `test_mode` を true にすると送信せずログのみ
- `comment_order` を "random" にするとランダム送信

## 使い方
1. accounts.json に自分のアカウントのOAuthトークンを追加
2. comments.txt にコメントを追加
3. config.json で必要な設定を変更
4. main.py を実行してライブURLを入力
5. test_mode=true ならログ確認、false で実際にコメント送信
