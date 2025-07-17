import PySimpleGUI as sg
import csv
import os

# Theme and font
sg.theme("DarkGrey1")
sg.set_options(font="Arial 16")

# Layout
layout = [
    [sg.Text('Enter your first name'), sg.Text('', expand_x=True), sg.InputText(key='-fname-')],
    [sg.Text('Enter your last name'), sg.Text('', expand_x=True), sg.InputText(key='-lname-')],
    [sg.Text('Enter your phone number'), sg.Text('', expand_x=True), sg.InputText(key='-phone-')],
    [sg.Text('Enter your email'), sg.Text('', expand_x=True), sg.InputText(key='-email-')],
    [sg.Text('Enter your address'), sg.Text('', expand_x=True), sg.InputText(key='-address-')],
    [sg.Button('Save'), sg.Button('Cancel')],
    [sg.HorizontalSeparator()],
    [sg.Text('Search/Delete by Last Name'), sg.Text('', expand_x=True), sg.InputText(key='-searchText-')],
    [sg.Text('Phone (for delete)'), sg.Text('', expand_x=True), sg.InputText(key='-deletePhone-')],
    [sg.Button('Search'), sg.Button('Delete')],
    [sg.Text('', key='-searchOutput-', size=(50, 6), text_color='black')]
]

# Window
window = sg.Window('Contact Book', layout, icon='favicon.ico')

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    fname = values['-fname-'].strip()
    lname = values['-lname-'].strip()
    phone = values['-phone-'].strip()
    email = values['-email-'].strip()
    address = values['-address-'].strip()
    info = [fname, lname, phone, email, address]

    # ✅ SAVE
    if event == 'Save':
        if not all(info):
            sg.popup_error('Please fill in all fields before saving.')
            continue
        if not phone.isdigit():
            sg.popup_error('Phone number must contain only digits.')
            continue
        if '@' not in email or '.' not in email:
            sg.popup_error('Please enter a valid email address.')
            continue

        with open('info.csv', 'a', newline="") as w:
            cw = csv.writer(w)
            cw.writerow(info)
        sg.popup_ok('Contact saved successfully!')

        for key in ['-fname-', '-lname-', '-phone-', '-email-', '-address-']:
            window[key].update('')

    # ✅ SEARCH
    if event == 'Search':
        searchText = values['-searchText-'].strip()
        if not searchText:
            sg.popup_error('Please enter a Last Name to search.')
            continue

        if not os.path.exists('info.csv'):
            window['-searchOutput-'].update('No records found. (File does not exist)')
            continue

        found = False
        with open('info.csv', 'r') as r:
            cr = csv.reader(r)
            for i in cr:
                if i[1].lower() == searchText.lower():
                    window['-searchOutput-'].update(
                        f'First name: {i[0]}\nLast name: {i[1]}\nPhone: {i[2]}\nEmail: {i[3]}\nAddress: {i[4]}'
                    )
                    found = True
                    break
        if not found:
            window['-searchOutput-'].update('No record found.')

    # ✅ DELETE
    if event == 'Delete':
        delete_last = values['-searchText-'].strip()
        delete_phone = values['-deletePhone-'].strip()

        if not delete_last or not delete_phone:
            sg.popup_error('Please enter both Last Name and Phone Number to delete.')
            continue

        if not os.path.exists('info.csv'):
            sg.popup_error('No records found. (File does not exist)')
            continue

        rows = []
        deleted = False

        with open('info.csv', 'r') as r:
            cr = csv.reader(r)
            for row in cr:
                if row[1].lower() == delete_last.lower() and row[2] == delete_phone:
                    deleted = True
                    continue  # Skip this record (delete it)
                rows.append(row)

        if deleted:
            with open('info.csv', 'w', newline="") as w:
                cw = csv.writer(w)
                cw.writerows(rows)
            sg.popup_ok('Deleted the record successfully.')
            window['-searchOutput-'].update('')
        else:
            sg.popup_ok('No matching record found.')

window.close()
