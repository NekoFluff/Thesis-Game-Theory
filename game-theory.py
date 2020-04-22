import numpy as np
import math
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
    reward_pool = 0
    start_date = 0
    end_date = 0

    voters = []
    arguments = []
    ether_for_lie = 0
    ether_for_truth = 0
    rep_for_lie = 0
    rep_for_truth = 0
    lie_votes = 0
    true_votes = 0

    # evidence
    all_evidence = []
    max_confidence = [0,0] # [True, False]

    def __init__(self, initial_value, start_date, end_date):
        self.reward_pool = initial_value
        self.start_date = start_date
        self.end_date = end_date
        self.all_evidence = list()
        self.max_confidence = [0,0]
        self.initialize_available_evidence()

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
        # Meaningful fact-checks include information that is corect but difficult to find.
        # Fact-checks easy to verify are not included.
        index = 0
        num_fake_evidence = 20
        num_true_evidence = 10
        for i in range(1, num_true_evidence + 1):
            difficulty = math.pow(i/num_true_evidence, 2)
            value = 1 / difficulty
            e = Evidence(index, True, difficulty, value)
            self.max_confidence[0] += value
            self.all_evidence.append(e)
            index += 1

        for i in range(1, num_fake_evidence + 1):
            difficulty = (i/num_fake_evidence) # Small numbers are hard, but give high reward
            value = 1 / difficulty
            e = Evidence(index, False, difficulty, value)
            self.max_confidence[1] += value
            self.all_evidence.append(e)
            index += 1
        
        print('evidence total:', len(self.all_evidence))

    def retrieve_evidence(self, time_spent):
        # User retrieves evidence given time (higher reward = more effort/time spent)
        import random

        found_evidence = []
        # There are t rounds. In each round each evidence has the opporunity of being found by the user
        for i in range(int(time_spent)):
            for e in self.all_evidence:
                r = random.random()
                # print(i, r, e.difficulty_to_find)
                if e not in found_evidence and r < e.difficulty_to_find:
                    found_evidence.append(e)

        return found_evidence

    def print_details(self):
        print(self.reward_pool, self.start_date, self.end_date)

    def get_utility_for_participation(self, user_ether):
        new_ether_pool = self.reward_pool + user_ether

        # Rational Strategy: Join the side of the majority to win! (votes not visible)
        if self.rep_for_lie > self.rep_for_truth:
            return (user_ether) / (user_ether + self.ether_for_lie) * new_ether_pool
        else:
            return (user_ether) / (user_ether + self.ether_for_truth) * new_ether_pool

    def add_argument(self, argument):
        self.arguments.append(argument)
        print('added argument', argument)

    def vote(self, argument, ether_spent, reputation_spent):
        argument.vote()
        self.reward_pool += ether_spent

        if argument.validity == False:
            self.ether_for_lie += ether_spent
            self.rep_for_lie += reputation_spent
        else:
            self.ether_for_truth += ether_spent
            self.rep_for_truth += reputation_spent

# Step 2: Define argument structure


class Argument:
    validity = False
    evidence = []
    total_confidence = 0
    creator = None
    topic = None
    vote_count = 0

    def __init__(self, creator, evidence, topic):
        self.creator = creator
        self.evidence = evidence
        self.topic = topic # reverse reference
        self.total_confidence = sum([e.confidence_value for e in evidence])
        self.validity = self.evidence[0].validity

    def vote(self):
        self.vote_count += 1

# Step 3: Define evidence structure

