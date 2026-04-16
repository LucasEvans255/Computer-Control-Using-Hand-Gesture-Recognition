import tkinter as tk
from config import Config


def invalid_int_win():
    """
    Opens a window informing the user that they have entered an invalid value
    """
    error_win = tk.Tk()
    l = tk.Label(error_win, text='Enter a valid positive integer')
    l.grid(row=0, column=0)
    error_win.mainloop()

def valid_int(val: tk.StringVar) -> bool:
    """
    Returns True if the value given is a positive integer, otherwise opens a window telling the user of the error, and returns False
    """
    try:
        if int(val.get()) < 0:
            invalid_int_win()
            return False
        return True
    except ValueError:
        invalid_int_win()
        return False
        
def assign_val_if_valid(field: str, config: Config, val: tk.StringVar) -> int:
    """
    If the value is a valid integer, it writes it into the config object and returns 0
    If invalid returns -1
    """
    if valid_int(val):
        config.json_dict[field] = val.get()
        return 0
    else:
        return -1

def save_changes(vals: list[tk.StringVar], config: Config, win: tk.Tk):
    """
    Saves the changes to the config file if the width and height values are positive integers
    If the changes are invalid, none will be saved
    """
    print(config.path)
    print(config.json_dict['device'])
    config.json_dict['device'] = vals[0].get()
    print(config.json_dict['device'])
    if assign_val_if_valid('cam_width', config, vals[1]) == -1:
        return
    if assign_val_if_valid('cam_height', config, vals[2]) == -1:
        return
            
    for i in range(3, len(vals)):
        # label_to_button starts at 0, but the settings to be stored in them starts at vals[3]
        config.json_dict['label_to_button'][str(i - 3)] = vals[i].get()

    config.save()
    win.destroy()

def edit_config_win(label_to_str: Config, config: Config):
    """
    Creates the window where the user can edit their config settings
    """
    N = max([int(key) for key in label_to_str.json_dict.keys()]) + 1

    root = tk.Tk()

    device_label = tk.Label(root, text='Device')
    device_label.grid(row=0, column=0)
    devices = ['cpu', 'cuda']
    device = tk.StringVar()
    device.set(config.json_dict['device'])
    device_menu = tk.OptionMenu(root, device, *devices)
    device_menu.grid(row=0, column=1)

    width_label = tk.Label(root, text='Webcam width')
    width_label.grid(row=1, column=0)
    width = tk.StringVar()
    width.set(config.json_dict['cam_width'])
    width_entry = tk.Entry(root, textvariable=width)
    width_entry.grid(row=1, column=1)

    height_label = tk.Label(root, text='Webcam height')
    height_label.grid(row=2, column=0)
    height = tk.StringVar()
    height.set(config.json_dict['cam_height'])
    height_entry = tk.Entry(root, textvariable=height)
    height_entry.grid(row=2, column=1)

    gesture_options = ['Next Track', 'Prev Track', 'Print Screen', 'Windows', 'Delete', 
                       'Browser Back', 'Browser Forward', 'Browser Refresh', 'Page Up', 
                       'Page Down', 'Volume Up', 'Volume Down', 'Mute', 'Escape', 'On Screen Keyboard',
                       'Left Click', 'Right Click', 'Middle Click', 'Double Click', 'None']
    
    stringvars = []
    menus = []
    for i in range(N):
        l = tk.Label(root, text=f'{label_to_str.json_dict[str(i)]}')
        # I wrote this as 2 + i + 1 to make it clearer that the first 2 are already used
        # Then incrementing i increments the location of the object once
        # and the +1 exists to prevent it overlapping with the previous objects
        l.grid(row=2 + i + 1, column=0)
        var = tk.StringVar()
        stringvars.append(var)
        try:
            var.set(config.json_dict['label_to_button'][str(i)])
        except KeyError:
            var.set('None')
            config.json_dict['label_to_button'][str(i)] = 'None'
        menu = tk.OptionMenu(root, var, *gesture_options)
        menus.append(menu)
        menu.grid(row=2 + i + 1, column=1)

    vals = [device, width, height] + stringvars
    save_button = tk.Button(root, text='Save changes', command=lambda: save_changes(vals, config, root))
    save_button.grid(row=2 + N + 2, column=0)

    root.mainloop()
