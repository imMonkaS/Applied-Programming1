import os


def save_character_to_json(self, character, filename):
    pass


def load_character_from_json(self, filename):
    pass


def save_character_to_xml(self, character, filename):
    pass


def load_character_from_xml(self, filename):
    pass


class Character:
    def __init__(self, _hp=100, _damage=20):
        self.hp = _hp
        self.damage = _damage
        self.alive = True

    def death(self):
        self.hp = 0
        self.alive = False

    def attack(self, enemy):
        enemy.hp -= self.damage
        if enemy.hp == 0:
            enemy.death()

    def status(self):
        return f"HP: {self.hp} ATTACK: {self.damage}"


# Main character
class MC(Character):
    def __init__(self, _name, _hp=100, _damage=20, _kill_counter=0):
        super().__init__(_hp, _damage)
        self.name = _name
        self.kills_counter = _kill_counter

    def heal(self):
        self.hp += 20
        self.check_hp()

    def check_hp(self):
        if self.hp < 0:
            self.hp = 0
        elif self.hp > 100:
            self.hp = 100


# Game mob that
class Mob(Character):
    def __init__(self, _hp=60, _damage=5):
        super().__init__(_hp, _damage)


class Game:
    def __init__(self):
        self.character = None
        self.mobs = []

    def start(self):
        print("Do you want to load your character? (Y/N)")
        if input().upper() == 'Y':
            pass
        else:
            _name = input("Enter your character's name:\n")
            self.character = MC(_name)
        self.menu()

    def fight(self, enemy, index):
        turn = 1
        while enemy.alive and self.character.alive:
            if turn % 2 != 0:  # Player's turn
                print("Your current status: " + self.character.status())
                print("Enemy status: " + enemy.status())
                print("1. Attack")
                print("2. Retreat")
                command = input()
                if command == '1':
                    self.character.attack(enemy)
                    if not enemy.alive:
                        del self.mobs[index]
                        self.menu(f"Congratulations, {self.character.name}! You killed it.")
                    turn += 1
                elif command == '2':
                    self.menu("You have retreated from enemy.")
            else:
                enemy.attack(self.character)
                turn += 1


    def fight_menu(self):
        print("Choose mob to fight with:")
        for el in range(len(self.mobs)):
            print(f"Mob #{el + 1}. Enemy status: " + self.mobs[el].status())
        command = ""
        while not command.isdigit():
            command = input()
        if 1 <= int(command) <= len(self.mobs):
            self.fight(self.mobs[int(command) - 1], int(command) - 1)

    def menu(self, pre_text=""):
        os.system('cls')
        print(pre_text)
        print(f"""\
What are you gonna do next, {self.character.name}?
1. Load my character
2. Save my current progress
3. Character Info
4. Heal
5. Spawn mob""")
        if len(self.mobs) != 0:
            print("6. Fight")
        print("q. Exit game")
        command = input()
        if command == '1':
            pass
        elif command == '2':
            pass
        elif command == '3':
            self.menu("Your current status: " + self.character.status())
        elif command == '4':
            self.character.heal()
            self.menu("You have been healed!")
        elif command == '5':
            self.mobs.append(Mob())
            self.menu()

        elif command == '6' and len(self.mobs) != 0:
            self.fight_menu()
        elif command == 'q':
            exit()
        else:
            self.menu()


def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
