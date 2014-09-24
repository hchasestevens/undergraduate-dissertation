import Data.Function (on)
import Data.List (maximumBy)

import Util (split_by)


-- Vector operators
(|*) :: Num a => [a] -> a -> [a]
vector |* scalar = map (* scalar) vector

(|-|) :: (Num a) => [a] -> [a] -> [a]
(|-|) = zipWith (-)

(|+|) :: (Num a) => [a] -> [a] -> [a]
(|+|) = zipWith (+)


type FitnessFunction = ([Float] -> Float)


data Position = Position {
    point :: [Float],
    fitness :: Maybe Float
} deriving (Show)

make_position :: [Float] -> Maybe FitnessFunction -> Position
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
new_particle id_num cfg pos vel = 
    Particle {
        uuid=id_num, 
        config=cfg, 
        position=pos, 
        velocity=vel,
        best_position=pos,
        time=0
    }

current_inertia :: Particle -> Float
current_inertia particle = initial_inertia cfg / inertial_dampening cfg ^ time particle
    where
        cfg = config particle

clip :: (Ord a) => a -> a -> [a] -> [a]
clip min_value max_value = map ((max min_value) . (min max_value))

update :: Position -> FitnessFunction -> Particle -> Float -> Float -> Particle
update best_neighbor_position fitness_func particle cognitive_mod social_mod =
    particle {
        position=position',
        velocity=velocity',
        best_position=best_position',
        time=time particle + 1
    }
    where
        cfg = config particle
        v_max = max_velocity cfg
        v_min = -v_max
        current_point = point . position $ particle

        -- new velocity:
        inertia = current_inertia particle

        inertial_velocity = velocity particle |* inertia
        cognitive_velocity = (point . best_position) particle |-| current_point |* (cognitive_comp cfg) |* cognitive_mod
        social_velocity = (point best_neighbor_position) |-| current_point |* (social_comp cfg) |* social_mod

        velocity' = clip v_min v_max $ inertial_velocity |+| cognitive_velocity |+| social_velocity
        
        -- new position:
        (p_max, p_min) = if (not . respect_boundaries) cfg 
                            then (max_position cfg, min_position cfg)
                            else (1.0, 0.0)
        point' = clip p_min p_max $ velocity' |* (velocity_dampening cfg) |+| current_point
        fitness_func' = if all (<= p_max) point' && all (>= p_min) point'  -- Technique from Engelbrecht 2005 
                           then Just fitness_func 
                           else Nothing
        position' = make_position point' fitness_func'

        -- check for new best position (n.b. order matters):
        best_position' = maximumBy (compare `on` fitness) [position', best_position particle]


data Swarm = Swarm {
    particle_groups :: [[Particle]],
    best_overall_position :: Maybe Position,
    best_group_positions :: [Maybe Position]
}

new_swarm :: Int -> Int -> [[Float]] -> ParticleConfig -> [Float] -> Swarm
new_swarm group_size no_groups particle_distribution particle_config randoms = 
    Swarm {
        particle_groups = groups,
        best_overall_position = Nothing,
        best_group_positions = map (const Nothing) [1..no_groups]
    }
    where
        no_dimensions = length $ particle_distribution !! 0
        velocities = split_by no_dimensions randoms
        particles = zip3 [1..no_groups * group_size] velocities $ map (flip make_position Nothing) particle_distribution
        groups = split_by group_size [new_particle id_ particle_config pos vel | (id_, vel, pos) <- particles]

step :: Swarm -> FitnessFunction -> [Float] -> Swarm
step swarm fitness_function randoms = undefined




main = do
    print $ [1..5] |* 2.0
    print $ [1..5] |+| [1..5]
    print $ [1..5] |-| [1..5]
    return ()
