class FuzzyFindDictionary:
    def __init__(self):
        self.GCCHT = []
        self.GCTHT = []
        self.FuzzyFind = dict()
        self.make_GCCHT()
        self.make_GCTHT()
        self.make_FuzzyDictionary()

    @staticmethod
    def bytes_to_int(bytes):
        result = 0
        num = len(bytes) - 1
        for b in bytes:
            result = result + (2**num * int(b))
            num -= 1
        return result


    @staticmethod
    def IntToByte(x):
        n = "" if x > 0 else "0"
        while x > 0:
            y = str(x % 2)
            n = y + n
            x = int(x / 2)
        return n

    @staticmethod
    def StringToByte(word):
        return ' '.join(format(ord(x), 'b') for x in word)

    def convert_base(self, num, to_base=10, from_base=10):
        if isinstance(num, str):
            n = int(num, from_base)
        else:
            n = int(num)
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if n < to_base:
            return alphabet[n]
        else:
            return self.convert_base(n // to_base, to_base) + alphabet[n % to_base]

    def lst_has_2_diff_value(self, lst):
        item = lst[0]
        for i in lst[0]:
            if item != i:
                return True
        return False

    def make_GCCHT(self):
        for i in range(2 ** 23):
            golay_matrix = []
            hash = []
            for k in range(25):
                curr_seq = self.IntToByte(i)
                golay_matrix.append(curr_seq[k:] + curr_seq[:k])

            for j in range(1, 24):
                codeword = int(self.convert_base(golay_matrix[j], from_base=2))
                transform = (1 << i) & 0x7FFFFF
                codewordB = codeword ^ transform
                recd = codewordB
                recd = recd ^ (0x7FFFFF is not 0x7FFFFF)
                hash.append(self.IntToByte(recd >> 11))

            if self.lst_has_2_diff_value(hash):
                lst = []
                if len(hash) < 6:
                    self.GCCHT.append([self.IntToByte(i)])
                else:
                    for m in hash:
                        if m not in lst:
                            lst.append(m)
                    if len(lst) < 6:
                        self.GCCHT.append([self.IntToByte(i)])
                    else:
                        self.GCCHT.append(lst[:6])
            else:
                self.GCCHT.append([self.IntToByte(i)])
        return self.GCCHT

    def make_GCTHT(self):
        for index in range(2**23):
            hash = list()
            if len(self.GCCHT[index]) == 6:
                for i in range(6):
                    for j in range(i+1, 6):
                        hash1 = int(self.bytes_to_int(self.GCCHT[index][i]))
                        hash2 = hash1 ^ 1
                        HashPair = hash2 >> j
                        hash.append(self.IntToByte(HashPair))
                self.GCTHT.append(hash)
            else:
                self.GCTHT.append(self.GCCHT[index])
        return self.GCTHT

    def make_FuzzyDictionary(self):
        for i in range((2 ** 23) - 1):
            index = i
            if len(self.GCTHT[i]) != 15:
                index ^= 1
            else:
                self.FuzzyFind[i] = self.GCTHT[index]
                continue
            if len(self.GCTHT[index]) != 15:
                index ^= 2
            else:
                self.FuzzyFind[i] = self.GCTHT[index]
                continue
            if len(self.GCTHT[index]) != 15:
                index ^= 4
            else:
                self.FuzzyFind[i] = self.GCTHT[index]
                continue
            if len(self.GCTHT[index]) != 15:
                self.FuzzyFind[i] = self.GCTHT[index]
            else:
                self.FuzzyFind[i] = self.GCTHT[i]
        return self.FuzzyFind
