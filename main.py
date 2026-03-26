import random
from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, name, hp, atk, df, max_hp):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.df = df
        self.level = 1
        self.xp = 0
        self._inv = []
        self.max_hp = max_hp

    @abstractmethod
    def d_point(self, target):
        pass

    def get_df(self):
        return self.df

    def get_atk(self):
        return self.atk

    def get_alive(self):
        return self.hp > 0

    def gain_xp(self, amount):
        self.xp += amount
        print(f"{self.name} получил {amount} опыта, всего xp {self.xp}")
        num = self.level * 1.5 * 20 // 1
        if self.xp > num:
            self.xp -= num
            print(self.gain_level())

    def gain_level(self):
        self.level += 1
        self.atk += 2
        self.df += 2
        self.hp += self.max_hp
        return F"ваш уровень повышен, теперь он составляет {self.level}, все характеристики повышены на 2"

    def take_damage(self, atk):
        k_atk = max(1, atk - self.get_df())
        self.hp -= k_atk
        print(f"{self.name} получил {k_atk} урона")
        print(f"{self.hp} осталось")
        return k_atk

    def inv_add(self, item):
        self._inv.append(item)
        return f"вы подобрали {item}"

    def inv_watch(self):
        if len(self._inv) == 0:
            for x in self._inv:
                print(x)
            return True
        else:
            return "инвентарь пуст"

    def __str__(self):
        return f"{self.name}-имя,{self.hp}/{self.max_hp},{self.atk}-урон,{self.df}-защита,{self.level}-уровень"


class Item(ABC):
    def __init__(self, name, desk):
        self.name = name
        self.desk = desk

    @abstractmethod
    def use_item(self, character):
        pass

    def __str__(self):
        return f"{self.name},{self.desk}"


class Voin(Character):
    def __init__(self, name):
        super().__init__(name, 120, 15, 5, 120)
        self.st = 0

    def d_point(self, target):
        dmg = self.get_atk()
        self.st += 1
        if self.st == 4:
            dmg *= 3
            print(f"у вашего врага была плохая карма, по нему проходит тройной урон")
            self.st = 0
        k_dmg = target.take_damage(dmg)
        return k_dmg

    def d_point_2(self):
        print("у тебя нет такой способности")
        return False


class Anti_Mag(Character):
    def __init__(self, name):
        super().__init__(name, 90, 12, 10, 90)
        self.mana = 100
        self.max_mana = 100
        self.spels = []

    def d_point(self, target):
        if self.mana > 10:
            self.mana -= 10
            dmg = self.get_atk()
            target.hp -= dmg
            print(f"{target.name} получил {dmg} урона")
            return dmg
        elif self.mana == 50:
            self.mana -= 30
            dmg = target.hp / 2 + self.get_atk()
            target.hp -= dmg
            print("вы разгневали богов, но они слегка промохнулись")
            return 0
        elif self.mana == 0:
            print("вы уподоблись советским чиновникам и нарисовали себе +20 маны, удачи!!!")
            self.mana += 20
        else:
            print("смерть в нищете")
            return 0

    def get_atk(self):
        return self.atk

    def read(self, item):
        self.spels.append(item)
        self.atk += 6
        print("вы научились фокусам с монетками!(+новое заклинание!!)")

    def d_point_2(self, target):
        if "s1" in self.spels:
            if 's2' in self.spels:
                chance = random.randint(1, 12)
                if 's3' in self.spels:
                    if self.mana == 30:
                        if chance == 5 or chance == 4 or chance == 2:
                            self.mana -= 30
                            target.hp = 0
                            print("рампейдж, на вашего противника обрушился гнев императора( мгновенная смерть )")
                            self.hp = self.max_hp
                            return 0
                        elif chance == 3:
                            self.mana -= 30
                            self.hp -= 20
                            print("к вам подошел инвокер и вошел в режим убийцы(-20hp)")
                            return 0
                        else:
                            dmg = self.atk * 4
                            k_dmg = target.take_damage(dmg)
                            print(f"{target.name} получил {k_dmg} урона")
                            return k_dmg
                    else:
                        print("ох черт ох боже( недостаточно маны )")
                        return 0
                else:
                    if self.mana > 20:
                        if chance == 5 or chance == 4:
                            self.mana -= 20
                            target.hp = 0
                            print("рампейдж, ваш противник подавился слюной( мгновенная смерть )")
                            return 0
                        elif chance == 3:
                            self.mana -= 20
                            self.hp -= 10
                            print("вы призвали языческого духа, он дал вал леща и сбежал (-10hp)")
                            return 0
                        else:
                            self.mana -= 20
                            dmg = self.atk * 3
                            k_dmg = target.take_damage(dmg)
                            print(f"{target.name} получил {k_dmg} урона")
                            return k_dmg
                    else:
                        print("проблемы со скилом( недостаточно маны )")
                        return 0
            else:
                if self.mana > 20:
                    self.mana -= 20
                    dmg = self.atk * 3
                    k_dmg = target.take_damage(dmg)
                    print(f"{target.name} получил {k_dmg} урона")
                    return k_dmg
                else:
                    print("проблемы со скилом брочачо( недостаточно маны )")
        else:
            print("ребята я хочу домой( заклинание не изучено )")
            return 0


