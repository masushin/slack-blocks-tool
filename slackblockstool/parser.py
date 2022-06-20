import json
import base64
import datetime
import zlib
import logging

class MetaDataParser:
    def __init__(self, key:str=""):
        '''
        self.key = generate_secret_key(key)
        self.cipher = AESCipher(key=self.key)
        '''
        self.key = key

    '''
    def cencode(self, d:dict) -> str:
        compressed = zlib.compress(json.dumps(d).encode())
        base64_encoded = base64.b64encode(compressed)
        logging.info("b:{}".format(base64_encoded))
        encrypted = self.cipher.encrypt(base64_encoded.decode())
        logging.info("e:{}".format(encrypted))
        return base64_encoded

    def cdecode(self, s:str) -> dict:
        logging.info("d:{}".format(s))        
        base64_decoded = base64.b64decode(s)
        uncompressed = zlib.decompress(base64_decoded)
        return json.loads(uncompressed.decode())
    '''

    @staticmethod
    def encode(d: dict) -> str:
        return base64.b64encode(json.dumps(d).encode()).decode()

    @staticmethod
    def decode(s: str) -> dict:
        return json.loads(base64.b64decode(s.encode()).decode())


class SubmissionValue:
    def __init__(self, type: str) -> None:
        self.type = type


class SubmissionValuePlainTextInput(SubmissionValue):
    def __init__(self, value: str) -> None:
        super().__init__(type="plain_text_input")
        self.value = value


class SubmissionValueDatePicker(SubmissionValue):
    def __init__(self, value: str) -> None:
        super().__init__(type="datepicker")
        self.value = value
        self.date_time = datetime.datetime.strptime(value, "%Y-%m-%d")
        self.date = datetime.date(year=self.date_time.year, month=self.date_time.month, day=self.date_time.day)


class SubmissionValueTimePicker(SubmissionValue):
    def __init__(self, value: str) -> None:
        super().__init__(type="timepicker")
        self.value = value
        self.time = datetime.time.fromisoformat("{}:00".format(value))


class SubmissionValueCheckBoxes(SubmissionValue):
    def __init__(self, selected_options: list) -> None:
        super().__init__(type="checkboxes")
        self.selected_options = selected_options
        self.values = {}
        for option in self.selected_options:
            self.values[option["value"]] = option

    def isSelected(self, value: str) -> bool:
        if value in self.values:
            return True
        else:
            return False



class SubmissionParser:
    def __init__(self, payload) -> None:
        self.payload = payload

    def getValue(self, action_id, block_id=None):
        blocks = self.payload["view"]["state"]["values"]
        for block in blocks:
            if block_id == None or block == block_id:
                for action in blocks[block]:
                    if action == action_id:
                        if blocks[block][action]["type"] == "plain_text_input":
                            return SubmissionValuePlainTextInput(
                                blocks[block][action]["value"]
                            )
                        elif blocks[block][action]["type"] == "checkboxes":
                            selected = {}
                            selected["type"] = "checkboxes"
                            return SubmissionValueCheckBoxes(
                                blocks[block][action]["selected_options"]
                            )
                        elif blocks[block][action]["type"] == "datepicker":
                            return SubmissionValueDatePicker(
                                blocks[block][action]["selected_date"]
                            )
                        elif blocks[block][action]["type"] == "timepicker":
                            return SubmissionValueTimePicker(
                                blocks[block][action]["selected_time"]
                            )
        return None