import argparse
import getpass
import subprocess
import magic
import os
from time import sleep
from random import randint
import requests
import urllib.request
#gsettings set org.gnome.desktop.background picture-uri 'file://PathToImage'
def change_wp(time,direc):
    print("changing your wallpaper...")
    files = os.listdir(direc)
    if(len(files)!=0):
        while(True):
            rand_idx = randint(0,len(files)-1)
            if magic.from_file(direc+files[rand_idx],mime=True).split('/')[0]=='image':
                ouput =  subprocess.call(["gsettings","set","org.gnome.desktop.background","picture-uri","'file://"+direc+files[rand_idx]+"'"])
                sleep(time)
    else:
        print("No images could be downloaded! Try after sometime.")

def get_redditpics():
    usr = getpass.getuser()
    pic_folder = "/home/"+usr+"/redditpics"
    if not os.path.exists(pic_folder):
        os.makedirs(pic_folder)
    url = "http://reddit.com/r/EarthPorn/.json?limit=10"
    try:
        print("Attempting to connect to Reddit...")
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            print("Connected!")
            data = r.json()
            posts = data['data']['children']
            for i,post in enumerate(posts):
                url = post['data']['url']
                title = post['data']['title']
                if 'i.imgur.com' in url:
                    filename = pic_folder+'/'+str(i)
                    print("Downloading: "+title)
                    urllib.request.urlretrieve(url,filename)
        else:
            print("No connection: error code: "+str(r.status_code))
            print("Try after sometime.")
            exit()
    except requests.exceptions.RequestException as e:
        print(e)
        exit()
    return pic_folder+'/'

if __name__ == "__main__":
    #time = int(input("Enter the time interval(in seconds): "))
    parser = argparse.ArgumentParser()
    parser.add_argument("time",help="time interval between 2 wallpapers")
    args = parser.parse_args()
    direc = get_redditpics()
    change_wp(int(args.time),direc)
