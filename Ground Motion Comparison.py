import UsefulFunctions as uf

auto = {}
man = {}
difs = {}
nums = [1, 2, 3, 9, 10]
for n in nums:
    auto[n] = uf.Earthquake(f'Data/Southern Alaska Coast/grids/QCF{n}grid.xml')
    man[n] = uf.Earthquake(f'Data/Southern Alaska Coast/grids/QCF{n}man_grid.xml')
    difs[n] = auto[n].mmi - man[n].mmi
