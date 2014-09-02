from PIL import Image
from PIL import ImageDraw
import sqlite3
from lxml import etree
import os.path
import os
import sys



def draw_nodes(im, nodelist):
    for x in nodelist:
        draw.ellipse(x,fill=1,outline=128)
    """
    Draws ellipses representing nodes onto an image. The center of the ellipse
        is the x,y coordinate of the node.
    Input Parameters:
    my_map_image -- PIL Image object.
    node_list -- tuple of tuples, with each inner tuple representing a node
        in format (id, (lat, lon))
    bounding_box -- 4-tuple representing bounds of the OSM map.
        the order of elements is (minlat, maxlat, minlon, maxlon)
    """



def draw_ways(im, linelist):
    for line in linelist:
        draw.line(line,fill=220,width=2)
    """
    Draws line segments representing ways onto an image.
    Input Parameters:
    my_map_image -- PIL Image object.
    way_list -- tuple of tuples, with each inner tuple representing the node ids
        in a particular way
    node_list -- tuple of tuples, with each inner tuple representing a node
        in format (id, (lat, lon))
    bounding_box -- 4-tuple representing bounds of the OSM map.
        the order of elements is (minlat, maxlat, minlon, maxlon)
    """


def save_to_file(im, file_name):
    """
    Saves PIL image my_map_image to file file_name

    """

    im.save(file_name)

def get_map(map_file_name):
    """
    Reads an osm file and returns information from the file.

    Input Parameters:
    map_file_name: string file name for the map file

    Return value: A 3 tuple containing the following elements

    bounding box -- 4-tuple listing the bounds of the map,
        in order (minlat, maxlat, minlon, maxlon)
    node list -- tuple of tuples, with each inner tuple representing a node
        in format (id, (lat, lon))
    way list -- tuple of tuples, with each inner tuple representing the node ids
        in a particular way

    """
    mapinfo=() 
    nodelist=() 
    wayinfo=() 
    boundinfo=()
    ps=etree.parse(map_file_name)
    nodes=ps.findall('node')
    ways=ps.findall('way')
    bounds=ps.find('bounds')
    boundinfo+=(float(bounds.get('minlat')),)
    boundinfo+=(float(bounds.get('maxlat')),)
    boundinfo+=(float(bounds.get('minlon')),)
    boundinfo+=(float(bounds.get('maxlon')),)
    for nd in nodes:
        nodetuple=(int(nd.get('id')),(float(nd.get('lat')),float(nd.get('lon'))))
        nodelist+=(nodetuple)
    for way in ways:
        nds=way.findall('nd')
        reftuple=()
        for nd in nds:
            ref=int(nd.get('ref'))
            reftuple+=(ref,)
        wayid=int(way.get('id'))
        wayinfo+=(wayid,reftuple)
    mapinfo+=(boundinfo,)
    mapinfo+=(nodelist,)
    mapinfo+=(wayinfo,)
    return mapinfo
#########################################################################

########################################################################
def create_nodelist(mapinfo,latwidth,longth):
    latsize=mapinfo[0][1]-mapinfo[0][0]
    lonsize=mapinfo[0][3]-mapinfo[0][2]
    latwidth=2048
    longth=2048
    longth=int (latwidth*lonsize/latsize)
    pointxy=mapinfo[1][1::2]
    nodelist=()
    for x,y in pointxy:
        if x>=mapinfo[0][0] and x<=mapinfo[0][1] and y<=mapinfo[0][3] and y>=mapinfo[0][2]:
            x=int((x-mapinfo[0][0])*latwidth/latsize)
            y=int((y-mapinfo[0][2])*longth/lonsize)
            x0=x-5
            y0=y-5
            x1=x+5
            y1=y+5
            #print(x,y),
            nodelist+=((x0,y0,x1,y1),)
    del pointxy
    return nodelist
#########################################################################

