# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 12:22:57 2020

@author: Matt
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:50:25 2020

@author: Matt
"""

from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Ellipse
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.image import Image
from kivy.uix.image import AsyncImage

import win32api
import win32gui
import winxpgui

from random import random as rand

from os import walk as walk
from os.path import join

class passiveAnimationCycle(BoxLayout):
    r = NumericProperty(0)
    sign = 1

    def __init__(s, grabbagvar="animdir",animation_type="loop", anim_rate=0.5, **kwargs):
        super(passiveAnimationCycle, s).__init__(**kwargs)
        Clock.schedule_interval(s.redraw, anim_rate)

        s.r = 0
        s.iter = -1
        s.files = []
        s.animation_type = animation_type

        dirname = join('img', grabbagvar)
        print("dirname",dirname)
        for root, dirs, files in walk(dirname):
            print(files)
            for file in files:
                print("reading file in passiveAnimationCycle:",file)
                s.files.append(join('img', grabbagvar, file))
        print("Files processed by passiveAnimationCycle: ",s.files)
        s.fh = s.files[0]

    def reset_files_list(s,filedir):
        print("Resetting opponent to:",filedir)
        s.files = []
        for root, dirs, files in walk(join('img', filedir)):
            for file in files:
                print("reading file in reset_files_list:",file)
                s.files.append(join('img', filedir, file))
        print("Files processed by passiveAnimationCycle: ",s.files)
        s.fh = s.files[0]

    def _update_rect(s,instance,value):
        s.rect.pos = instance.pos
        s.rect.size = instance.size

    def sizeposbind(s,instance,value):
        s.size = instance.size
        s.pos = instance.pos

    def redraw(s, *args):
        if(s.iter <= 0):
            s.iter += 1
            s.canvas.clear()

        with s.canvas:
            Image(source=s.fh, size=s.size,allow_stretch = True)

        if(s.animation_type == "seesaw"):
            if(s.r > len(s.files)):
                s.sign = -1
                s.r += 2*s.sign
            if(s.r < 1):
                s.sign = 1
                s.r += 2*s.sign

            s.fh = s.files[int(s.r)-1]
            s.r += 1*s.sign
        elif(s.animation_type == "flicker"):
            if(rand() > 0.5):
                s.r += 1
            else:
                s.r -= 1
            if(s.r >= len(s.files)):
                s.r = 0
            elif(s.r < 0):
                s.r = len(s.files)-1
            s.fh = s.files[int(s.r)-1]

        s.canvas.clear()
        with s.canvas:
            Image(source=s.fh, size=s.size,allow_stretch = True)

if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition

    class PassiveAnimationApp(App):
        def build(self):
            myScreenManager = ScreenManager(transition=NoTransition(duration=0))
            passiveanimationcycle = ScreenEnemyHP(name="passiveanimationcycle")
            myScreenManager.add_widget(passiveanimationcycle)
            #thiswin = win32gui.FindWindow(None,"Notepad") #"PassiveAnimation")
            #print("thiswin:",thiswin)
            #win32gui.SetWindowPos(thiswin,
            #                      2, #"HWND_TOP",
            #                      5,
            #                      5,
            #                      1,
            #                      1,
            #                      1)
            return myScreenManager

    class ScreenEnemyHP(Screen):
        def __init__(self,**kwargs):
            super (ScreenEnemyHP, self).__init__(**kwargs)

            #sw = passiveAnimationCycle(position=(300.,100.),grabbagvar="img\\tornadomonster",animation_type="seesaw",anim_rate=0.8)
            sw1 = passiveAnimationCycle(grabbagvar=join('breathe'),
                                        animation_type="seesaw",
                                        anim_rate=1.0)
            #sw2 = passiveAnimationCycle(position=(100.,75.),size=(200,200),grabbagvar="img\\redrobe",animation_type="seesaw",anim_rate=0.25)
            self.add_widget(sw1)


    PassiveAnimationApp().run()
