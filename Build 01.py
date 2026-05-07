from main import *


class MagiMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mana = 90
        self.max_mana = 90
        self.spels = []

    def kast(self, target, spell):
        for k in self.spels:
            if k.name == spell:
                if self.mana >= k.mana_cost:
                    self.mana -= k.mana_cost
                    return k.speak(self, target)
                else:
                    print("маны нет")
                    return 0
        print("заклинания нет")
        return 0

    def learn_spell(self, spell):
        self.spels.append(spell)
        print(f"+заклинание {spell.name}")

    def clarity(self):
        if not self.mana >= self.max_mana:
            self.mana += 40
            print("+40 маны")
            return True
        else:
            print("максимум маны")
            return False


class VenomMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.poisoned = False
        self.poison_damage = 0
        self.poison_cooldown = 0

    def venom(self, demege, cooldown):
        self.poisoned = True
        self.poison_damage = demege
        self.poison_cooldown += cooldown
        print(f"{self.name} был отравлен силами тьмы")

    def venom_demege(self):
        if self.poisoned and self.poison_cooldown > 0:
            self.poison_cooldown -= 1
            self.hp -= self.poison_damage
            print(f"{self.name} получил урон от яда")
            return True
        else:
            print(f"{self.name} больше не отравлен")
            self.poisoned = False
            return False


class Prizivatel(Character, MagiMixin):
    def __init__(self, name):
        Character.__init__(self, name, 80, 10, 2, 80)
        MagiMixin.__init__(self)
        self.mipoList = []

    def d_point(self, target):
        x = self.get_atk()
        chance = random.randint(1, 5)
        if chance == 5 and len(self.mipoList) <= 3:
            mipo = Ork(f"орк {len(self.mipo) + 1}")
            self.mipoList.append(mipo)
            print(f"вы призвали {mipo.name}")
        for y in self.mipoList:
            if y.get_alive():
                y.d_point(target)
            else:
                print(f"сегодня умер {y.name}")
        target.take_damage(x)

    def get_atk(self):
        return self.atk * len(self.mipoList)


class Spells(ABC):
    def __init__(self, name, cost, disk):
        self.name = name
        self.cost = cost
        self.disk = disk

    @abstractmethod
    def use(self, target, user):
        pass

    def __str__(self):
        return f"{self.name}-название,{self.cost}-стоимость,{self.disk}-описание :3"


class Meteor(Spells):
    def __init__(self):
        super().__init__("Метеор", 20, "кидаться камнями👍👍👍")

    def use(self, target, user):
        if user.mana >= self.cost:
            user.mana -= self.cost
            x = user.get_atk() * 5
            target.take_damage(x)
            print(f"{target.name} получил по голове")
            return x
        else:
            print("недостаточно маны")
            return False


class Kolba(Spells):
    def __init__(self):
        super().__init__("колба", 14, "восстанавливает здоровье👍👍👍")

    def use(self, target, user):
        if user.mana >= self.cost:
            user.mana -= self.cost
            user.hp = user.max_hp - 10
            print("вы пробудили второй аспект виверны и восстановили здоровье")
            return True
        else:
            print("у последнего дракона нет маны")
            return False


