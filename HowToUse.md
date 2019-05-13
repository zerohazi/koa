# how to use koa

@Windows(with Python)

1. chrome driver をインストール
1. chromedriver.exeのある場所をメモ
1. koa.pyの，driver = webdriver.Chrome(executable_path='hoge', options=options)の，hoge部分に，chromedriverへのパスを入れて保存
1. koa_basic_info.pyのID,PWを自分のものに書き換え
1. コマンドプロンプト等で，koa.pyのあるフォルダまで移動
1. pythonのインタラクティブシェルを開く
1. 「import koa」を実行（chromeが開く）
1. 「koa.run(rc, ic)」（rcには，整数値でクロールする範囲（100,200など）を入れる／icには，整数/小数で，スクレイピングの秒間隔を指定する）
1. ログを残しながらスクレイピングされると思う
