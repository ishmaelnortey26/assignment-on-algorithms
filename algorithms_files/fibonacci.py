
def fibonacci(n):
   # Computes the nth Fibonacci number using an iterative approach.
   if n < 0:
       raise ValueError("n must be >= 0")

   if n == 0:
       return 0
   if n == 1:
       return 1

   prev, curr = 0, 1
   for _ in range(2, n + 1):
       prev, curr = curr, prev + curr

   return curr

