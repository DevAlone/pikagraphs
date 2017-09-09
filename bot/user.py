from lxml import html
import re
import http.client
try:
    from . import api
    import json
except:
    pass
# import tor


def getUserProfileData(username, fast=False):
    if fast:
        return _getUserProfileDataFast(username)

    userData = {}

    connection = http.client.HTTPSConnection("pikabu.ru", timeout=20)
    connection.request("GET", "/profile/" + username)
    response = connection.getresponse()
    data = response.read().decode('cp1251')
#    data = response.read()
#    data = tor.get("https://pikabu.ru/profile/" + username)
#    data = data.decode('cp1251')

    tree = html.fromstring(data)

    try:
        userData['rating'] = int(tree.xpath("\
        .//span[@class='b-user-profile__label' and text()=\"рейтинг\"]\
        /following-sibling::span[@class='b-user-profile__value']")[0].text)
    except:
        userData.rating = None

    userData['commentsCount'] = int(tree.xpath("\
        .//span[@class='b-user-profile__label' and text()=\"комментариев\"]\
        /following-sibling::span[@class='b-user-profile__value']")[0].text)
    userData['postsCount'] = int(tree.xpath("\
       .//span[@class='b-user-profile__label' and contains(text(), \"постов\")]\
       /following-sibling::span[@class='b-user-profile__value']")[0].text)
    userData['hotPostsCount'] = int(tree.xpath("\
        .//span[@class='b-user-profile__label' \
        and starts-with(text(), \", из них в \")]\
        /following-sibling::span[@class='b-user-profile__value']")[0].text)
    userPlusesMinusesCount = tree.xpath("\
  .//span[@class='b-user-profile__label' and starts-with(text(), \"поставил\")]\
  /following-sibling::span[@class='b-user-profile__value']")[0]\
        .text_content()

    matches = re.search(r'^.*?([0-9]+).*плюс.*?([0-9]+).*$',
                        userPlusesMinusesCount, re.DOTALL)

    userData['plusesCount'] = int(matches.group(1))
    userData['minusesCount'] = int(matches.group(2))

    return userData


def _getUserProfileDataFast(username):
    jsonData = json.loads(api.getUserProfile(username).text)
    jsonData = jsonData['response']['user']

    userData = {}
    userData['rating'] = int(float(jsonData['rating']))
    userData['commentsCount'] = int(jsonData['comments_count'])
    userData['postsCount'] = int(jsonData['stories_count'])
    userData['hotPostsCount'] = int(jsonData['stories_hot_count'])
    userData['plusesCount'] = int(jsonData['pluses_count'])
    userData['minusesCount'] = int(jsonData['minuses_count'])
    try:
        userData['isRatingBan'] = bool(jsonData['is_rating_ban'])
    except KeyError:
        # TODO: log it
        pass
    try:
        userData['subscribersCount'] = int(jsonData['subscribers_count'])
    except KeyError:
        # TODO: log it
        pass

    return userData
