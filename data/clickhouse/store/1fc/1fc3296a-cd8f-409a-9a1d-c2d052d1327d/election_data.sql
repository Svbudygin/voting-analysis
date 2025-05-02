ATTACH TABLE _ UUID 'a59c6d48-83aa-4bcf-96dc-d90daceb45ac'
(
    `uik` String,
    `num_of_registered_voters_x` UInt32,
    `num_of_ballots_given_away_on_voting_day_indoors_x` UInt32,
    `num_of_ballots_given_away_on_voting_day_at_home_x` UInt32,
    `num_of_valid_ballots_x` UInt32,
    `putin_votes_x` UInt32,
    `coords_x` String,
    `num_of_registered_voters_y` UInt32,
    `num_of_ballots_given_away_on_voting_day_indoors_y` UInt32,
    `num_of_ballots_given_away_on_voting_day_at_home_y` UInt32,
    `num_of_valid_ballots_y` UInt32,
    `putin_votes_y` UInt32,
    `turnout_2012` Float32,
    `support_2012` Float32,
    `turnout_2018` Float32,
    `support_2018` Float32,
    `metro_build` UInt32,
    `kont_1` UInt32,
    `kont_2` UInt32,
    `lat` Float64,
    `lon` Float64
)
ENGINE = MergeTree
ORDER BY uik
SETTINGS index_granularity = 8192
