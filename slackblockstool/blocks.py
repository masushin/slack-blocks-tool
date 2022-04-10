from typing import List
from typing import Union
import json

from typing_extensions import get_origin

"""
Payload
"""

"""
View
"""

"""
Composition Object
"""


class Object:
    def __init__(self):
        pass

    def getDict(self):
        return {}


class ObjectText(Object):
    def __init__(
        self, type: str, text: str, emoji: bool = True, verbatim: bool = False
    ):
        if type == "plain_text" or type == "mrkdwn":
            self.type = type
        else:
            return None
        self.text = text
        self.emoji = emoji
        self.verbatim = verbatim

    def getDict(self):
        payload = super().getDict()
        payload["type"] = self.type
        payload["text"] = self.text
        # payload['emoji'] = self.emoji
        # payload['verbatim'] = self.verbatim
        return payload

    @classmethod
    def create(cls, params: dict) -> Object:
        if "type" in params:
            if params["type"] == "plain_text" or params["type"] == "mrkdwn":
                return ObjectText(type=params["type"], text=params["text"])
        return None


class ObjectPlainText(ObjectText):
    def __init__(self, text: str, emoji: bool = True):
        super().__init__("plain_text", text, emoji, False)


class ObjectMrkdwnText(ObjectText):
    def __init__(self, text: str, verbatim: bool = False):
        super().__init__("mrkdwn", text, True, verbatim)


class ObjectConfirmationDialog(Object):
    def __init__(
        self,
        title: ObjectPlainText,
        text: Union[ObjectPlainText, str],
        confirm: Union[ObjectPlainText, str],
        deny: Union[ObjectPlainText, str],
    ):
        super().__init__()
        self.type = "_object_confirmation_dialog"
        self.title = title
        self.text = ObjectPlainText(text) if type(text) is str else text
        self.confirm = ObjectPlainText(confirm) if type(confirm) is str else confirm
        self.deny = ObjectPlainText(deny) if type(deny) is str else deny

    def getDict(self):
        payload = super().getDict()
        payload["title"] = self.title.getDict()
        payload["text"] = self.text.getDict()
        payload["confirm"] = self.confirm.getDict()
        payload["deny"] = self.deny.getDict()
        return payload

    @classmethod
    def create(cls, params: dict) -> Object:
        return ObjectConfirmationDialog(
            title=ObjectPlainText.create(params["title"]),
            text=ObjectPlainText.create(params["text"]),
            confirm=ObjectPlainText.create(params["confirm"]),
            deny=ObjectPlainText.create(params["deny"]),
        )


class ObjectOption(Object):
    def __init__(
        self,
        text: Union[ObjectPlainText, str],
        value: str,
        description: Union[ObjectPlainText, str] = None,
        url: str = None,
    ):
        super().__init__()
        self.type = "_object_option"
        self.text = ObjectPlainText(text) if type(text) is str else text
        self.value = value
        self.description = (
            ObjectPlainText(description) if type(description) is str else description
        )
        self.url = url

    def getDict(self):
        payload = super().getDict()
        payload["text"] = self.text.getDict()
        payload["value"] = self.value
        if self.description is not None:
            payload["description"] = self.description.getDict()
        if self.url is not None:
            payload["url"] = self.url
        return payload

    @classmethod
    def create(cls, params: dict) -> Object:
        return ObjectOption(
            text=ObjectPlainText.create(params["text"]),
            value=params["value"],
            description=None
            if not "description" in params
            else ObjectPlainText.create(params["description"]),
            url=None if not "url" in params else params["url"],
        )


class ObjectOptionGroup(Object):
    def __init__(self, label: Union[ObjectPlainText, str], options: List[ObjectOption]):
        super().__init__()
        self.type = "_object_option_group"
        self.label = ObjectPlainText(label) if type(label) is str else label
        self.options = options

    def getDict(self):
        payload = super().getDict()
        payload["label"] = self.label.getDict()
        payload["options"] = []
        for option in self.options:
            payload["option"].append(option.getDict())
        return payload

    @classmethod
    def create(cls, params: dict) -> Object:
        return ObjectOptionGroup(
            label=ObjectPlainText.create(params["label"]),
            options=[ObjectOption.create(param) for param in params["options"]],
        )


