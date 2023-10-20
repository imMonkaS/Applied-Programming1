import json
import xml.etree.ElementTree as ET


def load_data_from_json(filename):
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        raise

    return data


def save_data_to_json(data, filename):
    try:
        with open(filename, 'w') as out:
            json.dump(data, out)
    except FileNotFoundError:
        raise


class WrongNameException(Exception):
    # Raise when name is not typed correctly
    pass


class TooManyAttemptsException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Character:
    def __init__(self, hp=100, damage=20):
        self._hp = hp
        self._damage = damage
        self._alive = True

    def hp(self):
        return self._hp

    def set_hp(self, hp):
        self._hp = hp

    def damage(self):
        return self._damage

    def set_damage(self, damage):
        self._damage = damage

    def alive(self):
        return self._alive

    def set_alive_status(self, alive):
        self._alive = alive

    def death(self):
        self._hp = 0
        self._alive = False

    def attack(self, enemy):
        enemy.set_hp(enemy.hp() - self._damage)
        self.check_hp()
        if enemy.hp() == 0:
            enemy.death()

    def check_hp(self):
        if self._hp < 0:
            self._hp = 0
        elif self._hp > 100:
            self._hp = 100

    def status(self):
        return f"HP: {self._hp} ATTACK: {self._damage}"


# Main character
class MC(Character):
    def __init__(self, name, hp=100, damage=20, kill_counter=0):
        super().__init__(hp, damage)
        self.__name = name
        self.__kill_counter = kill_counter

    def heal(self):
        self._hp += 20
        self.check_hp()

    def name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def kill_counter(self):
        return self.__kill_counter

    def set_kill_counter(self, kill_counter):
        self.__kill_counter = kill_counter


# Game mob that
class Mob(Character):
    def __init__(self, hp=60, damage=5):
        super().__init__(hp, damage)