class Evidence:
    # E.g. [(T, 0.5, 1), (F, 1.5, 2), (T, 3.5, 4), (F, 7.0, 8.0) ….] where each element is piece of evidence and is represented by a tuple of (statement is true/false (validity V), difficult to find, confidence)
    identification = 0
    validity = False
    difficulty_to_find = 0
    confidence_value = 0

    def __init__(self, identification, validity, difficulty_to_find, confidence_value):
        self.identification = identification
        self.validity = validity
        self.difficulty_to_find = difficulty_to_find
        self.confidence_value = confidence_value


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
    ether = 1 # Each user starts with approximately $200
    rep = 100
    daily_fact_checks = 1
    profile = [1.0, 0]
    num_visible_topics = 10
    rounds_of_effort_per_ether = 1

    def __init__(self, daily_fact_checks, profile):
        self.daily_fact_checks = daily_fact_checks
        self.profile = profile
        self.rep = 100

    def fact_check(self, all_topics, max_topic_ether_value, current_date):
        print("I fact check daily_posts posts")

        # Pick a topic
        chosen_topic, best_value = self.pick_best_topic(all_topics)

        # Retrieve evidence for the topic
        time_spent = best_value * self.rounds_of_effort_per_ether # number of rounds 
        best_evidence, all_evidence = self.search_for_evidence(chosen_topic, time_spent)
        print('found evidence', len(all_evidence))
        print('best', best_evidence)

        matching_evidence = [e for e in all_evidence if e.validity == best_evidence.validity]


        # Compare against existing evidence in other arguments
        

        added_evidence = True if len(chosen_topic.arguments) == 0 else False
        temp_id_list = [e.identification for e in matching_evidence]

        if not added_evidence:
            for arg in chosen_topic.arguments:
                if arg.validity == best_evidence.validity:
                    
                    # Include evidence from other arguments to improve 'convincing' value of argument a (q_a)
                    for arg_evidence in arg.evidence:
                        if arg_evidence.identification not in temp_id_list:
                            added_evidence = True
                            ## EVIDENCE SHOULD WORK!!!!
                            print('new', arg_evidence.identification, arg_evidence.validity, arg_evidence.confidence_value)
                            for x in matching_evidence:
                                print('old', x.identification, x.validity, x.confidence_value)
                            matching_evidence.append(arg_evidence)
                            temp_id_list.append(arg_evidence.identification)

            
        # Make an argument if there is new information.
        if (added_evidence):
            best_argument = Argument(self, matching_evidence, chosen_topic)
            best_argument_confidence = best_argument.total_confidence
            chosen_topic.add_argument(best_argument)

            # Deduct ether in wallet for argument creation transaction
            self.ether -= 0.00089 # Approximate transaction price in ether to create an argument (https://bitinfocharts.com/ethereum/) ... about 15 cents


        # Vote for most convincing argument
        best_argument_confidence = 0
        best_argument = None
        for arg in chosen_topic.arguments:
            # 3 pieces of information affect the user's decision
            reputation_influence = (chosen_topic.rep_for_lie + 1)/(chosen_topic.rep_for_truth+1) if arg.validity == False else (chosen_topic.rep_for_truth + 1)/(chosen_topic.rep_for_lie+1)
            print('rep', arg.creator.rep)
            print('aaaaa', arg.total_confidence , math.sqrt(arg.creator.rep) , reputation_influence)
            convincing_value = arg.total_confidence + reputation_influence + math.sqrt(arg.creator.rep) 
            if convincing_value > best_argument_confidence:
                best_argument = arg
                best_argument_confidence = convincing_value

        # Step 10: Define voting
        # Deduct ether in wallet for vote transaction
        e, r = self.calculate_ether_and_rep_to_spend(chosen_topic, best_argument)
        chosen_topic.vote(best_argument, e, r)
        self.ether -= e # Ether spent to add to reward pool
        self.rep -= r # Reputation spent to influence other players (fact-checkers)
        self.ether -= 0.00089 # Approximate transaction price in ether to create an argument (https://bitinfocharts.com/ethereum/) ... about 15 cents

    def pick_best_topic(self, all_topics):
        # Step 6: Define topic assignment (random)
        visible_topics = np.random.choice(all_topics, size=self.num_visible_topics, replace=True)

        # Step 6.5: Choose topic that maximizes reward for participation
        best_value = 0
        chosen_topic = None
        for topic in visible_topics:
            utility = topic.get_utility_for_participation(user_ether=self.ether)
            if utility > best_value:
                best_value = utility
                chosen_topic = topic

        return chosen_topic, best_value

    def search_for_evidence(self, topic, time_spent):
        # (Search for evidence in topic)
        evidence = topic.retrieve_evidence(time_spent=time_spent)
        # Choose side (based on most confidence-inducing evidence) and filter evidence
        e_conf = 0
        best_e = None
        for e in evidence:
            if e.confidence_value > e_conf:
                best_e = e
                e_conf = e.confidence_value

        return (best_e, evidence)

    def pick_strategy(self):
        # Strategies
        # Each player i has two possible actions: play honestly or play maliciously. 
        # If the player i plays honestly; it follows the protocol and attempts to maximize its own ether reward by creating convincing arguments.
        # If the player i acts malicously; it knowingly uses false information to construct its argument
        # s_i = honest, malicous
        pass



    # Simple mechanism where the more confident a user is in an argument, the more ether and reputation they are willing to spend when voting
    def calculate_ether_and_rep_to_spend(self, topic, argument):
        confidence_ratio = 0
        if argument.validity == False:
            confidence_ratio = argument.total_confidence / topic.max_confidence[1]
        else:
            confidence_ratio = argument.total_confidence / topic.max_confidence[0]
        
        print('reputation', self.rep, confidence_ratio * self.rep)
        if (confidence_ratio > 1.05):
            for x in argument.evidence:
                print('zzz', x.identification)
            print('ERROR')
            exit(1)
        confidence_ratio = min(confidence_ratio, 1)
        return (confidence_ratio * self.ether, confidence_ratio * self.rep)

    # Step 11: Define claiming (claim at the end of the epoch/day)
    def claim(self):
        pass


