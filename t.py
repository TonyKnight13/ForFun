class Solution:
    """
    @param: a: An integer
    @param: b: An integer
    @return: The sum of a and b
    """
    def aplusb(self, a, b):
        # write your code here
        if((a&b)==0):
            return a|b
        return self.aplusb((a&b)<<1,a^b)

x = Solution()
d = x.aplusb(100,-100)
print(d)