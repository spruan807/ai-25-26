from collections import deque, defaultdict

# shirley ruan
# have not yet tested on example 2, but example 1 works!

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def inorderTraversal(root):
        work = deque()
        length = defaultdict(int)
        gen = defaultdict(int)
        done = defaultdict(int)
        ans = []

        work.append(root)
        gen[root] = 0
        length[root] = 0

        def setValues(p, c, lr):
            gen[c] = gen[p] + 1

            if lr=="left":
                length[c] = length[p] - gen[c]
            else:
                length[c] = length[p] + gen[c]
            work.append(c)

        while work:
            curr = work.popleft()
            left = curr.left
            right = curr.right

            if left is not None:
                setValues(curr,left,"left")
            if right is not None:
                setValues(curr,right,"right")

        checkLengths = length.items()
        swappedLengths = []

        # i forgot how to use sorted...
        for l in checkLengths:
            x,y = l
            swappedLengths.append((y,x))

        swappedLengths = sorted(swappedLengths)

        for l in swappedLengths:
            x,y = l
            ans.append(y.val)

        return ans

def main():
    ex3 = TreeNode(3)
    ex2 = TreeNode(2,ex3)
    ex1 = TreeNode(1,None,ex2)

    ans1 = Solution.inorderTraversal(ex1)

    print(ans1)

main()
