from __future__ import annotations
from tkinter import Tk
from tkinter.ttk import Frame
import tkinter as tk
from source.course import Course, Program, User
from typing import List
import source.gui.gui_popups as gui_pop
from source import web_scraping


class CourseFrame(Frame):

    def __init__(self, course: Course, width: int, height: int, parent: Frame):
        if width <= 20:
            raise ValueError("Width must be greater than 20!")

        Frame.__init__(self,
                       master=parent,
                       width=width,
                       height=height,
                       relief='raised')

        self.course = course
        self.pack_propagate(0)

        # I don't know about the complexity of winfo_width and height so i just did this
        self._width = int(width)
        self._height = height
        self._set_frames()

    def _set_frames(self):
        self._header = Frame(self, width=self._width-4, height=14, borderwidth=0)
        self._footer = Frame(self, width=self._width-5, height=15, borderwidth=0)

        self._footer.pack_propagate(0)
        self._header.pack_propagate(0)

    def _get_labels(self) -> tuple:

        name_label = tk.Label(master=self,
                              text=self.course.get_course_name(), relief='raised')
        description_label = tk.Label(master=self, text=self.course.get_desc(),
                                     wraplength=self._width-2, justify=tk.LEFT, borderwidth=0)
        credit_label = tk.Label(master=self._footer,
                                text=str(self.course.get_credit_count()) + ' credits', relief='raised')
        code_label = tk.Label(master=self._header,
                              text=self.course.get_course_code(), relief='raised')
        type_label = tk.Label(master=self._footer,
                              text=self.course.get_course_type(), relief='raised')
        subject_label = tk.Label(master=self._footer,
                                 text=self.course.get_course_subject(), relief='raised')

        return code_label, name_label, subject_label, type_label, credit_label, description_label

    def _set_labels(self):
        code, name, subject, course_type, credit, desc = self._get_labels()

        code.pack(side='left', anchor='n')
        self._header.pack(side='top')

        name.pack(side='top', anchor='w')
        desc.pack(side='top', anchor='w')

        tags_label = tk.Label(self._footer, text='Tags:  ')
        tags_label.pack(side='left', anchor='w')

        course_type.pack(side='left', anchor='n')
        credit.pack(side='left', anchor='n', padx=5)
        subject.pack(side='left', anchor='n')
        self._footer.pack(side='top')

    def embed_course(self, column: int, row: int):
        self._set_labels()
        self.pack(side='left')


class CourseButton(tk.Button):

    def __init__(self, course: Course, width: int, height: int, applet: Applet, user: User):
        self._pixel = tk.PhotoImage(width=1, height=1)
        tk.Button.__init__(self, master=applet.mid, width=width, height=height,
                           command=lambda: self._on_press(user.get_active_courses()),
                           image=self._pixel, compound='c')
        self._course = course
        self.config(text=course.get_course_code())
        self._applet = applet

    def _on_press(self, user_active_courses: List[Course]):
        # Case 1: The course is already in user_active_courses
        if self._course in user_active_courses:
            index_to_remove = user_active_courses.index(self._course)
            user_active_courses.pop(index_to_remove)
            user_active_courses.append(self._course)
        else:
            if len(user_active_courses) == 4:
                user_active_courses.pop(0)
            user_active_courses.append(self._course)
        self._applet.update_active_courses_footer()


class ProgramButton(tk.Button):

    def __init__(self, program: Program, width: int, height: int, parent: Frame):

        # Must have reference to the pixel image
        self._pixel = tk.PhotoImage(width=1, height=1)
        tk.Button.__init__(self, master=parent, image=self._pixel, compound='c',
                           width=width, height=height, text=program.get_name(),
                           overrelief='raised', command=self._on_press)

        self._program = program
        self.status = 0

    def _on_press(self) -> None:
        for child in self.master.winfo_children():
            child.status = 0

        self.status = 1


