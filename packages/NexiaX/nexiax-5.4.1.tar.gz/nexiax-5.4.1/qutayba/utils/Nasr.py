import Nasr
def Hard(source):
    source = Nasr.k64encode(source)
    enc = f'''import Nasr
source = {source!r}
exec(compile(Nasr.k64decode(source), "<decrypted>", "exec"))'''
    return enc