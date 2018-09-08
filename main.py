import os
import piexif
import subprocess

inbox = './inbox/'
files = os.listdir(inbox)

for file in files:
    vid = False
    print(inbox + file)
    try:
        exif_dict = piexif.load(inbox + file)
    except:
        vid = True

    year = file[4:8]
    month = file[8:10]
    day = file[10:12]
    hour = file[13:15]
    minute = file[15:17]
    second = file[17:19]

    if not hour.isdecimal():
        id = int(file[15:19])
        hour = str((id//3600)%24)
        minute = str((id//60)%60)
        second = str(id%60)
        if(len(hour) != 2):
            hour = '0' + hour
        if(len(minute) != 2):
            minute = '0' + minute
        if(len(second) != 2):
            second = '0' + second

    datestr = year + ':' + month + ':' + day + ' ' + hour + ':' + minute + ':' + second
    date = datestr.encode()
    if not vid:
        exif_dict["Exif"][36867] = date
        exif_dict["Exif"][36868] = date
        try:
            piexif.insert(piexif.dump(exif_dict), inbox + file)
        except:
            print("Fallo en: " + file)
    else:
        subprocess.call(["exif.exe",
        "-overwrite_original",
        '-FileModifyDate="' + datestr + '"',
        '-FileCreateDate="' + datestr + '"',
        '-CreateDate="' + datestr + '"',
        '-ModifyDate="' + datestr + '"',
        '-TrackCreateDate="' + datestr + '"',
        '-TrackModifyDate="' + datestr + '"',
        '-MediaCreateDate="' + datestr + '"',
        '-MediaModifyDate="' + datestr + '"',
        inbox + file])