########################################################################   
def create_linelist(mapinfo,latwidth,longth):
    latsize=mapinfo[0][1]-mapinfo[0][0]
    lonsize=mapinfo[0][3]-mapinfo[0][2]
    latwidth=2048
    longth=2048
    longth=int (latwidth*lonsize/latsize)
    #print mapinfo[1][0:5]
    #print 'here'
    zipnode=zip(mapinfo[1][0::2],mapinfo[1][1::2])
    #print zipnode[0:10]
    #print 'here2'
    dictnode=dict(zipnode) #dict of nodes, id as key,(lat,lon as value)
    #print dictnode[0:10]
    linelist=()#store r x,y
    maplinelist=()#store lat,lon
    reflist=mapinfo[2][1::2]#all refs
    #print reflist[0][1:5]
    #print 'eee'
    for refs in reflist: #query value by ref
        singleline=()
        for ref in refs:
            checkexist=dictnode.get(ref)
            if checkexist!=None:
              singleline+=(checkexist,)
        maplinelist+=(singleline,)# get a tuple of tuples storing all line's ndoes
    #print maplinelist[0]
    for lines in maplinelist:#transfer lat lon to xy
        temline=()
        for x,y in lines:
            if x>=mapinfo[0][0] and x<=mapinfo[0][1] and y<=mapinfo[0][3] and y>=mapinfo[0][2]:
                x=int((x-mapinfo[0][0])*latwidth/latsize)
                y=int((y-mapinfo[0][2])*longth/lonsize)
                temline+=((x,y),)
                linelist+=(temline,)#put each line into linelist
    #print linelist
    return linelist





if __name__=="__main__":   
    
    if os.path.isfile('map.db')==True:
        os.remove('map.db')
    dbfile=open('map.db','wb')
    osmname=sys.argv[1]
    ps=etree.parse(osmname)
    nodes=ps.findall('node')
    ways=ps.findall('way')
    bounds=ps.find('bounds')
    mapinfo=get_map(osmname)
    #print mapinfo[0][0]
    #print len(mapinfo[1])
    #print mapinfo[2][1]
    #print mapinfo[1][1]
    
    ######################################
    '''initialize database'''
    ######################################
    
    conn=sqlite3.connect('map.db')
    conn.execute('''CREATE TABLE NODE
        (ID            REAL   ,
         LAT           REAL   ,
         LON           REAL);''')
    conn.execute('''CREATE TABLE WAY
        (ID REAL)''')
    #############################################################
    '''import into database from osm'''
    ##############################################################
    for nd in nodes:
        nodeid=int(nd.get('id'))
        nodelat=float(nd.get('lat'))
        nodelon=float(nd.get('lat'))
        conn.execute("INSERT INTO NODE (ID,LAT,LON) \
            VALUES(?,?,?)",(nodeid,nodelat,nodelon));
    for way in ways:
        wayid=int (way.get('id'))
        conn.execute("INSERT INTO WAY (ID) \
            VALUES(?)",(wayid,));
    cursor=conn.execute('SELECT id from NODE');
    ##############################################################
    count=0
    for row in cursor:
        count+=1
    print count,
    cursor=conn.execute('SELECT id from WAY');
    count=0
    for row in cursor:
        count+=1
    print count
    ################################################################
    '''draw picture here!'''
    #################################################################
    latsize=mapinfo[0][1]-mapinfo[0][0]
    lonsize=mapinfo[0][3]-mapinfo[0][2]
    latwidth=2048
    longth=2048
    longth=int (latwidth*lonsize/latsize)
    #mapxy=map_to_image(mapinfo,latwidth,longth)
    #pointxy=[x[1] for x in mapinfo[1]]
    #print pointxy[0:10]
    pointxy=mapinfo[1][1::2]
    mapxy=()
    for x,y in pointxy:
        if x>=mapinfo[0][0] and x<=mapinfo[0][1] and y<=mapinfo[0][3] and y>=mapinfo[0][2]:
            x=int((x-mapinfo[0][0])*latwidth/latsize)
            y=int((y-mapinfo[0][2])*longth/lonsize)
            #x1=float(x)
            mapxy+=((x,y),)
    '''
    print mapinfo[0]
    print latsize
    print lonsize
    print longth
    print mapxy[0:15]
    mapxy=mapxy[0:15]
    '''
########################################################################
    #print 'xixi'
    #print mapinfo[2][0:5]
    nodelist=create_nodelist(mapinfo,latwidth,longth)
    #print nodelist[0:5]
    linelist=create_linelist(mapinfo,latwidth,longth)
    #print linelist[0:2]
    
    im = Image.new("RGB", (latwidth, longth),"white")
    draw = ImageDraw.Draw(im)
    file_name='output.jpg'
    draw_nodes(im, nodelist)
    draw_ways(im, linelist)
    im=im.rotate(90)
    save_to_file(im, file_name)
    #im.show()

    '''
    print linelist
    for x in nodelist:
        draw.ellipse(x,fill=1,outline=128)
    for line in linelist:
        draw.line(line,fill=220,width=2)
    #im.rotate(90).show()
    #im.rotate(90).save('output.jpg')
    im.rotate(90).show()
    '''
    
    



