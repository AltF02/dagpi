import pandas as pd
import random
import string
from tabulate import tabulate

from app.main import tkc
from app.utils.exceptions import InvalidToken, RateLimit


class tokenprocess(object):
    def checkenhanced(self, token):
        df = pd.read_csv("tokens.csv")
        l = df.loc[(df.token == token) & (df.enhanced == 1)]
        if l.empty:
            return False
        else:
            return True

    def randomword(self, length):
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits

        st = "".join(random.choice(letters) for i in range(length))
        return st

    def gettoken(self, userid):
        userid = int(userid)
        df = pd.read_csv('tokens.csv')
        l = df.loc[(df.userid == userid)]
        if l.empty:
            return False, 1
        else:
            return True, l.iloc[0]['token']

    def validtoken(self, token):
        df = pd.read_csv("tokens.csv")
        l = df.loc[(df.token == token)]
        if l.empty:
            return False, 1
        else:
            rt = df[df.token == token].uses
            if int(rt) >= 60:
                return False, 2
            df.loc[(df.token == token), "uses"] += 1
            df.loc[(df.token == token), "totaluses"] += 1
            df.to_csv("tokens.csv", index=False)
            return True, 0

    def showtokens(self):
        df = pd.read_csv("tokens.csv")
        print(tabulate(df.head(), tablefmt="psql"))

    def deluser(self, userid):
        tkst = self.randomword(64)
        df = pd.read_csv("tokens.csv")
        if userid in df["userid"].tolist():
            newdf = df[df.userid != userid]
            newdf.to_csv("tokens.csv", index=False)
            return True
        else:
            return (False, 1)

    def getstats(self):
        df = pd.read_csv('tokens.csv')
        return (df.shape)

    def adduser(self, userid):
        tkst = self.randomword(64)
        df = pd.read_csv("tokens.csv")
        userid = int(userid)
        if userid not in df["userid"].tolist():
            newdf = df.append(
                {"token": tkst, "totaluses": 0, "userid": userid, "uses": 0, "enhanced": 0},
                ignore_index=True,
            )
            newdf.to_csv("tokens.csv", index=False)
            return True, tkst
        if userid in df["userid"].tolist():
            return False, 1
        else:
            return False, 2

    def resetlimits(self):
        df = pd.read_csv("tokens.csv")
        df.loc[df.uses != 0, "uses"] = 0
        df.to_csv("tokens.csv", index=False)
        return True


y = tokenprocess()
stat, co = y.adduser('247292930346319872')
if stat == True:
    print('Added user', co)
elif stat == False:
    if co == 1:
        tok = y.gettoken('491174779278065689')
        print(tok)
    else:
        print('some error occured while adding the token')


# #
# y = tokenprocess()
# print(y.randomword(64))
# try:
#     y.resetlimits()
# except:
#     print('error')

async def check_token(tok):
    y, s = tkc.validtoken(tok)
    print(y)
    print(s)
    if y:
        return y
    else:
        if s == 1:
            raise InvalidToken('Your token is invalid')
        elif s == 2:
            raise RateLimit('Tooo many requests')
        else:
            return False


async def check_enhanced(tok):
    y = tkc.checkenhanced(tok)
    if y:
        return y
    else:
        raise InvalidToken('You do not have an enhanced token. Only admins have this.')
