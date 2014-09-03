import Data.List


single_comm_success :: Float -> Float -> Float -> Float -> Float -> Float -> Float
single_comm_success ambiguous_reference_cost success_points partner_sum cost player_prob partner_prob
	| partner_prob > 0.0 = ambiguous_cost + ambiguous_reward + unambiguous_points
	| otherwise = ambiguous_cost + unambiguous_points
	where
		ambiguous_cost = ambiguous_reference_cost * player_prob
		ambiguous_reward = success_points * player_prob * (partner_prob / partner_sum)
		unambiguous_points = ((cost + success_points) * (1.0 - player_prob))

comm_success :: [Float] -> Float -> Float -> [Float] -> [Float] -> Float
comm_success costs ambiguous_reference_cost success_points player partner =
	sum $ zipWith3 item_comm_success costs player partner
	where
		partner_sum = sum partner
		item_comm_success = single_comm_success ambiguous_reference_cost success_points partner_sum

game :: ([Float] -> [Float] -> Float) -> [Float] -> [[Float]] -> Float -- Maybe have this take particles, have position implement eq?
game comm_func player [] = 0.0
game comm_func player group = sum $ map (pair_success player) $ delete player group
    where
    	pair_success player partner = comm_func player partner + comm_func partner player

main = do
	putStrLn $ show $ comm_success [0] 0 1 [1] [1]
	putStrLn $ show $ comm_success [0] 0 1 [1] [0]
	putStrLn $ show $ comm_success [0] 0 1 [1] [0.5]
	putStrLn $ show $ comm_success [0] 0 1 [1] [1]
	putStrLn $ show $ comm_success [0] 0 1 [0] [1]
	putStrLn $ show $ comm_success [0] 0 1 [0.5] [1]
	return $ (game $ comm_success [0] 0 1) [1] [[0.99], [0], [0.5]]