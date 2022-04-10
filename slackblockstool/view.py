from typing import List
import slack_sdk
import blocks as sb
from blocks import ObjectMrkdwnText as MText
from blocks import ObjectPlainText as PText

class SlackViewParts:
    def __init__(self, name: str, blocks: List[sb.Block], visible: bool = True):
        self.name = name
        self.blocks = blocks
        self.visible = visible


class SlackView:
    def __init__(self, client:slack_sdk.WebClient):
        self.parts = []
        self.client = client
        self.modal = self._defaultModal()
        self._defaultPart()

    def _defaultModal(self) -> sb.Modal:
        return sb.Modal(title=PText("Slack"), close=PText("Close"))

    def _defaultPart(self):
        pass

    def _getPartIndex(self, name: str):
        if name == "none":
            return -1
        for i, value in enumerate(self.parts):
            if value.name == name:
                return i
        return -1

    def updateModal(self, modal:sb.Modal):
        self.modal = modal


    def open(self, trigger_id:str):
        self.modal.clearBlocks()
        for part in self.parts:
            if part.visible is True:
                self.modal.addBlocks(blocks=part.blocks)
        ret = self.client.views_open(trigger_id=trigger_id, view=self.modal.getDict())
        return ret

    def update(self, view_id:str):
        self.modal.clearBlocks()
        for part in self.parts:
            if part.visible is True:
                self.modal.addBlocks(blocks=part.blocks)
        ret = self.client.views_update(view_id=view_id, view=self.modal.getDict())
        return ret

    def addPart(self, name: str, blocks: List[sb.Block] = [], position: str = None, visible:bool = True):
        if position == None:
            self.parts.append(SlackViewParts(name=name, blocks=blocks, visible=visible))
        else:
            index = self._getPartIndex(name=position)
            if index is not -1:
                self.parts.insert(index, SlackViewParts(name=name, blocks=blocks, visible=visible))

    def setPart(self, blocks: List[sb.Block], name: str, visible:bool=True):
        index = self._getPartIndex(name=name)
        if index is not -1:
            self.parts[index] = SlackViewParts(name=name, blocks=blocks, visible=visible)

    def removePart(self, name: str = None):
        if name == None:
            self.parts = []
        else:
            index = self._getPartIndex(name=name)
            if index is not -1:
                self.parts.pop(index)

    def setVisible(self, name: str, visible: bool):
        index = self._getPartIndex(name=name)
        if index is not -1:
            self.parts[index].visible = visible

