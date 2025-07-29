import random
import numpy as np
from scipy.stats import beta, norm

class EntropyPairSelector:
    def posterior_conjugate(self, data, n_pts=100):
        """r heads in n tosses
        See: https://en.wikipedia.org/wiki/Conjugate_prior#Table_of_conjugate_distributions"""
        data = np.array(data)
        unique, counts = np.unique(data, return_counts=True)
        N = len(data)
        d = dict(zip(unique, counts))
        # print(f"d: {d}, unique: {unique}, count: {counts}")
        try:
            R = d[1]
        except:
            R = 0
        a = 1 # successes
        b = 1 # failures
        a_post = a + R
        b_post = b + N - R
        H = np.linspace(0, 1, n_pts)
        pdf = beta.pdf(H, a=a_post, b=b_post)
        mean = self.beta_mean(a_post, b_post)
        std_dev = self.beta_std_dev(a_post, b_post)
        entropy = beta.entropy(a_post, b_post, loc=mean, scale=std_dev)
        
        return pdf, entropy
    
    def beta_mean(self, alpha, beta):
        return alpha/(alpha+beta)

    def beta_variance(self, alpha, beta):
        return alpha * beta / (alpha + beta)**2 / (alpha+beta+1)

    def beta_std_dev(self, alpha, beta):
        return np.sqrt(self.beta_variance(alpha, beta))
    
    def generate_winner_dist(self, a, b, dist):
        """_summary_

        Args:
            a (int): the integer value representing the item being used for item a.
            b (int): the integer value representing the item being used for item b.
            dist (dict): the dictionary containing the sampling distributions to select the winner out of a or b.

        Returns:
            int: returns who wins the comparison.
        """
        a_dist = dist[a]
        b_dist = dist[b]

        a_sample = a_dist.rvs()
        b_sample = b_dist.rvs()

        if a_sample > b_sample:
            winner = a
        else:
            winner = b
        
        return winner
    
    def __init__(self, n_items):
        
        self.sample_size = n_items
        # self.results = []

    def make_distributions(self):
        dist = {}
        for i in range(self.sample_size):
            dist[i] = norm(loc=self.scores[i], scale=self.standard_dev)
        # distributions = make them
        return dist

    def run_entropy_pairs_simulation(
        self, 
        scores,
        std_dev,
        # distributions: dict,
        k = 10
    ):
        """_summary_

        Args:
            distributions (dict): _description_
            items (int): _description_
            k (int, optional): _description_. Defaults to 10.

        Returns:
            _type_: _description_
        """
        self.scores = scores
        self.standard_dev = std_dev
        self.results = []
        self.distributions = self.make_distributions()
        rounds      = 0
        # sample_size = items
        self.comparison_results = [[-1 if i >= j else []
                                for j in range(self.sample_size)]
                                  for i in range(self.sample_size)]
        self.entropy_results    = [[-1 if i >= j else []
                                for j in range(self.sample_size)]
                                  for i in range(self.sample_size)]
        n_rounds = self.sample_size * k
        items_to_select = []

        while rounds < n_rounds:
            items_to_select = []
            for i in range(len(self.comparison_results)):
                for j in range(len(self.comparison_results[i])):
                    if self.comparison_results[i][j] != -1:
                        post, entropy = self.posterior_conjugate(self.comparison_results[i][j], n_pts=1000)
                        self.entropy_results[i][j].append(entropy)
            
            highest_entropy = -10000
            for i in range(len(self.entropy_results)):
                for j in range(len(self.entropy_results[i])):
                    if self.entropy_results[i][j] != -1:
                        if self.entropy_results[i][j][-1] > highest_entropy:
                            items_to_select = []
                            highest_entropy = self.entropy_results[i][j][-1]
                            items_to_select.append([i,j]) 
                        elif self.entropy_results[i][j][-1] == highest_entropy:
                            items_to_select.append([i,j])

            selected_items = random.choice(items_to_select)
            a = selected_items[0]
            b = selected_items[1]
            items_to_select.remove(selected_items)
            winner = self.generate_winner_dist(a, b, self.distributions)

            self.results.append([a, b, winner])

            if winner == a:
                self.comparison_results[a][b].append(1)
            elif winner == b:
                self.comparison_results[a][b].append(0)

            rounds += 1
        