class Game:
    def __init__(self):
        self.__character = None
        self.__mobs = []

    def save_char_to_xml_file(self):
        tree = ET.parse('characters.xml')
        root = tree.getroot()
        char = root.find('characters').find(self.__character.name())
        if char is not None:  # if character has already been saved
            char.find('hp').text = str(self.__character.hp())
            char.find('damage').text = str(self.__character.damage())
            char.find('alive').text = str(self.__character.alive())
            char.find('kill_counter').text = str(self.__character.kill_counter())

            mobs = char.find('mobs_spawned')
            # obj = root.find('characters').find("dan").find('mobs_spawned')
            for sub_element in [mob for mob in mobs.iter() if 'mob' in mob.tag and '_' not in mob.tag]:
                mobs.remove(sub_element)

            for i in range(len(self.__mobs)):
                ET.SubElement(mobs, f"mob{i + 1}")
                ET.SubElement(mobs.find(f"mob{i + 1}"), 'hp')
                ET.SubElement(mobs.find(f"mob{i + 1}"), 'damage')
                mobs.find(f"mob{i + 1}").find('hp').text = str(self.__mobs[i].hp())
                mobs.find(f"mob{i + 1}").find('damage').text = str(self.__mobs[i].damage())
        else:
            ET.SubElement(root.find('characters'), self.__character.name())
            new_character = root.find('characters').find(self.__character.name())
            hp = ET.SubElement(new_character, 'hp')
            hp.text = str(self.__character.hp())

            hp = ET.SubElement(new_character, 'damage')
            hp.text = str(self.__character.damage())

            hp = ET.SubElement(new_character, 'alive')
            hp.text = str(self.__character.alive())

            hp = ET.SubElement(new_character, 'kill_counter')
            hp.text = str(self.__character.kill_counter())

            mobs_spawned = ET.SubElement(new_character, 'mobs_spawned')
            for i in range(len(self.__mobs)):
                ET.SubElement(mobs_spawned, f"mob{i + 1}")
                ET.SubElement(mobs_spawned.find(f"mob{i + 1}"), 'hp')
                ET.SubElement(mobs_spawned.find(f"mob{i + 1}"), 'damage')
                mobs_spawned.find(f"mob{i + 1}").find('hp').text = str(self.__mobs[i].hp)
                mobs_spawned.find(f"mob{i + 1}").find('damage').text = str(self.__mobs[i].damage)

        tree.write('characters.xml')
        self.menu("Your character has been saved")

    def load_character_menu_for_xml(self, from_loaded_game=False):
        tree = ET.parse('characters.xml')
        characters = [char.tag for char in tree.getroot().find('characters')]

        while True:
            print("Choose your character:")

            for i in range(len(characters)):
                print(f"{i + 1}. {characters[i]}")

            if from_loaded_game:
                print("q. Go back to main menu")
            else:
                print("q. Back to start")

            command = input()

            if command.upper() == 'Q':
                break
            elif command.isdigit() and (1 <= int(command) <= len(characters)):
                break
            else:
                print('Something went wrong. Try again')

        if command.isdigit():
            self.load_char_from_xml_file(tree, characters[int(command) - 1])

            self.menu()

        elif command.upper() == 'Q':
            if from_loaded_game:
                self.menu()
            else:
                self.start()

    def load_char_from_xml_file(self, tree, name):
        root = tree.getroot()
        char = root.find('characters').find(name)
        self.__character = MC(
            name,
            int(char.find('hp').text),
            int(char.find('damage').text),
            int(char.find('kill_counter').text),
        )
        self.__character._alive = bool(char.find('alive').text)
        mobs = char.find('mobs_spawned')
        for m in [mob for mob in mobs.iter() if 'mob' in mob.tag and '_' not in mob.tag]:
            self.__mobs.append(Mob(
                int(m.find('hp').text),
                int(m.find('damage').text)
            ))

    def start(self):
        try:
            with open('characters.json'):
                pass
        except FileNotFoundError:
            with open('characters.json', 'w') as file:
                file.write('{"characters": {}}')

        while True:
            print("Do you want to load your character? (Y/N)")
            command = input()
            if command.upper() == "Y" or command.upper() == "N":
                break
            else:
                print("Something went wrong. Try again.")

        if command.upper() == 'Y':
            self.load_character_menu_for_xml()
        else:
            data = load_data_from_json('characters.json')
            attempts = 0
            while True:
                try:
                    _name = input("Enter your character's name (3-30 symbols, no multiple spaces in a row)\n")
                    if "  " not in _name and 3 <= len(_name) <= 30 and _name not in data["characters"].keys():
                        break
                    else:
                        raise WrongNameException()
                except WrongNameException:
                    print("You did something wrong: either your character's name have too many spaces or \
it's too long, or you already have a saved character with this name. Try again.")
                    if attempts == 8:
                        raise TooManyAttemptsException("This game is just not for you, i guess...")
                attempts += 1

            if _name[0] == " ":
                _name = _name[1:]
            elif _name[-1] == " ":
                _name = _name[:-1]

            self.__character = MC(_name)
        self.menu()

    def fight(self, enemy, index):
        turn = 1
        while enemy.alive() and self.__character.alive():
            if turn % 2 != 0:  # Player's turn
                while True:
                    print("Your current status: " + self.__character.status())
                    print("Enemy status: " + enemy.status())
                    print("1. Attack")
                    print("2. Retreat")
                    command = input()
                    if command == '1' or command == '2':
                        break
                    else:
                        print("Something went wrong. Try again")

                if command == '1':
                    self.__character.attack(enemy)
                    if not enemy.alive():
                        del self.__mobs[index]
                        self.__character.set_kill_counter(self.__character.kill_counter() + 1)
                        self.menu(f"Congratulations, {self.__character.name()}! You killed it.")

                elif command == '2':
                    self.menu("You have retreated from enemy.")
            else:
                enemy.attack(self.__character)

            turn += 1

    def delete_current_character_from_xml(self):
        tree = ET.parse('characters.xml')
        root = tree.getroot()
        char = root.find('characters')

        while True:
            print(f'Are you sure you want to delete your character, "{self.__character.name()}"? (Y/N)')
            command = input()
            if command.upper() == 'Y' or command.upper() == "N":
                break
            else:
                print("Something went wrong. Try again")

        if command.upper() == "Y":
            if char.find(self.__character.name()) is not None:
                char.remove(char.find(self.__character.name()))
            else:
                self.menu("You can not delete character, that you didn't saved once.")

            tree.write('characters.xml')
            print("Your character has been wiped out.")
            self.start()
        self.menu()

    def fight_menu(self):
        print("Choose mob to fight with:")
        for el in range(len(self.__mobs)):
            print(f"Mob #{el + 1}. Enemy status: " + self.__mobs[el].status())
        while True:
            command = input()
            if command.isdigit() and (1 <= int(command) <= len(self.__mobs)):
                break
            else:
                print("Something went wrong. Try again")
        self.fight(self.__mobs[int(command) - 1], int(command) - 1)

    def menu(self, pre_text=""):
        print(pre_text)
        print(f"""\
What are you gonna do next, {self.__character.name()}?
1. Load my character
2. Save my current progress
3. Character Info
4. Heal
5. Spawn mob""")
        if len(self.__mobs) != 0:
            print("6. Fight")
        print("DEL. Delete my character")
        print("q. Exit game")

        command = input()

        if command == '1':
            self.load_character_menu_for_xml(True)

        elif command == '2':
            self.save_char_to_xml_file()

        elif command == '3':
            self.menu("Your current status: " + self.__character.status() +
                      f"\nKills: {self.__character.kill_counter()}")

        elif command == '4':
            self.__character.heal()
            self.menu("You have been healed!")

        elif command == '5':
            if len(self.__mobs) < 5:
                self.__mobs.append(Mob())
                self.menu("Mob successfully spawned")
            self.menu("You cannot have more than 5 mobs")

        elif command == '6' and len(self.__mobs) != 0:
            self.fight_menu()

        elif command == 'DEL':
            self.delete_current_character_from_xml()

        elif command == 'q':
            exit()

        else:
            self.menu("Something went wrong. Try again")


def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