# Normal Form Game:
# To study the security of our incentive mechanism, we employ a static game to analyze the behaviors of the fact-checkers under different strategies. 
# The model of the fact-checking game is described as follows

# a. Players
# This game has N players, the number of fact-checkers F = (F1,F2, F3, ... FN)

# b. Strategies
# Each player i has two possible actions: play honestly or play maliciously. 
# If the player i plays honestly; it follows the protocol and attempts to maximize its own ether reward by creating convincing arguments.
# If the player i acts malicously; it knowingly uses false information to construct its argument but only if its argument is reasonably convincing compared to all other arguments and the odds aren't already stacked against him.
# s_i = honest, malicous

# c. Utilities
# The player i can get its utility by deducting its cost c_i from its received payment. 
# The recieved payment is equivalent to the amount invested E_i / total invested * reward pool R
# The cost c_i is comprised of the transaction cost to create the argument, and the cost transaction cost to vote
# 0 if i is not in the majority 
# (applies to all strategies) s_i = honest, malicous

# A Graph depicting the results would contain:
# X-Axis: Ratio of truth to lie
# Y-Axis: Time
# Z-Axis: Total Ether 

# Starting assumptions:
# 50 players (fact-checkers) total
# Each player is assigned some distribution of acting honestly vs maliciously
# If x is the probability of acting honestly 1-x is the probability of acting malicously
# For testing purposes, I uniformly vary the probabilities of acting honestly/malicously among all players
# For example in a game with 50 players, player 1 has a 100% chance of acting hoenstly, player 2 has a 98% chance, player 3 has a 96% chance, etc. 

# More staring assumptions:
# Each fact-checker fact-checks once a day
# There is 1 requester posting 10 topics a day (can be extended)
# Each topic lasts 3 days
# Each topic has a initial value of between 0 and 10 ether

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
    num_fact_checkers = 10
    num_fact_checks_daily = 1
    fact_checkers = []

    # Topics
    all_topics = [] # both expired and active topics
    topics = [] # only active topics
    topics_generated_per_day = 10  # 10 topics generated a day
    topic_duration = 3  # 3 days
    max_topic_ether_value = 6 # Constrained to 6 ether or $1000

    # Step 12: Define number of epochs (days) and repeat
    total_days = 365 # What would occur in a year?
    current_date = 0  # simulation starts at day 0

    def __init__(self):
        super().__init__()
        self.generate_requesters()
        self.generate_fact_checkers()

    def run_simulation(self):
        for i in range(self.total_days):
            self.current_date = i

            # Generate topics
            self.generate_new_topics()

            # Create arguments and vote
            for fc in self.fact_checkers:
                # 1) View arguments, 2) View evidence, and 3) Make new argument or fact-check
                fc.fact_check(self.topics, self.max_topic_ether_value, self.current_date)

            # Remove expired topics and claim rewards (reward is distributed to all voters)
            self.remove_expired_topics()

            # Repeat for # of total_days

    def random_topic_value(self):
        import random
        return random.random() * self.max_topic_ether_value

    def remove_expired_topics(self):
        new_topics = []
        for topic in self.topics:
            if topic.is_expired(self.current_date):
                topic.distribute_rewards()
            else:
                new_topics.append(topic)
        self.topics = new_topics

    def generate_new_topics(self):
        for i in range(self.topics_generated_per_day):
            t = Topic(self.random_topic_value(), self.current_date,
                      self.current_date + self.topic_duration)
            self.topics.append(t)
            self.all_topics.append(t)

        # for i in self.topics:
        #     print('reward', i.reward_pool)
        #     print('len', i.all_evidence[0].difficulty_to_find)

    def generate_requesters(self):
        for i in range(self.num_requesters):
            r = Requester(self.topics_generated_per_day)
            self.requesters.append(r)

    def generate_fact_checkers(self):
        for i in range(self.num_fact_checkers):
            honest_prob = 1 - (1/(self.num_fact_checkers - 1)) * i
            malicious_prob = 1 - honest_prob
            fc = FactChecker(self.num_fact_checks_daily, [honest_prob, malicious_prob])
            self.fact_checkers.append(fc)

    def print_topics(self):
        for topic in self.topics:
            topic.print_details()


def main():
    s = Simulator()
    s.run_simulation()




    # print('Hello World!')
    # s.generate_new_topics()
    # print(len(s.topics))
    # s.print_topics()
    # s.current_date = 3
    # s.remove_expired_topics()
    # print(len(s.topics))


if __name__ == "__main__":
    main()
