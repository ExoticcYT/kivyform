from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.core.window import Window
Window.size = (1000, 700)
from pathlib import Path

this_path = Path(__file__)
this_path_parent = this_path.parent

class RegistrationPage(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_elements = {}
        self.grid_two_elements = {}
        self.widgets_to_add = []
    
    def build(self):
        main_layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        first_grid = GridLayout(cols=2, spacing=10, row_force_default=True, row_default_height=40)
        self.widgets_to_add.append(first_grid)
        self.grid_elements = {
            "Name: ": TextInput(multiline=False),
            "Age: " : TextInput(multiline=False),
            "Gender: ": Spinner(text="Select", values=["Male", "Female"]),
            "Class/Grade: ": TextInput(multiline=False),
            "Address: ": TextInput(multiline=False),
        }
        values = []
        for element in self.grid_elements:
            label = Label(text=element)
            first_grid.add_widget(label)
            values.append(self.grid_elements[element])
            first_grid.add_widget(self.grid_elements[element])

        second_grid_title = Label(text="Subjects", size_hint_y=None, height=30)
        self.widgets_to_add.append(second_grid_title)
        second_grid = GridLayout(cols=2, spacing=5, row_force_default=True, row_default_height=40, padding=[300,0,300,0])
        self.widgets_to_add.append(second_grid)
        self.grid_two_elements = {
            "Math": CheckBox(),
            "Science": CheckBox(),
            "English": CheckBox(),
            "Computer": CheckBox(),
        }
        for element in self.grid_two_elements:
            second_grid.add_widget(self.grid_two_elements[element])
            label = Label(text=element, size_hint_y=None, height=30)
            second_grid.add_widget(label)

        submit_button = Button(text="Submit", size_hint_y=None, height=50, on_press=self.submit_data)
        self.widgets_to_add.append(submit_button)

        info_label = Label(size_hint_y=None, height=30)
        self.widgets_to_add.append(info_label)

        for widget in self.widgets_to_add:
            main_layout.add_widget(widget)
        return main_layout

    def clear_form(self):
        for element in self.grid_elements:
            if(element == "Gender: "):
                self.grid_elements[element].text = "Select"
            else:
                self.grid_elements[element].text = ""

        for checks in self.grid_two_elements:
            if(self.grid_two_elements[checks].active):
                self.grid_two_elements[checks].active = False

    def submit_data(self, instance):
        text_boxes = []
        
        name = self.grid_elements["Name: "].text
        text_boxes.append(name)
        age = self.grid_elements["Age: "].text
        text_boxes.append(age)
        gender = self.grid_elements["Gender: "].text
        if(gender == "Select"):
            text_boxes.append("")
        else:
            text_boxes.append(gender)
        grade = self.grid_elements["Class/Grade: "].text
        text_boxes.append(grade)
        address = self.grid_elements["Address: "].text
        text_boxes.append(address)
        
        selected_subjects = []
        for element in self.grid_two_elements:
            if self.grid_two_elements[element].active:
                selected_subjects.append(element)

        if "" in text_boxes or len(selected_subjects)<1:
            self.widgets_to_add[-1].text = "Please fill all boxes"
        else:
            try:
                with open(f"{this_path_parent}/students.txt", "a") as f:
                    line = ""
                    for text in text_boxes:
                        line = line+text+", "
                    for subject in selected_subjects:
                        line = line+subject+", "
                    f.write(line+"\n")
                self.widgets_to_add[-1].text = f"Thank you {name}! Your data was saved."
                self.clear_form()
            except Exception:
                self.widgets_to_add[-1].text = "An error took place, try again"

if __name__=="__main__":
    RegistrationPage().run()