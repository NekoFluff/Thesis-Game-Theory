# Using game theory to evaluate effectiveness of blockchain-enabled crowdsourcing approach to fact-checking

# Assumption 1: Fact-checkers want to win the reward by being in the majority

# How to simulate:
# 	1. Every day 10 new topics are generated with differing initial rewards (1 to 10)
# 		a. Sample from normal distribution
# 		b. Difficulty of finding true answer to topic depends on position on normal distribution. More difficult along tail ends. Say values from -1 to 1
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
# 	9. When creating an argument… Look at top

# Model assumes that fact-checkers fact-check after one another and not simulateously which may result in slightly different results

# Step 1: Define topic structure


class Topic:
    initial_value = 0
    start_date = 0
    end_date = 0

    voters = []
    arguments = []

    def __init__(self, initial_value, start_date, end_date):
        self.initial_value = initial_value
        self.start_date = start_date
        self.end_date = end_date

    def is_expired(self, date):
        return date >= self.end_date

    def distribute_rewards(self):
        pass
        # Calculate the majority
        # Calculate investment for true side
        # Calculate investment for lie side
        # Get all voters
        # If the voter was in majority hand out reward in proportion
        # Otherwise do calc for minority

    # Step 8: Define evidence creation
    def initialize_available_evidence(self):
        pass

    def retrieve_evidence(time_spent):
        # User retrieves evidence given time
        pass

    def print_details(self):
        print(self.initial_value, self.start_date, self.end_date)

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
    is_malicious = False

    def __init__(self, daily_fact_checks, is_malicious):
        self.daily_fact_checks = daily_fact_checks
        self.is_malicious = is_malicious

    def fact_check(self):
        print("I fact check daily_posts posts")
        # Step 6: Define topic assignment (random)

        # Step 7: Define argument creation
        # (Search for evidence in topic)
        # Choose side (based on most confidence-inducing evidence) and filter evidence
        # Make an argument if there is new information.

        # Step 10: Define voting

    def filter_evidence(self):
        pass

    def vote(self):
        pass

    # Step 11: Define claiming (claim at the end of the epoch/day)
    def claim(self):
        pass


# Starting assumptions:
# 20% fact-checkers are malicious (50 total)
# each fact-checker fact-checks once a day
# 1 requester posting 10 topics a day
# each topic lasts 3 days
# each topic has a initial value of between 0 and 10 ether


# Assumptions about fact-checker actions:
# Malicious fact-checkers:
# Knows true output of topic and act to support false information by *knowingly* making arguments and voting for the opposite of the true output
# Non-malicous fact-checkers:
# Acts to maximize ether reward by creating arguments that are the most convincing (measured by evidence used and character count of argument)

# Calculating Confidence:
# confidence = alpha * sum(evidence_convincing_value) + beta * character_count
# character_count = (10 * evidence_count)

# Assumptions about evidence:
# A tuple consisting of (statement is true/false (validity V), difficult to find, confidence)
# e.g. (T, 0.5, 1)
# We are going to assume that true information is MUCH more difficult to find than false information but is more convincing
# There exist 10 true links (difficult to find, but give higher confidence than false links)
# There exist 20 false links (easy to find, medium confidence)
# Total confidence value of true links > false links

# Assumptions about Topics:
#       b. Difficulty of finding true answer to topic depends on position on normal distribution. More difficult along tail ends. Say values from -1 to 1

# 		f. If the topic is suppose to be FALSE and there are 10 false links and 20 true links
# 		g. -1 is difficult and 1 is difficult. 0 is normal.
# 		h. Place all links along a number line depending on difficulty (time required) to find.  (simulate search results)
# 			i. E.g. [(T, 0.5, 1), (F, 1.5, 2), (T, 3.5, 4), (F, 7.0, 8.0) ….] where each value is a tuple of
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

# Assumptions about character count:
# Loose correlation between character count and convincing.
# A paragraph of analysis is more convincing than a sentence of analysis
# But it tapers off at a certain point
# impact on convincing argument is measured by log(character count)

# Assumptions about requester actions:
# Want to maximize the quality of arguments or how convincing they are (measured by evidence and character count of argument)
# Limited to posting between 0 and 10 ether

class Simulator():
    # Requesters
    num_requesters = 1
    requesters = []

    # Fact Checkers
    num_malicious_fact_checkers = 40
    num_non_malicious_fact_checkers = 10  # 20 % are malicious
    num_fact_checks_daily = 1
    fact_checkers = []

    # Topics
    all_topics = []
    topics = []
    topics_generated_per_day = 10  # 10 topics generated a day
    topic_duration = 3  # 3 days

    # Step 12: Define number of epochs (days) and repeat
    total_days = 30
    current_date = 0  # simulation starts at day 0

    def __init__(self):
        super().__init__()
        self.generate_requesters()
        self.generate_fact_checkers()

    def run_simulation(self):
        for i in range(self.total_days):
            # Generate topics
            self.generate_topics()

            # Create arguments and vote
            for fc in self.fact_checkers():
                # 1) View arguments, 2) View evidence, and 3) Make new argument or fact-check
                fc.fact_check()

            # Remove expired topics and claim rewards (reward is distributed to all voters)
            self.remove_expired_topics()

            # Repeat for # of total_days

    def random_topic_value(self):
        import random
        return random.random() * 10

    def remove_expired_topics(self):
        new_topics = []
        for topic in self.topics:
            if topic.is_expired(self.current_date):
                topic.distribute_rewards()
            else:
                new_topics.append(topic)
        self.topics = new_topics

    def generate_topics(self):
        for i in range(self.topics_generated_per_day):
            t = Topic(self.random_topic_value(), self.current_date,
                      self.current_date + self.topic_duration)
            self.topics.append(t)
            self.all_topics.append(t)

    def generate_requesters(self):
        for i in range(self.num_requesters):
            r = Requester(self.topics_generated_per_day)
            self.requesters.append(r)

    def generate_fact_checkers(self):
        for i in range(self.num_malicious_fact_checkers):
            fc = FactChecker(self.num_fact_checks_daily, True)
            self.fact_checkers.append(fc)

        for i in range(self.num_non_malicious_fact_checkers):
            fc = FactChecker(self.num_fact_checks_daily, False)
            self.fact_checkers.append(fc)

    def print_topics(self):
        for topic in self.topics:
            topic.print_details()


def main():
    s = Simulator()
    # s.run_simulation()
    print('Hello World!')
    s.generate_topics()
    print(len(s.topics))
    s.print_topics()
    s.current_date = 3
    s.remove_expired_topics()

    print(len(s.topics))


if __name__ == "__main__":
    main()
