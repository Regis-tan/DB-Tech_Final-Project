#MODULES
import customtkinter as TK
import mysql.connector

#DB CONNECTION
connection = mysql.connector.connect(
    user = "root",
    password = input("Enter root password:"),
    host = "127.0.0.1",
    database = "ums_db"
)

#PARAMETERS
HEIGHT = 500
WIDTH = 850
TITLE = "UMS - Admin"
CLR_BACKGROUND = "#fcfafd"
CLR_PRIMARY = "#00dfa2"
CLR_SECONDARY = "#e8f0fe"
CLR_TERTIARY = "#66ecc7"
CLR_TEXT = "#5c6a79"

APP = TK.CTk(fg_color=CLR_BACKGROUND)
APP.geometry(f"{WIDTH}x{HEIGHT}")
APP.resizable(False, False)
APP.title(TITLE)

#BUDGET INFORMATION SCHEMA
#note for later: [column name, name sake]
COLUMN_INFO = {
    "CLASS_COL": [["classId", "Class ID"], ["staffId", "Lecturer ID"], ["courseId", "Course ID"]],
    "COURSE_COL": [["courseId", "Course ID"], ["courseName", "Course Name"], ["credit", "Credit"]],
    "DEPARTMENT_COL": [["departmentId", "Dept. ID"], ["departmentName", "Dept. Name"]],
    "ENROLLMENT_COL": [["enrollId", "Enroll ID"], ["classId", "Class ID"], ["studentId", "Student ID"], ["enrollDate", "Enroll Date"], ["enrollAvailable", "Available Enroll Date"]],
    "PROGRAM_COL": [["programId", "Prog. ID"], ["programName", "Prog. Name"], ["departmentId", "Dept. ID"], ["degree", "Degree"]],
    "SCHEDULE_COL": [["scheduleId", "Schedule ID"], ["enrollId", "Enroll ID"], ["day", "Day"], ["time", "Time"]],
    "STAFF_COL": [["staffId", "Staff ID"], ["departmentId", "Dept. ID"], ["staffName", "Staff Name"], ["position", "Position"], ["DOB", "DOB"], ["gender", "Gender"], ["phoneNo", "Phone No."]],
    "STUDENT_COL": [["studentId", "Student ID"], ["studentName", "Student Name"], ["gender", "Gender"], ["programId", "Prog. Id"], ["DOB", "DOB"], ["entryDate", "Entry Date"],  ["phoneNo", "Phone No."], ["email", "E-mail"], ["gpa", "GPA"]]
}

global CURRENT_TABLE
CURRENT_TABLE = "Class"
global CURRENT_FORM
CURRENT_FORM = "Delete"

#GENERAL FUNCTIONS
def widget_remover(parent):
    for widget in parent.winfo_children():
        widget.destroy()

#INPUT FUNCTIONS
def set_form_delete():
    global CURRENT_FORM
    CURRENT_FORM = "Delete"

    widget_remover(INPUT_FRAME)
    def delete_function(id):
        input_field.delete(0, "end")
        try:
            pk = COLUMN_INFO[f"{CURRENT_TABLE.upper()}_COL"][0][0]
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {CURRENT_TABLE.lower()} WHERE {pk} = {id}")
            connection.commit()
        except Exception as e:
            debug_label = TK.CTkLabel(INPUT_FRAME, text=e, font=("Arial", 10), wraplength=180, justify="left", text_color="red")
            debug_label.pack(anchor="nw", padx=10, pady=10)
        finally:
            cursor.close()

    label = TK.CTkLabel(INPUT_FRAME, text="ID to Remove", font=("Arial", 15), text_color=CLR_TEXT)
    input_field = TK.CTkEntry(INPUT_FRAME, width=150, placeholder_text="Enter data", corner_radius=5, fg_color=CLR_SECONDARY, text_color=CLR_TEXT)
    submit = TK.CTkButton(INPUT_FRAME, width=80, text="Drop Data", corner_radius=10, fg_color=CLR_SECONDARY, hover_color="white", border_width=2, text_color=CLR_TEXT, command=lambda:delete_function(input_field.get()))

    label.pack(anchor="nw", pady=(10, 1), padx=10)
    input_field.pack(anchor="nw", padx=10)
    submit.pack(anchor="n", pady=10)