class Applet:

    def __init__(self, user: User):
        self.user = user
        self._create_basic_app()

    def _create_basic_app(self) -> tuple:
        """ Create basic field where everything will be"""
        root = Tk()
        root.geometry("1080x720+0+0")
        # This is necessary so that we can get the correct geometry info
        root.update()
        # small_frame = Basis(root)
        self._create_basic_frames(root)
        root.update()
        self._root = root

        self._set_frames_bottom()
        self._set_header()

        self._root.mainloop()

    def _create_basic_frames(self, parent: tk.Tk) -> None:
        parent_height, parent_width = parent.winfo_height(), parent.winfo_width()
        header = Frame(parent, width=parent_width, height='50', borderwidth=1)
        unnamed = Frame(parent, width=parent_width, height='300', relief=tk.SOLID)
        bottom = Frame(parent, width=parent_width, height='370', borderwidth=1)

        # These are stable and must be made so
        f = header, unnamed, bottom
        for item in f:
            item.grid_propagate(0)

        #TODO is the in_ needed?
        header.grid(column=0, row=0)
        unnamed.grid(column=0, row=1)
        bottom.grid(column=0, row=2)

        self.header, self.bottom, self.mid = header, bottom, unnamed

    def _set_frames_bottom(self):
        bottom = self.bottom
        bottom.pack_propagate(0)
        width, height = bottom.winfo_width()//4, bottom.winfo_height()

        frame_1 = tk.Frame(master=bottom, width=width, height=height)
        frame_2 = tk.Frame(master=bottom, width=width, height=height, relief=tk.SOLID)
        frame_3 = tk.Frame(master=bottom, width=width, height=height)
        frame_4 = tk.Frame(master=bottom, width=width, height=height, relief=tk.SOLID)
        frame_1.pack(side='left')
        frame_2.pack(side='left')
        frame_3.pack(side='left')
        frame_4.pack(side='left')

    def _set_header(self):
        header = self.header
        options_segment = Frame(master=header, width=3 * int(header.winfo_width()//8), height=header.winfo_height(),
                                borderwidth=0)
        programs_segment = Frame(master=header, width=5 * int(header.winfo_width()//8), height=header.winfo_height(),
                                 relief='raised')

        header.pack_propagate(0)
        options_segment.pack(side='left', anchor='w')
        programs_segment.pack(side='left', anchor='w')

        options_segment.pack_propagate(0)
        programs_segment.grid_propagate(0)

        self._set_options_segment(options_segment)
        program_entry_frame = tk.Frame(master=options_segment)

        # Width is exact number of letters in text. Text is there so width is taken with respect to text size
        program_entry = tk.Entry(master=program_entry_frame, text='Enter Program Code', width=18)
        program_entry.insert(0, 'Enter Program Code')
        add_program_button = tk.Button(master=program_entry_frame, text="Add Program", overrelief='raised',
                                       command=lambda: self._add_program(program_entry, programs_segment))

        program_entry.pack()
        add_program_button.pack(side='top', anchor='w')
        program_entry_frame.pack(side='left', padx=5)

        self._set_programs_segment(programs_segment)

    def _set_options_segment(self, options_segment: Frame):
        credits_label = tk.Label(master=options_segment, text="Credits: ")
        credits_label.pack(side='left')

        credit_num_label = tk.Label(master=options_segment, text="0.0/20.0")
        credit_num_label.pack(side='left')

        update_button = tk.Button(master=options_segment, text='Update', overrelief='raised',
                                  command=lambda: self.update_credit_num(credit_num_label))
        update_button.pack(side='left', padx=5)

        course_entry_frame = tk.Frame(master=options_segment)

        def add_course_from_entry(course_enter: tk.Entry, applet: Applet):
            web_scraping.add_custom_course(course=course_enter.get().upper(), applet=applet)

        # Width is exact number of letters in text. Text is there so width is taken with respect to text size
        course_entry = tk.Entry(master=course_entry_frame, text='Enter Course Code', width=17)
        course_entry.insert(0, 'Enter Course Code')
        add_course_button = tk.Button(master=course_entry_frame, text="Add course",
                                      command=lambda: add_course_from_entry(course_enter=course_entry, applet=self))
        course_entry.pack()
        add_course_button.pack(side='top', anchor='w')
        course_entry_frame.pack(side='left', padx=5)

    def _set_programs_segment(self, programs_segment: Frame):
        # Need this image to work in pixels
        pixel = tk.PhotoImage(width=1, height=1)

        p_label = tk.Label(master=programs_segment, relief='raised', text='PROGRAMS: ', image=pixel, compound='c',
                           width=int(programs_segment.winfo_reqwidth()/4),
                           height=programs_segment.winfo_reqheight())
        p_label.grid()

        empty_programs = tk.Label(master=programs_segment, relief='raised', image=pixel, compound='c',
                                  width=int((programs_segment.winfo_reqwidth()/4)),
                                  height=programs_segment.winfo_reqheight())

        empty_programs1 = tk.Label(master=programs_segment, relief='raised', image=pixel, compound='c',
                                   width=int(programs_segment.winfo_reqwidth() / 4),
                                   height=programs_segment.winfo_reqheight())
        empty_programs2 = tk.Label(master=programs_segment, relief='raised', image=pixel, compound='c',
                                   width=int(programs_segment.winfo_reqwidth() / 4),
                                   height=programs_segment.winfo_reqheight())

        empty_programs.grid(row=0, column=1)
        empty_programs1.grid(row=0, column=2)
        empty_programs2.grid(row=0, column=3)

    def program_header_update(self, program_header: Frame):
        user = self.user
        user_programs = user.get_programs()
        column_adjust = len(user_programs)
        program_header.grid_slaves(row=0)[-2].grid_forget()
        program_button = ProgramButton(program=user_programs[-1], width=int(program_header.winfo_width() // 4),
                                       height=program_header.winfo_height(), parent=program_header)
        program_button.grid(row=0, column=column_adjust)

    def update_credit_num(self, credit_num_label: tk.Label):
        user = self.user
        credit_num_label['text'] = '{0}/20.0'.format(user.get_credits())

    def _add_program(self, user_input: tk.Entry, programs_segment: Frame):
        user = self.user
        program_code = user_input.get().upper()
        user_programs = user.get_programs()

        for program in user_programs:
            if program.get_name() == program_code:
                gui_pop.popup_duplicate_program()
                return False

        program = web_scraping.create_program(program_code=program_code, applet=self)
        user.add_program(program)
        self.program_header_update(programs_segment)

    def update_active_courses_footer(self):
        user = self.user
        bot = self.bottom
        for slave in bot.pack_slaves():
            slave.destroy()

        col = 0
        for course in user.get_active_courses():
            new_card = CourseFrame(course=course, width=bot.winfo_width()//4, height=bot.winfo_height(), parent=bot)
            new_card.embed_course(row=0, column=col)
            col += 1

    def update_middle_segment(self, course: Course):
        user, applet = self.user, self
        parent_frame, bot = applet.mid, applet.bottom
        width_to_add = parent_frame.winfo_width()//8
        height_to_add = parent_frame.winfo_height()//8
        courses_per_row = 7

        button_to_add = CourseButton(course=course, width=width_to_add,
                                     height=height_to_add, applet=applet, user=user)
        row_num = len(parent_frame.grid_slaves())//courses_per_row
        col_num = len(parent_frame.grid_slaves()) % courses_per_row

        button_to_add.grid(row=row_num, column=col_num)


if __name__ == '__main__':
    u = User()
    f = Applet(u)