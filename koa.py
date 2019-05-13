# coding: UTF-8
import os
import re
# import random
import twitter
import textwrap
import koa_basic_info as b
from time import sleep
from datetime import datetime
from selenium import webdriver
from PIL import Image, ImageDraw, ImageFont


# option settings @ open browser
options = webdriver.ChromeOptions()
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path='C:/-/p/0/webdriver/chromedriver.exe', options=options)
print('◆ The browser(chrome web driver) has been opened!')


class KuNotice:
    def __init__(self, ntc_id, ntc_order):
        self.url = b.tgt_url_of(ntc_id)
        driver.get(self.url)

        try:
            self.addressee_list = driver.find_element_by_name('addresseelist').text
            self.status = 'Public' if b.re_addressee.match(self.addressee_list) else 'In-House' if self.addressee_list == '' else 'Confidential'
            self.status = self.status.ljust(13)
        except Exception:
            self.addressee_list = ''
            self.status = 'exc@addressee'

        try:
            self.content = driver.find_element_by_name('CONTENT').get_attribute('value') or '[ NO DATA ]'
        except Exception:
            self.content = 'No Content'
            self.status = self.status + ', exc@content'

        try:
            self.title = driver.find_element_by_name("TITLE").get_attribute("value") or '[ NO DATA ]'
        except Exception:
            self.title = 'No Title'
            self.status = self.status + ', exc@title'

        try:
            self.attachment = driver.find_element_by_name('ATTCHFILENAME').get_attribute('value')
            self.has_attach = '\n【添付あり】'
        except Exception:
            # When there is no attachment, the trial return exception
            self.attachment = ', exc@attachment'
            self.has_attach = ''

        # ログ出力用
        self.statuses = (
            str(ntc_id) + ' | ' +
            str(ntc_order).zfill(5) + ' |' +
            self.has_attach.strip().ljust(6, '　') + '| ' +  # 全角文字6文字分で左揃え
            self.status + ' | ' +
            self.title + ' | ' +
            ''.join(self.addressee_list.splitlines())
        ).strip() + '\n'

        # i want to see what is being processed immediately
        print('\r' + ' ' * 50, end='')
        print('\r' + self.status, end='')

    def img(self, tgt_id):
        font_size = 35
        # font_name = 'C:/Windows/Fonts/ipaexg.ttf' #IPAのフリーフォント
        font_name = 'C:/Windows/Fonts/yugothib.ttf'  # 游ゴシックBold
        img_src = 'koa_bg.jpg'
        draw_x = 70
        draw_y = 70
        attach = self.attachment if not ', exc@attachment' else '添付ファイルなし'
        text = (
            # お知らせの内容を改行ごとに分割したものを，さらに50字毎に分割して，連結
            '\n'.join(['\n'.join(textwrap.wrap(i, 50)) for i in self.content.splitlines()]) +
            '\n\n-----\n\n' +
            attach
        )

        image = Image.open(img_src)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_name, font_size)
        # 文字の枠線
        draw.text((draw_x + 1, draw_y + 1), text, font=font, fill=(50, 50, 50, 200))
        draw.text((draw_x + 1, draw_y - 1), text, font=font, fill=(50, 50, 50, 200))
        draw.text((draw_x - 1, draw_y + 1), text, font=font, fill=(50, 50, 50, 200))
        draw.text((draw_x - 1, draw_y - 1), text, font=font, fill=(50, 50, 50, 200))
        draw.text((draw_x, draw_y), text, font=font, fill=(255, 255, 255, 0))

        img_path = './img/' + datetime.today().strftime('%Y%m%d') + '/'
        os.makedirs(img_path, exist_ok=True)
        img_dest = img_path + str(tgt_id) + '.png'
        image.save(img_dest)
        return img_dest


def post_tweet(ntc, ntc_id):
    # rand_num = '(rand: ' + str(random.randint(1, 99999)).zfill(5) + ')'   # 試験運用表示
    t = twitter.Twitter(auth=b.auth)

    # generate body text
    status = (
        # '#TrialOperation' + rand_num + '\n' +  # 試験運用表示
        ntc.title + '\n' +
        ntc.has_attach + '\n' +
        'ログイン：' + b.portal_url + '\n' +
        'お知らせ：' + ntc.url
    )

    # load attach img
    pic = ntc.img(ntc_id)
    with open(pic, "rb") as img_file:
        img_data = img_file.read()
    pic_upload = twitter.Twitter(domain='upload.twitter.com', auth=b.auth)
    tw_img1 = pic_upload.media.upload(media=img_data)["media_id_string"]

    # post tweet
    t.statuses.update(status=status, media_ids=",".join([tw_img1]))


def run(rc, ic):
    '''
    rc: range of crawling
    ic: interval of crawling
    '''

    driver.get(b.portal_url)

    # if the session is valid, this section will be passed: you can leach the portal page directly.
    if b.re_login_url.match(driver.current_url):
        # login to information system
        driver.find_element_by_id('IDToken1').send_keys(b.login_id)
        driver.find_element_by_id('IDToken2').send_keys(b.login_pw)
        driver.find_element_by_name('Login.Submit').click()

    # check the start point for crawling and get a targets list
    ntc_id_base = '\n'
    last_line = -1
    while ntc_id_base == '\n':
        with open('koa_log_public.txt', 'r', encoding='utf_8') as f:
            # get a notice id in valid last line
            ntc_id_base = f.readlines()[last_line][:14]
        last_line -= 1
    ntc_id_list = [int(ntc_id_base) + (x + 1) for x in range(rc)]

    # put brank line for make log easy to read
    log_sep = '\n\n\n'
    with open('koa_log.txt', 'a', encoding='utf_8') as f:
        f.write(log_sep)
    with open('koa_log_public.txt', 'a', encoding='utf_8') as f:
        f.write(log_sep)

    # crawling phase
    for ntc_order, ntc_id in enumerate(ntc_id_list):
        ntc = KuNotice(ntc_id, ntc_order)

        with open('koa_log.txt', 'a', encoding='utf_8') as f:
            f.write(ntc.statuses)

        if re.match(r'\A(Public)', ntc.status):
            post_tweet(ntc, ntc_id)
            # ntc.img(ntc_id)     # for test

            with open('koa_log_public.txt', 'a', encoding='utf_8') as f:
                f.write(ntc.statuses)

        sleep(ic)  # 慈悲

    print('\r◆ All processes have been finished!' + ' ' * 10)
    # kill tab: close browser
    # driver.close()
