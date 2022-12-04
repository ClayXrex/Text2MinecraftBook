# Text2MinecraftBook provides a GUI to convert text into a format that can be pasted into a Minecraft book&quill.
    # Copyright (C) 2022 ClayXrex

    #This program is free software: you can redistribute it and/or modify
    #it under the terms of the GNU General Public License as published by
    #the Free Software Foundation, either version 3 of the License, or
    #any later version.

    #This program is distributed in the hope that it will be useful,
    #but WITHOUT ANY WARRANTY; without even the implied warranty of
    #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #GNU General Public License for more details.

    #You should have received a copy of the GNU General Public License
    #along with this program.  If not, see <https://www.gnu.org/licenses/>.

import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import re
import sys

# Check if module pyautogui can be imported since it's not part of the standard library.
try:
    import pyautogui
except ModuleNotFoundError as err:
    messagebox.showerror(
        title='Error: Missing python module',
        message='Failed to import python module <pyautogui>'
    )

def construct_pages(customized_line_list):

    # Create pages by grouping 14 lines together. Put \n between lines and save as one continous string.
    line_counter = 0
    page_counter = 1
    page = ''
    pages = []
    for line in customized_line_list:
        if line_counter == 0:
            page = line
            line_counter += 1
        elif line_counter < 14:
            page = page + '\n' + line
            line_counter += 1
        else:
            pages.append(page)
            page_counter += 1
            page = line
            line_counter = 1
    if page not in pages:
        pages.append(page)

    return pages

def convert_text(text):
    if len(text) != 0: # No need to do anything if there is no text.

        char_chart = {
                    'a' :		0.053,
                    'A' :    	0.053,
                    'b' :		0.053,
                    'B' :		0.053,
                    'c' :		0.053,
                    'C'	:		0.053,
                    'd'	:		0.053,
                    'D'	:		0.053,
                    'e'	:		0.053,
                    'E' :		0.053,
                    'f'	:		0.046,
                    'F'	:		0.053,
                    'g'	:		0.053,
                    'G' :		0.053,
                    'h'	:		0.053,
                    'H'	:		0.053,
                    'i'	:		0.018,
                    'I'	:		0.036,
                    'j'	:		0.053,
                    'J'	:		0.053,
                    'k'	:		0.046,
                    'K'	:		0.053,
                    'l'	:		0.027,
                    'L'	:		0.053,
                    'm'	:		0.053,
                    'M'	:		0.053,
                    'n'	:		0.053,
                    'N'	:		0.053,
                    'o'	:		0.053,
                    'O'	:		0.053,
                    'p'	:		0.053,
                    'P'	:		0.053,
                    'q'	:		0.053,
                    'Q'	:		0.053,
                    'r' :		0.053,
                    'R'	:		0.053,
                    's'	:		0.053,
                    'S'	:		0.053,
                    't'	:		0.036,
                    'T'	:		0.053,
                    'u'	:		0.053,
                    'U'	:		0.053,
                    'v'	:		0.053,
                    'V'	:		0.053,
                    'w'	:		0.053,
                    'W'	:		0.053,
                    'x'	:		0.053,
                    'X'	:		0.053,
                    'y'	:		0.053,
                    'Y'	:		0.053,
                    'z'	:		0.053,
                    'Z'	:		0.053,
                    'ß'	:		0.053,
                    '0'	:		0.053,
                    '1'	:		0.053,
                    '2'	:		0.053,
                    '3'	:		0.053,
                    '4'	:		0.053,
                    '5'	:		0.053,
                    '6'	:		0.053,
                    '7'	:		0.053,
                    '8'	:		0.053,
                    '9'	:		0.053,
                    ' '	:		0.034,
                    '!'	:		0.018,
                    '"'	:		0.036,
                    '$'	:		0.053,
                    '%'	:		0.053,
                    '&'	:		0.053,
                    '/'	:		0.053,
                    '('	:		0.036,
                    ')'	:		0.036,
                    '='	:		0.053,
                    '?'	:		0.053,
                    '`'	:		0.027,
                    '{'	:		0.036,
                    '}'	:		0.036,
                    '['	:		0.036,
                    ']'	:		0.036,
                    '´'	:		0.027,
                    '.'	:		0.018,
                    ','	:		0.018,
                    ';'	:		0.018,
                    '-'	:		0.053,
                    '_'	:		0.053,
                    '<'	:		0.046,
                    '>'	:		0.046,
                    '^'	:		0.053,
                    '°'	:		0.046,
                    '€'	:		0.063,
                    '@'	:		0.063,
                    '#'	:		0.053,
                    "'"	:		0.018,
                    '+'	:		0.053,
                    '*'	:		0.036,
                    '~'	:		0.063,
                    '⇒' :   	0.084,
                    ':' :       0.018,
                    'ä' :       0.053,     
                    'Ä' :       0.053,  
                    'ö' :       0.053,
                    'Ö' :       0.053,
                    'ü' :       0.053,
                    'Ü' :       0.053
        }

        # Split clipboard_content into individual lines.
        line_list = text.splitlines()

        word_list = [] # Contains nested lists. Each nested list represents a line. Every entry of a nested list represents a word of that line.
        for line in line_list: # Turn each line into a nested list that contains all words.
            word_list.append(line.split(' '))

        customized_line_list = [] # Contains nested lists. Each list has the correct length to be printed as one line in a minecraft book.

        for line in word_list:
            customized_line = '' # Line in a minecraft book. Must not be longer than "1".
            line_space_counter = 0

            for index, word in enumerate(line):

                unknown_chars_and_replacement = {
                                                    '\xa0' :    ' '
                }

                # Calculate length of word.
                word_length = 0
                for char in word:

                    # Check for 'unkown' characters.
                    if char in unknown_chars_and_replacement:
                        print(f'Found {repr(char)} in unkown!')

                        replacement = unknown_chars_and_replacement[char]
                        # Save word with appropriate replacement
                        line[index] = word.replace(char, replacement)
                        # Replace char 
                        char = replacement 

                    try:
                        word_length += char_chart[char]
                    except KeyError:
                        # Notify user with pop-up
                        messagebox.showerror(
                            title='Unkown character error',
                            message=f'{repr(char)} could not be found in the character dictionary!'
                        )
                        return None

                # Check if line_space_counter + word_length + whitespace is > 1. If so save customized_line and create new line.
                if (line_space_counter + word_length + char_chart[' ']) > 1:
                    customized_line_list.append(customized_line)
                    customized_line = word + ' '
                    line_space_counter = word_length + char_chart[' ']
                else:
                    customized_line = customized_line + word + ' '
                    line_space_counter += word_length + char_chart[' ']

            # Save customized_line if the last word of the line has been reached.
            customized_line_list.append(customized_line.rstrip()) # Remove whitespace at end of the line.

        pages = construct_pages(customized_line_list)

        return pages

