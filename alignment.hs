import qualified Data.Text as T
import Data.Maybe

-- Test sequences
t1 :: String
t2 :: String
t1 = "GAATC"
t2 = "CATAC"

-- Used to map sequence elements to their coordinate in the substitution matrix
b2i :: Char -> Int
b2i b = fromJust $ lookup b [('A', 0),  ('C', 1), ('G' , 2), ('T', 3)]

-- Substitution matrix
sub :: [[Int]]
--      A    C  G   T
sub = [[10, -5, 0, -5], -- A
       [-5, 10, -5, 0], -- C
       [0, -5, 10, -5], -- G
       [-5, 0, -5, 10]] -- T

-- Gap penalty
d :: Int
d = -4

-- Implement recursion cases
v :: Int -> Int -> T.Text -> T.Text -> Int
v 0 0 _ _ = 0
v i 0 s1 s2 = v (i - 1) 0 s1 s2 + d
v 0 j s1 s2 = v 0 (j - 1) s1 s2 + d
v i j s1 s2 = maximum [v (i - 1) (j - 1) s1 s2 + sub !! b2i (s1 `T.index` i) !! b2i (s2 `T.index` j),
                       v (i - 1) j s1 s2 + d,
                       v (j - 1) i s1 s2 + d]

-- Since sequences are indexed from 1 ... and strings are indexed from 0
-- ... spaces are added to realign the sequence indexes with the string
-- indices.
findMaxV :: String -> String -> Int
findMaxV s1 s2 = v (length s1) (length s2) s1' s2'
  where s1' = T.pack $ " " ++ s1
        s2' = T.pack $ " " ++ s2

main :: IO ()
main = print (findMaxV t1 t2)
