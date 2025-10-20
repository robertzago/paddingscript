USAGE (RUN IN TERMINAL):
"python -m main.py"

"python -m main.py -h" for help

Default: Pads + Expands everything in Folder "source" into 1920*1080 

options:
  -h, --help            show this help message and exit
  -i, --input INPUT     The Input Folder (default: source/)
  -o, --output OUTPUT   The Output folder (default: padded/)
  -c, --color {blue,indigo,purple,pink,red,orange,yellow,green,teal,cyan,white,gray,gray-dark,primary,secondary,success,info,warning,danger,light,dark}
                        The color that will get used for the padding (default: dark)
  --hexcolor HEXCOLOR   Insert a hexcolor to use. Put into ""!!
  -r, --recursive       Will it go recursively through all folders inside input? Add this if not!
  -e, --extensions EXTENSIONS
                        File Extensions to use (Default: png, jpg, jpeg, webp)
  -d, --dynamic         Use a dynamic size nearest to the original image size
  -f, --fixed           Use a fixed size and pad around it
  -s, --size SIZE       Sets the size (Default: 1920, 1080) (does not work for dynamic sizing)
  -p, --proportion PROPORTION
                        Change the proportion from 16:9 to anything else (Format: 16,9)
  -b, --bordermult BORDERMULT

                        Change the size of the padded border if using --dynamic option (recommended: 0.05)
