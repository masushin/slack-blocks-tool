import os
import logging
import slack_sdk

import re

class SlackEventFunc:
    def __init__(self, eventType:str, id: str, func: callable):
        self.eventType = eventType
        self.func = func
        self.id = id


class SlackEventFuncList:
    def __init__(self):
        self.functions = []

    def addFunc(self, eventFunc: SlackEventFunc):
        self.functions.append(eventFunc)

    def getFunc(self, type: str, id: str):
        for efunc in self.functions:
            if type == efunc.eventType and re.fullmatch(efunc.id, id) != None:
                return efunc.func
        return None


class SlackEventHandler:
    def __init__(self, bot_token: str = None):
        self.funclist = SlackEventFuncList()
        self.bot_token = bot_token
        self.client = slack_sdk.WebClient(token=self.bot_token)

    def event_shortcut(self, id):
        def _event(func):
            self.funclist.addFunc(SlackEventFunc("shortcut", id, func))

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return _event

    def event_view_submission(self, id):
        def _event(func):
            self.funclist.addFunc(SlackEventFunc("view_submission", id, func))
        return _event

    def event_block_actions(self, id):
        def _event(func):
            self.funclist.addFunc(SlackEventFunc("block_actions", id, func))
        return _event

    def event_message_actions(self, id):
        def _event(func):
            logging.info("addFunc [message_action] {}".format(id))
            self.funclist.addFunc(SlackEventFunc("message_action", id, func))
        return _event

    def event_slash_command(self, id):
        def _event(func):
            self.funclist.addFunc(SlackEventFunc("slach_command", id, func))
        return _event

    

    def handler(self, param: dict):
        if "type" in param:
            type = param["type"]

            if type == "shortcut":
                func = self.funclist.getFunc(type, param["callback_id"])
                if func == None:
                    logging.warning("Undefined Event 1: {}".format(param))
                    return None
                return func(payload=param, client=self.client)
            elif type == 'view_submission':
                func = self.funclist.getFunc(
                    type, param["view"]["callback_id"]
                )
                if func == None:
                    logging.warning("Undefined Event 2: {}".format(param))
                    return None
                return func(payload=param, client=self.client)
            elif type == 'message_action':
                logging.info("[Message Action] {}".format(param['callback_id']))
                func = self.funclist.getFunc(type, param["callback_id"])
                if func == None:
                    logging.warning("Undefined Event 3: {}".format(param))
                    return None
                return func(payload=param, client=self.client)
            elif type == 'block_actions':
                actions = param['actions']
                for action in actions:
                    func = self.funclist.getFunc(
                        type, action['action_id']
                    )
                    if func is not None:
                        return func(payload=param, client=self.client, action_id=action['action_id'])
        elif "command" in param:
            type = "slach_command"
            func = self.funclist.getFunc(type, param['command'])
            if func == None:
                logging.warning("Undefined Event SlashCommand: {}".format(param))
                return None
            return func(payload=param, client=self.client)




        logging.warning('Undefined Event x: {}'.format(param))
        return None