def set_form_add():
    global CURRENT_FORM
    CURRENT_FORM = "Add"

    widget_remover(INPUT_FRAME)
    column_data = COLUMN_INFO[f"{CURRENT_TABLE.upper()}_COL"][1:]
    entries = []

    def add_function():
        column_name = []
        for column in column_data:
            column_name.append(column[0])

        entry_outputs = []
        for entry in entries:
            try:
                int(entry.get())
                entry_outputs.append(entry.get())
            except:
                try:
                    float(entry.get())
                    entry_outputs.append(entry.get())
                except:
                    entry_outputs.append(f'"{entry.get()}"')

            try:
                entry.delete(0, "end")
            except:
                pass
        
        try:
            cursor = connection.cursor()

            string_cols = ", ".join(column_name)
            string_outs = ", ".join(entry_outputs)
            
            cursor.execute(f'INSERT INTO {CURRENT_TABLE.lower()}({string_cols}) VALUES({string_outs});')
            connection.commit()
        except Exception as e:
            debug_label = TK.CTkLabel(INPUT_FRAME, text=e, font=("Arial", 10), wraplength=180, justify="left", text_color="red")
            debug_label.pack(anchor="nw", padx=10, pady=10)
        finally:
            cursor.close()

    for column in column_data:
        label = TK.CTkLabel(INPUT_FRAME, text=column[1], font=("Arial", 15), text_color=CLR_TEXT)
        if column[1] != "Gender":
            entry = TK.CTkEntry(INPUT_FRAME, width=150, placeholder_text="Enter data", corner_radius=5, fg_color=CLR_SECONDARY, text_color=CLR_TEXT)
        else:
            entry = TK.CTkComboBox(INPUT_FRAME, width=150, values=["M", "F", "O"], fg_color=CLR_SECONDARY, border_color="black" ,button_color=CLR_PRIMARY, button_hover_color=CLR_TERTIARY, dropdown_fg_color=CLR_TERTIARY, text_color=CLR_TEXT, dropdown_text_color=CLR_TEXT, state="readonly")
            entry.set("M")
        entries.append(entry)

        label.pack(anchor="nw", pady=(10, 1), padx=10)
        entry.pack(anchor="nw", padx=10)
    
    submit = TK.CTkButton(INPUT_FRAME, width=80, text="Insert Data", corner_radius=10, fg_color=CLR_SECONDARY, hover_color="white", border_width=2, text_color=CLR_TEXT, command=add_function)
    submit.pack(anchor="n", pady=10)