"""
Block Elements
"""


class Element:
    def __init__(self, type: str):
        self.type = type

    def getDict(self):
        payload = {}
        payload["type"] = self.type
        return payload

    @classmethod
    def create(cls, params: dict):
        if "type" in params:
            if params["type"] == "button":
                return ElementButton.create(params)
            elif params["type"] == "checkboxes":
                return ElementCheckbox.create(params)
            elif params["type"] == "datepicker":
                return ElementDatepicker.create(params)
            elif params["type"] == "timepicker":
                return ElementTimepicker.create(params)
            elif params["type"] == "image":
                return ElementImage.create(params)
            elif params["type"] == "plain_text_input":
                return ElementPlainTextInput.create(params)
            elif params["type"] == "static_select":
                return ElementSelectWithStatic.create(params)
            elif params["type"] == "mrkdwn" or params["type"] == "plain_text":
                return ObjectText.create(params)


class ElementButton(Element):
    TYPE = "button"

    def __init__(
        self,
        text: Union[ObjectText, str],
        action_id: str,
        url: str = None,
        value: str = None,
        style: str = None,
        confirm: ObjectConfirmationDialog = None,
    ):
        super().__init__(self.TYPE)
        self.text = ObjectPlainText(text) if type(text) is str else text
        self.action_id = action_id
        self.url = url
        self.value = value
        self.style = style
        self.confirm = confirm

    def getDict(self):
        payload = super().getDict()
        payload["text"] = self.text.getDict()
        payload["action_id"] = self.action_id
        if self.url is not None:
            payload["url"] = self.url
        if self.value is not None:
            payload["value"] = self.value
        if self.style is not None:
            payload["style"] = self.style
        if self.confirm is not None:
            payload["confirm"] = self.confirm.getDict()
        return payload

    @classmethod
    def create(cls, params: dict) -> Element:
        return ElementButton(
            text=ObjectText.create(params["text"]),
            action_id=params["action_id"],
            url=None if not "url" in params else params["url"],
            value=None if not "value" in params else params["value"],
            style=None if not "style" in params else params["style"],
            confirm=None
            if not "confirm" in params
            else ObjectConfirmationDialog.create(),  # TODO
        )


class ElementCheckbox(Element):
    TYPE = "checkboxes"

    def __init__(
        self,
        action_id: str,
        options: List[ObjectOption],
        initial_options: List[ObjectOption] = None,
        confirm: ObjectConfirmationDialog = None,
    ):
        super().__init__(self.TYPE)
        self.action_id = action_id
        self.options = options
        self.initial_options = initial_options
        self.confirm = confirm

    def getDict(self):
        payload = super().getDict()
        payload["action_id"] = self.action_id
        if self.options is not None:
            payload["options"] = []
            for option in self.options:
                payload["options"].append(option.getDict())
        if self.initial_options is not None:
            payload["initial_options"] = []
            for initial_option in self.initial_options:
                payload["initial_options"].append(initial_option.getDict())
        if self.confirm is not None:
            payload["confirm"] = self.confirm.getDict()
        return payload

    @classmethod
    def create(cls, params: dict) -> Element:
        return ElementCheckbox(
            action_id=params["action_id"],
            options=[ObjectOption.create(param) for param in params["options"]],
            initial_options=None
            if not "initial_options" in params
            else [ObjectOption.create(param) for param in params["initial_options"]],
            confirm=None
            if not "confirm" in params
            else ObjectConfirmationDialog.create(params["confirm"]),
        )


