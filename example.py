from TohyoTalk import TohyoTalk


Tohyo = TohyoTalk(debug=False)  # debug=Trueでデバッグモード

# 投票トークアカウント作成
userID = "ユーザーID"
userName = "ユーザー名"
password = "パスワード"
Tohyo.create_account(userID, userName, password)

# 投票トークログイン
userID = "ユーザー名"
password = "パスワード"
Tohyo.login(userID, password)

#以下はアカウント作成 or ログインをしたら動く機能

# 投票トークつぶやき(戻り値: MessageID)
content = "つぶやく内容"
Tohyo.tweet(content)

# 投票トークいいね
MessageID = "メッセージID"
Tohyo.like(MessageID)

# 投票トーク投票(ターゲットは右が2左が1)
VoteID = "投票ID"
target = "ターゲット"
Tohyo.vote(MessageID)

# 投票トークフォロー
UserID = "フォローしたい人のユーザーID"
Tohyo.follow(UserID)

# 投票トークゲーム(戻り値: ランキング)
Score = "土管を超えた回数"
Tohyo.game(Score)

# 投票トークプロフィールメッセージ変更
content = "プロフィールメッセージ"
Tohyo.profile(content)

# 投票トークプロフィール画像変更
path = "画像のパス"
Tohyo.icon(path)