def set_form_update():
    global CURRENT_FORM
    CURRENT_FORM = "Update"

    widget_remover(INPUT_FRAME)
    column_data = COLUMN_INFO[f"{CURRENT_TABLE.upper()}_COL"]
    entries = []

    def update_function():
        column_name = []
        for column in column_data:
            column_name.append(column[0])

        entry_outputs = []
        for entry in entries:
            try:
                int(entry.get())
                entry_outputs.append(entry.get())
            except:
                entry_outputs.append(f'"{entry.get()}"')

            try:
                entry.delete(0, "end")
            except:
                pass

        try:
            cursor = connection.cursor()

            set_values = []

            for column in column_name[1:]:
                set_values.append(f"{column} = {entry_outputs[column_name.index(column)]}")

            joined_set_values = ", ".join(set_values)
            
            cursor.execute(f"UPDATE {CURRENT_TABLE.lower()} SET {joined_set_values} WHERE {column_name[0]} = {entry_outputs[0]};")
            connection.commit()
        except Exception as e:
            debug_label = TK.CTkLabel(INPUT_FRAME, text=e, font=("Arial", 10), wraplength=180, justify="left", text_color="red")
            debug_label.pack(anchor="nw", padx=10, pady=10)
        finally:
            cursor.close()

    for column in column_data:
        label = TK.CTkLabel(INPUT_FRAME, text=column[1], font=("Arial", 15), text_color=CLR_TEXT)
        if column[1] != "Gender":
            entry = TK.CTkEntry(INPUT_FRAME, width=150, placeholder_text="Enter data", corner_radius=5, fg_color=CLR_SECONDARY, text_color=CLR_TEXT)
        else:
            entry = TK.CTkComboBox(INPUT_FRAME, width=150, values=["M", "F", "O"], fg_color=CLR_SECONDARY, border_color="black" ,button_color=CLR_PRIMARY, button_hover_color=CLR_TERTIARY, dropdown_fg_color=CLR_TERTIARY, text_color=CLR_TEXT, dropdown_text_color=CLR_TEXT, state="readonly")
            entry.set("M")
        entries.append(entry)

        label.pack(anchor="nw", pady=(10, 1), padx=10)
        entry.pack(anchor="nw", padx=10)
    
    submit = TK.CTkButton(INPUT_FRAME, width=80, text="Update Data", corner_radius=10, fg_color=CLR_SECONDARY, hover_color="white", border_width=2, text_color=CLR_TEXT, command=update_function)
    submit.pack(anchor="n", pady=10)

#DASHBOARD FUNCTIONS
def update_table_frame(data):
    widget_remover(TABLE_FRAME)

    for col_num, info in enumerate(data[0]):
        info_frame = TK.CTkFrame(TABLE_FRAME, fg_color="#d1d8e5", corner_radius=2)
        info_label = TK.CTkLabel(info_frame, text=info, anchor="center", font=("Arial", 15), text_color=CLR_TEXT)
        
        info_frame.grid(row=0, column=col_num, padx=2, pady=4, sticky="ew")
        info_label.pack(anchor="center",padx=2, pady=2)

    for row_num, row in enumerate(data[1:], start=1):
        for col_num, value in enumerate(row):
            content_frame = TK.CTkFrame(TABLE_FRAME, fg_color="#d1d8e5", corner_radius=6)
            content = TK.CTkLabel(content_frame, text=value, anchor="center", font=("Arial", 10), text_color=CLR_TEXT)

            content_frame.grid(row=row_num, column=col_num, padx=2, pady=2, sticky="ew")
            content.pack(anchor="center", padx=10, pady=2)

def update_table(table):
    global CURRENT_TABLE
    CURRENT_TABLE = table
    info_row = []
    data = []

    for list in COLUMN_INFO[f"{CURRENT_TABLE.upper()}_COL"]:
        info_row.append(list[1])

    data.append(info_row)

    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {CURRENT_TABLE.lower()};")

        data.extend(cursor.fetchall())
        update_table_frame(data)
    except Exception as e:
        print(f"Error Occured: {e}")
    finally:
        cursor.close()

    if CURRENT_FORM == "Delete":
        set_form_delete()
    elif CURRENT_FORM  == "Add":
        set_form_add()
    elif CURRENT_FORM == "Update":
        set_form_update()

def update_form(form):
    if form == "Delete":
        set_form_delete()
    elif form == "Add":
        set_form_add()
    elif form == "Update":
        set_form_update()

def search_table(id):
    global CURRENT_TABLE
    info_row = []
    data = []

    for list in COLUMN_INFO[f"{CURRENT_TABLE.upper()}_COL"]:
        info_row.append(list[1])

    data.append(info_row)

    try:
        cursor = connection.cursor()

        current_table_id = COLUMN_INFO[f"{CURRENT_TABLE.upper()}_COL"][0][0]

        cursor.execute(f"SELECT * FROM {CURRENT_TABLE.lower()} WHERE {current_table_id} = {id};")

        data.extend(cursor.fetchall())
        update_table_frame(data)
    except Exception as e:
        print(f"Error Occured: {e}")
    finally:
        cursor.close()

