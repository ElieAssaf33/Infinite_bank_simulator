import PySimpleGUI as sg
import sqlite3
from gui_balance import check_balance
from gui_investments import make_investment
from gui_loans import make_loan

main_layout = [
    [
    sg.Button('Invest', key = '-INVEST-'), 
    sg.Button('Loan', key = '-LOAN-'), 
    sg.Button('Balance', key = '-BALANCE-'), 
    sg.Button('Exit', key='-EXIT-')
    ],
]

main_window = sg.Window(
    'Infinite', 
    main_layout, 
    size=(400,100), 
    element_justification='center', 
    element_padding=10, 
    font = 'Arial 23',
    finalize=True
)

while True:
    event, values = main_window.read(timeout=0.1)
    if event in [sg.WINDOW_CLOSED, "-EXIT-"]:
        break
    if event == '-INVEST-':
        make_investment(main_window)
    if event == '-LOAN-':
        make_loan(main_window)
    if event == '-BALANCE-':
        check_balance(main_window)



 