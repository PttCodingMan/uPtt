
import os
from os import listdir
from os.path import isfile, join
import json

import log


LogPath = None


def log2File(Msg):
    global LogPath
    if LogPath is None:
        desktop = os.path.join(
            os.path.join(
                os.environ['USERPROFILE']
            ),
            'Desktop'
        )

        LogPath = f'{desktop}/uPttLog.txt'

        print(LogPath)

    with open(LogPath, 'a') as f:
        f.write(f'{Msg}\n')


class Type:
    System = 1
    User = 2


class Config:

    Version = '0.0.1'
    QueryCycle = 3.1
    RecoverTime = 2
    Port = 50732
    HttpPort = 57983
    PttLogHandler = None
    PttLogLevel = log.Level.INFO

    def __init__(self):
        # 不想給使用者改的設定值就寫在這兒
        # 想給使用者改的就透過 setValue
        # 因為會被存起來

        self.ConfigFileName = 'config.txt'
        self.FriendFileName = 'friend.txt'

        self.ConfigPath = None
        self.friendlist = None

        if os.name == 'nt':
            log.showvalue(
                'Config',
                log.Level.INFO,
                '作業系統',
                'Windows'
            )
            self.ConfigPath = 'C:/ProgramData/uPtt'

        self.ConfigFullPath = self.ConfigPath + self.ConfigFileName
        self.UserConfigPath = None

        if not os.path.exists(self.ConfigPath):
            os.makedirs(self.ConfigPath)

        try:
            with open(self.ConfigFullPath, encoding='utf8') as File:
                self.SystemData = json.load(File)
        except FileNotFoundError:
            self.SystemData = dict()

        self.UserData = dict()

        log.showvalue(
            'Config',
            log.Level.INFO,
            '設定檔',
            '初始化'
        )

    def initUser(self, ID):
        self.id = ID
        self.UserConfigPath = f'{self.ConfigPath}/{ID}/{self.ConfigFileName}'
        if not os.path.exists(f'{self.ConfigPath}/{ID}'):
            os.makedirs(f'{self.ConfigPath}/{ID}')
        else:
            if os.path.exists(f'{self.ConfigPath}/{self.id}/dialogue/'):

                dialogpath = f'{self.ConfigPath}/{self.id}/dialogue/'
                self.dialogfiles = [join(dialogpath, f) for f in listdir(
                    dialogpath) if isfile(join(dialogpath, f))]

                self.dialogfiles = [
                    x for x in self.dialogfiles if x.endswith('.txt')]

                log.showvalue(
                    'Config',
                    log.Level.INFO,
                    '對話紀錄檔案',
                    self.dialogfiles
                )

            fname = f'{self.ConfigPath}/{self.id}/{self.FriendFileName}'
            if os.path.exists(fname):
                log.showvalue(
                    'Config',
                    log.Level.INFO,
                    '載入朋友清單',
                    self.dialogfiles
                )

                try:
                    with open(fname, encoding='utf8') as f:
                        self.friendlist = json.load(f)
                except Exception as e:

                    log.show(
                        'Config',
                        log.Level.INFO,
                        e.__traceback__.__str__()
                    )
                    log.show(
                        'Config',
                        log.Level.INFO,
                        e.__str__()
                    )

                    log.show(
                        'Config',
                        log.Level.INFO,
                        f'無法讀取 {fname}'
                    )
                    self.friendlist = None

        try:
            with open(self.UserConfigPath, encoding='utf8') as File:
                self.UserData = json.load(File)
        except FileNotFoundError:
            pass

    def getValue(self, inputType, Key):

        if inputType == Type.System:
            if Key not in self.SystemData:
                return None
            return self.SystemData[Key]
        elif inputType == Type.User:
            if Key not in self.UserData:
                return None
            return self.UserData[Key]

    def setValue(self, inputType, Key, Value):

        if inputType == Type.System:
            if Value is not None:
                self.SystemData[Key] = Value
            elif Key in self.SystemData:
                del self.SystemData[Key]

            with open(self.ConfigFullPath, 'w', encoding='utf8') as File:
                json.dump(self.SystemData, File, indent=4, ensure_ascii=False)

        if inputType == Type.User:
            if Value is not None:
                self.UserData[Key] = Value
            elif Key in self.UserData:
                del self.UserData[Key]

            with open(self.UserConfigPath, 'w', encoding='utf8') as File:
                json.dump(self.UserData, File, indent=4, ensure_ascii=False)

    def saveDialogue(self, target, msglist):
        filepath = f'{self.ConfigPath}/{self.id}/dialogue/{target}.txt'
        if not os.path.exists(f'{self.ConfigPath}/{self.id}/dialogue/'):
            os.makedirs(f'{self.ConfigPath}/{self.id}/dialogue/')

        with open(filepath, 'w', encoding='utf8') as f:
            json.dump(
                msglist,
                f,
                indent=4,
                ensure_ascii=False
            )