import sys
import time
from PIL import Image
import numpy as np
import os

# Thanks, Stack Overflow!
def progressbar(it, prefix="", size=60, out=sys.stdout, char=u"█"): # Python3.3+
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, char*x, "."*(size-x), j, count),
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)

class imgProcessing:
    def MakeRow(row, name):
        images = [Image.open(x) for x in row]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]

        new_im.save(name)

    def CombineRows(rows, name):
        imgs = [Image.open(i) for i in rows]
        min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
        imgs_comb = np.vstack([i.resize(min_shape) for i in imgs])
        imgs_comb = Image.fromarray(imgs_comb)
        imgs_comb.save(name)
        for row in rows:
            os.remove(row)

    def create_image(color, name):
        # Create a new 100x100 image with the specified color
        image = Image.new('RGB', (100, 100), color)

        # Save the image as a PNG file
        image.save(f'Assets/CustomColorTiles/{name}.png')

class osStuff:
    def findInDIR(di):
        if type(di) == type(''):
            try:
                return os.listdir(di)
            except:
                raise Exception("PLEASE ENTER A VALID DIRECTORY")
        else:
            raise Exception("PLEASE ENTER A STRING")

def FindARG(toSearch, arg):
    toFind = list(arg)
    Res = True
    toSearch = toSearch.replace(' ', '')
    for i in range(len(toSearch)):
        try:
            if toSearch[i] != toFind[i]:
                Res = False
                break
        except:
            if toSearch[i] == ':':
                break
    return Res

