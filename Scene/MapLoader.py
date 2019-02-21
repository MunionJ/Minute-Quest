

def loadMap(filename):
    """Parses the file output from Tiled into a map structure"""
    fp = None
    try:
        fp = open(filename, 'r')  # Reads file
    except:
        print(filename + ' not found.');
        return None

    section = None
    mymap = {}
    headermap = {}
    layerData = []
    tileData = None
    readingData = False
    map_h = None
    dataCount = 0
    for line in fp:
        if line[-1] == '\n':
            line = line[0:-1]

        if line and line[0] == '[' and line[-1] == ']':
            section = line[1:-1]

        if section == 'header' and '=' in line:
            key, value = line.split('=')
            key.strip()
            key.rstrip()
            value.strip()
            value.rstrip()
            if 'orientation' not in key:
                value = [int(datum) for datum in value.split(',') if len(datum)] if ',' in value else int(value)
            headermap[key] = value
            if key == 'height':
                map_h = int(value)
        elif section == 'tilesets' and '=' in line:
            lhs, rhs = line.split('=')
            tilesetInfo = rhs.split(',')
            lhs.strip()
            lhs.rstrip()
            rhs.strip()
            rhs.rstrip()
            toAdd = [tilesetInfo[0]]
            for i in range(1, len(tilesetInfo)):
                toAdd.append(int(tilesetInfo[i]))
            mymap[lhs] = toAdd                              #filename, tile_width,tile_height,gap_x,gap_y
        elif section == 'layer':
            if readingData:
                dataCount += 1
                tileStr = line.split(',')
                lineData = [int(datum) - 1 for datum in tileStr if len(datum)]
                tileData.append(lineData)
                if dataCount == map_h:
                    readingData = False
                    layerData.append(tileData)
            if 'data' in line:
                readingData = True
                tileData = []
                dataCount = 0

    mymap['header'] = headermap

    mymap['layers'] = layerData

    fp.close()
    return mymap