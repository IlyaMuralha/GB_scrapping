import json
import re
from urllib.parse import urlencode
from copy import deepcopy

import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem


class InstaSpider(scrapy.Spider):
    name = 'insta'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    user_parse = 'ai_machine_learning'

    # with open('./instagram.json', 'r') as f:
    #     INSTA = json.load(f)
    #
    #     insta_login = INSTA['insta_login']
    #     insta_password = INSTA['insta_password']
    #     graphql_url = INSTA['graphql_url']
    #     query_posts_hash = INSTA['query_posts_hash']
    #     query_post_hash = INSTA['query_post_hash']

    def parse(self, response: HtmlResponse):
        csrf = self.get_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={
                                     'username': "kuznizza", 'enc_password': "#PWD_INSTAGRAM_BROWSER:10:1630736374:AV1QAHXfFcarr9JQh4rtjg/VZc9gFCSYza/I+TnHNYDq6vhJ5B2IuQjXZhLYmdxO/TtrYKpOoRMYZ5GHiiLQQ1teQew0Vxd3ajO1hF1HkP1ZuI7PiLk81h1TYR582JatIhA8g/vPdsCTc7IzcQAZk0IO"
                                 },
                                 headers={'x-csrftoken': csrf})

    def login(self, response: HtmlResponse):
        print()
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(f'/{self.user_parse}/',
                                  callback=self.user_parsing,
                                  cb_kwargs={'username': self.user_parse})

    def user_parsing(self, response: HtmlResponse, username):
        user_id = self.get_user_id(response.text, username)
        variables = {'id': user_id,
                     'first': 12}
        url_posts = self.graphql_url + f'query_hash={self.query_posts_hash}&{urlencode(variables)}'
        yield response.follow(url_posts,
                              callback=self.user_data_parsing,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)})

    def user_data_parsing(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_posts = self.graphql_url + f'query_hash={self.query_posts_hash}&{urlencode(variables)}'
            yield response.follow(url_posts,
                                  callback=self.user_data_parsing,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)})

        posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
        for post in posts:
            variables = {'shortcode': post.get('node').get('shortcode'),
                         'child_comment_count': 3,
                         'fetch_comment_count': 40,
                         'parent_comment_count': 24,
                         'has_threaded_comments': 'true',
                         }
            url_post = self.graphql_url + f'query_hash={self.query_post_hash}&{urlencode(variables)}'
            yield response.follow(url_post,
                                  callback=self.user_post_parsing)

            # item = InstaparserItem(user_id=user_id,
            #                        username=username,
            #                        node=post.get('node'))
            # yield item

    def user_post_parsing(self, response: HtmlResponse):
        j_data = response.json()
        post_info = j_data.get('data').get('shortcode_media')
        item = InstaparserItem(user_id=post_info.get('owner').get('id'),
                               username=post_info.get('owner').get('username'),
                               picture_profile_url=post_info.get('owner').get('profile_pic_url'),
                               data_owner_public=post_info.get('owner'),
                               data_post=post_info,
                               picture_post_url=post_info.get('display_url'),
                               comments=post_info.get('edge_media_to_parent_comment').get('edges'),
                               count_comments=post_info.get('edge_media_to_parent_comment').get('count'),
                               likes=post_info.get('edge_media_preview_like').get('count'),
                               accessibility_caption=post_info.get('accessibility_caption')
                               )
        yield item

    # получаем токен для авторизации
    def get_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # получаем id пользователя
    def get_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')
