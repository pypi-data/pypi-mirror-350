import Nasr
def s(source):
    source = Nasr.nexia(source)
    enc = f'''import Nasr
source = {source!r}
exec(compile(Nexia.Nexia(source), "<decrypted>", "exec"))'''
    return enc