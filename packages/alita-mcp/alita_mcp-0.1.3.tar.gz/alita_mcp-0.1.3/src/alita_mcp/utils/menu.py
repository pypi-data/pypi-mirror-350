import msvcrt
import os


def show_menu(tree={}):
    lines, positions = _flat_tree_to_menu_lines(tree)

    current = 0
    selected = [True] * len(lines)
    menu_indexes = positions.keys()

    _print_menu(lines, current, selected, positions)
    while True:
        key = msvcrt.getch()
        if key == b'\xe0':  # Special keys (arrows, f keys, ins, del, etc.)
            key = msvcrt.getch()
            if key == b'H' and current > 0:  # Up arrow
                current -= 1
                _print_menu(lines, current, selected, positions)
            elif key == b'P' and current < len(lines) - 1:  # Down arrow
                current += 1
                _print_menu(lines, current, selected, positions)
        elif key == b' ':  # Space
            choice = not selected[current]
            selected[current] = choice
            if current in menu_indexes:
                # top-level menu selected
                for pos in positions[current]:
                    selected[pos] = choice
            else:
                # sub-item selected
                # find the top-level menu item and select it also
                for menu, sub_items in positions.items():
                    if current in sub_items:
                        sub_items_statuses = [selected[i] for i in sub_items]
                        selected[menu] = any(sub_items_statuses)
                        break
            _print_menu(lines, current, selected, positions)
        elif key == b'q':
            raise KeyboardInterrupt
        elif key == b'\r':  # Enter
            break

    selection = {}
    current_menu_item = lines[0]
    for (index, is_selected) in enumerate(selected):
        if is_selected:
            if index in menu_indexes:
                current_menu_item = lines[index]
                selection[current_menu_item] = []
            else:
                selection[current_menu_item].append(lines[index])

    return selection


def _print_menu(lines =[], current=0, selected=[], positions={}):
    menu_indexes = positions.keys()
    os.system('cls')

    print("Press <up>/<down> to navigate.")
    print("Press <space> to select current item.")
    print("Press <s> to select all.")
    print("Press <u> to unselect all.")
    print("Press <q> to quit.")
    print("Press <enter> to accept and proceed.\n")

    for idx, item in  enumerate(lines):
        prefix = ""
        if idx in menu_indexes:
            sub_items_statuses = [selected[i] for i in positions[idx]]
            prefix = "[x]  " if all(sub_items_statuses) else "[o]  " if any(sub_items_statuses) else "[ ]  "
        else:
            prefix = "  [x]  " if selected[idx] else "  [ ]  "
        
        if idx == current:
            print(f"> {prefix}{item}")
            # print(Fore.GREEN + f"> {prefix}  {item}" + Style.RESET_ALL)
        else:
            print(f"  {prefix}{item}")


def _flat_tree_to_menu_lines(tree):
    lines = []
    toolkit_ids = {}
    cursor = 0
    for menu, sub_items in tree.items():
        lines.append(menu)
        lines.extend(sub_items)
        toolkit_ids[cursor] = list(range(cursor + 1, cursor + len(sub_items) + 1))
        cursor += len(sub_items) + 1
    return lines, toolkit_ids