def Compile_DML_file(fileName = 'example.dml', intoRaw = False, outPath = 'Compiled/'):
    paths, rowPaths, grid = [], [], []
    temp = None
    commands = ['holdMeta']
    line = 0
    File = fileName  # Define the File to Read
    compiledName = f'{outPath}{fileName.split(".")[0]}.png'
    config = [False]
    compiled = '# RETURNS \n# \n'
    Default = 'Assets/DEFAULT/Empty.png'

    # 0 = Upwards Wall
    # 1 = Side Wall
    # 2 = Corner Wall
    # 3 = Open Door
    # 4 = Closed Door
    # 5 = Stairs going up
    # 6 = Stairs going down
    # 7 = The default icon for a custom item without a custom sprite
    # len(SPRITES) - 1 = Default icon if a spot is empty

    print(f'OPENING: {File}\n')
    try:
        with open(File, 'r') as fh:
            raw = fh.read()
    except:
        try:
            File = 'DML_Files/' + File  # Define the File to Read
            with open(File, 'r') as fh:
                raw = fh.read()
        except:
            print(File)
            raise Exception("PLEASE ENTER A VALID FILE TYPE")
    fileRows = raw.split('\n')
    # Read DML and compiles it
    for i in progressbar(it=range(len(fileRows)), prefix="READING: ", size=40, char='~'):
        row = fileRows[i]
        line += 1
        toCheck = row
        try:
            if row.replace(' ', '')[0] == '#' or row == '':
                continue
        except IndexError:
            if row == '':
                continue
        if FindARG(toSearch=toCheck, arg='META') or FindARG(toSearch=toCheck, arg='MET'):
            continue
        if FindARG(toSearch=toCheck, arg='CONFIG') or FindARG(toSearch=toCheck, arg='CONF'):
            temp = ((row.split(':'))[1].replace(' ', '').split('#'))[0].split(',')
            Found = False
            temp2 = None
            for arg in temp:
                temp2 = arg.split('/')
                for command in commands:
                    if temp2[0] == command:
                        Found = True
                        break
            if not Found:
                raise Exception(f"INVALID COMMAND ON LINE {line}\nCODE >> {fileRows[line - 1]}")
            else:
                match temp2[0]:
                    case 'holdMeta':
                        if temp2[1]:
                            config[0] = True
            continue
        if FindARG(toSearch=toCheck, arg="mapSize") or FindARG(toSearch=toCheck, arg="ms"):
            temp = row.split(':')
            temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
            gridSize = [int(temp[0]), int(temp[1])]
            for x in range(gridSize[0]):
                grid.append([])
                for y in range(gridSize[1]):
                    grid[x].append([])
            continue
        if FindARG(toSearch=toCheck, arg="customDefaultTileName") or FindARG(toSearch=toCheck, arg="CDTM"):
            temp = row.split(':')
            temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
            Default = temp[0]
            continue
        if grid != []:
            if FindARG(toSearch=toCheck, arg="wall") or FindARG(toSearch=toCheck, arg="W"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'WALL']
                except IndexError:
                    raise Exception('PLEASE PLACE WALL WITHIN THE GRID')
                continue
            if FindARG(toSearch=toCheck, arg="door") or FindARG(toSearch=toCheck, arg="D"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'DOOR']
                except IndexError:
                    raise Exception('PLEASE PLACE DOOR WITHIN THE GRID')
                continue
            if FindARG(toSearch=toCheck, arg="stairs") or FindARG(toSearch=toCheck, arg="S"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'STAIRS']
                except IndexError:
                    raise Exception('PLEASE PLACE STAIRS WITHIN THE GRID')
                continue
            if FindARG(toSearch=toCheck, arg="clear") or FindARG(toSearch=toCheck, arg="cl"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = []
                except IndexError:
                    raise Exception('PLEASE REMOVE SOMETHING WITHIN THE GRID')
                continue
            if FindARG(toSearch=toCheck, arg="custom") or FindARG(toSearch=toCheck, arg="cu"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], temp[3], 'CUSTOM']
                except IndexError:
                    raise Exception('PLEASE PLACE CUSTOM ITEM WITHIN THE GRID')
                continue
            if FindARG(toSearch=toCheck, arg='player') or FindARG(toSearch=toCheck, arg="P"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'PLAYER']
                except IndexError:
                    raise Exception('PLEASE PLACE PLAYER WITHIN THE GRID')
                continue
            if FindARG(toSearch=toCheck, arg='enemy') or FindARG(toSearch=toCheck, arg="E"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'ENEMY']
                except IndexError:
                    raise Exception('PLEASE PLACE ENEMY WITHIN THE GRID')
                continue
            if FindARG(toSearch=toCheck, arg='group') or FindARG(toSearch=toCheck, arg='G'):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                points = []
                meta = []
                for thing in temp:
                    if len(thing.split(';')) == 2:
                        points.append(thing)
                    else:
                        meta.append(str(thing))

                if len(meta) == 3:
                    for point in points:
                        if i != len(temp) - 1 and i != len(temp) - 2:
                            try:
                                grid[int(point.split(';')[0])][int(point.split(';')[1])] = [meta[1], meta[2], 'CUSTOM']
                            except IndexError as e:
                                raise Exception(f'PLEASE PLACE ITEM WITHIN THE GRID\n Code: {row}\n Line: {line}')
                else:
                    for i in range(len(temp) - 1):
                        if i != len(temp) and i != len(temp) - 2:
                            point = temp[i].split(';')
                            try:
                                grid[int(point[0])][int(point[1])] = [temp[len(temp) - 1], temp[len(temp) - 2]]
                            except IndexError as e:
                                raise Exception(f'PLEASE PLACE ITEM WITHIN THE GRID\n Code: {row}\n Line: {line}')
                continue
            if FindARG(toSearch=toCheck, arg='box') or FindARG(toSearch=toCheck, arg='B'):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                if temp[4] != 'colorTile' and temp[4] != 'cT':
                    try:
                        x1, x2, y1, y2 = int(temp[0]), int(temp[2]), int(temp[1]), int(temp[3])
                        direction = temp[5]
                        Type = temp[4]
                        for x in range(y2):
                            if x >= y1:
                                for i in range(x2):
                                    if i >= x1:
                                        if Type != 'CUSTOM':
                                            grid[i][x] = [direction, Type]
                                        else:
                                            grid[i][x] = [temp[5], temp[6], 'CUSTOM']
                    except IndexError:
                        raise Exception(f"BAD, USE 6 ARGUMENTS OR I WILL KILL UR MOTHER\n LINE: {line}\nCODE >> {row}")
                elif temp[4] == 'colorTile' or temp[4] == 'cT':
                    try:
                        x1, x2, y1, y2 = int(temp[0]), int(temp[2]), int(temp[1]), int(temp[3])
                        colorHex = temp[5]
                        name = temp[6]
                        symbol = temp[7]
                        imgProcessing.create_image(f"#{colorHex}", name)
                        for x in range(y2):
                            if x >= y1:
                                for i in range(x2):
                                    if i >= x1:
                                        print([name, symbol, 'COLORTILE'])
                                        grid[x][i] = [name, symbol, 'COLORTILE']
                    except IndexError:
                        raise Exception(f"USE 6 ARGUMENTS\n LINE: {line}\nCODE >> {row}")

                continue
            if FindARG(toSearch=toCheck, arg='colorTile') or FindARG(toSearch=toCheck, arg='cT'):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    imgProcessing.create_image(f"#{temp[2]}", temp[3])
                    grid[int(temp[0])][int(temp[1])] = [temp[3], temp[4], 'COLORTILE']
                except IndexError:
                    raise Exception(f'PLEASE PLACE WALL WITHIN THE GRID\n FOUND AT LINE {line}\nCODE >> {row}\n {temp}')
                continue
            else:
                raise Exception(f'COMMAND NOT RECOGNIZED\n FOUND AT LINE {line}\nCODE >> {row}')

    SPRITES = ['Assets/DEFAULT/WALL/wall_N_S_UP.png', 'Assets/DEFAULT/Wall/wall_E_W_SIDE.png',
               'Assets/DEFAULT/Wall/wall_CORNER.png', 'Assets/DEFAULT/DOOR/doorO.png',
               'Assets/DEFAULT/DOOR/doorC.png', 'Assets/CUSTOM/stairsU.png',
               'Assets/DEFAULT/STAIRS/stairsD.png', 'Assets/DEFAULT/CUSTOM.png',
               Default]
    # Processes Map
    i = 0
    while 1:
        foo = 'Y'
        match foo:
            case 'Y':
                for x in progressbar(it=range(len(grid)), prefix="COMPILING: ", size=40):
                    row = grid[x]
                    rowToAdd = []
                    toPrint = ''
                    for item in row:
                        if type(item) is type([]):
                            try:
                                if len(item) == 2:
                                    if item[1] == 'WALL':
                                        match item[0]:
                                            case 'N':
                                                toPrint += ' | '
                                                rowToAdd.append(' | ')
                                                paths.append(SPRITES[0])
                                            case 'S':
                                                toPrint += ' | '
                                                rowToAdd.append(' | ')
                                                paths.append(SPRITES[0])
                                            case 'UP':
                                                toPrint += ' | '
                                                rowToAdd.append(' | ')
                                                paths.append(SPRITES[0])
                                            case 'E':
                                                toPrint += ' - '
                                                rowToAdd.append(' - ')
                                                paths.append(SPRITES[1])
                                            case 'W':
                                                toPrint += ' - '
                                                rowToAdd.append(' - ')
                                                paths.append(SPRITES[1])
                                            case 'LEFT':
                                                toPrint += ' - '
                                                rowToAdd.append(' - ')
                                                paths.append(SPRITES[1])
                                            case 'RIGHT':
                                                toPrint += ' - '
                                                rowToAdd.append(' - ')
                                                paths.append(SPRITES[1])
                                            case 'SIDE':
                                                toPrint += ' - '
                                                rowToAdd.append(' - ')
                                                paths.append(SPRITES[1])
                                            case 'CORNER':
                                                toPrint += ' # '
                                                rowToAdd.append(' # ')
                                                paths.append(SPRITES[2])
                                            case _:
                                                raise Exception("PLEASE CHOOSE A VALID DIRECTION (N, E, S, W, UP, SIDE, CORNER)")
                                    elif item[1] == 'DOOR':
                                        match item[0]:
                                            case 'O':
                                                toPrint += ' O '
                                                rowToAdd.append(' O ')
                                                paths.append(SPRITES[3])
                                            case 'OPEN':
                                                toPrint += ' O '
                                                rowToAdd.append(' O ')
                                                paths.append(SPRITES[3])
                                            case 'C':
                                                toPrint += ' C '
                                                rowToAdd.append(' C ')
                                                paths.append(SPRITES[4])
                                            case 'CLOSED':
                                                toPrint += ' C '
                                                rowToAdd.append(' C ')
                                                paths.append(SPRITES[4])
                                            case _:
                                                raise Exception("PLEASE CHOOSE A VALID DIRECTION (O, OPEN, C, CLOSED)")
                                    elif item[1] == 'STAIRS':
                                        match item[0]:
                                            case 'U':
                                                toPrint += ' U '
                                                rowToAdd.append(' U ')
                                                paths.append(SPRITES[5])
                                            case 'UP':
                                                toPrint += ' U '
                                                rowToAdd.append(' U ')
                                                paths.append(SPRITES[5])
                                            case 'D':
                                                toPrint += ' D '
                                                rowToAdd.append(' D ')
                                                paths.append(SPRITES[6])
                                            case 'DOWN':
                                                toPrint += ' D '
                                                rowToAdd.append(' D ')
                                                paths.append(SPRITES[6])
                                            case _:
                                                raise Exception("PLEASE CHOOSE A VALID DIRECTION (U, UP, D, DOWN)")
                                    elif item[1] == 'PLAYER':
                                        toPrint += f' {item[0][0]} '
                                        rowToAdd.append(f' {item[0][0]} ')
                                        try:
                                            fh = open(f'Assets/DEFAULT/PLAYERS/{item[0]}.png', 'r')
                                            paths.append(f'Assets/DEFAULT/PLAYERS/{item[0]}.png')
                                        except FileNotFoundError:
                                            paths.append('Assets/DEFAULT/PLAYERS/DefultPlayer.png')
                                    elif item[1] == 'ENEMY':
                                        toPrint += f' {item[0][0]} '
                                        rowToAdd.append(f' {item[0][0]} ')
                                        try:
                                            fh = open(f'Assets/DEFAULT/ENEMIES/{item[0]}.png', 'r')
                                            paths.append(f'Assets/DEFAULT/ENEMIES/{item[0]}.png')
                                        except FileNotFoundError:
                                            paths.append('Assets/DEFAULT/ENEMIES/DefultEnemy.png')
                                    elif item[1] == 'EMPTY':
                                        toPrint += f'   '
                                        rowToAdd.append(f'   ')
                                        paths.append(SPRITES[len(SPRITES) - 1])
                                elif len(item) == 3:
                                    if item[2] == 'CUSTOM':
                                        toPrint += f' {item[1]} '
                                        rowToAdd.append(f' {item[1]} ')
                                        try:
                                            fh = open(f'Assets/CUSTOM/{item[0]}.png', 'r')
                                            paths.append(f'Assets/CUSTOM/{item[0]}.png')
                                        except FileNotFoundError:
                                            paths.append(SPRITES[7])
                                    elif item[2] == 'COLORTILE':
                                        toPrint += f' {item[1]} '
                                        rowToAdd.append(f' {item[1]} ')
                                        try:
                                            fh = open(f'Assets/CustomColorTiles/{item[0]}.png', 'r')
                                            paths.append(f'Assets/CustomColorTiles/{item[0]}.png')
                                        except FileNotFoundError:
                                            paths.append(SPRITES[7])
                                elif not item:
                                    toPrint += '   '
                                    rowToAdd.append(f'   ')
                                    paths.append(SPRITES[len(SPRITES) - 1])
                                else:
                                    raise Exception(
                                        f"PLEASE ONLY USE THE CURRENT AVAILABLE COMMANDS\n INVALID COMMAND >> {item}")
                            except IndexError:
                                continue
                    if intoRaw:
                        print(toPrint)
                    compiled += "# " + toPrint + '\n'
                    imgProcessing.MakeRow(row=paths, name=f'Compiled/Rows/row{i}.png')
                    rowPaths.append(f'Compiled/Rows/row{i}.png')
                    print(toPrint)
                    paths = []
                    i += 1
                break
            case 'N':
                break
            case _:
                print("PLEASE ENTER A VALID COMMAND (Y or N)")
    # Combines all rows into one image
    imgProcessing.CombineRows(rowPaths, compiledName)

