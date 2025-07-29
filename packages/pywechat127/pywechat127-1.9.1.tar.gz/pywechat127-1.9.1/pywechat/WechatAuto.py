'''
WechatAuto
-------
模块:\n
---------------
Messages: 5种类型的发送消息功能包括:单人单条,单人多条,多人单条,多人多条,转发消息:多人同一条消息\n
Files: 5种类型的发送文件功能包括:单人单个,单人多个,多人单个,多人多个,转发文件:多人同一个文件\n
FriendSettings: 涵盖了PC微信针对某个好友的全部操作\n
GroupSettings: 涵盖了PC微信针对某个群聊的全部操作\n
Contacts:获取微信好友详细信息(昵称,备注,地区，标签,个性签名,共同群聊,微信号,来源),\n
获取微信好友的信息(昵称,备注,微信号),获取微信好友的名称(昵称,备注),获取企业号微信信息(好友名称,企业名称),获取群聊信息(群聊名称与人数)\n
Call: 给某个好友打视频或语音电话\n
AutoReply:包含对指定好友的AI自动回复消息,自动回复指定消息,以及自动接听语音或视频电话\n
WeChatSettings: 修改PC微信设置\n
----------------------------------
函数:\n
函数为上述模块内的所有方法\n
--------------------------------------
使用该pywechat时,你可以导入模块,使用模块内的方法:\n
```s
from pywechat.WechatAuto import Messages
Messages.send_messages_to_friend()
```
或者直接导入与方法名一致的函数\n
```
from pywechat import send_messages_to_friend
send_messages_to_friend()
```
或者将模块重命名后,使用别名.函数名的方式\n
```
from pywechat import WechatAuto as wechat
wechat.send_messages_to_friend()来进行使用
```
'''
#################################################################
#微信主界面:
#==========================================================================================
#工具栏 |搜索|       |+|添加好友              ···聊天信息按钮  #
#                                             |
#|头像|   |          |                            |
#|聊天|   |          |                            |
#|通讯录|  | 会话列表     |                            |
#|收藏|   |          |    聊天界面                    |
#|聊天文件| |          |                            |
#|朋友圈|  |          |                            |
#|视频号|  |          |                            |
#|看一看|  |          |                            |
#|搜一搜|  |          |                            |
#      |          |                            |
#      |          |                            |
#      |          |                            | 
#      |          |---------------------------------------------------------
#小程序面板 |          |  表情 聊天文件 截图 聊天记录           |
#|手机|   |          |                            |
#|设置及其他||          |                            |
#===========================================================================================

#########################################依赖环境#####################################
import os 
import re
import time
import json
import pyautogui
from warnings import warn
from .Warnings import LongTextWarning,ChatHistoryNotEnough
from .WechatTools import Tools,mouse,Desktop
from .WinSettings import Systemsettings
from .Errors import NoWechat_number_or_Phone_numberError
from .Errors import HaveBeenSetChatonlyError
from .Errors import HaveBeenSetUnseentohimError
from .Errors import HaveBeenSetDontseehimError
from .Errors import PrivacyNotCorrectError
from .Errors import EmptyFileError
from .Errors import EmptyFolderError
from .Errors import NotFileError
from .Errors import NotFolderError
from .Errors import CantCreateGroupError
from .Errors import NoPermissionError
from .Errors import SameNameError
from .Errors import AlreadyCloseError
from .Errors import AlreadyInContactsError
from .Errors import EmptyNoteError
from .Errors import NoChatHistoryError
from .Errors import CantSendEmptyMessageError
from .Errors import WrongParameterError
from .Errors import TimeNotCorrectError
from .Errors import TickleError
from .Errors import ElementNotFoundError
from .Errors import CantReplyToOfficialAccountError
from .Uielements import (Main_window,SideBar,Independent_window,Buttons,
Edits,Texts,TabItems,Lists,Panes,Windows,CheckBoxes,MenuItems,Menus)
from .WechatTools import match_duration
#######################################################################################
language=Tools.language_detector()#有些功能需要判断语言版本
Main_window=Main_window()#主界面UI
SideBar=SideBar()#侧边栏UI
Independent_window=Independent_window()#独立主界面UI
Buttons=Buttons()#所有Button类型UI
Edits=Edits()#所有Edit类型UI
Texts=Texts()#所有Text类型UI
TabItems=TabItems()#所有TabIem类型UI
Lists=Lists()#所有列表类型UI
Panes=Panes()#所有Pane类型UI
Windows=Windows()#所有Window类型UI
CheckBoxes=CheckBoxes()#所有CheckBox类型UI
MenuItems=MenuItems()#所有MenuItem类型UI
Menus=Menus()#所有Menu类型UI
pyautogui.FAILSAFE=False#防止鼠标在屏幕边缘处造成的误触
class Messages():
    @staticmethod
    def send_message_to_friend(friend:str,message:str,delay:float=1,tickle:bool=False,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于给单个好友或群聊发送单条信息\n
        Args:
            friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
            message:\t待发送消息。格式:message="消息"\n
            tickle:\t是否在发送消息或文件后拍一拍好友,默认为False\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            delay:\t发送单条消息延迟,单位:秒/s,默认1s。\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        if len(message)==0:
            raise CantSendEmptyMessageError
        #先使用open_dialog_window打开对话框
        chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        if is_maximize:
            main_window.maximize()
        chat.click_input()
        #字数超过2000字直接发txt
        if len(message)<2000:
            Systemsettings.copy_text_to_windowsclipboard(message)
            pyautogui.hotkey('ctrl','v')
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        elif len(message)>2000:
            Systemsettings.convert_long_text_to_txt(message)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)    
        if tickle:
            tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
        time.sleep(1)
        if close_wechat:
            main_window.close()

    @staticmethod
    def send_messages_to_friend(friend:str,messages:list[str],tickle:bool=False,delay:float=1,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于给单个好友或群聊发送多条信息\n
        Args:
            friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
            message:\t待发送消息列表。格式:message=["发给好友的消息1","发给好友的消息2"]\n
            tickle:\t是否在发送消息或文件后拍一拍好友,默认为False\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            delay\t:发送单条消息延迟,单位:秒/s,默认1s。\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        if not messages:
            raise CantSendEmptyMessageError
        #先使用open_dialog_window打开对话框
        chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        chat.click_input()
        for message in messages:
            if len(message)==0:
                main_window.close()
                raise CantSendEmptyMessageError
            if len(message)<2000:
                Systemsettings.copy_text_to_windowsclipboard(message)
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
            elif len(message)>2000:#字数超过200字发送txt文件
                Systemsettings.convert_long_text_to_txt(message)
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
                warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
        if tickle:
            tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
        time.sleep(1)
        if close_wechat:
            main_window.close()

    @staticmethod
    def send_messages_to_friends(friends:list[str],messages:list[list[str]],tickle:list[bool]=[],delay:float=1,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于给多个好友或群聊发送多条信息\n
        Args:
            friends:\t好友或群聊备注列表,格式:firends=["好友1","好友2","好友3"]。\n
            messages:\t待发送消息,格式: message=[[发给好友1的多条消息],[发给好友2的多条消息],[发给好友3的多条信息]]。\n
            tickle:\t是否给每一个好友发送消息或文件后拍一拍好友,格式为:[True,True,False,...]的bool值列表,与friends列表中的每一个好友对应\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            delay:\t发送单条消息延迟,单位:秒/s,默认1s。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        注意!messages与friends长度需一致,并且messages内每一个列表顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
        '''
        #多个好友的发送任务不需要使用open_dialog_window方法了直接在顶部搜索栏搜索,一个一个打开好友的聊天界面，发送消息,这样最高效
        Chats=dict(zip(friends,messages))
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        i=0
        for friend in Chats:
            search=main_window.child_window(**Main_window.Search)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(1)
            pyautogui.press('enter')
            chat=main_window.child_window(title=friend,control_type='Edit')
            chat.click_input()
            for message in Chats.get(friend):
                if len(message)==0:
                    main_window.close()
                    raise CantSendEmptyMessageError
                if len(message)<2000:
                    Systemsettings.copy_text_to_windowsclipboard(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                elif len(message)>2000:#字数超过2000字直接发txt
                    Systemsettings.convert_long_text_to_txt(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                    warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
            if tickle:
                if tickle[i]:
                    tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
                i+=1
        time.sleep(1)
        if close_wechat:
            main_window.close()

    @staticmethod
    def send_message_to_friends(friends:list[str],message:list[str],tickle:list[bool]=[],delay:float=1,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于给每friends中的一个好友或群聊发送message中对应的单条信息\n
        Args:
            friends:\t好友或群聊备注。格式:friends=["好友1","好友2","好友3"]\n
            message:\t待发送消息,格式: message=[发给好友1的多条消息,发给好友2的多条消息,发给好友3的多条消息]。\n
            tickle:\t是否给每一个好友发送消息或文件后拍一拍好友,格式为:[True,True,False,...]的bool值列表,与friends列表中的每一个好友对应\n
            delay:\t发送单条消息延迟,单位:秒/s,默认1s。\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        注意!message与friends长度需一致,并且messages内每一条消息顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
        '''
        #多个好友的发送任务不需要使用open_dialog_window方法了直接在顶部搜索栏搜索,一个一个打开好友的聊天界面，发送消息,这样最高效
        Chats=dict(zip(friends,message))
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        time.sleep(1)
        i=0
        for friend in Chats:
            search=main_window.child_window(**Main_window.Search)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(1)
            pyautogui.press('enter')
            chat=main_window.child_window(title=friend,control_type='Edit')
            chat.click_input()
            #字数超过2000字直接发txt
            if len(Chats.get(friend))==0:
                main_window.close()
                raise CantSendEmptyMessageError
            if len(Chats.get(friend))<2000:
                Systemsettings.copy_text_to_windowsclipboard(Chats.get(friend))
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
            elif len(Chats.get(friend))>2000:
                Systemsettings.convert_long_text_to_docx(Chats.get(friend))
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
                warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
            if tickle:
                if tickle[i]:
                    tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
                i+=1
        time.sleep(1)
        if close_wechat:
            main_window.close()

    @staticmethod
    def forward_message(friends:list[str],message:str,delay:float=0.8,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于给好友转发消息,实际使用时建议先给文件传输助手转发\n
        这样可以避免对方聊天信息更新过快导致转发消息被'淹没',进而无法定位出错的问题。\n
        Args:
            friends:\t好友或群聊备注列表。格式:friends=["好友1","好友2","好友3"]\n
            message:\t待发送消息,格式: message="转发消息"。\n
            delay:\t搜索好友等待时间\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            search_pages:\t在会话列表中查询查找带转发消息的第一个好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        def right_click_message():
            max_retry_times=25
            retry_interval=0.2
            counter=0
            #查找最新的我自己发的消息，并右键单击我发送的消息，点击转发按钮
            chatList=main_window.child_window(**Main_window.FriendChatList)
            myname=main_window.child_window(**Buttons.MySelfButton).window_text()
            #if message.descendants(conrol_type)是用来筛选这个消息(control_type为ListItem)内有没有按钮(消息是人发的必然会有头像按钮这个UI,系统消息比如'8:55'没有这个UI)
            chats=[chat for chat in chatList.children(control_type='ListItem') if chat.descendants(control_type='Button')]#不包括时间戳和系统消息
            sent_message=[sent_message for sent_message in chats if sent_message.descendants(control_type='Button')[-1].window_text()==myname]
            while not sent_message and sent_message[-1].is_visible():#如果聊天记录页为空或者我发过的最后一条消息(转发的消息)不可见(可能是网络延迟发送较慢造成，也不排除是被顶到最上边了)
                chats=[chat for chat in chatList.children(control_type='ListItem') if chat.descendants(control_type='Button')]#不包括时间戳和系统消息,只有是好友发送的时候，这个消息内部才有(Button属性)
                sent_message=[sent_message for sent_message in chats if sent_message.descendants(control_type='Button')[-1].window_text()==myname]
                time.sleep(retry_interval)
                counter+=1
                if counter>max_retry_times: 
                    raise TimeoutError
            button=sent_message[-1].children()[0].children()[1]
            button.right_click_input()
            menu=main_window.child_window(**Menus.RightClickMenu)
            select_contact_window=main_window.child_window(**Main_window.SelectContactWindow)
            if not select_contact_window.exists():
                while not menu.exists():
                    button.right_click_input()
                    time.sleep(0.2)
            forward=menu.child_window(**MenuItems.ForwardMenuItem)
            while not forward.exists():
                main_window.click_input()
                button.right_click_input()
                time.sleep(0.2)
            forward.click_input()
            select_contact_window.child_window(**Buttons.MultiSelectButton).click_input()   
            send_button=select_contact_window.child_window(**Buttons.SendRespectivelyButton)
            search_button=select_contact_window.child_window(**Edits.SearchEdit)
            return search_button,send_button
        if len(message)==0:
            raise CantSendEmptyMessageError
        chat,main_window=Tools.open_dialog_window(friends[0],wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        #超过2000字发txt
        if len(message)<2000:
            chat.click_input()
            Systemsettings.copy_text_to_windowsclipboard(message)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        elif len(message)>2000:
            chat.click_input()
            Systemsettings.convert_long_text_to_txt(message)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
        friends=friends[1:]
        #转发消息一次只能转发9个好友,当转发好友人数超过9时需要9个9个分批发送
        if len(friends)<=9:
            search_button,send_button=right_click_message()
            for other_friend in friends:
                search_button.click_input()
                Systemsettings.copy_text_to_windowsclipboard(other_friend)
                pyautogui.hotkey('ctrl','v')
                time.sleep(delay)
                pyautogui.press('enter')
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('backspace')
                time.sleep(delay)
            send_button.click_input()
        else:  
            res=len(friends)%9#余数
            for i in range(0,len(friends),9):#9个一批
                if i+9<=len(friends):
                    search_button,send_button=right_click_message()
                    for other_friend in friends[i:i+9]:
                        search_button.click_input()
                        Systemsettings.copy_text_to_windowsclipboard(other_friend)
                        pyautogui.hotkey('ctrl','v')
                        time.sleep(delay)
                        pyautogui.press('enter')
                        pyautogui.hotkey('ctrl','a')
                        pyautogui.press('backspace')
                        time.sleep(delay)
                    send_button.click_input()
                else:
                    pass
            if res:
                search_button,send_button=right_click_message()
                for other_friend in friends[len(friends)-res:len(friends)]:
                    search_button.click_input()
                    Systemsettings.copy_text_to_windowsclipboard(other_friend)
                    pyautogui.hotkey('ctrl','v')
                    time.sleep(delay)
                    pyautogui.press('enter')
                    pyautogui.hotkey('ctrl','a')
                    pyautogui.press('backspace')
                    time.sleep(delay)
                send_button.click_input()
        time.sleep(1)
        if close_wechat:
            main_window.close()

    @staticmethod
    def check_new_message(duration:str=None,wechat_path:str=None,close_wechat:bool=True):
        '''
        该方法用来查看新消息,若你传入了duration参数,那么可以用来监听新消息\n
        注意,使用该功能需要开启文件传输助手功能,为了更好监听新消息,需要切换聊天界面至文件传输助手\n
        否则当前聊天界面内的新消息无法监控\n
        当你传入duration后如出现偶尔停顿此为正常等待机制:每遍历一次会话列表会停顿一小段时间等待新消息\n
        Args:
            duration:\t监听消息持续时长,格式:'s','min','h'单位:s/秒,min/分,h/小时\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        Returns:
            新消息json or 未查找到任何新消息\n
            json格式:[{'名称':'好友备注','新消息条数',25:'类型':'群聊or个人or公众号','消息':[str]}]\n
        '''
        #先遍历消息列表查找是否存在新消息,然后在遍历一遍消息列表,点击具有新消息的好友，记录消息，没有直接返回'未查找到任何新消息'
        Names=[]#有新消息的好友名称
        Nums=[]#与Names中好友一一对应的消息条数
        search_pages=1#在聊天列表中查找新消息好友位置时遍历的,初始为1,如果有新消息的话,后续会变化
        if language=='简体中文':
            pattern=r'\[语音\]\d+秒'
            filetransfer='文件传输助手'
        if language=='英文':
            pattern=r'\[Audio\]\d+s'
            filetransfer='File Transfer'
        if language=='繁体中文':
            pattern=r'\[語音\]\d+秒'
            filetransfer='檔案傳輸'
        def ConvertMessages(Messages,type):
            #用来获取开启语音转文字后新消息中语音转文字结果
            for i in range(len(Messages)):
                if re.match(pattern,Messages[i].window_text()):#匹配是否是语音消息
                    try:#是语音消息就定位语音转文字结果
                        if type=='群聊':
                            result=Messages[i].descendants(control_type='Text')[2].window_text()
                            Messages[i]=Messages[i].window_text()+f'  消息内容:{result}'
                        else:
                            result=Messages[i].descendants(control_type='Text')[1].window_text()
                            Messages[i]=Messages[i].window_text()+f'  消息内容:{result}'
                    except Exception:#定位时不排除有人只发送[语音]\d+秒这样的文本消息，所以可能出现异常
                        Messages[i]=Messages[i].window_text()
                else:#不是语音消息直接获取文本
                    Messages[i]=Messages[i].window_text()
            return Messages
        
        def get_message_content(name,number,search_pages):
            Messages=[]
            main_window=Tools.find_friend_in_MessageList(friend=name,search_pages=search_pages)[1]
            check_more_messages_button=main_window.child_window(**Buttons.CheckMoreMessagesButton)
            voice_call_button=main_window.child_window(**Buttons.VoiceCallButton)#语音聊天按钮
            video_call_button=main_window.child_window(**Buttons.VideoCallButton)#视频聊天按钮
            if voice_call_button.exists() and not video_call_button.exists():#只有语音和聊天按钮没有视频聊天按钮是群聊
                type='群聊' 
                chatList=main_window.child_window(**Main_window.FriendChatList)
                x,y=chatList.rectangle().left+10,(main_window.rectangle().top+main_window.rectangle().bottom)//2
                messages=chatList.children(control_type='ListItem')
                Messages.extend([message for message in messages  if not re.match(r'\d+:\d+',message.window_text())])
                #点击聊天区域侧边栏靠里一些的位置,依次来激活滑块,不直接main_window.click_input()是为了防止点到消息
                mouse.click(coords=(x,y))
                #按一下pagedown到最下边
                pyautogui.press('pagedown')
                ########################
                #需要先提前向上遍历一遍,防止语音消息没有转换完毕
                if number<=10:#10条消息最多先向上遍历3页
                    pages=number//3
                else:
                    pages=number//2
                for _ in range(pages):
                    if check_more_messages_button.exists():
                        check_more_messages_button.click_input()
                        mouse.click(coords=(x,y))
                    pyautogui.press('pageup',_pause=False)
                pyautogui.press('End')
                mouse.click(coords=(x,y))
                pyautogui.press('pagedown')
                ##################################
                #开始记录
                while len(list(set(Messages)))<number:
                    if check_more_messages_button.exists():
                        check_more_messages_button.click_input()
                        mouse.click(coords=(x,y))
                    pyautogui.press('pageup',_pause=False)
                    messages=chatList.children(control_type='ListItem')
                    Messages.extend([message for message in messages if not re.match(r'\d+:\d+',message.window_text())])
                #######################################################
                Messages=ConvertMessages(Messages,type)#将listitem转换为文本内容
                Messages=Messages[-number:]#返回从后向前数number条消息
                pyautogui.press('End')
                return {'名称':name,'新消息条数':number,'类型':type,'消息':Messages}
            
            if video_call_button.exists() and video_call_button.exists():#同时有语音聊天和视频聊天按钮的是个人
                type='好友'
                chatList=main_window.child_window(**Main_window.FriendChatList)
                x,y=chatList.rectangle().left+10,(main_window.rectangle().top+main_window.rectangle().bottom)//2
                messages=chatList.children(control_type='ListItem')
                Messages.extend([message for message in messages  if not re.match(r'\d+:\d+',message.window_text())])
                #点击聊天区域侧边栏靠里一些的位置,依次来激活滑块,不直接main_window.click_input()是为了防止点到消息
                mouse.click(coords=(x,y))
                #按一下pagedown到最下边
                pyautogui.press('pagedown')
                ########################
                #需要先提前向上遍历一遍,防止语音消息没有转换完毕
                if number<=10:#10条消息最多先向上遍历number//3页
                    pages=number//3
                else:
                    pages=number//2#超过10页
                for _ in range(pages):
                    if check_more_messages_button.exists():
                        check_more_messages_button.click_input()
                        mouse.click(coords=(x,y))
                    pyautogui.press('pageup',_pause=False)
                pyautogui.press('End')
                mouse.click(coords=(x,y))
                pyautogui.press('pagedown')
                ##################################
                #开始记录
                while len(list(set(Messages)))<number:
                    if check_more_messages_button.exists():
                        check_more_messages_button.click_input()
                        mouse.click(coords=(x,y))
                    pyautogui.press('pageup',_pause=False)
                    messages=chatList.children(control_type='ListItem')
                    Messages.extend([message for message in messages if not re.match(r'\d+:\d+',message.window_text())])
                #######################################################
                Messages=ConvertMessages(Messages,type)#将listitem转换为文本内容
                Messages=Messages[-number:]#返回从后向前数number条消息
                pyautogui.press('End')
                return {'名称':name,'新消息条数':number,'类型':type,'消息':Messages}
            else:#都没有是公众号
                type='公众号'
                return {'名称':name,'新消息条数':number,'类型':type}
        def record():
            #遍历当前会话列表内可见的所有成员，获取他们的名称和新消息条数，没有新消息的话返回[],[]
            #newMessagefriends为会话列表(List)中所有含有新消息的ListItem
            newMessagefriends=[friend for friend in messageList.items() if '条新消息' in friend.window_text()]
            if newMessagefriends:
                #newMessageTips为newMessagefriends中每个元素的文本:['测试365 5条新消息','一家人已置顶20条新消息']这样的字符串列表
                newMessageTips=[friend.window_text() for friend in newMessagefriends]
                #会话列表中的好友具有Text属性，Text内容为备注名，通过这个按钮的名称获取好友名字
                names=[friend.descendants(control_type='Text')[0].window_text() for friend in newMessagefriends]
                #此时filtered_Tips变为：['5条新消息','20条新消息']直接正则匹配就不会出问题了
                filtered_Tips=[friend.replace(name,'') for name,friend in zip(names,newMessageTips)]
                nums=[int(re.findall(r'\d+',tip)[0]) for tip in filtered_Tips]
                return names,nums 
            return [],[]
        
        #打开文件传输助手是为了防止当前窗口有好友给自己发消息无法检测到,因为当前窗口即使有新消息也不会在会话列表中好友头像上显示数字,
        main_window=Tools.open_dialog_window(friend=filetransfer,wechat_path=wechat_path,is_maximize=True)[1]
        messageList=main_window.child_window(**Main_window.ConversationList)
        scrollable=Tools.is_VerticalScrollable(messageList)
        chatsButton=main_window.child_window(**SideBar.Chats)
        if not duration:#没有持续时间。
            #侧边栏没有红色消息提示直接返回未查找到新消息
            if not chatsButton.legacy_properties().get('Value'):#通过微信侧边栏的聊天按钮的LegarcyProperties.value有没有消息提示(右上角的红色数字,有的话这个值为'\d+')
                if close_wechat:
                    main_window.close()
                return '未查找到新消息'     
            if not scrollable:#聊天列表内不足12人以上且有新消息,没有滑块，不用遍历,直接原地在列表里查找
                names,nums=record()
                if names and nums:
                    Names.extend(names)
                    Nums.extend(nums)
                dic=dict(zip(Names,Nums))#临时变量,存储好友名称与新消息数量的字典
                newMessages=[]
                for key,value in dic.items():         
                    newMessages.append(get_message_content(key,value,search_pages=search_pages))
                Tools.open_dialog_window(friend=filetransfer,wechat_path=wechat_path,is_maximize=True)
                if close_wechat:
                    main_window.close()
                newMessages_json=json.dumps(newMessages,ensure_ascii=False,indent=4)
                if close_wechat:
                    main_window.close()
                return newMessages_json
            
            if scrollable:#聊天列表在12人以上且有新消息,遍历一遍
                x,y=messageList.rectangle().right-5,messageList.rectangle().top+8
                mouse.click(coords=(x,y))#点击右上方激活滑块
                pyautogui.press('Home')
                pyautogui.press('End')
                lastmemberName=messageList.items()[-1].window_text()
                pyautogui.press('Home')#按下Home健确保从顶部开始
                while messageList.items()[-1].window_text()!=lastmemberName:
                    names,nums=record()
                    if names and nums:
                        Names.extend(names)   
                        Nums.extend(nums)
                    pyautogui.keyDown('pagedown',_pause=False)
                    search_pages+=1
                pyautogui.press('Home')
                #################
                #回到顶部后,再查找一下,以防在向下遍历会话列表时顶部有好友给发消息,没检测到新的变化的数字
                names,nums=record()
                if names and nums:
                    Names.extend(names)
                    Nums.extend(nums)
                ###########################
                dic=dict(zip(Names,Nums))#临时变量,存储好友名称与新消息数量的字典
                newMessages=[]
                for key,value in dic.items():         
                    newMessages.append(get_message_content(key,value,search_pages=search_pages))
                Tools.open_dialog_window(friend=filetransfer,wechat_path=wechat_path,is_maximize=True)
                newMessages_json=json.dumps(newMessages,ensure_ascii=False,indent=4)
                if close_wechat:
                    main_window.close()
                return newMessages_json

        else:#有持续时间,需要在指定时间内一直遍历,最终返回结果
            if not scrollable:#聊天列表不足12人以上,会话列表没有满,没有滑块，不用遍历,直接原地等待即可
                duration=match_duration(duration)
                if not duration:#不是指定形式的duration报错
                    main_window.close()
                    raise TimeNotCorrectError
                start_time=time.time()
                while True:#一直等待直到时间差超过durtation
                    if time.time()-start_time>=duration:
                        break
                if not chatsButton.legacy_properties().get('Value'):#文件传输助手界面原地等待duration后如果侧边栏的消息按钮还是没有红色消息提示直接返回未查找到新消息
                    if close_wechat:
                        main_window.close()
                    return '未查找到新消息'
                names,nums=record()#侧边栏消息按钮有红色消息提示,直接在当前的会话列表内record
                Names.extend(names)
                Nums.extend(nums)
                dic=dict(zip(Names,Nums))#临时变量,存储好友名称与新消息数量的字典
                newMessages=[]
                for key,value in dic.items(): 
                    newMessages.append(get_message_content(key,value,search_pages=search_pages))
                Tools.open_dialog_window(friend=filetransfer,wechat_path=wechat_path,is_maximize=True)
                newMessages_json=json.dumps(newMessages,ensure_ascii=False,indent=4)
                if close_wechat:
                    main_window.close()
                return newMessages_json
            else:
                chatsButton=main_window.child_window(**SideBar.Chats)
                x,y=messageList.rectangle().right-5,messageList.rectangle().top+8
                mouse.click(coords=(x,y))#点击右上方激活滑块
                pyautogui.press('Home')
                pyautogui.press('End')
                lastmemberName=messageList.items()[-1].window_text()
                pyautogui.press('Home')#按下Home健确保从顶部开始
                duration=match_duration(duration)
                if not duration:
                    main_window.close()
                    raise TimeNotCorrectError
                start_time=time.time()
                while True:#y一直原地等待,直到时间差超过duration
                    if time.time()-start_time>=duration:
                        break
                if not chatsButton.legacy_properties().get('Value'):
                    if close_wechat:
                        main_window.close()
                    return '未查找到新消息'
                while messageList.items()[-1].window_text()!=lastmemberName:
                    names,nums=record()
                    if names and nums:
                        Names.extend(names)
                        Nums.extend(nums)
                    pyautogui.press('pagedown',_pause=False)
                    search_pages+=1
                pyautogui.press('Home')
                #################
                #回到顶部后,再查找一下顶部,以防在向下遍历会话列表时顶部有好友给发消息,没检测到
                names,nums=record()
                if names and nums:
                    Names.extend(names)
                    Nums.extend(nums)
                #################
                dic=dict(zip(Names,Nums))#临时变量,存储好友名称与新消息数量的字典
                newMessages=[]
                for key,value in dic.items():         
                    newMessages.append(get_message_content(key,value,search_pages=search_pages))
                Tools.open_dialog_window(friend=filetransfer,wechat_path=wechat_path,is_maximize=True)
                newMessages_json=json.dumps(newMessages,ensure_ascii=False,indent=4)
                if close_wechat:
                    main_window.close()
                return newMessages_json

        
class Files():
    @staticmethod
    def send_file_to_friend(friend:str,file_path:str,with_messages:bool=False,messages:list=[],messages_first:bool=False,delay:float=1,tickle:bool=False,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于给单个好友或群聊发送单个文件\n
        Args:
            friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
            file_path:\t待发送文件绝对路径。\n
            with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False\n
            messages:\t与文件一同发送的消息。格式:message=["消息1","消息2","消息3"]\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            delay:\t发送单条信息或文件的延迟,单位:秒/s,默认2s。\n
            tickle:\t是否在发送消息或文件后拍一拍好友,默认为False\n
            messages_first:\t默认先发送文件后发送消息,messages_first设置为True,先发送消息,后发送文件,\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏法搜索好友信息打开聊天界面\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        if len(file_path)==0:
            raise NotFileError
        if not Systemsettings.is_file(file_path):
            raise NotFileError
        if Systemsettings.is_dirctory(file_path):
            raise NotFileError
        if Systemsettings.is_empty_file(file_path):
            raise EmptyFileError
        chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        chat.click_input()
        if with_messages and messages:
            if messages_first:
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
                Systemsettings.copy_file_to_windowsclipboard(file_path=file_path)
                pyautogui.hotkey("ctrl","v")
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)   
            else:
                Systemsettings.copy_file_to_windowsclipboard(file_path=file_path)
                pyautogui.hotkey("ctrl","v")
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:#超过2000字发txt
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
        else:
            Systemsettings.copy_file_to_windowsclipboard(file_path)
            pyautogui.hotkey("ctrl","v")
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        if tickle:
            tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
        time.sleep(1)
        if close_wechat:
            main_window.close()

        
    @staticmethod
    def send_files_to_friend(friend:str,folder_path:str,with_messages:bool=False,messages:list=[str],messages_first:bool=False,delay:float=1,tickle:bool=False,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,search_pages:int=5):
        '''
        该方法用于给单个好友或群聊发送多个文件\n
        Args:
            friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
            folder_path:\t所有待发送文件所处的文件夹的地址。\n
            with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False。\n
            messages:\t与文件一同发送的消息。格式:message=["消息1","消息2","消息3"]\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。
            delay:\t发送单条信息或文件的延迟,单位:秒/s,默认2s。\n
            tickle:\t是否在发送文件或消息后拍一拍好友,默认为False\n
            messages_first:\t默认先发送文件后发送消息,messages_first设置为True,先发送消息,后发送文件,\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
        '''
        if len(folder_path)==0:
            raise NotFolderError
        if not Systemsettings.is_dirctory(folder_path):
            raise NotFolderError
        files_in_folder=Systemsettings.get_files_in_folder(folder_path=folder_path)
        if not files_in_folder:
            raise EmptyFolderError
        def send_files():#发送文件单次上限为9,需要9个9个分批发送
            if len(files_in_folder)<=9:
                Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder)
                pyautogui.hotkey("ctrl","v")
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
            else:
                files_num=len(files_in_folder)
                rem=len(files_in_folder)%9
                for i in range(0,files_num,9):
                    if i+9<files_num:
                        Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[i:i+9])
                        pyautogui.hotkey("ctrl","v")
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                if rem:
                    Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[files_num-rem:files_num])
                    pyautogui.hotkey("ctrl","v")
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
        chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        chat.click_input()
        if with_messages and messages:
            if messages_first:
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
                send_files()
            else:
                send_files()
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
        else:
            send_files()
        if tickle:
            tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)        
        time.sleep(1)
        if close_wechat:
            main_window.close()
    

    @staticmethod
    def send_file_to_friends(friends:list[str],file_paths:list[str],with_messages:bool=False,messages:list[list[str]]=[],messages_first:bool=False,delay:float=1,tickle:list[bool]=[],wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于给每个好友或群聊发送单个不同的文件以及多条消息\n
        Args:
            friends:\t好友或群聊备注。格式:friends=["好友1","好友2","好友3"]\n
            file_paths:\t待发送文件,格式: file=[发给好友1的单个文件,发给好友2的文件,发给好友3的文件]。\n
            with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False\n
            messages:\t待发送消息,格式:messages=["发给好友1的单条消息","发给好友2的单条消息","发给好友3的单条消息"]
            messages_first:\t先发送消息还是先发送文件.默认先发送文件\n
            delay:\t发送单条消息延迟,单位:秒/s,默认1s。\n
            tickle:\t是否给每一个好友发送消息或文件后拍一拍好友,格式为:[True,True,False,...]的bool值列表,与friends列表中的每一个好友对应\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
            close_wechat:任务结束后是否关闭微信,默认关闭\n
        注意!messages,filepaths与friends长度需一致,并且messages内每一条消息顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
        '''
        for file_path in file_paths:
            file_path=re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',file_path)
            if len(file_path)==0:
                raise NotFileError
            if not Systemsettings.is_file(file_path):
                raise NotFileError
            if Systemsettings.is_dirctory(file_path):
                raise NotFileError
            if Systemsettings.is_empty_file(file_path):
                raise EmptyFileError  
        Files=dict(zip(friends,file_paths))#临时便量用来使用字典来存储好友名称与对于文件路径
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        time.sleep(1)
         #多个好友的发送任务不需要使用open_dialog_window方法了直接在顶部搜索栏搜索,一个一个打开好友的聊天界面，发送消息,这样最高效
        if with_messages and messages:
            Chats=dict(zip(friends,messages))
            i=0
            for friend in Files:
                search=main_window.child_window(**Main_window.Search)
                search.click_input()
                Systemsettings.copy_text_to_windowsclipboard(friend)
                pyautogui.hotkey('ctrl','v')
                time.sleep(0.5)
                pyautogui.press('enter')
                chat=main_window.child_window(title=friend,control_type='Edit')
                chat.click_input()
                if messages_first:
                    messages=Chats.get(friend)
                    for message in messages:
                        if len(message)==0:
                            main_window.close()
                            raise CantSendEmptyMessageError
                        if len(message)<2000:
                            Systemsettings.copy_text_to_windowsclipboard(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                        elif len(message)>2000:
                            Systemsettings.convert_long_text_to_txt(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
                    Systemsettings.copy_file_to_windowsclipboard(Files.get(friend))
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                else:
                    Systemsettings.copy_file_to_windowsclipboard(Files.get(friend))
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                    messages=Chats.get(friend)
                    for message in messages:
                        if len(message)==0:
                            main_window.close()
                            raise CantSendEmptyMessageError
                        if len(message)<2000:
                            Systemsettings.copy_text_to_windowsclipboard(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                        elif len(message)>2000:
                            Systemsettings.convert_long_text_to_txt(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
                if tickle:
                    if tickle[i]:
                        tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
                    i+=1
        else:
            i=0
            for friend in Files:
                search=main_window.child_window(**Main_window.Search)
                search.click_input()
                Systemsettings.copy_text_to_windowsclipboard(friend)
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(1)
                pyautogui.press('enter')
                chat=main_window.child_window(title=friend,control_type='Edit')
                chat.click_input()
                Systemsettings.copy_file_to_windowsclipboard(Files.get(friend))
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
                if tickle:
                    if tickle[i]:
                        tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
                    i+=1
        time.sleep(1)
        if close_wechat:
            main_window.close()

    @staticmethod
    def send_files_to_friends(friends:list[str],folder_paths:list[str],with_messages:bool=False,messages:list[list[str]]=[],messages_first:bool=False,delay:float=1,tickle:list[bool]=[],wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于给多个好友或群聊发送多个不同或相同的文件夹内的所有文件\n
        Args:
            friends:\t好友或群聊备注。格式:friends=["好友1","好友2","好友3"]\n
            folder_paths:\t待发送文件夹路径列表,每个文件夹内可以存放多个文件,格式: FolderPath_list=["","",""]\n
            with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False\n
            message_list:\t待发送消息,格式:message=[[""],[""],[""]]\n
            messages_first:\t先发送消息还是先发送文件,默认先发送文件\n
            delay:\t发送单条消息延迟,单位:秒/s,默认1s。\n
            tickle:\t是否给每一个好友发送消息或文件后拍一拍好友,格式为:[True,True,False,...]的bool值列表,与friends列表中的每一个好友对应\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        注意! messages,folder_paths与friends长度需一致,并且messages内每一条消息FolderPath_list每一个文件\n
        顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
        '''
        for folder_path in folder_paths:
            folder_path=re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',folder_path)
            if len(folder_path)==0:
                raise NotFolderError
            if not Systemsettings.is_dirctory(folder_path):
                raise NotFolderError
        def send_files(folder_path):
            files_in_folder=Systemsettings.get_files_in_folder(folder_path=folder_path)
            if len(files_in_folder)<=9:
                Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder)
                pyautogui.hotkey("ctrl","v")
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
            else:
                files_num=len(files_in_folder)
                rem=len(files_in_folder)%9
                for i in range(0,files_num,9):
                    if i+9<files_num:
                        Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[i:i+9])
                        pyautogui.hotkey("ctrl","v")
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                if rem:
                    Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[files_num-rem:files_num])
                    pyautogui.hotkey("ctrl","v")
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
        folder_paths=[re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',folder_path) for folder_path in folder_paths]
        Files=dict(zip(friends,folder_paths))
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        if with_messages and messages:
            Chats=dict(zip(friends,messages))
            i=0
            for friend in Files:
                search=main_window.child_window(**Main_window.Search)
                search.click_input()
                Systemsettings.copy_text_to_windowsclipboard(friend)
                pyautogui.hotkey('ctrl','v')
                time.sleep(0.5)
                pyautogui.press('enter')
                chat=main_window.child_window(title=friend,control_type='Edit')
                chat.click_input()
                if messages_first:
                    messages=Chats.get(friend)
                    for message in messages:
                        if len(message)==0:
                            main_window.close()
                            raise CantSendEmptyMessageError
                        if len(message)<2000:
                            Systemsettings.copy_text_to_windowsclipboard(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                        elif len(message)>2000:
                            Systemsettings.convert_long_text_to_txt(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
                    folder_path=Files.get(friend)
                    send_files(folder_path)
                else:
                    folder_path=Files.get(friend)
                    send_files(folder_path)
                    messages=Chats.get(friend)
                    for message in messages:
                        if len(message)==0:
                            main_window.close()
                            raise CantSendEmptyMessageError
                        if len(message)<2000:
                            Systemsettings.copy_text_to_windowsclipboard(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                        elif len(message)>2000:
                            Systemsettings.convert_long_text_to_txt(message)
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            time.sleep(delay)
                            pyautogui.hotkey('alt','s',_pause=False)
                            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
                if tickle:
                    if tickle[i]:
                        tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
                    i+=1
        else:
            i=0
            for friend in Files:
                search=main_window.child_window(**Main_window.Search)
                search.click_input()
                Systemsettings.copy_text_to_windowsclipboard(friend)
                time.sleep(0.5)
                pyautogui.hotkey('ctrl','v')
                pyautogui.press('enter')
                chat=main_window.child_window(title=friend,control_type='Edit')
                chat.click_input()
                folder_path=Files.get(friend)
                send_files(folder_path)
                if tickle:
                    if tickle[i]:
                        tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
                    i+=1
        time.sleep(1)
        if close_wechat:
            main_window.close()

    @staticmethod
    def forward_file(friends:list[str],file_path:str,delay:float=0.5,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用于给好友转发文件,实际使用时建议先给文件传输助手转发\n
        这样可以避免对方聊天信息更新过快导致转发文件被'淹没',进而无法定位出错的问题。\n
        Args:
            friends:\t好友或群聊备注列表。格式:friends=["好友1","好友2","好友3"]\n
            file_path:\t待发送文件,格式: file_path="转发文件路径"。\n
            delay:发送单条消息延迟,单位:秒/s,默认1s。\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
            search_pages:在会话列表中查询查找第一个转发文件的好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            close_wechat:任务结束后是否关闭微信,默认关闭\n
        '''
        if len(file_path)==0:
            raise NotFileError
        if Systemsettings.is_empty_file(file_path):
            raise EmptyFileError
        if Systemsettings.is_dirctory(file_path):
            raise NotFileError
        if not Systemsettings.is_file(file_path):
            raise NotFileError    
        def right_click_message():
            max_retry_times=25
            retry_interval=0.2
            counter=0
            #查找最新的我自己发的消息，并右键单击我发送的消息，点击转发按钮
            chatList=main_window.child_window(**Main_window.FriendChatList)
            myname=main_window.child_window(**Buttons.MySelfButton).window_text()
            #if message.descendants(conrol_type)是用来筛选这个消息(control_type为ListItem)内有没有按钮(消息是人发的必然会有头像按钮这个UI,系统消息比如'8:55'没有这个UI)
            chats=[chat for chat in chatList.children(control_type='ListItem') if chat.descendants(control_type='Button')]#不包括时间戳和系统消息
            sent_message=[sent_message for sent_message in chats if sent_message.descendants(control_type='Button')[-1].window_text()==myname]
            while not sent_message and sent_message[-1].is_visible():#如果聊天记录页为空或者我发过的最后一条消息(转发的消息)不可见(可能是网络延迟发送较慢造成，也不排除是被顶到最上边了)
                chats=[chat for chat in chatList.children(control_type='ListItem') if chat.descendants(control_type='Button')]#不包括时间戳和系统消息,只有是好友发送的时候，这个消息内部才有(Button属性)
                sent_message=[sent_message for sent_message in chats if sent_message.descendants(control_type='Button')[-1].window_text()==myname]
                time.sleep(retry_interval)
                counter+=1
                if counter>max_retry_times: 
                    raise TimeoutError
            button=sent_message[-1].children()[0].children()[1]
            button.right_click_input()
            menu=main_window.child_window(**Menus.RightClickMenu)
            select_contact_window=main_window.child_window(**Main_window.SelectContactWindow)
            if not select_contact_window.exists():
                while not menu.exists():
                    button.right_click_input()
                    time.sleep(0.2)
            forward=menu.child_window(**MenuItems.ForwardMenuItem)
            while not forward.exists():
                main_window.click_input()
                button.right_click_input()
                time.sleep(0.2)
            forward.click_input()
            select_contact_window.child_window(**Buttons.MultiSelectButton).click_input()   
            send_button=select_contact_window.child_window(**Buttons.SendRespectivelyButton)
            search_button=select_contact_window.child_window(**Edits.SearchEdit)
            return search_button,send_button
        chat,main_window=Tools.open_dialog_window(friend=friends[0],wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        chat.click_input()
        Systemsettings.copy_file_to_windowsclipboard(file_path=file_path)
        pyautogui.hotkey("ctrl","v")
        time.sleep(delay)
        pyautogui.hotkey('alt','s') 
        friends=friends[1:]
        if len(friends)<=9:
            search_button,send_button=right_click_message()
            for other_friend in friends:
                search_button.click_input()
                Systemsettings.copy_text_to_windowsclipboard(other_friend)
                pyautogui.hotkey('ctrl','v')
                time.sleep(delay)
                pyautogui.press('enter')
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('backspace')
                time.sleep(delay)
            send_button.click_input()
        else:  
            res=len(friends)%9
            for i in range(0,len(friends),9):
                if i+9<=len(friends):
                    search_button,send_button=right_click_message()
                    for other_friend in friends[i:i+9]:
                        search_button.click_input()
                        Systemsettings.copy_text_to_windowsclipboard(other_friend)
                        pyautogui.hotkey('ctrl','v')
                        time.sleep(delay)
                        pyautogui.press('enter')
                        pyautogui.hotkey('ctrl','a')
                        pyautogui.press('backspace')
                        time.sleep(delay)
                    send_button.click_input()
                else:
                    pass
            if res:
                search_button,send_button=right_click_message()
                for other_friend in friends[len(friends)-res:len(friends)]:
                    search_button.click_input()
                    Systemsettings.copy_text_to_windowsclipboard(other_friend)
                    pyautogui.hotkey('ctrl','v')
                    time.sleep(delay)
                    pyautogui.press('enter')
                    pyautogui.hotkey('ctrl','a')
                    pyautogui.press('backspace')
                    time.sleep(delay)
                send_button.click_input()
        time.sleep(1)
        if close_wechat:
            main_window.close()
    @staticmethod
    def get_chat_files(friend:str,folder_path:str,number:int=10,search_pages:int=5,wechat_path:str=None,is_maximize:bool=False,close_wechat:bool=True):
        '''
        该方法用来保存与某个好友的聊天文件。\n
        Args:
            friend:\t好友或群聊的备注\n
            folder_path:\t用来保存聊天文件的文件夹路径\n
            number:\t要保存的文件数量\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        if len(folder_path)==0:
            raise NotFolderError
        if not Systemsettings.is_dirctory(folder_path):
            raise NotFolderError(r'给定路径不是文件夹!无法保存聊天文件,请重新选择文件夹！')
        Systemsettings.copy_text_to_windowsclipboard(folder_path)
        if number<8:#文件列表一页八个文件，每翻一页有8个文件可以保存
            pages=1
            res=0
        else:
            pages=number//8
            res=number%8
        desktop=Desktop(**Independent_window.Desktop)
        saved=[]
        def save_file(file):
            if file not in saved:
                saved.append(file)
                file.right_click_input()
                menu=chat_history_window.child_window(**Menus.RightClickMenu)
                save_as_button=menu.child_window(title='另存为...',control_type='MenuItem')
                save_as_button.click_input()
                time.sleep(1)
                save_as_window=desktop.window(title_re='另存为...',control_type='Window',framework_id='Win32',top_level_only=False)
                path_bar=save_as_window.child_window(class_name='ToolbarWindow32',control_type='ToolBar',auto_id='1001')
                rec=path_bar.rectangle()
                mouse.click(coords=(rec.right-5,int(rec.top+rec.bottom)//2))
                pyautogui.press('backspace')
                pyautogui.hotkey('ctrl','v',_pause=False)
                pyautogui.press('enter')
                pyautogui.hotkey('alt','s',_pause=False)
                confirm_save_as_dialog=save_as_window.child_window(title='确认另存为',control_type='Window')
                if confirm_save_as_dialog.exists():
                    pyautogui.hotkey('alt','y')
            else:
                pass
        chat_history_window=Tools.open_chat_history(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat,search_pages=search_pages)[0]
        file_button=chat_history_window.child_window(title='文件',control_type='TabItem')
        file_button.click_input()
        file_list=chat_history_window.child_window(title='文件',control_type='List')
        rec=file_list.rectangle()
        mouse.click(coords=(rec.right-8,rec.top+2))
        for _ in range(pages):
            files=file_list.descendants(control_type='ListItem')
            for i in range(len(files)):
                save_file(files[i])
            pyautogui.press('pagedown')
        if res:
            i=0
            files=file_list.descendants(control_type='ListItem')
            while files[i] in saved:
                i+=1
                if i>len(files):
                    break 
            if i<len(files):     
                for i in range(i,i+res):
                    try:
                        save_file(files[i])
                    except IndexError:
                        print(f'文件总数为{len(saved)},不足{number}，已为你保存所有文件')

            else:
                print(f'文件总数为{len(saved)},不足{number}，已为你保存所有文件')
        chat_history_window.close()


class WechatSettings():

    @staticmethod
    def open_settings(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来打开微信设置界面。\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        setting=main_window.child_window(**SideBar.SettingsAndOthers)
        setting.click_input()
        settings_menu=main_window.child_window(**Main_window.SettingsMenu)
        settings_button=settings_menu.child_window(Buttons.SettingsButton)
        settings_button.click_input() 
        time.sleep(1)
        desktop=Desktop(**Independent_window.Desktop)
        settings_window=desktop.window(**Independent_window.SettingWindow)
        if close_wechat:
            main_window.close()
        return settings_window,main_window
    
    @staticmethod
    def Log_out(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来PC微信退出登录。\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        settings_window=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        log_out_button=settings_window.window(**Buttons.LogoutButton)
        log_out_button.click_input()
        time.sleep(2)
        confirm_button=settings_window.window(**Buttons.ConfirmButton)
        confirm_button.click_input()

    @staticmethod
    def Auto_convert_voice_messages_to_text(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信开启或关闭设置中的语音消息自动转文字。\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        choices={'open','close'}
        if state not in choices:
            raise WrongParameterError
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.GeneralTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=6)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                print("已关闭聊天中的语音消息自动转成文字")
            else:
                print('聊天的语音消息自动转成文字已开启,无需开启')
        else:     
            if state=='open':
                check_box.click_input()
                print("已开启聊天中的语音消息自动转成文字")
            else:
                print('聊天中的语音消息自动转成文字已关闭,无需关闭')
        if close_settings_window:
            settings.close()

    @staticmethod
    def Adapt_to_PC_display_scalling(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信开启或关闭适配微信设置中的系统所释放比例。\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        choices={'open','close'}
        if state not in choices:
            raise WrongParameterError
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.GeneralTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=4)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                print("已关闭适配系统缩放比例")
            else:
                print('适配系统缩放比例已开启,无需开启')
        else:
            if state=='open':
                check_box.click_input()
                print("已开启适配系统缩放比例")
            else:
                print('适配系统缩放比例已关闭,无需关闭')
        if close_settings_window:
            settings.close()
    
    @staticmethod
    def Save_chat_history(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信打开或关闭微信设置中的保留聊天记录选项。\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        choices={'open','close'}
        if state not in choices:
            raise WrongParameterError
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.GeneralTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=2)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                query_window=settings.child_window(title="",control_type="Pane",class_name='WeUIDialog')
                confirm=query_window.child_window(**Buttons.ConfirmButton)
                confirm.click_input()
                print("已关闭保留聊天记录")
            else:
                print('保留聊天记录已开启,无需开启')
        else:
            if state=='open':
                check_box.click_input()
                print("已开启保留聊天记录")
            else:
                print('保留聊天记录已关闭,无需关闭')
        if close_settings_window:
            settings.close()

    @staticmethod
    def Run_wechat_when_pc_boots(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信打开或关闭微设置中的开机自启动微信。\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        choices={'open','close'}
        if state not in choices:
            raise WrongParameterError
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.GeneralTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=1)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                print("已关闭开机自启动微信")
            else:
                print('开机自启动微信已开启,无需开启')
        else:
            if state=='open':
                check_box.click_input()
                print("已开启关机自启动微信")
            else:
                print('开机自启动微信已关闭,无需关闭')
        if close_settings_window:
            settings.close()
    
    @staticmethod
    def Using_default_browser(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信打开或关闭微信设置中的使用系统默认浏览器打开网页\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
       
        '''
        choices={'open','close'}
        if state not in choices:
            raise WrongParameterError
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.GeneralTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=5)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                print("已关闭使用系统默认浏览器打开网页")
            else:
                print('使用系统默认浏览器打开网页已开启,无需开启')
        else:
            if state=='open':
                check_box.click_input()
                print("已开启使用系统默认浏览器打开网页")
            else:
                print('使用系统默认浏览器打开网页已关闭,无需关闭')
        if close_settings_window:
            settings.close()

    @staticmethod
    def Auto_update_wechat(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信打开或关闭微信设置中的有更新时自动升级微信。\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        choices={'open','close'}
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.GeneralTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=0)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                query_window=settings.child_window(title="",control_type="Pane",class_name='WeUIDialog')
                confirm=query_window.child_window(title="关闭",control_type="Button")
                confirm.click_input()
                print("已关闭有更新时自动升级微信")
            else:
                print('有更新时自动升级微信已开启,无需开启')
        else:
            if state=='open':
                check_box.click_input()
                print("已开启有更新时自动升级微信")
            else:
                print('有更新时自动升级微信已关闭,无需关闭') 
        if close_settings_window:
            settings.close()

    @staticmethod
    def Clear_chat_history(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信清空所有聊天记录,谨慎使用。\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.GeneralTabItem)
        general_settings.click_input()
        settings.child_window(**Buttons.ClearChatHistoryButton).click_input()
        query_window=settings.child_window(title="",control_type="Pane",class_name='WeUIDialog')
        confirm=query_window.child_window(**Buttons.ConfirmButton)
        confirm.click_input()
        if close_settings_window:
            settings.close()

    @staticmethod
    def Close_auto_log_in(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信关闭自动登录,若需要开启需在手机端设置。\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        account_settings=settings.child_window(**TabItems.MyAccountTabItem)
        account_settings.click_input()
        try:
            close_button=settings.child_window(**Buttons.CloseAutoLoginButton)
            close_button.click_input()
            query_window=settings.child_window(title="",control_type="Pane",class_name='WeUIDialog')
            confirm=query_window.child_window(**Buttons.ConfirmButton)
            confirm.click_input()
            if close_settings_window:
                settings.close()
        except ElementNotFoundError:
            if close_settings_window:
                settings.close()
            raise AlreadyCloseError(f'已关闭自动登录选项,无需关闭！')
    
    @staticmethod
    def Show_web_search_history(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信打开或关闭微信设置中的显示网络搜索历史。\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        choices={'open','close'}
        if state not in choices:
            raise WrongParameterError
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.GeneralTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=3)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                print("已关闭显示网络搜索历史")
            else:
                print('显示网络搜索历史已开启,无需开启')
        else:
            if state=='open':
                check_box.click_input()
                print("已开启显示网络搜索历史")
            else:
                print('显示网络搜索历史已关闭,无需关闭')
        if close_settings_window:
            settings.close()

    @staticmethod
    def New_message_alert_sound(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信开启或关闭设置中的新消息通知声音。\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:任务完成后是否关闭设置界面窗口,默认关闭\n   
        '''
        choices={'open','close'}
        if state not in choices:
            raise WrongParameterError
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.NotificationsTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=0)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                print("已关闭新消息通知声音")
            else:
                print('新消息通知声音已开启,无需开启')
        else:
            if state=='open':
                check_box.click_input()
                print("已开启新消息通知声音")
            else:
                print('新消息通知声音已关闭,无需关闭')
        if close_settings_window:
            settings.close()

    @staticmethod
    def Voice_and_video_calls_alert_sound(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来PC微信开启或关闭设置中的语音和视频通话通知声音。\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        
        '''
        choices={'open','close'}
        if state not in choices:
            raise WrongParameterError
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.NotificationsTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=1)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                print("已关闭语音和视频通话通知声音")
            else:
                print('语音和视频通话通知声音已开启,无需开启')
        else:
            if state=='open':
                check_box.click_input()
                print("已开启语音和视频通话通知声音")
            else:
                print('语音和视频通话通知声音已关闭,无需关闭')
        settings.close()

    @staticmethod
    def Moments_notification_flag(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信开启或关闭设置中的朋友圈消息提示。\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        choices={'open','close'}
        if state not in choices:
            raise WrongParameterError
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.NotificationsTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=2)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                print("已关闭朋友圈消息提示")
            else:
                print('朋友圈消息提示已开启,无需开启')
        else:
            if state=='open':
                check_box.click_input()
                print("已开启朋友圈消息提示")
            else:
                print('朋友圈消息提示已关闭,无需关闭')
        if close_settings_window:
            settings.close()
    
    @staticmethod
    def Channel_notification_flag(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信开启或关闭设置中的视频号消息提示。\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        choices={'open','close'}
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.NotificationsTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=3)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                print("已关闭视频号消息提示")
            else:
                print('视频号消息提示已开启,无需开启')
        else:
            if state=='open':
                check_box.click_input()
                print("已开启视频号消息提示")
            else:
                print('视频号消息提示已关闭,无需关闭')
        if close_settings_window:
            settings.close()

    @staticmethod
    def Topstories_notification_flag(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信开启或关闭设置中的看一看消息提示。\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        choices={'open','close'}
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.NotificationsTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=4)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                print("已关闭看一看消息提示")
            else:
                print("看一看消息提示已开启,无需开启")
        else:
            if state=='open':
                check_box.click_input()
                print("已开启看一看消息提示")
            else:
                print("看一看消息提示已关闭,无需关闭")
        if close_settings_window:
            settings.close()

    @staticmethod
    def Miniprogram_notification_flag(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信开启或关闭设置中的小程序消息提示。\n
        Args:
            state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        choices={'open','close'}
        if state not in choices:
            raise WrongParameterError
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general_settings=settings.child_window(**TabItems.NotificationsTabItem)
        general_settings.click_input()
        check_box=settings.child_window(control_type="CheckBox",found_index=5)
        if check_box.get_toggle_state():
            if state=='close':
                check_box.click_input()
                print("已关闭小程序消息提示")
            else:
                print('小程序消息提示已开启,无需开启')
        else:
            if state=='open':
                check_box.click_input()
                print("已开启小程序消息提示")
            else:
                print('小程序消息提示已关闭,无需关闭')
        if close_settings_window:
            settings.close()
    
    @staticmethod
    def Change_capture_screen_shortcut(shortcuts:list[str],wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信修改微信设置中截取屏幕的快捷键。\n
        Args:
            shortcuts:\t快捷键键位名称列表,若你想将截取屏幕的快捷键设置为'ctrl+shift',那么shortcuts=['ctrl','shift']\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        
        '''
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        shortcut=settings.child_window(**TabItems.ShortCutTabItem)
        shortcut.click_input()
        capture_screen_button=settings.child_window(**Texts.CptureScreenShortcutText).parent().children()[1]
        capture_screen_button.click_input()
        settings.child_window(**Panes.ChangeShortcutPane).click_input()
        time.sleep(1)
        pyautogui.hotkey(*shortcuts)
        confirm_button=settings.child_window(**Buttons.ConfirmButton) 
        confirm_button.click_input()
        if close_settings_window:
            settings.close()
            
    @staticmethod
    def Change_open_wechat_shortcut(shortcuts:list[str],wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信修改微信设置中打开微信的快捷键。\n
        Args:
            shortcuts:\t快捷键键位名称列表,若你想将截取屏幕的快捷键设置为'ctrl+shift',那么shortcuts=['ctrl','shift']\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        shortcut=settings.child_window(**TabItems.ShortCutTabItem)
        shortcut.click_input()
        open_wechat_button=settings.child_window(**Texts.OpenWechatShortcutText).parent().children()[1]
        open_wechat_button.click_input()
        settings.child_window(**Panes.ChangeShortcutPane).click_input()
        time.sleep(1)
        pyautogui.hotkey(*shortcuts)
        confirm_button=settings.child_window(**Buttons.ConfirmButton) 
        confirm_button.click_input()
        if close_settings_window:
            settings.close()
    
    @staticmethod
    def Change_lock_wechat_shortcut(shortcuts:list[str],wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信修改微信设置中锁定微信的快捷键。\n
        Args:
            shortcuts:\t快捷键键位名称列表,若你想将截取屏幕的快捷键设置为'ctrl+shift',那么shortcuts=['ctrl','shift']\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
           close_settings_window:任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        shortcut=settings.child_window(**TabItems.ShortCutTabItem)
        shortcut.click_input()
        lock_wechat_button=settings.child_window(**Texts.LockWechatShortcutText).parent().children()[1]
        lock_wechat_button.click_input()
        settings.child_window(**Panes.ChangeShortcutPane).click_input()
        time.sleep(1)
        pyautogui.hotkey(*shortcuts)
        confirm_button=settings.child_window(**Buttons.ConfirmButton) 
        confirm_button.click_input()
        if close_settings_window:
            settings.close()
    
    @staticmethod
    def Change_send_message_shortcut(shortcuts:str='Enter',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信修改微信设置中发送消息的快捷键。\n
        Args:
            shortcuts:\t快捷键键位名称,发送消息的快捷键只有Enter与ctrl+enter。\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        shortcut=settings.child_window(**TabItems.ShortCutTabItem)
        shortcut.click_input()
        message_combo_button=settings.child_window(**Texts.SendMessageShortcutText).parent().children()[1]
        message_combo_button.click_input()
        message_combo=settings.child_window(class_name='ComboWnd')
        if shortcuts=='Enter':
            listitem=message_combo.child_window(control_type='ListItem',found_index=0)
            listitem.click_input()
        else:
            listitem=message_combo.child_window(control_type='ListItem',found_index=1)
            listitem.click_input()
        if close_settings_window:
            settings.close()

    def Change_Language(lang:int=0,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来PC微信修改语言。\n
        Args:
            lang:\t语言名称,只支持简体中文,English,繁体中文,使用0,1,2表示。\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        language_map={0:'简体中文',1:'英文',2:'繁体中文'}
        if language_map[lang]==language:
            raise WrongParameterError(f'当前微信语言已经为{language},无需更换为{language_map[lang]}')
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        general=settings.child_window(**TabItems.GeneralTabItem)
        general.click_input()
        message_combo_button=settings.child_window(**Texts.LanguageText).parent().children()[1]
        message_combo_button.click_input()
        message_combo=settings.child_window(class_name='ComboWnd')
        if lang==0:
            listitem=message_combo.child_window(control_type='ListItem',found_index=0)
            listitem.click_input()
        if lang==1:
            listitem=message_combo.child_window(control_type='ListItem',found_index=1)
            listitem.click_input()
        if lang==2:
            listitem=message_combo.child_window(control_type='ListItem',found_index=2)
            listitem.click_input()
        confirm_button=settings.child_window(**Buttons.ConfirmButton)
        confirm_button.click_input()


    @staticmethod
    def Shortcut_default(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
        '''
        该方法用来PC微信将快捷键恢复为默认设置。\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
        '''
        settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
        shortcut=settings.child_window(**TabItems.ShortCutTabItem)
        shortcut.click_input()
        default_button=settings.child_window(**Buttons.RestoreDefaultSettingsButton)
        default_button.click_input()
        print('已恢复快捷键为默认设置')
        if close_settings_window:
            settings.close()
class Call():

    @staticmethod
    def voice_call(friend:str,search_pages:int=5,wechat_path=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来给好友拨打语音电话\n
        Args:
            friend:好友备注\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        main_window=Tools.open_dialog_window(friend,wechat_path,search_pages=search_pages,is_maximize=is_maximize)[1]  
        Tool_bar=main_window.child_window(**Main_window.ChatToolBar)
        voice_call_button=Tool_bar.children(**Buttons.VoiceCallButton)[0]
        time.sleep(1)
        voice_call_button.click_input()
        if close_wechat:
            main_window.close()

    @staticmethod
    def video_call(friend:str,search_pages:int=5,wechat_path=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来给好友拨打视频电话\n
        Args:
            friend:\t好友备注.\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        main_window=Tools.open_dialog_window(friend,wechat_path,search_pages=search_pages,is_maximize=is_maximize)[1]  
        Tool_bar=main_window.child_window(**Main_window.ChatToolBar)
        voice_call_button=Tool_bar.children(**Buttons.VideoCallButton)[0]
        time.sleep(1)
        voice_call_button.click_input()
        if close_wechat:
            main_window.close()

    @staticmethod
    def voice_call_in_group(group_name:str,friends:list[str],search_pages:int=5,wechat_path=None,is_maximize:bool=True,close_wechat:bool=True,):
        '''
        该方法用来在群聊中发起语音电话\n
        Args:
            group_name:\t群聊备注\n
            friends:\t所有要呼叫的群友备注\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            lose_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        main_window=Tools.open_dialog_window(friend=group_name,search_pages=search_pages,wechat_path=wechat_path,is_maximize=is_maximize)[1]  
        Tool_bar=main_window.child_window(**Main_window.ChatToolBar)
        voice_call_button=Tool_bar.children(**Buttons.VoiceCallButton)[0]
        time.sleep(2)
        voice_call_button.click_input()
        add_talk_memver_window=main_window.child_window(**Main_window.AddTalkMemberWindow)
        search=add_talk_memver_window.child_window(*Edits.SearchEdit)
        for friend in friends:
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.5)
            pyautogui.press('enter')
            pyautogui.hotkey('ctrl','a')
            pyautogui.press('backspace')
            time.sleep(0.5)
        confirm_button=add_talk_memver_window.child_window(**Buttons.CompleteButton)
        confirm_button.click_input()
        time.sleep(1)
        if close_wechat:
            main_window.close()


class FriendSettings():
    '''这个模块包括:修改好友备注,获取聊天记录,删除联系人,设为星标朋友,将好友聊天界面置顶\n
    消息免打扰,置顶聊天,清空聊天记录,加入黑名单,推荐给朋友,取消设为星标朋友,取消消息免打扰,\n
    取消置顶聊天,取消聊天界面置顶,移出黑名单,添加好友,通过昵称或备注获取单个或多个好友微信号共计18项功能\n'''
    
    @staticmethod
    def pin_friend(friend:str,state:str='open',search_pages:int=5,wechat_path=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来将好友在会话内置顶或取消置顶\n
        Args:
            friend:\t好友备注。\n
            state:取值为open或close,默认值为open,用来决定置顶或取消置顶好友,state为open时执行置顶操作,state为close时执行取消置顶操作\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        choices=['open','close']
        if state not in choices:
            raise WrongParameterError
        main_window,chat_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages) 
        Tool_bar=chat_window.child_window(found_index=1,title='',control_type='ToolBar')
        Pinbutton=Tool_bar.child_window(**Buttons.PinButton)
        if Pinbutton.exists():
            if state=='open':
                Pinbutton.click_input()
            if state=='close':
                print(f"好友'{friend}'未被置顶,无需取消置顶!")
        else:
            Cancelpinbutton=Tool_bar.child_window(**Buttons.CancelPinButton)
            if state=='open':
                print(f"好友'{friend}'已被置顶,无需置顶!")
            if state=='close':
                Cancelpinbutton.click_input()
        main_window.click_input()
        if close_wechat:
            main_window.close()

    @staticmethod   
    def mute_friend_notifications(friend:str,state:str='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来开启或关闭好友的消息免打扰\n
        Args:
            friend:好友备注\n
            state:取值为open或close,默认值为open,用来决定开启或关闭好友的消息免打扰设置,state为open时执行开启消息免打扰操作,state为close时执行关闭消息免打扰操作\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        choices=['open','close']
        if state not in choices:
            raise WrongParameterError
        friend_settings_window,main_window=Tools.open_friend_settings(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        mute_checkbox=friend_settings_window.child_window(**CheckBoxes.MuteNotificationsCheckBox)
        if mute_checkbox.get_toggle_state():
            if state=='open':
                print(f"好友'{friend}'的消息免打扰已开启,无需再开启消息免打扰!")
            if state=='close':
                mute_checkbox.click_input()
            friend_settings_window.close()
            if close_wechat:
                main_window.click_input()  
                main_window.close()
        else:
            if state=='open':
                mute_checkbox.click_input()
            if state=='close':
               print(f"好友'{friend}'的消息免打扰未开启,无需再关闭消息免打扰!") 
            friend_settings_window.close()
            if close_wechat:
                main_window.click_input()  
                main_window.close()

    @staticmethod
    def sticky_friend_on_top(friend:str,state:str='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来开启或关闭好友的聊天置顶\n
        Args:
            friend:\t好友备注\n 
            state:取值为open或close,默认值为open,用来决定开启或关闭好友的聊天置顶设置,state为open时执行开启聊天置顶操作,state为close时执行关闭消息免打扰操作\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        choices=['open','close']
        if state not in choices:
            raise WrongParameterError
        friend_settings_window,main_window=Tools.open_friend_settings(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        sticky_on_top_checkbox=friend_settings_window.child_window(**CheckBoxes.StickyonTopCheckBox)
        if sticky_on_top_checkbox.get_toggle_state():
            if state=='open':
                print(f"好友'{friend}'的置顶聊天已开启,无需再设为置顶聊天")
            if state=='close':
                sticky_on_top_checkbox.click_input()
            friend_settings_window.close()
            main_window.click_input()
            if close_wechat:
                main_window.close()
        else:
            if state=='open':
                sticky_on_top_checkbox.click_input()
            if state=='close':
                print(f"好友'{friend}'的置顶聊天未开启,无需再取消置顶聊天")
            friend_settings_window.close()
            main_window.click_input()
            if close_wechat:
                main_window.close()

    @staticmethod
    def clear_friend_chat_history(friend:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        ''' 
        该方法用来清空与好友的聊天记录\n
        Args:
            friend:\t好友备注\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        
        '''
        friend_settings_window,main_window=Tools.open_friend_settings(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        clear_chat_history_button=friend_settings_window.child_window(**Buttons.ClearChatHistoryButton)
        clear_chat_history_button.click_input()
        confirm_button=main_window.child_window(**Buttons.ConfirmEmptyChatHistoryButon)
        confirm_button.click_input()
        if close_wechat:
            main_window.close()
    
    @staticmethod
    def delete_friend(friend:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        ''' 
        该方法用来删除好友\n
        Args:
            friend:好友备注\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        menu,friend_settings_window,main_window=Tools.open_friend_settings_menu(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        delete_friend_item=menu.child_window(**MenuItems.DeleteMenuItem)
        delete_friend_item.click_input()
        confirm_window=friend_settings_window.child_window(**Panes.ConfirmPane)
        confirm_buton=confirm_window.child_window(**Buttons.DeleteButton)
        confirm_buton.click_input()
        time.sleep(1)
        if close_wechat:
            main_window.close()
    
    @staticmethod
    def add_new_friend(phone_number:str=None,wechat_number:str=None,request_content:str=None,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来添加新朋友\n
        Args:
            phone_number:\t手机号\n
            wechat_number:\t微信号\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        注意:手机号与微信号至少要有一个!\n
        '''
        desktop=Desktop(**Independent_window.Desktop)
        main_window=Tools.open_contacts(wechat_path,is_maximize=is_maximize)
        add_friend_button=main_window.child_window(**Buttons.AddNewFriendButon)
        add_friend_button.click_input()
        search_new_friend_bar=main_window.child_window(**Main_window.SearchNewFriendBar)
        search_new_friend_bar.click_input()
        if phone_number and not wechat_number:
            Systemsettings.copy_text_to_windowsclipboard(phone_number)
            pyautogui.hotkey('ctrl','v')
        elif wechat_number and phone_number:
            Systemsettings.copy_text_to_windowsclipboard(wechat_number)
            pyautogui.hotkey('ctrl','v')
        elif not phone_number and wechat_number:
            Systemsettings.copy_text_to_windowsclipboard(wechat_number)
            pyautogui.hotkey('ctrl','v')
        else:
            if close_wechat:
                main_window.close()
            raise NoWechat_number_or_Phone_numberError
        search_new_friend_result=main_window.child_window(**Main_window.SearchNewFriendResult)
        search_new_friend_result.child_window(**Texts.SearchContactsResult).click_input()
        time.sleep(1.5)
        profile_pane=desktop.window(**Independent_window.ContactProfileWindow)
        add_to_contacts=profile_pane.child_window(**Buttons.AddToContactsButton)
        if add_to_contacts.exists():
            add_to_contacts.click_input()
            add_friend_request_window=main_window.child_window(**Main_window.AddFriendRequestWindow)
            if add_friend_request_window.exists():
                if request_content:
                    request_content_edit=add_friend_request_window.child_window(**Edits.RequestContentEdit)
                    request_content_edit.click_input()
                    pyautogui.hotkey('ctrl','a')
                    pyautogui.press('backspace')
                    request_content_edit=add_friend_request_window.child_window(title='',control_type='Edit',found_index=0)
                    Systemsettings.copy_text_to_windowsclipboard(request_content)
                    pyautogui.hotkey('ctrl','v')
                    confirm_button=add_friend_request_window.child_window(**Buttons.ConfirmButton)
                    confirm_button.click_input()
                    time.sleep(3)
                    if language=='简体中文':
                        cancel_button=main_window.child_window(title='取消',control_type='Button',found_index=0)
                    if language=='英文':
                        cancel_button=main_window.child_window(title='Cancel',control_type='Button',found_index=0)
                    cancel_button.click_input()
                    if close_wechat:
                        main_window.close()
                else:
                    confirm_button=add_friend_request_window.child_window(**Buttons.ConfirmButton)
                    confirm_button.click_input()
                    time.sleep(3)
                    if language=='简体中文':
                        cancel_button=main_window.child_window(title='取消',control_type='Button',found_index=0)
                    if language=='英文':
                        cancel_button=main_window.child_window(title='Cancel',control_type='Button',found_index=0)
                    cancel_button.click_input()
                    if close_wechat:
                        main_window.close() 
        else:
            time.sleep(1)
            profile_pane.close()
            if close_wechat:
                main_window.close()
            raise AlreadyInContactsError

    @staticmethod
    def change_friend_remark_and_tag(friend:str,remark:str,tag:str=None,description:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来修改好友备注和标签\n
        Args:
            friend:\t好友备注\n
            tag:标签名\n
            description:描述\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        if friend==remark:
            raise SameNameError
        menu,friend_settings_window,main_window=Tools.open_friend_settings_menu(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        change_remark=menu.child_window(**MenuItems.EditContactMenuItem)
        change_remark.click_input()
        sessionchat=friend_settings_window.child_window(**Windows.EditContactWindow)
        remark_edit=sessionchat.child_window(title=friend,control_type='Edit')
        remark_edit.click_input()
        pyautogui.hotkey('ctrl','a')
        pyautogui.press('backspace')
        remark_edit=sessionchat.child_window(control_type='Edit',found_index=0)
        Systemsettings.copy_text_to_windowsclipboard(remark)
        pyautogui.hotkey('ctrl','v')
        if tag:
           tag_set=sessionchat.child_window(**Buttons.TagEditButton)
           tag_set.click_input()
           confirm_pane=main_window.child_window(**Main_window.SetTag)
           edit=confirm_pane.child_window(**Edits.TagEdit)
           edit.click_input()
           Systemsettings.copy_text_to_windowsclipboard(tag)
           pyautogui.hotkey('ctrl','v')
           confirm_pane.child_window(**Buttons.ConfirmButton).click_input()
        if description:
            description_edit=sessionchat.child_window(control_type='Edit',found_index=1)
            description_edit.click_input()
            pyautogui.hotkey('ctrl','a')
            pyautogui.press('backspace')
            Systemsettings.copy_text_to_windowsclipboard(description)
            pyautogui.hotkey('ctrl','v')
        confirm=sessionchat.child_window(**Buttons.ConfirmButton)
        confirm.click_input()
        friend_settings_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close()

    @staticmethod
    def add_friend_to_blacklist(friend:str,state:str='open',search_pages:int=0,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来将好友添加至黑名单\n
        Args:
            friend:\t好友备注\n
            state:\t取值为open或close,默认值为open,用来决定是否将好友添加至黑名单,state为open时执行将好友加入黑名单操作,state为close时执行将好友移出黑名单操作。\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为0,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        choices=['open','close']
        if state not in choices:
            raise WrongParameterError
        menu,friend_settings_window,main_window=Tools.open_friend_settings_menu(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        blacklist=menu.child_window(**MenuItems.BlockMenuItem)
        if blacklist.exists():
            if state=='open':
                blacklist.click_input()
                confirm_window=friend_settings_window.child_window(**Panes.ConfirmPane)
                confirm_buton=confirm_window.child_window(**Buttons.ConfirmButton)
                confirm_buton.click_input()
            if state=='close':
                print(f'好友"{friend}"未处于黑名单中,无需移出黑名单!')
            friend_settings_window.close()
            main_window.click_input() 
            if close_wechat:
                main_window.close()
        else:
            move_out_of_blacklist=menu.child_window(**MenuItems.UnBlockMenuItem)
            if state=='close':
                move_out_of_blacklist.click_input()
            if state=='open':
                print(f'好友"{friend}"已位于黑名单中,无需添加至黑名单!')
            friend_settings_window.close()
            main_window.click_input() 
            if close_wechat:
                main_window.close()
            
    @staticmethod
    def set_friend_as_star_friend(friend:str,state:str='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来将好友设置为星标朋友\n
        Args:
            friend:好友备注。\n
            state:\t取值为open或close,默认值为open,用来决定是否将好友设为星标朋友,state为open时执行将好友设为星标朋友操作,state为close时执行不再将好友设为星标朋友\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        choices=['open','close']
        if state not in choices:
            raise WrongParameterError
        menu,friend_settings_window,main_window=Tools.open_friend_settings_menu(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        star=menu.child_window(**MenuItems.StarMenuItem)
        if star.exists():
            if state=='open':
                star.click_input()
            if state=='close':
                print(f"好友'{friend}'未被设为星标朋友,无需操作！")
            friend_settings_window.close()
            main_window.click_input()
            if close_wechat:
                main_window.close()
        else:
            cancel_star=menu.child_window(**MenuItems.UnStarMenuItem)
            if state=='open':
                print(f"好友'{friend}'已被设为星标朋友,无需操作！")
            if state=='close':
                cancel_star.click_input()
            friend_settings_window.close()
            main_window.click_input() 
            if close_wechat: 
                main_window.close()
            
    @staticmethod
    def change_friend_privacy(friend:str,privacy:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来修改好友权限\n
        Args:
            friend:好友备注。\n
            privacy:好友权限,共有：'仅聊天',"聊天、朋友圈、微信运动等",'不让他（她）看',"不看他（她）"四种\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
            close_wechat:任务结束后是否关闭微信,默认关闭\n
        '''
        privacy_rights=['仅聊天',"聊天、朋友圈、微信运动等",'不让他（她）看',"不看他（她）"]
        if privacy not in privacy_rights:
            raise PrivacyNotCorrectError
        menu,friend_settings_window,main_window=Tools.open_friend_settings_menu(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        privacy_button=menu.child_window(**MenuItems.SetPrivacyMenuItem)
        privacy_button.click_input()
        privacy_window=friend_settings_window.child_window(**Windows.EditPrivacyWindow)
        if privacy=="仅聊天":
            only_chat=privacy_window.child_window(**CheckBoxes.ChatsOnlyCheckBox)
            if only_chat.get_toggle_state():
                privacy_window.close()
                friend_settings_window.close()
                main_window.click_input()
                if close_wechat:
                    main_window.close()
                raise HaveBeenSetChatonlyError(f"好友'{friend}'权限已被设置为仅聊天")
            else:
                only_chat.click_input()
                sure_button=privacy_window.child_window(**Buttons.ConfirmButton)
                sure_button.click_input()
                friend_settings_window.close()
                if close_wechat:
                    main_window.close()
        elif  privacy=="聊天、朋友圈、微信运动等":
            open_chat=privacy_window.child_window(**CheckBoxes.OpenChatCheckBox)
            if open_chat.get_toggle_state():
                privacy_window.close()
                friend_settings_window.close()
                main_window.click_input()
                if close_wechat:
                    main_window.close()
            else:
                open_chat.click_input()
                sure_button=privacy_window.child_window(**Buttons.ConfirmButton)
                sure_button.click_input()
                friend_settings_window.close()
                if close_wechat:
                    main_window.close()
        else:
            if privacy=='不让他（她）看':
                unseen_to_him=privacy_window.child_window(title="",control_type='CheckBox',found_index=0)
                if unseen_to_him.exists():
                    if unseen_to_him.get_toggle_state():
                        privacy_window.close()
                        friend_settings_window.close()
                        main_window.click_input()
                        if close_wechat:
                            main_window.close()
                        raise HaveBeenSetUnseentohimError(f"好友 {friend}权限已被设置为不让他（她）看")
                    else:
                        unseen_to_him.click_input()
                        sure_button=privacy_window.child_window(**Buttons.ConfirmButton)
                        sure_button.click_input()
                        friend_settings_window.close()
                        if close_wechat:
                            main_window.close()
                else:
                    privacy_window.close()
                    friend_settings_window.close()
                    main_window.click_input()
                    if close_wechat:
                        main_window.close()
                    raise HaveBeenSetChatonlyError(f"好友 {friend}已被设置为仅聊天,无法设置为不让他（她）看\n若需将其设置为不让他（她）看,请先将好友设置为：\n聊天、朋友圈、微信运动等")
            if privacy=="不看他（她）":
                dont_see_him=privacy_window.child_window(title="",control_type='CheckBox',found_index=1)
                if dont_see_him.exists():
                    if dont_see_him.get_toggle_state():
                        privacy_window.close()
                        friend_settings_window.close()
                        main_window.click_input()
                        if close_wechat:
                            main_window.close()
                        raise HaveBeenSetDontseehimError(f"好友 {friend}权限已被设置为不看他（她）")
                    else:
                        dont_see_him.click_input()
                        sure_button=privacy_window.child_window(**Buttons.ConfirmButton)
                        sure_button.click_input()
                        friend_settings_window.close()
                        if close_wechat:
                            main_window.close()  
                else:
                    privacy_window.close()
                    friend_settings_window.close()
                    main_window.click_input()
                    if close_wechat:
                        main_window.close()
                    raise HaveBeenSetChatonlyError(f"好友 {friend}已被设置为仅聊天,无法设置为不看他（她）\n若需将其设置为不看他（她）,请先将好友设置为：\n聊天、朋友圈、微信运动等")    
    
    @staticmethod
    def share_contact(friend:str,others:list[str],search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来推荐好友给其他人\n
        Args:
            friend:\t被推荐好友备注\n
            others:\t推荐人备注列表\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        menu,friend_settings_window,main_window=Tools.open_friend_settings_menu(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        share_contact=menu.child_window(**MenuItems.ShareContactMenuItem)
        share_contact.click_input()
        select_contact_window=main_window.child_window(**Main_window.SelectContactWindow)
        if len(others)>1:
            multi=select_contact_window.child_window(**Buttons.MultiSelectButton)
            multi.click_input()
            send=select_contact_window.child_window(**Buttons.SendRespectivelyButton)
        else:
            send=select_contact_window.child_window(**Buttons.SendButton)
        search=select_contact_window.child_window(*Edits.SearchEdit)
        for other_friend in others:
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(other_friend)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.5)
            pyautogui.press('enter')
            pyautogui.hotkey('ctrl','a')
            pyautogui.press('backspace')
            time.sleep(0.5)
        send.click_input()
        friend_settings_window.close()
        if close_wechat:
            main_window.close()

    @staticmethod
    def get_friend_wechat_number(friend:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法根据微信备注获取单个好友的微信号\n
        Args:
            friend:\t好友备注。\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
            close_wechat:任务结束后是否关闭微信,默认关闭\n
        '''
        profile_window,main_window=Tools.open_friend_profile(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        wechat_number=profile_window.child_window(control_type='Text',found_index=4).window_text()
        profile_window.close()
        if close_wechat:
            main_window.close()
        return wechat_number

    @staticmethod
    def get_friends_wechat_numbers(friends:list[str],wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法根据微信备注获取多个好友微信号\n
        Args:
            friends:\t所有待获取微信号的好友的备注列表。\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        wechat_numbers=[]
        for friend in friends:
            profile_window,main_window=Tools.open_friend_profile(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize)
            wechat_number=profile_window.child_window(control_type='Text',found_index=4).window_text()
            wechat_numbers.append(wechat_number)
            profile_window.close()
        wechat_numbers=dict(zip(friends,wechat_numbers)) 
        if close_wechat:       
            main_window.close()
        return wechat_numbers 
    
    @staticmethod
    def tickle_friend(friend:str,maxSearchNum:int=50,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来拍一拍好友\n
        Args:
            friend:好友备注\n
            maxSearchNum:主界面找不到好友聊天记录时在聊天记录窗口内查找好友聊天信息时的最大查找次数,默认为20,如果历史信息比较久远,可以更大一些\n
            search_pages:在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏法搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
            close_wechat:任务结束后是否关闭微信,默认关闭\n
        '''
        def find_firend_buttons_in_chat_history(chatlist):
            if len(chatlist.children())==0:
                chat.close()
                main_window.close()
                raise NoChatHistoryError(f'你还未与{friend}聊天,只有互相聊天后才可以拍一拍哦！')
            else:
                top=chatlist.rectangle().top
                bottom=chatlist.rectangle().bottom
                chats=[chat for chat in chatlist.children() if chat.descendants(control_type='Button',title=friend)]
                buttons=[chat.descendants(control_type='Button',title=friend)[0] for chat in chats]
                visible_buttons=[button for button in buttons if button.is_visible()]
                #聊天窗口的坐标轴是在左上角,好友头像按钮必须在聊天窗口顶部以下底部以上
                visible_buttons=[button for button in buttons if button.rectangle().bottom>top and button.rectangle().top<bottom]#
                return visible_buttons
        def find_latest_chat_in_chat_history():
            #在聊天记录中查找好友最后一次发言
            ChatMessage=main_window.child_window(**Buttons.ChatMessageButton)
            if ChatMessage.exists():#文件传输助手或公众号没有右侧三个点的聊天信息按钮
                ChatMessage.click_input()
                friend_settings_window=main_window.child_window(**Main_window.FriendSettingsWindow)
                chat_history_button=friend_settings_window.child_window(**Buttons.ChatHistoryButton)
                chat_history_button.click_input()
                time.sleep(0.5)
                desktop=Desktop(**Independent_window.Desktop)
                chat_history_window=desktop.window(**Independent_window.ChatHistoryWindow,title=friend)
                Tools.move_window_to_center(Window_handle=chat_history_window.handle)
                rec=chat_history_window.rectangle()
                mouse.click(coords=(rec.right-8,rec.bottom-8))
                contentlist=chat_history_window.child_window(**Lists.ChatHistoryList)
                if not contentlist.exists():
                    chat_history_window.close()
                    main_window.close()
                    raise NoChatHistoryError(f'你还未与{friend}聊天,只有互相聊天后才可以拍一拍哦！')
                friend_chat=contentlist.child_window(control_type='Button',title=friend,found_index=0)
                friend_message=None
                selected_items=[] #selected_items用来存放向上遍历过程中选中的聊天记录          
                for _ in range(maxSearchNum):
                    pyautogui.press('up',_pause=False,presses=2)
                    selected_item=[item for item in contentlist.children(control_type='ListItem') if item.is_selected()][0]
                    selected_items.append(selected_item)
                    if friend_chat.exists():#在`聊天记录窗口找到了某一条对方的聊天记录`
                        friend_message=friend_chat.parent().descendants(title=friend,control_type='Text')[0]
                        break
                    #################################################
                    #当给定number大于实际聊天记录条数时
                    #没必要继续向上了，此时已经到头了，可以提前break了
                    #也就是当前selected_item在selected_items的倒数第二个时，就可以直接退出了，当然，必须得保证selected_items大于2
                    if len(selected_items)>2 and selected_item==selected_items[-2]:
                        break
                if friend_message:#双击后便可定位到聊天界面中去
                    friend_message.double_click_input()
                    chat_history_window.close()
                else:
                    chat_history_window.close()
                    main_window.close()
                    raise TickleError(f'你与好友{friend}最近的聊天记录中没有找到最新消息,无法拍一拍对方!')  
            else:
                main_window.close()
                raise TickleError('非正常聊天好友,可能是文件传输助手,无法拍一拍对方!') 
        chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        chatlist=main_window.child_window(**Main_window.FriendChatList)
        tickle=main_window.child_window(**Main_window.Tickle)
        buttons=find_firend_buttons_in_chat_history(chatlist)
        if buttons:
            for button in buttons:
                button.right_click_input()
                if tickle.exists():
                    break
            tickle.click_input()
        else:
            find_latest_chat_in_chat_history()
            buttons=find_firend_buttons_in_chat_history(chatlist)
            for button in buttons:
                button.right_click_input()
                if tickle.exists():
                    break
            tickle.click_input()
        if close_wechat:
            chat.close()

    @staticmethod
    def get_chat_history(friend:str,number:int=10,capture_screen:bool=False,folder_path:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来获取好友或群聊的聊天记录\n
        Args:
            friend:\t好友或群聊备注或昵称\n
            number:\t待获取的聊天记录条数,默认10条\n
            capture_scren:\t聊天记录是否截屏,默认不截屏\n
            folder_path:\t存放聊天记录截屏图片的文件夹路径\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
            close_wechat:任务结束后是否关闭微信,默认关闭\n'
        '''
        def get_info(message):
            message_sender=message.descendants(control_type='Text')[0].window_text()#无论什么类型消息,发送人永远是属性为Texts的UI组件中的第一个
            message_time=message.descendants(control_type='Text')[1].window_text()#无论什么类型消息.发送时间都是属性为Texts的UI组件中的第二个
            #至于消息的内容那就需要仔细判断一下了
            specialMegCN={'[图片]':'图片消息','[视频]':'视频消息','[动画表情]':'动画表情','[视频号]':'视频号'}
            specialMegEN={'[Photo]':'图片消息','[Video]':'视频消息','[Sticker]':'动画表情','[Channel]':'视频号'}
            specialMegTC={'[圖片]':'图片消息','[影片]':'视频消息','[動態貼圖]':'动画表情','[影音號]':'视频号'}
            #不同语言,处理消息内容时不同
            if language=='简体中文':
                if message.window_text() in specialMegCN.keys():#内容在特殊消息中
                    message_content=specialMegCN.get(message.window_text())
                else:#文件,卡片链接,语音,以及正常的文本消息
                    if message.window_text()=='[文件]':
                        filename=message.descendants(control_type='Text')[2].texts()[0]
                        message_content=f'文件:{filename}'
                    elif re.match(r'\[语音\]\d+秒',message.window_text()):
                        message_content='语音消息'
                    elif len(message.descendants(control_type='Text'))>3:#
                        cardContent=message.descendants(control_type='Text')[2:]
                        cardContent=[link.window_text() for link in cardContent]
                        if '微信转账' in cardContent:
                            index=cardContent.index('微信转账')
                            message_content=f'微信转账:{cardContent[index-2]}:{cardContent[index-1]}'
                        else:
                            message_content='卡片内容:'+','.join(cardContent)
                    else:#正常文本
                        texts=message.descendants(control_type='Text')
                        texts=[text.window_text() for text in texts]
                        message_content=texts[2]
                    
            if language=='英文':
                if message.window_text() in specialMegEN.keys():
                    message_content=specialMegEN.get(message.window_text())
                else:#文件,卡片链接,语音,以及正常的文本消息
                    if message.window_text()=='[File]':
                        filename=message.descendants(control_type='Text')[2].texts()[0]
                        message_content=f'文件:{filename}'
                    elif re.match(r'\[Audio\]\d+s',message.window_text()):
                        message_content='语音消息'

                    elif len(message.descendants(control_type='Text'))>3:#
                        cardContent=message.descendants(control_type='Text')[2:]
                        cardContent=[link.window_text() for link in cardContent]
                        if 'Weixin Transfer' in cardContent:
                            index=cardContent.index('Weixin Transfer')
                            message_content=f'微信转账:{cardContent[index-2]}:{cardContent[index-1]}'
                        else:
                            message_content='卡片内容:'+','.join(cardContent)
                    else:#正常文本
                        texts=message.descendants(control_type='Text')
                        texts=[text.window_text() for text in texts]
                        message_content=texts[2]
            
            if language=='繁体中文':
                if message.window_text() in specialMegTC.keys():
                    message_content=specialMegTC.get(message.window_text())
                else:#文件,卡片链接,语音,以及正常的文本消息
                    if message.window_text()=='[檔案]':
                        filename=message.descendants(control_type='Text')[2].texts()[0]
                        message_content=f'文件:{filename}'
                    elif re.match(r'\[語音\]\d+秒',message.window_text()):
                        message_content='语音消息'
                    elif len(message.descendants(control_type='Text'))>3:#
                        cardContent=message.descendants(control_type='Text')[2:]
                        cardContent=[link.window_text() for link in cardContent]
                        if message.window_text()=='' and '微信轉賬' in cardContent:
                            index=cardContent.index('微信轉賬')
                            message_content=f'微信转账:{cardContent[index-2]}:{cardContent[index-1]}'
                        else:
                            message_content='链接卡片内容:'+','.join(cardContent)
                    else:#正常文本
                        texts=message.descendants(control_type='Text')
                        texts=[text.window_text() for text in texts]
                        message_content=texts[2]
            return message_sender,message_time,message_content
    
        def ByNum():
            #不指定起始和截止时间
            rec=chat_history_window.rectangle()
            mouse.click(coords=(rec.right-10,rec.bottom-10))
            pyautogui.press('End')
            chat_history=[]
            contentList=chat_history_window.child_window(**Lists.ChatHistoryList)
            if not contentList.exists():    
                chat_history_window.close()
                raise NoChatHistoryError(f'你还未与{friend}聊天,无法获取聊天记录!')  
            selected_items=[] #selected_items用来存放向上遍历过程中选中的聊天记录          
            for _ in range(number):
                pyautogui.press('up',_pause=False,presses=2)
                selected_item=[item for item in contentList.children(control_type='ListItem') if item.is_selected()][0]
                selected_items.append(selected_item)
                #################################################
                #当给定number大于实际聊天记录条数时
                #没必要继续向上了，此时已经到头了，可以提前break了
                #也就是当前selected_item在selected_items的倒数第二个时，就可以直接退出了，当然，必须得保证selected_items大于2
                if len(selected_items)>2 and selected_item==selected_items[-2]:
                    break
                chat_history.append(get_info(selected_item))
                ############################################
            pyautogui.press('END')
            ###############################################################
            #截图逻辑:selected_items中存放的是向上遍历过程中被选中的且数量正确(不使用number是因为number可能比所有的聊天记录总数还大)聊天记录列表
            #selected_items最多也就是所有的聊天记录
            #length是向上时每一页的聊天记录数量，比较一下length是否达到selected_items内的聊天记录数量，如果达到那么不再截取每一页的图片
            if capture_screen:
                Num=1
                length=len(contentList.children(control_type='ListItem'))
                while length<len(selected_items):
                    chat_history_image=chat_history_window.capture_as_image()
                    if folder_path:
                        pic_path=os.path.abspath(os.path.join(folder_path,f'与{friend}的聊天记录{Num}.png'))
                    else:
                        pic_path=os.path.abspath(os.path.join(os.getcwd(),f'与{friend}的聊天记录{Num}.png'))
                    chat_history_image.save(pic_path)
                    pyautogui.keyDown('pageup',_pause=False)
                    Num+=1
                    length+=len(contentList.children(control_type='ListItem'))
                #退出循环后还要记得截最后一张图片
                chat_history_image=chat_history_window.capture_as_image()
                if folder_path:
                    pic_path=os.path.abspath(os.path.join(folder_path,f'与{friend}的聊天记录{Num}.png'))
                else:
                    pic_path=os.path.abspath(os.path.join(os.getcwd(),f'与{friend}的聊天记录{Num}.png'))
                chat_history_image.save(pic_path)
            pyautogui.press('END')
            chat_history_window.close()
            if len(chat_history)<number:
                warn(message=f"你与{friend}的聊天记录不足{number},已为你导出全部的{len(chat_history)}条聊天记录",category=ChatHistoryNotEnough)
                chat_history_json=json.dumps(chat_history,ensure_ascii=False,indent=4)
            else:
                chat_history_json=json.dumps(chat_history[:number],ensure_ascii=False,indent=4)
            return chat_history_json
        
        if capture_screen and folder_path:
            folder_path=re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',folder_path)
            if not Systemsettings.is_dirctory(folder_path):
                raise NotFolderError(r'给定路径不是文件夹!无法保存聊天记录截图,请重新选择文件夹！')
        chat_history_window=Tools.open_chat_history(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat,search_pages=search_pages)[0]
        chat_history_json=ByNum()
        ########################################################################
        return chat_history_json
   
class GroupSettings():

    @staticmethod
    def pin_group(group_name:str,state:str='open',search_pages:int=5,wechat_path=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来将群聊在会话内置顶或取消置顶\n
        Args:
            group_name:\t群聊备注。\n
            state:取值为open或close,默认值为open,用来决定置顶或取消置顶群聊,state为open时执行置顶操作,state为close时执行取消置顶操作\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        choices=['open','close']
        if state not in choices:
            raise WrongParameterError
        main_window,chat_window=Tools.open_dialog_window(friend=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages) 
        Tool_bar=chat_window.child_window(found_index=1,title='',control_type='ToolBar')
        Pinbutton=Tool_bar.child_window(**Buttons.PinButton)
        if Pinbutton.exists():
            if state=='open':
                Pinbutton.click_input()
            if state=='close':
                print(f"群聊'{group_name}'未被置顶,无需取消置顶!")
        else:
            Cancelpinbutton=Tool_bar.child_window(**Buttons.CancelPinButton)
            if state=='open':
                print(f"群聊'{group_name}'已被置顶,无需置顶!")
            if state=='close':
                Cancelpinbutton.click_input()
        main_window.click_input()
        if close_wechat:
            main_window.close()

    @staticmethod
    def create_group_chat(friends:list[str],group_name:str=None,wechat_path:str=None,is_maximize:bool=True,messages:list=[str],close_wechat:bool=True):
        '''
        该方法用来新建群聊\n
        Args:
            friends:\t新群聊的好友备注列表。\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
            messages:\t建群后是否发送消息,messages非空列表,在建群后会发送消息\n
        '''
        if len(friends)<=2:
            raise CantCreateGroupError
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        cerate_group_chat_button=main_window.child_window(**Buttons.CreateGroupChatButton)
        cerate_group_chat_button.click_input()
        Add_member_window=main_window.child_window(**Main_window.AddMemberWindow)
        for member in friends:
            search=Add_member_window.child_window(*Edits.SearchEdit)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(member)
            pyautogui.hotkey('ctrl','v')
            pyautogui.press("enter")
            pyautogui.press('backspace')
            time.sleep(2)
        confirm=Add_member_window.child_window(Buttons.CompleteButton)
        confirm.click_input()
        time.sleep(10)
        if messages:
            group_edit=main_window.child_window(**Main_window.CurrentChatWindow)
            group_edit.click_input()
            for message in message:
                Systemsettings.copy_text_to_windowsclipboard(message)
                pyautogui.hotkey('ctrl','v')
                pyautogui.hotkey('alt','s',_pause=False)
        if group_name:
            chat_message=main_window.child_window(**Buttons.ChatMessageButton)
            chat_message.click_input()
            group_settings_window=main_window.child_window(**Main_window.GroupSettingsWindow)
            change_group_name_button=group_settings_window.child_window(**Buttons.ChangeGroupNameButton)
            change_group_name_button.click_input()
            pyautogui.hotkey('ctrl','a')
            pyautogui.press('backspace')
            change_group_name_edit=group_settings_window.child_window(**Edits.EditWnd)
            change_group_name_edit.click_input()
            Systemsettings.copy_text_to_windowsclipboard(group_name)
            pyautogui.hotkey('ctrl','v')
            pyautogui.press('enter')
            group_settings_window.close()
        if close_wechat:    
            main_window.close()

    @staticmethod
    def change_group_name(group_name:str,change_name:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来修改群聊名称\n
        Args:
            group_name:群聊名称\n
            change_name:待修改的名称\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
            close_wechat:任务结束后是否关闭微信,默认关闭\n
        '''
        if group_name==change_name:
            raise SameNameError(f'待修改的群名需与先前的群名不同才可修改！')
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        ChangeGroupNameWarnText=group_chat_settings_window.child_window(**Texts.ChangeGroupNameWarnText)
        if ChangeGroupNameWarnText.exists():
            group_chat_settings_window.close()
            main_window.click_input()
            if close_wechat:
                main_window.close()
            raise NoPermissionError(f"你不是'{group_name}'的群主或管理员,无权修改群聊名称")
        else:
            change_group_name_button=group_chat_settings_window.child_window(**Buttons.ChangeGroupNameButton)
            change_group_name_button.click_input()
            change_group_name_edit=group_chat_settings_window.child_window(**Edits.EditWnd)
            change_group_name_edit.click_input()
            time.sleep(0.5)
            pyautogui.press('end')
            time.sleep(0.5)
            pyautogui.press('backspace',presses=35,_pause=False)
            time.sleep(0.5)
            Systemsettings.copy_text_to_windowsclipboard(change_name)
            pyautogui.hotkey('ctrl','v')
            pyautogui.press('enter')
            group_chat_settings_window.close()
            main_window.click_input()
            if close_wechat:
                main_window.close()

    @staticmethod
    def change_my_nickname_in_group(group_name:str,my_nickname:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来修改我在本群的昵称\n
        Args:
            group_name:\t群聊名称\n
            my_nickname:\t待修改昵称\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        change_my_nickname_button=group_chat_settings_window.child_window(**Buttons.MyNicknameInGroupButton)
        change_my_nickname_button.click_input()
        change_my_nickname_edit=group_chat_settings_window.child_window(**Edits.EditWnd)
        change_my_nickname_edit.click_input()
        time.sleep(0.5)
        pyautogui.press('end')
        time.sleep(0.5)
        pyautogui.press('backspace',presses=35,_pause=False)
        time.sleep(0.5)
        Systemsettings.copy_text_to_windowsclipboard(my_nickname)
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('enter')
        group_chat_settings_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close()

    @staticmethod
    def change_group_remark(group_name:str,group_remark:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来修改群聊备注\n
        Args:
            group_name:\t群聊名称\n
            group_remark:\t群聊备注\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        change_group_remark_button=group_chat_settings_window.child_window(**Buttons.RemarkButton)
        change_group_remark_button.click_input()
        change_group_remark_edit=group_chat_settings_window.child_window(**Edits.EditWnd)
        change_group_remark_edit.click_input()
        time.sleep(0.5)
        pyautogui.press('end')
        time.sleep(0.5)
        pyautogui.press('backspace',presses=35,_pause=False)
        time.sleep(0.5)
        Systemsettings.copy_text_to_windowsclipboard(group_remark)
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('enter')
        group_chat_settings_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close()
    
    @staticmethod
    def show_group_members_nickname(group_name:str,state:str='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来开启或关闭显示群聊成员名称\n
        Args:
            group_name:\t群聊名称\n
            state:\t取值为open或close,默认值为open,用来决定是否显示群聊成员名称,state为open时执行将开启显示群聊成员名称操作,state为close时执行关闭显示群聊成员名称\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        choices=['open','close']
        if state not in choices:
            raise WrongParameterError
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        show_group_members_nickname_button=group_chat_settings_window.child_window(**CheckBoxes.OnScreenNamesCheckBox)
        if not show_group_members_nickname_button.get_toggle_state():
            if state=='open':
                show_group_members_nickname_button.click_input()
            if state=='close':
                print(f"群聊'{group_name}'显示群成员昵称功能未开启,无需关闭!")
            group_chat_settings_window.close()
            main_window.click_input()
            if close_wechat:
                main_window.close()
        else:
            if state=='open':
                print(f"群聊'{group_name}'显示群成员昵称功能已开启,无需再开启!")
            if state=='close':
                show_group_members_nickname_button.click_input()
            group_chat_settings_window.close()
            main_window.click_input()
            main_window.close()
    
    @staticmethod
    def mute_group_notifications(group_name:str,state:str='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来开启或关闭群聊消息免打扰\n
        Args:
            group_name:\t群聊名称\n
            state:\t取值为open或close,默认值为open,用来决定是否对该群开启消息免打扰,state为open时执行将开启消息免打扰操作,state为close时执行关闭消息免打扰\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        choices=['open','close']
        if state not in choices:
            raise WrongParameterError
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        mute_checkbox=group_chat_settings_window.child_window(**CheckBoxes.MuteNotificationsCheckBox)
        if mute_checkbox.get_toggle_state():
            if state=='open':
                print(f"群聊'{group_name}'的消息免打扰已开启,无需再开启消息免打扰!")
            if state=='close':
                mute_checkbox.click_input()
            group_chat_settings_window.close()
            main_window.click_input()
            if close_wechat:  
                main_window.close()
           
        else:
            if state=='open':
                mute_checkbox.click_input()
            if state=='close':
                print(f"群聊'{group_name}'的消息免打扰未开启,无需再关闭消息免打扰!")
            group_chat_settings_window.close()
            main_window.click_input()
            if close_wechat:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                main_window.close() 

    @staticmethod
    def sticky_group_on_top(group_name:str,state='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来将微信群聊聊天置顶或取消聊天置顶\n
        Args:
            group_name:\t群聊名称\n
            state:\t取值为open或close,默认值为open,用来决定是否将该群聊聊天置顶,state为open时将该群聊聊天置顶,state为close时取消该群聊聊天置顶\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        choices=['open','close']
        if state not in choices:
            raise WrongParameterError
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        sticky_on_top_checkbox=group_chat_settings_window.child_window(**CheckBoxes.StickyonTopCheckBox)
        if not sticky_on_top_checkbox.get_toggle_state():
            if state=='open':
                sticky_on_top_checkbox.click_input()
            if state=='close':
                print(f"群聊'{group_name}'的置顶聊天未开启,无需再关闭置顶聊天!")
            group_chat_settings_window.close()
            main_window.click_input() 
            if close_wechat: 
                main_window.close()
        else:
            if state=='open':
                print(f"群聊'{group_name}'的置顶聊天已开启,无需再设置为置顶聊天!")
            if state=='close':
                sticky_on_top_checkbox.click_input()
            group_chat_settings_window.close()
            main_window.click_input()
            if close_wechat:
                main_window.close() 

    @staticmethod           
    def save_group_to_contacts(group_name:str,state:str='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来将群聊保存或取消保存到通讯录\n
        Args:
            group_name:\t群聊名称\n
            state:\t取值为open或close,默认值为open,用来,state为open时将该群聊保存至通讯录,state为close时取消该群保存到通讯录\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        choices=['open','close']
        if state not in choices:
            raise WrongParameterError
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        save_to_contacts_checkbox=group_chat_settings_window.child_window(**CheckBoxes.SavetoContactsCheckBox)
        if not save_to_contacts_checkbox.get_toggle_state():
            if state=='open':
                save_to_contacts_checkbox.click_input()
            if state=='close':
                print(f"群聊'{group_name}'未保存到通讯录,无需取消保存到通讯录！")
            group_chat_settings_window.close()
            main_window.click_input() 
            if close_wechat: 
                main_window.close()
        else:
            if state=='open':
                print(f"群聊'{group_name}'已保存到通讯录,无需再保存到通讯录")
            if state=='close':
                save_to_contacts_checkbox.click_input()
            group_chat_settings_window.close()
            main_window.click_input()
            if close_wechat:
                main_window.close() 
    @staticmethod
    def clear_group_chat_history(group_name:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来清空群聊聊天记录\n
        Args:
            group_name:群聊名称\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        clear_chat_history_button=group_chat_settings_window.child_window(**Buttons.ClearChatHistoryButton)
        clear_chat_history_button.click_input()
        confirm_button=main_window.child_window(**Buttons.ConfirmEmptyChatHistoryButon)
        confirm_button.click_input()
        if close_wechat:
            main_window.close()

    @staticmethod
    def quit_group_chat(group_name:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来退出微信群聊\n
        Args:
            group_name:\t群聊名称\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        quit_group_chat_button=group_chat_settings_window.child_window(**Buttons.QuitGroupButton)
        quit_group_chat_button.click_input()
        quit_button=main_window.child_window(**Buttons.ConfirmQuitGroupButton)
        quit_button.click_input()
        if close_wechat:
            main_window.close()

    @staticmethod
    def invite_others_to_group(group_name:str,friends:list[str],search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来邀请他人至群聊\n
        Args:
            group_name:\t群聊名称\n
            friends:\t所有待邀请好友备注列表\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        add=group_chat_settings_window.child_window(title='',control_type="Button",found_index=1)
        add.click_input()
        Add_member_window=main_window.child_window(**Main_window.AddMemberWindow)
        for member in friends:
            search=Add_member_window.child_window(*Edits.SearchEdit)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(member)
            pyautogui.hotkey('ctrl','v')
            pyautogui.press("enter")
            pyautogui.press('backspace')
            time.sleep(2)
        confirm=Add_member_window.child_window(**Buttons.CompleteButton)
        confirm.click_input()
        group_chat_settings_window.close()
        if close_wechat:
            main_window.close()

    @staticmethod
    def remove_friend_from_group(group_name:str,friends:list[str],search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来将群成员移出群聊\n
        Args:
            group_name:\t群聊名称\n
            friends:\t所有移出群聊的成员备注列表\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        delete=group_chat_settings_window.child_window(title='',control_type="Button",found_index=2)
        if not delete.exists():
            group_chat_settings_window.close()
            main_window.click_input()
            if close_wechat:
                main_window.close()
            raise NoPermissionError(f"你不是'{group_name}'的群主或管理员,无权将好友移出群聊")
        else:
            delete.click_input()
            delete_member_window=main_window.child_window(**Main_window.DeleteMemberWindow)
            for member in friends:
                search=delete_member_window.child_window(*Edits.SearchEdit)
                search.click_input()
                Systemsettings.copy_text_to_windowsclipboard(member)
                pyautogui.hotkey('ctrl','v')
                button=delete_member_window.child_window(title=member,control_type='Button')
                button.click_input()
            confirm=delete_member_window.child_window(**Buttons.CompleteButton)
            confirm.click_input()
            confirm_dialog_window=delete_member_window.child_window(class_name='ConfirmDialog',framework_id='Win32')
            delete=confirm_dialog_window.child_window(**Buttons.DeleteButton)
            delete.click_input()
            group_chat_settings_window.close()
            if close_wechat:
                main_window.close()

    @staticmethod
    def add_friend_from_group(group_name:str,friend:str,request_content:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来添加群成员为好友\n
        Args:
            group_name:\t群聊名称\n
            friend:\t待添加群聊成员群聊中的名称\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        search=group_chat_settings_window.child_window(**Edits.SearchGroupMemeberEdit)
        search.click_input()
        Systemsettings.copy_text_to_windowsclipboard(friend)
        pyautogui.hotkey('ctrl','v')
        friend_butotn=group_chat_settings_window.child_window(title=friend,control_type='Button',found_index=1)
        friend_butotn.double_click_input()
        contact_window=group_chat_settings_window.child_window(class_name='ContactProfileWnd',framework_id="Win32")
        add_to_contacts_button=contact_window.child_window(**Buttons.AddToContactsButton)
        if add_to_contacts_button.exists():
            add_to_contacts_button.click_input()
            add_friend_request_window=main_window.child_window(**Main_window.AddFriendRequestWindow)
            request_content_edit=add_friend_request_window.child_window(**Edits.RequestContentEdit)
            request_content_edit.click_input()
            pyautogui.hotkey('ctrl','a')
            pyautogui.press('backspace')
            request_content_edit=add_friend_request_window.child_window(title='',control_type='Edit',found_index=0)
            Systemsettings.copy_text_to_windowsclipboard(request_content)
            pyautogui.hotkey('ctrl','v')
            confirm_button=add_friend_request_window.child_window(**Buttons.ConfirmButton)
            confirm_button.click_input()
            time.sleep(5)
            if close_wechat:
                main_window.close()
        else:
            group_chat_settings_window.close()
            if close_wechat:
                main_window.close()
            raise AlreadyInContactsError(f"好友'{friend}'已在通讯录中,无需通过该群聊添加！")
    
    @staticmethod
    def edit_group_notice(group_name:str,content:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来编辑群公告\n
        Args:
            group_name:\t群聊名称\n
            content:\t群公告内容\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat\t:任务结束后是否关闭微信,默认关闭\n
        '''
        group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        edit_group_notice_button=group_chat_settings_window.child_window(**Buttons.EditGroupNotificationButton)
        edit_group_notice_button.click_input()
        edit_group_notice_window=Tools.move_window_to_center(Window=Independent_window.GroupAnnouncementWindow)
        EditGroupNoticeWarnText=edit_group_notice_window.child_window(**Texts.EditGroupNoticeWarnText)
        if EditGroupNoticeWarnText.exists():
            edit_group_notice_window.close()
            main_window.click_input()
            if close_wechat:
                main_window.close()
            raise NoPermissionError(f"你不是'{group_name}'的群主或管理员,无权发布群公告")
        else:
            main_window.minimize()
            edit_board=edit_group_notice_window.child_window(control_type='Edit',found_index=0)
            if edit_board.window_text()!='':
                edit_button=edit_group_notice_window.child_window(**Buttons.EditButton)
                edit_button.click_input()
                time.sleep(1)
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('backspace')
                Systemsettings.copy_text_to_windowsclipboard(content)
                pyautogui.hotkey('ctrl','v')
                confirm_button=edit_group_notice_window.child_window(**Buttons.CompleteButton)
                confirm_button.click_input()
                confirm_pane=edit_group_notice_window.child_window(**Panes.ConfirmPane)
                forward=confirm_pane.child_window(**Buttons.PublishButton)
                forward.click_input()
                time.sleep(2)
                main_window.click_input()
                if close_wechat:
                    main_window.close()
            else:
                edit_board.click_input()
                time.sleep(1)
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('backspace')
                Systemsettings.copy_text_to_windowsclipboard(content)
                pyautogui.hotkey('ctrl','v')
                confirm_button=edit_group_notice_window.child_window(**Buttons.CompleteButton)
                confirm_button.click_input()
                confirm_pane=edit_group_notice_window.child_window(**Panes.ConfirmPane)
                forward=confirm_pane.child_window(**Buttons.PublishButton)
                forward.click_input()
                time.sleep(2)
                main_window.click_input()
                if close_wechat:
                    main_window.close()

    @staticmethod
    def get_chat_history(friend:str,number:int=10,capture_screen:bool=False,folder_path:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来获取好友或群聊的聊天记录\n
        Args:
            friend:\t好友或群聊备注或昵称\n
            number:\t待获取的聊天记录条数,默认10条\n
            capture_scren:\t聊天记录是否截屏,默认不截屏\n
            folder_path:\t存放聊天记录截屏图片的文件夹路径\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:微信界面是否全屏,默认全屏。\n
            close_wechat:任务结束后是否关闭微信,默认关闭\n'
        '''
        def get_info(message):
            message_sender=message.descendants(control_type='Text')[0].window_text()#无论什么类型消息,发送人永远是属性为Texts的UI组件中的第一个
            message_time=message.descendants(control_type='Text')[1].window_text()#无论什么类型消息.发送时间都是属性为Texts的UI组件中的第二个
            #至于消息的内容那就需要仔细判断一下了
            specialMegCN={'[图片]':'图片消息','[视频]':'视频消息','[动画表情]':'动画表情','[视频号]':'视频号'}
            specialMegEN={'[Photo]':'图片消息','[Video]':'视频消息','[Sticker]':'动画表情','[Channel]':'视频号'}
            specialMegTC={'[圖片]':'图片消息','[影片]':'视频消息','[動態貼圖]':'动画表情','[影音號]':'视频号'}
            #不同语言,处理消息内容时不同
            if language=='简体中文':
                if message.window_text() in specialMegCN.keys():#内容在特殊消息中
                    message_content=specialMegCN.get(message.window_text())
                else:#文件,卡片链接,语音,以及正常的文本消息
                    if message.window_text()=='[文件]':
                        filename=message.descendants(control_type='Text')[2].texts()[0]
                        message_content=f'文件:{filename}'
                    elif re.match(r'\[语音\]\d+秒',message.window_text()):
                        message_content='语音消息'
                    elif len(message.descendants(control_type='Text'))>3:#
                        cardContent=message.descendants(control_type='Text')[2:]
                        cardContent=[link.window_text() for link in cardContent]
                        if '微信转账' in cardContent:
                            index=cardContent.index('微信转账')
                            message_content=f'微信转账:{cardContent[index-2]}:{cardContent[index-1]}'
                        else:
                            message_content='卡片内容:'+','.join(cardContent)
                    else:#正常文本
                        texts=message.descendants(control_type='Text')
                        texts=[text.window_text() for text in texts]
                        message_content=texts[2]
                    
            if language=='英文':
                if message.window_text() in specialMegEN.keys():
                    message_content=specialMegEN.get(message.window_text())
                else:#文件,卡片链接,语音,以及正常的文本消息
                    if message.window_text()=='[File]':
                        filename=message.descendants(control_type='Text')[2].texts()[0]
                        message_content=f'文件:{filename}'
                    elif re.match(r'\[Audio\]\d+s',message.window_text()):
                        message_content='语音消息'

                    elif len(message.descendants(control_type='Text'))>3:#
                        cardContent=message.descendants(control_type='Text')[2:]
                        cardContent=[link.window_text() for link in cardContent]
                        if 'Weixin Transfer' in cardContent:
                            index=cardContent.index('Weixin Transfer')
                            message_content=f'微信转账:{cardContent[index-2]}:{cardContent[index-1]}'
                        else:
                            message_content='卡片内容:'+','.join(cardContent)
                    else:#正常文本
                        texts=message.descendants(control_type='Text')
                        texts=[text.window_text() for text in texts]
                        message_content=texts[2]
            
            if language=='繁体中文':
                if message.window_text() in specialMegTC.keys():
                    message_content=specialMegTC.get(message.window_text())
                else:#文件,卡片链接,语音,以及正常的文本消息
                    if message.window_text()=='[檔案]':
                        filename=message.descendants(control_type='Text')[2].texts()[0]
                        message_content=f'文件:{filename}'
                    elif re.match(r'\[語音\]\d+秒',message.window_text()):
                        message_content='语音消息'
                    elif len(message.descendants(control_type='Text'))>3:#
                        cardContent=message.descendants(control_type='Text')[2:]
                        cardContent=[link.window_text() for link in cardContent]
                        if message.window_text()=='' and '微信轉賬' in cardContent:
                            index=cardContent.index('微信轉賬')
                            message_content=f'微信转账:{cardContent[index-2]}:{cardContent[index-1]}'
                        else:
                            message_content='链接卡片内容:'+','.join(cardContent)
                    else:#正常文本
                        texts=message.descendants(control_type='Text')
                        texts=[text.window_text() for text in texts]
                        message_content=texts[2]

            return message_sender,message_time,message_content
        
        def ByNum():
            #不指定起始和截止时间
            rec=chat_history_window.rectangle()
            mouse.click(coords=(rec.right-10,rec.bottom-10))
            pyautogui.press('End')
            chat_history=[]
            contentList=chat_history_window.child_window(**Lists.ChatHistoryList)
            if not contentList.exists():    
                chat_history_window.close()
                raise NoChatHistoryError(f'你还未与{friend}聊天,无法获取聊天记录!')  
            selected_items=[] #selected_items用来存放向上遍历过程中选中的聊天记录          
            for _ in range(number):
                pyautogui.press('up',_pause=False,presses=2)
                selected_item=[item for item in contentList.children(control_type='ListItem') if item.is_selected()][0]
                selected_items.append(selected_item)
                #################################################
                #当给定number大于实际聊天记录条数时
                #没必要继续向上了，此时已经到头了，可以提前break了
                #也就是当前selected_item在selected_items的倒数第二个时，就可以直接退出了，当然，必须得保证selected_items大于2
                if len(selected_items)>2 and selected_item==selected_items[-2]:
                    break
                chat_history.append(get_info(selected_item))
                ############################################
            pyautogui.press('END')
            ###############################################################
            #截图逻辑:selected_items中存放的是向上遍历过程中被选中的且数量正确(不使用number是因为number可能比所有的聊天记录总数还大)聊天记录列表
            #selected_items最多也就是所有的聊天记录
            #length是向上时每一页的聊天记录数量，比较一下length是否达到selected_items内的聊天记录数量，如果达到那么不再截取每一页的图片
            if capture_screen:
                Num=1
                length=len(contentList.children(control_type='ListItem'))
                while length<len(selected_items):
                    chat_history_image=chat_history_window.capture_as_image()
                    if folder_path:
                        pic_path=os.path.abspath(os.path.join(folder_path,f'与{friend}的聊天记录{Num}.png'))
                    else:
                        pic_path=os.path.abspath(os.path.join(os.getcwd(),f'与{friend}的聊天记录{Num}.png'))
                    chat_history_image.save(pic_path)
                    pyautogui.keyDown('pageup',_pause=False)
                    Num+=1
                    length+=len(contentList.children(control_type='ListItem'))
                #退出循环后还要记得截最后一张图片
                chat_history_image=chat_history_window.capture_as_image()
                if folder_path:
                    pic_path=os.path.abspath(os.path.join(folder_path,f'与{friend}的聊天记录{Num}.png'))
                else:
                    pic_path=os.path.abspath(os.path.join(os.getcwd(),f'与{friend}的聊天记录{Num}.png'))
                chat_history_image.save(pic_path)
            pyautogui.press('END')
            chat_history_window.close()
            if len(chat_history)<number:
                warn(message=f"你与{friend}的聊天记录不足{number},已为你导出全部的{len(chat_history)}条聊天记录",category=ChatHistoryNotEnough)
                chat_history_json=json.dumps(chat_history,ensure_ascii=False,indent=4)
            else:
                chat_history_json=json.dumps(chat_history[:number],ensure_ascii=False,indent=4)
            return chat_history_json
        
        if capture_screen and folder_path:
            folder_path=re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',folder_path)
            if not Systemsettings.is_dirctory(folder_path):
                raise NotFolderError(r'给定路径不是文件夹!无法保存聊天记录截图,请重新选择文件夹！')
        chat_history_window=Tools.open_chat_history(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat,search_pages=search_pages)[0]
        chat_history_json=ByNum()
        ########################################################################
        return chat_history_json

class Contacts():
    @staticmethod
    def get_friends_names(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来获取通讯录中所有好友的名称与昵称。\n
        结果以json格式返回\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        def get_names(friends):
            names=[]
            for ListItem in friends:
                nickname=ListItem.descendants(control_type='Button')[0].window_text()
                remark=ListItem.descendants(control_type='Text')[0].window_text()
                names.append((nickname,remark))
            return names
        contacts_settings_window=Tools.open_contacts_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=True)[0]
        total_pane=contacts_settings_window.child_window(**Panes.ContactsManagePane)
        total_number=total_pane.child_window(control_type='Text',found_index=1).window_text()
        total_number=total_number.replace('(','').replace(')','')
        total_number=int(total_number)#好友总数
        #先点击选中第一个好友，双击选中取消后，才可以在按下pagedown之后才可以滚动页面，每页可以记录11人
        friends_list=contacts_settings_window.child_window(title='',control_type='List')
        friends=friends_list.children(control_type='ListItem')
        first=friends_list.children()[0].descendants(control_type='CheckBox')[0]     
        first.double_click_input()
        pages=total_number//11#点击选中在不选中第一个好友后，每一页最少可以记录11人，pages是总页数，也是pagedown按钮的按下次数
        res=total_number%11#好友人数不是11的整数倍数时，需要处理余数部分
        Names=[]
        if total_number<=11:
            friends=friends_list.children(control_type='ListItem')
            Names.extend(get_names(friends))
            contacts_settings_window.close()
            contacts=[{'昵称':name[1],'备注':name[0]}for name in Names]
            contacts_json=json.dumps(contacts,ensure_ascii=False,indent=4)
            if not close_wechat:
                Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
            return contacts_json
        else:
            for _ in range(pages):
                friends=friends_list.children(control_type='ListItem')
                Names.extend(get_names(friends))
                pyautogui.keyDown('pagedown',_pause=False)
            if res:
            #处理余数部分
                pyautogui.keyDown('pagedown',_pause=False)
                friends=friends_list.children(control_type='ListItem')
                Names.extend(get_names(friends[11-res:11]))
                contacts_settings_window.close()
                contacts=[{'昵称':name[1],'备注':name[0]}for name in Names]
                contacts_json=json.dumps(contacts,ensure_ascii=False,indent=4)
                if not close_wechat:
                    Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
            else:
                contacts_settings_window.close()
                contacts=[{'昵称':name[1],'备注':name[0]}for name in Names]
                contacts_json=json.dumps(contacts,ensure_ascii=False,indent=4)
                if not close_wechat:
                    Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
            return contacts_json
    @staticmethod
    def get_friends_info(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该函数用来获取通讯录中所有微信好友的基本信息(昵称,备注,微信号),速率约为1秒7-12个好友,注:不包含企业微信好友,\n
        结果以json格式返回\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        #获取右侧变化的好友信息面板内的信息
        def get_info():
            nickname=None
            wechatnumber=None
            remark=None
            try: #通讯录界面右侧的好友信息面板  
                global base_info_pane
                try:
                    base_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                except IndexError:
                    base_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                base_info=base_info_pane.descendants(control_type='Text')
                base_info=[element.window_text() for element in base_info]
                # #如果有昵称选项,说明好友有备注
                if language=='简体中文':
                    if base_info[1]=='昵称：':
                        remark=base_info[0]   
                        nickname=base_info[2]
                        wechatnumber=base_info[4]
                    else:#没有昵称选项，好友昵称就是备注,备注就是昵称
                        nickname=base_info[0]
                        remark=nickname
                        wechatnumber=base_info[2]

                if language=='英文':
                    if base_info[1]=='Name: ':
                        remark=base_info[0]   
                        nickname=base_info[2]
                        wechatnumber=base_info[4]
                    else:#没有昵称选项，好友昵称就是备注,备注就是昵称
                        nickname=base_info[0]
                        remark=nickname
                        wechatnumber=base_info[2]

                if language=='繁体中文':
                    if base_info[1]=='暱稱: ':
                        remark=base_info[0]   
                        nickname=base_info[2]
                        wechatnumber=base_info[4]
                    else:#没有昵称选项，好友昵称就是备注,备注就是昵称
                        nickname=base_info[0]
                        remark=nickname
                        wechatnumber=base_info[2]
                return nickname,remark,wechatnumber
            except IndexError:
                return '非联系人'
        main_window=Tools.open_contacts(wechat_path=wechat_path,is_maximize=is_maximize)
        ContactsLists=main_window.child_window(**Main_window.ContactsList)
        #############################
        #先去通讯录列表最底部把最后一个好友的信息记录下来，通过键盘上的END健实现
        rec=ContactsLists.rectangle()
        mouse.click(coords=(rec.right-5,rec.top))
        pyautogui.press('End')
        last_member_info=get_info()
        while last_member_info=='非联系人':
            pyautogui.press('up')
            time.sleep(0.01)
            last_member_info=get_info()
        last_member_info={'wechatnumber':last_member_info[2]}
        pyautogui.press('Home')
        ######################################################################
        nicknames=[] 
        remarks=[]
        #初始化微信号列表为最后一个好友的微信号与任意字符,至于为什么要填充任意字符，自己想想
        wechatnumbers=[last_member_info['wechatnumber'],'nothing']
        #核心思路，一直比较存放所有好友微信号列表的首个元素和最后一个元素是否相同，
        #当记录到最后一个好友时,列表首位元素相同,此时结束while循环,while循环内是一直按下down健，记录右侧变换
        #的好友信息面板内的好友信息
        while wechatnumbers[-1]!=wechatnumbers[0]:
            pyautogui.keyDown('down',_pause=False)
            time.sleep(0.01)
            #这里将get_info内容提取出来重复是因为，这样会加快速度，若在while循环内部直接调用get_info函数，会导致速度变慢
            try: #通讯录界面右侧的好友信息面板  
                base_info=base_info_pane.descendants(control_type='Text')
                base_info=[element.window_text() for element in base_info]
                # #如果有昵称选项,说明好友有备注s
                if language=='简体中文':
                    if base_info[1]=='昵称：':
                        remark=base_info[0]
                        nickname=base_info[2]
                        wechatnumber=base_info[4]
                    else:#没有昵称选项，好友昵称就是备注,备注就是昵称
                        nickname=base_info[0]
                        remark=nickname
                        wechatnumber=base_info[2]
                    nicknames.append(nickname)
                    remarks.append(remark)
                    wechatnumbers.append(wechatnumber) 
                if language=='英文':
                    if base_info[1]=='Name: ':
                        remark=base_info[0]
                        nickname=base_info[2]
                        wechatnumber=base_info[4]
                    else:#没有昵称选项，好友昵称就是备注,备注就是昵称
                        nickname=base_info[0]
                        remark=nickname
                        wechatnumber=base_info[2]
                    nicknames.append(nickname)
                    remarks.append(remark)
                    wechatnumbers.append(wechatnumber)

                if language=='繁体中文':
                    if base_info[1]=='暱稱: ':
                        remark=base_info[0]
                        nickname=base_info[2]
                        wechatnumber=base_info[4]
                    else:#没有昵称选项，好友昵称就是备注,备注就是昵称
                        nickname=base_info[0]
                        remark=nickname
                        wechatnumber=base_info[2]
                    nicknames.append(nickname)
                    remarks.append(remark)
                    wechatnumbers.append(wechatnumber)      
            except IndexError:
                pass
        #删除一开始存放在起始位置的最后一个好友的微信号,不然重复了
        del(wechatnumbers[0])
        #第二个位置上是填充的任意字符,删掉上一个之后它变成了第一个,也删掉
        del(wechatnumbers[0])
        ##########################################
        #转为json格式
        records=zip(nicknames,remarks,wechatnumbers)
        contacts=[{'昵称':name[0],'备注':name[1],'微信号':name[2]} for name in records]
        contacts_json=json.dumps(contacts,ensure_ascii=False,separators=(',', ':'),indent=4)
        ##############################################################
        pyautogui.press('Home')
        if close_wechat:
            main_window.close()
        return contacts_json
    
    @staticmethod
    def get_friends_detail(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来获取通讯录中所有微信好友的详细信息(昵称,备注,地区，标签,个性签名,共同群聊,微信号,来源),注:不包含企业微信好友,速率约为1秒4-6个好友\n
        结果以json格式返回\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        #获取右侧变化的好友信息面板内的信息
        #从主窗口开始查找
        nickname='无'#昵称
        wechatnumber='无'#微信号
        region='无'#好友的地区
        tag='无'#好友标签
        common_group_num='无'
        remark='无'#备注
        signature='无'#个性签名
        source='无'#好友来源
        descrption='无'#描述
        phonenumber='无'#电话号
        permission='无'#朋友权限
        def get_info(): 
            nickname='无'#昵称
            wechatnumber='无'#微信号
            region='无'#好友的地区
            tag='无'#好友标签
            common_group_num='无'
            remark='无'#备注
            signature='无'#个性签名
            source='无'#好友来源
            descrption='无'#描述
            phonenumber='无'#电话号
            permission='无'#朋友权限
            global base_info_pane#设为全局变量，只需在第一次查找最后一个人时定位一次基本信息和详细信息面板即可
            global detail_info_pane
            try: #通讯录界面右侧的好友信息面板   
                try:
                    base_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                except IndexError:
                    base_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                base_info=base_info_pane.descendants(control_type='Text')
                base_info=[element.window_text() for element in base_info]
                # #如果有昵称选项,说明好友有备注
                if language=='简体中文':
                    if base_info[1]=='昵称：':
                        remark=base_info[0]
                        nickname=base_info[2]
                        wechatnumber=base_info[4]
                        if '地区：' in base_info:
                            region=base_info[base_info.index('地区：')+1]
                        else:
                            region='无'
                        
                    else:
                        nickname=base_info[0]
                        remark=nickname
                        wechatnumber=base_info[2]
                        if '地区：' in base_info:
                            region=base_info[base_info.index('地区：')+1]
                        else:
                            region='无'
                        
                    detail_info=[]
                    try:
                        detail_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                    except IndexError:
                        detail_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                    buttons=detail_info_pane.descendants(control_type='Button')
                    for pane in detail_info_pane.children(control_type='Pane',title='')[1:]:
                        detail_info.extend(pane.descendants(control_type='Text'))
                    detail_info=[element.window_text() for element in detail_info]
                    for button in buttons:
                        if '个' in button.window_text(): 
                            common_group_num=button.window_text()
                            break
                        else:
                            common_group_num='无'
                    if '个性签名' in detail_info:
                        signature=detail_info[detail_info.index('个性签名')+1]
                    if '标签' in detail_info:
                        tag=detail_info[detail_info.index('标签')+1]
                    if '来源' in detail_info:
                        source=detail_info[detail_info.index('来源')+1]
                    if '朋友权限' in detail_info:
                        permission=detail_info[detail_info.index('朋友权限')+1]
                    if '电话' in detail_info:
                        phonenumber=detail_info[detail_info.index('电话')+1]
                    if '描述' in detail_info:
                        descrption=detail_info[detail_info.index('描述')+1]
                    return nickname,remark,wechatnumber,region,tag,common_group_num,signature,source,permission,phonenumber,descrption
                
                if language=='英文':
                    if base_info[1]=='Name: ':
                            remark=base_info[0]
                            nickname=base_info[2]
                            wechatnumber=base_info[4]
                            if 'Region: ' in base_info:
                                region=base_info[base_info.index('Region: ')+1]
                            else:
                                region='无' 
                    else:
                        nickname=base_info[0]
                        remark=nickname
                        wechatnumber=base_info[2]
                        if 'Region: ' in base_info:
                            region=base_info[base_info.index('Region: ')+1]
                        else:
                            region='无'
                        
                    detail_info=[]
                    try:
                        detail_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                    except IndexError:
                        detail_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                    buttons=detail_info_pane.descendants(control_type='Button')
                    for pane in detail_info_pane.children(control_type='Pane',title='')[1:]:
                        detail_info.extend(pane.descendants(control_type='Text'))
                    detail_info=[element.window_text() for element in detail_info]
                    for button in buttons:
                        if re.match(r'\d+',button.window_text()):
                            common_group_num=button.window_text()
                            break
                        else:
                            common_group_num='无'
                    if "What's Up" in detail_info:
                        signature=detail_info[detail_info.index("What's Up")+1]
                    if 'Tag' in detail_info:
                        tag=detail_info[detail_info.index('Tag')+1]
                    if 'Source' in detail_info:
                        source=detail_info[detail_info.index('Source')+1]
                    if 'Privacy' in detail_info:
                        permission=detail_info[detail_info.index('Privacy')+1]
                    if 'Mobile' in detail_info:
                        phonenumber=detail_info[detail_info.index('Mobile')+1]
                    if 'Description' in detail_info:
                        descrption=detail_info[detail_info.index('Description')+1]
                    return nickname,remark,wechatnumber,region,tag,common_group_num,signature,source,permission,phonenumber,descrption
                
                if language=='繁体中文':
                    if base_info[1]=='暱稱：':
                        remark=base_info[0]
                        nickname=base_info[2]
                        wechatnumber=base_info[4]
                        if '地區：' in base_info:
                            region=base_info[base_info.index('地區：')+1]
                        else:
                            region='无'
                        
                    else:
                        nickname=base_info[0]
                        remark=nickname
                        wechatnumber=base_info[2]
                        if '地區：' in base_info:
                            region=base_info[base_info.index('地區：')+1]
                        else:
                            region='无'
                        
                    detail_info=[]
                    try:
                        detail_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                    except IndexError:
                        detail_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                    buttons=detail_info_pane.descendants(control_type='Button')
                    for pane in detail_info_pane.children(control_type='Pane',title='')[1:]:
                        detail_info.extend(pane.descendants(control_type='Text'))
                    detail_info=[element.window_text() for element in detail_info]
                    for button in buttons:
                        if '個' in button.window_text(): 
                            common_group_num=button.window_text()
                            break
                        else:
                            common_group_num='无'
                    if '個性簽名' in detail_info:
                        signature=detail_info[detail_info.index('個性簽名')+1]
                    if '標籤' in detail_info:
                        tag=detail_info[detail_info.index('標籤')+1]
                    if '來源' in detail_info:
                        source=detail_info[detail_info.index('來源')+1]
                    if '朋友權限' in detail_info:
                        permission=detail_info[detail_info.index('朋友權限')+1]
                    if '電話' in detail_info:
                        phonenumber=detail_info[detail_info.index('電話')+1]
                    if '描述' in detail_info:
                        descrption=detail_info[detail_info.index('描述')+1]
                    return nickname,remark,wechatnumber,region,tag,common_group_num,signature,source,permission,phonenumber,descrption
                
            except IndexError:
                    #注意:企业微信好友也会被判定为非联系人
                return '非联系人'
        main_window=Tools.open_contacts(wechat_path=wechat_path,is_maximize=is_maximize)
        ContactsLists=main_window.child_window(**Main_window.ContactsList)
        #####################################################################
        #先去通讯录列表最底部把最后一个好友的信息记录下来，通过键盘上的END健实现
        rec=ContactsLists.rectangle()
        mouse.click(coords=(rec.right-5,rec.top))
        pyautogui.press('End')
        last_member_info=get_info()
        while last_member_info=='非联系人':#必须确保通讯录底部界面下的最有一个好友是具有微信号的联系人，因此要向上查询
            pyautogui.press('up',_pause=False)
            last_member_info=get_info()
        last_member_info={'wechatnumber':last_member_info[2]}
        pyautogui.press('Home')
        ######################################################################
        #初始化微信号列表为最后一个好友的微信号与任意字符,至于为什么要填充任意字符，自己想想
        wechatnumbers=[last_member_info['wechatnumber'],'nothing']
        nicknames=[]
        remarks=[]
        tags=[]
        regions=[]
        common_group_nums=[]
        permissions=[]
        phonenumbers=[]
        descrptions=[]
        signatures=[]
        sources=[]
        #核心思路，一直比较存放所有好友微信号列表的首个元素和最后一个元素是否相同，
        #当记录到最后一个好友时,列表首末元素相同,此时结束while循环,while循环内是一直按下down健，记录右侧变换
        #的好友信息面板内的好友信息
        while wechatnumbers[-1]!=wechatnumbers[0]:
            pyautogui.keyDown('down',_pause=False)
            time.sleep(0.01)
            try: #通讯录界面右侧的好友信息面板   
                base_info=base_info_pane.descendants(control_type='Text')
                base_info=[element.window_text() for element in base_info]
                # #如果有昵称选项,说明好友有备注
                if language=='简体中文':
                    if base_info[1]=='昵称：':
                        remark=base_info[0]
                        nickname=base_info[2]
                        wechatnumber=base_info[4]
                        if '地区：' in base_info:
                            region=base_info[base_info.index('地区：')+1]
                        else:
                            region='无'
                    else:
                        nickname=base_info[0]
                        remark=nickname
                        wechatnumber=base_info[2]
                        if '地区：' in base_info:
                            region=base_info[base_info.index('地区：')+1]
                        else:
                            region='无'
                    detail_info=[]
                    buttons=detail_info_pane.descendants(control_type='Button')
                    for pane in detail_info_pane.children(control_type='Pane',title='')[1:]:
                        detail_info.extend(pane.descendants(control_type='Text'))
                    detail_info=[element.window_text() for element in detail_info]
                    for button in buttons:
                        if '个' in button.window_text(): 
                            common_group_num=button.window_text()
                            break
                        else:
                            common_group_num='无'
                    
                    if '个性签名' in detail_info:
                        signature=detail_info[detail_info.index('个性签名')+1]
                    else:
                        signature='无'
                    if '标签' in detail_info:
                        tag=detail_info[detail_info.index('标签')+1]
                    else:
                        tag='无'
                    if '来源' in detail_info:
                        source=detail_info[detail_info.index('来源')+1]
                    else:
                        source='无'
                    if '朋友权限' in detail_info:
                        permission=detail_info[detail_info.index('朋友权限')+1]
                    else:
                        permission='无'
                    if '电话' in detail_info:
                        phonenumber=detail_info[detail_info.index('电话')+1]
                    else:
                        phonenumber='无'
                    if '描述' in detail_info:
                        descrption=detail_info[detail_info.index('描述')+1]
                    else:
                        descrption='无'
                    nicknames.append(nickname)
                    remarks.append(remark)
                    wechatnumbers.append(wechatnumber)
                    regions.append(region)
                    tags.append(tag)
                    common_group_nums.append(common_group_num)
                    signatures.append(signature)
                    sources.append(source)
                    permissions.append(permission)
                    phonenumbers.append(phonenumber)
                    descrptions.append(descrption)

                if language=='英文':
                    if base_info[1]=='Name: ':
                        remark=base_info[0]
                        nickname=base_info[2]
                        wechatnumber=base_info[4]
                        if 'Region: ' in base_info:
                            region=base_info[base_info.index('Region: ')+1]
                        else:
                            region='无'
                    else:
                        nickname=base_info[0]
                        remark=nickname
                        wechatnumber=base_info[2]
                        if 'Region: ' in base_info:
                            region=base_info[base_info.index('Region: ')+1]
                        else:
                            region='无'
                    detail_info=[]
                    buttons=detail_info_pane.descendants(control_type='Button')
                    for pane in detail_info_pane.children(control_type='Pane',title='')[1:]:
                        detail_info.extend(pane.descendants(control_type='Text'))
                    detail_info=[element.window_text() for element in detail_info]
                    for button in buttons:
                        if re.match(r'\d+',button.window_text()):
                            common_group_num=button.window_text()
                            break
                        else:
                            common_group_num='无'
                    
                    if  "What's Up" in detail_info:
                        signature=detail_info[detail_info.index("What's Up")+1]
                    else:
                        signature='无'
                    if 'Tag' in detail_info:
                        tag=detail_info[detail_info.index('Tag')+1]
                    else:
                        tag='无'
                    if 'Source' in detail_info:
                        source=detail_info[detail_info.index('Source')+1]
                    else:
                        source='无'
                    if 'Privacy' in detail_info:
                        permission=detail_info[detail_info.index('Privacy')+1]
                    else:
                        permission='无'
                    if 'Mobile' in detail_info:
                        phonenumber=detail_info[detail_info.index('Mobile')+1]
                    else:
                        phonenumber='无'
                    if 'Description' in detail_info:
                        descrption=detail_info[detail_info.index('Description')+1]
                    else:
                        descrption='无'
                    nicknames.append(nickname)
                    remarks.append(remark)
                    wechatnumbers.append(wechatnumber)
                    regions.append(region)
                    tags.append(tag)
                    common_group_nums.append(common_group_num)
                    signatures.append(signature)
                    sources.append(source)
                    permissions.append(permission)
                    phonenumbers.append(phonenumber)
                    descrptions.append(descrption)
                
                if language=='繁体中文':
                    if base_info[1]=='暱稱：':
                        remark=base_info[0]
                        nickname=base_info[2]
                        wechatnumber=base_info[4]
                        if '地區：' in base_info:
                            region=base_info[base_info.index('地區：')+1]
                        else:
                            region='无'
                    else:
                        nickname=base_info[0]
                        remark=nickname
                        wechatnumber=base_info[2]
                        if '地區：' in base_info:
                            region=base_info[base_info.index('地區：')+1]
                        else:
                            region='无'
                    detail_info=[]
                    buttons=detail_info_pane.descendants(control_type='Button')
                    for pane in detail_info_pane.children(control_type='Pane',title='')[1:]:
                        detail_info.extend(pane.descendants(control_type='Text'))
                    detail_info=[element.window_text() for element in detail_info]
                    for button in buttons:
                        if '個' in button.window_text(): 
                            common_group_num=button.window_text()
                            break
                        else:
                            common_group_num='无'
                    
                    if '個性簽名' in detail_info:
                        signature=detail_info[detail_info.index('個性簽名')+1]
                    else:
                        signature='无'
                    if '標籤' in detail_info:
                        tag=detail_info[detail_info.index('標籤')+1]
                    else:
                        tag='无'
                    if '來源' in detail_info:
                        source=detail_info[detail_info.index('來源')+1]
                    else:
                        source='无'
                    if '朋友權限' in detail_info:
                        permission=detail_info[detail_info.index('朋友權限')+1]
                    else:
                        permission='无'
                    if '電話' in detail_info:
                        phonenumber=detail_info[detail_info.index('電話')+1]
                    else:
                        phonenumber='无'
                    if '描述' in detail_info:
                        descrption=detail_info[detail_info.index('描述')+1]
                    else:
                        descrption='无'
                    nicknames.append(nickname)
                    remarks.append(remark)
                    wechatnumbers.append(wechatnumber)
                    regions.append(region)
                    tags.append(tag)
                    common_group_nums.append(common_group_num)
                    signatures.append(signature)
                    sources.append(source)
                    permissions.append(permission)
                    phonenumbers.append(phonenumber)
                    descrptions.append(descrption)

            except IndexError:
                pass
        #删除一开始存放在起始位置的最后一个好友的微信号,不然重复了
        del(wechatnumbers[0])
        #第二个位置上是填充的任意字符,删掉上一个之后它变成了第一个,也删掉
        del(wechatnumbers[0])
        ##########################################
        #转为json格式
        records=zip(nicknames,wechatnumbers,regions,remarks,phonenumbers,tags,descrptions,permissions,common_group_nums,signatures,sources)
        contacts=[{'昵称':name[0],'微信号':name[1],'地区':name[2],'备注':name[3],'电话':name[4],'标签':name[5],'描述':name[6],'朋友权限':name[7],'共同群聊':name[8],'个性签名':name[9],'来源':name[10]} for name in records]
        contacts_json=json.dumps(contacts,ensure_ascii=False,separators=(',', ':'),indent=4)#ensure_ascii必须为False
        ##############################################################
        pyautogui.press('Home')#回到起始位置,方便下次打开
        if close_wechat:
            main_window.close()
        return contacts_json


    @staticmethod
    def get_wecom_friends_info(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来获取通讯录中所有未离职的企业微信好友的信息(昵称,企业名称)\n
        结果以json格式返回\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        def get_info():
            post='无'
            company='无'
            global base_info_pane
            global detail_info_pane
            try:
                try:
                    base_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                except IndexError:
                    base_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                try:
                    detail_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                except  IndexError:
                    detail_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                detail_info=detail_info_pane.descendants(control_type='Text')
                detail_info=[element.window_text() for element in detail_info]
                if language=='简体中文':
                    if '企业信息' in detail_info and '已离职' not in detail_info:
                        base_info=base_info_pane.descendants(control_type='Text')
                        base_info=[element.window_text() for element in base_info]
                        # #如果有昵称选项,说明好友有备注
                        if base_info[1]=='昵称：':
                            remark=base_info[0]
                            nickname=base_info[2]
                        else:
                            nickname=base_info[0]
                            remark=nickname
                        company=detail_info[detail_info.index('企业')+1]
                        if '职务' in detail_info:
                            post=detail_info[detail_info.index('职务')+1]
                        return nickname,company,remark,post
                    else:
                        return '非企业微信联系人'
                    
                if language=='英文':
                    if 'Enterprise Information' in detail_info and '已离职' not in detail_info:
                        base_info=base_info_pane.descendants(control_type='Text')
                        base_info=[element.window_text() for element in base_info]
                        # #如果有昵称选项,说明好友有备注
                        if base_info[1]=='Name: ':
                            remark=base_info[0]
                            nickname=base_info[2]
                        else:
                            nickname=base_info[0]
                            remark=nickname
                        company=detail_info[detail_info.index('Company')+1]
                        if 'Title' in detail_info:
                            post=detail_info[detail_info.index('Title')+1]
                        return nickname,company,remark,post
                    else:
                        return '非企业微信联系人'
                    
                if language=='繁体中文':
                    if '企業資訊' in detail_info and '已离职' not in detail_info:
                        base_info=base_info_pane.descendants(control_type='Text')
                        base_info=[element.window_text() for element in base_info]
                        # #如果有昵称选项,说明好友有备注
                        if base_info[1]=='暱稱：':
                            remark=base_info[0]
                            nickname=base_info[2]
                        else:
                            nickname=base_info[0]
                            remark=nickname
                        company=detail_info[detail_info.index('企業')+1]
                        if '職務' in detail_info:
                            post=detail_info[detail_info.index('職務')+1]
                        return nickname,company,remark,post
                    else:
                        return '非企业微信联系人'
            except IndexError:
                return '非企业微信联系人'

                
        main_window=Tools.open_contacts(wechat_path=wechat_path,is_maximize=is_maximize)
        contacts=main_window.child_window(**SideBar.Contacts)
        contacts.set_focus()
        contacts.click_input()
        contacts_list=main_window.child_window(**Main_window.ContactsList)
        rec=contacts_list.rectangle()  
        mouse.click(coords=(rec.right-5,rec.top+10))
        pyautogui.press('End')
        contacts_list=main_window.child_window(**Main_window.ContactsList)
        last_wecom_friend_info=get_info()
        while last_wecom_friend_info=='非企业微信联系人':
            pyautogui.keyDown('up')
            try:
                detail_info=detail_info_pane.descendants(control_type='Text')
                detail_info=[element.window_text() for element in detail_info]
                if language=='简体中文':
                    if '企业信息' in detail_info and '已离职' not in detail_info:
                        base_info=base_info_pane.descendants(control_type='Text')
                        base_info=[element.window_text() for element in base_info]
                        # #如果有昵称选项,说明好友有备注
                        if base_info[1]=='昵称：':
                            remark=base_info[0]
                            nickname=base_info[2] 
                        else:
                            nickname=base_info[0]
                            remark=nickname
                        company=detail_info[detail_info.index('企业')+1]
                        if '职务' in detail_info:
                            post=detail_info[detail_info.index('职务')+1] 
                        last_wecom_friend_info=company 

                if language=='英文':
                    if 'Enterprise Information' in detail_info and '已离职' not in detail_info:
                        base_info=base_info_pane.descendants(control_type='Text')
                        base_info=[element.window_text() for element in base_info]
                        # #如果有昵称选项,说明好友有备注
                        if base_info[1]=='Name: ':
                            remark=base_info[0]
                            nickname=base_info[2] 
                        else:
                            nickname=base_info[0]
                            remark=nickname
                        company=detail_info[detail_info.index('Company')+1]
                        if 'Title' in detail_info:
                            post=detail_info[detail_info.index('Title')+1] 
                        last_wecom_friend_info=company
                
                if language=='繁体中文':
                    if '企業資訊' in detail_info and '已离职' not in detail_info:
                        base_info=base_info_pane.descendants(control_type='Text')
                        base_info=[element.window_text() for element in base_info]
                        # #如果有昵称选项,说明好友有备注
                        if base_info[1]=='暱稱：':
                            remark=base_info[0]
                            nickname=base_info[2] 
                        else:
                            nickname=base_info[0]
                            remark=nickname
                        company=detail_info[detail_info.index('企業')+1]
                        if '職務' in detail_info:
                            post=detail_info[detail_info.index('職務')+1] 
                        last_wecom_friend_info=company 
            except IndexError:
                pass
        
        pyautogui.press('Home')
        companies=[last_wecom_friend_info,'nothing']
        nicknames=[]
        remarks=[]
        posts=[]
        while companies[-1]!=companies[0]:
            try:
                detail_info=detail_info_pane.descendants(control_type='Text')
                detail_info=[element.window_text() for element in detail_info]
                if language=='简体中文':
                    if '企业信息' in detail_info and '已离职' not in detail_info:
                        base_info=base_info_pane.descendants(control_type='Text')
                        base_info=[element.window_text() for element in base_info]
                        # #如果有昵称选项,说明好友有备注
                        if base_info[1]=='昵称：':
                            remark=base_info[0]
                            nickname=base_info[2]
                        else:
                            nickname=base_info[0]
                            remark=nickname
                        company=detail_info[detail_info.index('企业')+1]
                        if '职务' in detail_info:
                            post=detail_info[detail_info.index('职务')+1]
                            posts.append(post)
                        else:
                            posts.append('无')
                        nicknames.append(nickname)
                        remarks.append(remark)
                        companies.append(company)
                    else:
                        pass

                if language=='英文':
                    if 'Enterprise Information' in detail_info and '已离职' not in detail_info:
                        base_info=base_info_pane.descendants(control_type='Text')
                        base_info=[element.window_text() for element in base_info]
                        # #如果有昵称选项,说明好友有备注
                        if base_info[1]=='Name: ':
                            remark=base_info[0]
                            nickname=base_info[2]
                        else:
                            nickname=base_info[0]
                            remark=nickname
                        company=detail_info[detail_info.index('Company')+1]
                        if 'Title' in detail_info:
                            post=detail_info[detail_info.index('Title')+1]
                            posts.append(post)
                        else:
                            posts.append('无')
                        nicknames.append(nickname)
                        remarks.append(remark)
                        companies.append(company)
                    else:
                        pass
                
                if language=='繁体中文':
                    if '企業資訊' in detail_info and '已离职' not in detail_info:
                        base_info=base_info_pane.descendants(control_type='Text')
                        base_info=[element.window_text() for element in base_info]
                        # #如果有昵称选项,说明好友有备注
                        if base_info[1]=='暱稱：':
                            remark=base_info[0]
                            nickname=base_info[2]
                        else:
                            nickname=base_info[0]
                            remark=nickname
                        company=detail_info[detail_info.index('企業')+1]
                        if '職務' in detail_info:
                            post=detail_info[detail_info.index('職務')+1]
                            posts.append(post)
                        else:
                            posts.append('无')
                        nicknames.append(nickname)
                        remarks.append(remark)
                        companies.append(company)
                    else:
                        pass

            except IndexError:
                pass
            pyautogui.keyDown('down')  
        del(companies[0])
        del(companies[0])
        record=zip(nicknames,remarks,companies,posts)
        contacts=[{'昵称':friend[0],'备注':friend[1],'企业':friend[2],'职务':friend[3]}for friend in record]
        WeCom_json=json.dumps(contacts,ensure_ascii=False,indent=4)
        if close_wechat:
            main_window.close()
        return WeCom_json

    @staticmethod
    def get_groups_info(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来获取通讯录中所有群聊的信息(名称,成员数量)\n
        结果以json格式返回\n
        Args:
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        def remove_duplicate(List1,List2):
            #为了保证两个列表使用extend方法合二为一后没有重复项
            #利用集合的intersection运算找到两个列表的公共部分并将其在其中一个列表中去除掉
            ##a=[1,2,3,4],b=[3,4,5,6],最后返回值为a=[1,2,3,4],b=[5,6]
            common=set(List1).intersection(set(List2))
            List2=[element for element in List2 if element not in common]
            return List1,List2
        def get_info(group_chat_list):
            names=[chat.children()[0].children()[0].children(control_type="Button")[0].texts()[0] for chat in group_chat_list]
            numbers=[chat.children()[0].children()[0].children()[1].children()[0].children()[1].texts()[0] for chat in group_chat_list]
            numbers=[number.replace('(','').replace(')','') for number in numbers]
            return names,numbers
        contacts_settings_window=Tools.open_contacts_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)[0]
        recent_group_chat=contacts_settings_window.child_window(**Buttons.RectentGroupButton)
        try:
            group_chat_list_item=contacts_settings_window.child_window(control_type="List",found_index=0,title="").children(control_type="ListItem",title="")      
            first_group=group_chat_list_item[0].children()[0].children()[0].children(control_type="Button")[0]
            first_group.click_input()
        except IndexError:
            recent_group_chat.set_focus()
            recent_group_chat.click_input()
            group_chat_list_item=contacts_settings_window.child_window(control_type="List",found_index=0,title="").children(control_type="ListItem",title="")      
            first_group=group_chat_list_item[0].children()[0].children()[0].children(control_type="Button")[0]
            first_group.click_input()
        pyautogui.press('End')
        group_chat_list_item=contacts_settings_window.child_window(control_type="List",found_index=0,title="").children(control_type="ListItem",title="")
        last_group_name=get_info(group_chat_list_item)[0][-1]
        pyautogui.press('Home')
        temp=[last_group_name,'nothing']#记录最后一个群的群聊名称，和get_friends_info一样的思路
        groups_members=[]
        groups_names=[]
        record1=[]
        record2=[]
        while temp[-1]!=temp[0]:#比较temp中记录的群聊名称有没有和temp首个元素相同，若相同说明已经到达底部，结束循环
            group_chat_list_item=contacts_settings_window.child_window(control_type="List",found_index=0,title="").children(control_type="ListItem",title="")      
            names,numbers=get_info(group_chat_list_item)
            temp.append(names[-1])
            record1.append(names)
            record2.append(numbers)
            pyautogui.press("pagedown",_pause=False)
        contacts_settings_window.close()
        temp.clear()
        record1[-1],record1[-2]=remove_duplicate(record1[-1],record1[-2])
        record2[-1],record2[-2]=remove_duplicate(record2[-1],record2[-2])
        for names in record1:
            groups_names.extend(names)
        for numbers in record2:
            groups_members.extend(numbers)
        record=zip(groups_names,groups_members)
        groups_info=[{"群聊名称":group[0],"群聊人数":group[1]}for group in record]
        groups_info_json=json.dumps(groups_info,indent=4,ensure_ascii=False)
        return groups_info_json

    @staticmethod
    def get_groupmembers_info(group_name:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来获取某个群聊中所有群成员的群昵称(名称,成员数量)\n
        结果以列表的json格式返回\n
        Args:
            group_name\t:群聊名称或备注\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为5,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        def find_group_in_contacts_list(group_name):
            contacts_list=main_window.child_window(**Main_window.ContactsList)
            rec=contacts_list.rectangle()  
            mouse.click(coords=(rec.right-5,rec.top+10))
            listitems=contacts_list.children(control_type='ListItem')
            names=[item.window_text() for item in listitems]
            while group_name not in names:
                contacts_list=main_window.child_window(**Main_window.ContactsList)
                listitems=contacts_list.children(control_type='ListItem')
                names=[item.window_text() for item in listitems]
                pyautogui.press('down',_pause=False)
            group=listitems[names.index(group_name)]
            group_button=group.descendants(control_type='Button',title=group_name)[0]
            rec=group_button.rectangle()
            mouse.click(coords=(int(rec.left+rec.right)//2,rec.top-12))
        def get_info():
            groupmember_names=[]
            detail_info_pane=main_window.child_window(title_re=r'.*\(\d+\).*',control_type='Text').parent().parent().children()[1]
            detail_info=detail_info_pane.descendants(control_type='ListItem')
            groupmember_names=[element.window_text() for element in detail_info]
            return groupmember_names
        GroupSettings.save_group_to_contacts(group_name=group_name,state='open',wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=False,search_pages=search_pages)
        main_window=Tools.open_contacts(wechat_path=wechat_path,is_maximize=is_maximize)
        find_group_in_contacts_list(group_name=group_name)
        groupmember_names=get_info()
        GroupSettings.save_group_to_contacts(group_name=group_name,state='close',wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=False)
        if close_wechat:
            main_window.close()
        groupmember_json={'群聊':group_name,'人数':len(groupmember_names),'群成员群昵称':groupmember_names}
        groupmember_json=json.dumps(groupmember_json,ensure_ascii=False,indent=4)
        return groupmember_json
    
    
class AutoReply():

    @staticmethod
    def auto_answer_call(duration:str,broadcast_content:str,message:str=None,times:int=2,wechat_path:str=None,close_wechat:bool=True):
        '''
        该方法用来自动接听微信电话\n
        注意！一旦开启自动接听功能后,在设定时间内,你的所有视频语音电话都将优先被PC微信接听,并按照设定的播报与留言内容进行播报和留言。\n
        Args:
            duration:\t自动接听功能持续时长,格式:s,min,h分别对应秒,分钟,小时,例:duration='1.5h'持续1.5小时\n
            broadcast_content:\twindowsAPI语音播报内容\n
            message:\t语音播报结束挂断后,给呼叫者发送的留言\n
            times:\t语音播报重复次数\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        def judge_call(call_interface):
            window_text=call_interface.child_window(found_index=1,control_type='Button').texts()[0]
            if '视频通话' in window_text:
                index=window_text.index("邀")
                caller_name=window_text[0:index]
                return '视频通话',caller_name
            else:
                index=window_text.index("邀")
                caller_name=window_text[0:index]
                return "语音通话",caller_name
        caller_names=[]
        flags=[]
        unchanged_duration=duration
        duration=match_duration(duration)
        if not duration:
            raise TimeNotCorrectError
        Systemsettings.open_listening_mode(volume=True)
        start_time=time.time()
        desktop=Desktop(**Independent_window.Desktop)
        while True:
            if time.time()-start_time<duration:
                call_interface1=desktop.window(**Independent_window.OldIncomingCallWindow)
                call_interface2=desktop.window(**Independent_window.NewIncomingCallWindow)
                if call_interface1.exists():
                    flag,caller_name=judge_call(call_interface1)
                    caller_names.append(caller_name)
                    flags.append(flag)
                    call_window=call_interface1.child_window(found_index=3,title="",control_type='Pane')
                    accept=call_window.children(**Buttons.AcceptButton)[0]
                    if flag=="语音通话":
                        time.sleep(1)
                        accept.click_input()
                        time.sleep(1)
                        accept_call_window=desktop.window(**Independent_window.OldVoiceCallWindow)
                        if accept_call_window.exists():
                            duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                            while not duration_time.exists():
                                time.sleep(1)
                                duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                            Systemsettings.speaker(times=times,text=broadcast_content)
                            answering_window=accept_call_window.child_window(found_index=13,control_type='Pane',title='')
                            if answering_window.exists():
                                reject=answering_window.child_window(**Buttons.HangUpButton)
                                reject.click_input()
                                if message:
                                    Messages.send_message_to_friend(wechat_path=wechat_path,friend=caller_name,close_wechat=close_wechat,message=message)     
                    else:
                        time.sleep(1)
                        accept.click_input()
                        time.sleep(1)
                        accept_call_window=desktop.window(**Independent_window.OldVideoCallWindow)
                        accept_call_window.click_input()
                        duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                        while not duration_time.exists():
                                time.sleep(1)
                                accept_call_window.click_input()
                                duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                        Systemsettings.speaker(times=times,text=broadcast_content)
                        rec=accept_call_window.rectangle()
                        mouse.move(coords=(rec.left//2+rec.right//2,rec.bottom-50))
                        reject=accept_call_window.child_window(**Buttons.HangUpButton)
                        reject.click_input()
                        if message:
                            Messages.send_message_to_friend(wechat_path=wechat_path,friend=caller_name,message=message,close_wechat=close_wechat)
                        
                elif call_interface2.exists():
                    call_window=call_interface2.child_window(found_index=4,title="",control_type='Pane')
                    accept=call_window.children(**Buttons.AcceptButton)[0]
                    flag,caller_name=judge_call(call_interface2)
                    caller_names.append(caller_name)
                    flags.append(flag)
                    if flag=="语音通话":
                        time.sleep(1)
                        accept.click_input()
                        time.sleep(1)
                        accept_call_window=desktop.window(**Independent_window.NewVoiceCallWindow)
                        if accept_call_window.exists():
                            answering_window=accept_call_window.child_window(found_index=13,control_type='Pane',title='')
                            duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                            while not duration_time.exists():
                                time.sleep(1)
                                duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                            Systemsettings.speaker(times=times,text=broadcast_content)
                            if answering_window.exists():
                                reject=answering_window.children(**Buttons.HangUpButton)[0]
                                reject.click_input()
                                if message:
                                    Messages.send_message_to_friend(wechat_path=wechat_path,friend=caller_name,message=message,close_wechat=close_wechat)
                    else:
                        time.sleep(1)
                        accept.click_input()
                        time.sleep(1)
                        accept_call_window=desktop.window(**Independent_window.NewVideoCallWindow)
                        accept_call_window.click_input()
                        duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                        while not duration_time.exists():
                                time.sleep(1)
                                accept_call_window.click_input()
                                duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                        Systemsettings.speaker(times=times,text=broadcast_content)
                        rec=accept_call_window.rectangle()
                        mouse.move(coords=(rec.left//2+rec.right//2,rec.bottom-50))
                        reject=accept_call_window.child_window(**Buttons.HangUpButton)
                        reject.click_input()
                        if message:
                            Messages.send_message_to_friend(wechat_path=wechat_path,friend=caller_name,message=message,close_wechat=close_wechat)
                        
                else:
                    call_interface1=call_interface2=None
            else:
                break
        Systemsettings.close_listening_mode()
        if caller_names:
            print(f'自动接听微信电话结束,在{unchanged_duration}内内共计接听{len(caller_names)}个电话\n接听对象:{caller_names}\n电话类型{flags}')
        else:
            print(f'未接听到任何微信视频或语音电话')

    @staticmethod
    def auto_reply_messages(content:str,duration:str,dontReplyGroup:bool=False,max_pages:int=5,never_reply:list=[],scroll_delay:int=0,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该函数用来遍历会话列表查找新消息自动回复,最大回复数量=max_pages*(8~10)\n
        如果你不想回复某些好友,你可以临时将其设为消息免打扰,或传入\n
        一个包含不回复好友或群聊的昵称列表never_reply\n
        Args:
            content:\t自动回复内容\n
            duration:\t自动回复持续时长,格式:'s','min','h'单位:s/秒,min/分,h/小时\n
            dontReplyGroup:\t不回复群聊(即使有新消息也不回复)\n
            max_pages:\t遍历会话列表页数,一页为8~10人,设定持续时间后,将持续在max_pages内循环遍历查找是否有新消息\n
            never_reply:\t在never_reply列表中的好友即使有新消息时也不会回复\n
            scroll_delay:\t滚动遍历max_pages页会话列表后暂停秒数,如果你的max_pages很大,且持续时间长,scroll_delay还为0的话,那么一直滚动遍历有可能被微信检测到自动退出登录\n
                该参数只在会话列表可以滚动的情况下生效\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        if language=='简体中文':
            taboo_list=['微信团队','微信支付','微信运动','订阅号','腾讯新闻','服务通知']
        if language=='繁体中文':
            taboo_list=['微信团队','微信支付','微信运动','訂閱賬號','騰訊新聞','服務通知']
        if language=='英文':
            taboo_list=['微信团队','微信支付','微信运动','Subscriptions','Tencent News','Service Notifications']
        taboo_list.extend(never_reply)
        responsed_friend=set()
        responsed_groups=set()
        unchanged_duration=duration
        duration=match_duration(duration)
        if not duration:
            raise TimeNotCorrectError
        Systemsettings.open_listening_mode(volume=False)
        Systemsettings.copy_text_to_windowsclipboard(content)
        def record():
            #遍历当前会话列表内的所有成员，获取他们的名称和新消息条数，没有新消息的话返回[],[]
            #newMessagefriends为会话列表(List)中所有含有新消息的ListItem
            newMessagefriends=[friend for friend in messageList.children() if '条新消息' in friend.window_text()]
            if newMessagefriends:
                #newMessageTips为newMessagefriends中每个元素的文本:['测试365 5条新消息','一家人已置顶20条新消息']这样的字符串列表
                newMessageTips=[friend.window_text() for friend in newMessagefriends]
                #会话列表中的好友具有Text属性，Text内容为备注名，通过这个按钮的名称获取好友名字
                names=[friend.descendants(control_type='Text')[0].window_text() for friend in newMessagefriends]
                return names
            return []

        #监听并且回复右侧聊天界面
        def listen_on_current_chat():
            voice_call_button=main_window.child_window(**Buttons.VoiceCallButton)
            video_call_button=main_window.child_window(**Buttons.VideoCallButton)
            current_chat=main_window.child_window(**Main_window.CurrentChatWindow)
            #判断好友类型
            if video_call_button.exists() and voice_call_button.exists():#好友
                type='好友'
            if not video_call_button.exists() and voice_call_button.exists():#好友
                type='群聊'
            if not video_call_button.exists() and not voice_call_button.exists():#好友
                type='非好友'
            #自动回复逻辑
            if type=='好友' and current_chat.window_text() not in taboo_list:
                latest_message,who=Tools.pull_latest_message(chatlist)#最新的消息
                if who==current_chat.window_text() and latest_message!=initial_last_message:#不等于刚打开页面时的那条消息且发送者是对方
                    current_chat.click_input()
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    pyautogui.hotkey('alt','s',_pause=False)
                    responsed_friend.add(current_chat.window_text())
                    if scorllable:
                        mouse.click(coords=(x+2,y-6))#点击右上方激活滑块
            if type=='群聊' and current_chat.window_text() not in taboo_list:
                latest_message,who=Tools.pull_latest_message(chatlist)#最新的消息
                if latest_message!=initial_last_message and who!=myname:
                    if not dontReplyGroup:
                        current_chat.click_input()
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        pyautogui.hotkey('alt','s',_pause=False)
                        responsed_friend.add(current_chat.window_text())
                        responsed_groups.add(current_chat.window_text())
                        if scorllable:
                            mouse.click(coords=(x+2,y-6))#点击右上方激活滑块

        #用来回复在会话列表中找到的头顶有红色数字新消息提示的好友
        def reply(names):
            names=[name for name in names if name not in taboo_list]#tabool_list是传入的never_reply和我这里定义的的一些不回复对象,比如'微信运动','微信支付'灯
            if names:
                for name in names:       
                    Tools.find_friend_in_MessageList(friend=name,search_pages=search_pages,is_maximize=is_maximize)
                    voice_call_button=main_window.child_window(**Buttons.VoiceCallButton)
                    video_call_button=main_window.child_window(**Buttons.VideoCallButton)
                    #判断好友类型
                    if video_call_button.exists() and voice_call_button.exists():#好友
                        type='好友'
                    if not video_call_button.exists() and voice_call_button.exists():#好友
                        type='群聊'
                    if not video_call_button.exists() and not voice_call_button.exists():#好友
                        type='非好友'
                    if type=='好友':#有语音聊天按钮不是公众号,不用关注
                        current_chat=main_window.child_window(**Main_window.CurrentChatWindow)
                        current_chat.click_input()
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        pyautogui.hotkey('alt','s',_pause=False)
                        responsed_friend.add(name) 
                    if type=='群聊' and not dontReplyGroup:
                            current_chat=main_window.child_window(**Main_window.CurrentChatWindow)
                            current_chat.click_input()
                            pyautogui.hotkey('ctrl','v',_pause=False)
                            pyautogui.hotkey('alt','s',_pause=False)
                            responsed_friend.add(name)
                            responsed_groups.add(name)
                if scorllable:
                    mouse.click(coords=(x,y))#回复完成后点击右上方,激活滑块，继续遍历会话列表

        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        chat_button=main_window.child_window(**SideBar.Chats)
        chat_button.click_input()
        myname=main_window.child_window(control_type='Button',found_index=0).window_text()
        chatlist=main_window.child_window(**Main_window.FriendChatList)#聊天界面内存储所有聊天信息的消息列表
        initial_last_message=Tools.pull_latest_message(chatlist)[0]#刚打开聊天界面时的最后一条消息的listitem 
        messageList=main_window.child_window(**Main_window.ConversationList)#左侧的会话列表
        scorllable=Tools.is_VerticalScrollable(messageList)#只调用一次is_VerticallyScrollable函数来判断会话列表是否可以滚动
        x,y=messageList.rectangle().right-5,messageList.rectangle().top+8#右上方滑块的位置
        if scorllable:
            mouse.click(coords=(x,y))#点击右上方激活滑块
            pyautogui.press('Home')#按下Home健确保从顶部开始
        search_pages=1
        start_time=time.time()
        chatsButton=main_window.child_window(**SideBar.Chats)
        while time.time()-start_time<=duration:
            if chatsButton.legacy_properties().get('Value'):#如果左侧的聊天按钮式红色的就遍历,否则原地等待
                if scorllable:
                    for _ in range(max_pages+1):
                        names=record()
                        reply(names)
                        names.clear()
                        pyautogui.press('pagedown',_pause=False)
                        search_pages+=1
                    pyautogui.press('Home')
                    time.sleep(scroll_delay)
                else:
                    names=record()
                    reply(names)
                    names.clear()
            listen_on_current_chat()
        Systemsettings.close_listening_mode()
        if responsed_friend:
            print(f"在{unchanged_duration}内回复了以下好友\n{responsed_friend}")
            if responsed_groups:
                print(f"回复的群聊有\n{responsed_groups}")
        if close_wechat:
            main_window.close()

    @staticmethod
    def auto_reply_to_friend(friend:str,duration:str,content:str,save_chat_history:bool=False,capture_screen:bool=False,folder_path:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来实现类似QQ的自动回复某个好友的消息\n
        Args:
            friend:\t好友或群聊备注\n
            duration:\t自动回复持续时长,格式:'s','min','h',单位:s/秒,min/分,h/小时\n
            content:\t指定的回复内容,比如:自动回复[微信机器人]:您好,我当前不在,请您稍后再试。\n
            save_chat_history:\t是否保存自动回复时留下的聊天记录,若值为True该函数返回值为聊天记录json,否则该函数无返回值。\n
            capture_screen:\t是否保存聊天记录截图,默认值为False不保存。\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为5,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
            folder_path:\t存放聊天记录截屏图片的文件夹路径\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        if save_chat_history and capture_screen and folder_path:#需要保存自动回复后的聊天记录截图时，可以传入一个自定义文件夹路径，不然保存在运行该函数的代码所在文件夹下
            #当给定的文件夹路径下的内容不是一个文件夹时
            if not Systemsettings.is_dirctory(folder_path):#
                raise NotFolderError(r'给定路径不是文件夹!无法保存聊天记录截图,请重新选择文件夹！')
        duration=match_duration(duration)#将's','min','h'转换为秒
        if not duration:#有SB不按照指定的时间格式输入,需要提前中断退出
            raise TimeNotCorrectError
        #打开好友的对话框,返回值为编辑消息框和主界面
        chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        #需要判断一下是不是公众号
        voice_call_button=main_window.child_window(**Buttons.VoiceCallButton)
        video_call_button=main_window.child_window(**Buttons.VideoCallButton)
        if not voice_call_button.exists():
            #公众号没有语音聊天按钮
            main_window.close()
            raise CantReplyToOfficialAccountError
        if video_call_button.exists() and voice_call_button.exists():
            type='好友'
        if not video_call_button.exists() and voice_call_button.exists():
            type='群聊'
            myname=main_window.child_window(control_type='Button',found_index=0).window_text()#自己的名字
        #####################################################################################
        chatList=main_window.child_window(**Main_window.FriendChatList)#聊天界面内存储所有信息的容器
        initial_last_message=Tools.pull_latest_message(chatList)[0]#刚打开聊天界面时的最后一条消息的listitem   
        Systemsettings.copy_text_to_windowsclipboard(content)#复制回复内容到剪贴板
        Systemsettings.open_listening_mode(volume=False)#开启监听模式,此时电脑只要不断电不会息屏 
        count=0
        start_time=time.time()  
        while True:
            if time.time()-start_time<duration:
                newMessage,who=Tools.pull_latest_message(chatList)
                #消息列表内的最后一条消息(listitem)不等于刚打开聊天界面时的最后一条消息(listitem)
                #并且最后一条消息的发送者是好友时自动回复
                #这里我们判断的是两条消息(listitem)是否相等,不是文本是否相等,要是文本相等的话,对方一直重复发送
                #刚打开聊天界面时的最后一条消息的话那就一直不回复了
                if type=='好友':
                    if newMessage!=initial_last_message and who==friend:
                        chat.click_input()
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        pyautogui.hotkey('alt','s',_pause=False)
                        count+=1  
                if type=='群聊':
                    if newMessage!=initial_last_message and who!=myname:
                        chat.click_input()
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        pyautogui.hotkey('alt','s',_pause=False)
                        count+=1
            else:
                break
        if count:
            if save_chat_history:
                chat_history=get_chat_history(friend=friend,number=2*count,capture_screen=capture_screen,folder_path=folder_path,wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)  
                return chat_history
        Systemsettings.close_listening_mode()
        if close_wechat:
            main_window.close()

    @staticmethod
    def AI_auto_reply_to_friend(friend:str,duration:str,AI_engine,save_chat_history:bool=False,capture_screen:bool=False,folder_path:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        该方法用来接入AI大模型自动回复好友消息\n
        Args:
            friend:\t好友或群聊备注\n
            duration:\t自动回复持续时长,格式:'s','min','h'单位:s/秒,min/分,h/小时\n
            Ai_engine:\t调用的AI大模型API函数,去各个大模型官网找就可以\n
            search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏法搜索好友信息打开聊天界面\n
            wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
                尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
                传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
            is_maximize:\t微信界面是否全屏,默认全屏。\n
            close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        '''
        if save_chat_history and capture_screen and folder_path:#需要保存自动回复后的聊天记录截图时，可以传入一个自定义文件夹路径，不然保存在运行该函数的代码所在文件夹下
            #当给定的文件夹路径下的内容不是一个文件夹时
            if not Systemsettings.is_dirctory(folder_path):#
                raise NotFolderError(r'给定路径不是文件夹!无法保存聊天记录截图,请重新选择文件夹！')
        def get_latest_chat_history():#获取聊天界面内的聊天记录
            #筛选消息，每条消息都是一个listitem
            if chatlist.children():
                ###################
                chats=[message for message in chatlist.children(control_type='ListItem') if not re.findall(r'\d\d:\d\d',message.window_text())]
                chats=[item for item in chats if item.window_text()!='查看更多消息']
                chats=[item for item in chats if '撤回了一条消息' not in item.window_text()]
                chats=[item for item in chats if '以下是新消息' not in item.window_text()]
                chats=[item for item in chats if item.children()[0].children()!=[]]
                ##################
                if chats:#如果有聊天记录
                    who=chats[-1].descendants(control_type='Button')[0].window_text()
                    return chats,who#返回的chats不是文本,是listitem
            return [None],None#此时的聊天界面是一片空白,可能是刚刚清空过聊天记录
        duration=match_duration(duration)#将's','min','h'转换为秒
        if not duration:#有SB不按照指定的时间格式输入,需要提前中断退出
            raise TimeNotCorrectError
        #打开好友的对话框,返回值为编辑消息框和主界面
        chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
        #有SB想自动回复微信支付这样的公众号,需要判断一下是不是公众号
        voice_call_button=main_window.child_window(**Buttons.VoiceCallButton)
        video_call_button=main_window.child_window(**Buttons.VideoCallButton)
        if not voice_call_button.exists():
            #公众号没有语音聊天按钮
            main_window.close()
            raise CantReplyToOfficialAccountError
        if video_call_button.exists() and voice_call_button.exists():
            type='好友'
        if not video_call_button.exists() and voice_call_button.exists():
            type='群聊'
            myname=main_window.child_window(control_type='Button',found_index=0).window_text()#自己的名字
        #####################################################################################
        chatlist=main_window.child_window(**Main_window.FriendChatList)#聊天界面内存储所有信息的容器
        initial_last_message=get_latest_chat_history()[0][-1]#刚打开聊天界面时的最后一条消息的listitem   
        Systemsettings.open_listening_mode(volume=False)#开启监听模式,此时电脑只要不断电不会息屏 
        count=0
        start_time=time.time()  
        while True:
            if time.time()-start_time<duration:
                chats,who=get_latest_chat_history()
                #消息列表内的最后一条消息(listitem)不等于刚打开聊天界面时的最后一条消息(listitem)
                #并且最后一条消息的发送者是好友时自动回复
                #这里我们判断的是两条消息(listitem)是否相等,不是文本是否相等,要是文本相等的话,对方一直重复发送
                #刚打开聊天界面时的最后一条消息的话那就一直不回复了
                if type=='好友':
                    if chats[-1]!=initial_last_message and who==friend:
                        chat.click_input()
                        Systemsettings.copy_text_to_windowsclipboard(AI_engine(chats[-1].window_text()))#复制回复内容到剪贴板
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        pyautogui.hotkey('alt','s',_pause=False)
                        count+=1  
                if type=='群聊':
                    if chats[-1]!=initial_last_message and who!=myname:
                        chat.click_input()
                        Systemsettings.copy_text_to_windowsclipboard(AI_engine(chats[-1].window_text()))#复制回复内容到剪贴板
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        pyautogui.hotkey('alt','s',_pause=False)
                        count+=1
            else:
                break
        if count:
            if save_chat_history:
                chat_history=get_chat_history(friend=friend,number=int(1.5*count),capture_screen=capture_screen,folder_path=folder_path,wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)  
                return chat_history
        Systemsettings.close_listening_mode()
        if close_wechat:
            main_window.close()

def send_message_to_friend(friend:str,message:str,delay:float=1,tickle:bool=False,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于给单个好友或群聊发送单条信息\n
    Args:
        friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
        message:\t待发送消息。格式:message="消息"\n
        tickle:\t是否在发送消息或文件后拍一拍好友,默认为False\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        delay:\t发送单条消息延迟,单位:秒/s,默认1s。\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    if len(message)==0:
        raise CantSendEmptyMessageError
    #先使用open_dialog_window打开对话框
    chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    if is_maximize:
        main_window.maximize()
    chat.click_input()
    #字数超过2000字直接发txt
    if len(message)<2000:
        Systemsettings.copy_text_to_windowsclipboard(message)
        pyautogui.hotkey('ctrl','v',_pause=False)
        time.sleep(delay)
        pyautogui.hotkey('alt','s',_pause=False)
    elif len(message)>2000:
        Systemsettings.convert_long_text_to_txt(message)
        pyautogui.hotkey('ctrl','v',_pause=False)
        time.sleep(delay)
        pyautogui.hotkey('alt','s',_pause=False)
        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)    
    if tickle:
        tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
    time.sleep(1)
    if close_wechat:
        main_window.close()

def send_messages_to_friend(friend:str,messages:list[str],tickle:bool=False,delay:float=1,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于给单个好友或群聊发送多条信息\n
    Args:
        friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
        message:\t待发送消息列表。格式:message=["发给好友的消息1","发给好友的消息2"]\n
        tickle:\t是否在发送消息或文件后拍一拍好友,默认为False\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        delay\t:发送单条消息延迟,单位:秒/s,默认1s。\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    
    '''
    if not messages:
        raise CantSendEmptyMessageError
    #先使用open_dialog_window打开对话框
    chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    chat.click_input()
    #字数在100字以内打字发送,超过100字复制粘贴发送,#字数在100字以内打字发送,超过50字复制粘贴发送,#字数在50字以内打字发送,超过50字复制粘贴发送,超过2000字直接发word
    for message in messages:
        if len(message)==0:
            main_window.close()
            raise CantSendEmptyMessageError
        if len(message)<2000:
            Systemsettings.copy_text_to_windowsclipboard(message)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        elif len(message)>2000:
            Systemsettings.convert_long_text_to_txt(message)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
    if tickle:
        tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
    time.sleep(1)
    if close_wechat:
        main_window.close()

def send_message_to_friends(friends:list[str],message:list[str],tickle:list[bool]=[],delay:float=1,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于给每friends中的一个好友或群聊发送message中对应的单条信息\n
    Args:
        friends:\t好友或群聊备注。格式:friends=["好友1","好友2","好友3"]\n
        message:\t待发送消息,格式: message=[发给好友1的多条消息,发给好友2的多条消息,发给好友3的多条消息]。\n
        tickle:\t是否给每一个好友发送消息或文件后拍一拍好友,格式为:[True,True,False,...]的bool值列表,与friends列表中的每一个好友对应\n
        delay:\t发送单条消息延迟,单位:秒/s,默认1s。\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    注意!message与friends长度需一致,并且messages内每一条消息顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
    '''
    #多个好友的发送任务不需要使用open_dialog_window方法了直接在顶部搜索栏搜索,一个一个打开好友的聊天界面，发送消息,这样最高效
    Chats=dict(zip(friends,message))
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    time.sleep(1)
    i=0
    for friend in Chats:
        search=main_window.child_window(**Main_window.Search)
        search.click_input()
        Systemsettings.copy_text_to_windowsclipboard(friend)
        pyautogui.hotkey('ctrl','v',_pause=False)
        time.sleep(1)
        pyautogui.press('enter')
        chat=main_window.child_window(title=friend,control_type='Edit')
        chat.click_input()
        #字数在50字以内打字发送,超过50字复制粘贴发送,超过2000字直接发word
        if len(Chats.get(friend))==0:
            main_window.close()
            raise CantSendEmptyMessageError
        if len(Chats.get(friend))<2000:
            Systemsettings.copy_text_to_windowsclipboard(Chats.get(friend))
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        elif len(Chats.get(friend))>2000:
            Systemsettings.convert_long_text_to_docx(Chats.get(friend))
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
            warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
        if tickle:
            if tickle[i]:
                tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
            i+=1
    time.sleep(1)
    if close_wechat:
        main_window.close()

    
def send_messages_to_friends(friends:list[str],messages:list[list[str]],tickle:list[bool]=[],delay:float=1,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于给多个好友或群聊发送多条信息\n
    Args:
        friends:\t好友或群聊备注列表,格式:firends=["好友1","好友2","好友3"]。\n
        messages:\t待发送消息,格式: message=[[发给好友1的多条消息],[发给好友2的多条消息],[发给好友3的多条信息]]。\n
        tickle:\t是否给每一个好友发送消息或文件后拍一拍好友,格式为:[True,True,False,...]的bool值列表,与friends列表中的每一个好友对应\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        delay:\t发送单条消息延迟,单位:秒/s,默认1s。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    注意!messages与friends长度需一致,并且messages内每一个列表顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
    '''
    #多个好友的发送任务不需要使用open_dialog_window方法了直接在顶部搜索栏搜索,一个一个打开好友的聊天界面，发送消息,这样最高效
    Chats=dict(zip(friends,messages))
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    i=0
    for friend in Chats:
        search=main_window.child_window(**Main_window.Search)
        search.click_input()
        Systemsettings.copy_text_to_windowsclipboard(friend)
        pyautogui.hotkey('ctrl','v',_pause=False)
        time.sleep(1)
        pyautogui.press('enter')
        chat=main_window.child_window(title=friend,control_type='Edit')
        chat.click_input()
        #字数在50字以内打字发送,超过50字复制粘贴发送,超过2000字直接发word
        for message in Chats.get(friend):
            if len(message)==0:
                main_window.close()
                raise CantSendEmptyMessageError
            if len(message)<2000:
                Systemsettings.copy_text_to_windowsclipboard(message)
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
            elif len(message)>2000:
                Systemsettings.convert_long_text_to_txt(message)
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
                warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
        if tickle:
            if tickle[i]:
                tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
            i+=1
    time.sleep(1)
    if close_wechat:
        main_window.close()

def forward_message(friends:list[str],message:str,delay:float=0.8,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于给好友转发消息,实际使用时建议先给文件传输助手转发\n
    这样可以避免对方聊天信息更新过快导致转发消息被'淹没',进而无法定位出错的问题。\n
    Args:
        friends:\t好友或群聊备注列表。格式:friends=["好友1","好友2","好友3"]\n
        message:\t待发送消息,格式: message="转发消息"。\n
        delay:\t搜索好友等待时间\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        search_pages:\t在会话列表中查询查找带转发消息的第一个好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    def right_click_message():
        max_retry_times=25
        retry_interval=0.2
        counter=0
        #查找最新的我自己发的消息，并右键单击我发送的消息，点击转发按钮
        chatList=main_window.child_window(**Main_window.FriendChatList)
        myname=main_window.child_window(**Buttons.MySelfButton).window_text()
        #if message.descendants(conrol_type)是用来筛选这个消息(control_type为ListItem)内有没有按钮(消息是人发的必然会有头像按钮这个UI,系统消息比如'8:55'没有这个UI)
        chats=[chat for chat in chatList.children(control_type='ListItem') if chat.descendants(control_type='Button')]#不包括时间戳和系统消息
        sent_message=[sent_message for sent_message in chats if sent_message.descendants(control_type='Button')[-1].window_text()==myname]
        while not sent_message and sent_message[-1].is_visible():#如果聊天记录页为空或者我发过的最后一条消息(转发的消息)不可见(可能是网络延迟发送较慢造成，也不排除是被顶到最上边了)
            chats=[chat for chat in chatList.children(control_type='ListItem') if chat.descendants(control_type='Button')]#不包括时间戳和系统消息,只有是好友发送的时候，这个消息内部才有(Button属性)
            sent_message=[sent_message for sent_message in chats if sent_message.descendants(control_type='Button')[-1].window_text()==myname]
            time.sleep(retry_interval)
            counter+=1
            if counter>max_retry_times: 
                raise TimeoutError
        button=sent_message[-1].children()[0].children()[1]
        button.right_click_input()
        menu=main_window.child_window(**Menus.RightClickMenu)
        select_contact_window=main_window.child_window(**Main_window.SelectContactWindow)
        if not select_contact_window.exists():
            while not menu.exists():
                button.right_click_input()
                time.sleep(0.2)
        forward=menu.child_window(**MenuItems.ForwardMenuItem)
        while not forward.exists():
            main_window.click_input()
            button.right_click_input()
            time.sleep(0.2)
        forward.click_input()
        select_contact_window.child_window(**Buttons.MultiSelectButton).click_input()   
        send_button=select_contact_window.child_window(**Buttons.SendRespectivelyButton)
        search_button=select_contact_window.child_window(**Edits.SearchEdit)
        return search_button,send_button
    if len(message)==0:
        raise CantSendEmptyMessageError
    chat,main_window=Tools.open_dialog_window(friends[0],wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    #超过2000字发txt
    if len(message)<2000:
        chat.click_input()
        Systemsettings.copy_text_to_windowsclipboard(message)
        pyautogui.hotkey('ctrl','v',_pause=False)
        time.sleep(delay)
        pyautogui.hotkey('alt','s',_pause=False)
    elif len(message)>2000:
        chat.click_input()
        Systemsettings.convert_long_text_to_txt(message)
        pyautogui.hotkey('ctrl','v',_pause=False)
        time.sleep(delay)
        pyautogui.hotkey('alt','s',_pause=False)
        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
    friends=friends[1:]
    if len(friends)<=9:
        search_button,send_button=right_click_message()
        for other_friend in friends:
            search_button.click_input()
            Systemsettings.copy_text_to_windowsclipboard(other_friend)
            pyautogui.hotkey('ctrl','v')
            time.sleep(delay)
            pyautogui.press('enter')
            pyautogui.hotkey('ctrl','a')
            pyautogui.press('backspace')
            time.sleep(delay)
        send_button.click_input()
    else:  
        res=len(friends)%9
        for i in range(0,len(friends),9):
            if i+9<=len(friends):
                search_button,send_button=right_click_message()
                for other_friend in friends[i:i+9]:
                    search_button.click_input()
                    Systemsettings.copy_text_to_windowsclipboard(other_friend)
                    pyautogui.hotkey('ctrl','v')
                    time.sleep(delay)
                    pyautogui.press('enter')
                    pyautogui.hotkey('ctrl','a')
                    pyautogui.press('backspace')
                    time.sleep(delay)
                send_button.click_input()
            else:
                pass
        if res:
            search_button,send_button=right_click_message()
            for other_friend in friends[len(friends)-res:len(friends)]:
                search_button.click_input()
                Systemsettings.copy_text_to_windowsclipboard(other_friend)
                pyautogui.hotkey('ctrl','v')
                time.sleep(delay)
                pyautogui.press('enter')
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('backspace')
                time.sleep(delay)
            send_button.click_input()
    time.sleep(1)
    if close_wechat:
        main_window.close()
        
def send_file_to_friend(friend:str,file_path:str,with_messages:bool=False,messages:list=[],messages_first:bool=False,delay:float=1,tickle:bool=False,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于给单个好友或群聊发送单个文件\n
    Args:
        friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
        file_path:\t待发送文件绝对路径。\n
        with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False\n
        messages:\t与文件一同发送的消息。格式:message=["消息1","消息2","消息3"]\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        delay:\t发送单条信息或文件的延迟,单位:秒/s,默认2s。\n
        tickle:\t是否在发送消息或文件后拍一拍好友,默认为False\n
        messages_first:\t默认先发送文件后发送消息,messages_first设置为True,先发送消息,后发送文件,\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏法搜索好友信息打开聊天界面\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    if len(file_path)==0:
        raise NotFileError
    if not Systemsettings.is_file(file_path):
        raise NotFileError
    if Systemsettings.is_dirctory(file_path):
        raise NotFileError
    if Systemsettings.is_empty_file(file_path):
        raise EmptyFileError
    chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    chat.click_input()
    if with_messages and messages:
        if messages_first:
            for message in messages:
                if len(message)==0:
                    main_window.close()
                    raise CantSendEmptyMessageError
                if len(message)<2000:
                    Systemsettings.copy_text_to_windowsclipboard(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                elif len(message)>2000:
                    Systemsettings.convert_long_text_to_txt(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                    warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
            Systemsettings.copy_file_to_windowsclipboard(file_path=file_path)
            pyautogui.hotkey("ctrl","v")
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)   
        else:
            Systemsettings.copy_file_to_windowsclipboard(file_path=file_path)
            pyautogui.hotkey("ctrl","v")
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
            for message in messages:
                if len(message)==0:
                    main_window.close()
                    raise CantSendEmptyMessageError
                if len(message)<2000:
                    Systemsettings.copy_text_to_windowsclipboard(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                elif len(message)>2000:
                    Systemsettings.convert_long_text_to_txt(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                    warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
    else:
        Systemsettings.copy_file_to_windowsclipboard(file_path=file_path)
        pyautogui.hotkey("ctrl","v")
        time.sleep(delay)
        pyautogui.hotkey('alt','s',_pause=False)
    if tickle:
        tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
    time.sleep(1)
    if close_wechat:
        main_window.close()

def send_files_to_friend(friend:str,folder_path:str,with_messages:bool=False,messages:list=[str],messages_first:bool=False,delay:float=1,tickle:bool=False,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,search_pages:int=5):
    '''
    该函数用于给单个好友或群聊发送多个文件\n
    Args:
        friend:\t好友或群聊备注。格式:friend="好友或群聊备注"\n
        folder_path:\t所有待发送文件所处的文件夹的地址。\n
        with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False。\n
        messages:\t与文件一同发送的消息。格式:message=["消息1","消息2","消息3"]\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。
        delay:\t发送单条信息或文件的延迟,单位:秒/s,默认2s。\n
        tickle:\t是否在发送文件或消息后拍一拍好友,默认为False\n
        messages_first:\t默认先发送文件后发送消息,messages_first设置为True,先发送消息,后发送文件,\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
    '''
    if len(folder_path)==0:
        raise NotFolderError
    if not Systemsettings.is_dirctory(folder_path):
        raise NotFolderError
    files_in_folder=Systemsettings.get_files_in_folder(folder_path=folder_path)
    if not files_in_folder:
        raise EmptyFolderError
    def send_files():
        if len(files_in_folder)<=9:
            Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder)
            pyautogui.hotkey("ctrl","v")
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        else:
            files_num=len(files_in_folder)
            rem=len(files_in_folder)%9
            for i in range(0,files_num,9):
                if i+9<files_num:
                    Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[i:i+9])
                    pyautogui.hotkey("ctrl","v")
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
            if rem:
                Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[files_num-rem:files_num])
                pyautogui.hotkey("ctrl","v")
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
    chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    chat.click_input()
    if with_messages and messages:
        if messages_first:
            for message in messages:
                if len(message)==0:
                    main_window.close()
                    raise CantSendEmptyMessageError
                if len(message)<2000:
                    Systemsettings.copy_text_to_windowsclipboard(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                elif len(message)>2000:
                    Systemsettings.convert_long_text_to_txt(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                    warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
            send_files()
        else:
            send_files()
            for message in messages:
                if len(message)==0:
                    main_window.close()
                    raise CantSendEmptyMessageError
                if len(message)<2000:
                    Systemsettings.copy_text_to_windowsclipboard(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                elif len(message)>2000:
                    Systemsettings.convert_long_text_to_txt(message)
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
                    warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning) 
    else:
        send_files()
    if tickle:
        tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)        
    time.sleep(1)
    if close_wechat:
        main_window.close()

def send_file_to_friends(friends:list[str],file_paths:list[str],with_messages:bool=False,messages:list[list[str]]=[],messages_first:bool=False,delay:float=1,tickle:list[bool]=[],wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于给每个好友或群聊发送单个不同的文件以及消息\n
    Args:
        friends:\t好友或群聊备注。格式:friends=["好友1","好友2","好友3"]\n
        file_paths:\t待发送文件,格式: file=[发给好友1的单个文件,发给好友2的文件,发给好友3的文件]。\n
        with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False\n
        messages:\t待发送消息,格式:messages=["发给好友1的单条消息","发给好友2的单条消息","发给好友3的单条消息"]
        messages_first:\t先发送消息还是先发送文件.默认先发送文件\n
        delay:\t发送单条消息延迟,单位:秒/s,默认1s。\n
        tickle:\t是否给每一个好友发送消息或文件后拍一拍好友,格式为:[True,True,False,...]的bool值列表,与friends列表中的每一个好友对应\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
    注意!messages,filepaths与friends长度需一致,并且messages内每一条消息顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
    
    '''
    for file_path in file_paths:
        file_path=re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',file_path)
        if len(file_path)==0:
            raise NotFileError
        if not Systemsettings.is_file(file_path):
            raise NotFileError
        if Systemsettings.is_dirctory(file_path):
            raise NotFileError
        if Systemsettings.is_empty_file(file_path):
            raise EmptyFileError
    Files=dict(zip(friends,file_paths))
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    time.sleep(1)
        #多个好友的发送任务不需要使用open_dialog_window方法了直接在顶部搜索栏搜索,一个一个打开好友的聊天界面，发送消息,这样最高效
    if with_messages and messages:
        Chats=dict(zip(friends,messages))
        i=0
        for friend in Files:
            search=main_window.child_window(**Main_window.Search)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            pyautogui.hotkey('ctrl','v')
            time.sleep(0.5)
            pyautogui.press('enter')
            chat=main_window.child_window(title=friend,control_type='Edit')
            chat.click_input()
            if messages_first:
                messages=Chats.get(friend)
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
                Systemsettings.copy_file_to_windowsclipboard(Files.get(friend))
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
            else:
                Systemsettings.copy_file_to_windowsclipboard(Files.get(friend))
                pyautogui.hotkey('ctrl','v',_pause=False)
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
                messages=Chats.get(friend)
                for message in messages:
                    if len(message)==0:
                        main_window.close()
                        raise CantSendEmptyMessageError
                    if len(message)<2000:
                        Systemsettings.copy_text_to_windowsclipboard(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                    elif len(message)>2000:
                        Systemsettings.convert_long_text_to_txt(message)
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        time.sleep(delay)
                        pyautogui.hotkey('alt','s',_pause=False)
                        warn(message=f"微信消息字数上限为2000,超过2000字部分将被省略,该条长文本消息已为你转换为txt发送",category=LongTextWarning)
            if tickle:
                if tickle[i]:
                    tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
                i+=1
    else:
        i=0
        for friend in Files:
            search=main_window.child_window(**Main_window.Search)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(1)
            pyautogui.press('enter')
            chat=main_window.child_window(title=friend,control_type='Edit')
            chat.set_focus()
            chat.click_input()
            Systemsettings.copy_file_to_windowsclipboard(Files.get(friend))
            pyautogui.hotkey('ctrl','v',_pause=False)
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
            if tickle:
                if tickle[i]:
                    tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
                i+=1
    time.sleep(1)
    if close_wechat:
        main_window.close()

def send_files_to_friends(friends:list[str],folder_paths:list[str],with_messages:bool=False,messages:list[list[str]]=[],message_first:bool=False,delay:float=1,tickle:list[bool]=[],wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于给多个好友或群聊发送多个不同或相同的文件夹内的所有文件\n
    Args:
        friends:\t好友或群聊备注。格式:friends=["好友1","好友2","好友3"]\n
        folder_paths:\t待发送文件夹路径列表,每个文件夹内可以存放多个文件,格式: FolderPath_list=["","",""]\n
        with_messages:\t发送文件时是否给好友发消息。True发送消息,默认为False\n
        message_list:\t待发送消息,格式:message=[[""],[""],[""]]\n
        message_first:\t先发送消息还是先发送文件,默认先发送文件\n
        delay:\t发送单条消息延迟,单位:秒/s,默认1s。\n
        tickle:\t是否给每一个好友发送消息或文件后拍一拍好友,格式为:[True,True,False,...]的bool值列表,与friends列表中的每一个好友对应\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    注意! messages,folder_paths与friends长度需一致,并且messages内每一条消息FolderPath_list每一个文件\n
    顺序需与friends中好友名称出现顺序一致,否则会出现消息发错的尴尬情况\n
    '''
    for folder_path in folder_paths:
        folder_path=re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',folder_path)
        if len(folder_path)==0:
            raise NotFolderError
        if not Systemsettings.is_dirctory(folder_path):
            raise NotFolderError
    def send_files(folder_path):
        files_in_folder=Systemsettings.get_files_in_folder(folder_path=folder_path)
        if len(files_in_folder)<=9:
            Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder)
            pyautogui.hotkey("ctrl","v")
            time.sleep(delay)
            pyautogui.hotkey('alt','s',_pause=False)
        else:
            files_num=len(files_in_folder)
            rem=len(files_in_folder)%9
            for i in range(0,files_num,9):
                if i+9<files_num:
                    Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[i:i+9])
                    pyautogui.hotkey("ctrl","v")
                    time.sleep(delay)
                    pyautogui.hotkey('alt','s',_pause=False)
            if rem:
                Systemsettings.copy_files_to_windowsclipboard(filepaths_list=files_in_folder[files_num-rem:files_num])
                pyautogui.hotkey("ctrl","v")
                time.sleep(delay)
                pyautogui.hotkey('alt','s',_pause=False)
    folder_paths=[re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',folder_path) for folder_path in folder_paths]
    Files=dict(zip(friends,folder_paths))
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    if with_messages and messages:
        Chats=dict(zip(friends,messages))
        i=0
        for friend in Files:
            search=main_window.child_window(**Main_window.Search)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            time.sleep(0.5)
            pyautogui.hotkey('ctrl','v',_pause=False)
            pyautogui.press('enter')
            chat=main_window.child_window(title=friend,control_type='Edit')
            chat.click_input()
            if message_first:
                messages=Chats.get(friend)
                Messages.send_messages_to_friend(friend=friend,messages=messages,close_wechat=False,delay=delay)
                folder_path=Files.get(friend)
                send_files(folder_path)
            else:
                folder_path=Files.get(friend)
                send_files(folder_path)
                messages=Chats.get(friend)
                Messages.send_messages_to_friend(friend=friend,messages=messages,close_wechat=False,delay=delay)
            if tickle:
                if tickle[i]:
                    tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
                i+=1
    else:
        i=0
        for friend in Files:
            search=main_window.child_window(**Main_window.Search)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(friend)
            time.sleep(1)
            pyautogui.press('enter')
            chat=main_window.child_window(title=friend,control_type='Edit')
            chat.click_input()
            folder_path=Files.get(friend)
            send_files(folder_path)
            if tickle:
                if tickle[i]:
                    tickle_friend(friend=friend,wechat_path=wechat_path,is_maximize=True,close_wechat=False)
                i+=1
    time.sleep(1)
    if close_wechat:
        main_window.close()

def forward_file(friends:list[str],file_path:str,delay:float=0.5,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用于给好友转发文件,实际使用时建议先给文件传输助手转发\n
    这样可以避免对方聊天信息更新过快导致转发消息被'淹没',进而无法定位出错的问题。\n
    Args:
        friends:\t好友或群聊备注列表。格式:friends=["好友1","好友2","好友3"]\n
        file_path:\t待发送文件,格式: file_path="转发文件路径"。\n
        delay:发送单条消息延迟,单位:秒/s,默认1s。\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        search_pages:在会话列表中查询查找第一个转发文件的好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
    '''
    if len(file_path)==0:
        raise NotFileError
    if Systemsettings.is_empty_file(file_path):
        raise EmptyFileError
    if Systemsettings.is_dirctory(file_path):
        raise NotFileError
    if not Systemsettings.is_file(file_path):
        raise NotFileError    
    def right_click_message():
        max_retry_times=25
        retry_interval=0.2
        counter=0
        #查找最新的我自己发的消息，并右键单击我发送的消息，点击转发按钮
        chatList=main_window.child_window(**Main_window.FriendChatList)
        myname=main_window.child_window(**Buttons.MySelfButton).window_text()
        #if message.descendants(conrol_type)是用来筛选这个消息(control_type为ListItem)内有没有按钮(消息是人发的必然会有头像按钮这个UI,系统消息比如'8:55'没有这个UI)
        chats=[chat for chat in chatList.children(control_type='ListItem') if chat.descendants(control_type='Button')]#不包括时间戳和系统消息
        sent_message=[sent_message for sent_message in chats if sent_message.descendants(control_type='Button')[-1].window_text()==myname]
        while not sent_message and sent_message[-1].is_visible():#如果聊天记录页为空或者我发过的最后一条消息(转发的消息)不可见(可能是网络延迟发送较慢造成，也不排除是被顶到最上边了)
            chats=[chat for chat in chatList.children(control_type='ListItem') if chat.descendants(control_type='Button')]#不包括时间戳和系统消息,只有是好友发送的时候，这个消息内部才有(Button属性)
            sent_message=[sent_message for sent_message in chats if sent_message.descendants(control_type='Button')[-1].window_text()==myname]
            time.sleep(retry_interval)
            counter+=1
            if counter>max_retry_times: 
                raise TimeoutError
        button=sent_message[-1].children()[0].children()[1]
        button.right_click_input()
        menu=main_window.child_window(**Menus.RightClickMenu)
        select_contact_window=main_window.child_window(**Main_window.SelectContactWindow)
        if not select_contact_window.exists():
            while not menu.exists():
                button.right_click_input()
                time.sleep(0.2)
        forward=menu.child_window(**MenuItems.ForwardMenuItem)
        while not forward.exists():
            main_window.click_input()
            button.right_click_input()
            time.sleep(0.2)
        forward.click_input()
        select_contact_window.child_window(**Buttons.MultiSelectButton).click_input()   
        send_button=select_contact_window.child_window(**Buttons.SendRespectivelyButton)
        search_button=select_contact_window.child_window(**Edits.SearchEdit)
        return search_button,send_button
    chat,main_window=Tools.open_dialog_window(friend=friends[0],wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    chat.click_input()
    Systemsettings.copy_file_to_windowsclipboard(file_path=file_path)
    pyautogui.hotkey("ctrl","v")
    time.sleep(delay)
    pyautogui.hotkey('alt','s',_pause=False) 
    friends=friends[1:]
    if len(friends)<=9:
        search_button,send_button=right_click_message()
        for other_friend in friends:
            search_button.click_input()
            Systemsettings.copy_text_to_windowsclipboard(other_friend)
            pyautogui.hotkey('ctrl','v')
            time.sleep(delay)
            pyautogui.press('enter')
            pyautogui.hotkey('ctrl','a')
            pyautogui.press('backspace')
            time.sleep(delay)
        send_button.click_input()
    else:  
        res=len(friends)%9
        for i in range(0,len(friends),9):
            if i+9<=len(friends):
                search_button,send_button=right_click_message()
                for other_friend in friends[i:i+9]:
                    search_button.click_input()
                    Systemsettings.copy_text_to_windowsclipboard(other_friend)
                    pyautogui.hotkey('ctrl','v')
                    time.sleep(delay)
                    pyautogui.press('enter')
                    pyautogui.hotkey('ctrl','a')
                    pyautogui.press('backspace')
                    time.sleep(delay)
                send_button.click_input()
            else:
                pass
        if res:
            search_button,send_button=right_click_message()
            for other_friend in friends[len(friends)-res:len(friends)]:
                search_button.click_input()
                Systemsettings.copy_text_to_windowsclipboard(other_friend)
                pyautogui.hotkey('ctrl','v')
                time.sleep(delay)
                pyautogui.press('enter')
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('backspace')
                time.sleep(delay)
            send_button.click_input()
    time.sleep(1)
    if close_wechat:
        main_window.close()

def voice_call(friend:str,search_pages:int=5,wechat_path=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来给好友拨打语音电话\n
    Args:
        friend:好友备注\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    main_window=Tools.open_dialog_window(friend,wechat_path,search_pages=search_pages,is_maximize=is_maximize)[1]  
    Tool_bar=main_window.child_window(**Main_window.ChatToolBar)
    voice_call_button=Tool_bar.children(**Buttons.VoiceCallButton)[0]
    time.sleep(1)
    voice_call_button.click_input()
    if close_wechat:
        main_window.close()

def video_call(friend:str,search_pages:int=5,wechat_path=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来给好友拨打视频电话\n
    Args:
        friend:\t好友备注.\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    main_window=Tools.open_dialog_window(friend,wechat_path,search_pages=search_pages,is_maximize=is_maximize)[1]  
    Tool_bar=main_window.child_window(**Main_window.ChatToolBar)
    voice_call_button=Tool_bar.children(**Buttons.VideoCallButton)[0]
    time.sleep(1)
    voice_call_button.click_input()
    if close_wechat:
        main_window.close()

def voice_call_in_group(group_name:str,friends:list[str],search_pages:int=5,wechat_path=None,is_maximize:bool=True,close_wechat:bool=True,):
    '''
    该函数用来在群聊中发起语音电话\n
    Args:
        group_name:\t群聊备注\n
        friends:\t所有要呼叫的群友备注\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        lose_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    main_window=Tools.open_dialog_window(friend=group_name,search_pages=search_pages,wechat_path=wechat_path,is_maximize=is_maximize)[1]  
    Tool_bar=main_window.child_window(**Main_window.ChatToolBar)
    voice_call_button=Tool_bar.children(**Buttons.VoiceCallButton)[0]
    time.sleep(2)
    voice_call_button.click_input()
    add_talk_memver_window=main_window.child_window(**Main_window.AddTalkMemberWindow)
    search=add_talk_memver_window.child_window(**Edits.SearchEdit)
    for friend in friends:
        search.click_input()
        Systemsettings.copy_text_to_windowsclipboard(friend)
        pyautogui.hotkey('ctrl','v')
        time.sleep(0.5)
        pyautogui.press('enter')
        pyautogui.hotkey('ctrl','a')
        pyautogui.press('backspace')
        time.sleep(0.5)
    confirm_button=add_talk_memver_window.child_window(**Buttons.CompleteButton)
    confirm_button.click_input()
    time.sleep(1)
    if close_wechat:
        main_window.close()

def get_friends_names(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来获取通讯录中所有好友的名称与昵称。\n
    结果以json格式返回\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    def get_names(friends):
        names=[]
        for ListItem in friends:
            nickname=ListItem.descendants(control_type='Button')[0].window_text()
            remark=ListItem.descendants(control_type='Text')[0].window_text()
            names.append((nickname,remark))
        return names
    contacts_settings_window=Tools.open_contacts_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=True)[0]
    total_pane=contacts_settings_window.child_window(**Panes.ContactsManagePane)
    total_number=total_pane.child_window(control_type='Text',found_index=1).window_text()
    total_number=total_number.replace('(','').replace(')','')
    total_number=int(total_number)#好友总数
    #先点击选中第一个好友，双击选中取消后，才可以在按下pagedown之后才可以滚动页面，每页可以记录11人
    friends_list=contacts_settings_window.child_window(title='',control_type='List')
    friends=friends_list.children(control_type='ListItem')
    first=friends_list.children()[0].descendants(control_type='CheckBox')[0]     
    first.double_click_input()
    pages=total_number//11#点击选中在不选中第一个好友后，每一页最少可以记录11人，pages是总页数，也是pagedown按钮的按下次数
    res=total_number%11#好友人数不是11的整数倍数时，需要处理余数部分
    Names=[]
    if total_number<=11:
        friends=friends_list.children(control_type='ListItem')
        Names.extend(get_names(friends))
        contacts_settings_window.close()
        contacts=[{'昵称':name[1],'备注':name[0]}for name in Names]
        contacts_json=json.dumps(contacts,ensure_ascii=False,indent=4)
        if not close_wechat:
            Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        return contacts_json
    else:
        for _ in range(pages):
            friends=friends_list.children(control_type='ListItem')
            Names.extend(get_names(friends))
            pyautogui.keyDown('pagedown',_pause=False)
        if res:
        #处理余数部分
            pyautogui.keyDown('pagedown',_pause=False)
            friends=friends_list.children(control_type='ListItem')
            Names.extend(get_names(friends[11-res:11]))
            contacts_settings_window.close()
            contacts=[{'昵称':name[1],'备注':name[0]}for name in Names]
            contacts_json=json.dumps(contacts,ensure_ascii=False,indent=4)
            if not close_wechat:
                Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        else:
            contacts_settings_window.close()
            contacts=[{'昵称':name[1],'备注':name[0]}for name in Names]
            contacts_json=json.dumps(contacts,ensure_ascii=False,indent=4)
            if not close_wechat:
                Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        return contacts_json
                     
def get_wecom_friends_info(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函數用来获取通讯录中所有未离职的企业微信好友的信息(昵称,企业名称)\n
    结果以json格式返回\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    def get_info():
        post='无'
        company='无'
        global base_info_pane
        global detail_info_pane
        try:
            try:
                base_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
            except IndexError:
                base_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
            try:
                detail_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
            except  IndexError:
                detail_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
            detail_info=detail_info_pane.descendants(control_type='Text')
            detail_info=[element.window_text() for element in detail_info]
            if language=='简体中文':
                if '企业信息' in detail_info and '已离职' not in detail_info:
                    base_info=base_info_pane.descendants(control_type='Text')
                    base_info=[element.window_text() for element in base_info]
                    # #如果有昵称选项,说明好友有备注
                    if base_info[1]=='昵称：':
                        remark=base_info[0]
                        nickname=base_info[2]
                    else:
                        nickname=base_info[0]
                        remark=nickname
                    company=detail_info[detail_info.index('企业')+1]
                    if '职务' in detail_info:
                        post=detail_info[detail_info.index('职务')+1]
                    return nickname,company,remark,post
                else:
                    return '非企业微信联系人'
                
            if language=='英文':
                if 'Enterprise Information' in detail_info and '已离职' not in detail_info:
                    base_info=base_info_pane.descendants(control_type='Text')
                    base_info=[element.window_text() for element in base_info]
                    # #如果有昵称选项,说明好友有备注
                    if base_info[1]=='Name: ':
                        remark=base_info[0]
                        nickname=base_info[2]
                    else:
                        nickname=base_info[0]
                        remark=nickname
                    company=detail_info[detail_info.index('Company')+1]
                    if 'Title' in detail_info:
                        post=detail_info[detail_info.index('Title')+1]
                    return nickname,company,remark,post
                else:
                    return '非企业微信联系人'
                
            if language=='繁体中文':
                if '企業資訊' in detail_info and '已离职' not in detail_info:
                    base_info=base_info_pane.descendants(control_type='Text')
                    base_info=[element.window_text() for element in base_info]
                    # #如果有昵称选项,说明好友有备注
                    if base_info[1]=='暱稱：':
                        remark=base_info[0]
                        nickname=base_info[2]
                    else:
                        nickname=base_info[0]
                        remark=nickname
                    company=detail_info[detail_info.index('企業')+1]
                    if '職務' in detail_info:
                        post=detail_info[detail_info.index('職務')+1]
                    return nickname,company,remark,post
                else:
                    return '非企业微信联系人'
        except IndexError:
            return '非企业微信联系人'

            
    main_window=Tools.open_contacts(wechat_path=wechat_path,is_maximize=is_maximize)
    contacts=main_window.child_window(**SideBar.Contacts)
    contacts.set_focus()
    contacts.click_input()
    contacts_list=main_window.child_window(**Main_window.ContactsList)
    rec=contacts_list.rectangle()  
    mouse.click(coords=(rec.right-5,rec.top+10))
    pyautogui.press('End')
    contacts_list=main_window.child_window(**Main_window.ContactsList)
    last_wecom_friend_info=get_info()
    while last_wecom_friend_info=='非企业微信联系人':
        pyautogui.keyDown('up')
        try:
            detail_info=detail_info_pane.descendants(control_type='Text')
            detail_info=[element.window_text() for element in detail_info]
            if language=='简体中文':
                if '企业信息' in detail_info and '已离职' not in detail_info:
                    base_info=base_info_pane.descendants(control_type='Text')
                    base_info=[element.window_text() for element in base_info]
                    # #如果有昵称选项,说明好友有备注
                    if base_info[1]=='昵称：':
                        remark=base_info[0]
                        nickname=base_info[2] 
                    else:
                        nickname=base_info[0]
                        remark=nickname
                    company=detail_info[detail_info.index('企业')+1]
                    if '职务' in detail_info:
                        post=detail_info[detail_info.index('职务')+1] 
                    last_wecom_friend_info=company 

            if language=='英文':
                if 'Enterprise Information' in detail_info and '已离职' not in detail_info:
                    base_info=base_info_pane.descendants(control_type='Text')
                    base_info=[element.window_text() for element in base_info]
                    # #如果有昵称选项,说明好友有备注
                    if base_info[1]=='Name: ':
                        remark=base_info[0]
                        nickname=base_info[2] 
                    else:
                        nickname=base_info[0]
                        remark=nickname
                    company=detail_info[detail_info.index('Company')+1]
                    if 'Title' in detail_info:
                        post=detail_info[detail_info.index('Title')+1] 
                    last_wecom_friend_info=company
            
            if language=='繁体中文':
                if '企業資訊' in detail_info and '已离职' not in detail_info:
                    base_info=base_info_pane.descendants(control_type='Text')
                    base_info=[element.window_text() for element in base_info]
                    # #如果有昵称选项,说明好友有备注
                    if base_info[1]=='暱稱：':
                        remark=base_info[0]
                        nickname=base_info[2] 
                    else:
                        nickname=base_info[0]
                        remark=nickname
                    company=detail_info[detail_info.index('企業')+1]
                    if '職務' in detail_info:
                        post=detail_info[detail_info.index('職務')+1] 
                    last_wecom_friend_info=company 
        except IndexError:
            pass
    
    pyautogui.press('Home')
    companies=[last_wecom_friend_info,'nothing']
    nicknames=[]
    remarks=[]
    posts=[]
    while companies[-1]!=companies[0]:
        try:
            detail_info=detail_info_pane.descendants(control_type='Text')
            detail_info=[element.window_text() for element in detail_info]
            if language=='简体中文':
                if '企业信息' in detail_info and '已离职' not in detail_info:
                    base_info=base_info_pane.descendants(control_type='Text')
                    base_info=[element.window_text() for element in base_info]
                    # #如果有昵称选项,说明好友有备注
                    if base_info[1]=='昵称：':
                        remark=base_info[0]
                        nickname=base_info[2]
                    else:
                        nickname=base_info[0]
                        remark=nickname
                    company=detail_info[detail_info.index('企业')+1]
                    if '职务' in detail_info:
                        post=detail_info[detail_info.index('职务')+1]
                        posts.append(post)
                    else:
                        posts.append('无')
                    nicknames.append(nickname)
                    remarks.append(remark)
                    companies.append(company)
                else:
                    pass

            if language=='英文':
                if 'Enterprise Information' in detail_info and '已离职' not in detail_info:
                    base_info=base_info_pane.descendants(control_type='Text')
                    base_info=[element.window_text() for element in base_info]
                    # #如果有昵称选项,说明好友有备注
                    if base_info[1]=='Name: ':
                        remark=base_info[0]
                        nickname=base_info[2]
                    else:
                        nickname=base_info[0]
                        remark=nickname
                    company=detail_info[detail_info.index('Company')+1]
                    if 'Title' in detail_info:
                        post=detail_info[detail_info.index('Title')+1]
                        posts.append(post)
                    else:
                        posts.append('无')
                    nicknames.append(nickname)
                    remarks.append(remark)
                    companies.append(company)
                else:
                    pass
            
            if language=='繁体中文':
                if '企業資訊' in detail_info and '已离职' not in detail_info:
                    base_info=base_info_pane.descendants(control_type='Text')
                    base_info=[element.window_text() for element in base_info]
                    # #如果有昵称选项,说明好友有备注
                    if base_info[1]=='暱稱：':
                        remark=base_info[0]
                        nickname=base_info[2]
                    else:
                        nickname=base_info[0]
                        remark=nickname
                    company=detail_info[detail_info.index('企業')+1]
                    if '職務' in detail_info:
                        post=detail_info[detail_info.index('職務')+1]
                        posts.append(post)
                    else:
                        posts.append('无')
                    nicknames.append(nickname)
                    remarks.append(remark)
                    companies.append(company)
                else:
                    pass

        except IndexError:
            pass
        pyautogui.keyDown('down')  
    del(companies[0])
    del(companies[0])
    record=zip(nicknames,remarks,companies,posts)
    contacts=[{'昵称':friend[0],'备注':friend[1],'企业':friend[2],'职务':friend[3]}for friend in record]
    WeCom_json=json.dumps(contacts,ensure_ascii=False,indent=4)
    if close_wechat:
        main_window.close()
    return WeCom_json

def auto_answer_call(duration:str,broadcast_content:str,message:str=None,times:int=2,wechat_path:str=None,close_wechat:bool=True):
    '''
    该函数用来自动接听微信电话\n
    注意！一旦开启自动接听功能后,在设定时间内,你的所有视频语音电话都将优先被PC微信接听,并按照设定的播报与留言内容进行播报和留言。\n
    Args:
        duration:\t自动接听功能持续时长,格式:s,min,h分别对应秒,分钟,小时,例:duration='1.5h'持续1.5小时\n
        broadcast_content:\twindowsAPI语音播报内容\n
        message:\t语音播报结束挂断后,给呼叫者发送的留言\n
        times:\t语音播报重复次数\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    def judge_call(call_interface):
        window_text=call_interface.child_window(found_index=1,control_type='Button').texts()[0]
        if '视频通话' in window_text:
            index=window_text.index("邀")
            caller_name=window_text[0:index]
            return '视频通话',caller_name
        else:
            index=window_text.index("邀")
            caller_name=window_text[0:index]
            return "语音通话",caller_name
    caller_names=[]
    flags=[]
    unchanged_duration=duration
    duration=match_duration(duration)
    if not duration:
        raise TimeNotCorrectError
    desktop=Desktop(**Independent_window.Desktop)
    Systemsettings.open_listening_mode(volume=True)
    start_time=time.time()
    while True:
        if time.time()-start_time<duration:
           
            call_interface1=desktop.window(**Independent_window.OldIncomingCallWindow)
            call_interface2=desktop.window(**Independent_window.NewIncomingCallWindow)
            if call_interface1.exists():
                flag,caller_name=judge_call(call_interface1)
                caller_names.append(caller_name)
                flags.append(flag)
                call_window=call_interface1.child_window(found_index=3,title="",control_type='Pane')
                accept=call_window.children(**Buttons.AcceptButton)[0]
                if flag=="语音通话":
                    time.sleep(1)
                    accept.click_input()
                    time.sleep(1)
                    accept_call_window=desktop.window(**Independent_window.OldVoiceCallWindow)
                    if accept_call_window.exists():
                        duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                        while not duration_time.exists():
                            time.sleep(1)
                            duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                        Systemsettings.speaker(times=times,text=broadcast_content)
                        answering_window=accept_call_window.child_window(found_index=13,control_type='Pane',title='')
                        if answering_window.exists():
                            reject=answering_window.child_window(**Buttons.HangUpButton)
                            reject.click_input()
                            if message:
                                Messages.send_message_to_friend(wechat_path=wechat_path,friend=caller_name,close_wechat=close_wechat,message=message)     
                else:
                    time.sleep(1)
                    accept.click_input()
                    time.sleep(1)
                    accept_call_window=desktop.window(**Independent_window.OldVideoCallWindow)
                    accept_call_window.click_input()
                    duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                    while not duration_time.exists():
                            time.sleep(1)
                            accept_call_window.click_input()
                            duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                    Systemsettings.speaker(times=times,text=broadcast_content)
                    rec=accept_call_window.rectangle()
                    mouse.move(coords=(rec.left//2+rec.right//2,rec.bottom-50))
                    reject=accept_call_window.child_window(**Buttons.HangUpButton)
                    reject.click_input()
                    if message:
                        Messages.send_message_to_friend(wechat_path=wechat_path,friend=caller_name,message=message,close_wechat=close_wechat)
                    
            elif call_interface2.exists():
                call_window=call_interface2.child_window(found_index=4,title="",control_type='Pane')
                accept=call_window.children(**Buttons.AcceptButton)[0]
                flag,caller_name=judge_call(call_interface2)
                caller_names.append(caller_name)
                flags.append(flag)
                if flag=="语音通话":
                    time.sleep(1)
                    accept.click_input()
                    time.sleep(1)
                    accept_call_window=desktop.window(**Independent_window.NewVoiceCallWindow)
                    if accept_call_window.exists():
                        answering_window=accept_call_window.child_window(found_index=13,control_type='Pane',title='')
                        duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                        while not duration_time.exists():
                            time.sleep(1)
                            duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                        Systemsettings.speaker(times=times,text=broadcast_content)
                        if answering_window.exists():
                            reject=answering_window.children(**Buttons.HangUpButton)[0]
                            reject.click_input()
                            if message:
                                Messages.send_message_to_friend(wechat_path=wechat_path,friend=caller_name,message=message,close_wechat=close_wechat)
                else:
                    time.sleep(1)
                    accept.click_input()
                    time.sleep(1)
                    accept_call_window=desktop.window(**Independent_window.NewVideoCallWindow)
                    accept_call_window.click_input()
                    duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                    while not duration_time.exists():
                            time.sleep(1)
                            accept_call_window.click_input()
                            duration_time=accept_call_window.child_window(title_re='00:',control_type='Text')
                    Systemsettings.speaker(times=times,text=broadcast_content)
                    rec=accept_call_window.rectangle()
                    mouse.move(coords=(rec.left//2+rec.right//2,rec.bottom-50))
                    reject=accept_call_window.child_window(**Buttons.HangUpButton)
                    reject.click_input()
                    if message:
                        Messages.send_message_to_friend(wechat_path=wechat_path,friend=caller_name,message=message,close_wechat=close_wechat)
                    
            else:
                call_interface1=call_interface2=None
        else:
            break
    Systemsettings.close_listening_mode()
    if caller_names:
        print(f'自动接听微信电话结束,在{unchanged_duration}内内共计接听{len(caller_names)}个电话\n接听对象:{caller_names}\n电话类型{flags}')
    else:
        print(f'未接听到任何微信视频或语音电话')

def open_settings(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来打开微信设置界面。\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    setting=main_window.child_window(**SideBar.SettingsAndOthers)
    setting.click_input()
    settings_menu=main_window.child_window(**Main_window.SettingsMenu)
    settings_button=settings_menu.child_window(**Buttons.SettingsButton)
    settings_button.click_input() 
    time.sleep(2)
    desktop=Desktop(**Independent_window.Desktop)
    settings_window=desktop.window(**Independent_window.SettingWindow)
    if close_wechat:
        main_window.close()
    return settings_window,main_window
  
def Log_out(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来PC微信退出登录。\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    log_out_button=settings.window(**Buttons.LogoutButton)
    log_out_button.click_input()
    time.sleep(2)
    confirm_button=settings.window(**Buttons.ConfirmButton)
    confirm_button.click_input()

   
def Auto_convert_voice_messages_to_text(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信开启或关闭设置中的语音消息自动转文字。\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.GeneralTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=6)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            print("已关闭聊天中的语音消息自动转成文字")
        else:
            print('聊天的语音消息自动转成文字已开启,无需开启')
    else:     
        if state=='open':
            check_box.click_input()
            print("已开启聊天中的语音消息自动转成文字")
        else:
            print('聊天中的语音消息自动转成文字已关闭,无需关闭')
    if close_settings_window:
        settings.close()
   
def Adapt_to_PC_display_scalling(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信开启或关闭适配微信设置中的系统所释放比例。\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.GeneralTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=4)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            print("已关闭适配系统缩放比例")
        else:
            print('适配系统缩放比例已开启,无需开启')
    else:
        if state=='open':
            check_box.click_input()
            print("已开启适配系统缩放比例")
        else:
            print('适配系统缩放比例已关闭,无需关闭')
    if close_settings_window:
        settings.close()
  
def Save_chat_history(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信打开或关闭微信设置中的保留聊天记录选项。\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.GeneralTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=2)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            query_window=settings.child_window(title="",control_type="Pane",class_name='WeUIDialog')
            confirm=query_window.child_window(**Buttons.ConfirmButton)
            confirm.click_input()
            print("已关闭保留聊天记录")
        else:
            print('保留聊天记录已开启,无需开启')
    else:
        if state=='open':
            check_box.click_input()
            print("已开启保留聊天记录")
        else:
            print('保留聊天记录已关闭,无需关闭')
    if close_settings_window:
        settings.close()

def Run_wechat_when_pc_boots(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信打开或关闭微设置中的开机自启动微信。\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.GeneralTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=1)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            print("已关闭开机自启动微信")
        else:
            print('开机自启动微信已开启,无需开启')
    else:
        if state=='open':
            check_box.click_input()
            print("已开启关机自启动微信")
        else:
            print('开机自启动微信已关闭,无需关闭')
    if close_settings_window:
        settings.close()

def Using_default_browser(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信打开或关闭微信设置中的使用系统默认浏览器打开网页\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.GeneralTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=5)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            print("已关闭使用系统默认浏览器打开网页")
        else:
            print('使用系统默认浏览器打开网页已开启,无需开启')
    else:
        if state=='open':
            check_box.click_input()
            print("已开启使用系统默认浏览器打开网页")
        else:
            print('使用系统默认浏览器打开网页已关闭,无需关闭')
    if close_settings_window:
        settings.close()

   
def Auto_update_wechat(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信打开或关闭微信设置中的有更新时自动升级微信。\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.GeneralTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=0)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            query_window=settings.child_window(title="",control_type="Pane",class_name='WeUIDialog')
            confirm=query_window.child_window(title="关闭",control_type="Button")
            confirm.click_input()
            print("已关闭有更新时自动升级微信")
        else:
            print('有更新时自动升级微信已开启,无需开启')
    else:
        if state=='open':
            check_box.click_input()
            print("已开启有更新时自动升级微信")
        else:
            print('有更新时自动升级微信已关闭,无需关闭') 
    if close_settings_window:
        settings.close()


def Clear_chat_history(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信清空所有聊天记录,谨慎使用。\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.GeneralTabItem)
    general_settings.click_input()
    settings.child_window(**Buttons.ClearChatHistoryButton).click_input()
    query_window=settings.child_window(title="",control_type="Pane",class_name='WeUIDialog')
    confirm=query_window.child_window(**Buttons.ClearButton)
    confirm.click_input()
    if close_settings_window:
        settings.close()

def Close_auto_log_in(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信关闭自动登录,若需要开启需在手机端设置。\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    account_settings=settings.child_window(**TabItems.MyAccountTabItem)
    account_settings.click_input()
    try:
        close_button=settings.child_window(**Buttons.CloseAutoLoginButton)
        close_button.click_input()
        query_window=settings.child_window(title="",control_type="Pane",class_name='WeUIDialog')
        confirm=query_window.child_window(**Buttons.ConfirmButton)
        confirm.click_input()
        if close_settings_window:
            settings.close()
    except ElementNotFoundError:
        if close_settings_window:
            settings.close()
        raise AlreadyCloseError(f'已关闭自动登录选项,无需关闭！')
    
    
   
def Show_web_search_history(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信打开或关闭微信设置中的显示网络搜索历史。\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.GeneralTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=3)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            print("已关闭显示网络搜索历史")
        else:
            print('显示网络搜索历史已开启,无需开启')
    else:
        if state=='open':
            check_box.click_input()
            print("已开启显示网络搜索历史")
        else:
            print('显示网络搜索历史已关闭,无需关闭')
    if close_settings_window:
        settings.close()

def New_message_alert_sound(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信开启或关闭设置中的新消息通知声音。\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        swechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:任务完成后是否关闭设置界面窗口,默认关闭\n   
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.NotificationsTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=0)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            print("已关闭新消息通知声音")
        else:
            print('新消息通知声音已开启,无需开启')
    else:
        if state=='open':
            check_box.click_input()
            print("已开启新消息通知声音")
        else:
            print('新消息通知声音已关闭,无需关闭')
    if close_settings_window:
        settings.close()
    
def Voice_and_video_calls_alert_sound(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来PC微信开启或关闭设置中的语音和视频通话通知声音。\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.NotificationsTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=1)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            print("已关闭语音和视频通话通知声音")
        else:
            print('语音和视频通话通知声音已开启,无需开启')
    else:
        if state=='open':
            check_box.click_input()
            print("已开启语音和视频通话通知声音")
        else:
            print('语音和视频通话通知声音已关闭,无需关闭')
    settings.close()
  
def Moments_notification_flag(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信开启或关闭设置中的朋友圈消息提示。\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.NotificationsTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=2)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            print("已关闭朋友圈消息提示")
        else:
            print('朋友圈消息提示已开启,无需开启')
    else:
        if state=='open':
            check_box.click_input()
            print("已开启朋友圈消息提示")
        else:
            print('朋友圈消息提示已关闭,无需关闭')
    if close_settings_window:
        settings.close()

    
def Channel_notification_flag(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信开启或关闭设置中的视频号消息提示。\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.NotificationsTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=3)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            print("已关闭视频号消息提示")
        else:
            print('视频号消息提示已开启,无需开启')
    else:
        if state=='open':
            check_box.click_input()
            print("已开启视频号消息提示")
        else:
            print('视频号消息提示已关闭,无需关闭')
    if close_settings_window:
        settings.close()

def Topstories_notification_flag(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信开启或关闭设置中的看一看消息提示。\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.NotificationsTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=4)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            print("已关闭看一看消息提示")
        else:
            print("看一看消息提示已开启,无需开启")
    else:
        if state=='open':
            check_box.click_input()
            print("已开启看一看消息提示")
        else:
            print("看一看消息提示已关闭,无需关闭")
    if close_settings_window:
        settings.close()

def Miniprogram_notification_flag(state:str='open',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信开启或关闭设置中的小程序消息提示。\n
    Args:
        state:\t决定是否开启或关闭某项设置,取值:'close','open',默认为open\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    choices={'open','close'}
    if state not in choices:
        raise WrongParameterError
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general_settings=settings.child_window(**TabItems.NotificationsTabItem)
    general_settings.click_input()
    check_box=settings.child_window(control_type="CheckBox",found_index=5)
    if check_box.get_toggle_state():
        if state=='close':
            check_box.click_input()
            print("已关闭小程序消息提示")
        else:
            print('小程序消息提示已开启,无需开启')
    else:
        if state=='open':
            check_box.click_input()
            print("已开启小程序消息提示")
        else:
            print('小程序消息提示已关闭,无需关闭')
    if close_settings_window:
        settings.close()

def Change_capture_screen_shortcut(shortcuts:list[str],wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信修改微信设置中截取屏幕的快捷键。\n
    Args:
        shortcuts:\t快捷键键位名称列表,若你想将截取屏幕的快捷键设置为'ctrl+shift',那么shortcuts=['ctrl','shift']\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    
    '''
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    shortcut=settings.child_window(**TabItems.ShortCutTabItem)
    shortcut.click_input()
    capture_screen_button=settings.child_window(**Texts.CptureScreenShortcutText).parent().children()[1]
    capture_screen_button.click_input()
    settings.child_window(**Panes.ChangeShortcutPane).click_input()
    time.sleep(1)
    pyautogui.hotkey(*shortcuts)
    confirm_button=settings.child_window(**Buttons.ConfirmButton) 
    confirm_button.click_input()
    if close_settings_window:
        settings.close()
            
   
def Change_open_wechat_shortcut(shortcuts:list[str],wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信修改微信设置中打开微信的快捷键。\n
    Args:
        shortcuts:\t快捷键键位名称列表,若你想将截取屏幕的快捷键设置为'ctrl+shift',那么shortcuts=['ctrl','shift']\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    shortcut=settings.child_window(**TabItems.ShortCutTabItem)
    shortcut.click_input()
    open_wechat_button=settings.child_window(**Texts.OpenWechatShortcutText).parent().children()[1]
    open_wechat_button.click_input()
    settings.child_window(**Panes.ChangeShortcutPane).click_input()
    time.sleep(1)
    pyautogui.hotkey(*shortcuts)
    confirm_button=settings.child_window(**Buttons.ConfirmButton) 
    confirm_button.click_input()
    if close_settings_window:
        settings.close()

def Change_lock_wechat_shortcut(shortcuts:list[str],wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信修改微信设置中锁定微信的快捷键。\n
    Args:
        shortcuts:\t快捷键键位名称列表,若你想将截取屏幕的快捷键设置为'ctrl+shift',那么shortcuts=['ctrl','shift']\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    shortcut=settings.child_window(**TabItems.ShortCutTabItem)
    shortcut.click_input()
    lock_wechat_button=settings.child_window(**Texts.LockWechatShortcutText).parent().children()[1]
    lock_wechat_button.click_input()
    settings.child_window(**Panes.ChangeShortcutPane).click_input()
    time.sleep(1)
    pyautogui.hotkey(*shortcuts)
    confirm_button=settings.child_window(**Buttons.ConfirmButton) 
    confirm_button.click_input()
    if close_settings_window:
        settings.close()

def Change_send_message_shortcut(shortcuts:str='Enter',wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信修改微信设置中发送消息的快捷键。\n
    Args:
        shortcuts:\t快捷键键位名称,发送消息的快捷键只有Enter与ctrl+enter。\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    shortcut=settings.child_window(**TabItems.ShortCutTabItem)
    shortcut.click_input()
    message_combo_button=settings.child_window(**Texts.SendMessageShortcutText).parent().children()[1]
    message_combo_button.click_input()
    message_combo=settings.child_window(class_name='ComboWnd')
    if shortcuts=='Enter':
        listitem=message_combo.child_window(control_type='ListItem',found_index=0)
        listitem.click_input()
    else:
        listitem=message_combo.child_window(control_type='ListItem',found_index=1)
        listitem.click_input()
    if close_settings_window:
        settings.close()

def Shortcut_default(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True,close_settings_window:bool=True):
    '''
    该函数用来PC微信将快捷键恢复为默认设置。\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        close_settings_window:\t任务完成后是否关闭设置界面窗口,默认关闭\n
    '''
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    shortcut=settings.child_window(**TabItems.ShortCutTabItem)
    shortcut.click_input()
    default_button=settings.child_window(**Buttons.RestoreDefaultSettingsButton)
    default_button.click_input()
    print('已恢复快捷键为默认设置')
    if close_settings_window:
        settings.close()

def pin_friend(friend:str,state:str='open',search_pages:int=5,wechat_path=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来将好友在会话内置顶或取消置顶\n
    Args:
        friend:\t好友备注。\n
        state:取值为open或close,默认值为open,用来决定置顶或取消置顶好友,state为open时执行置顶操作,state为close时执行取消置顶操作\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    choices=['open','close']
    if state not in choices:
        raise WrongParameterError
    main_window,chat_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages) 
    Tool_bar=chat_window.child_window(found_index=1,title='',control_type='ToolBar')
    Pinbutton=Tool_bar.child_window(**Buttons.PinButton)
    if Pinbutton.exists():
        if state=='open':
            Pinbutton.click_input()
        if state=='close':
            print(f"好友'{friend}'未被置顶,无需取消置顶!")
    else:
        Cancelpinbutton=Tool_bar.child_window(**Buttons.CancelPinButton)
        if state=='open':
            print(f"好友'{friend}'已被置顶,无需置顶!")
        if state=='close':
            Cancelpinbutton.click_input()
    main_window.click_input()
    if close_wechat:
        main_window.close()
    
def mute_friend_notifications(friend:str,state:str='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来开启或关闭好友的消息免打扰\n
    Args:
        friend:好友备注\n
        state:取值为open或close,默认值为open,用来决定开启或关闭好友的消息免打扰设置,state为open时执行开启消息免打扰操作,state为close时执行关闭消息免打扰操作\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    choices=['open','close']
    if state not in choices:
        raise WrongParameterError
    friend_settings_window,main_window=Tools.open_friend_settings(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    mute_checkbox=friend_settings_window.child_window(**CheckBoxes.MuteNotificationsCheckBox)
    if mute_checkbox.get_toggle_state():
        if state=='open':
            print(f"好友'{friend}'的消息免打扰已开启,无需再开启消息免打扰!")
        if state=='close':
            mute_checkbox.click_input()
        friend_settings_window.close()
        if close_wechat:
            main_window.click_input()  
            main_window.close()
    else:
        if state=='open':
            mute_checkbox.click_input()
        if state=='close':
            print(f"好友'{friend}'的消息免打扰未开启,无需再关闭消息免打扰!") 
        friend_settings_window.close()
        if close_wechat:
            main_window.click_input()  
            main_window.close()
    
def sticky_friend_on_top(friend:str,state:str='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来开启或关闭好友的聊天置顶\n
    Args:
        friend:\t好友备注\n 
        state:取值为open或close,默认值为open,用来决定开启或关闭好友的聊天置顶设置,state为open时执行开启聊天置顶操作,state为close时执行关闭消息免打扰操作\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    choices=['open','close']
    if state not in choices:
        raise WrongParameterError
    friend_settings_window,main_window=Tools.open_friend_settings(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    sticky_on_top_checkbox=friend_settings_window.child_window(**CheckBoxes.StickyonTopCheckBox)
    if sticky_on_top_checkbox.get_toggle_state():
        if state=='open':
            print(f"好友'{friend}'的置顶聊天已开启,无需再设为置顶聊天")
        if state=='close':
            sticky_on_top_checkbox.click_input()
        friend_settings_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close()
    else:
        if state=='open':
            sticky_on_top_checkbox.click_input()
        if state=='close':
            print(f"好友'{friend}'的置顶聊天未开启,无需再取消置顶聊天")
        friend_settings_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close()
    
def clear_friend_chat_history(friend:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    ''' 
    该函数用来清空与好友的聊天记录\n
    Args:
        friend:\t好友备注\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    
    '''
    friend_settings_window,main_window=Tools.open_friend_settings(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    clear_chat_history_button=friend_settings_window.child_window(**Buttons.ClearChatHistoryButton)
    clear_chat_history_button.click_input()
    confirm_button=main_window.child_window(**Buttons.ConfirmEmptyChatHistoryButon)
    confirm_button.click_input()
    if close_wechat:
        main_window.close()
    
        
def delete_friend(friend:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    ''' 
    该函数用来删除好友\n
    Args:
        friend:好友备注\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path\t:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    menu,friend_settings_window,main_window=Tools.open_friend_settings_menu(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    delete_friend_item=menu.child_window(**MenuItems.DeleteMenuItem)
    delete_friend_item.click_input()
    confirm_window=friend_settings_window.child_window(**Panes.ConfirmPane)
    confirm_buton=confirm_window.child_window(**Buttons.DeleteButton)
    confirm_buton.click_input()
    time.sleep(1)
    if close_wechat:
        main_window.close()
    
def add_new_friend(phone_number:str=None,wechat_number:str=None,request_content:str=None,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来添加新朋友\n
    Args:
        phone_number:\t手机号\n
        wechat_number:\t微信号\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    注意:手机号与微信号至少要有一个!\n
    '''
    desktop=Desktop(**Independent_window.Desktop)
    main_window=Tools.open_contacts(wechat_path,is_maximize=is_maximize)
    add_friend_button=main_window.child_window(**Buttons.AddNewFriendButon)
    add_friend_button.click_input()
    search_new_friend_bar=main_window.child_window(**Main_window.SearchNewFriendBar)
    search_new_friend_bar.click_input()
    if phone_number and not wechat_number:
        Systemsettings.copy_text_to_windowsclipboard(phone_number)
        pyautogui.hotkey('ctrl','v')
    elif wechat_number and phone_number:
        Systemsettings.copy_text_to_windowsclipboard(wechat_number)
        pyautogui.hotkey('ctrl','v')
    elif not phone_number and wechat_number:
        Systemsettings.copy_text_to_windowsclipboard(wechat_number)
        pyautogui.hotkey('ctrl','v')
    else:
        if close_wechat:
            main_window.close()
        raise NoWechat_number_or_Phone_numberError
    search_new_friend_result=main_window.child_window(**Main_window.SearchNewFriendResult)
    search_new_friend_result.child_window(**Texts.SearchContactsResult).click_input()
    time.sleep(1.5)
    profile_pane=desktop.window(**Independent_window.ContactProfileWindow)
    add_to_contacts=profile_pane.child_window(**Buttons.AddToContactsButton)
    if add_to_contacts.exists():
        add_to_contacts.click_input()
        add_friend_request_window=main_window.child_window(**Main_window.AddFriendRequestWindow)
        if add_friend_request_window.exists():
            if request_content:
                request_content_edit=add_friend_request_window.child_window(**Edits.RequestContentEdit)
                request_content_edit.click_input()
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('backspace')
                request_content_edit=add_friend_request_window.child_window(title='',control_type='Edit',found_index=0)
                Systemsettings.copy_text_to_windowsclipboard(request_content)
                pyautogui.hotkey('ctrl','v')
                confirm_button=add_friend_request_window.child_window(**Buttons.ConfirmButton)
                confirm_button.click_input()
                time.sleep(3)
                if language=='简体中文':
                    cancel_button=main_window.child_window(title='取消',control_type='Button',found_index=0)
                if language=='英文':
                    cancel_button=main_window.child_window(title='Cancel',control_type='Button',found_index=0)
                cancel_button.click_input()
                if close_wechat:
                    main_window.close()
            else:
                confirm_button=add_friend_request_window.child_window(**Buttons.ConfirmButton)
                confirm_button.click_input()
                time.sleep(3)
                if language=='简体中文':
                    cancel_button=main_window.child_window(title='取消',control_type='Button',found_index=0)
                if language=='英文':
                    cancel_button=main_window.child_window(title='Cancel',control_type='Button',found_index=0)
                cancel_button.click_input()
                if close_wechat:
                    main_window.close() 
    else:
        time.sleep(1)
        profile_pane.close()
        if close_wechat:
            main_window.close()
        raise AlreadyInContactsError
        
def change_friend_remark_and_tag(friend:str,remark:str,tag:str=None,description:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来修改好友备注和标签\n
    Args:
        friend:\t好友备注\n
        tag:标签名\n
        description:描述\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    if friend==remark:
        raise SameNameError
    menu,friend_settings_window,main_window=Tools.open_friend_settings_menu(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    change_remark=menu.child_window(**MenuItems.EditContactMenuItem)
    change_remark.click_input()
    sessionchat=friend_settings_window.child_window(**Windows.EditContactWindow)
    remark_edit=sessionchat.child_window(title=friend,control_type='Edit')
    remark_edit.click_input()
    pyautogui.hotkey('ctrl','a')
    pyautogui.press('backspace')
    remark_edit=sessionchat.child_window(control_type='Edit',found_index=0)
    Systemsettings.copy_text_to_windowsclipboard(remark)
    pyautogui.hotkey('ctrl','v')
    if tag:
        tag_set=sessionchat.child_window(**Buttons.TagEditButton)
        tag_set.click_input()
        confirm_pane=main_window.child_window(**Main_window.SetTag)
        edit=confirm_pane.child_window(**Edits.TagEdit)
        edit.click_input()
        Systemsettings.copy_text_to_windowsclipboard(tag)
        pyautogui.hotkey('ctrl','v')
        confirm_pane.child_window(**Buttons.ConfirmButton).click_input()
    if description:
        description_edit=sessionchat.child_window(control_type='Edit',found_index=1)
        description_edit.click_input()
        pyautogui.hotkey('ctrl','a')
        pyautogui.press('backspace')
        Systemsettings.copy_text_to_windowsclipboard(description)
        pyautogui.hotkey('ctrl','v')
    confirm=sessionchat.child_window(**Buttons.ConfirmButton)
    confirm.click_input()
    friend_settings_window.close()
    main_window.click_input()
    if close_wechat:
        main_window.close()


def add_friend_to_blacklist(friend:str,state:str='open',search_pages:int=0,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来将好友添加至黑名单\n
    Args:
        friend:\t好友备注\n
        state:\t取值为open或close,默认值为open,用来决定是否将好友添加至黑名单,state为open时执行将好友加入黑名单操作,state为close时执行将好友移出黑名单操作。\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为0,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    choices=['open','close']
    if state not in choices:
        raise WrongParameterError
    menu,friend_settings_window,main_window=Tools.open_friend_settings_menu(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    blacklist=menu.child_window(**MenuItems.BlockMenuItem)
    if blacklist.exists():
        if state=='open':
            blacklist.click_input()
            confirm_window=friend_settings_window.child_window(**Panes.ConfirmPane)
            confirm_buton=confirm_window.child_window(**Buttons.ConfirmButton)
            confirm_buton.click_input()
        if state=='close':
            print(f'好友"{friend}"未处于黑名单中,无需移出黑名单!')
        friend_settings_window.close()
        main_window.click_input() 
        if close_wechat:
            main_window.close()
    else:
        move_out_of_blacklist=menu.child_window(**MenuItems.UnBlockMenuItem)
        if state=='close':
            move_out_of_blacklist.click_input()
        if state=='open':
            print(f'好友"{friend}"已位于黑名单中,无需添加至黑名单!')
        friend_settings_window.close()
        main_window.click_input() 
        if close_wechat:
            main_window.close()
           
def set_friend_as_star_friend(friend:str,state:str='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来将好友设置为星标朋友\n
    Args:
        friend:好友备注。\n
        state:\t取值为open或close,默认值为open,用来决定是否将好友设为星标朋友,state为open时执行将好友设为星标朋友操作,state为close时执行不再将好友设为星标朋友\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    choices=['open','close']
    if state not in choices:
        raise WrongParameterError
    menu,friend_settings_window,main_window=Tools.open_friend_settings_menu(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    star=menu.child_window(**MenuItems.StarMenuItem)
    if star.exists():
        if state=='open':
            star.click_input()
        if state=='close':
            print(f"好友'{friend}'未被设为星标朋友,无需操作！")
        friend_settings_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close()
    else:
        cancel_star=menu.child_window(**MenuItems.UnStarMenuItem)
        if state=='open':
            print(f"好友'{friend}'已被设为星标朋友,无需操作！")
        if state=='close':
            cancel_star.click_input()
        friend_settings_window.close()
        main_window.click_input() 
        if close_wechat: 
            main_window.close()
                    
def change_friend_privacy(friend:str,privacy:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来修改好友权限\n
    Args:
        friend:好友备注。\n
        privacy:好友权限,共有：'仅聊天',"聊天、朋友圈、微信运动等",'不让他（她）看',"不看他（她）"四种\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
    '''
    privacy_rights=['仅聊天',"聊天、朋友圈、微信运动等",'不让他（她）看',"不看他（她）"]
    if privacy not in privacy_rights:
        raise PrivacyNotCorrectError
    menu,friend_settings_window,main_window=Tools.open_friend_settings_menu(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    privacy_button=menu.child_window(**MenuItems.SetPrivacyMenuItem)
    privacy_button.click_input()
    privacy_window=friend_settings_window.child_window(**Windows.EditPrivacyWindow)
    if privacy=="仅聊天":
        only_chat=privacy_window.child_window(**CheckBoxes.ChatsOnlyCheckBox)
        if only_chat.get_toggle_state():
            privacy_window.close()
            friend_settings_window.close()
            main_window.click_input()
            if close_wechat:
                main_window.close()
            raise HaveBeenSetChatonlyError(f"好友'{friend}'权限已被设置为仅聊天")
        else:
            only_chat.click_input()
            sure_button=privacy_window.child_window(**Buttons.ConfirmButton)
            sure_button.click_input()
            friend_settings_window.close()
            if close_wechat:
                main_window.close()
    elif  privacy=="聊天、朋友圈、微信运动等":
        open_chat=privacy_window.child_window(**CheckBoxes.OpenChatCheckBox)
        if open_chat.get_toggle_state():
            privacy_window.close()
            friend_settings_window.close()
            main_window.click_input()
            if close_wechat:
                main_window.close()
        else:
            open_chat.click_input()
            sure_button=privacy_window.child_window(**Buttons.ConfirmButton)
            sure_button.click_input()
            friend_settings_window.close()
            if close_wechat:
                main_window.close()
    else:
        if privacy=='不让他（她）看':
            unseen_to_him=privacy_window.child_window(title="",control_type='CheckBox',found_index=0)
            if unseen_to_him.exists():
                if unseen_to_him.get_toggle_state():
                    privacy_window.close()
                    friend_settings_window.close()
                    main_window.click_input()
                    if close_wechat:
                        main_window.close()
                    raise HaveBeenSetUnseentohimError(f"好友 {friend}权限已被设置为不让他（她）看")
                else:
                    unseen_to_him.click_input()
                    sure_button=privacy_window.child_window(**Buttons.ConfirmButton)
                    sure_button.click_input()
                    friend_settings_window.close()
                    if close_wechat:
                        main_window.close()
            else:
                privacy_window.close()
                friend_settings_window.close()
                main_window.click_input()
                if close_wechat:
                    main_window.close()
                raise HaveBeenSetChatonlyError(f"好友 {friend}已被设置为仅聊天,无法设置为不让他（她）看\n若需将其设置为不让他（她）看,请先将好友设置为：\n聊天、朋友圈、微信运动等")
        if privacy=="不看他（她）":
            dont_see_him=privacy_window.child_window(title="",control_type='CheckBox',found_index=1)
            if dont_see_him.exists():
                if dont_see_him.get_toggle_state():
                    privacy_window.close()
                    friend_settings_window.close()
                    main_window.click_input()
                    if close_wechat:
                        main_window.close()
                    raise HaveBeenSetDontseehimError(f"好友 {friend}权限已被设置为不看他（她）")
                else:
                    dont_see_him.click_input()
                    sure_button=privacy_window.child_window(**Buttons.ConfirmButton)
                    sure_button.click_input()
                    friend_settings_window.close()
                    if close_wechat:
                        main_window.close()  
            else:
                privacy_window.close()
                friend_settings_window.close()
                main_window.click_input()
                if close_wechat:
                    main_window.close()
                raise HaveBeenSetChatonlyError(f"好友 {friend}已被设置为仅聊天,无法设置为不看他（她）\n若需将其设置为不看他（她）,请先将好友设置为：\n聊天、朋友圈、微信运动等")
            
def get_friend_wechat_number(friend:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数根据微信备注获取单个好友的微信号\n
    Args:
        friend:\t好友备注。\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
    '''
    profile_window,main_window=Tools.open_friend_profile(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    wechat_number=profile_window.child_window(control_type='Text',found_index=4).window_text()
    profile_window.close()
    if close_wechat:
        main_window.close()
    return wechat_number

def get_friends_wechat_numbers(friends:list[str],wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数根据微信备注获取多个好友微信号\n
    Args:
        friends:\t所有待获取微信号的好友的备注列表。\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    wechat_numbers=[]
    for friend in friends:
        profile_window,main_window=Tools.open_friend_profile(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize)
        wechat_number=profile_window.child_window(control_type='Text',found_index=4).window_text()
        wechat_numbers.append(wechat_number)
        profile_window.close()
    wechat_numbers=dict(zip(friends,wechat_numbers)) 
    if close_wechat:       
        main_window.close()
    return wechat_numbers 

def share_contact(friend:str,others:list[str],search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来推荐好友给其他人\n
    Args:
        friend:\t被推荐好友备注\n
        others:\t推荐人备注列表\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    menu,friend_settings_window,main_window=Tools.open_friend_settings_menu(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
  
    share_contact=menu.child_window(**MenuItems.ShareContactMenuItem)
    share_contact.click_input()
    select_contact_window=main_window.child_window(**Main_window.SelectContactWindow)
    if len(others)>1:
        multi=select_contact_window.child_window(**Buttons.MultiSelectButton)
        multi.click_input()
        send=select_contact_window.child_window(**Buttons.SendRespectivelyButton)
    else:
        send=select_contact_window.child_window(**Buttons.SendButton)
    search=select_contact_window.child_window(**Edits.SearchEdit)
    for other_friend in others:
        search.click_input()
        Systemsettings.copy_text_to_windowsclipboard(other_friend)
        pyautogui.hotkey('ctrl','v')
        time.sleep(0.5)
        pyautogui.press('enter')
        pyautogui.hotkey('ctrl','a')
        pyautogui.press('backspace')
        time.sleep(0.5)
    send.click_input()
    friend_settings_window.close()
    if close_wechat:
        main_window.close()

def pin_group(group_name:str,state:str='open',search_pages:int=5,wechat_path=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来将群聊在会话内置顶或取消置顶\n
    Args:
        group_name:\t群聊备注。\n
        state:取值为open或close,默认值为open,用来决定置顶或取消置顶群聊,state为open时执行置顶操作,state为close时执行取消置顶操作\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    choices=['open','close']
    if state not in choices:
        raise WrongParameterError
    main_window,chat_window=Tools.open_dialog_window(friend=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages) 
    Tool_bar=chat_window.child_window(found_index=1,title='',control_type='ToolBar')
    Pinbutton=Tool_bar.child_window(**Buttons.PinButton)
    if Pinbutton.exists():
        if state=='open':
            Pinbutton.click_input()
        if state=='close':
            print(f"群聊'{group_name}'未被置顶,无需取消置顶!")
    else:
        Cancelpinbutton=Tool_bar.child_window(**Buttons.CancelPinButton)
        if state=='open':
            print(f"群聊'{group_name}'已被置顶,无需置顶!")
        if state=='close':
            Cancelpinbutton.click_input()
    main_window.click_input()
    if close_wechat:
        main_window.close()

def create_group_chat(friends:list[str],group_name:str=None,wechat_path:str=None,is_maximize:bool=True,messages:list=[str],close_wechat:bool=True):
    '''
    该函数用来新建群聊\n
    Args:
        friends:\t新群聊的好友备注列表。\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
        messages:\t建群后是否发送消息,messages非空列表,在建群后会发送消息\n
    '''
    if len(friends)<=2:
        raise CantCreateGroupError
    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    cerate_group_chat_button=main_window.child_window(title="发起群聊",control_type="Button")
    cerate_group_chat_button.click_input()
    Add_member_window=main_window.child_window(**Main_window.AddMemberWindow)
    for member in friends:
        search=Add_member_window.child_window(**Edits.SearchEdit)
        search.click_input()
        Systemsettings.copy_text_to_windowsclipboard(member)
        pyautogui.hotkey('ctrl','v')
        pyautogui.press("enter")
        pyautogui.press('backspace')
        time.sleep(2)
    confirm=Add_member_window.child_window(**Buttons.CompleteButton)
    confirm.click_input()
    time.sleep(10)
    if messages:
        group_edit=main_window.child_window(**Main_window.CurrentChatWindow)
        for message in message:
            Systemsettings.copy_text_to_windowsclipboard(message)
            pyautogui.hotkey('ctrl','v')
            pyautogui.hotkey('alt','s',_pause=False)
    if group_name:
        chat_message=main_window.child_window(**Buttons.ChatMessageButton)
        chat_message.click_input()
        group_settings_window=main_window.child_window(**Main_window.GroupSettingsWindow)
        change_group_name_button=group_settings_window.child_window(**Buttons.ChangeGroupNameButton)
        change_group_name_button.click_input()
        pyautogui.hotkey('ctrl','a')
        pyautogui.press('backspace')
        change_group_name_edit=group_settings_window.child_window(**Edits.EditWnd)
        change_group_name_edit.click_input()
        Systemsettings.copy_text_to_windowsclipboard(group_name)
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('enter')
        group_settings_window.close()
    if close_wechat:    
        main_window.close()

def change_group_name(group_name:str,change_name:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来修改群聊名称\n
    Args:
        group_name:群聊名称\n
        change_name:待修改的名称\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
    '''
    if group_name==change_name:
        raise SameNameError(f'待修改的群名需与先前的群名不同才可修改！')
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    ChangeGroupNameWarnText=group_chat_settings_window.child_window(**Texts.ChangeGroupNameWarnText)
    if ChangeGroupNameWarnText.exists():
        group_chat_settings_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close()
        raise NoPermissionError(f"你不是'{group_name}'的群主或管理员,无权修改群聊名称")
    else:
        change_group_name_button=group_chat_settings_window.child_window(**Buttons.ChangeGroupNameButton)
        change_group_name_button.click_input()
        change_group_name_edit=group_chat_settings_window.child_window(**Edits.EditWnd)
        change_group_name_edit.click_input()
        time.sleep(0.5)
        pyautogui.press('end')
        time.sleep(0.5)
        pyautogui.press('backspace',presses=35,_pause=False)
        time.sleep(0.5)
        Systemsettings.copy_text_to_windowsclipboard(change_name)
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('enter')
        group_chat_settings_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close()

def change_my_nickname_in_group(group_name:str,my_nickname:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来修改我在本群的昵称\n
    Args:
        group_name:\t群聊名称\n
        my_nickname:\t待修改昵称\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    change_my_nickname_button=group_chat_settings_window.child_window(**Buttons.MyNicknameInGroupButton)
    change_my_nickname_button.click_input() 
    change_my_nickname_edit=group_chat_settings_window.child_window(**Edits.EditWnd)
    change_my_nickname_edit.click_input()
    time.sleep(0.5)
    pyautogui.press('end')
    time.sleep(0.5)
    pyautogui.press('backspace',presses=35,_pause=False)
    time.sleep(0.5)
    Systemsettings.copy_text_to_windowsclipboard(my_nickname)
    pyautogui.hotkey('ctrl','v')
    pyautogui.press('enter')
    group_chat_settings_window.close()
    main_window.click_input()
    if close_wechat:
        main_window.close()

def change_group_remark(group_name:str,group_remark:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来修改群聊备注\n
    Args:
        group_name:\t群聊名称\n
        group_remark:\t群聊备注\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    change_group_remark_button=group_chat_settings_window.child_window(**Buttons.RemarkButton)
    change_group_remark_button.click_input()
    change_group_remark_edit=group_chat_settings_window.child_window(**Edits.EditWnd)
    change_group_remark_edit.click_input()
    time.sleep(0.5)
    pyautogui.press('end')
    time.sleep(0.5)
    pyautogui.press('backspace',presses=35,_pause=False)
    time.sleep(0.5)
    Systemsettings.copy_text_to_windowsclipboard(group_remark)
    pyautogui.hotkey('ctrl','v')
    pyautogui.press('enter')
    group_chat_settings_window.close()
    main_window.click_input()
    if close_wechat:
        main_window.close()

def show_group_members_nickname(group_name:str,state:str='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来开启或关闭显示群聊成员名称\n
    Args:
        group_name:\t群聊名称\n
        state:\t取值为open或close,默认值为open,用来决定是否显示群聊成员名称,state为open时执行将开启显示群聊成员名称操作,state为close时执行关闭显示群聊成员名称\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    choices=['open','close']
    if state not in choices:
        raise WrongParameterError
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    show_group_members_nickname_button=group_chat_settings_window.child_window(**CheckBoxes.OnScreenNamesCheckBox)
    if not show_group_members_nickname_button.get_toggle_state():
        if state=='open':
            show_group_members_nickname_button.click_input()
        if state=='close':
            print(f"显示群成员昵称功能未开启,无需关闭!")
        group_chat_settings_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close()
    else:
        if state=='open':
            print(f"显示群成员昵称功能已开启,无需再开启!")
        if state=='close':
            show_group_members_nickname_button.click_input()
        group_chat_settings_window.close()
        main_window.click_input()
        main_window.close()


def mute_group_notifications(group_name:str,state:str='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来开启或关闭群聊消息免打扰\n
    Args:
        group_name:\t群聊名称\n
        state:\t取值为open或close,默认值为open,用来决定是否对该群开启消息免打扰,state为open时执行将开启消息免打扰操作,state为close时执行关闭消息免打扰\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    choices=['open','close']
    if state not in choices:
        raise WrongParameterError
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    mute_checkbox=group_chat_settings_window.child_window(**CheckBoxes.MuteNotificationsCheckBox)
    if mute_checkbox.get_toggle_state():
        if state=='open':
            print(f"群聊'{group_name}'的消息免打扰已开启,无需再开启消息免打扰！")
        if state=='close':
            mute_checkbox.click_input()
        group_chat_settings_window.close()
        main_window.click_input()
        if close_wechat:  
            main_window.close()
        
    else:
        if state=='open':
            mute_checkbox.click_input()
        if state=='close':
            print(f"群聊'{group_name}'的消息免打扰未开启,无需再关闭消息免打扰！")
        group_chat_settings_window.close()
        main_window.click_input()
        if close_wechat:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            main_window.close() 

def sticky_group_on_top(group_name:str,state='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来将微信群聊聊天置顶或取消聊天置顶\n
    Args:
        group_name:\t群聊名称\n
        state:\t取值为open或close,默认值为open,用来决定是否将该群聊聊天置顶,state为open时将该群聊聊天置顶,state为close时取消该群聊聊天置顶\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    choices=['open','close']
    if state not in choices:
        raise WrongParameterError
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    sticky_on_top_checkbox=group_chat_settings_window.child_window(**CheckBoxes.StickyonTopCheckBox)
    if not sticky_on_top_checkbox.get_toggle_state():
        if state=='open':
            sticky_on_top_checkbox.click_input()
        if state=='close':
            print(f"群聊'{group_name}'的置顶聊天未开启,无需再关闭置顶聊天!")
        group_chat_settings_window.close()
        main_window.click_input() 
        if close_wechat: 
            main_window.close()
    else:
        if state=='open':
            print(f"群聊'{group_name}'的置顶聊天已开启,无需再设置为置顶聊天!")
        if state=='close':
            sticky_on_top_checkbox.click_input()
        group_chat_settings_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close() 
         
def save_group_to_contacts(group_name:str,state:str='open',search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来将群聊保存或取消保存到通讯录\n
    Args:
        group_name:\t群聊名称\n
        state:\t取值为open或close,默认值为open,用来,state为open时将该群聊保存至通讯录,state为close时取消该群保存到通讯录\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    choices=['open','close']
    if state not in choices:
        raise WrongParameterError
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    save_to_contacts_checkbox=group_chat_settings_window.child_window(**CheckBoxes.SavetoContactsCheckBox)
    if not save_to_contacts_checkbox.get_toggle_state():
        if state=='open':
            save_to_contacts_checkbox.click_input()
        if state=='close':
            print(f"群聊'{group_name}'未保存到通讯录,无需取消保存到通讯录！")
        group_chat_settings_window.close()
        main_window.click_input() 
        if close_wechat: 
            main_window.close()
    else:
        if state=='open':
            print(f"群聊'{group_name}'已保存到通讯录,无需再保存到通讯录")
        if state=='close':
            save_to_contacts_checkbox.click_input()
        group_chat_settings_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close()  

def clear_group_chat_history(group_name:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来清空群聊聊天记录\n
    Args:
        group_name:群聊名称\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    clear_chat_history_button=group_chat_settings_window.child_window(**Buttons.ClearChatHistoryButton)
    clear_chat_history_button.click_input()
    confirm_button=main_window.child_window(**Buttons.ConfirmEmptyChatHistoryButon)
    confirm_button.click_input()
    if close_wechat:
        main_window.close()

def quit_group_chat(group_name:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来退出微信群聊\n
    Args:
        group_name:\t群聊名称\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    quit_group_chat_button=group_chat_settings_window.child_window(**Buttons.QuitGroupButton)
    quit_group_chat_button.click_input()
    quit_button=main_window.child_window(**Buttons.ConfirmQuitGroupButton)
    quit_button.click_input()
    if close_wechat:
        main_window.close()

def invite_others_to_group(group_name:str,friends:list[str],search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来邀请他人至群聊\n
    Args:
        group_name:\t群聊名称\n
        friends:\t所有待邀请好友备注列表\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    add=group_chat_settings_window.child_window(title='',control_type="Button",found_index=1)
    add.click_input()
    Add_member_window=main_window.child_window(**Main_window.AddMemberWindow)
    for member in friends:
        search=Add_member_window.child_window(**Edits.SearchEdit)
        search.click_input()
        Systemsettings.copy_text_to_windowsclipboard(member)
        pyautogui.hotkey('ctrl','v')
        pyautogui.press("enter")
        pyautogui.press('backspace')
        time.sleep(2)
    confirm=Add_member_window.child_window(**Buttons.CompleteButton)
    confirm.click_input()
    group_chat_settings_window.close()
    if close_wechat:
        main_window.close()

def remove_friend_from_group(group_name:str,friends:list[str],search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来将群成员移出群聊\n
    Args:
        group_name:\t群聊名称\n
        friends:\t所有移出群聊的成员备注列表\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    delete=group_chat_settings_window.child_window(title='',control_type="Button",found_index=2)
    if not delete.exists():
        group_chat_settings_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close()
        raise NoPermissionError(f"你不是'{group_name}'的群主或管理员,无权将好友移出群聊")
    else:
        delete.click_input()
        delete_member_window=main_window.child_window(**Main_window.DeleteMemberWindow)
        for member in friends:
            search=delete_member_window.child_window(**Edits.SearchEdit)
            search.click_input()
            Systemsettings.copy_text_to_windowsclipboard(member)
            pyautogui.hotkey('ctrl','v')
            button=delete_member_window.child_window(title=member,control_type='Button')
            button.click_input()
        confirm=delete_member_window.child_window(**Buttons.CompleteButton)
        confirm.click_input()
        confirm_dialog_window=delete_member_window.child_window(class_name='ConfirmDialog',framework_id='Win32')
        delete=confirm_dialog_window.child_window(**Buttons.DeleteButton)
        delete.click_input()
        group_chat_settings_window.close()
        if close_wechat:
            main_window.close()

def add_friend_from_group(group_name:str,friend:str,request_content:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来添加群成员为好友\n
    Args:
        group_name:\t群聊名称\n
        friend:\t待添加群聊成员群聊中的名称\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    search=group_chat_settings_window.child_window(**Edits.SearchGroupMemeberEdit)
    search.click_input()
    Systemsettings.copy_text_to_windowsclipboard(friend)
    pyautogui.hotkey('ctrl','v')
    friend_butotn=group_chat_settings_window.child_window(title=friend,control_type='Button',found_index=1)
    friend_butotn.double_click_input()
    contact_window=group_chat_settings_window.child_window(class_name='ContactProfileWnd',framework_id="Win32")
    add_to_contacts_button=contact_window.child_window(**Buttons.AddToContactsButton)
    if add_to_contacts_button.exists():
        add_to_contacts_button.click_input()
        add_friend_request_window=main_window.child_window(**Main_window.AddFriendRequestWindow)
        request_content_edit=add_friend_request_window.child_window(**Edits.RequestContentEdit)
        request_content_edit.click_input()
        pyautogui.hotkey('ctrl','a')
        pyautogui.press('backspace')
        request_content_edit=add_friend_request_window.child_window(title='',control_type='Edit',found_index=0)
        Systemsettings.copy_text_to_windowsclipboard(request_content)
        pyautogui.hotkey('ctrl','v')
        confirm_button=add_friend_request_window.child_window(**Buttons.ConfirmButton)
        confirm_button.click_input()
        time.sleep(5)
        if close_wechat:
            main_window.close()
    else:
        group_chat_settings_window.close()
        if close_wechat:
            main_window.close()
        raise AlreadyInContactsError(f"好友'{friend}'已在通讯录中,无需通过该群聊添加！")
       
def create_an_new_note(content:str=None,file:str=None,wechat_path:str=None,is_maximize:bool=True,content_first:bool=True,close_wechat:bool=True):
    '''
    该函数用来创建一个新笔记\n
    Args:
        content:\t笔记文本内容\n
        file:\t笔记文件内容\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        content_first:\t先写文本内容还是先放置文件\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    main_window=Tools.open_collections(wechat_path=wechat_path,is_maximize=is_maximize)
    create_an_new_note_button=main_window.child_window(**Buttons.CerateNewNote)
    create_an_new_note_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    note_window=desktop.window(**Independent_window.NoteWindow)
    if file and content:
        if content_first:
            edit_note=note_window.child_window(control_type='Edit',found_index=0)
            edit_note.click_input()
            Systemsettings.copy_text_to_windowsclipboard(content)
            pyautogui.hotkey('ctrl','v')
            if Systemsettings.is_empty_file(file):
                note_window.close()
                if close_wechat:
                    main_window.close()
                raise EmptyFileError(f"输入的路径下的文件为空!请重试")
            elif Systemsettings.is_dirctory(file):
                files=Systemsettings.get_files_in_folder(file)
                if len(files)>10:
                    print("笔记中最多只能存放10个文件,已为你存放前10个文件")
                    files=files[0:10]
                Systemsettings.copy_files_to_windowsclipboard(files)
                edit_note.click_input()
                pyautogui.hotkey('ctrl','v',_pause=False)
            else:
                Systemsettings.copy_file_to_windowsclipboard(file)
                pyautogui.press('enter')
                edit_note.click_input()
                pyautogui.hotkey('ctrl','v',_pause=False)
            pyautogui.hotkey('ctrl','s') 
            note_window.close()
            if close_wechat:
                main_window.close()
        if not content_first:
            edit_note=note_window.child_window(control_type='Edit',found_index=0)
            edit_note.click_input()
            if Systemsettings.is_empty_file(file):
                note_window.close()
                if close_wechat:
                    main_window.close()
                raise EmptyFileError(f"输入的路径下的文件为空!请重试")
            elif Systemsettings.is_dirctory(file):
                files=Systemsettings.get_files_in_folder(file)
                if len(files)>10:
                    print("笔记中最多只能存放10个文件,已为你存放前10个文件")
                    files=files[0:10]
                Systemsettings.copy_files_to_windowsclipboard(files)
                pyautogui.hotkey('ctrl','v',_pause=False)
            else:
                Systemsettings.copy_file_to_windowsclipboard(file)
                pyautogui.hotkey('ctrl','v',_pause=False)
            pyautogui.press('enter')
            edit_note.click_input()
            Systemsettings.copy_text_to_windowsclipboard(content)
            pyautogui.hotkey('ctrl','v')
            pyautogui.hotkey('ctrl','s')
            note_window.close()
            if close_wechat:
                main_window.close()
    if  not file and content:
        edit_note=note_window.child_window(control_type='Edit',found_index=0)
        edit_note.click_input()
        Systemsettings.copy_text_to_windowsclipboard(content)
        pyautogui.hotkey('ctrl','v')
        note_window.close()
        pyautogui.hotkey('ctrl','s')
        if close_wechat:
            main_window.close()
    if file and not content:
        edit_note=note_window.child_window(control_type='Edit',found_index=0)
        edit_note.click_input()
        if Systemsettings.is_empty_file(file):
            note_window.close()
            if close_wechat:
                main_window.close()
            raise EmptyFileError(f"输入的路径下的文件为空!请重试")
        elif Systemsettings.is_dirctory(file):
            files=Systemsettings.get_files_in_folder(file)
            if len(files)>10:
                print("笔记中最多只能存放10个文件,已为你存放前10个文件")
                files=files[0:10]
            edit_note=note_window.child_window(control_type='Edit',found_index=0)
            Systemsettings.copy_files_to_windowsclipboard(files)
            pyautogui.hotkey('ctrl','v',_pause=False)
        else:
            edit_note=note_window.child_window(control_type='Edit',found_index=0)
            Systemsettings.copy_file_to_windowsclipboard(file)
            pyautogui.hotkey('ctrl','v',_pause=False)
        pyautogui.hotkey('ctrl','s')
        if close_wechat:
            main_window.close()
        time.sleep(5)
        note_window.close()
    if not file and not content:
        raise EmptyNoteError

def edit_group_notice(group_name:str,content:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来编辑群公告\n
    Args:
        group_name:\t群聊名称\n
        content:\t群公告内容\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat\t:任务结束后是否关闭微信,默认关闭\n
    '''
    group_chat_settings_window,main_window=Tools.open_group_settings(group_name=group_name,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    edit_group_notice_button=group_chat_settings_window.child_window(**Buttons.EditGroupNotificationButton)
    edit_group_notice_button.click_input()
    edit_group_notice_window=Tools.move_window_to_center(Window=Independent_window.GroupAnnouncementWindow)
    EditGroupNoticeWarnText=edit_group_notice_window.child_window(**Texts.EditGroupNoticeWarnText)
    if EditGroupNoticeWarnText.exists():
        edit_group_notice_window.close()
        main_window.click_input()
        if close_wechat:
            main_window.close()
        raise NoPermissionError(f"你不是'{group_name}'的群主或管理员,无权发布群公告")
    else:
        main_window.minimize()
        edit_board=edit_group_notice_window.child_window(control_type='Edit',found_index=0)
        if edit_board.window_text()!='':
            edit_button=edit_group_notice_window.child_window(**Buttons.EditButton)
            edit_button.click_input()
            time.sleep(1)
            pyautogui.hotkey('ctrl','a')
            pyautogui.press('backspace')
            Systemsettings.copy_text_to_windowsclipboard(content)
            pyautogui.hotkey('ctrl','v')
            confirm_button=edit_group_notice_window.child_window(**Buttons.CompleteButton)
            confirm_button.click_input()
            confirm_pane=edit_group_notice_window.child_window(**Panes.ConfirmPane)
            forward=confirm_pane.child_window(**Buttons.PublishButton)
            forward.click_input()
            time.sleep(2)
            main_window.click_input()
            if close_wechat:
                main_window.close()
        else:
            edit_board.click_input()
            time.sleep(1)
            pyautogui.hotkey('ctrl','a')
            pyautogui.press('backspace')
            Systemsettings.copy_text_to_windowsclipboard(content)
            pyautogui.hotkey('ctrl','v')
            confirm_button=edit_group_notice_window.child_window(**Buttons.CompleteButton)
            confirm_button.click_input()
            confirm_pane=edit_group_notice_window.child_window(**Panes.ConfirmPane)
            forward=confirm_pane.child_window(**Buttons.PublishButton)
            forward.click_input()
            time.sleep(2)
            main_window.click_input()
            if close_wechat:
                main_window.close()

def auto_reply_to_friend(friend:str,duration:str,content:str,save_chat_history:bool=False,capture_screen:bool=False,folder_path:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来实现类似QQ的自动回复某个好友的消息\n
    Args:
        friend:\t好友或群聊备注\n
        duration:\t自动回复持续时长,格式:'s','min','h',单位:s/秒,min/分,h/小时\n
        content:\t指定的回复内容,比如:自动回复[微信机器人]:您好,我当前不在,请您稍后再试。\n
        save_chat_history:\t是否保存自动回复时留下的聊天记录,若值为True该函数返回值为聊天记录json,否则该函数无返回值。\n
        capture_screen:\t是否保存聊天记录截图,默认值为False不保存。\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为5,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        folder_path:\t存放聊天记录截屏图片的文件夹路径\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    if save_chat_history and capture_screen and folder_path:#需要保存自动回复后的聊天记录截图时，可以传入一个自定义文件夹路径，不然保存在运行该函数的代码所在文件夹下
        #当给定的文件夹路径下的内容不是一个文件夹时
        if not Systemsettings.is_dirctory(folder_path):#
            raise NotFolderError(r'给定路径不是文件夹!无法保存聊天记录截图,请重新选择文件夹！')
    duration=match_duration(duration)#将's','min','h'转换为秒
    if not duration:#有SB不按照指定的时间格式输入,需要提前中断退出
        raise TimeNotCorrectError
    #打开好友的对话框,返回值为编辑消息框和主界面
    chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    #需要判断一下是不是公众号
    voice_call_button=main_window.child_window(**Buttons.VoiceCallButton)
    video_call_button=main_window.child_window(**Buttons.VideoCallButton)
    if not voice_call_button.exists():
        #公众号没有语音聊天按钮
        main_window.close()
        raise CantReplyToOfficialAccountError
    if video_call_button.exists() and voice_call_button.exists():
        type='好友'
    if not video_call_button.exists() and voice_call_button.exists():
        type='群聊'
        myname=main_window.child_window(control_type='Button',found_index=0).window_text()#自己的名字
    #####################################################################################
    chatList=main_window.child_window(**Main_window.FriendChatList)#聊天界面内存储所有信息的容器
    initial_last_message=Tools.pull_latest_message(chatList)[0]#刚打开聊天界面时的最后一条消息的内容 
    Systemsettings.copy_text_to_windowsclipboard(content)#复制回复内容到剪贴板
    Systemsettings.open_listening_mode(volume=False)#开启监听模式,此时电脑只要不断电不会息屏 
    count=0
    start_time=time.time()  
    while True:
        if time.time()-start_time<duration:
            newMessage,who=Tools.pull_latest_message(chatList)
            #消息列表内的最后一条消息(listitem)不等于刚打开聊天界面时的最后一条消息(listitem)
            #并且最后一条消息的发送者是好友时自动回复
            #这里我们判断的是两条消息(listitem)是否相等,不是文本是否相等,要是文本相等的话,对方一直重复发送
            #刚打开聊天界面时的最后一条消息的话那就一直不回复了
            if type=='好友':
                if newMessage!=initial_last_message and who==friend:
                    chat.click_input()
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    pyautogui.hotkey('alt','s',_pause=False)
                    count+=1  
            if type=='群聊':
                if newMessage!=initial_last_message and who!=myname:
                    chat.click_input()
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    pyautogui.hotkey('alt','s',_pause=False)
                    count+=1
        else:
            break
    if count:
        if save_chat_history:
            chat_history=get_chat_history(friend=friend,number=2*count,capture_screen=capture_screen,folder_path=folder_path,wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)  
            return chat_history
    Systemsettings.close_listening_mode()
    if close_wechat:
        main_window.close()

def tickle_friend(friend:str,maxSearchNum:int=50,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该方法用来拍一拍好友\n
    Args:
        friend:好友备注\n
        maxSearchNum:主界面找不到好友聊天记录时在聊天记录窗口内查找好友聊天信息时的最大查找次数,默认为20,如果历史信息比较久远,可以更大一些\n
        search_pages:在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏法搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
    '''
    def find_firend_buttons_in_chat_history(chatlist):
        if len(chatlist.children())==0:
            chat.close()
            main_window.close()
            raise NoChatHistoryError(f'你还未与{friend}聊天,只有互相聊天后才可以拍一拍哦！')
        else:
            top=chatlist.rectangle().top
            bottom=chatlist.rectangle().bottom
            chats=[chat for chat in chatlist.children() if chat.descendants(control_type='Button',title=friend)]
            buttons=[chat.descendants(control_type='Button',title=friend)[0] for chat in chats]
            visible_buttons=[button for button in buttons if button.is_visible()]
            #聊天窗口的坐标轴是在左上角,好友头像按钮必须在聊天窗口顶部以下底部以上
            visible_buttons=[button for button in buttons if button.rectangle().bottom>top and button.rectangle().top<bottom]#
            return visible_buttons
    def find_latest_chat_in_chat_history():
        #在聊天记录中查找好友最后一次发言
        ChatMessage=main_window.child_window(**Buttons.ChatMessageButton)
        if ChatMessage.exists():#文件传输助手或公众号没有右侧三个点的聊天信息按钮
            ChatMessage.click_input()
            friend_settings_window=main_window.child_window(**Main_window.FriendSettingsWindow)
            chat_history_button=friend_settings_window.child_window(**Buttons.ChatHistoryButton)
            chat_history_button.click_input()
            time.sleep(0.5)
            desktop=Desktop(**Independent_window.Desktop)
            chat_history_window=desktop.window(**Independent_window.ChatHistoryWindow,title=friend)
            Tools.move_window_to_center(Window_handle=chat_history_window.handle)
            rec=chat_history_window.rectangle()
            mouse.click(coords=(rec.right-8,rec.bottom-8))
            contentlist=chat_history_window.child_window(**Lists.ChatHistoryList)
            if not contentlist.exists():
                chat_history_window.close()
                main_window.close()
                raise NoChatHistoryError(f'你还未与{friend}聊天,只有互相聊天后才可以拍一拍哦！')
            friend_chat=contentlist.child_window(control_type='Button',title=friend,found_index=0)
            friend_message=None
            selected_items=[] #selected_items用来存放向上遍历过程中选中的聊天记录          
            for _ in range(maxSearchNum):
                pyautogui.press('up',_pause=False,presses=2)
                selected_item=[item for item in contentlist.children(control_type='ListItem') if item.is_selected()][0]
                selected_items.append(selected_item)
                if friend_chat.exists():#在`聊天记录窗口找到了某一条对方的聊天记录`
                    friend_message=friend_chat.parent().descendants(title=friend,control_type='Text')[0]
                    break
                #################################################
                #当给定number大于实际聊天记录条数时
                #没必要继续向上了，此时已经到头了，可以提前break了
                #也就是当前selected_item在selected_items的倒数第二个时，就可以直接退出了，当然，必须得保证selected_items大于2
                if len(selected_items)>2 and selected_item==selected_items[-2]:
                    break
            if friend_message:#双击后便可定位到聊天界面中去
                friend_message.double_click_input()
                chat_history_window.close()
            else:
                chat_history_window.close()
                main_window.close()
                raise TickleError(f'你与好友{friend}最近的聊天记录中没有找到最新消息,无法拍一拍对方!')  
        else:
            main_window.close()
            raise TickleError('非正常聊天好友,可能是文件传输助手,无法拍一拍对方!') 
    chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    chatlist=main_window.child_window(**Main_window.FriendChatList)
    tickle=main_window.child_window(**Main_window.Tickle)
    buttons=find_firend_buttons_in_chat_history(chatlist)
    if buttons:
        for button in buttons:
            button.right_click_input()
            if tickle.exists():
                break
        tickle.click_input()
    else:
        find_latest_chat_in_chat_history()
        buttons=find_firend_buttons_in_chat_history(chatlist)
        for button in buttons:
            button.right_click_input()
            if tickle.exists():
                break
        tickle.click_input()
    if close_wechat:
        chat.close()

                         

def get_friends_info(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来获取通讯录中所有微信好友的基本信息(昵称,备注,微信号),速率约为1秒7-12个好友,注:不包含企业微信好友,\n
    结果以json格式返回\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    #获取右侧变化的好友信息面板内的信息
    def get_info():
        nickname=None
        wechatnumber=None
        remark=None
        try: #通讯录界面右侧的好友信息面板  
            global base_info_pane
            try:
                base_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
            except IndexError:
                base_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
            base_info=base_info_pane.descendants(control_type='Text')
            base_info=[element.window_text() for element in base_info]
            # #如果有昵称选项,说明好友有备注
            if language=='简体中文':
                if base_info[1]=='昵称：':
                    remark=base_info[0]   
                    nickname=base_info[2]
                    wechatnumber=base_info[4]
                else:#没有昵称选项，好友昵称就是备注,备注就是昵称
                    nickname=base_info[0]
                    remark=nickname
                    wechatnumber=base_info[2]

            if language=='英文':
                if base_info[1]=='Name: ':
                    remark=base_info[0]   
                    nickname=base_info[2]
                    wechatnumber=base_info[4]
                else:#没有昵称选项，好友昵称就是备注,备注就是昵称
                    nickname=base_info[0]
                    remark=nickname
                    wechatnumber=base_info[2]

            if language=='繁体中文':
                if base_info[1]=='暱稱: ':
                    remark=base_info[0]   
                    nickname=base_info[2]
                    wechatnumber=base_info[4]
                else:#没有昵称选项，好友昵称就是备注,备注就是昵称
                    nickname=base_info[0]
                    remark=nickname
                    wechatnumber=base_info[2]
            return nickname,remark,wechatnumber
        except IndexError:
            return '非联系人'
    main_window=Tools.open_contacts(wechat_path=wechat_path,is_maximize=is_maximize)
    ContactsLists=main_window.child_window(**Main_window.ContactsList)
    #############################
    #先去通讯录列表最底部把最后一个好友的信息记录下来，通过键盘上的END健实现
    rec=ContactsLists.rectangle()
    mouse.click(coords=(rec.right-5,rec.top))
    pyautogui.press('End')
    last_member_info=get_info()
    while last_member_info=='非联系人':
        pyautogui.press('up')
        time.sleep(0.01)
        last_member_info=get_info()
    last_member_info={'wechatnumber':last_member_info[2]}
    pyautogui.press('Home')
    ######################################################################
    nicknames=[] 
    remarks=[]
    #初始化微信号列表为最后一个好友的微信号与任意字符,至于为什么要填充任意字符，自己想想
    wechatnumbers=[last_member_info['wechatnumber'],'nothing']
    #核心思路，一直比较存放所有好友微信号列表的首个元素和最后一个元素是否相同，
    #当记录到最后一个好友时,列表首位元素相同,此时结束while循环,while循环内是一直按下down健，记录右侧变换
    #的好友信息面板内的好友信息
    while wechatnumbers[-1]!=wechatnumbers[0]:
        pyautogui.keyDown('down',_pause=False)
        time.sleep(0.01)
        #这里将get_info内容提取出来重复是因为，这样会加快速度，若在while循环内部直接调用get_info函数，会导致速度变慢
        try: #通讯录界面右侧的好友信息面板  
            base_info=base_info_pane.descendants(control_type='Text')
            base_info=[element.window_text() for element in base_info]
            # #如果有昵称选项,说明好友有备注s
            if language=='简体中文':
                if base_info[1]=='昵称：':
                    remark=base_info[0]
                    nickname=base_info[2]
                    wechatnumber=base_info[4]
                else:#没有昵称选项，好友昵称就是备注,备注就是昵称
                    nickname=base_info[0]
                    remark=nickname
                    wechatnumber=base_info[2]
                nicknames.append(nickname)
                remarks.append(remark)
                wechatnumbers.append(wechatnumber) 
            if language=='英文':
                if base_info[1]=='Name: ':
                    remark=base_info[0]
                    nickname=base_info[2]
                    wechatnumber=base_info[4]
                else:#没有昵称选项，好友昵称就是备注,备注就是昵称
                    nickname=base_info[0]
                    remark=nickname
                    wechatnumber=base_info[2]
                nicknames.append(nickname)
                remarks.append(remark)
                wechatnumbers.append(wechatnumber)

            if language=='繁体中文':
                if base_info[1]=='暱稱: ':
                    remark=base_info[0]
                    nickname=base_info[2]
                    wechatnumber=base_info[4]
                else:#没有昵称选项，好友昵称就是备注,备注就是昵称
                    nickname=base_info[0]
                    remark=nickname
                    wechatnumber=base_info[2]
                nicknames.append(nickname)
                remarks.append(remark)
                wechatnumbers.append(wechatnumber)      
        except IndexError:
            pass
    #删除一开始存放在起始位置的最后一个好友的微信号,不然重复了
    del(wechatnumbers[0])
    #第二个位置上是填充的任意字符,删掉上一个之后它变成了第一个,也删掉
    del(wechatnumbers[0])
    ##########################################
    #转为json格式
    records=zip(nicknames,remarks,wechatnumbers)
    contacts=[{'昵称':name[0],'备注':name[1],'微信号':name[2]} for name in records]
    contacts_json=json.dumps(contacts,ensure_ascii=False,separators=(',', ':'),indent=4)
    ##############################################################
    pyautogui.press('Home')
    if close_wechat:
        main_window.close()
    return contacts_json

def get_friends_detail(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函數用来获取通讯录中所有微信好友的详细信息(昵称,备注,地区，标签,个性签名,共同群聊,微信号,来源),注:不包含企业微信好友,速率约为1秒4-6个好友\n
    结果以json格式返回\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    #获取右侧变化的好友信息面板内的信息
    #从主窗口开始查找
    nickname='无'#昵称
    wechatnumber='无'#微信号
    region='无'#好友的地区
    tag='无'#好友标签
    common_group_num='无'
    remark='无'#备注
    signature='无'#个性签名
    source='无'#好友来源
    descrption='无'#描述
    phonenumber='无'#电话号
    permission='无'#朋友权限
    def get_info(): 
        nickname='无'#昵称
        wechatnumber='无'#微信号
        region='无'#好友的地区
        tag='无'#好友标签
        common_group_num='无'
        remark='无'#备注
        signature='无'#个性签名
        source='无'#好友来源
        descrption='无'#描述
        phonenumber='无'#电话号
        permission='无'#朋友权限
        global base_info_pane#设为全局变量，只需在第一次查找最后一个人时定位一次基本信息和详细信息面板即可
        global detail_info_pane
        try: #通讯录界面右侧的好友信息面板   
            try:
                base_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
            except IndexError:
                base_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
            base_info=base_info_pane.descendants(control_type='Text')
            base_info=[element.window_text() for element in base_info]
            # #如果有昵称选项,说明好友有备注
            if language=='简体中文':
                if base_info[1]=='昵称：':
                    remark=base_info[0]
                    nickname=base_info[2]
                    wechatnumber=base_info[4]
                    if '地区：' in base_info:
                        region=base_info[base_info.index('地区：')+1]
                    else:
                        region='无'
                    
                else:
                    nickname=base_info[0]
                    remark=nickname
                    wechatnumber=base_info[2]
                    if '地区：' in base_info:
                        region=base_info[base_info.index('地区：')+1]
                    else:
                        region='无'
                    
                detail_info=[]
                try:
                    detail_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                except IndexError:
                    detail_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                buttons=detail_info_pane.descendants(control_type='Button')
                for pane in detail_info_pane.children(control_type='Pane',title='')[1:]:
                    detail_info.extend(pane.descendants(control_type='Text'))
                detail_info=[element.window_text() for element in detail_info]
                for button in buttons:
                    if '个' in button.window_text(): 
                        common_group_num=button.window_text()
                        break
                    else:
                        common_group_num='无'
                if '个性签名' in detail_info:
                    signature=detail_info[detail_info.index('个性签名')+1]
                if '标签' in detail_info:
                    tag=detail_info[detail_info.index('标签')+1]
                if '来源' in detail_info:
                    source=detail_info[detail_info.index('来源')+1]
                if '朋友权限' in detail_info:
                    permission=detail_info[detail_info.index('朋友权限')+1]
                if '电话' in detail_info:
                    phonenumber=detail_info[detail_info.index('电话')+1]
                if '描述' in detail_info:
                    descrption=detail_info[detail_info.index('描述')+1]
                return nickname,remark,wechatnumber,region,tag,common_group_num,signature,source,permission,phonenumber,descrption
            
            if language=='英文':
                if base_info[1]=='Name: ':
                        remark=base_info[0]
                        nickname=base_info[2]
                        wechatnumber=base_info[4]
                        if 'Region: ' in base_info:
                            region=base_info[base_info.index('Region: ')+1]
                        else:
                            region='无' 
                else:
                    nickname=base_info[0]
                    remark=nickname
                    wechatnumber=base_info[2]
                    if 'Region: ' in base_info:
                        region=base_info[base_info.index('Region: ')+1]
                    else:
                        region='无'
                    
                detail_info=[]
                try:
                    detail_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                except IndexError:
                    detail_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                buttons=detail_info_pane.descendants(control_type='Button')
                for pane in detail_info_pane.children(control_type='Pane',title='')[1:]:
                    detail_info.extend(pane.descendants(control_type='Text'))
                detail_info=[element.window_text() for element in detail_info]
                for button in buttons:
                    if re.match(r'\d+',button.window_text()):
                        common_group_num=button.window_text()
                        break
                    else:
                        common_group_num='无'
                if "What's Up" in detail_info:
                    signature=detail_info[detail_info.index("What's Up")+1]
                if 'Tag' in detail_info:
                    tag=detail_info[detail_info.index('Tag')+1]
                if 'Source' in detail_info:
                    source=detail_info[detail_info.index('Source')+1]
                if 'Privacy' in detail_info:
                    permission=detail_info[detail_info.index('Privacy')+1]
                if 'Mobile' in detail_info:
                    phonenumber=detail_info[detail_info.index('Mobile')+1]
                if 'Description' in detail_info:
                    descrption=detail_info[detail_info.index('Description')+1]
                return nickname,remark,wechatnumber,region,tag,common_group_num,signature,source,permission,phonenumber,descrption
            
            if language=='繁体中文':
                if base_info[1]=='暱稱：':
                    remark=base_info[0]
                    nickname=base_info[2]
                    wechatnumber=base_info[4]
                    if '地區：' in base_info:
                        region=base_info[base_info.index('地區：')+1]
                    else:
                        region='无'
                    
                else:
                    nickname=base_info[0]
                    remark=nickname
                    wechatnumber=base_info[2]
                    if '地區：' in base_info:
                        region=base_info[base_info.index('地區：')+1]
                    else:
                        region='无'
                    
                detail_info=[]
                try:
                    detail_info_pane=main_window.children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                except IndexError:
                    detail_info_pane=main_window.children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[1].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0].children(title='',control_type='Pane')[0]
                buttons=detail_info_pane.descendants(control_type='Button')
                for pane in detail_info_pane.children(control_type='Pane',title='')[1:]:
                    detail_info.extend(pane.descendants(control_type='Text'))
                detail_info=[element.window_text() for element in detail_info]
                for button in buttons:
                    if '個' in button.window_text(): 
                        common_group_num=button.window_text()
                        break
                    else:
                        common_group_num='无'
                if '個性簽名' in detail_info:
                    signature=detail_info[detail_info.index('個性簽名')+1]
                if '標籤' in detail_info:
                    tag=detail_info[detail_info.index('標籤')+1]
                if '來源' in detail_info:
                    source=detail_info[detail_info.index('來源')+1]
                if '朋友權限' in detail_info:
                    permission=detail_info[detail_info.index('朋友權限')+1]
                if '電話' in detail_info:
                    phonenumber=detail_info[detail_info.index('電話')+1]
                if '描述' in detail_info:
                    descrption=detail_info[detail_info.index('描述')+1]
                return nickname,remark,wechatnumber,region,tag,common_group_num,signature,source,permission,phonenumber,descrption
            
        except IndexError:
                #注意:企业微信好友也会被判定为非联系人
            return '非联系人'
    main_window=Tools.open_contacts(wechat_path=wechat_path,is_maximize=is_maximize)
    ContactsLists=main_window.child_window(**Main_window.ContactsList)
    #####################################################################
    #先去通讯录列表最底部把最后一个好友的信息记录下来，通过键盘上的END健实现
    rec=ContactsLists.rectangle()
    mouse.click(coords=(rec.right-5,rec.top))
    pyautogui.press('End')
    last_member_info=get_info()
    while last_member_info=='非联系人':#必须确保通讯录底部界面下的最有一个好友是具有微信号的联系人，因此要向上查询
        pyautogui.press('up',_pause=False)
        last_member_info=get_info()
    last_member_info={'wechatnumber':last_member_info[2]}
    pyautogui.press('Home')
    ######################################################################
    #初始化微信号列表为最后一个好友的微信号与任意字符,至于为什么要填充任意字符，自己想想
    wechatnumbers=[last_member_info['wechatnumber'],'nothing']
    nicknames=[]
    remarks=[]
    tags=[]
    regions=[]
    common_group_nums=[]
    permissions=[]
    phonenumbers=[]
    descrptions=[]
    signatures=[]
    sources=[]
    #核心思路，一直比较存放所有好友微信号列表的首个元素和最后一个元素是否相同，
    #当记录到最后一个好友时,列表首末元素相同,此时结束while循环,while循环内是一直按下down健，记录右侧变换
    #的好友信息面板内的好友信息
    while wechatnumbers[-1]!=wechatnumbers[0]:
        pyautogui.keyDown('down',_pause=False)
        time.sleep(0.01)
        try: #通讯录界面右侧的好友信息面板   
            base_info=base_info_pane.descendants(control_type='Text')
            base_info=[element.window_text() for element in base_info]
            # #如果有昵称选项,说明好友有备注
            if language=='简体中文':
                if base_info[1]=='昵称：':
                    remark=base_info[0]
                    nickname=base_info[2]
                    wechatnumber=base_info[4]
                    if '地区：' in base_info:
                        region=base_info[base_info.index('地区：')+1]
                    else:
                        region='无'
                else:
                    nickname=base_info[0]
                    remark=nickname
                    wechatnumber=base_info[2]
                    if '地区：' in base_info:
                        region=base_info[base_info.index('地区：')+1]
                    else:
                        region='无'
                detail_info=[]
                buttons=detail_info_pane.descendants(control_type='Button')
                for pane in detail_info_pane.children(control_type='Pane',title='')[1:]:
                    detail_info.extend(pane.descendants(control_type='Text'))
                detail_info=[element.window_text() for element in detail_info]
                for button in buttons:
                    if '个' in button.window_text(): 
                        common_group_num=button.window_text()
                        break
                    else:
                        common_group_num='无'
                
                if '个性签名' in detail_info:
                    signature=detail_info[detail_info.index('个性签名')+1]
                else:
                    signature='无'
                if '标签' in detail_info:
                    tag=detail_info[detail_info.index('标签')+1]
                else:
                    tag='无'
                if '来源' in detail_info:
                    source=detail_info[detail_info.index('来源')+1]
                else:
                    source='无'
                if '朋友权限' in detail_info:
                    permission=detail_info[detail_info.index('朋友权限')+1]
                else:
                    permission='无'
                if '电话' in detail_info:
                    phonenumber=detail_info[detail_info.index('电话')+1]
                else:
                    phonenumber='无'
                if '描述' in detail_info:
                    descrption=detail_info[detail_info.index('描述')+1]
                else:
                    descrption='无'
                nicknames.append(nickname)
                remarks.append(remark)
                wechatnumbers.append(wechatnumber)
                regions.append(region)
                tags.append(tag)
                common_group_nums.append(common_group_num)
                signatures.append(signature)
                sources.append(source)
                permissions.append(permission)
                phonenumbers.append(phonenumber)
                descrptions.append(descrption)

            if language=='英文':
                if base_info[1]=='Name: ':
                    remark=base_info[0]
                    nickname=base_info[2]
                    wechatnumber=base_info[4]
                    if 'Region: ' in base_info:
                        region=base_info[base_info.index('Region: ')+1]
                    else:
                        region='无'
                else:
                    nickname=base_info[0]
                    remark=nickname
                    wechatnumber=base_info[2]
                    if 'Region: ' in base_info:
                        region=base_info[base_info.index('Region: ')+1]
                    else:
                        region='无'
                detail_info=[]
                buttons=detail_info_pane.descendants(control_type='Button')
                for pane in detail_info_pane.children(control_type='Pane',title='')[1:]:
                    detail_info.extend(pane.descendants(control_type='Text'))
                detail_info=[element.window_text() for element in detail_info]
                for button in buttons:
                    if re.match(r'\d+',button.window_text()):
                        common_group_num=button.window_text()
                        break
                    else:
                        common_group_num='无'
                
                if  "What's Up" in detail_info:
                    signature=detail_info[detail_info.index("What's Up")+1]
                else:
                    signature='无'
                if 'Tag' in detail_info:
                    tag=detail_info[detail_info.index('Tag')+1]
                else:
                    tag='无'
                if 'Source' in detail_info:
                    source=detail_info[detail_info.index('Source')+1]
                else:
                    source='无'
                if 'Privacy' in detail_info:
                    permission=detail_info[detail_info.index('Privacy')+1]
                else:
                    permission='无'
                if 'Mobile' in detail_info:
                    phonenumber=detail_info[detail_info.index('Mobile')+1]
                else:
                    phonenumber='无'
                if 'Description' in detail_info:
                    descrption=detail_info[detail_info.index('Description')+1]
                else:
                    descrption='无'
                nicknames.append(nickname)
                remarks.append(remark)
                wechatnumbers.append(wechatnumber)
                regions.append(region)
                tags.append(tag)
                common_group_nums.append(common_group_num)
                signatures.append(signature)
                sources.append(source)
                permissions.append(permission)
                phonenumbers.append(phonenumber)
                descrptions.append(descrption)
            
            if language=='繁体中文':
                if base_info[1]=='暱稱：':
                    remark=base_info[0]
                    nickname=base_info[2]
                    wechatnumber=base_info[4]
                    if '地區：' in base_info:
                        region=base_info[base_info.index('地區：')+1]
                    else:
                        region='无'
                else:
                    nickname=base_info[0]
                    remark=nickname
                    wechatnumber=base_info[2]
                    if '地區：' in base_info:
                        region=base_info[base_info.index('地區：')+1]
                    else:
                        region='无'
                detail_info=[]
                buttons=detail_info_pane.descendants(control_type='Button')
                for pane in detail_info_pane.children(control_type='Pane',title='')[1:]:
                    detail_info.extend(pane.descendants(control_type='Text'))
                detail_info=[element.window_text() for element in detail_info]
                for button in buttons:
                    if '個' in button.window_text(): 
                        common_group_num=button.window_text()
                        break
                    else:
                        common_group_num='无'
                
                if '個性簽名' in detail_info:
                    signature=detail_info[detail_info.index('個性簽名')+1]
                else:
                    signature='无'
                if '標籤' in detail_info:
                    tag=detail_info[detail_info.index('標籤')+1]
                else:
                    tag='无'
                if '來源' in detail_info:
                    source=detail_info[detail_info.index('來源')+1]
                else:
                    source='无'
                if '朋友權限' in detail_info:
                    permission=detail_info[detail_info.index('朋友權限')+1]
                else:
                    permission='无'
                if '電話' in detail_info:
                    phonenumber=detail_info[detail_info.index('電話')+1]
                else:
                    phonenumber='无'
                if '描述' in detail_info:
                    descrption=detail_info[detail_info.index('描述')+1]
                else:
                    descrption='无'
                nicknames.append(nickname)
                remarks.append(remark)
                wechatnumbers.append(wechatnumber)
                regions.append(region)
                tags.append(tag)
                common_group_nums.append(common_group_num)
                signatures.append(signature)
                sources.append(source)
                permissions.append(permission)
                phonenumbers.append(phonenumber)
                descrptions.append(descrption)
        except IndexError:
            pass
    #删除一开始存放在起始位置的最后一个好友的微信号,不然重复了
    del(wechatnumbers[0])
    #第二个位置上是填充的任意字符,删掉上一个之后它变成了第一个,也删掉
    del(wechatnumbers[0])
    ##########################################
    #转为json格式
    records=zip(nicknames,wechatnumbers,regions,remarks,phonenumbers,tags,descrptions,permissions,common_group_nums,signatures,sources)
    contacts=[{'昵称':name[0],'微信号':name[1],'地区':name[2],'备注':name[3],'电话':name[4],'标签':name[5],'描述':name[6],'朋友权限':name[7],'共同群聊':name[8],'个性签名':name[9],'来源':name[10]} for name in records]
    contacts_json=json.dumps(contacts,ensure_ascii=False,separators=(',', ':'),indent=4)#ensure_ascii必须为False
    ##############################################################
    pyautogui.press('Home')#回到起始位置,方便下次打开
    if close_wechat:
        main_window.close()
    return contacts_json

def get_groups_info(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来获取通讯录中所有群聊的信息(名称,成员数量)\n
    结果以json格式返回\n
    Args:
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    def remove_duplicate(List1,List2):
        #为了保证两个列表使用extend方法合二为一后没有重复项
        #利用集合的intersection运算找到两个列表的公共部分并将其在其中一个列表中去除掉
        ##a=[1,2,3,4],b=[3,4,5,6],最后返回值为a=[1,2,3,4],b=[5,6]
        common=set(List1).intersection(set(List2))
        List2=[element for element in List2 if element not in common]
        return List1,List2
    def get_info(group_chat_list):
        names=[chat.children()[0].children()[0].children(control_type="Button")[0].texts()[0] for chat in group_chat_list]
        numbers=[chat.children()[0].children()[0].children()[1].children()[0].children()[1].texts()[0] for chat in group_chat_list]
        numbers=[number.replace('(','').replace(')','') for number in numbers]
        return names,numbers
    contacts_settings_window=Tools.open_contacts_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)[0]
    recent_group_chat=contacts_settings_window.child_window(**Buttons.RectentGroupButton)
    try:
        group_chat_list_item=contacts_settings_window.child_window(control_type="List",found_index=0,title="").children(control_type="ListItem",title="")      
        first_group=group_chat_list_item[0].children()[0].children()[0].children(control_type="Button")[0]
        first_group.click_input()
    except IndexError:
        recent_group_chat.set_focus()
        recent_group_chat.click_input()
        group_chat_list_item=contacts_settings_window.child_window(control_type="List",found_index=0,title="").children(control_type="ListItem",title="")      
        first_group=group_chat_list_item[0].children()[0].children()[0].children(control_type="Button")[0]
        first_group.click_input()
    pyautogui.press('End')
    group_chat_list_item=contacts_settings_window.child_window(control_type="List",found_index=0,title="").children(control_type="ListItem",title="")
    last_group_name=get_info(group_chat_list_item)[0][-1]
    pyautogui.press('Home')
    temp=[last_group_name,'nothing']#记录最后一个群的群聊名称，和get_friends_info一样的思路
    groups_members=[]
    groups_names=[]
    record1=[]
    record2=[]
    while temp[-1]!=temp[0]:#比较temp中记录的群聊名称有没有和temp首个元素相同，若相同说明已经到达底部，结束循环
        group_chat_list_item=contacts_settings_window.child_window(control_type="List",found_index=0,title="").children(control_type="ListItem",title="")      
        names,numbers=get_info(group_chat_list_item)
        temp.append(names[-1])
        record1.append(names)
        record2.append(numbers)
        pyautogui.press("pagedown",_pause=False)
    contacts_settings_window.close()
    temp.clear()
    record1[-1],record1[-2]=remove_duplicate(record1[-1],record1[-2])
    record2[-1],record2[-2]=remove_duplicate(record2[-1],record2[-2])
    for names in record1:
        groups_names.extend(names)
    for numbers in record2:
        groups_members.extend(numbers)
    record=zip(groups_names,groups_members)
    groups_info=[{"群聊名称":group[0],"群聊人数":group[1]}for group in record]
    groups_info_json=json.dumps(groups_info,indent=4,ensure_ascii=False)
    return groups_info_json

def get_groupmembers_info(group_name:str,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来获取某个群聊中所有群成员的群昵称(名称,成员数量)\n
    结果以列表的json格式返回\n
    Args:
        group_name\t:群聊名称或备注\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    def find_group_in_contacts_list(group_name):
        contacts_list=main_window.child_window(**Main_window.ContactsList)
        rec=contacts_list.rectangle()  
        mouse.click(coords=(rec.right-5,rec.top+10))
        listitems=contacts_list.children(control_type='ListItem')
        names=[item.window_text() for item in listitems]
        while group_name not in names:
            contacts_list=main_window.child_window(**Main_window.ContactsList)
            listitems=contacts_list.children(control_type='ListItem')
            names=[item.window_text() for item in listitems]
            pyautogui.press('down',_pause=False)
        group=listitems[names.index(group_name)]
        group_button=group.descendants(control_type='Button',title=group_name)[0]
        rec=group_button.rectangle()
        mouse.click(coords=(int(rec.left+rec.right)//2,rec.top-12))
    def get_info():
        groupmember_names=[]
        detail_info_pane=main_window.child_window(title_re=r'.*\(\d+\).*',control_type='Text').parent().parent().children()[1]
        detail_info=detail_info_pane.descendants(control_type='ListItem')
        groupmember_names=[element.window_text() for element in detail_info]
        return groupmember_names
    GroupSettings.save_group_to_contacts(group_name=group_name,state='open',wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=False,search_pages=search_pages)
    main_window=Tools.open_contacts(wechat_path=wechat_path,is_maximize=is_maximize)
    find_group_in_contacts_list(group_name=group_name)
    groupmember_names=get_info()
    GroupSettings.save_group_to_contacts(group_name=group_name,state='close',wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=False)
    if close_wechat:
        main_window.close()
    groupmember_json={'群聊':group_name,'人数':len(groupmember_names),'群成员群昵称':groupmember_names}
    groupmember_json=json.dumps(groupmember_json,ensure_ascii=False,indent=4)
    return groupmember_json
    

def get_chat_history(friend:str,number:int=10,capture_screen:bool=False,folder_path:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来获取好友或群聊的聊天记录\n
    Args:
        friend:\t好友或群聊备注或昵称\n
        number:\t待获取的聊天记录条数,默认10条\n
        capture_scren:\t聊天记录是否截屏,默认不截屏\n
        folder_path:\t存放聊天记录截屏图片的文件夹路径\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n'
    '''
    def parse_message_content(message):
        message_sender=message.descendants(control_type='Text')[0].window_text()#无论什么类型消息,发送人永远是属性为Texts的UI组件中的第一个
        message_time=message.descendants(control_type='Text')[1].window_text()#无论什么类型消息.发送时间都是属性为Texts的UI组件中的第二个
        #至于消息的内容那就需要仔细判断一下了
        specialMegCN={'[图片]':'图片消息','[视频]':'视频消息','[动画表情]':'动画表情','[视频号]':'视频号'}
        specialMegEN={'[Photo]':'图片消息','[Video]':'视频消息','[Sticker]':'动画表情','[Channel]':'视频号'}
        specialMegTC={'[圖片]':'图片消息','[影片]':'视频消息','[動態貼圖]':'动画表情','[影音號]':'视频号'}
        #不同语言,处理消息内容时不同
        if language=='简体中文':
            if message.window_text() in specialMegCN.keys():#内容在特殊消息中
                message_content=specialMegCN.get(message.window_text())
            else:#文件,卡片链接,语音,以及正常的文本消息
                if message.window_text()=='[文件]':
                    filename=message.descendants(control_type='Text')[2].texts()[0]
                    message_content=f'文件:{filename}'
                elif re.match(r'\[语音\]\d+秒',message.window_text()):
                    message_content='语音消息'
                elif len(message.descendants(control_type='Text'))>3:#
                    cardContent=message.descendants(control_type='Text')[2:]
                    cardContent=[link.window_text() for link in cardContent]
                    if '微信转账' in cardContent:
                        index=cardContent.index('微信转账')
                        message_content=f'微信转账:{cardContent[index-2]}:{cardContent[index-1]}'
                    else:
                        message_content='卡片内容:'+','.join(cardContent)
                else:#正常文本
                    texts=message.descendants(control_type='Text')
                    texts=[text.window_text() for text in texts]
                    message_content=texts[2]
                
        if language=='英文':
            if message.window_text() in specialMegEN.keys():
                message_content=specialMegEN.get(message.window_text())
            else:#文件,卡片链接,语音,以及正常的文本消息
                if message.window_text()=='[File]':
                    filename=message.descendants(control_type='Text')[2].texts()[0]
                    message_content=f'文件:{filename}'
                elif re.match(r'\[Audio\]\d+s',message.window_text()):
                    message_content='语音消息'

                elif len(message.descendants(control_type='Text'))>3:#
                    cardContent=message.descendants(control_type='Text')[2:]
                    cardContent=[link.window_text() for link in cardContent]
                    if 'Weixin Transfer' in cardContent:
                        index=cardContent.index('Weixin Transfer')
                        message_content=f'微信转账:{cardContent[index-2]}:{cardContent[index-1]}'
                    else:
                        message_content='卡片内容:'+','.join(cardContent)
                else:#正常文本
                    texts=message.descendants(control_type='Text')
                    texts=[text.window_text() for text in texts]
                    message_content=texts[2]
        
        if language=='繁体中文':
            if message.window_text() in specialMegTC.keys():
                message_content=specialMegTC.get(message.window_text())
            else:#文件,卡片链接,语音,以及正常的文本消息
                if message.window_text()=='[檔案]':
                    filename=message.descendants(control_type='Text')[2].texts()[0]
                    message_content=f'文件:{filename}'
                elif re.match(r'\[語音\]\d+秒',message.window_text()):
                    message_content='语音消息'
                elif len(message.descendants(control_type='Text'))>3:#
                    cardContent=message.descendants(control_type='Text')[2:]
                    cardContent=[link.window_text() for link in cardContent]
                    if message.window_text()=='' and '微信轉賬' in cardContent:
                        index=cardContent.index('微信轉賬')
                        message_content=f'微信转账:{cardContent[index-2]}:{cardContent[index-1]}'
                    else:
                        message_content='链接卡片内容:'+','.join(cardContent)
                else:#正常文本
                    texts=message.descendants(control_type='Text')
                    texts=[text.window_text() for text in texts]
                    message_content=texts[2]

        return message_sender,message_time,message_content
    
    def ByNum():
        #根据数量来获取聊天记录,后序还会增加一个ByDate
        rec=chat_history_window.rectangle()
        mouse.click(coords=(rec.right-10,rec.bottom-10))
        pyautogui.press('End')
        chat_history=[]
        contentList=chat_history_window.child_window(**Lists.ChatHistoryList)
        if not contentList.exists():    
            chat_history_window.close()
            raise NoChatHistoryError(f'你还未与{friend}聊天,无法获取聊天记录!')  
        selected_items=[] #selected_items用来存放向上遍历过程中选中的聊天记录          
        for _ in range(number):
            pyautogui.press('up',_pause=False,presses=2)
            selected_item=[item for item in contentList.children(control_type='ListItem') if item.is_selected()][0]
            selected_items.append(selected_item)
            #################################################
            #当给定number大于实际聊天记录条数时
            #没必要继续向上了，此时已经到头了，可以提前break了
            #也就是当前selected_item在selected_items的倒数第二个时，就可以直接退出了，当然，必须得保证selected_items大于2
            if len(selected_items)>2 and selected_item==selected_items[-2]:
                break
            chat_history.append(parse_message_content(selected_item))
            ############################################
        pyautogui.press('END')
        ###############################################################
        #截图逻辑:selected_items中存放的是向上遍历过程中被选中的且数量正确(不使用number是因为number可能比所有的聊天记录总数还大)聊天记录列表
        #selected_items最多也就是所有的聊天记录
        #length是向上时每一页的聊天记录数量，比较一下length是否达到selected_items内的聊天记录数量，如果达到那么不再截取每一页的图片
        if capture_screen:
            Num=1
            length=len(contentList.children(control_type='ListItem'))
            while length<len(selected_items):
                chat_history_image=chat_history_window.capture_as_image()
                if folder_path:
                    pic_path=os.path.abspath(os.path.join(folder_path,f'与{friend}的聊天记录{Num}.png'))
                else:
                    pic_path=os.path.abspath(os.path.join(os.getcwd(),f'与{friend}的聊天记录{Num}.png'))
                chat_history_image.save(pic_path)
                pyautogui.keyDown('pageup',_pause=False)
                Num+=1
                length+=len(contentList.children(control_type='ListItem'))
            #退出循环后还要记得截最后一张图片
            chat_history_image=chat_history_window.capture_as_image()
            if folder_path:
                pic_path=os.path.abspath(os.path.join(folder_path,f'与{friend}的聊天记录{Num}.png'))
            else:
                pic_path=os.path.abspath(os.path.join(os.getcwd(),f'与{friend}的聊天记录{Num}.png'))
            chat_history_image.save(pic_path)
        pyautogui.press('END')
        chat_history_window.close()
        if len(chat_history)<number:
            warn(message=f"你与{friend}的聊天记录不足{number},已为你导出全部的{len(chat_history)}条聊天记录",category=ChatHistoryNotEnough)
            chat_history_json=json.dumps(chat_history,ensure_ascii=False,indent=4)
        else:
            chat_history_json=json.dumps(chat_history[:number],ensure_ascii=False,indent=4)
        return chat_history_json
    
    if capture_screen and folder_path:
        folder_path=re.sub(r'(?<!\\)\\(?!\\)',r'\\\\',folder_path)
        if not Systemsettings.is_dirctory(folder_path):
            raise NotFolderError(r'给定路径不是文件夹!无法保存聊天记录截图,请重新选择文件夹！')
    chat_history_window=Tools.open_chat_history(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat,search_pages=search_pages)[0]
    chat_history_json=ByNum()#
    ########################################################################
    return chat_history_json


def check_new_message(duration:str=None,wechat_path:str=None,close_wechat:bool=True):
    '''
    该函数用来查看新消息,若你传入了duration参数,那么可以用来监听新消息\n
    注意,使用该功能需要开启文件传输助手功能,为了更好监听新消息,需要切换聊天界面至文件传输助手\n
    否则当前聊天界面内的新消息无法监控\n
    当你传入duration后如出现偶尔停顿此为正常等待机制:每遍历一次会话列表会停顿一小段时间等待新消息\n
    Args:
        duration:\t监听消息持续时长,格式:'s','min','h'单位:s/秒,min/分,h/小时\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    Returns:
        新消息json or 未查找到任何新消息\n
        json格式:[{'名称':'好友备注','新消息条数',25:'类型':'群聊or个人or公众号','消息':[str]}]\n
    '''
    #先遍历消息列表查找是否存在新消息,然后在遍历一遍消息列表,点击具有新消息的好友，记录消息，没有直接返回'未查找到任何新消息'
    Names=[]#有新消息的好友名称
    Nums=[]#与Names中好友一一对应的消息条数
    search_pages=1#在聊天列表中查找新消息好友位置时遍历的,初始为1,如果有新消息的话,后续会变化
    if language=='简体中文':
        pattern=r'\[语音\]\d+秒'
        filetransfer='文件传输助手'
    if language=='英文':
        pattern=r'\[Audio\]\d+s'
        filetransfer='File Transfer'
    if language=='繁体中文':
        pattern=r'\[語音\]\d+秒'
        filetransfer='檔案傳輸'
    def ConvertMessages(Messages,type):
        #用来获取开启语音转文字后新消息中语音转文字结果
        for i in range(len(Messages)):
            if re.match(pattern,Messages[i].window_text()):#匹配是否是语音消息
                try:#是语音消息就定位语音转文字结果
                    if type=='群聊':
                        result=Messages[i].descendants(control_type='Text')[2].window_text()
                        Messages[i]=Messages[i].window_text()+f'  消息内容:{result}'
                    else:
                        result=Messages[i].descendants(control_type='Text')[1].window_text()
                        Messages[i]=Messages[i].window_text()+f'  消息内容:{result}'
                except Exception:#定位时不排除有人只发送[语音]\d+秒这样的文本消息，所以可能出现异常
                    Messages[i]=Messages[i].window_text()
            else:#不是语音消息直接获取文本
                Messages[i]=Messages[i].window_text()
        return Messages
    
    def get_message_content(name,number,search_pages):
        Messages=[]
        main_window=Tools.find_friend_in_MessageList(friend=name,search_pages=search_pages)[1]
        check_more_messages_button=main_window.child_window(**Buttons.CheckMoreMessagesButton)
        voice_call_button=main_window.child_window(**Buttons.VoiceCallButton)#语音聊天按钮
        video_call_button=main_window.child_window(**Buttons.VideoCallButton)#视频聊天按钮
        if voice_call_button.exists() and not video_call_button.exists():#只有语音和聊天按钮没有视频聊天按钮是群聊
            type='群聊' 
            chatList=main_window.child_window(**Main_window.FriendChatList)
            x,y=chatList.rectangle().left+10,(main_window.rectangle().top+main_window.rectangle().bottom)//2
            messages=chatList.children(control_type='ListItem')
            Messages.extend([message for message in messages  if not re.match(r'\d+:\d+',message.window_text())])
            #点击聊天区域侧边栏靠里一些的位置,依次来激活滑块,不直接main_window.click_input()是为了防止点到消息
            mouse.click(coords=(x,y))
            #按一下pagedown到最下边
            pyautogui.press('pagedown')
            ########################
            #需要先提前向上遍历一遍,防止语音消息没有转换完毕
            if number<=10:#10条消息最多先向上遍历3页
                pages=number//3
            else:
                pages=number//2
            for _ in range(pages):
                if check_more_messages_button.exists():
                    check_more_messages_button.click_input()
                    mouse.click(coords=(x,y))
                pyautogui.press('pageup',_pause=False)
            pyautogui.press('End')
            mouse.click(coords=(x,y))
            pyautogui.press('pagedown')
            ##################################
            #开始记录
            while len(list(set(Messages)))<number:
                if check_more_messages_button.exists():
                    check_more_messages_button.click_input()
                    mouse.click(coords=(x,y))
                pyautogui.press('pageup',_pause=False)
                messages=chatList.children(control_type='ListItem')
                Messages.extend([message for message in messages if not re.match(r'\d+:\d+',message.window_text())])
            #######################################################
            Messages=ConvertMessages(Messages,type)#将listitem转换为文本内容
            Messages=Messages[-number:]#返回从后向前数number条消息
            pyautogui.press('End')
            return {'名称':name,'新消息条数':number,'类型':type,'消息':Messages}
        
        if video_call_button.exists() and video_call_button.exists():#同时有语音聊天和视频聊天按钮的是个人
            type='好友'
            chatList=main_window.child_window(**Main_window.FriendChatList)
            x,y=chatList.rectangle().left+10,(main_window.rectangle().top+main_window.rectangle().bottom)//2
            messages=chatList.children(control_type='ListItem')
            Messages.extend([message for message in messages  if not re.match(r'\d+:\d+',message.window_text())])
            #点击聊天区域侧边栏靠里一些的位置,依次来激活滑块,不直接main_window.click_input()是为了防止点到消息
            mouse.click(coords=(x,y))
            #按一下pagedown到最下边
            pyautogui.press('pagedown')
            ########################
            #需要先提前向上遍历一遍,防止语音消息没有转换完毕
            if number<=10:#10条消息最多先向上遍历number//3页
                pages=number//3
            else:
                pages=number//2#超过10页
            for _ in range(pages):
                if check_more_messages_button.exists():
                    check_more_messages_button.click_input()
                    mouse.click(coords=(x,y))
                pyautogui.press('pageup',_pause=False)
            pyautogui.press('End')
            mouse.click(coords=(x,y))
            pyautogui.press('pagedown')
            ##################################
            #开始记录
            while len(list(set(Messages)))<number:
                if check_more_messages_button.exists():
                    check_more_messages_button.click_input()
                    mouse.click(coords=(x,y))
                pyautogui.press('pageup',_pause=False)
                messages=chatList.children(control_type='ListItem')
                Messages.extend([message for message in messages if not re.match(r'\d+:\d+',message.window_text())])
            #######################################################
            Messages=ConvertMessages(Messages,type)#将listitem转换为文本内容
            Messages=Messages[-number:]#返回从后向前数number条消息
            pyautogui.press('End')
            return {'名称':name,'新消息条数':number,'类型':type,'消息':Messages}
        else:#都没有是公众号
            type='公众号'
            return {'名称':name,'新消息条数':number,'类型':type}
    def record():
        #遍历当前会话列表内可见的所有成员，获取他们的名称和新消息条数，没有新消息的话返回[],[]
        #newMessagefriends为会话列表(List)中所有含有新消息的ListItem
        newMessagefriends=[friend for friend in messageList.items() if '条新消息' in friend.window_text()]
        if newMessagefriends:
            #newMessageTips为newMessagefriends中每个元素的文本:['测试365 5条新消息','一家人已置顶20条新消息']这样的字符串列表
            newMessageTips=[friend.window_text() for friend in newMessagefriends]
            #会话列表中的好友具有Text属性，Text内容为备注名，通过这个按钮的名称获取好友名字
            names=[friend.descendants(control_type='Text')[0].window_text() for friend in newMessagefriends]
            #此时filtered_Tips变为：['5条新消息','20条新消息']直接正则匹配就不会出问题了
            filtered_Tips=[friend.replace(name,'') for name,friend in zip(names,newMessageTips)]
            nums=[int(re.findall(r'\d+',tip)[0]) for tip in filtered_Tips]
            return names,nums 
        return [],[]
    
    #打开文件传输助手是为了防止当前窗口有好友给自己发消息无法检测到,因为当前窗口即使有新消息也不会在会话列表中好友头像上显示数字,
    main_window=Tools.open_dialog_window(friend=filetransfer,wechat_path=wechat_path,is_maximize=True)[1]
    messageList=main_window.child_window(**Main_window.ConversationList)
    scrollable=Tools.is_VerticalScrollable(messageList)
    chatsButton=main_window.child_window(**SideBar.Chats)
    if not duration:#没有持续时间。
        #侧边栏没有红色消息提示直接返回未查找到新消息
        if not chatsButton.legacy_properties().get('Value'):#通过微信侧边栏的聊天按钮的LegarcyProperties.value有没有消息提示(右上角的红色数字,有的话这个值为'\d+')
            if close_wechat:
                main_window.close()
            return '未查找到新消息'     
        if not scrollable:#聊天列表内不足12人以上且有新消息,没有滑块，不用遍历,直接原地在列表里查找
            names,nums=record()
            if names and nums:
                Names.extend(names)
                Nums.extend(nums)
            dic=dict(zip(Names,Nums))#临时变量,存储好友名称与新消息数量的字典
            newMessages=[]
            for key,value in dic.items():         
                newMessages.append(get_message_content(key,value,search_pages=search_pages))
            Tools.open_dialog_window(friend=filetransfer,wechat_path=wechat_path,is_maximize=True)
            if close_wechat:
                main_window.close()
            newMessages_json=json.dumps(newMessages,ensure_ascii=False,indent=4)
            if close_wechat:
                main_window.close()
            return newMessages_json
          
        if scrollable:#聊天列表在12人以上且有新消息,遍历一遍
            x,y=messageList.rectangle().right-5,messageList.rectangle().top+8
            mouse.click(coords=(x,y))#点击右上方激活滑块
            pyautogui.press('Home')
            pyautogui.press('End')
            lastmemberName=messageList.items()[-1].window_text()
            pyautogui.press('Home')#按下Home健确保从顶部开始
            while messageList.items()[-1].window_text()!=lastmemberName:
                names,nums=record()
                if names and nums:
                    Names.extend(names)   
                    Nums.extend(nums)
                pyautogui.keyDown('pagedown',_pause=False)
                search_pages+=1
            pyautogui.press('Home')
            #################
            #回到顶部后,再查找一下,以防在向下遍历会话列表时顶部有好友给发消息,没检测到新的变化的数字
            names,nums=record()
            if names and nums:
                Names.extend(names)
                Nums.extend(nums)
            ###########################
            dic=dict(zip(Names,Nums))#临时变量,存储好友名称与新消息数量的字典
            newMessages=[]
            for key,value in dic.items():         
                newMessages.append(get_message_content(key,value,search_pages=search_pages))
            Tools.open_dialog_window(friend=filetransfer,wechat_path=wechat_path,is_maximize=True)
            newMessages_json=json.dumps(newMessages,ensure_ascii=False,indent=4)
            if close_wechat:
                main_window.close()
            return newMessages_json

    else:#有持续时间,需要在指定时间内一直遍历,最终返回结果
        if not scrollable:#聊天列表不足12人以上,会话列表没有满,没有滑块，不用遍历,直接原地等待即可
            duration=match_duration(duration)
            if not duration:#不是指定形式的duration报错
                main_window.close()
                raise TimeNotCorrectError
            start_time=time.time()
            while True:#一直等待直到时间差超过durtation
                if time.time()-start_time>=duration:
                    break
            if not chatsButton.legacy_properties().get('Value'):#文件传输助手界面原地等待duration后如果侧边栏的消息按钮还是没有红色消息提示直接返回未查找到新消息
                if close_wechat:
                    main_window.close()
                return '未查找到新消息'
            names,nums=record()#侧边栏消息按钮有红色消息提示,直接在当前的会话列表内record
            Names.extend(names)
            Nums.extend(nums)
            dic=dict(zip(Names,Nums))#临时变量,存储好友名称与新消息数量的字典
            newMessages=[]
            for key,value in dic.items(): 
                newMessages.append(get_message_content(key,value,search_pages=search_pages))
            Tools.open_dialog_window(friend=filetransfer,wechat_path=wechat_path,is_maximize=True)
            newMessages_json=json.dumps(newMessages,ensure_ascii=False,indent=4)
            if close_wechat:
                main_window.close()
            return newMessages_json
        else:
            chatsButton=main_window.child_window(**SideBar.Chats)
            x,y=messageList.rectangle().right-5,messageList.rectangle().top+8
            mouse.click(coords=(x,y))#点击右上方激活滑块
            pyautogui.press('Home')
            pyautogui.press('End')
            lastmemberName=messageList.items()[-1].window_text()
            pyautogui.press('Home')#按下Home健确保从顶部开始
            duration=match_duration(duration)
            if not duration:
                main_window.close()
                raise TimeNotCorrectError
            start_time=time.time()
            while True:#y一直原地等待,直到时间差超过duration
                if time.time()-start_time>=duration:
                    break
            if not chatsButton.legacy_properties().get('Value'):
                if close_wechat:
                    main_window.close()
                return '未查找到新消息'
            while messageList.items()[-1].window_text()!=lastmemberName:
                names,nums=record()
                if names and nums:
                    Names.extend(names)
                    Nums.extend(nums)
                pyautogui.press('pagedown',_pause=False)
                search_pages+=1
            pyautogui.press('Home')
            #################
            #回到顶部后,再查找一下顶部,以防在向下遍历会话列表时顶部有好友给发消息,没检测到
            names,nums=record()
            if names and nums:
                Names.extend(names)
                Nums.extend(nums)
            #################
            dic=dict(zip(Names,Nums))#临时变量,存储好友名称与新消息数量的字典
            newMessages=[]
            for key,value in dic.items():         
                newMessages.append(get_message_content(key,value,search_pages=search_pages))
            Tools.open_dialog_window(friend=filetransfer,wechat_path=wechat_path,is_maximize=True)
            newMessages_json=json.dumps(newMessages,ensure_ascii=False,indent=4)
            if close_wechat:
                main_window.close()
            return newMessages_json


def auto_reply_messages(content:str,duration:str,dontReplyGroup:bool=False,max_pages:int=5,never_reply:list=[],scroll_delay:int=0,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来遍历会话列表查找新消息自动回复,最大回复数量=max_pages*(8~10)\n
    如果你不想回复某些好友,你可以临时将其设为消息免打扰,或传入\n
    一个包含不回复好友或群聊的昵称列表never_reply\n
    Args:
        content:\t自动回复内容\n
        duration:\t自动回复持续时长,格式:'s','min','h'单位:s/秒,min/分,h/小时\n
        dontReplyGroup:\t不回复群聊(即使有新消息也不回复)\n
        max_pages:\t遍历会话列表页数,一页为8~10人,设定持续时间后,将持续在max_pages内循环遍历查找是否有新消息\n
        never_reply:\t在never_reply列表中的好友即使有新消息时也不会回复\n
        scroll_delay:\t滚动遍历max_pages页会话列表后暂停秒数,如果你的max_pages很大,且持续时间长,scroll_delay还为0的话,那么一直滚动遍历有可能被微信检测到自动退出登录\n
               该参数只在会话列表可以滚动的情况下生效\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    if language=='简体中文':
        taboo_list=['微信团队','微信支付','微信运动','订阅号','腾讯新闻','服务通知']
    if language=='繁体中文':
        taboo_list=['微信团队','微信支付','微信运动','訂閱賬號','騰訊新聞','服務通知']
    if language=='英文':
        taboo_list=['微信团队','微信支付','微信运动','Subscriptions','Tencent News','Service Notifications']
    taboo_list.extend(never_reply)
    responsed_friend=set()
    responsed_groups=set()
    unchanged_duration=duration
    duration=match_duration(duration)
    if not duration:
        raise TimeNotCorrectError
    Systemsettings.open_listening_mode(volume=False)
    Systemsettings.copy_text_to_windowsclipboard(content)
    def record():
        #遍历当前会话列表内的所有成员，获取他们的名称和新消息条数，没有新消息的话返回[],[]
        #newMessagefriends为会话列表(List)中所有含有新消息的ListItem
        newMessagefriends=[friend for friend in messageList.children() if '条新消息' in friend.window_text()]
        if newMessagefriends:
            #newMessageTips为newMessagefriends中每个元素的文本:['测试365 5条新消息','一家人已置顶20条新消息']这样的字符串列表
            newMessageTips=[friend.window_text() for friend in newMessagefriends]
            #会话列表中的好友具有Text属性，Text内容为备注名，通过这个按钮的名称获取好友名字
            names=[friend.descendants(control_type='Text')[0].window_text() for friend in newMessagefriends]
            return names
        return []

    #监听并且回复右侧聊天界面
    def listen_on_current_chat():
        voice_call_button=main_window.child_window(**Buttons.VoiceCallButton)
        video_call_button=main_window.child_window(**Buttons.VideoCallButton)
        current_chat=main_window.child_window(**Main_window.CurrentChatWindow)
        #判断好友类型
        if video_call_button.exists() and voice_call_button.exists():#好友
            type='好友'
        if not video_call_button.exists() and voice_call_button.exists():#好友
            type='群聊'
        if not video_call_button.exists() and not voice_call_button.exists():#好友
            type='非好友'
        #自动回复逻辑
        if type=='好友' and current_chat.window_text() not in taboo_list:
            latest_message,who=Tools.pull_latest_message(chatlist)#最新的消息
            if who==current_chat.window_text() and latest_message!=initial_last_message:#不等于刚打开页面时的那条消息且发送者是对方
                current_chat.click_input()
                pyautogui.hotkey('ctrl','v',_pause=False)
                pyautogui.hotkey('alt','s',_pause=False)
                responsed_friend.add(current_chat.window_text())
                if scorllable:
                    mouse.click(coords=(x+2,y-6))#点击右上方激活滑块
        if type=='群聊' and current_chat.window_text() not in taboo_list:
            latest_message,who=Tools.pull_latest_message(chatlist)#最新的消息
            if latest_message!=initial_last_message and who!=myname:
                if not dontReplyGroup:
                    current_chat.click_input()
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    pyautogui.hotkey('alt','s',_pause=False)
                    responsed_friend.add(current_chat.window_text())
                    responsed_groups.add(current_chat.window_text())
                    if scorllable:
                        mouse.click(coords=(x+2,y-6))#点击右上方激活滑块

    #用来回复在会话列表中找到的头顶有红色数字新消息提示的好友
    def reply(names):
        names=[name for name in names if name not in taboo_list]#tabool_list是传入的never_reply和我这里定义的的一些不回复对象,比如'微信运动','微信支付'灯
        if names:
            for name in names:       
                Tools.find_friend_in_MessageList(friend=name,search_pages=search_pages,is_maximize=is_maximize)
                voice_call_button=main_window.child_window(**Buttons.VoiceCallButton)
                video_call_button=main_window.child_window(**Buttons.VideoCallButton)
                #判断好友类型
                if video_call_button.exists() and voice_call_button.exists():#好友
                    type='好友'
                if not video_call_button.exists() and voice_call_button.exists():#好友
                    type='群聊'
                if not video_call_button.exists() and not voice_call_button.exists():#好友
                    type='非好友'
                if type=='好友':#有语音聊天按钮不是公众号,不用关注
                    current_chat=main_window.child_window(**Main_window.CurrentChatWindow)
                    current_chat.click_input()
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    pyautogui.hotkey('alt','s',_pause=False)
                    responsed_friend.add(name) 
                if type=='群聊' and not dontReplyGroup:
                        current_chat=main_window.child_window(**Main_window.CurrentChatWindow)
                        current_chat.click_input()
                        pyautogui.hotkey('ctrl','v',_pause=False)
                        pyautogui.hotkey('alt','s',_pause=False)
                        responsed_friend.add(name)
                        responsed_groups.add(name)
            if scorllable:
                mouse.click(coords=(x,y))#回复完成后点击右上方,激活滑块，继续遍历会话列表

    main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    chat_button=main_window.child_window(**SideBar.Chats)
    chat_button.click_input()
    myname=main_window.child_window(control_type='Button',found_index=0).window_text()
    chatlist=main_window.child_window(**Main_window.FriendChatList)#聊天界面内存储所有聊天信息的消息列表
    initial_last_message=Tools.pull_latest_message(chatlist)[0]#刚打开聊天界面时的最后一条消息的listitem 
    messageList=main_window.child_window(**Main_window.ConversationList)#左侧的会话列表
    scorllable=Tools.is_VerticalScrollable(messageList)#只调用一次is_VerticallyScrollable函数来判断会话列表是否可以滚动
    x,y=messageList.rectangle().right-5,messageList.rectangle().top+8#右上方滑块的位置
    if scorllable:
        mouse.click(coords=(x,y))#点击右上方激活滑块
        pyautogui.press('Home')#按下Home健确保从顶部开始
    search_pages=1
    start_time=time.time()
    chatsButton=main_window.child_window(**SideBar.Chats)
    while time.time()-start_time<=duration:
        if chatsButton.legacy_properties().get('Value'):#如果左侧的聊天按钮式红色的就遍历,否则原地等待
            if scorllable:
                for _ in range(max_pages+1):
                    names=record()
                    reply(names)
                    names.clear()
                    pyautogui.press('pagedown',_pause=False)
                    search_pages+=1
                pyautogui.press('Home')
                time.sleep(scroll_delay)
            else:
                names=record()
                reply(names)
                names.clear()
        listen_on_current_chat()
    Systemsettings.close_listening_mode()
    if responsed_friend:
        print(f"在{unchanged_duration}内回复了以下好友\n{responsed_friend}")
        if responsed_groups:
            print(f"回复的群聊有\n{responsed_groups}")
    if close_wechat:
        main_window.close()

def AI_auto_reply_to_friend(friend:str,duration:str,AI_engine,save_chat_history:bool=False,capture_screen:bool=False,folder_path:str=None,search_pages:int=5,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来接入AI大模型自动回复好友消息\n
    Args:
        friend:\t好友或群聊备注\n
        duration:\t自动回复持续时长,格式:'s','min','h'单位:s/秒,min/分,h/小时\n
        Ai_engine:\t调用的AI大模型API函数,去各个大模型官网找就可以\n
        search_pages:\t在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏法搜索好友信息打开聊天界面\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    if save_chat_history and capture_screen and folder_path:#需要保存自动回复后的聊天记录截图时，可以传入一个自定义文件夹路径，不然保存在运行该函数的代码所在文件夹下
        #当给定的文件夹路径下的内容不是一个文件夹时
        if not Systemsettings.is_dirctory(folder_path):#
            raise NotFolderError(r'给定路径不是文件夹!无法保存聊天记录截图,请重新选择文件夹！')
    def get_latest_chat_history():#获取聊天界面内的聊天记录
        #筛选消息，每条消息都是一个listitem
        if chatlist.children():
            ###################
            chats=[message for message in chatlist.children(control_type='ListItem') if not re.findall(r'\d\d:\d\d',message.window_text())]
            chats=[item for item in chats if item.window_text()!='查看更多消息']
            chats=[item for item in chats if '撤回了一条消息' not in item.window_text()]
            chats=[item for item in chats if '以下是新消息' not in item.window_text()]
            chats=[item for item in chats if item.children()[0].children()!=[]]
            ##################
            if chats:#如果有聊天记录
                who=chats[-1].descendants(control_type='Button')[0].window_text()
                return chats,who#返回的chats不是文本,是listitem
        return [None],None#此时的聊天界面是一片空白,可能是刚刚清空过聊天记录
    duration=match_duration(duration)#将's','min','h'转换为秒
    if not duration:#有SB不按照指定的时间格式输入,需要提前中断退出
        raise TimeNotCorrectError
    #打开好友的对话框,返回值为编辑消息框和主界面
    chat,main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize,search_pages=search_pages)
    #有SB想自动回复微信支付这样的公众号,需要判断一下是不是公众号
    voice_call_button=main_window.child_window(**Buttons.VoiceCallButton)
    video_call_button=main_window.child_window(**Buttons.VideoCallButton)
    if not voice_call_button.exists():
        #公众号没有语音聊天按钮
        main_window.close()
        raise CantReplyToOfficialAccountError
    if video_call_button.exists() and voice_call_button.exists():
        type='好友'
    if not video_call_button.exists() and voice_call_button.exists():
        type='群聊'
        myname=main_window.child_window(control_type='Button',found_index=0).window_text()#自己的名字
    #####################################################################################
    chatlist=main_window.child_window(**Main_window.FriendChatList)#聊天界面内存储所有信息的容器
    initial_last_message=get_latest_chat_history()[0][-1]#刚打开聊天界面时的最后一条消息的listitem   
    Systemsettings.open_listening_mode(volume=False)#开启监听模式,此时电脑只要不断电不会息屏 
    count=0
    start_time=time.time()  
    while True:
        if time.time()-start_time<duration:#在指定时间内
            chats,who=get_latest_chat_history()
            #消息列表内的最后一条消息(listitem)不等于刚打开聊天界面时的最后一条消息(listitem)
            #并且最后一条消息的发送者是好友时自动回复
            #这里我们判断的是两条消息(listitem)是否相等,不是文本是否相等,要是文本相等的话,对方一直重复发送
            #刚打开聊天界面时的最后一条消息的话那就一直不回复了
            if type=='好友':
                if chats[-1]!=initial_last_message and who==friend:
                    chat.click_input()
                    Systemsettings.copy_text_to_windowsclipboard(AI_engine(chats[-1].window_text()))#复制回复内容到剪贴板
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    pyautogui.hotkey('alt','s',_pause=False)
                    count+=1  
            if type=='群聊':
                if chats[-1]!=initial_last_message and who!=myname:
                    chat.click_input()
                    Systemsettings.copy_text_to_windowsclipboard(AI_engine(chats[-1].window_text()))#复制回复内容到剪贴板
                    pyautogui.hotkey('ctrl','v',_pause=False)
                    pyautogui.hotkey('alt','s',_pause=False)
                    count+=1
        else:
            break
    if count:
        if save_chat_history:
            chat_history=get_chat_history(friend=friend,number=int(1.5*count),capture_screen=capture_screen,folder_path=folder_path,wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)  
            return chat_history
    Systemsettings.close_listening_mode()
    if close_wechat:
        main_window.close()


def Change_Language(lang:int=0,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    该函数用来PC微信修改语言。\n
    Args:
        lang:\t语言名称,只支持简体中文,English,繁体中文,使用0,1,2表示。\n
        wechat_path:\t微信的WeChat.exe文件地址,主要针对未登录情况而言,一般而言不需要传入该参数,因为pywechat会通过查询环境变量,注册表等一些方法\n
            尽可能地自动找到微信路径,然后实现无论PC微信是否启动都可以实现自动化操作,除非你的微信路径手动修改过,发生了变动的话可能需要\n
            传入该参数。最后,还是建议加入到环境变量里吧,这样方便一些。加入环境变量可调用set_wechat_as_environ_path函数\n
        is_maximize:\t微信界面是否全屏,默认全屏。\n
        close_wechat:\t任务结束后是否关闭微信,默认关闭\n
    '''
    language_map={0:'简体中文',1:'英文',2:'繁体中文'}
    if language_map[lang]==language:
        raise WrongParameterError(f'当前微信语言已经为{language},无需更换为{language_map[lang]}')
    settings=Tools.open_settings(wechat_path=wechat_path,is_maximize=is_maximize,close_wechat=close_wechat)
    general=settings.child_window(**TabItems.GeneralTabItem)
    general.click_input()
    message_combo_button=settings.child_window(**Texts.LanguageText).parent().children()[1]
    message_combo_button.click_input()
    message_combo=settings.child_window(class_name='ComboWnd')
    if lang==0:
        listitem=message_combo.child_window(control_type='ListItem',found_index=0)
        listitem.click_input()
    if lang==1:
        listitem=message_combo.child_window(control_type='ListItem',found_index=1)
        listitem.click_input()
    if lang==2:
        listitem=message_combo.child_window(control_type='ListItem',found_index=2)
        listitem.click_input()
    confirm_button=settings.child_window(**Buttons.ConfirmButton)
    confirm_button.click_input()