class TextConverter(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.title('Text2MinecraftBook')
        self.geometry('650x400')
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)

        self.create_input_frame().grid(
            column=0,
            row=0,
            padx=5,
            pady=5
        )
 
        self.create_output_frame().grid(
            column=1,
            row=0,
            padx=5,
            pady=5
        )

        self.create_convert_btn().grid(
            column=0,
            row=1,
            ipadx=10,
            ipady=10,
            padx=5,
            pady=5
        )

        self.create_navigation_frame().grid(
            column=1,
            row=1
        )

    def create_input_frame(self):

        frame = ttk.Frame(self)
        
        self.original_text_field = scrolledtext.ScrolledText(
            frame,
            height=14,
            width=30
        )
        self.original_text_field.pack()
        
        return frame

    def create_output_frame(self):
        frame = ttk.Frame(self)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self.pages_field = tkinter.Text(
            frame,
            height=14,
            width=30
        )
        self.pages_field.pack()
        self.pages_field['state'] = 'disabled'

        return frame

    def create_convert_btn(self):
        convert_btn = ttk.Button(
            self,
            text='Convert Text',
            command=self.convert_btn_clicked
        )

        return convert_btn

    def create_navigation_frame(self):

        frame = ttk.Frame(self)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        
        # Previous page btn
        self.previous_page_btn = ttk.Button(
            frame,
            text='Previous Page',
            command=self.previous_page_btn_clicked
        )
        self.previous_page_btn.grid(
            column=0,
            row=0,
        )
        self.previous_page_btn.state(['disabled'])

        # Next page btn
        self.next_page_btn = ttk.Button(
            frame,
            text='Next Page',
            command=self.next_page_btn_clicked
        )
        self.next_page_btn.grid(
            column=2,
            row=0,
        )
        self.next_page_btn.state(['disabled'])

        # Save btn
        self.save_btn = ttk.Button(
            frame,
            text='Save Pages',
            command=self.save_btn_clicked
        )
        self.save_btn.grid(
            column=2,
            row=1
        )
        self.save_btn.state(['disabled'])

        # Current page label
        self.current_page_label = ttk.Label(
            frame,
            text='Page:         '
        )
        self.current_page_label.grid(
            column=1,
            row=0
        )        

        # Go to page btn
        self.go_to_page_btn = ttk.Button(
            frame,
            text='Go to Page',
            command=self.go_to_page_btn_clicked
        )
        self.go_to_page_btn.grid(
            column=0,
            row=1
        )
        self.go_to_page_btn.state(['disabled'])

        # Page choice entry
        self.page_choice = tkinter.StringVar()
        self.page_choice_entry = ttk.Entry(
            frame,
            textvariable=self.page_choice)
        self.page_choice_entry.grid(
            column=1,
            row=1
        )
        self.page_choice_entry.state(['disabled'])

        # Paste pages btn
        self.paste_pages_btn = ttk.Button(
            frame,
            text='Paste Pages',
            command=self.paste_pages_btn_clicked
        )
        self.paste_pages_btn.grid(
            column=0,
            row=2,
        )
        self.paste_pages_btn.state(['disabled'])

        for widget in frame.winfo_children():
            widget.grid(
                ipadx=5,
                ipady=5,
                padx=5,
                pady=5,
                sticky='ew'
            )

        return frame

    def convert_btn_clicked(self):
        self.pages = convert_text(self.original_text_field.get('1.0', 'end-1c'))
        # converted_text is a list. Each entry is a complete page of a minecraft book.
        
        if self.pages != None:
            if len(self.pages) > 1:
                self.next_page_btn.state(['!disabled'])
                self.go_to_page_btn.state(['!disabled'])
                self.page_choice_entry.state(['!disabled'])
            else:
                self.next_page_btn.state(['disabled'])
                self.go_to_page_btn.state(['disabled'])
                self.page_choice_entry.state(['disabled'])
            self.save_btn.state(['!disabled'])
            self.paste_pages_btn.state(['!disabled'])

            self.page_index = 0
            self.update_current_page_label()

            self.display_page()

    def display_page(self):
        self.pages_field['state'] = 'normal'
        self.pages_field.replace('1.0', 'end', self.pages[self.page_index])
        self.pages_field['state'] = 'disabled'

    def update_current_page_label(self):
        text = 'Page: ' + ((3-len(str(self.page_index))) * ' ') + str(self.page_index + 1) + '/'  + str(len(self.pages)) + ((3-len(str(self.page_index))) * ' ')
        self.current_page_label['text'] = text
        
        # Disable previous/next page button if end of pages is reached.
        if self.page_index == 0:
            self.previous_page_btn.state(['disabled'])
            if len(self.pages) > 1:
                self.next_page_btn.state(['!disabled'])
        elif self.page_index == (len(self.pages) - 1):
            self.next_page_btn.state(['disabled'])
            self.previous_page_btn.state(['!disabled'])
        else:
            self.previous_page_btn.state(['!disabled'])
            self.next_page_btn.state(['!disabled'])

    def previous_page_btn_clicked(self):
        if self.page_index > 0: # No need to do anything if it's already the first page.
            self.page_index -= 1
            self.update_current_page_label()
            self.display_page()

    def next_page_btn_clicked(self):
        if self.page_index < (len(self.pages) - 1): # No need to do anything if it's already the last page.
            self.page_index += 1
            self.update_current_page_label()
            self.display_page()

    def go_to_page_btn_clicked(self):
        try:
            choice = int(self.page_choice.get()) # Check if entry field empty
        except ValueError:
            return

        if choice >0 and (choice -1) != self.page_index:
            try:
                self.pages[(choice-1)]
                
            except IndexError:
                return  

            self.page_index = (choice -1)
            self.display_page()
            self.update_current_page_label()      

    def save_btn_clicked(self):
        # Get save location
        save_dir = filedialog.askdirectory()

        # Save individual pages
        for index, page in enumerate(self.pages):
            # Construct file path
            path = save_dir + '/page' + str(index + 1) + '.txt'
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(page)
            except PermissionError:
                return

    def paste_pages_btn_clicked(self):

        if 'pyautogui' in sys.modules.keys():
            self.lower()
            MinecraftBookWriter(self.pages)
        else:
            # Inform user that pyautogui module is needed for this function
            messagebox.showerror(
                title='Error: Missing python module',
                message='Failed to import python module <pyautogui>.\nModule is required for this feature.'
            )

