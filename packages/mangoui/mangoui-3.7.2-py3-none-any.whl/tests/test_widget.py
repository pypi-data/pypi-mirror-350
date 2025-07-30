from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Hello, Kivy!')
        self.button = Button(text='Click Me!')

        self.button.bind(on_press=self.on_button_click)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)

        return self.layout

    def on_button_click(self, instance):
        self.label.text = 'Button Clicked!'


if __name__ == '__main__':
    MyApp().run()
