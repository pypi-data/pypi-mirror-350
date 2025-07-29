from dg_clt.screen import clear


class Menu:

    def __init__(self, title: str, menu_items: dict[str, str], selection: str = '> '):
        self.title: str = title
        self.menu_items: dict[str, str] = menu_items
        self.selection: str = selection

    def display(self):
        clear()
        print(self.title)
        print(f'{'-' * len(self.title)}\n')
        for key, value in self.menu_items.items():
            if key:
                print(f'{key}: {value}')
            else:
                print()

    def get_input(self):
        while True:
            self.display()
            user_input = input(f'\n{self.selection}')
            if user_input in self.menu_items.keys():
                return user_input