class MinecraftBookWriter(tkinter.Toplevel):

    def __init__(self, pages):
        super().__init__()

        self.pages = pages

        ttk.Label(
            self,
            text='Is the game running in the background and a book&quill opened on the page you want to start pasting in?'
        ).pack()
        ttk.Button(
            self,
            text='Confirm',
            command=self.get_turn_page_arrow_position
        ).pack()

        for widget in self.winfo_children():
            widget.pack(
                ipadx=5,
                ipady=5,
                padx=5,
                pady=5
        )

        self.turn_page_arrow_position = (None, None)
        
    def get_turn_page_arrow_position(self):

        self.title('Pick position of arrow to turn page')
        self.state('zoomed')
        self.attributes('-alpha', 0.5)
        self.bind('<Button-1>', self.confirm_turn_page_arrow_position) # Check for left mouse btn click -> Ask user to confirm position

    def confirm_turn_page_arrow_position(self, arrow_position):

        self.unbind('<Button-1>')
        arrow_position	 = str(arrow_position)
        x = int(re.search(r'x=\d+', arrow_position).group(0).removeprefix('x='))
        y = int(re.search(r'y=\d+', arrow_position).group(0).removeprefix('y='))

        self.turn_page_arrow_position = (x, y)
        print(self.turn_page_arrow_position, pyautogui.position())

        self.display_turn_page_arrow_position()

        self.confirmation_window = tkinter.Toplevel()
        self.confirmation_window.title('Confirm position of arrow to turn page')
        self.confirmation_window.geometry(f'+{self.turn_page_arrow_position[0]}+{self.turn_page_arrow_position[1]}')
        ttk.Label(self.confirmation_window, text='Happy with placement?').pack(padx=5, pady=5)
        ttk.Button(
            self.confirmation_window, 
            text='Confirm', 
            command=self.confirm_btn_clicked
        ).pack(pady=2.5)
        ttk.Button(
            self.confirmation_window,
            text='Retry', 
            command=self.retry_btn_clicked
        ).pack(pady=5)

    def display_turn_page_arrow_position(self):

        #self.title('Confirm position of arrow to turn page')
        canvas = tkinter.Canvas(self, bg='white')
        canvas.pack(fill='both', expand=True)

        # Draw X over self.turn_page_arrow_position
        top_left = (self.turn_page_arrow_position[0] - 10, self.turn_page_arrow_position[1] - 10)
        bottom_left = (self.turn_page_arrow_position[0] - 10, self.turn_page_arrow_position[1] + 10)
        top_right = (self.turn_page_arrow_position[0] + 10, self.turn_page_arrow_position[1] - 10)
        bottom_right = (self.turn_page_arrow_position[0] + 10, self.turn_page_arrow_position[1] + 10)
        
        # Line top_left -> bottom_right
        canvas.create_line(top_left, bottom_right, width=3, fill='red')

        # Line bottom_left -> top_right
        canvas.create_line(bottom_left, top_right, width=3, fill='red')

    def confirm_btn_clicked(self):

        # Close toplevel window
        self.confirmation_window.destroy()
        self.lower()
        self.paste_2_Minecraft_book()

    def retry_btn_clicked(self):
        # Close toplevel window
        self.confirmation_window.destroy()

        # Clear window
        for widget in self.winfo_children():
            widget.destroy()
        self.get_turn_page_arrow_position()

    def paste_2_Minecraft_book(self):
        pyautogui_arrow_pos = (self.turn_page_arrow_position[0], self.turn_page_arrow_position[1] + 23) # y value anomaly -> read next line comment
        # pyautogui registeres the y coordinate differently compared to tkinter
        # tkinter_y + 23 pixels == pyautogui_y 
        # Don't ask me why
        
        # Click 50 pixels above arrow to take focus of game
        pyautogui.click(pyautogui_arrow_pos[0], pyautogui_arrow_pos[1] + 50)

        # Start pasting pages
        last_page_index = len(self.pages) - 1
        for index, page in enumerate(self.pages):
            if index != last_page_index:
                pyautogui.write(page)
                pyautogui.click(pyautogui_arrow_pos[0], pyautogui_arrow_pos[1])
            else:
                pyautogui.write(page)
                
        self.destroy()

def main():
    app = TextConverter()
    app.mainloop()

if __name__ == "__main__":
    main()
