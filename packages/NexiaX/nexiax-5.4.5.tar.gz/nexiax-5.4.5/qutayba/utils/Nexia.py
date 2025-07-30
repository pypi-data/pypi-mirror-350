def R2(ψ): return [(ord(c) + i * i) % 127 for i, c in enumerate(ψ[::-1])]
def R1(δ): return ''.join([chr((c - i * i) % 127) for i, c in enumerate(δ)][::-1])
def κ1(κ): return [((ord(c) * (i + 3) + (i * i % 7)) % 95) + 32 for i, c in enumerate(κ)]
def κ2(λ): return ''.join([chr(((c - 32 - (i * i % 7)) % 95) // (i + 3)) for i, c in enumerate(λ)])
def μ1(α, β): return [(α[i] + β[i % len(β)]) % 127 for i in range(len(α))]
def My2(α, β): return [(α[i] - β[i % len(β)]) % 127 for i in range(len(α))]

def Ψ(τ, κ):
    a = κ1(κ)
    b = R2(κ)
    c = R2(τ)
    d = μ1(c, a)
    return μ1(d, b)

def Ω(ε, κ):
    a = κ1(κ)
    b = R2(κ)
    c = My2(ε, b)
    d = My2(c, a)
    return R1(d)

def enc(source):
    key = ("/sdcard/Android/data/ru.iiec.nasr/Source.py").strip()
    encrypted = Ψ(source, key)
    k = f'''python = "{key}"
data = {encrypted}
def R2(ψ): return [(ord(c) + i * i) % 127 for i, c in enumerate(ψ[::-1])]
def R1(δ): return ''.join([chr((c - i * i) % 127) for i, c in enumerate(δ)][::-1])
def κ1(κ): return [((ord(c) * (i + 3) + (i * i % 7)) % 95) + 32 for i, c in enumerate(κ)]
def μ1(α, β): return [(α[i] + β[i % len(β)]) % 127 for i in range(len(α))]
def My2(α, β): return [(α[i] - β[i % len(β)]) % 127 for i in range(len(α))]
def R1(δ): return ''.join([chr((c - i * i) % 127) for i, c in enumerate(δ)][::-1])
def Ω(ε, κ):
    a = κ1(κ)
    b = R2(κ)
    c = My2(ε, b)
    d = My2(c, a)
    return R1(d)
decrypted = Ω(data, python)
decrypted = decrypted.replace('\\x00', '')
exec(compile(decrypted, "<decrypted>", "exec"))
'''

    return k