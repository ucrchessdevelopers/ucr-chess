import hello.models as mds

def read(name, rating, record):
    a = mds.Player()
    (a.name, a.rating, a.record) = (name, rating, record)
    a.save()
    print(name + ' saved.')

def delete(args):
    mds.Player.objects.filter(name = args).delete()
    print(args + ' deleted.')
