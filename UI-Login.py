from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock

# Login Screen
class LoginScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.screen_manager = screen_manager

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Login to BidMasters', font_size=24, size_hint=(1, 0.2)))

        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input = TextInput(hint_text='Password', multiline=False, password=True)
        login_btn = Button(text='Login', on_press=self.validate_user)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_btn)
        self.status_label = Label(text='', size_hint=(1, 0.1))
        layout.add_widget(self.status_label)

        self.add_widget(layout)

    def validate_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username and password:
            self.screen_manager.current = 'auction'
        else:
            self.status_label.text = 'Invalid username or password.'

# Auction Screen
class AuctionUI(Screen):
    def __init__(self, **kwargs):
        super(AuctionUI, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Welcome to the Auction Platform', font_size=24, size_hint=(1, 0.1)))

        bid_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        self.bid_input = TextInput(hint_text='Enter your bid...', multiline=False)
        place_bid_btn = Button(text='Place Bid', on_press=self.place_bid)
        bid_box.add_widget(self.bid_input)
        bid_box.add_widget(place_bid_btn)
        layout.add_widget(bid_box)

        self.auction_log = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.auction_log.bind(minimum_height=self.auction_log.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 0.6))
        scroll_view.add_widget(self.auction_log)
        layout.add_widget(scroll_view)

        self.status_label = Label(text='Status: Connected', size_hint=(1, 0.1))
        layout.add_widget(self.status_label)

        quit_btn = Button(text='Quit', size_hint=(1, 0.1))
        quit_btn.bind(on_press=self.quit_app)
        layout.add_widget(quit_btn)

        self.add_widget(layout)

    def place_bid(self, instance):
        bid = self.bid_input.text
        if bid:
            self.auction_log.add_widget(Label(text=f'You placed a bid: {bid}'))
            self.bid_input.text = ''
        else:
            self.status_label.text = 'Status: Please enter a bid before submitting.'

    def quit_app(self, instance):
        Clock.schedule_once(lambda dt: App.get_running_app().stop(), 0.1)

# App with Screen Manager
class AuctionApp(App):
    def build(self):
        Window.bind(on_request_close=self.on_request_close)
        self.sm = ScreenManager()

        login_screen = LoginScreen(self.sm, name='login')
        self.sm.add_widget(login_screen)

        auction_screen = AuctionUI(name='auction')
        self.sm.add_widget(auction_screen)

        self.sm.current = 'login'
        return self.sm

    def on_request_close(self, *args):
        Clock.schedule_once(lambda dt: App.get_running_app().stop(), 0.1)
        return False

if __name__ == '__main__':
    AuctionApp().run()
