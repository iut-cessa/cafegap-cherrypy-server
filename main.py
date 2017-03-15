#! /usr/bin/env python3

import json
import cherrypy
from cherrypy import tools
from hashlib import sha256
from datetime import datetime

class Constants:
    ADMINS_FILENAME = "staff.json"
    PARTICIPANTS_FILENAME = "participants.json"
    IP_ADDRESS = "172.16.6.54"
    PORT_NUMBER = 8080


class IUTCafeGap:
    def log(self, message):
        self.__log.write('{} : {}\n'.format(datetime.today().ctime(), message))
        self.__log.flush()

    @cherrypy.expose
    def __init__(self, users={}, database={}):
        super().__init__()
        self.__users = users
        self.__log = open('server.log', 'a+')

    @cherrypy.expose
    @tools.json_out()
    def check(self, username=None, secret=None):
        self.log('Login with username: {}, secret: {}'.format(username, secret))
        status = 'Error'

        try:
            if username is not None and secret is not None:
                if username in self.__users and sha256(self.__users[username].encode()).hexdigest() == secret:
                    self.log('\tLogin was successful.')
                    status = 'Ok'
        except:
            self.log('\tLogin faild!')

        return {"Status": status}

    @cherrypy.expose
    @tools.json_out()
    def info(self, username=None, part_id=None, auth=None):
        self.log('Get info username: {}, part_id: {}, auth: {}'.format(username, part_id, auth))
        try:
            if sha256((username + part_id + self.__users[username]).encode()).hexdigest() == auth:
                participants = json.loads(open(Constants.PARTICIPANTS_FILENAME).read())
                ret = {"Status": "Ok"}
                ret.update(participants[part_id])
                self.log('\tInformation sent. Info: {}'.format(ret))
                return ret
            else:
                self.log('\tAuthentication failed!')
                return {"Status": "Error"}
        except:
            self.log('\tException happened!!')
            return {"Status": "Error"}

    @cherrypy.expose
    @tools.json_out()
    def update(self, username=None, part_id=None, parameter=None, value=None, auth=None):
        self.log('Update username: {}, part_id: {}, parameter: {}, value: {}, auth: {}'.format(username, part_id, parameter, value, auth))
        try:
            if sha256((username + part_id + parameter + value + self.__users[username]).encode()).hexdigest() == auth:
                participants = json.loads(open(Constants.PARTICIPANTS_FILENAME).read())
                participants[part_id][parameter] = (value == "true")
                open(Constants.PARTICIPANTS_FILENAME, 'w').write(json.dumps(participants, indent=4, sort_keys=True))
                self.log('\tInformation updated successfully.')
                return {"Status": "Ok"}
            else:
                self.log('\tAuthentication failed!')
        except:
            self.log('\tException happened!!')
            return {"Status": "Error"}


if __name__ == "__main__":
    cherrypy.config.update({
        'server.socket_host': Constants.IP_ADDRESS,
        'server.socket_port': Constants.PORT_NUMBER
    })

    users = json.loads(open(Constants.ADMINS_FILENAME).read())
    database = json.loads(open(Constants.PARTICIPANTS_FILENAME).read())
    cherrypy.quickstart(IUTCafeGap(users=users, database=database))

