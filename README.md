## SET SOLVER

The game of set — finding groups of cards that either match or vary in different aspects — is an interesting exercise in combinatorics and, when solving programatically, problem representation. See below!

### DEPENDENCIES
* Solution components require only Python core
* Test suite uses pytest
* See requirements.txt for complete package and version info

### USAGE
* Install dependencies via `pip install -r requirements.txt`
* The `set_solver` module provides both deck generation and game solving
* A deck is a collection of cards to be searched for Sets
* A card is a list of length `dimensions`, where each entry is an integer in the interval [0, feature_size]
* Example: a game with dimensions color, shape, and number, and 4 possible values for each, would be described as: dimensions = 3, feature_size = 4 with cards like [0, 2, 3] or [2, 2, 2]
* The `get_card_collection` method provides a deck of cards for a given game setting
* To find all solution sets in a deck, use the `solution_generator` method
* This generator yields lists of length `match_size` of cards from `deck`
* Each solution satisfies the rules of a game of Set
* To provide validation of the input deck, `solution_generator` requires the game setting parameters (`dimension` and `feature_size`)


### TESTS
* Correctness follows from local correctness of `is_set` method and the checking of every possible combination of cards in deck
* Testing suite can be ran by simply invoking `py.test` in this directory
* Unit/integration testing can be ran separately via (for ex.) `-m unit`
* Unit tests verify input validation and output consistency with alternative combinatoric toolboxes like the `math` and `itertools` packages
* Integration test takes example decks and verifies the results
