import numpy as np
import math
import matplotlib.pyplot as plt
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

important_votes = []
all_times = []


class Topic:
    reward_pool = 0
    start_date = 0
    end_date = 0

    voters = {}
    arguments = []
    ether_for_lie = 0
    ether_for_truth = 0
    rep_for_lie = 0
    rep_for_truth = 0
    lie_votes = 0
    true_votes = 0
    initial_reward = 0

    # evidence
    all_evidence = []
    max_confidence = [0, 0]  # [True, False]

    def __init__(self, initial_value, start_date, end_date, identifier):
        self.reward_pool = initial_value
        self.initial_reward = initial_value

        self.start_date = start_date
        self.end_date = end_date
        self.all_evidence = list()
        self.max_confidence = [0, 0]
        self.voters = {}
        self.initialize_available_evidence()
        self.identifier = identifier
        self.arguments = []

    def is_expired(self, date):
        return date >= self.end_date

    def distribute_rewards(self):
        final_reward_pool = self.reward_pool

        # No one participated
        if (self.lie_votes + self.true_votes == 0):
            # print("no participants")
            return

        total_num_winners = 0
        total_investment = 0
        investments = []
        total_eth = self.ether_for_lie if self.lie_votes > self.true_votes else self.ether_for_truth

        for key, value in self.voters.items():
            # print('self.voters', key, value)
            user, arg, eth, rep = value
            # print('arg validity', arg.validity,
            #   self.true_votes, self.lie_votes)

            if (arg.validity == True and self.true_votes > self.lie_votes) or (arg.validity == False and self.lie_votes > self.true_votes):
                # print('user id', user.identification,
                #       'rep', user.rep, 'eth', user.ether)
                user.ether += self.calculate_eth_reward(
                    eth, total_eth, final_reward_pool)
                user.rep += 1.1 * rep
                user.rep = min(user.rep, 1000)
                # print('user', user.identification, user.rep, user.ether)
                total_num_winners += 1
                total_investment += eth
                investments.append(eth)
            else:
                user.rep += 0.8 * rep

        # print('Make sure distribution == one', total_num_winners,
        #       investments, total_investment, total_eth)
        # print('Distribution == 1?', total_investment/total_eth)

    # Function to calculate rewards given the amount of ether a user spent
    def calculate_eth_reward(self, spent_eth, total_eth, reward_pool):
        # print('spent', spent_eth, 'total',
        #       total_eth, 'reward pool', reward_pool)
        return spent_eth / total_eth * reward_pool

    # Step 8: Define evidence creation
    def initialize_available_evidence(self):
        # Meaningful fact-checks include information that is corect but difficult to find.
        # Fact-checks easy to verify are not included.
        index = 0
        num_fake_evidence = 20
        num_true_evidence = 20
        for i in range(1, num_true_evidence + 1):
            difficulty = math.pow(i/num_true_evidence, 2)
            # difficulty = i/num_true_evidence
            value = 1 - math.log(difficulty)  # + 0.01
            e = Evidence(index, True, difficulty, value)
            self.max_confidence[0] += value
            self.all_evidence.append(e)
            index += 1

        for i in range(1, num_fake_evidence + 1):
            # Small numbers are hard, but give high reward
            difficulty = (i/num_fake_evidence)
            value = 1 - math.log(difficulty)
            e = Evidence(index, False, difficulty, value)
            self.max_confidence[1] += value
            self.all_evidence.append(e)
            index += 1
        # print('max_confidence', self.max_confidence)
        # print('evidence total:', len(self.all_evidence))

    def retrieve_evidence(self, time_spent):
        # User retrieves evidence given time (higher reward = more effort/time spent)
        import random

        found_evidence = []
        # There are t rounds. In each round each evidence has the opporunity of being found by the user
        global all_times
        all_times.append(time_spent + 1)

        for i in range(int(time_spent + 1)):
            for e in self.all_evidence:
                r = random.random()
                # print(i, r, e.difficulty_to_find)
                if e not in found_evidence and r < e.difficulty_to_find:
                    # print('evidence', e.identification, r)
                    found_evidence.append(e)

        return found_evidence

    def print_details(self):
        print(self.reward_pool, self.start_date, self.end_date)

    def get_utility_for_participation(self, user_ether):
        # No ether used, no reward
        if user_ether == 0:
            return 0

        new_ether_pool = self.reward_pool + user_ether
        # print('pool', new_ether_pool, user_ether, self.ether_for_lie, self.ether_for_truth)
        # Rational Strategy: Join the side of the majority to win! (votes not visible)
        if self.rep_for_lie > self.rep_for_truth:
            return (user_ether) / (user_ether + self.ether_for_lie) * new_ether_pool
        else:
            return (user_ether) / (user_ether + self.ether_for_truth) * new_ether_pool

    def add_argument(self, argument):
        self.arguments.append(argument)
        # print('added argument', argument)

    def vote(self, user, argument, ether_spent, reputation_spent, current_date):
        if user.identification in self.voters:
            print("ERROR: Already voted")
            exit(1)

        argument.vote()
        self.reward_pool += ether_spent
        # print('user vote', user.identification, argument.validity, ether_spent, reputation_spent)
        if argument.validity == False:
            self.lie_votes += 1
            self.ether_for_lie += ether_spent
            self.rep_for_lie += reputation_spent
        else:
            self.true_votes += 1
            self.ether_for_truth += ether_spent
            self.rep_for_truth += reputation_spent

        self.voters[user.identification] = [
            user, argument, ether_spent, reputation_spent]
        # print('items after vote', self.voters.items(), current_date)
        if user.identification == 99:
            global important_votes
            important_votes.append(
                (user.identification, current_date, argument.validity, ether_spent, reputation_spent))
        # if (current_date > 10):
            # exit(1)
        # if user.identification == 99 and current_date > 25:
            # exit(1)

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
        self.topic = topic  # reverse reference
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
        # print("I posted daily_posts posts")
        pass

