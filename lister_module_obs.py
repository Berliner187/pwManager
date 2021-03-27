import enc_module_obs #1
import random #2
import os #3
from csv import DictReader ,DictWriter #4
yellow ,blue ,purple ,green ,mc ,red ,under_="\033[33m","\033[36m","\033[35m","\033[32m","\033[0m","\033[31m","\033[4m"#8
main_folder ='files/'#11
gty_for_listers =1000 #12
file_lister =main_folder +".lister.dat"#13
def ClearTerminal ():#16
    os .system ('cls'if os .name =='nt'else 'clear')#17
def MakingRows (OO0OO000O0O0O0O0O ,O0OO00O0OOOOOOO00 ):#20
    ClearTerminal ()#21
    print (yellow +'Please, wait ...'+mc )#22
    global gty_for_listers #23
    for O00O00000O0O0O000 in range (gty_for_listers ):#24
        OOO00O000000OO0O0 =[]#25
        for OO0OO00O0OOO000OO in O0OO00O0OOOOOOO00 :#26
            OOO00O000000OO0O0 .append (OO0OO00O0OOO000OO )#27
        random .shuffle (OOO00O000000OO0O0 )#28
        O0000OOO0OO0O0OOO =''.join (OOO00O000000OO0O0 )#29
        O00O0O0O00OO0O0OO =enc_module_obs .EncryptionByTwoLevels (O0000OOO0OO0O0OOO ,OO0OO000O0O0O0O0O )#31
        with open (file_lister ,"a")as O0OO00O00000O00O0 :#33
            O0OO00O00000O00O0 .write (O00O0O0O00OO0O0OO )#34
            O0OO00O00000O00O0 .write ('\n')#35
            O0OO00O00000O00O0 .close ()#36
    ClearTerminal ()#37
def AppendInListerFromFile (O0O00000OO00OOO0O ,OOOOO0OOO0OO00OO0 ):#40
    ""#41
    OO0O0OO0O000O0000 =[]#42
    with open (file_lister )as O00O0O0O0O000000O :#43
        OO0O0OOOOOO0OO000 =0 #44
        for O00O000O00O0O0O00 in O00O0O0O0O000000O :#45
            OO0O0OOOOOO0OO000 +=1 #46
            if OO0O0OOOOOO0OO000 ==O0O00000OO00OOO0O :#47
                OOOO00OO00OO0O00O =enc_module_obs .DecryptionByTwoLevels (O00O000O00O0O0O00 ,OOOOO0OOO0OO00OO0 )#49
                for O0O0OOO0000OOOO0O in OOOO00OO00OO0O00O :#50
                    OO0O0OO0O000O0000 .append (O0O0OOO0000OOOO0O )#51
    return OO0O0OO0O000O0000 #52
file_keys =main_folder +".keys.csv"#55
check_file_keys =os .path .exists (file_keys )#56
def getUniqueSewnKey (O0OO0O00O0O0O0O00 ):#59
    ""#60
    global gty_for_listers #61
    if check_file_keys ==bool (False ):#62
        O0O0O0O000OOO0OO0 =random .randrange (52 )#63
        O0OO0O00O00O00O0O =random .randrange (gty_for_listers )#64
        OO00000O0OOO0O0OO =enc_module_obs .EncryptionByTwoLevels (O0O0O0O000OOO0OO0 ,O0OO0O00O0O0O0O00 )#66
        OO0O0000O000OOO00 =enc_module_obs .EncryptionByTwoLevels (O0OO0O00O00O00O0O ,O0OO0O00O0O0O0O00 )#67
        O0O0O0O000OOO0OO0 ,O0OO0O00O00O00O0O =str (O0O0O0O000OOO0OO0 ),str (O0OO0O00O00O00O0O )#68
        with open (file_keys ,mode ="w",encoding ='utf-8')as O0000O000OO0O0O0O :#69
            OO0OO00O000O0OO0O =DictWriter (O0000O000OO0O0O0O ,fieldnames =['key','additional_key'])#70
            if check_file_keys ==bool (False ):#71
                OO0OO00O000O0OO0O .writeheader ()#72
            OO0OO00O000O0OO0O .writerow ({'key':OO00000O0OOO0O0OO ,'additional_key':OO0O0000O000OOO00 })#76
            return str (O0O0O0O000OOO0OO0 ),str (O0OO0O00O00O00O0O )#77
    else :#78
        with open (file_keys ,encoding ='utf-8')as OOO0OOOOO0O0OO0O0 :#80
            O0O0OO0O000OOOO0O =DictReader (OOO0OOOOO0O0OO0O0 ,delimiter =',')#81
            for O00OO0O00OOOOO0OO in O0O0OO0O000OOOO0O :#82
                O0O0O0O000OOO0OO0 =O00OO0O00OOOOO0OO ["key"]#83
                O0OO0O00O00O00O0O =O00OO0O00OOOOO0OO ["additional_key"]#84
            O000OOOOOOO0OO0O0 =enc_module_obs .DecryptionByTwoLevels (O0O0O0O000OOO0OO0 ,O0OO0O00O0O0O0O00 )#86
            O00OO0OO00O00O0OO =enc_module_obs .DecryptionByTwoLevels (O0OO0O00O00O00O0O ,O0OO0O00O0O0O0O00 )#87
            return str (O000OOOOOOO0OO0O0 ),str (O00OO0OO00O00O0OO )#88
