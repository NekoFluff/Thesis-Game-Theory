# Using game theory to evaluate effectiveness of blockchain-enabled crowdsourcing approach to fact-checking

# Assumption 1: Fact-checkers want to win the reward by being in the majority

# How to simulate:
# 	1. Every day 10 new topics are generated with differing initial rewards (1 to 30)
# 		a. Sample from normal distribution
# 		b. Difficult depends on position on normal distribution. More difficult along tail ends. Say values from -1 to 1
# 		c. There exist 10 true links (difficult to find, but give higher confidence than false links)
# 		d. There exist 20 false links (easy to find, medium confidence)
# 		e. Total confidence value of true links > false links
# 		f. If the topic is suppose to be FALSE and there are 10 false links and 20 true links
# 		g. -1 is difficult and 1 is difficult. 0 is normal.
# 		h. Place all links along a number line depending on difficulty (time required) to find.  (simulate search results)
# 			i. E.g. [(T, 0.5, 1), (F, 1.5, 2), (T, 3.5, 4), (F, 7.0, 8.0) ….] where each value is a tuple of (statement is true/false (validity V), difficult to find, confidence)
# 			ii. Difficulty to find (min = 1, max = 100)
# 			iii. Probability of finding link is (100-difficulty to find/sqrt(time))/100 … Model how as users spend more time, they have a much higher chance of finding the link. Eventually after spending so much time, it shouldn't really impact the chances of finding the link.
# 		i. Amount of time spent determines the links found by the user. The more time spent = the more links found (generally) since it is only a probability.
# 		j. The user will choose the most convincing link with value C_i and all other found links supporting that same C_i
# 		k. The amount of time spent depends on the topic reward pool.
# 		l. TimeSpent T = X units of time per $1 (depending on user.)
# 		m. Assumption: # of links found depend on the amount of time the user spent.
# 			i. L = number of links with difficulty value less than T and match the validity V of the most convincing argument.
# 		n. The user will construct an argument utilizing those links and the confidence of that argument is the sum of the C_i values.
# 		o. Users use information from previous links


# 	2. 10 random topics are given to the user to choose from every day
# 	3. There are 50 users
# 	4. Each user will rate 1 topic a day
# 	5. The probability of choosing the topic depends on the current reward pool of the topic
# 	6. After choosing a topic a user has not initially created, they will choose an argument with probability X and choose to create an argument with 1-X
# 	7. X is a function that depends on how convincing the existing arguments are
# 		a. Each argument has a probability of being chosen called P
# 		b. An argument consists of links each with some convincing value C_l
# 		c. Sum up C_l for each argument
# 		d. User is convinced after C_l
# 	8. The amount of reputation used when voting is proportional to the amount of confidence in the argument.
# 	9. When creating an argument… Loook at top

# Model assumes that fact-checkers fact-check after one another and not simulateously which may result in slightly different results

requesters = []
fact_checkers = []
topics = []
current_date = 0

# Step 12: Define number of epochs (days) and repeat
total_days = 30

# At the end of an epoch/day remove expired topics


def remove_expired_topics():
    pass

# Step 1: Define topic structure


class Topic:
    initial_value = 0
    start_date = 0
    end_date = 0

    voters = []
    arguments = []

    def __init__(self, initial_value):
        self.initial_value = initial_value

    def distribute_rewards():
        pass
        # Calculate the majority
        # Calculate investment for true side
        # Calculate investment for lie side
        # Get all voters
        # If the voter was in majority hand out reward in proportion
        # Otherwise do calc for minority

    # Step 8: Define evidence creation
    def initialize_available_evidence():
        pass

    def retrieve_evidence(time_spent):
        # User retrieves evidence given time
        pass
# Step 2: Define argument structure


class Argument:
    evidence = []
    total_confidence = 0

    def __init__(self, evidence):
        self.evidence = evidence
        self.total_confidence = sum(evidence)


# Step 3: Define evidence structure


class Evidence:
    # E.g. [(T, 0.5, 1), (F, 1.5, 2), (T, 3.5, 4), (F, 7.0, 8.0) ….] where each value is a tuple of (statement is true/false (validity V), difficult to find, confidence)
    validity = False
    difficulty_to_find = 0
    confidence = 0

    def __init__(self, validity, difficulty_to_find, confidence):
        self.validity = validity
        self.difficulty_to_find = difficulty_to_find
        self.confidence = confidence

# Step 3: Define poster/requester structure


class Requester:
    daily_posts = 10
    # utility:
    # number of arguments
    # number of characters

    def __init__(self, daily_posts):
        self.daily_posts = daily_posts

    # Step 5: Define topic creation
    def post_topic(self):
        print("I posted daily_posts posts")

# Step 4: Define fact-checker/worker structure


class FactChecker:
    dollars = 20
    rep = 100
    daily_fact_checks = 1

    def __init__(self, daily_fact_checks):
        self.daily_fact_checks = daily_fact_checks

    def fact_check(self):
        print("I fact check daily_posts posts")
        # Step 6: Define topic assignment (random)

        # Step 7: Define argument creation
        # (Search for evidence in topic)
        # Choose side (based on most confidence-inducing evidence) and filter evidence
        # Make an argument if there is new information.

        # Step 10: Define voting

    def filter_evidence():
        pass

    def vote():
        pass

    # Step 11: Define claiming (claim at the end of the epoch/day)
    def claim():
        pass


def main():
    print('Hello World!')


if __name__ == "__main__":
    main()