# Step 4: Define fact-checker/worker structure


class FactChecker:
    ether = 1  # Each user starts with approximately $200
    rep = 100
    daily_fact_checks = 1
    profile = [1.0, 0]
    num_visible_topics = 10
    rounds_of_effort_per_ether = 25  # 8 dollars per round (minimum wage)
    identification = 0
    history = []

    def __init__(self, identification, daily_fact_checks, profile):
        self.identification = identification
        self.daily_fact_checks = daily_fact_checks
        self.profile = profile
        self.rep = 100
        self.history = []
        self.voted_topics = []

    def fact_check(self, all_topics, max_topic_ether_value, current_date):
        # You cannot participate unless you have enough ether
        if self.ether == 0:
            return

        # print("I fact check daily_posts posts")

        # Pick a topic
        chosen_topic, best_value = self.pick_best_topic(all_topics)
        if chosen_topic == None:  # None of the topics are able to be voted on.
            return

        # Retrieve evidence for the topic
        time_spent = best_value * self.rounds_of_effort_per_ether  # number of rounds
        best_evidence, all_evidence = self.search_for_evidence(
            chosen_topic, time_spent)
        # print('found evidence', len(all_evidence))
        # print('best', best_evidence)

        if (len(all_evidence) == 0):
            return

        self.pick_strategy(all_evidence, best_evidence,
                           chosen_topic, current_date)

    def pick_best_topic(self, all_topics):
        # Step 6: Define topic assignment (random)
        visible_topics = np.random.choice(
            all_topics, size=self.num_visible_topics, replace=True)

        # Step 6.5: Choose topic that maximizes reward for participation
        best_value = 0
        chosen_topic = None
        for topic in visible_topics:
            # The fact-checker has already fact-checked this topic
            if self.identification in topic.voters:
                # print('already fact-checked')
                continue

            utility = topic.get_utility_for_participation(
                user_ether=self.ether)
            if utility < 0:
                print("ERROR: Negative Utility")
                exit(1)
            if utility > best_value:
                best_value = utility
                chosen_topic = topic

        # print('chosen topic', best_value, chosen_topic)
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

    def pick_strategy(self, all_evidence, best_evidence, chosen_topic, current_date):
        # Strategies
        # Each player i has two possible actions: play honestly or play maliciously.
        # If the player i plays honestly; it follows the protocol and attempts to maximize its own ether reward by creating convincing arguments.
        # If the player i acts malicously; it knowingly uses false information to construct its argument
        # s_i = honest, malicous
        import random
        r = random.random()

        if r <= self.profile[0]:
            self.act_honestly(all_evidence, best_evidence,
                              chosen_topic, current_date)
        else:
            self.act_maliciously(all_evidence, best_evidence,
                                 chosen_topic, current_date)

    def act_honestly(self, all_evidence, best_evidence, chosen_topic, current_date):
        matching_evidence = [
            e for e in all_evidence if e.validity == best_evidence.validity]

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
                            matching_evidence.append(arg_evidence)
                            temp_id_list.append(arg_evidence.identification)

        # Make an argument if there is new information.
        if (added_evidence) and self.ether >= 0.00089:
            best_argument = Argument(self, matching_evidence, chosen_topic)
            best_argument_confidence = best_argument.total_confidence
            chosen_topic.add_argument(best_argument)

            # Deduct ether in wallet for argument creation transaction
            # Approximate transaction price in ether to create an argument (https://bitinfocharts.com/ethereum/) ... about 15 cents
            self.spend_ether(0.0089)

        # Vote for most convincing argument
        best_argument_confidence = 0
        best_argument = None
        for arg in chosen_topic.arguments:
            # 3 pieces of information affect the user's decision
            reputation_influence = chosen_topic.rep_for_lie / \
                100 if arg.validity == False else chosen_topic.rep_for_truth/100
            convincing_value = arg.total_confidence + \
                reputation_influence + math.sqrt(arg.creator.rep)
            if convincing_value > best_argument_confidence:
                best_argument = arg
                best_argument_confidence = convincing_value

        if best_argument is None:
            return

        # Step 10: Define voting
        # Deduct ether in wallet for vote transaction
        # Approximate transaction price in ether to create an argument (https://bitinfocharts.com/ethereum/) ... about 15 cents
        self.spend_ether(0.0089)
        e, r = self.calculate_ether_and_rep_to_spend(
            chosen_topic, best_argument)
        if (e > 0.05):
            chosen_topic.vote(self, best_argument, e, r, current_date)
            self.ether -= e  # Ether spent to add to reward pool
            # Reputation spent to influence other players (fact-checkers)
            self.rep -= r
            self.voted_topics.append(chosen_topic)

    def act_maliciously(self, all_evidence, best_evidence, chosen_topic, current_date):
        matching_evidence = [e for e in all_evidence if e.validity == False]
        # Compare against existing evidence in other arguments
        added_evidence = True if len(
            [a for a in chosen_topic.arguments if a.validity == False]) == 0 else False
        temp_id_list = [e.identification for e in matching_evidence]

        if len(matching_evidence) > 0:
            if not added_evidence:
                for arg in chosen_topic.arguments:
                    if arg.validity == False:

                        # Include evidence from other arguments to improve 'convincing' value of argument a (q_a)
                        for arg_evidence in arg.evidence:
                            if arg_evidence.identification not in temp_id_list:
                                added_evidence = True
                                matching_evidence.append(arg_evidence)
                                temp_id_list.append(
                                    arg_evidence.identification)

            # Make an argument if there is new information.
            if (added_evidence) and self.ether >= 0.00089:
                best_argument = Argument(self, matching_evidence, chosen_topic)
                best_argument_confidence = best_argument.total_confidence
                chosen_topic.add_argument(best_argument)

                # Deduct ether in wallet for argument creation transaction
                # Approximate transaction price in ether to create an argument (https://bitinfocharts.com/ethereum/) ... about 15 cents
                self.spend_ether(0.0089)

        # Vote for most convincing argument
        # if len(chosen_topic.arguments) == 0:
        #     return

        best_argument_confidence = 0
        best_argument = None
        for arg in chosen_topic.arguments:
            # Skip all arguments that actually reveal the truth about the topic
            if arg.validity == True:
                continue
            # 3 pieces of information affect the user's decision
            reputation_influence = chosen_topic.rep_for_lie / \
                100 if arg.validity == False else chosen_topic.rep_for_truth/100
            convincing_value = arg.total_confidence + \
                reputation_influence + math.sqrt(arg.creator.rep)
            if convincing_value > best_argument_confidence:
                best_argument = arg
                best_argument_confidence = convincing_value

        if best_argument is None:
            return

        # Step 10: Define voting
        # Deduct ether in wallet for vote transaction
        # Approximate transaction price in ether to create an argument (https://bitinfocharts.com/ethereum/) ... about 15 cents
        self.spend_ether(0.0089)
        e, r = self.calculate_ether_and_rep_to_spend(
            chosen_topic, best_argument)
        if (e > 0.05):
            chosen_topic.vote(self, best_argument, 0.05, r, current_date)
            self.ether -= 0.05  # Ether spent to add to reward pool
            # Reputation spent to influence other players (fact-checkers)
            self.rep -= r
            self.voted_topics.append(chosen_topic)

    def spend_ether(self, eth):
        self.ether -= eth
        self.ether = max(self.ether, 0)

    # Simple mechanism where the more confident a user is in an argument, the more ether and reputation they are willing to spend when voting
    def calculate_ether_and_rep_to_spend(self, topic, argument):
        confidence_ratio = 0
        if argument.validity == False:
            confidence_ratio = argument.total_confidence / \
                topic.max_confidence[1]
        else:
            confidence_ratio = argument.total_confidence / \
                topic.max_confidence[0]

        # print('reputation', argument.validity, argument.total_confidence, self.rep, confidence_ratio, confidence_ratio * self.rep)

        # Rounding errors cause it to go over 1. Players are conservative and only want to put at most half of current at risk
        confidence_ratio = min(confidence_ratio, 1) / 2

        return (min(confidence_ratio * self.ether, 1), confidence_ratio * self.rep)

    # Store data
    def save(self, current_day):
        additional_ether = 0
        additonal_rep = 0
        new_topics = []

        for t in self.voted_topics:
            if t.is_expired(current_day - 1):
                continue
            new_topics.append(t)
            # [user, argument, ether, rep]
            additional_ether += t.voters[self.identification][2]
            # [user, argument, ether, rep]
            additonal_rep += t.voters[self.identification][3]

        self.voted_topics = new_topics
        self.history.append(
            [self.identification, current_day, self.ether + additional_ether, min(self.rep + additonal_rep, 1000), self.profile])


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
    num_fact_checkers = 20
    num_fact_checks_daily = 1
    fact_checkers = []

    # Topics
    all_topics = []  # both expired and active topics
    topics = []  # only active topics
    topics_generated_per_day = 10  # 10 topics generated a day
    topic_duration = 5  # 5 days
    max_topic_ether_value = 1  # Constrained to 1 ether or $200

    # Step 12: Define number of epochs (days) and repeat
    total_days = 200  # What would occur in a year?
    current_date = 0  # simulation starts at day 0

    def __init__(self):
        super().__init__()
        self.generate_requesters()
        self.generate_fact_checkers()
        self.topic_index = 0

    def run_simulation(self):
        # Record status of each person
        for fc in self.fact_checkers:
            fc.save(self.current_date)

        for i in range(self.total_days):
            self.current_date = i

            # Shuffle fact_checkers
            np.random.shuffle(self.fact_checkers)

            if (self.total_days - i > self.topic_duration):
                # Generate topics
                self.generate_new_topics()

                # Create arguments and vote
                for fc in self.fact_checkers:
                    # Stop fact-checking when there are 3 days remaining only
                    if (self.total_days - i <= self.topic_duration):
                        break

                    # 1) View arguments, 2) View evidence, and 3) Make new argument or fact-check
                    fc.fact_check(
                        self.topics, self.max_topic_ether_value, self.current_date)

            # Remove expired topics and claim rewards (reward is distributed to all voters)
            self.remove_expired_topics()

            # Record status of each person
            for fc in self.fact_checkers:
                fc.save(self.current_date + 1)

            # Repeat for # of total_days

    def retrieve_results(self):
        all_fact_checker_data = {}
        for fc in self.fact_checkers:
            # all_fact_checker_data[fc.profile[0]] = fc.history
            all_fact_checker_data[fc.identification] = fc.history

        true_topics = 0
        lie_topics = 0
        equal_topics = 0
        not_voted_topics = 0
        for topic in self.all_topics:

            if topic.true_votes == 0 and topic.lie_votes == 0:
                not_voted_topics += 1
            elif topic.true_votes > topic.lie_votes:
                true_topics += 1
            elif topic.lie_votes > topic.true_votes:
                lie_topics += 1
            else:
                equal_topics += 1

        return all_fact_checker_data, (true_topics, lie_topics, equal_topics, not_voted_topics)

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
                      self.current_date + self.topic_duration, self.topic_index)
            self.topics.append(t)
            self.all_topics.append(t)
            self.topic_index += 1

        # for i in self.topics:
        #     print('reward', i.reward_pool)
        #     print('len', i.all_evidence[0].difficulty_to_find)

    def generate_requesters(self):
        for i in range(self.num_requesters):
            r = Requester(self.topics_generated_per_day)
            self.requesters.append(r)

    def generate_fact_checkers(self):
        # at least 80% are non-malicious
        num_honest = int(self.num_fact_checkers * 0.8)
        num_partial = int(self.num_fact_checkers * 0.1)
        num_malicious = int(self.num_fact_checkers * 0.1)
        index = 0

        # for i in range(self.num_fact_checkers):
        #     honest_prob = 1 - (1/(self.num_fact_checkers - 1)) * i
        #     malicious_prob = 1 - honest_prob
        #     fc = FactChecker(index, self.num_fact_checks_daily, [honest_prob, malicious_prob])
        #     self.fact_checkers.append(fc)
        #     index += 1

        for i in range(num_honest):
            honest_prob = 1  # 1 - (1/(self.num_fact_checkers - 1)) * i
            malicious_prob = 0  # 1 - honest_prob
            fc = FactChecker(index, self.num_fact_checks_daily, [
                             honest_prob, malicious_prob])
            self.fact_checkers.append(fc)
            index += 1

        for i in range(num_partial):
            honest_prob = 0.5
            malicious_prob = 0.5
            fc = FactChecker(index, self.num_fact_checks_daily, [
                             honest_prob, malicious_prob])
            self.fact_checkers.append(fc)
            index += 1

        for i in range(num_malicious):
            honest_prob = 0
            malicious_prob = 1
            fc = FactChecker(index, self.num_fact_checks_daily, [
                             honest_prob, malicious_prob])
            self.fact_checkers.append(fc)
            index += 1

    def print_topics(self):
        for topic in self.topics:
            topic.print_details()

    def save_data(self, fc_data):
        n = str(self.num_fact_checkers)
        np.save('fc_data_' + n, fc_data)
        np.save('topics_data_' + n, self.all_topics)

    def plot_data(self, fc_data):
        for k, fc in fc_data.items():
            # line 1 points
            x1 = [x[1] for x in fc]
            y1 = [x[2] for x in fc]
            # plotting the line 1 points
            profile = fc[0][4]
            color = 'green' if profile[0] == 1 else 'purple' if profile[0] == 0.5 else 'red'
            # plt.plot(x1, y1, label=str(fc[0][0]), color=color)  # identifier
            plt.plot(x1, y1, color=color)  # identifier

        plt.xlabel('epoch/day')
        # Set the y axis label of the current axis.
        plt.ylabel('ether')

        # Set a title of the current axes.
        plt.title('Ether vs Epoch')
        # show a legend on the plot
        # plt.legend()
        # Display a figure.
        plt.savefig('ether_vs_epoch' + str(self.num_fact_checkers))
        plt.show()
        plt.clf()

        for k, fc in fc_data.items():
            # line 1 points
            x1 = [x[1] for x in fc]
            y1 = [x[3] for x in fc]
            # plotting the line 1 points
            profile = fc[0][4]
            color = 'green' if profile[0] == 1 else 'purple' if profile[0] == 0.5 else 'red'
            # plt.plot(x1, y1, label=str(fc[0][0]), color=color)  # identifier
            plt.plot(x1, y1, color=color)  # identifier

        plt.xlabel('epoch/day')
        # Set the y axis label of the current axis.
        plt.ylabel('reputation')

        # Set a title of the current axes.
        plt.title('Reputation vs Epoch')
        # show a legend on the plot
        # plt.legend()
        # Display a figure.
        plt.savefig('reputation_vs_epoch' + str(self.num_fact_checkers))
        plt.show()
        plt.clf()

        true_topics = []
        lie_topics = []
        equal_topics = []
        not_voted_topics = []
        temp = [true_topics, lie_topics, equal_topics, not_voted_topics]
        for topic in self.all_topics:

            r = topic.initial_reward
            if topic.true_votes == 0 and topic.lie_votes == 0:
                not_voted_topics.append(r)
            elif topic.true_votes > topic.lie_votes:
                true_topics.append(r)
            elif topic.lie_votes > topic.true_votes:
                lie_topics.append(r)
            else:
                equal_topics.append(r)

        bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0001]

        binned_results = []
        for idx, array in enumerate(temp):
            binned = [[], [], [], [], [], [], [], [], [], []]
            for initial_val in array:
                for i in range(len(bins) - 1):
                    if initial_val >= bins[i] and initial_val < bins[i+1]:
                        binned[i].append(initial_val)
            binned_results.append(binned)
            print(binned_results[idx])

        print("Success Rates for bins")
        success_rates = []
        for x in range(len(bins) - 1):
            success_rates.append(len(binned_results[0][x]) /
                                 (len(binned_results[0][x]) + len(binned_results[1][x]) +
                                  len(binned_results[2][x]) + len(binned_results[3][x])))

        # line 1 points
        x1 = bins[1:]
        y1 = success_rates
        # plotting the line 1 points
        plt.plot(x1, y1, color='green')  # identifier

        plt.xlabel('max ether')
        # Set the y axis label of the current axis.
        plt.ylabel('success rate')

        # Set a title of the current axes.
        plt.title('Success Rate vs Initial Ether')
        # show a legend on the plot
        # plt.legend()
        # Display a figure.
        plt.savefig('success_rate_vs_ether' + str(self.num_fact_checkers))
        plt.show()
        plt.clf()

        # PIE CHART
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'Success', 'Failure', 'Tie', 'No Votes'
        sizes = [len(x) for x in temp]
        total = sum(sizes)
        explode = (0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        p, tx, autotexts = ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                   shadow=True, startangle=45)

        # p, tx, autotexts = plt.pie(sizes, labels=labels, colors=colors,
        #                            autopct="", shadow=True)

        for i, a in enumerate(autotexts):
            a.set_text("{:.2f}% ({})".format(sizes[i]/total * 100, sizes[i]))

        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.axis('equal')
        plt.title('Distribution of Topics')

        plt.savefig('pie_chart_dist' + str(self.num_fact_checkers))
        plt.show()
        plt.clf()

        # Votes
        all_topics_binned = [[], [], [], [], [], [], [], [], [], []]
        for t in self.all_topics:
            initial_val = t.initial_reward
            for i in range(len(bins) - 1):
                if initial_val >= bins[i] and initial_val < bins[i+1]:
                    all_topics_binned[i].append(t)

        average_votes_per_bin = []
        for arr in all_topics_binned:
            total_for_bin = 0
            for t in arr:
                total_for_bin += len(t.voters)

            average_votes_per_bin.append(total_for_bin/len(arr))

        # line 1 points
        x1 = bins[1:]
        y1 = average_votes_per_bin
        # plotting the line 1 points
        plt.plot(x1, y1, color='blue')  # identifier

        plt.xlabel('max ether')
        # Set the y axis label of the current axis.
        plt.ylabel('votes')

        # Set a title of the current axes.
        plt.title('Average Number of Votes vs Initial Ether')
        # show a legend on the plot
        # plt.legend()
        # Display a figure.
        plt.savefig('average_votes_vs_ether' + str(self.num_fact_checkers))
        plt.show()
        plt.clf()


def main():
    s = Simulator()
    s.run_simulation()

    fact_checker_data, topic_data = s.retrieve_results()
    # for k, v in fact_checker_data.items():
    #     print('-' * 50)
    #     print(v)
    print('Topic Data:', topic_data)

    # print('x' * 50)
    # global important_votes
    # print(important_votes)

    s.save_data(fact_checker_data)
    s.plot_data(fact_checker_data)
    # print('-' * 50)
    # global all_times
    # print(all_times)

    # print('Hello World!')
    # s.generate_new_topics()
    # print(len(s.topics))
    # s.print_topics()
    # s.current_date = 3
    # s.remove_expired_topics()
    # print(len(s.topics))


if __name__ == "__main__":
    main()