def DMLtoArray(fileName):
    paths, rowPaths, grid = [], [], []
    commands = ['holdMeta']
    line = 0
    File = fileName  # Define the File to Read
    config = [False]

    print(f'OPENING: {File}\n')
    try:
        with open(File, 'r') as fh:
            raw = fh.read()
    except:
        try:
            File = 'DML_Files/' + File  # Define the File to Read
            with open(File, 'r') as fh:
                raw = fh.read()
        except:
            print(File)
            # raise Exception("PLEASE ENTER A VALID FILE TYPE")
    fileRows = raw.split('\n')
    # Read DML and compiles it
    for i in progressbar(it=range(len(fileRows)), prefix="READING: ", size=40, char='~'):
        row = fileRows[i]
        line += 1
        try:
            if row.replace(' ', '')[0] == '#' or row == '':
                continue
        except IndexError:
            if row == '':
                continue
        if FindARG(toSearch=row, arg='META'):
            continue
        if FindARG(toSearch=row, arg='CONFIG'):
            temp = ((row.split(':'))[1].replace(' ', '').split('#'))[0].split(',')
            Found = False
            temp2 = None
            for arg in temp:
                temp2 = arg.split('/')
                for command in commands:
                    if temp2[0] == command:
                        Found = True
                        break
            if not Found:
                raise Exception(f"INVALID COMMAND ON LINE {line}\nCODE >> {fileRows[line - 1]}")
            else:
                match temp2[0]:
                    case 'holdMeta':
                        if temp2[1]:
                            config[0] = True
            continue
        if FindARG(toSearch=row, arg="mapSize"):
            temp = row.split(':')
            temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
            gridSize = [int(temp[0]), int(temp[1])]
            for x in range(gridSize[0]):
                grid.append([])
                for y in range(gridSize[1]):
                    grid[x].append([])
            continue
        if grid != []:
            if FindARG(toSearch=row, arg="wall"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'WALL']
                except IndexError:
                    raise Exception('PLEASE PLACE WALL WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg="door"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'DOOR']
                except IndexError:
                    raise Exception('PLEASE PLACE DOOR WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg="stairs"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'STAIRS']
                except IndexError:
                    raise Exception('PLEASE PLACE STAIRS WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg="clear"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = []
                except IndexError:
                    raise Exception('PLEASE REMOVE SOMETHING WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg="custom"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], temp[3], 'CUSTOM']
                except IndexError:
                    raise Exception('PLEASE PLACE CUSTOM ITEM WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg='player'):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'PLAYER']
                except IndexError:
                    raise Exception('PLEASE PLACE PLAYER WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg='enemy'):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'ENEMY']
                except IndexError:
                    raise Exception('PLEASE PLACE ENEMY WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg='group'):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                for i in range(len(temp) - 1):
                    if i != len(temp) and i != len(temp) - 2:
                        point = temp[i].split(';')
                        try:
                            grid[int(point[0])][int(point[1])] = [temp[len(temp) - 1], temp[len(temp) - 2]]
                        except IndexError as e:
                            raise Exception(f'PLEASE PLACE ITEM WITHIN THE GRID\n Code: {row}\n Line: {line}')
                continue
            if FindARG(toSearch=row, arg='box'):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    x1, x2, y1, y2 = int(temp[0]), int(temp[2]), int(temp[1]), int(temp[3])
                    direction = temp[5]
                    Type = temp[4]
                    for x in range(y2):
                        if x >= y1:
                            for i in range(x2):
                                if i >= x1:
                                    if Type != 'CUSTOM':
                                        grid[i][x] = [direction, Type]
                                    else:
                                        grid[i][x] = [temp[5], temp[6], 'CUSTOM']
                except IndexError:
                    raise Exception("BAD, USE 6 ARGUMENTS OR I WILL KILL UR MOTHER")
                continue
            else:
                raise Exception(f'COMMAND NOT RECOGNIZED\n FOUND AT LINE {line}\nCODE >> {row}')

    return grid

def DMLtoArrayLAT(fileName):
    paths, rowPaths, grid = [], [], []
    commands = ['holdMeta']
    line = 0
    File = fileName  # Define the File to Read
    config = [False]

    print(f'OPENING: {File}\n')
    try:
        with open(File, 'r') as fh:
            raw = fh.read()
    except:
        try:
            File = 'Latin Assets/DML_Files/' + File  # Define the File to Read
            with open(File, 'r') as fh:
                raw = fh.read()
        except:
            print(File)
            # raise Exception("PLEASE ENTER A VALID FILE TYPE")
    fileRows = raw.split('\n')
    # Read DML and compiles it
    for i in progressbar(it=range(len(fileRows)), prefix="PARSING: ", size=40, char='~'):
        row = fileRows[i]
        line += 1
        try:
            if row.replace(' ', '')[0] == '#' or row == '':
                continue
        except IndexError:
            if row == '':
                continue
        if FindARG(toSearch=row, arg='META'):
            continue
        if FindARG(toSearch=row, arg='CONFIG'):
            temp = ((row.split(':'))[1].replace(' ', '').split('#'))[0].split(',')
            Found = False
            temp2 = None
            for arg in temp:
                temp2 = arg.split('/')
                for command in commands:
                    if temp2[0] == command:
                        Found = True
                        break
            if not Found:
                raise Exception(f"INVALID COMMAND ON LINE {line}\nCODE >> {fileRows[line - 1]}")
            else:
                match temp2[0]:
                    case 'holdMeta':
                        if temp2[1]:
                            config[0] = True
            continue
        if FindARG(toSearch=row, arg="mapSize"):
            temp = row.split(':')
            temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
            gridSize = [int(temp[0]), int(temp[1])]
            for x in range(gridSize[0]):
                grid.append([])
                for y in range(gridSize[1]):
                    grid[x].append([])
            continue
        if grid != []:
            if FindARG(toSearch=row, arg="wall"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'WALL']
                except IndexError:
                    raise Exception('PLEASE PLACE WALL WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg="door"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'DOOR']
                except IndexError:
                    raise Exception('PLEASE PLACE DOOR WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg="stairs"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'STAIRS']
                except IndexError:
                    raise Exception('PLEASE PLACE STAIRS WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg="clear"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = []
                except IndexError:
                    raise Exception('PLEASE REMOVE SOMETHING WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg="custom"):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], temp[3], 'CUSTOM']
                except IndexError:
                    raise Exception('PLEASE PLACE CUSTOM ITEM WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg='player'):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'PLAYER']
                except IndexError:
                    raise Exception('PLEASE PLACE PLAYER WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg='enemy'):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    grid[int(temp[0])][int(temp[1])] = [temp[2], 'ENEMY']
                except IndexError:
                    raise Exception('PLEASE PLACE ENEMY WITHIN THE GRID')
                continue
            if FindARG(toSearch=row, arg='group'):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                for i in range(len(temp) - 1):
                    if i != len(temp) and i != len(temp) - 2:
                        point = temp[i].split(';')
                        try:
                            grid[int(point[0])][int(point[1])] = [temp[len(temp) - 1], temp[len(temp) - 2]]
                        except IndexError as e:
                            raise Exception(f'PLEASE PLACE ITEM WITHIN THE GRID\n Code: {row}\n Line: {line}')
                continue
            if FindARG(toSearch=row, arg='box'):
                temp = row.split(':')
                temp = (temp[1].replace(' ', '').split('#'))[0].split(',')
                try:
                    x1, x2, y1, y2 = int(temp[0]), int(temp[2]), int(temp[1]), int(temp[3])
                    direction = temp[5]
                    Type = temp[4]
                    for x in range(y2):
                        if x >= y1:
                            for i in range(x2):
                                if i >= x1:
                                    if Type != 'CUSTOM':
                                        grid[i][x] = [direction, Type]
                                    else:
                                        grid[i][x] = [temp[5], temp[6], 'CUSTOM']
                except IndexError:
                    raise Exception("BAD, USE 6 ARGUMENTS OR I WILL KILL UR MOTHER")
                continue
            else:
                raise Exception(f'COMMAND NOT RECOGNIZED\n FOUND AT LINE {line}\nCODE >> {row}')


    return grid

def DisplayArr(arr):
    out = ''
    i = 0
    while 1:
        foo = 'Y'
        match foo:
            case 'Y':
                for x in progressbar(it=range(len(arr)), prefix="COMPILING: ", size=40, char=u"█"):
                    row = arr[x]
                    rowToAdd = []
                    toPrint = ''
                    for item in row:
                        if type(item) is type([]):
                            try:
                                if len(item) == 2:
                                    if item[1] == 'WALL':
                                        match item[0]:
                                            case 'N':
                                                toPrint += ' | '
                                                rowToAdd.append(' | ')
                                            case 'S':
                                                toPrint += ' | '
                                                rowToAdd.append(' | ')
                                            case 'UP':
                                                toPrint += ' | '
                                                rowToAdd.append(' | ')
                                            case 'E':
                                                toPrint += ' - '
                                                rowToAdd.append(' - ')
                                            case 'W':
                                                toPrint += ' - '
                                                rowToAdd.append(' - ')
                                            case 'SIDE':
                                                toPrint += ' - '
                                                rowToAdd.append(' - ')
                                            case 'CORNER':
                                                toPrint += ' # '
                                                rowToAdd.append(' # ')
                                            case _:
                                                raise Exception(
                                                    "PLEASE CHOOSE A VALID DIRECTION (N, E, S, W, UP, SIDE, CORNER)")
                                    elif item[1] == 'DOOR':
                                        match item[0]:
                                            case 'O':
                                                toPrint += ' O '
                                                rowToAdd.append(' O ')
                                            case 'OPEN':
                                                toPrint += ' O '
                                                rowToAdd.append(' O ')
                                            case 'C':
                                                toPrint += ' C '
                                                rowToAdd.append(' C ')
                                            case 'CLOSED':
                                                toPrint += ' C '
                                                rowToAdd.append(' C ')
                                            case _:
                                                raise Exception("PLEASE CHOOSE A VALID DIRECTION (O, OPEN, C, CLOSED)")
                                    elif item[1] == 'STAIRS':
                                        match item[0]:
                                            case 'U':
                                                toPrint += ' U '
                                                rowToAdd.append(' U ')
                                            case 'UP':
                                                toPrint += ' U '
                                                rowToAdd.append(' U ')
                                            case 'D':
                                                toPrint += ' D '
                                                rowToAdd.append(' D ')
                                            case 'DOWN':
                                                toPrint += ' D '
                                                rowToAdd.append(' D ')
                                            case _:
                                                raise Exception("PLEASE CHOOSE A VALID DIRECTION (U, UP, D, DOWN)")
                                    elif item[1] == 'PLAYER':
                                        toPrint += f' {item[0][0]} '
                                        rowToAdd.append(f' {item[0][0]} ')
                                    elif item[1] == 'ENEMY':
                                        toPrint += f' {item[0][0]} '
                                        rowToAdd.append(f' {item[0][0]} ')
                                    elif item[1] == 'EMPTY':
                                        toPrint += f'   '
                                        rowToAdd.append(f'   ')
                                elif len(item) == 3:
                                    if item[2] == 'CUSTOM':
                                        toPrint += f' {item[1]} '
                                        rowToAdd.append(f' {item[1]} ')
                                elif not item:
                                    toPrint += '   '
                                    rowToAdd.append(f'   ')
                                else:
                                    raise Exception(
                                        f"PLEASE ONLY USE THE CURRENT AVAILABLE COMMANDS\n INVALID COMMAND >> {item}")
                            except IndexError:
                                continue
                    out += toPrint + '\n'
                    paths = []
                    i += 1
                break
            case 'N':
                break
            case _:
                print("PLEASE ENTER A VALID COMMAND (Y or N)")

    print(out)