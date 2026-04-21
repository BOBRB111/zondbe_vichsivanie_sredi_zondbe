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
        self.poison_cooldown = cooldown
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
        super().__init__("Метеор",20,"кидаться камнями👍👍👍")

    def use(self, target, user):
        if user.mana>=self.cost:
            user.mana-=self.cost
            x=user.get_atk() * 5
            target.take_damage(x)
            print(f"{target.name} получил по голове")
            return x
        else:
            print("недостаточно маны")
            return False

class Kolba(Spells):
    def __init__(self):
        super().__init__("колба",14,"восстанавливает здоровье👍👍👍")

    def use(self,target, user):
        if user.mana>=self.cost:
            user.mana-=self.cost
            user.hp=user.max_hp-10
            print("вы пробудили второй аспект виверны и восстановили здоровье")
            return True
        else:
            print("у последнего дракона нет маны")
            return False

class SunStrike(Spells):
    def __init__(self):
        super().__init__("санстрайк",30,"САНЯ, санстрайк")

    def use(self,target,user):
        if user.mana >= self.cost:
            user.mana -= self.cost
            target.get_damage(target.hp//5)
            print(f"{target.name} забыл намазать крем от загара")
        else:
            print("купите манго, недостаточно маны")

class Priest(Character,VenomMixin):
    def __init__(self,name):
        Character.__init__(self,name,90,8,3,90)
        VenomMixin.__init__(self)
        self.buff = False

    def get_atk(self):
        return self.atk

    def d_point(self,target):
        if not self.buff:
            target.take_damage(self.get_atk)
            target.venom(self.get_atk,3)
            return True
        else:
            target.take_damage(self.get_atk()*2)
            target.venom(self.get_atk()*2,5)
            return True

    def d_point_2(self):
        if not self.buff:
            self.buff=True


