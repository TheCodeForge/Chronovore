import math

from chronovore.helpers.lazy import lazy
from chronovore.helpers.sigmoid import sigmoid

from .base import Base

from chronovore.__main__ import cache

class Weapon(Base):

    def __repr__(self):
        return f"<Weapon({self.faction.name} / {self.id})>"

    @property
    @cache.memoize()
    def profiles(self):
        return [Weapon(x, faction=self.faction, id=f"{self.id} / {x['name']}", is_profile=True) for x in self.__dict__.get('profiles', [])]

    @property
    @cache.memoize()
    def keywords(self):
        return sorted(self.__dict__.get("keywords", []))

    @property
    @lazy
    def weapon_points_raw(self):

        if self.profiles:
            return max([x.weapon_points_raw for x in self.profiles])

        #evaluate attack and damage strings, as needed
        if isinstance(self.atk, str):
            atk = eval(self.atk.replace("2d6", "7").replace("d6", "3.5").replace("d3", "2"))
        else:
            atk = self.atk

        if isinstance(self.dmg, str):
            dmg = eval(self.dmg.replace("2d6", "7").replace("d6", "3.5").replace("d3", "2"))
        else:  
            dmg = self.dmg

        if "psk" in self.__dict__:

            rng = self.__dict__.get('rng')

            dice_map={
                2:36,
                3:35,
                4:33,
                5:30,
                6:26,
                7:21,
                8:15,
                9:10,
                10:6,
                11:3,
                12:1,
            }



            weapon_pts = dice_map[self.psk] * self.atk * math.sqrt(self.ap+1) * dmg * math.sqrt(rng)

            if self.target=="multi":
                weapon_pts*=1.1
            elif self.target=="aoe":
                weapon_pts*=math.sqrt(rng)



        else:

            if not self.__dict__.get('str'):
                return 0

            if "Torrent" in self.keywords:
                skl=1
            else:
                skl = self.skl

            rng = self.__dict__.get('rng',7) #7 is average effective range of melee weapons due to charge

            weapon_pts = (atk * (7-skl) * sigmoid(self.str) * math.sqrt(self.ap+1) * dmg * math.sqrt(rng))

            for kwd in self.keywords:
                if kwd.startswith("Anti-"):
                    weapon_pts *= 1.1
                elif kwd=="Assault":
                    weapon_pts *= 1.1
                elif kwd=="Blast":
                    weapon_pts *= 1.1
                elif kwd=="Demoralizing":
                    weapon_pts *= 1.1
                elif kwd=="Devastating Wounds":
                    weapon_pts *= 1.2
                elif kwd=="Hazardous":
                    weapon_pts *= 5/6
                elif kwd=="Heavy":
                    weapon_pts *= 1.1
                elif kwd=="Ignore Cover":
                    weapon_pts *= 1.2
                elif kwd=="Incendiary":
                    weapon_pts *= 1.1
                elif kwd=="Indirect Fire":
                    weapon_pts *= 1.1
                elif kwd=="Lance":
                    weapon_pts *= 1.1
                elif kwd=="Lethal Hits":
                    weapon_pts *= 1.2
                elif kwd.startswith("Melta"):
                    weapon_pts *= 1.2
                elif kwd=="One-Shot":
                    weapon_pts /= 5
                elif kwd=="Pistol":
                    weapon_pts *= 1.1
                elif kwd=="Precise":
                    weapon_pts *= 1.1
                elif kwd.startswith("Rapid Fire"):
                    weapon_pts *= 1.5
                elif kwd.startswith("Sustained Hits"):
                    weapon_pts *= 1.17
                elif kwd=="Twin-Linked":
                    weapon_pts *= 1.25

        # print(f"    {self.name}: {weapon_pts}")
        return int(weapon_pts)