class ElementDatepicker(Element):
    TYPE = "datepicker"

    def __init__(
        self,
        action_id: str,
        placeholder: Union[ObjectText, str] = None,
        initial_date: str = None,
        confirm: ObjectConfirmationDialog = None,
    ):
        super().__init__(self.TYPE)
        self.action_id = action_id
        self.placeholder = (
            ObjectPlainText(placeholder) if type(placeholder) is str else placeholder
        )
        self.initial_date = initial_date
        self.confirm = confirm

    def getDict(self):
        payload = super().getDict()
        payload["action_id"] = self.action_id
        if self.placeholder is not None:
            payload["placeholder"] = self.placeholder.getDict()
        if self.initial_date is not None:
            payload["initial_date"] = self.initial_date
        if self.confirm is not None:
            payload["confirm"] = self.confirm.getDict()
        return payload

    @classmethod
    def create(cls, params: dict) -> Element:
        return ElementDatepicker(
            action_id=params["action_id"],
            placeholder=None
            if not "placeholder" in params
            else ObjectText.create(params["placeholder"]),
            initial_date=None
            if not "initial_date" in params
            else params["initial_date"],
            confirm=None
            if not "confirm" in params
            else ObjectConfirmationDialog.create(params["confirm"]),
        )


class ElementTimepicker(Element):
    TYPE = "timepicker"

    def __init__(
        self,
        action_id: str,
        placeholder: Union[ObjectText, str] = None,
        initial_time: str = None,
        confirm: ObjectConfirmationDialog = None,
    ):
        super().__init__(self.TYPE)
        self.action_id = action_id
        self.placeholder = (
            ObjectPlainText(placeholder) if type(placeholder) is str else placeholder
        )
        self.initial_time = initial_time
        self.confirm = confirm

    def getDict(self):
        payload = super().getDict()
        payload["action_id"] = self.action_id
        if self.placeholder is not None:
            payload["placeholder"] = self.placeholder.getDict()
        if self.initial_time is not None:
            payload["initial_time"] = self.initial_time
        if self.confirm is not None:
            payload["confirm"] = self.confirm.getDict()
        return payload

    @classmethod
    def create(cls, params: dict) -> Element:
        return ElementTimepicker(
            action_id=params["action_id"],
            placeholder=None
            if not "placeholder" in params
            else ObjectText.create(params["placeholder"]),
            initial_time=None
            if not "initial_time" in params
            else params["initial_time"],
            confirm=None
            if not "confirm" in params
            else ObjectConfirmationDialog.create(params["confirm"]),
        )


class ElementImage(Element):
    TYPE = "image"

    def __init__(self, image_url: str, alt_text: str):
        super().__init__(self.TYPE)
        self.image_url = image_url
        self.alt_text = alt_text

    def getDict(self):
        payload = super().getDict()
        payload["image_url"] = self.image_url
        payload["alt_text"] = self.alt_text
        return payload

    @classmethod
    def create(cls, params: dict) -> Element:
        return ElementImage(image_url=params["image_url"], alt_text=params["alt_text"])


