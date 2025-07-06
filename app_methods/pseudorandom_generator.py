class Generator:
    def __init__(self, m: int, a: int, c: int, x0: int, k: int):
        self.m = m
        self.a = a
        self.c = c
        self.x0 = x0
        self.k = k

    def generate(self) -> dict:
        l = [self.x0]
        x_next = (self.a * self.x0 + self.c) % self.m

        while x_next not in l:
            l.append(x_next)
            x_prev = x_next
            x_next = (self.a * x_prev + self.c) % self.m

        p = len(l)

        if self.k <= p:
            sequence_to_display = l[:self.k]
        else:
            sequence_to_display = l + [l[(i - p) % p] for i in range(p, self.k)]

        return {"period": p, "sequence": sequence_to_display}
