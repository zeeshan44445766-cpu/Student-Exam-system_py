# FINAL COMPLETE ONLINE EXAM SYSTEM (GUI + MYSQL + BEAUTIFUL DESIGN)

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import random
from datetime import datetime


# =====================================================
# DATABASE CLASS
# =====================================================
class Database:

    def __init__(self):

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Zeeshan143$",
            database="online_exam"
        )

        self.cursor = self.conn.cursor()


    # -------------------------------------------------
    # ADD RESULT
    # -------------------------------------------------
    def add_result(self, result):

        query = """
        INSERT INTO results
        (student_name, exam_title, marks, percentage, grade, exam_date)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (
            result.user.name,
            result.exam.title,
            result.marks,
            result.calculate_percentage(),
            result.calculate_grade(),
            result.date
        )

        self.cursor.execute(query, values)
        self.conn.commit()


    # -------------------------------------------------
    # GET RESULTS
    # -------------------------------------------------
    def get_results(self):

        self.cursor.execute("SELECT * FROM results")
        return self.cursor.fetchall()


    # -------------------------------------------------
    # ADD QUESTION
    # -------------------------------------------------
    def add_question(self, question, a, b, c, d, correct):

        query = """
        INSERT INTO questions
        (question, option_a, option_b, option_c, option_d, correct_answer)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (
            question,
            a,
            b,
            c,
            d,
            correct.upper()
        )

        self.cursor.execute(query, values)
        self.conn.commit()


    # -------------------------------------------------
    # GET QUESTIONS
    # -------------------------------------------------
    def get_questions(self):

        self.cursor.execute("SELECT * FROM questions")
        return self.cursor.fetchall()


    # -------------------------------------------------
    # DELETE QUESTION
    # -------------------------------------------------
    def delete_question(self, qid):

        query = "DELETE FROM questions WHERE id=%s"

        self.cursor.execute(query, (qid,))
        self.conn.commit()


    # -------------------------------------------------
    # UPDATE QUESTION
    # -------------------------------------------------
    def update_question(self, qid, new_question):

        query = """
        UPDATE questions
        SET question=%s
        WHERE id=%s
        """

        self.cursor.execute(query, (new_question, qid))
        self.conn.commit()


# =====================================================
# USER CLASS
# =====================================================
class User:

    def __init__(self, user_id, name, username, password):

        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password


# =====================================================
# QUESTION CLASS
# =====================================================
class Question:

    def __init__(self, text, options, correct):

        self.text = text
        self.options = options
        self.correct = correct


    def check_answer(self, ans):

        return ans.upper() == self.correct.upper()


# =====================================================
# EXAM CLASS
# =====================================================
class Exam:

    def __init__(self, title, questions):

        self.title = title
        self.questions = questions


# =====================================================
# RESULT CLASS
# =====================================================
class Result:

    def __init__(self, user, exam, marks):

        self.user = user
        self.exam = exam
        self.marks = marks
        self.date = datetime.now()


    def calculate_percentage(self):

        return (self.marks / len(self.exam.questions)) * 100


    def calculate_grade(self):

        p = self.calculate_percentage()

        if p >= 80:
            return "A"

        elif p >= 60:
            return "B"

        elif p >= 40:
            return "C"

        else:
            return "F"


# =====================================================
# LOAD QUESTIONS
# =====================================================
def load_questions(db):

    records = db.get_questions()

    qlist = []

    for row in records:

        q = Question(
            row[1],
            {
                "A": row[2],
                "B": row[3],
                "C": row[4],
                "D": row[5]
            },
            row[6]
        )

        qlist.append(q)

    return qlist


