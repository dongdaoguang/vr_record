#! /usr/bin/env python
#coding=utf-8

import os,sys
import urllib2
import wave
import pyaudio
import numpy as np
from Tkinter import *

NUM_SAMPLES = 2000
framerate = 16000
channels = 1 
sampwidth = 2
TIME = 7

class VR_record:
    def __init__(self):
        self.root = Tk()
        self.root.title("VR Recorder")
        self.root.resizable(False, False)
        
        self.findLab = Label(self.root, text="查词：")
        self.findLab.grid(row=1,column=11,sticky=W)
        
        self.findtxt = Entry(self.root)
        self.findtxt.grid(row=1, column=12)
        
        self.vp_bt = Button(self.root, text="发音", command=self.play_cmd)
        self.vp_bt.grid(row=2,column=12, sticky=W+E)
        
        self.curLab = Label(self.root, text="Hello Voice", width=50, height=5)
        self.curLab.grid(row=0, column=0, padx=2, pady=5)
        
        # Result Info
        self.result = Text(self.root, width=50, height=5)
        self.result.grid(row=1, column=0, padx=2, pady=5)

        # 录音命令列表
        self.cmdsb = Scrollbar(self.root)
        self.cmdsb.grid(row=3, column=10, rowspan=3, padx=0, pady=5, sticky=N+S+E+W)
        self.cmdList = Listbox(self.root, width=80, height=8, yscrollcommand=self.cmdsb.set)
        self.cmdsb.config(command=self.cmdList.yview)
        self.cmdList.grid(row=3, column=0, rowspan=3, columnspan=10, padx=2, pady=5)
        self.initList("cmd.txt")
        self.cmdList.bind('<Double-Button-1>',self.printList)
        self.cmdList.bind('<ButtonRelease-1>', self.showCurCmd)

        # 录音开始
        self.recodstart_bt = Button(self.root, text="开始录音", width=8, height=2, command=self.record_wave,activeforeground='white',activebackground='green')
        self.recodstart_bt.grid(row=0, column=8, padx=4, pady=5)

        # 播放
        self.play_bt = Button(self.root, text="播放录音", width=8, height=2, command=self.playRecord,activeforeground='white',activebackground='green')
        self.play_bt.grid(row=0, column=9, padx=4, pady=5)
        
        # 下一个
        self.notrecord_bt = Button(self.root, text="下一个", command=self.nextCmd, width=8, height=2, activeforeground='white',activebackground='green')
        self.notrecord_bt.grid(row=1, column=8)

        # 未录音
        self.quit_bt = Button(self.root, text="显示还未\n录音列表", width=8, height=2, command=self.updateList, activeforeground='white', activebackground='green')
        self.quit_bt.grid(row=1, column=9)
                
    #--------------------------Call back func-------------------------#
    def getCurName(self):
        return self.cmdList.get(self.cmdList.curselection())    
    def showCurCmd(self,event):
        #print self.cmdList.curselection()
        #print self.cmdList.size()
        wavename = os.path.splitext(self.getCurName())[0]
        self.curLab.config(text= "请说命令:  " + wavename)
    def nextCmd(self):
        curIndex = self.cmdList.curselection()[0]
        if int(curIndex) == self.cmdList.size()-1:
            nextIndex = 0
        else:
            nextIndex = int(curIndex) + 1

        self.cmdList.selection_clear(curIndex)
        self.cmdList.selection_set(nextIndex)
        self.cmdList.see(nextIndex)
        wavename = os.path.splitext(self.getCurName())[0]
        self.curLab.config(text= "请说命令:  " + wavename)
    def getGoogleTts(self, cmd):
        formatCmd = urllib2.quote(cmd)
        Url = 'http://translate.google.cn/translate_tts?ie=UTF-8&'\
                    + 'q=%s&tl=en&total=1&idx=0&textlen=%d&client=t&prev=input'
        transUrl = Url % (formatCmd, len(formatCmd))
        headers = {'User-Agent'\
                      :'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
        req = urllib2.Request(url=transUrl, headers=headers)
        transData = urllib2.urlopen(req).read()
        saveTTS = open('record.mp3', 'wb')
        saveTTS.write(transData)
        saveTTS.close()
    def play_cmd(self):
        cmd = self.findtxt.get()
        self.getGoogleTts(cmd)
        wave.play("record.mp3")
    def playRecord(self,cmd=''):
        if cmd:
            wavename = cmd
        else:
            wavename = self.getCurName() + ".wav"
        if not os.path.exists(wavename):
            log = "Not exist: %s\n" % wavename
            self.showLog(log)
        else:
            wf = wave.open(wavename, "rb")
            p = pyaudio.PyAudio()
            
            #打开声音输出流
            stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),\
                            channels = wf.getnchannels(),\
                            rate = wf.getframerate(),\
                            output = True)
            while True:
                data = wf.readframes(1024)
                if data=='':
                    break
                stream.write(data)
            stream.close()
            p.terminate()
    def printList(self,event):
        wavename = self.getCurName() + ".wav"
        if not os.path.exists(wavename):
            log = "Not exist: %s\n" % wavename
            self.showLog(log)
        else:
            wf = wave.open(wavename, "rb")
            p = pyaudio.PyAudio()
            stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),\
                            channels = wf.getnchannels(),\
                            rate = wf.getframerate(),\
                            output = True)
            while True:
                data = wf.readframes(1024)
                if data=='':
                    break
                stream.write(data)
            stream.close()
            p.terminate()
    def save_wave_file(self, filename, data):  
        '''''save the date to the wav file'''  
        wf = wave.open(filename, 'wb')  
        wf.setnchannels(channels)  
        wf.setsampwidth(sampwidth)  
        wf.setframerate(framerate)  
        wf.writeframes("".join(data))  
        wf.close()  
    def record_wave(self):
        pa = pyaudio.PyAudio()  
        stream = pa.open(format = pyaudio.paInt16, channels = 1,  
                        rate = framerate, input = True,  
                        frames_per_buffer = NUM_SAMPLES)  
        save_buffer = []  
        count = 0  
        while count < TIME*4:  
            #read NUM_SAMPLES sampling data  
            string_audio_data = stream.read(NUM_SAMPLES)  
            save_buffer.append(string_audio_data)  
            count += 1  
            print '.'  
        wavename = self.getCurName() + ".wav" 
        self.save_wave_file(wavename, save_buffer)  
        save_buffer = []
        log = "Saved : %s" % wavename
        self.showLog(log)
    def initList(self,filename):
        if not os.path.exists(filename):
            pass
        else:
            fin = open(filename)
            tmplist = fin.readlines()
            for tmp in tmplist:
                self.cmdList.insert(END, tmp.strip())
            self.cmdList.selection_set(0)
            fin.close()
    def updateList(self):
        size = self.cmdList.size()
        #print size
        self.cmdList.delete(0,END)
        updatelist = []
        recordlist = []
        if not os.path.exists("cmd.txt"):
            pass
        else:
            l = os.listdir(os.getcwd())
            for file in l:
                if file.endswith(".wav"):
                    recordlist.append(os.path.splitext(file)[0])
            fin = open("cmd.txt")
            allcmd = fin.readlines()
            tmplist = [i.strip() for i in allcmd]
            updatelist = [a for a in tmplist if a not in recordlist]
            for item in updatelist:
                self.cmdList.insert(END, item.strip())
            self.cmdList.selection_set(0)
    def showLog(self,loginfo):
        self.result.delete(0.0, END)
        self.result.insert(END, loginfo + "\n")
    def run(self):
        self.root.mainloop()
        
if __name__ == '__main__':
    record = VR_record()
    record.run()