class ElementMultiselectWithStatic(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__("")
        pass


class ElementMultiselectWithExternalData(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__("")
        pass


class ElementMultiselectWithUserList(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__("")
        pass


class ElementMultiselectWithConversationsList(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__("")
        pass


class ElementMultiselectWithChannelsList(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__("")
        pass


class ElementOverflow(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__("")
        pass


class ElementPlainTextInput(Element):
    TYPE = "plain_text_input"

    def __init__(
        self,
        action_id: str,
        placeholder: Union[ObjectText, str] = None,
        initial_value: str = None,
        multiline: bool = False,
        min_length: int = None,
        max_length: int = None,
    ):
        super().__init__(self.TYPE)
        self.action_id = action_id
        self.placeholder = (
            ObjectPlainText(placeholder) if type(placeholder) is str else placeholder
        )
        self.initial_value = initial_value
        self.multiline = multiline
        self.min_length = min_length
        self.max_length = max_length

    def getDict(self):
        payload = super().getDict()
        payload["action_id"] = self.action_id
        if self.placeholder is not None:
            payload["placeholder"] = self.placeholder.getDict()
        if self.initial_value is not None:
            payload["initial_value"] = self.initial_value
        payload["multiline"] = self.multiline
        if self.min_length is not None:
            payload["min_length"] = self.min_length
        if self.max_length is not None:
            payload["max_length"] = self.max_length
        return payload

    @classmethod
    def create(cls, params: dict) -> Element:
        return ElementPlainTextInput(
            action_id=params["action_id"],
            placeholder=None
            if not "placeholder" in params
            else ObjectText.create(params["placeholder"]),
            initial_value=None
            if not "initial_value" in params
            else params["initial_value"],
            multiline=False if not "multiline" in params else params["multiline"],
            min_length=None if not "min_length" in params else params["min_length"],
            max_length=None if not "max_length" in params else params["max_length"],
        )


class ElementRadioButton(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__("")
        pass


class ElementSelectWithStatic(Element):
    def __init__(
        self,
        placeholder: Union[ObjectText, str],
        action_id: str,
        options: List[ObjectOption],
        option_groups: List[ObjectOptionGroup] = None,
        initial_option: ObjectOption = None,
        confirm: ObjectConfirmationDialog = None,
    ):
        super().__init__("static_select")
        self.placeholder = (
            ObjectPlainText(placeholder) if type(placeholder) is str else placeholder
        )
        self.action_id = action_id
        self.options = options
        self.option_groups = option_groups
        self.initial_option = initial_option
        self.confirm = confirm

    def getDict(self):
        payload = super().getDict()
        payload["action_id"] = self.action_id
        payload["options"] = []
        for option in self.options:
            payload["options"].append(option.getDict())
        if self.option_groups is not None:
            payload["option_groups"] = []
            for option_group in self.option_groups:
                payload["option_groups"].append(option_group.getDict())
        if self.initial_option is not None:
            payload["initial_option"] = self.initial_option.getDict()
        if self.confirm is not None:
            payload["confirm"] = self.confirm.getDict()
        return payload

    @classmethod
    def create(cls, params: dict) -> Element:
        return ElementSelectWithStatic(
            placeholder=ObjectText.create(params["placeholder"]),
            action_id=params["action_id"],
            options=[ObjectOption.create(param) for param in params["options"]],
            option_groups=None
            if not "option_groups" in params
            else [ObjectOptionGroup.create(param) for param in params["option_groups"]],
            initial_option=None
            if not "initial_option" in params
            else ObjectOption.create(params["initial_option"]),
            confirm=None
            if not "confirm" in params
            else ObjectConfirmationDialog.create(params["confirm"]),
        )


class ElementSelectWithExternalData(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__("")
        pass


class ElementSelectWithUserList(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__("")
        pass


class ElementSelectWithConversationsList(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__("")
        pass


class ElementSelectWithChannelsList(Element):
    """
    not implemented
    """

    def __init__(self):
        super().__init__("")
        pass


"""
Blocks
"""


class Block:
    def __init__(self, type: str, block_id: str = None):
        self.type = type
        self.block_id = block_id

    def getDict(self):
        payload = {}
        payload["type"] = self.type
        if self.block_id is not None:
            payload["block_id"] = self.block_id
        return payload


class BlockSection(Block):
    TYPE = "section"

    def __init__(
        self,
        text: Union[ObjectText, str] = None,
        block_id: str = None,
        fields: List[ObjectText] = None,
        accessory: Element = None,
    ):
        super().__init__(self.TYPE, block_id)
        if text == None:
            self.text = None
        else:
            self.text = ObjectPlainText(text) if type(text) is str else text
        self.fields = fields
        self.accessory = accessory

    def getDict(self):
        payload = super().getDict()
        if self.text != None:
            payload["text"] = self.text.getDict()
        if self.fields is not None:
            payload["fields"] = []
            for field in self.fields:
                payload["fields"].append(field.getDict())
        if self.accessory is not None:
            payload["accessory"] = self.accessory.getDict()
        return payload

    @classmethod
    def create(cls, params: dict) -> Block:
        if "type" in params:
            if params["type"] == cls.TYPE:
                return BlockSection(
                    text=None
                    if not "text" in params
                    else ObjectText.create(params["text"]),
                    block_id=None if not "block_id" in params else params["block_id"],
                    fields=None
                    if not "fields" in params
                    else [ObjectText.create(param) for param in params["fields"]],
                    accessory=None if not "accessory" in params else Element.create(params["accessory"]),
                )


class BlockDivider(Block):
    TYPE = "divider"

    def __init__(self, block_id: str = None):
        super().__init__(self.TYPE, block_id)

    def getDict(self):
        payload = super().getDict()
        return payload

    @classmethod
    def create(cls, params: dict) -> Block:
        return BlockDivider(
            block_id=None if "block_id" in params else params["block_id"]
        )


class BlockImage(Block):
    TYPE = "image"

    def __init__(
        self,
        image_url: str,
        alt_text: str,
        title: Union[ObjectText, str] = None,
        block_id: str = None,
    ):
        super().__init__(self.TYPE, block_id)
        self.image_url = image_url
        self.alt_text = alt_text
        self.title = ObjectPlainText(title) if type(title) is str else title

    def getDict(self):
        payload = super().getDict()
        payload["image_url"] = self.image_url
        payload["alt_text"] = self.alt_text
        payload["title"] = self.title.getDict()
        return payload

    @classmethod
    def create(cls, params: dict) -> Block:
        return BlockImage(
            image_url=params["image_url"],
            alt_text=params["alt_text"],
            title=None if not "title" in params else ObjectText.create(params["title"]),
            block_id=None if not "block_id" in params else params["block_id"],
        )


class BlockAction(Block):
    TYPE = "actions"

    def __init__(self, elements: List[Element], block_id: str = None):
        super().__init__(self.TYPE, block_id)
        self.elements = elements

    def getDict(self):
        payload = super().getDict()
        if self.elements is not None:
            payload["elements"] = []
            for element in self.elements:
                payload["elements"].append(element.getDict())
        return payload

    @classmethod
    def create(cls, params: dict) -> Block:
        return BlockAction(
            elements=[Element.create(param) for param in params["elements"]],
            block_id=None if not "block_id" in params else params["block_id"],
        )


class BlockContext(Block):
    TYPE = "context"

    def __init__(self, elements: List[Element], block_id: str = None):
        super().__init__(self.TYPE, block_id)
        self.elements = elements

    def getDict(self):
        payload = super().getDict()
        if self.elements is not None:
            payload["elements"] = []
            for element in self.elements:
                payload["elements"].append(element.getDict())
        return payload

    @classmethod
    def create(cls, params: dict) -> Block:
        return BlockContext(
            elements=[Element.create(param) for param in params["elements"]],
            block_id=None if not "block_id" in params else params["block_id"],
        )


class BlockInput(Block):
    TYPE = "input"

    def __init__(
        self,
        label: Union[ObjectText, str],
        element: Element,
        block_id: str = None,
        hint: Union[ObjectText, str] = None,
        optional: bool = False,
    ):
        super().__init__(self.TYPE, block_id)
        self.label = ObjectPlainText(label) if type(label) is str else label
        self.element = element
        self.hint = ObjectPlainText(hint) if type(hint) is str else hint
        self.optional = optional

    def getDict(self):
        payload = super().getDict()
        payload["label"] = self.label.getDict()
        payload["element"] = self.element.getDict()
        if self.hint is not None:
            payload["hint"] = self.hint.getDict()
        payload["optional"] = self.optional
        return payload

    @classmethod
    def create(cls, params: dict) -> Block:
        return BlockInput(
            label=ObjectText.create( params["label"] ),
            element=Element.create(params["element"]),
            block_id=None if not "block_id" in params else params["block_id"],
            hint=None if not "hint" in params else ObjectText.create(params["hit"]),
            optional=False if not "optional" in params else params["optional"],
        )


class BlockFile(Block):
    TYPE = "file"

    def __init__(self, external_id: str, source: str, block_id: str = None):
        super().__init__(self.TYPE, block_id)
        self.external_id = external_id
        self.source = source

    def getDict(self):
        payload = super().getDict()
        payload["external_id"] = self.external_id
        payload["source"] = self.source
        return payload

    @classmethod
    def create(cls, params: dict) -> Block:
        return BlockFile(
            external_id=params["external_id"],
            source=params["source"],
            block_id=None if not "block_id" in params else params["block_id"],
        )


class BlockHeader(Block):
    TYPE = "header"

    def __init__(self, text: Union[ObjectPlainText, str], block_id: str = None):
        super().__init__(self.TYPE, block_id)
        self.text = ObjectPlainText(text) if type(text) is str else text

    def getDict(self):
        payload = super().getDict()
        payload["text"] = self.text.getDict()
        return payload

    @classmethod
    def create(cls, params: dict) -> Block:
        return BlockHeader(
            text=ObjectPlainText.create(params["text"]),
            block_id=None if not "block_id" in params else params["block_id"],
        )


"""
Block types
"""


class SlackBlocks:
    def __init__(self, type=None):
        self.type = type
        self.blocks = []
        self.payload = {}

    def addBlocks(self, blocks: List[Block], position=None):
        if position == None:
            for block in blocks:
                self.blocks.append(block)
        else:
            for index, block in enumerate(blocks):
                self.blocks.insert(position + index, block)

    def clearBlocks(self, block_ids: List[str] = None):
        if block_ids == None:
            self.blocks = []
        else:
            for id in block_ids:
                for index, originalBlock in enumerate(self.blocks):
                    if originalBlock.block_id == id:
                            self.blocks.pop(index)

    def getDict(self):
        if self.type is not None:
            self.payload["type"] = self.type
        self.payload["blocks"] = []
        for block in self.blocks:
            self.payload["blocks"].append(block.getDict())
        return self.payload

    def getBlocks(self):
        return self.getDict()

    def getBlockParam(self, block_id) -> dict:
        for block in self.blocks:
            if block.block_id == block_id:
                return block.getDict()
        return None

    def getPosition(self, block_id: str) -> int:
        for index, originalBlock in enumerate(self.blocks):
            if originalBlock.block_id == block_id:
                return index

    def parseBlocks(self, paramsList: List[dict]):

        creationClasses = [
            {"type": BlockSection.TYPE, "func": BlockSection.create},
            {"type": BlockDivider.TYPE, "func": BlockDivider.create},
            {"type": BlockImage.TYPE, "func": BlockImage.create},
            {"type": BlockAction.TYPE, "func": BlockAction.create},
            {"type": BlockContext.TYPE, "func": BlockContext.create},
            {"type": BlockInput.TYPE, "func": BlockInput.create},
            {"type": BlockFile.TYPE, "func": BlockFile.create},
            {"type": BlockHeader.TYPE, "func": BlockHeader.create},
        ]
        self.clearBlocks()
        for param in paramsList:
            for creationClass in creationClasses:
                if param["type"] == creationClass["type"]:
                    block = creationClass["func"](param)
                    if block != None:
                        self.blocks.append(block)

    def replaceBlock(self, blocks: List[Block]):
        for block in blocks:
            for index, originalBlock in enumerate(self.blocks):
                if originalBlock.block_id == block.block_id:
                    self.blocks[index] = block


class Message(SlackBlocks):
    def __init__(self):
        super().__init__("")

    def getDict(self):
        dict = super().getDict()
        return dict["blocks"]


class Modal(SlackBlocks):
    def __init__(
        self,
        title: Union[ObjectText, str],
        callback_id: str = None,
        submit: Union[ObjectText, str] = None,
        close: Union[ObjectText, str] = None,
        private_metadata: str = None,
        clear_on_close: bool = False,
        notify_on_close: bool = False,
        external_id: str = None,
        submit_disabled : bool = False
    ):
        super().__init__("modal")
        self.title = ObjectPlainText(title) if type(title) is str else title
        self.callback_id = callback_id
        self.submit = ObjectPlainText(submit) if type(submit) is str else submit
        self.close = ObjectPlainText(close) if type(close) is str else close
        self.private_metadata = private_metadata
        self.clear_on_close = clear_on_close
        self.notify_on_close = notify_on_close
        self.external_id = external_id
        self.submit_disable = submit_disabled

    def getDict(self):
        payload = super().getDict()
        payload["title"] = self.title.getDict()
        if self.callback_id is not None:
            payload["callback_id"] = self.callback_id
        if self.submit is not None:
            payload["submit"] = self.submit.getDict()
        if self.close is not None:
            payload["close"] = self.close.getDict()
        if self.private_metadata is not None:
            payload["private_metadata"] = self.private_metadata
        payload["clear_on_close"] = self.clear_on_close
        payload["notify_on_close"] = self.notify_on_close
        if self.external_id is not None:
            payload["external_id"] = self.external_id
        return payload