# =====================================================
# GUI APPLICATION
# =====================================================
class ExamGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Online Exam System")
        self.root.geometry("1100x700")
        self.root.config(bg="#111827")

        self.db = Database()

        self.questions = []
        self.q_index = 0
        self.score = 0

        self.show_main_menu()


    # =================================================
    # CLEAR SCREEN
    # =================================================
    def clear(self):

        for widget in self.root.winfo_children():
            widget.destroy()


    # =================================================
    # MAIN MENU
    # =================================================
    def show_main_menu(self):

        self.clear()

        self.root.configure(bg="#111827")

        tk.Label(
            self.root,
            text="🎓 ONLINE EXAM SYSTEM",
            font=("Arial", 34, "bold"),
            bg="#111827",
            fg="#38bdf8"
        ).pack(pady=50)


        tk.Label(
            self.root,
            text="GUI Based Examination Project",
            font=("Arial", 16),
            bg="#111827",
            fg="white"
        ).pack()


        btn_font = ("Arial", 16, "bold")


        tk.Button(
            self.root,
            text="🧑‍🎓 Student Exam",
            width=22,
            height=2,
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            font=btn_font,
            bd=5,
            cursor="hand2",
            command=self.student_login
        ).pack(pady=25)


        tk.Button(
            self.root,
            text="👨‍💼 Admin Panel",
            width=22,
            height=2,
            bg="#3b82f6",
            fg="white",
            activebackground="#2563eb",
            font=btn_font,
            bd=5,
            cursor="hand2",
            command=self.admin_login
        ).pack(pady=25)


        tk.Button(
            self.root,
            text="❌ Exit",
            width=22,
            height=2,
            bg="#ef4444",
            fg="white",
            activebackground="#dc2626",
            font=btn_font,
            bd=5,
            cursor="hand2",
            command=self.root.quit
        ).pack(pady=25)


    # =================================================
    # STUDENT LOGIN
    # =================================================
    def student_login(self):

        self.clear()

        self.root.configure(bg="#1e293b")

        tk.Label(
            self.root,
            text="🧑‍🎓 STUDENT LOGIN",
            font=("Arial", 28, "bold"),
            bg="#1e293b",
            fg="#38bdf8"
        ).pack(pady=30)


        frame = tk.Frame(self.root, bg="#334155", padx=40, pady=40)
        frame.pack(pady=20)


        tk.Label(frame, text="Name", font=("Arial", 14), bg="#334155", fg="white").grid(row=0, column=0, pady=10)
        self.name_entry = tk.Entry(frame, width=30, font=("Arial", 14))
        self.name_entry.grid(row=0, column=1, pady=10)


        tk.Label(frame, text="Username", font=("Arial", 14), bg="#334155", fg="white").grid(row=1, column=0, pady=10)
        self.username_entry = tk.Entry(frame, width=30, font=("Arial", 14))
        self.username_entry.grid(row=1, column=1, pady=10)


        tk.Label(frame, text="Password", font=("Arial", 14), bg="#334155", fg="white").grid(row=2, column=0, pady=10)
        self.password_entry = tk.Entry(frame, show="*", width=30, font=("Arial", 14))
        self.password_entry.grid(row=2, column=1, pady=10)


        tk.Button(
            self.root,
            text="🚀 Start Exam",
            bg="#22c55e",
            fg="white",
            font=("Arial", 16, "bold"),
            width=18,
            height=2,
            bd=5,
            cursor="hand2",
            command=self.start_exam
        ).pack(pady=20)


        tk.Button(
            self.root,
            text="⬅ Back",
            bg="#64748b",
            fg="white",
            font=("Arial", 14, "bold"),
            width=15,
            bd=5,
            cursor="hand2",
            command=self.show_main_menu
        ).pack()


    # =================================================
    # START EXAM
    # =================================================
    def start_exam(self):

        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.student = User(1, name, username, password)

        self.questions = load_questions(self.db)

        random.shuffle(self.questions)

        self.exam = Exam("Online Quiz", self.questions)

        self.q_index = 0
        self.score = 0

        self.show_question()


    # =================================================
    # SHOW QUESTION
    # =================================================
    def show_question(self):

        self.clear()

        self.root.configure(bg="#0f172a")

        if self.q_index >= len(self.questions):
            self.show_result()
            return


        q = self.questions[self.q_index]


        tk.Label(
            self.root,
            text=f"Question {self.q_index + 1}",
            font=("Arial", 24, "bold"),
            bg="#0f172a",
            fg="#38bdf8"
        ).pack(pady=20)


        tk.Label(
            self.root,
            text=q.text,
            font=("Arial", 18),
            bg="#0f172a",
            fg="white",
            wraplength=800
        ).pack(pady=20)


        self.answer_var = tk.StringVar()


        for key, value in q.options.items():

            tk.Radiobutton(
                self.root,
                text=f"{key}. {value}",
                variable=self.answer_var,
                value=key,
                font=("Arial", 16),
                bg="#1e293b",
                fg="white",
                selectcolor="#334155",
                width=40,
                pady=10
            ).pack(pady=8)


        tk.Button(
            self.root,
            text="Next ➡",
            bg="#3b82f6",
            fg="white",
            font=("Arial", 16, "bold"),
            width=15,
            height=2,
            bd=5,
            cursor="hand2",
            command=self.next_question
        ).pack(pady=30)


    # =================================================
    # NEXT QUESTION
    # =================================================
    def next_question(self):

        ans = self.answer_var.get()

        q = self.questions[self.q_index]

        if q.check_answer(ans):
            self.score += 1

        self.q_index += 1

        self.show_question()


    # =================================================
    # SHOW RESULT
    # =================================================
    def show_result(self):

        self.clear()

        self.root.configure(bg="#111827")

        result = Result(self.student, self.exam, self.score)

        self.db.add_result(result)


        tk.Label(
            self.root,
            text="🏆 EXAM RESULT",
            font=("Arial", 32, "bold"),
            bg="#111827",
            fg="#22c55e"
        ).pack(pady=30)


        tk.Label(
            self.root,
            text=f"Student: {self.student.name}",
            font=("Arial", 20),
            bg="#111827",
            fg="white"
        ).pack(pady=10)


        tk.Label(
            self.root,
            text=f"Marks: {self.score}/{len(self.questions)}",
            font=("Arial", 20),
            bg="#111827",
            fg="white"
        ).pack(pady=10)


        tk.Label(
            self.root,
            text=f"Percentage: {result.calculate_percentage():.2f}%",
            font=("Arial", 20),
            bg="#111827",
            fg="white"
        ).pack(pady=10)


        tk.Label(
            self.root,
            text=f"Grade: {result.calculate_grade()}",
            font=("Arial", 22, "bold"),
            bg="#111827",
            fg="#38bdf8"
        ).pack(pady=20)


        tk.Button(
            self.root,
            text="⬅ Main Menu",
            bg="#3b82f6",
            fg="white",
            font=("Arial", 16, "bold"),
            width=18,
            height=2,
            bd=5,
            cursor="hand2",
            command=self.show_main_menu
        ).pack(pady=30)


    # =================================================
    # ADMIN LOGIN
    # =================================================
    def admin_login(self):

        self.clear()

        self.root.configure(bg="#1e293b")

        tk.Label(
            self.root,
            text="👨‍💼 ADMIN LOGIN",
            font=("Arial", 28, "bold"),
            bg="#1e293b",
            fg="#f59e0b"
        ).pack(pady=40)


        tk.Label(self.root, text="Username", font=("Arial", 14), bg="#1e293b", fg="white").pack()
        self.admin_user = tk.Entry(self.root, width=30, font=("Arial", 14))
        self.admin_user.pack(pady=10)


        tk.Label(self.root, text="Password", font=("Arial", 14), bg="#1e293b", fg="white").pack()
        self.admin_pass = tk.Entry(self.root, show="*", width=30, font=("Arial", 14))
        self.admin_pass.pack(pady=10)


        tk.Button(
            self.root,
            text="Login",
            bg="#f59e0b",
            fg="white",
            font=("Arial", 16, "bold"),
            width=15,
            bd=5,
            cursor="hand2",
            command=self.check_admin
        ).pack(pady=30)


    # =================================================
    # CHECK ADMIN
    # =================================================
    def check_admin(self):

        if self.admin_user.get() == "admin" and self.admin_pass.get() == "1234":
            self.admin_panel()
        else:
            messagebox.showerror("Error", "Wrong Credentials")


    # =================================================
    # ADMIN PANEL
    # =================================================
    def admin_panel(self):

        self.clear()

        self.root.configure(bg="#0f172a")

        tk.Label(
            self.root,
            text="⚡ ADMIN CONTROL PANEL ⚡",
            font=("Arial", 30, "bold"),
            bg="#0f172a",
            fg="#38bdf8"
        ).pack(pady=30)


        font_style = ("Arial", 14, "bold")


        tk.Button(self.root, text="➕ Add Question", width=25, height=2,
                  font=font_style, bg="#22c55e", fg="white",
                  bd=5, cursor="hand2",
                  command=self.add_question_screen).pack(pady=12)


        tk.Button(self.root, text="📄 View Questions", width=25, height=2,
                  font=font_style, bg="#3b82f6", fg="white",
                  bd=5, cursor="hand2",
                  command=self.view_questions).pack(pady=12)


        tk.Button(self.root, text="❌ Remove Question", width=25, height=2,
                  font=font_style, bg="#ef4444", fg="white",
                  bd=5, cursor="hand2",
                  command=self.delete_question_screen).pack(pady=12)


        tk.Button(self.root, text="✏ Update Question", width=25, height=2,
                  font=font_style, bg="#f59e0b", fg="white",
                  bd=5, cursor="hand2",
                  command=self.update_question_screen).pack(pady=12)


        tk.Button(self.root, text="🏆 View Results", width=25, height=2,
                  font=font_style, bg="#8b5cf6", fg="white",
                  bd=5, cursor="hand2",
                  command=self.view_results).pack(pady=12)


        tk.Button(self.root, text="⬅ Back", width=25, height=2,
                  font=font_style, bg="#64748b", fg="white",
                  bd=5, cursor="hand2",
                  command=self.show_main_menu).pack(pady=20)


    # =================================================
    # ADD QUESTION SCREEN
    # =================================================
    def add_question_screen(self):

        self.clear()

        self.root.configure(bg="#111827")

        tk.Label(self.root, text="➕ ADD QUESTION",
                 font=("Arial", 28, "bold"),
                 bg="#111827", fg="#22c55e").pack(pady=20)


        labels = [
            "Question",
            "Option A",
            "Option B",
            "Option C",
            "Option D",
            "Correct Answer"
        ]

        self.entries = []

        for text in labels:

            tk.Label(self.root, text=text,
                     font=("Arial", 14),
                     bg="#111827", fg="white").pack()

            entry = tk.Entry(self.root, width=70, font=("Arial", 13))
            entry.pack(pady=8)

            self.entries.append(entry)


        tk.Button(self.root,
                  text="Save Question",
                  bg="#22c55e",
                  fg="white",
                  font=("Arial", 14, "bold"),
                  width=20,
                  bd=5,
                  command=self.save_question).pack(pady=20)


    # =================================================
    # SAVE QUESTION
    # =================================================
    def save_question(self):

        q = self.entries[0].get()
        a = self.entries[1].get()
        b = self.entries[2].get()
        c = self.entries[3].get()
        d = self.entries[4].get()
        ans = self.entries[5].get()

        self.db.add_question(q, a, b, c, d, ans)

        messagebox.showinfo("Success", "Question Added Successfully")

        self.admin_panel()


    # =================================================
    # VIEW QUESTIONS
    # =================================================
    def view_questions(self):

        self.clear()

        rows = self.db.get_questions()

        tree = ttk.Treeview(
            self.root,
            columns=("ID", "Question", "Correct"),
            show="headings"
        )

        tree.heading("ID", text="ID")
        tree.heading("Question", text="Question")
        tree.heading("Correct", text="Correct")

        tree.pack(fill="both", expand=True)

        for row in rows:
            tree.insert("", "end", values=(row[0], row[1], row[6]))


        tk.Button(self.root,
                  text="⬅ Back",
                  bg="#64748b",
                  fg="white",
                  font=("Arial", 12, "bold"),
                  command=self.admin_panel).pack(pady=10)


    # =================================================
    # DELETE QUESTION SCREEN
    # =================================================
    def delete_question_screen(self):

        self.clear()

        tk.Label(self.root,
                 text="❌ DELETE QUESTION",
                 font=("Arial", 26, "bold"),
                 bg="#111827",
                 fg="#ef4444").pack(pady=20)


        rows = self.db.get_questions()

        tree = ttk.Treeview(
            self.root,
            columns=("ID", "Question"),
            show="headings"
        )

        tree.heading("ID", text="ID")
        tree.heading("Question", text="Question")

        tree.pack(fill="both", expand=True)

        for row in rows:
            tree.insert("", "end", values=(row[0], row[1]))


        tk.Label(self.root,
                 text="Enter Question ID",
                 font=("Arial", 14),
                 bg="#111827",
                 fg="white").pack(pady=10)


        self.delete_id_entry = tk.Entry(self.root, width=20, font=("Arial", 14))
        self.delete_id_entry.pack()


        tk.Button(self.root,
                  text="Delete",
                  bg="#ef4444",
                  fg="white",
                  font=("Arial", 14, "bold"),
                  width=15,
                  bd=5,
                  command=self.delete_question).pack(pady=15)


    # =================================================
    # DELETE QUESTION
    # =================================================
    def delete_question(self):

        qid = self.delete_id_entry.get()

        self.db.delete_question(qid)

        messagebox.showinfo("Success", "Question Deleted")

        self.admin_panel()


    # =================================================
    # UPDATE QUESTION SCREEN
    # =================================================
    def update_question_screen(self):

        self.clear()

        tk.Label(self.root,
                 text="✏ UPDATE QUESTION",
                 font=("Arial", 26, "bold"),
                 bg="#111827",
                 fg="#f59e0b").pack(pady=20)


        tk.Label(self.root,
                 text="Question ID",
                 bg="#111827",
                 fg="white",
                 font=("Arial", 14)).pack()

        self.update_id = tk.Entry(self.root, width=20, font=("Arial", 14))
        self.update_id.pack(pady=10)


        tk.Label(self.root,
                 text="New Question",
                 bg="#111827",
                 fg="white",
                 font=("Arial", 14)).pack()

        self.new_question_entry = tk.Entry(self.root, width=70, font=("Arial", 14))
        self.new_question_entry.pack(pady=10)


        tk.Button(self.root,
                  text="Update",
                  bg="#f59e0b",
                  fg="white",
                  font=("Arial", 14, "bold"),
                  width=15,
                  bd=5,
                  command=self.update_question).pack(pady=20)


    # =================================================
    # UPDATE QUESTION
    # =================================================
    def update_question(self):

        qid = self.update_id.get()
        new_q = self.new_question_entry.get()

        self.db.update_question(qid, new_q)

        messagebox.showinfo("Success", "Question Updated")

        self.admin_panel()


    # =================================================
    # VIEW RESULTS
    # =================================================
    def view_results(self):

        self.clear()

        rows = self.db.get_results()

        tree = ttk.Treeview(
            self.root,
            columns=("ID", "Student", "Exam", "Marks", "Percentage", "Grade"),
            show="headings"
        )

        headings = ["ID", "Student", "Exam", "Marks", "Percentage", "Grade"]

        for h in headings:
            tree.heading(h, text=h)

        tree.pack(fill="both", expand=True)

        for row in rows:

            tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                )
            )


        tk.Button(self.root,
                  text="⬅ Back",
                  bg="#64748b",
                  fg="white",
                  font=("Arial", 12, "bold"),
                  command=self.admin_panel).pack(pady=10)


# =====================================================
# RUN APPLICATION
# =====================================================
root = tk.Tk()

app = ExamGUI(root)

root.mainloop()








