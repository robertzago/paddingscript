from PIL import Image, ImageOps
import os
import glob
import argparse
from pathlib import Path
import math

imgcount = 0
# Taken from the Website!
colors = {
    "blue": "#0076bd",
    "indigo": "#6610f2",
    "purple": "#6f42c1",
    "pink": "#e83e8c",
    "red": "#b81216",
    "orange": "#f0593e",
    "yellow": "#feca0a",
    "green": "#40ae49",
    "teal": "#20c997",
    "cyan": "#17a2b8",
    "white": "#fff",
    "gray": "#6f6f6f",
    "gray-dark": "#343a40",
    "primary": "#00395b",
    "secondary": "#307197",
    "success": "#40ae49",
    "info": "#d7d7d7",
    "warning": "#ff9914",
    "danger": "#f0593e",
    "light": "#f3f5f6",
    "dark": "#343a40",
}

reverse_colors  = {
    '#0076bd': 'blue',
    '#6610f2': 'indigo',
    '#6f42c1': 'purple', 
    '#e83e8c': 'pink', 
    '#b81216': 'red', 
    '#f0593e': 'orange', 
    '#feca0a': 'yellow', 
    '#40ae49': 'green', 
    '#20c997': 'teal', 
    '#17a2b8': 'cyan', 
     '#fff'    : 'white', 
    '#6f6f6f': 'gray', 
    '#343a40': 'gray-dark', 
    '#00395b': 'primary', 
    '#307197': 'secondary', 
    '#d7d7d7': 'info', 
    '#ff9914': 'warning', 
    '#f3f5f6': 'light'}

def resizeImagePadded(Image: Image, size: tuple = (1920,1080), color=colors["dark"], fixated=False):
    global imgcount
    imgcount += 1
    width,height = Image.size
    if fixated:
        print(size)
        bordersize = abs(width-size[0]),abs(height-size[1])
        return ImageOps.expand(Image, bordersize, fill=color)
    return ImageOps.pad(Image, size, color=color)

def resizeImagePaddedDynamic(Image: Image, color=colors["dark"], fixated=False, bordermult=0, ratio=(16,9)):
    global imgcount
    imgcount += 1
    width,height = Image.size
    ratiow,ratioh = ratio
    if width/height == ratiow/ratioh:
        size = width, height
    else:
        mwidth = round(math.ceil(width/ratiow)*(1.0+float(bordermult)))
        mheight = round(math.ceil(height/ratioh)*(1.0+float(bordermult)))
        if mwidth > mheight:
            size = ratiow*mwidth,ratioh*mwidth
        else:
            size = ratiow*mheight,ratioh*mheight
    if fixated:
        print(size)
        bordersize = abs(size[0]-width),abs(size[1]-height)
        return ImageOps.expand(Image, bordersize, fill=color)
    return ImageOps.pad(Image, size, color=color)

def resizeImagesPadded(paths, input_folder: Path, output_folder: Path, size=(1920,1080), color=colors["dark"], dynamic=False, fixated=False, bordermult=0, ratio=(16,9)):
    print(
        f"Resizing to {"dynamic size" if dynamic else size} with the hexcode {color} {f"({reverse_colors[color] })" if color in reverse_colors else ""}. Images will {"not " if fixated else ""}expand to fill the space!"
        )
    for path in paths:
        inp_location, out_location = getLocations(path,input_folder,output_folder)
        print(f"Resizing Image at {inp_location}!")
        if dynamic:
            print(f"Resizing dynamically with aspect ratio {ratio} and border multiplicator {bordermult}")
            resizeImagePaddedDynamic(Image.open(inp_location),color, fixated, bordermult, ratio).save(out_location)
        else: 
            resizeImagePadded(Image.open(inp_location),size, color, fixated).save(out_location)

def getPaths(folder: str, extensions = ["png","jpg","jpeg","webp"], recursive=True):
    print(f"Getting Path files {"recursively " if recursive else ""}with extensions {extensions} in folder \"{folder}\"!")
    p = Path(folder)
    image_paths = []
    for ext in extensions:
        if recursive:
            for fp in p.rglob(f"*.{ext}"):
                image_paths.append(fp.relative_to(p))
        else:
            for fp in p.glob(f"*.{ext}"):
                image_paths.append(fp.relative_to(p))
    return image_paths

def getLocations(path, input_folder, output_folder):
    out_location = output_folder.joinpath(path)
    print(out_location)
    out_location.parent.mkdir(parents=True,exist_ok=True)
    inp_location = input_folder.joinpath(path)
    print(inp_location)
    image_name = f"{out_location.stem}_padded{out_location.suffix}"
    out_location = out_location.with_name(image_name)
    return inp_location,out_location


def cmdargs():
    parser = argparse.ArgumentParser(description="Pad all images inside a folder")
    parser.add_argument("-i","--input",help="The Input Folder (default: source/)")
    parser.add_argument("-o","--output",help="The Output folder (default: padded/)")
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument(
        "-c","--color",help="The color that will get used for the padding (default: dark)", choices=
        [
           "blue",
            "indigo",
            "purple",
            "pink",
            "red",
            "orange",
            "yellow",
            "green",
            "teal",
            "cyan",
            "white",
            "gray",
            "gray-dark",
            "primary",
            "secondary",
            "success",
            "info",
            "warning",
            "danger",
            "light",
            "dark", 
        ]
    )
    group1.add_argument("--hexcolor",help="Insert a hexcolor to use. Put into \"\"!!")
    parser.add_argument("-r","--recursive",help="Will it go recursively through all folders inside input? Add this if not!", action="store_true")
    parser.add_argument("-e","--extensions",help="File Extensions to use (Default: png, jpg, jpeg, webp)")
    parser.add_argument("-d","--dynamic",help="Use a dynamic size nearest to the original image size", action="store_true")
    parser.add_argument("-f","--fixed",help="Use a fixed size and pad around it", action="store_true")
    parser.add_argument("-s","--size",help="Sets the size (Default: 1920, 1080) (does not work for dynamic sizing)")
    parser.add_argument("-p","--proportion",help="Change the proportion from 16:9 to anything else (Format: 16,9)")
    parser.add_argument("-b","--bordermult",help="Change the size of the padded border if using --dynamic option (recommended: 0.05)")
    return parser.parse_args()

if __name__ == "__main__":
    args = cmdargs()
    inp = Path(args.input) if args.input is not None else Path("source")
    out = Path(args.output) if args.output is not None else Path("padded")
    extensions = args.extensions.strip().split(",") if args.extensions is not None else ["png","jpeg","jpg","webp"]
    size = tuple(map(int, args.size.strip().split(","))) if args.size is not None else (1920,1080)
    recursive = True if args.recursive is False else not args.recursive
    ratio = tuple(map(int, args.proportion.strip().split(","))) if args.proportion is not None else (16,9)
    if not args.bordermult:
        bordermult = 0
    else:
        bordermult = args.bordermult
    img_paths = getPaths(inp, extensions, recursive)
    if args.color:
        resizeImagesPadded(img_paths, inp, out, size, colors[args.color], args.dynamic, args.fixed, bordermult, ratio)
    elif args.hexcolor:
        resizeImagesPadded(img_paths, inp, out, size, args.hexcolor, args.dynamic, args.fixed, bordermult, ratio)
    else:
        resizeImagesPadded(img_paths, inp, out, size, colors["dark"], args.dynamic, args.fixed, bordermult, ratio)
    print("\n"*5)
    print(f"Done! Resized {imgcount} images!")
    print("\n"*5)