class SunStrike(Spells):
    def __init__(self):
        super().__init__("санстрайк", 30, "САНЯ, санстрайк")

    def use(self, target, user):
        if user.mana >= self.cost:
            user.mana -= self.cost
            target.get_damage(target.hp // 5)
            print(f"{target.name} забыл намазать крем от загара")
        else:
            print("купите манго, недостаточно маны")


class Priest(Character, VenomMixin):
    def __init__(self, name):
        Character.__init__(self, name, 90, 8, 3, 90)
        VenomMixin.__init__(self)
        self.buff = False

    def get_atk(self):
        if self.buff:
            self.hp -= 5
            return self.atk * 2
        else:
            return self.atk

    def d_point(self, target):
        if not self.buff:
            target.take_damage(self.get_atk)
            target.venom(self.get_atk, 3)
            return True
        else:
            target.take_damage(self.get_atk() * 2)
            target.venom(self.get_atk() * 2, 5)
            return True

    def d_point_2(self):
        if not self.buff:
            self.buff = True
            print("вы прочитали молитву,вы стали сильнее")
        else:
            self.buff = False
            print("вы перестали читать молитвы и терять здоровье")


class Viper(Enemy, VenomMixin):
    def __init__(self):
        Enemy.__init__(self, "viper", 100, 5, 0, 150, 100)
        VenomMixin.__init__(self)

    def get_atk(self):
        return self.atk

    def d_point(self, target):
        if self.hp >= 30:
            print("в вас плюнул вайпер, не терпите")
            target.take_damage(self.get_atk())
            target.venom(self.get_atk(), 3)
        else:
            self.d_point_2(target)

    def d_point_2(self, target):
        print("вайпер зол и атакует с большей силой")
        target.take_damage(self.get_atk() * 2)
        target.venom(self.get_atk(), 2)


class Roshan(Enemy):

    def __init__(self):
        super().__init__("Рошан", 200, 20, 10, 1000, 200)
        self.stac = 0
        self.patchs = 3

    def get_atk(self):
        return self.atk

    def atack(self, target):
        target.take_damage(self.get_atk)
        print("вас ударил рошан")
        return True

    def stacs(self, target):
        target.stan()
        target.take_damage(self.get_atk)
        print("вас сильно ударил рошан")
        return True

    def patch(self):
        self.hp += 40
        print("рошан принял неизбежное и сьел Аегис (+40хп)")
        return True

    def d_point(self, target):
        if self.hp <= 50 and self.patchs > 0:
            self.patchs -= 1
            self.patch()

        elif self.stacs == 4:
            self.stac = 0
            self.stacs(target)

        else:
            self.stac += 1
            self.atack(target)


class Mantiya_intelekta:
    def __init__(self, name, stats, type):
        self.name = name
        self.stats = stats
        self.flag = False
        self.type = type

    def flag(self, character):
        if not self.flag:
            self.flag = True
            for keys, znacheniya in self.stats.items():
                if hasattr(character, keys):
                    setattr(character, keys), getattr((character, keys) + znacheniya)
            print(f"{character.name} надевает {self.name}")
            return True
        return False

    def unflag(self, character):
        if self.flag:
            self.flag = False
            for keys, znacheniya in self.stats.items():
                if hasattr(character, keys):
                    setattr(character, keys), getattr((character, keys) - znacheniya)
            print(f"{character.name} снимает {self.name}")
            return True
        return False

    def __str__(self):
        return f"{self.name}:название, {self.stats}:статы, {self.type}:тип"


class Ems:
    def __init__(self, character):
        self.character = character
        self.slots = {
            "weapon": None, "helmet": None, "bronik": None, "ring": None
        }
        self.inventory = []

    def add(self, item):
        self.inventory.append(item)
        print(f"{item} был добавлен в инвентарь")
        return True

    def equip(self, item_index):
        if 0 <= item_index < len(self.inventory) - 1:
            item = self.inventory[item_index]
            slot = item.type
            if self.slots[slot]:
                self.slots[slot].unflag(self.character)
            if self.flag(self.character):
                self.slots[slot] = item
                self.inventory.pop(item_index)
                return True
        return False

    def show_inv(self):
        print("предметы:")
        for i, x in enumerate(self.inventory):
            print(i, x)
        return True

    def show_slots(self):
        print("экипировка")
        for i, x in self.slots.items():
            print(i, x)
        return True


class Equipment(Item):
    def __init__(self, ecvp):
        super().__init__(ecvp.name, f"предмет {ecvp}")
        self.ecvp = ecvp

    def use(self, character):
        if hasattr(character, "equipment_system"):
            character.equipment_system.add(self.ecvp)
            return True
        else:
            print("персонаж не может одеть эту экипировку :(")
            return False


class Game_plus(Game):
    def __init__(self):
        super().__init__()
        self.difficult = "norm"
        self.roshanchik = 0

    def create_character(self):
        print("ку, сегодня время гулять по мультиверс фанфикам")
        print("создай себе персонажа")
        name = input("введите имя ")
        print("на выбор: 1-воин 2-маг 3-(админ) 4-призыватель 5-священник")
        while True:
            ch = input("введите число ")
            if ch == 1:
                self.player = Voin(name)
                break
            elif ch == 2:
                self.player = Anti_Mag(name)
                break
            elif ch == 3:
                self.player = Heavy(name)
                break
            elif ch == 4:
                self.player = Prizivatel(name)
                break
            elif ch == 5:
                self.player = Priest(name)
                break
            else:
                print("неправильно, попробуй еще раз")
        print("ваш персонаж успешно создан")
        print(self.player)
        self.player.equipment_system=Ems(self.player)
        self.player.inv_add(Beli_monstr())
        self.player.inv_add(Beli_monstr())
        if isinstance(self.player, Anti_Mag):
            self.player.inv_add(Rozoviy_monstr())
        x=Mantiya_intelekta("палка",{"atk":1},"weapon")
        self.player.equipment_system.add(x)
        print("вам выдали палку")