class Heavy(Character):
    def __init__(self, name):
        super().__init__(name, 200, 5, 30, 200)
        self.sandvich = 4

    def get_atk(self):
        return self.atk

    def d_point(self, target):
        k_dmg = 0

        for x in range(10):
            chance = random.randint(1, 75)
            if chance == 1:
                dmg = self.get_atk() * 20
                print("Крит")
                k_dmg += dmg
            else:
                dmg = self.get_atk()
            target.get_atk(dmg)
            print(f"{target.name} получил {dmg} урона")
            k_dmg += dmg
        print(f"{target.name} всего получил {k_dmg} урона")
        return k_dmg

    def d_point_2(self):
        self.sandvich -= 1
        self.hp += 40
        print("вы сьели сендвич!👍👍👍")
        return True


class Beli_monstr(Item):
    def __init__(self, num=30):
        super().__init__("hp_monstr", "восстанавливает здоровье")
        self.num = num

    def use_item(self, target):
        if target.hp == target.max_hp:
            print("полное здороье")
            return False
        else:
            target.hp = min(target.max_hp, target.hp + self.num)
            print(f"вы пьете белый монстр(+{self.num}hp)")
            return True


class Rozoviy_monstr(Item):
    def __init__(self, num=50):
        super().__init__("mana_monstr", "восстанавливает ману")
        self.num = num

    def use_item(self, target):
        if target.hp == target.max_hp:
            print("полная мана")
            return False
        else:
            target.mana = min(target.max_mana, target.mana + self.num)
            print(f"вы пьете розовый монстр(+{self.num} маны)")
            return True


class Enemy(Character):
    def __init__(self, name, hp, atk, df, ex, max_hp):
        super().__init__(name, hp, atk, df, max_hp)
        self.ex = ex

    def d_point(self, target):
        dmg = self.get_atk()
        return target.take_damage(int(dmg))


class Ork(Enemy):
    # ммм грибочки
    def __init__(self, name="Орк", hp=60, atk=5, df=5, ex=10, max_hp=60):
        super().__init__(name, hp, atk, df, ex, max_hp)

    def d_point(self, target):
        dmg = self.get_atk()
        print("вы пропустили удар")
        return target.take_damage(int(dmg))


class Kofevarka(Enemy):

    def __init__(self, name="Кофеварка", hp=50, atk=8, df=10, ex=20, max_hp=50):
        super().__init__(name, hp, atk, df, ex, max_hp)

    def d_point(self, target):
        k_dmg = 0
        for x in range(2):
            dmg = self.get_atk()
            print("вы пропустили удар")
            k_dmg += dmg
        print(f"вы потеряли всего{k_dmg}hp")
        return target.take_damage(int(k_dmg))


class STCR(Enemy):
    def __init__(self, name="S.T.C.R.", hp=40, atk=1, df=3, ex=30, max_hp=40):
        super().__init__(name, hp, atk, df, ex, max_hp)

    def d_point(self, target):
        dmg = random.randint(0, 30) + self.get_atk()
        print("вы пропустили удар")
        return target.take_damage(int(dmg))


class Game:
    def __init__(self):
        self.player = None
        self.enemy = None
        self.flag = False
        self.korabliki = 0
        # кол-во битв за игру

    def create_character(self):
        print("создание персонажа,выберете класс")
        print("1=воин 2=маг 3=Ассасин!")
        while True:
            clas = input("выберете класс")
            if clas == 1:
                name = input("введите имя")
                self.player = Voin(name)
                break
            elif clas == 2:
                name = input("введите имя")
                self.player = Anti_Mag(name)
                break
            elif clas == 3:
                name = input("введите имя")
                self.player = Heavy(name)
                break
            else:
                print("error")
        print("ваш персонаж успешно создан")
        print(self.player)
        self.player.inv_add(Beli_monstr())
        self.player.inv_add(Beli_monstr())
        if isinstance(self.player, Anti_Mag):
            self.player.inv_add(Rozoviy_monstr())

    def create_enemy(self):
        enemys = [Ork, Kofevarka, STCR]
        chance = [50, 35, 15]
        enemy = random.choice(enemys, weights=chance)
        self.enemy = enemy()
        print(f"на вас напал {self.enemy.name}")
        print(self.enemy)

    def player_turn(self):
        while True:
            print("ваш ход")
            print("1-атаковать, 2-способность, 3-просмотреть инвентарь")
            turn = int(input("выберете действие"))
            if turn == 1:
                self.player.d_point(self.enemy)
                break
            elif turn == 2:
                self.player.d_point_2(self.enemy)
                break
            elif turn == 3:
                for i, x in enumerate(self.player._inv):
                    print(i, x)
                print("какой предмет вы хотите использовать?")
                choice = int(input("введите номер предмета"))
                t = (self.player._inv[choice].use_item())
                if t:
                    self.player._inv.pop(choice)

    def fight(self):
