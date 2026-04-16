import pyautogui


def osk():
    pyautogui.hotkey('win', 'ctrl', 'o')

def click():
    pyautogui.click()

def right_click():
    pyautogui.rightClick()

def middle_click():
    pyautogui.middleClick()

def double_click():
    pyautogui.doubleClick()

def none():
    pass

def nexttrack():
    pyautogui.press('nexttrack')

def prevtrack():
    pyautogui.press('prevtrack')

def printscr():
    pyautogui.press('printscr')

def win():
    pyautogui.press('win')

def delete():
    pyautogui.press('Delete')

def browserback():
    pyautogui.press('browserback')

def browserforward():
    pyautogui.press('browserforward')

def browserrefresh():
    pyautogui.press('browserrefresh')

def pageup():
    pyautogui.press('pageup')

def pagedown():
    pyautogui.press('pagedown')

def volumeup():
    pyautogui.press('volumeup')

def volumedown():
    pyautogui.press('volumedown')

def volumemute():
    pyautogui.press('volumemute')

def esc():
    pyautogui.press('esc')

def func_from_str(s: str):
    str_to_key = {'Next Track': nexttrack, 'Prev Track': prevtrack, 'Print Screen': printscr, 'Windows': win, 'Delete': delete, 'Browser Back': browserback,
                      'Browser Forward': browserforward, 'Browser Refresh': browserrefresh, 'Page Up': pageup, 'Page Down': pagedown, 'Volume Up': volumeup,
                      'Volume Down': volumedown, 'Mute': volumemute, 'Escape': esc, 'On Screen Keyboard': osk, 'Left Click': click, 'Right Click': right_click,
                      'Middle Click': middle_click, 'Double Click': double_click, 'None': none}
    return str_to_key[s]
