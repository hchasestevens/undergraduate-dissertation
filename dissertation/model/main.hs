import Data.List (splitAt)


split_by :: (Num a) => Int -> [a] -> [[a]]
split_by _ [] = []
split_by n xs = grouping : (split_by n rest)
	where
		(grouping, rest) = splitAt n xs


main = do
	print $ split_by 2 $ take 11 [1..]