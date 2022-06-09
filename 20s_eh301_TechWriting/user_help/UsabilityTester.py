from pprint import pprint as ppt
"""
hurricanes = [
    ("Howard",(-17,2),"Beta"),
    ("Darby",(11,18),"Alpha"),
    ("Kay",(20,15),"Beta"),
    ("Ceilia",(14,-1),"Beta"),
    ("Lester",(-3,5),"Beta"),
    ("Agatha",(4,-27),"Alpha"),
    ("Javier",(-6,10),"Beta"),
    ("Frank",(-9,-58),"Gamma"),
    ("Ivette",(1,-12),"Beta"),
    ("Estelle",(14,-27),"Beta"),
    ("Georgette",(17,12),"Beta"),
    ("Blas",(14,-41),"Beta"),
    ]
"""

IDs = [
    2681,
    2674,
    2638,
    2671,
    2678,
    2659,
    2679,
    2683,
    2688,
    2673,
    2677,
    2654,
    ]

Names=[
    "Howard",
    "Darby",
    "Kay",
    "Ceilia",
    "Lester",
    "Agatha",
    "Javier",
    "Frank",
    "Ivette",
    "Estelle",
    "Georgette",
    "Blas",
    ]

Types=[
    "Beta",
    "Alpha",
    "Alpha",
    "Beta",
    "Beta",
    "Alpha",
    "Beta",
    "Gamma",
    "Beta",
    "Beta",
    "Gamma",
    "Beta",
    ]
Coords=[
    (-17,2),
    (11,18),
    (20,15),
    (14,-1),
    (-3,5),
    (4,-27),
    (-6,10),
    (-9,-58),
    (1,-12),
    (14,-27),
    (17,12),
    (14,-41),
    ]

"""
ZIP
"""
hurricanes = list(zip(Names,Coords,Types))

print("\n\nZIP\n")
ppt(hurricanes)



"""
MAP
"""
hurricanes = list(map(
    list,
    hurricanes,
    ))

print("\n\nMAP\n")
ppt(hurricanes)


"""
LAMBDA
"""
hurricanes = list(map(
    lambda a,b: a+[b],
    hurricanes,
    IDs,
    ))

print("\n\nLAMBDA\n")
ppt(hurricanes)


"""
SORTED
"""
hurricanes = list(sorted(
    hurricanes,
    key=lambda a: a[0],
    ))

print("\n\nSORTED\n")
ppt(hurricanes)


"""
FILTER
"""

hurricanes = list(filter(
    lambda a: a[2]=="Beta",
    hurricanes,
    ))

print("\n\nFILTER\n")
ppt(hurricanes)


"""
LIST COMPREHENSION
"""
N_hc = [ i[0] for i in hurricanes if (i[1][0] > 0) ]

print("\n\nCOMPREHENSION\n")
ppt(N_hc)



"""
ppt(list(map(
    lambda a,b: list(b)+list(a),
    hurricanes,
    IDs,
    )))
"""
