cat << 'EOF' > main.py
import ast
import sys
import traceback
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

Window.clearcolor = (0.95, 0.95, 0.95, 1)

class CodeAnalyzerApp(App):
    def build(self):
        self.title = "Python Code & Error Analyzer"
        layout = BoxLayout(orientation="vertical", padding=15, spacing=10)

        header = Label(
            text="Python Error Assistant",
            font_size="22sp",
            bold=True,
            size_hint_y=None,
            height=40,
            color=(0.1, 0.1, 0.1, 1),
        )
        layout.add_widget(header)

        self.code_input = TextInput(
            text='# এখানে আপনার Python কোড লিখুন\nprint("Hello World")\n\n# একটি ভুলের উদাহরণ:\n# print(hello)',
            multiline=True,
            font_size="16sp",
            size_hint_y=0.5,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
        )
        layout.add_widget(self.code_input)

        run_btn = Button(
            text="Run & Analyze Code",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1),
        )
        run_btn.bind(on_press=self.analyze_and_run)
        layout.add_widget(run_btn)

        scroll = ScrollView(size_hint_y=0.4)
        self.output_label = Label(
            text="ফলাফল এখানে দেখাবে...",
            font_size="16sp",
            size_hint_y=None,
            color=(0.2, 0.2, 0.2, 1),
            halign="left",
            valign="top",
        )
        self.output_label.bind(
            size=lambda instance, value: setattr(
                instance, "text_size", (value[0], None)
            )
        )
        self.output_label.bind(
            minimum_height=self.output_label.setter("height")
        )

        scroll.add_widget(self.output_label)
        layout.add_widget(scroll)

        return layout

    def analyze_and_run(self, instance):
        user_code = self.code_input.text

        try:
            ast.parse(user_code)
        except SyntaxError as e:
            self.output_label.color = (0.8, 0.1, 0.1, 1)
            self.output_label.text = (
                f"❌ [Syntax Error - কাঠামোগত ভুল]\n\n"
                f"📌 ভুল লাইন: {e.lineno}\n"
                f"⚠️ সমস্যা: কোডের গঠনে বা বানানে ভুল আছে।\n"
                f"💡 টিপস: কোটেশন (' '), ব্র্যাকেট, Colon (:) বা ইন্ডেন্টেশন (স্পেস) ঠিক আছে কিনা চেক করুন।"
            )
            return

        try:
            import io
            buffer = io.StringIO()
            sys.stdout = buffer

            exec(user_code, {"__builtins__": __builtins__})

            sys.stdout = sys.__stdout__
            output = buffer.getvalue()

            self.output_label.color = (0.1, 0.6, 0.1, 1)
            self.output_label.text = f"✅ [সফলভাবে রান হয়েছে!]\n\nOutput:\n{output}"

        except Exception as e:
            sys.stdout = sys.__stdout__
            exc_type, exc_value, exc_tb = sys.exc_info()
            last_tb = traceback.extract_tb(exc_tb)[-1]

            error_name = exc_type.__name__
            line_no = last_tb.lineno

            error_explanations = {
                "NameError": "এমন একটি Variable বা Function ব্যবহার করা হয়েছে যা আগে ডিফাইন করা হয়নি।",
                "ZeroDivisionError": "কোনো সংখ্যাকে ০ (শূন্য) দিয়ে ভাগ করার চেষ্টা করা হয়েছে।",
                "TypeError": "অনুপযুক্ত Data Type-এর ওপর কাজ করার চেষ্টা করা হয়েছে।",
                "IndentationError": "কোডের লাইনের শুরুতে সঠিক পরিমাণ স্পেস দেওয়া হয়নি।",
                "IndexError": "List-এর সীমার বাইরের কোনো পজিশন/ইনডেক্স কল করা হয়েছে।",
            }

            explanation = error_explanations.get(
                error_name, f"সমস্যা: {str(e)}"
            )

            self.output_label.color = (0.8, 0.1, 0.1, 1)
            self.output_label.text = (
                f"❌ [{error_name} - রানটাইম ভুল]\n\n"
                f"📌 ভুল লাইন: {line_no}\n"
                f"⚠️ কারণ: {explanation}\n"
                f"💡 সমাধান: লাইন নম্বর {line_no}-এর লজিক ও ইনপুট আবার পরীক্ষা করুন।"
            )

if __name__ == "__main__":
    CodeAnalyzerApp().run()
EOF
