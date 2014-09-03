import Data.Function (on)
import Data.List (maximumBy)


-- Vector operators
(*|) :: Num a => a -> [a] -> [a]
x *| v = map (* x) v

(|*) :: Num a => [a] -> a -> [a]
(|*) = flip (*|)

(|-|) :: (Num a) => [a] -> [a] -> [a]
(|-|) = zipWith (-)

(|+|) :: (Num a) => [a] -> [a] -> [a]
(|+|) = zipWith (+)


data Position = Position {
	point :: [Float],
	fitness :: Maybe Float
} deriving (Show)

make_position :: [Float] -> Maybe ([Float] -> Float) -> Position
make_position point (Just fitness_func) = Position {point=point, fitness=Just $ fitness_func point}
make_position point _ = Position {point=point, fitness=Nothing}


data ParticleConfig = ParticleConfig {
	max_velocity :: Float,
	max_position :: Float,
	min_position :: Float,
	
	respect_boundaries :: Bool,

	initial_inertia :: Float,
	cognitive_comp :: Float,
	social_comp :: Float,

	inertial_dampening :: Float,
	velocity_dampening :: Float
} deriving (Show)

defaultParticleConfig = ParticleConfig {
	max_velocity=1, 
	max_position=10,
	min_position=(-10),

	respect_boundaries=False,

	-- Values taken from Shi & Eberhart 1998
	initial_inertia=1.2,
	cognitive_comp=2,
	social_comp=2,

	inertial_dampening=1.001,
	velocity_dampening=1
}


data Particle = Particle {
	uuid :: Int,
	
	config :: ParticleConfig,

	position :: Position,
	velocity :: [Float],
	best_position :: Position,

	time :: Int
} deriving (Show)

new_particle :: Int -> ParticleConfig -> Position -> [Float] -> Particle
new_particle id_num conf pos vel = 
	Particle {
		uuid=id_num, 
		config=conf, 
		position=pos, 
		velocity=vel,
		best_position=pos,
		time=0
	}

current_inertia :: Particle -> Float
current_inertia particle = initial_inertia conf / inertial_dampening conf ^ time particle
    where
    	conf = config particle

clip :: (Ord a) => a -> a -> [a] -> [a]
clip min_value max_value = map ((max min_value) . (min max_value))

update :: Position -> ([Float] -> Float) -> Particle -> Float -> Float -> Particle
update best_neighbor_position fitness_func particle cognitive_mod social_mod =
	particle {
		position=new_position,
		velocity=new_velocity,
		best_position=new_best_position,
		time=time particle + 1
	}
	where
		conf = config particle
		v_max = max_velocity conf
		v_min = -v_max
		current_point = point . position $ particle

		-- new velocity:
		inertia = current_inertia particle

		inertial_velocity = inertia *| (velocity particle)
		cognitive_velocity = (point . best_position) particle |-| current_point |* (cognitive_comp conf) |* cognitive_mod
		social_velocity = (point best_neighbor_position) |-| current_point |* (social_comp conf) |* social_mod

		new_velocity = clip v_min v_max $ inertial_velocity |+| cognitive_velocity |+| social_velocity
		
		-- new position:
		new_point = clip (max_position conf) (min_position conf) $ new_velocity |* (velocity_dampening conf) |+| current_point
		new_position = make_position new_point $ Just fitness_func

		-- check for new best position:
		new_best_position = maximumBy (compare `on` fitness) [best_position particle, new_position]


main = do
	print $ 2.0 *| [1..5]
	print $ [1..5] |* 2.0
	print $ [1..5] |+| [1..5]
	print $ [1..5] |-| [1..5]
	return ()