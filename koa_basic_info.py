import re
import twitter

# ku
portal_url = 'https://portal.kansai-u.ac.jp/Portal/'
login_id = "＊＊＊＊"   # ログインID
login_pw = "＊＊＊＊"   # ログインパスワード
ntc_url_prefix = "https://portal.kansai-u.ac.jp/vespine/Notice?REQUEST_NAME=CMD_SHOW_DETAIL_IN_LIST&PAGE_ID=noticeinlist&REQUEST_ITEM_NO1="
ntc_url_suffix = "&REQUEST_ITEM_NO2=0&REQUEST_ITEM_NO3=0&NOTICE_TP=0"

re_addressee = re.compile(r'(関西大学|学生|学部生|大学院生|学部|学科|研究科|年|留学生別科)\Z')
re_login_url = re.compile(r'\A(https://aft.auth.kansai-u.ac.jp/amserver/UI/Login)')
re_ntc_url = re.compile(r'\A(https://portal.kansai-u.ac.jp/vespine/Notice)')


def tgt_url_of(tgt_id):
    # this function exists as attribute of basic info (using like: "b.tgt_url_of(ntc_id)" )
    # because the prefix/suffix of notice URLs also should not be public.
    return (
        ntc_url_prefix +
        str(tgt_id) +
        ntc_url_suffix
    )


# tw
auth = twitter.OAuth(
    consumer_key="＊＊＊＊＊",
    consumer_secret="＊＊＊＊＊",
    token="＊＊＊＊＊",
    token_secret="＊＊＊＊＊"
)
