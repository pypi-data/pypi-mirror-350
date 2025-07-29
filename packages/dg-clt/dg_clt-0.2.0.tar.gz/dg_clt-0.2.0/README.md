# The Dazed Gerbil's Command Line Tools

This is intended to become a simple set of tools I use on a regular basis when developing a cli based app.

You almost certainly don't want to use this. There are probably hundreds of alternatives on PyPi already - each one notably better than my own.

Regardless, if you're determined to cause yourself pain, what does this library do? Not much so far, even less if you don't install it. Handily it's on pypi so just 'pip install dg_clt', 'uv add dg_clt', or whatever your package manager of choice requires. 

## dg_clt.screen

This little function exists out of sheer laziness on my part. All it does is clear the terminal window while remaining platform independent.

```python
import dg_clt as tdg

tdg.screen.clear()
```

The entire code to provide that function is as follows:

```python
import os

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
```

I can just never recall the line off-hand when I need it.

## dg_clt.menus

This is a simple class that will clear the screen, display a menu from data you pass in, and return the user's choice once they select a correct menu item.

The Menu class accepts a title as a string, the list of menu items as a dictionary (using a blank key to display a blank line), and a prompt to ask the user to select a menu item (optional, with a default of '> '). The user's choice will be returned as a string.

```python
import dg_clt as tdg

main_menu = tdg.menus.Menu(title='Main Menu',
                           menu_items={'1': 'First item',
                                       '2': 'Second item',
                                       '3': 'Final item',
                                       '':'',
                                       'q': 'Quit the application'},
                           selection="What's it to be? ")

user_choice = main_menu.get_input()
```