#UI
SIDEBAR = TK.CTkFrame(APP, width=250, corner_radius=0, border_color="black", border_width=1, fg_color=CLR_PRIMARY)
username = TK.CTkLabel(SIDEBAR, text="User:\nPlaceholder\nAdmin", font=("Arial", 20, "bold"), text_color=CLR_TEXT, justify="left")
sidebar_seperator = TK.CTkFrame(SIDEBAR, width=200, height=1, bg_color="black")

INPUT_FRAME = TK.CTkScrollableFrame(SIDEBAR, width=220, height=350, fg_color=CLR_TERTIARY)

dashboard_label = TK.CTkLabel(APP, text="Dashboard", font=("Arial", 30, "bold"), text_color=CLR_TEXT, justify="left")
dashboard_seperator = TK.CTkFrame(APP, width=200, height=1, bg_color="black")
OPTION_FRAME = TK.CTkFrame(APP, fg_color="transparent")
table_dropdown = TK.CTkComboBox(OPTION_FRAME, values=["Class", "Staff", "Department", "Course", "Enrollment", "Student", "Program", "Schedule"], fg_color=CLR_SECONDARY, border_color=CLR_PRIMARY ,button_color=CLR_PRIMARY, button_hover_color=CLR_TERTIARY, dropdown_fg_color=CLR_TERTIARY, text_color=CLR_TEXT, dropdown_text_color=CLR_TEXT, state="readonly", command=update_table)
input_dropdown = TK.CTkComboBox(OPTION_FRAME, values=["Delete", "Add", "Update"], fg_color=CLR_SECONDARY, border_color=CLR_PRIMARY ,button_color=CLR_PRIMARY, button_hover_color=CLR_TERTIARY, dropdown_fg_color=CLR_TERTIARY, text_color=CLR_TEXT, dropdown_text_color=CLR_TEXT, state="readonly", command=update_form)
refresh_button = TK.CTkButton(OPTION_FRAME, fg_color=CLR_PRIMARY, text="Refresh", font=("Arial", 15), text_color=CLR_TEXT, width=30, hover_color=CLR_TERTIARY, command=lambda:update_table(CURRENT_TABLE))
search_button = TK.CTkButton(OPTION_FRAME, fg_color=CLR_PRIMARY, text=">", font=("Arial", 18, "bold"), text_color=CLR_TEXT, width=30, hover_color=CLR_TERTIARY, command=lambda:search_table(search_row.get()))
search_row = TK.CTkEntry(OPTION_FRAME, width=100, placeholder_text="Search by ID", corner_radius=5, fg_color=CLR_SECONDARY, text_color=CLR_TEXT, border_color=CLR_PRIMARY)

H_FRAME = TK.CTkScrollableFrame(APP, orientation="horizontal", fg_color=CLR_SECONDARY, width=650, height=400)
TABLE_FRAME = TK.CTkScrollableFrame(H_FRAME, fg_color=CLR_SECONDARY, width = 800)

#PACKING
SIDEBAR.pack(side="left", fill="y")
SIDEBAR.pack_propagate(False)

username.pack(anchor="nw", padx=10, pady=10)
sidebar_seperator.pack(side="top")

INPUT_FRAME.pack(side="top", pady=10, padx=10)

dashboard_label.pack(anchor="nw", padx=20, pady=(20,1))
dashboard_seperator.pack(anchor="nw", padx=20)
OPTION_FRAME.pack(anchor="nw", padx=(20,5), pady=(30,5))
table_dropdown.pack(side="left", padx=5)
table_dropdown.set("Class")
input_dropdown.pack(side="left", padx=5)
input_dropdown.set("Delete")
refresh_button.pack(side="left", padx=5)
search_button.pack(side="right")
search_row.pack(side="right", padx=(30, 1))

H_FRAME.pack(anchor="nw", padx=20, pady=10)
TABLE_FRAME.pack(anchor="center")

update_table(CURRENT_TABLE)
update_form(CURRENT_FORM)
APP.mainloop()
