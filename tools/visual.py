def on_enter_left(e):
    e.widget['background'] = 'gray14'
    e.widget['foreground'] = 'white'
    e.widget['activebackground'] = 'gray14'
    e.widget['activeforeground'] = 'white'


def on_leave_left(e):
    e.widget['background'] = 'gray10'
    e.widget['foreground'] = 'orange'


def on_enter_exit(e):
    e.widget['background'] = 'red'
    e.widget['foreground'] = 'white'
    e.widget['activebackground'] = 'red'
    e.widget['activeforeground'] = 'white'


def on_leave_exit(e):
    e.widget['background'] = 'gray20'
    e.widget['foreground'] = 'orange'
