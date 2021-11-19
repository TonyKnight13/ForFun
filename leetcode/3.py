 
def lengthOfLongestSubstring(s: str) -> int:
    slen = len(s)
    if slen < 2 :
        return slen
    
    dp = [1 for _ in range(slen)]
    d = dict()
    
    d[s[0]] = 0
    for i in range(1, slen):
        if s[i] in d:
            if dp[i-1] >= i - d[s[i]]:
                dp[i] = i - d[s[i]]
            else:
                dp[i] = dp[i-1] + 1
        else:
            dp[i] = dp[i-1] + 1
        
        d[s[i]] = i 
    return max(dp)

s = "abcabcbb"
print(lengthOfLongestSubstring(s))

# 超时间限
# def lengthOfLongestSubstring2(s: str) -> int:
#         if s == "":
#             return 0
#         maxl = 0

#         for j in  range(len(s)):
#             windowhead = j
#             windowtail = j
#             for i in range(j, len(s)):
#                 if s[i] in smax:
#                     windowhead = i
#                     windowtail = i + 1
#                 else:
#                     windowtail += 1
#                     smax = s[windowhead:windowtail]
#                     l = windowtail - windowhead
#                     maxl = max(l,maxl)
#         return maxl

# print(lengthOfLongestSubstring("asjrgapa"))