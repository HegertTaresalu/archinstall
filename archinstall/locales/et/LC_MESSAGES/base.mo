��    D      <  a   \      �  L   �  Z   .  i   �     �       $   "  <   G     �     �     �  ;   �  #      #   $  .   H     w  '   �     �     �     �  1   �  3   	  :   P	  C   �	  J   �	  :   
  @   U
  ,   �
  0   �
  w   �
  v   l  i   �  e   M     �     �     �     �  v   �     h     z  )   �  3   �  &   �  3     )   J     t  J   �  :   �  D     6   Y  H   �  )   �  p     Q   t  6   �  G   �  C   E  #   �  M   �  ]   �  +   Y  2   �  .   �  .   �  /     1   F  1   x  D   �  �   �  a   �  \     `   x     �  &   �       G   7          �     �  O   �  ,     &   2  3   Y     �  #   �     �     �  	   �  ;     =   >  7   |  H   �  E   �  T   C  W   �  (   �  8     ~   R  �   �  l   T  d   �     &     ;     T     a  ~   o     �     �  +     4   D  ,   y  D   �  2   �       H   3  1   |  U   �  F     i   K  <   �  �   �  _   s   6   �   ^   
!  ?   i!  "   �!  j   �!     7"  "   Q"  @   t"  <   �"  A   �"  A   4#  B   v#  >   �#  S   �#     :       /                    '   !   6   #   >         3   @   &      8               A   ;             C   ,   4   7      .   )   9                   	                                $              *                    -   =   5   ?   B               0                  "                
       %   2      +   D                1             <      (       

Select a graphics driver or leave blank to install all open-source drivers     Please submit this issue (and file) to https://github.com/archlinux/archinstall/issues  * Partition mount-points are relative to inside the installation, the boot would be /boot as an example. Adding partition.... All open-source (default) And one more time for verification:  Any additional users to install (leave blank for no users):  Archinstall language Choose a bootloader Choose an audio server Choose which kernels to use or leave blank for default "{}" Choose which locale encoding to use Choose which locale language to use Copy ISO network configuration to installation Current partition layout Desired hostname for the installation:  Disk layout Do you really want to abort? Drive(s) Enter a desired filesystem type for the partition Enter a desired filesystem type for the partition:  Enter the IP and subnet for {} (example: 192.168.0.5/24):  Enter the end location (in parted units: s, GB, %, etc. ; ex: {}):  Enter the start location (in parted units: s, GB, %, etc. ; default: {}):  Enter your DNS servers (space separated, blank for none):  Enter your gateway (router) IP address or leave blank for none:  Error: Could not decode "{}" result as JSON: Error: Listing profiles on URL "{}" resulted in: For the best compatibility with your AMD hardware, you may want to use either the all open-source or AMD / ATI options. For the best compatibility with your Intel hardware, you may want to use either the all open-source or Intel options.
 For the best compatibility with your Nvidia hardware, you may want to use the Nvidia proprietary driver.
 If you desire a web browser, such as firefox or chromium, you may specify it in the following prompt. Keyboard layout Locale encoding Locale language Mirror region Only packages such as base, base-devel, linux, linux-firmware, efibootmgr and optional profile packages are installed. Select a timezone Select keyboard layout Select one network interface to configure Select one of the regions to download packages from Select one of the values shown below:  Select one or more hard drives to use and configure Select one or more of the options below:  Select what to do with
{} Select what to do with each individual drive (followed by partition usage) Select what you wish to do with the selected block devices Select where to mount partition (leave blank to remove mountpoint):  Select which filesystem your main partition should use Select which mode to configure for "{}" or skip to use default mode "{}" Should this user be a superuser (sudoer)? This is a list of pre-programmed profiles, they might make it easier to install things like desktop environments Use NetworkManager (necessary to configure internet graphically in GNOME and KDE) Username for required superuser with sudo privileges:  Wipe all selected drives and use a best-effort default partition layout Would you like to use GRUB as a bootloader instead of systemd-boot? Would you like to use swap on zram? Write additional packages to install (space separated, leave blank to skip):  You need to enter a valid fs-type in order to continue. See `man parted` for valid fs-type's. [!] A log file has been created here: {} {} {}

Select by index which partition to mount where {}

Select by index which partitions to delete {}

Select which partition to mark as bootable {}

Select which partition to mark as encrypted {}

Select which partition to mask for formatting {}

Select which partition to set a filesystem on {} contains queued partitions, this will remove those, are you sure? Project-Id-Version: 
PO-Revision-Date: 
Last-Translator: 
Language-Team: 
Language: et
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: Poedit 3.3
 

Valige graafikadraiver või jätke tühjaks, et paigaldada kõik avatud lähtekoodiga draiverid     Esitage see probleem (ja fail) aadressil https://github.com/archlinux/archinstall/issues  * Partitsioonide kinnituspunktid on suhtelised installeerimise sees, näiteks boot oleks /boot. Partitsiooni lisamine.... Kõik avatud lähtekoodiga (vaikimisi) Ja veel kord kinnitamiseks:  Lisa kasutajate lisamine(jäta tühjaks kui ei soovi lisa kasutajaid):  Archinstalli keel Vali buudilaadija Vali audio server Valige, milliseid tuumasid soovite kasutada või jätke vaikimisi tühjaks "{}" Valige, millist asukoha kodeeringut kasutada Valige, millist asukoha keelt kasutada ISO-võrgu konfiguratsiooni kopeerimine paigaldusse Praegune partitsiooni paigutus Installimiseks soovitud hostinimi:  Ketta paigutus Kas sa tahad katkestada? Draiv(id) Sisestage partitsiooni jaoks soovitud failisüsteemi tüüp Sisestage partitsiooni jaoks soovitud failisüsteemi tüüp:  Sisestage IP ja alamvõrk {} (näide: 192.168.0.5/24):  Sisestage lõpu asukoht (parted ühikutes: s, GB, % jne; näiteks: {}):  Sisestage alguskoht (parted ühikutes: s, GB, % jne; vaikimisi: {}):  Sisestage oma DNS-serverid (tühikuga eraldatud, jätke tühjaks, kui neid ei ole):  Sisestage oma võrguvärava (ruuteri) IP-aadress või jätke tühjaks, kui see puudub:  Viga: {}" tulemust JSON-ina dekodeerida: Viga: URL-i "{}" profiilide loetlemine andis tulemuseks: Parima ühilduvuse saavutamiseks oma AMD riistvaraga võiksite kasutada kas kõiki avatud lähtekoodiga või AMD/ATI valikuid. Parima ühilduvuse saavutamiseks oma Inteli riistvaraga võiksite kasutada kas kõiki avatud lähtekoodiga või Inteli valikuid.

 Parima ühilduvuse saavutamiseks oma Nvidia riistvaraga peaksite kasutama Nvidia enda toodetud draiverit.


 Kui soovite veebibrauserit, näiteks firefox või chromium, saate selle määrata järgmises viipas. Klaviatuuri paigutus Kohaliku keele kodeering Kohalik keel Peegelregioon Paigaldatakse ainult sellised paketid nagu base, base-devel, linux, linux-firmware, efibootmgr ja valikulised profiilipaketid. Vali ajatsoon Valige klaviatuuri paigutus Valige üks võrguliides konfigureerimiseks Valige üks piirkondadest, kust pakette alla laadida Valige üks allpool esitatud väärtustest:  Valige üks või mitu kõvaketast kasutamiseks ja konfigureerimiseks Valige üks või mitu järgmistest võimalustest:  Valige, mida teha
{} Valige, mida teha iga üksiku kettaga (järgneb partitsiooni kasutamine) Valige, mida soovite valitud plokkseadmetega teha Valige, kuhu partitsiooni paigaldada (jätke tühjaks, et eemaldada paigalduspunkt):  Valige, millist failisüsteemi teie peamine partitsioon peaks kasutama Valige, millist režiimi soovite konfigureerida "{}" või jätke vahele, kasutada vaikimisi režiimi "{}" Kas see kasutaja peaks olema superkasutaja (sudo õigustega) See on nimekiri eelprogrammeeritud profiilidest, need võivad lihtsustada selliste asjade nagu töölauakeskkondade paigaldamist Kasutage NetworkManagerit (vajalik interneti graafiliseks konfigureerimiseks GNOME-s ja KDE-s). Kasutajanimi nõutud superkasutajale sudo õigustega:  Pühkige kõik valitud kettad ja kasutage parimat võimalikku vaikimisi partitsiooni paigutust Kas soovite systemd-booti asemel kasutada GRUBi buudilaadijana? Kas soovite zramis kasutada swapi? Kirjutage paigaldatavad lisapaketid (tühikutega eraldatuna, jätke tühjaks, kui soovite vahele jätta):  Partitsiooni lisamine.... [!] Siia on loodud logifail: {} {} {}


Valige indeksi järgi, millise partitsiooni kuhu paigaldada {}


Valige indeksi järgi, milliseid partitsioone kustutada {}


Valige, millist partitsiooni soovite märkida käivitatavaks {}


Valige, millist partitsiooni soovite krüpteerituks märkida {}

Valige, millist partitsiooni soovite vormindamiseks maskeerida {}


Valige, millisele partitsioonile failisüsteemi määrata {} sisaldab järjekorras olevaid partitsioone, see eemaldab need, kas olete kindel? 