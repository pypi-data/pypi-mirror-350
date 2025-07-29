import numpy as np
import pandas as pd
import numpy as np
import ray
import matplotlib.pyplot as plt
import itertools as it


from scipy.stats import norm, beta
from itertools import combinations


class BayesianCJ:
    def __init__(self, n_items):
        self.n_items = n_items
        self.prob_dist = {k:[] for k in range(n_items)}
        self.comparison_results = [[-1 if i >= j else [] 
                               for j in range(self.n_items)] 
                                for i in range(self.n_items)]

    def run(
        self, 
        X: list
    ):
        """Runs the Bayesian CJ algorithm, fitting the 
        parameters to the pairwise comparison data results.

        Args:
            X (list): Inputted data following a n by 3 format (a, b, winner).
        """
        @ray.remote
        def _find_expected_score_thread(
            prob_matrix, 
            each_item, 
        ):
            options = list(range(self.n_items))
            checking = each_item
            exp_result = []
            for i in range(1, self.n_items+1):
                rank_position = i
                exp_result.append(self.find_position(options, rank_position, checking, prob_matrix))

            return each_item, exp_result

        @ray.remote
        def find_expected_score(prob_matrix, prob_dist
        ):
            futures = [_find_expected_score_thread.remote(prob_matrix, each_item)
                        for each_item in range(0, self.n_items)]
            results = ray.get(futures)
            for result in results:
                prob_dist[result[0]] = result[1]

            return prob_dist

        number_of_rounds = len(X)

        for _ in range(number_of_rounds):
            a = X[_][0]
            b = X[_][1]
            winner = X[_][2]

            if a > b:
                b, a = a, b

            if winner == a:
                self.comparison_results[a][b].append(1)
            elif winner == b:
                self.comparison_results[a][b].append(0)

            if _ == 0:
                p_matrix = self.create_cdf_matrix(self.comparison_results, 
                                                  self.n_items)
            else:
                p_matrix = self.update_cdf_matrix(self.comparison_results, 
                                                  p_matrix, 
                                                  a, b)

            a = X[_][0]
            b = X[_][1]
            winner = X[_][2]

        self.prob_dist = find_expected_score.remote(p_matrix,
                                                    self.prob_dist)
        self.prob_dist = ray.get(self.prob_dist)
        self.Er_scores = [self.expected_value(range(1,self.n_items+1),
                                                 self.prob_dist[key]) 
                                                    for key in self.prob_dist.keys()]
        self.rank = np.argsort(np.array(self.Er_scores))

    
    def expected_value(
        self, 
        values, 
        weights
    ):
        """_summary_

        Args:
            values (_type_): _description_
            weights (_type_): _description_

        Returns:
            _type_: _description_
        """
        values = np.asarray(values)
        weights = np.asarray(weights)

        return (values * weights).sum() / weights.sum()


    def create_cdf_matrix(
        self, 
        data: list, 
        sample_size: int
    ):
        """_summary_

        Args:
            data (list): _description_
            sample_size (int): _description_

        Returns:
            _type_: _description_
        """
        full_matrix = [[-1 if i >= j else [] for j in range(sample_size)] for i in range(sample_size)] 
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] != -1:
                    a_prob, b_prob = self.get_CDF(data[i][j])
                    full_matrix[i][j] = a_prob
                    full_matrix[j][i] = b_prob

        return full_matrix
    

    def update_cdf_matrix(
        self, 
        data: list, 
        full_matrix: list, 
        a: int, 
        b: int
    ):
        """

        Args:
            data (list): _description_
            full_matrix (list): _description_
            a (int): _description_
            b (int): _description_

        Returns:
            _type_: _description_
        """

        a_prob, b_prob = self.get_CDF(data[a][b])
        full_matrix[a][b] = a_prob
        full_matrix[b][a] = b_prob

        return full_matrix
    

    def get_CDF(self, data):
        """
            r heads in n tosses
            See: https://en.wikipedia.org/wiki/Conjugate_prior#Table_of_conjugate_distributions
        """
        data = np.array(data)
        unique, counts = np.unique(data, return_counts=True)
        N = len(data)
        d = dict(zip(unique, counts))
        try:
            R = d[1]
        except:
            R = 0
        a = 1 # successes
        b = 1 # failures
        a_post = a + R
        b_post = b + N - R
        p_a_wins = beta.cdf(1, a=a_post, b=b_post) - beta.cdf(0.5, a=a_post, b=b_post)
        p_b_wins = 1 - p_a_wins

        return p_a_wins, p_b_wins

    
    def find_position(
        self, 
        items_ops: list, 
        n: int, 
        check_item: int, 
        data: np.ndarray
    ):
        
        items = items_ops.copy()
        number_of_items = len(items)
        items.remove(check_item)

        # Generate all combinations of winning items
        winning_items = combinations(items, n-1)

        each_prod_combination_results = []
        for each_combination in winning_items:
            # Get indices of losing items
            losing_items = np.array(list(set(range(number_of_items)) - set(each_combination) - {check_item}))

            # Compute probabilities of winning and losing items
            prob_win = 1 - np.array([data[check_item][i] for i in each_combination])
            prob_lose = np.array([data[check_item][i] for i in losing_items])

            # Compute product of probabilities
            prod_win = np.multiply.reduce(prob_win)
            prod_lose = np.multiply.reduce(prob_lose)

            # Append product of probabilities to list
            each_prod_combination_results.append(prod_win * prod_lose)

        # Compute total result using numpy's einsum() function
        total_results = np.einsum('i->', each_prod_combination_results)

        return total_results


class BayesianCJMC:
    def check(self):
        print("BayesianCJMC")


import numpy as np
import pandas as pd
import numpy as np
import ray
import matplotlib.pyplot as plt
import itertools as it


from scipy.stats import norm, beta
from itertools import combinations

class MBayesianCJ:
    def __init__(
            self, 
            n_items, 
            weights
    ):
        self.n_items = n_items
        self.n_los = len(weights)
        self.weights = weights
        self.prob_dist      = {k:{j: [] for j in range(n_items)} 
                                for k in range(self.n_los)}
        self.lo_prob_des    = {k:{j: [] for j in range(n_items)}
                                for k in range(self.n_los)}
        self.lo_rank_scores = {k:{j: [] for j in range(n_items)}
                                for k in range(self.n_los)}


    def run(
        self, 
        results: list
    ):
        @ray.remote
        def _find_expected_score_thread(
            prob_matrix, 
            each_item, 
            sample_range
        ):
            options = list(range(sample_range))
            checking = each_item
            exp_result = []
            for i in range(1, sample_range+1):
                rank_position = i
                exp_result.append(find_position(options, rank_position,
                                                checking, prob_matrix))

            return each_item, exp_result
        
        @ray.remote
        def find_expected_score(
            prob_matrix, 
            prob_dist, 
            sample_range
        ):
            # expected_item_score = []
            # values = list(range(1, sample_range+1))
            # if len(prob_dist[a_b[0]]) == 0:
            futures = [_find_expected_score_thread.remote(prob_matrix, each_item, 
                                                        sample_range)
                    for each_item in range(0, sample_range)]
            results = ray.get(futures)
            for result in results:
                prob_dist[result[0]] = result[1]

            return prob_dist


        def find_position(
            items_ops, 
            n, 
            check_item, 
            data
        ):
            items = items_ops.copy()
            number_of_items = len(items)
            items.remove(check_item)

            # Generate all combinations of winning items
            winning_items = it.combinations(items, n-1)

            each_prod_combination_results = []
            for each_combination in winning_items:
                # Get indices of losing items
                losing_items = np.array(list(set(range(number_of_items)) - \
                                            set(each_combination) - {check_item}))

                # Compute probabilities of winning and losing items
                prob_win = 1 - np.array([data[check_item][i] 
                                            for i in each_combination])
                prob_lose = np.array([data[check_item][i] 
                                        for i in losing_items])

                # Compute product of probabilities
                prod_win = np.multiply.reduce(prob_win)
                prod_lose = np.multiply.reduce(prob_lose)

                # Append product of probabilities to list
                each_prod_combination_results.append(prod_win * prod_lose)

            # Compute total result using numpy's einsum() function
            total_results = np.einsum('i->', each_prod_combination_results)  # equivalent to np.sum(each_prod_combination_results)

            return total_results
        
        
        n_rounds = len(results)
        self.comparison_results, self.p_matrix = self.multiple_LO_comparisons_wd(n_rounds, 
                                                                  self.n_los, 
                                                                  self.n_items,  
                                                                  results)

        self.lo_prob_des, self.lo_rank_scores = self.calculate_lo_Er(self.comparison_results, 
                                                  self.p_matrix, 
                                                  self.prob_dist, 
                                                  self.lo_prob_des, 
                                                  self.lo_rank_scores, 
                                                  self.n_items)
        
        for i in range(len(self.comparison_results)):
            self.prob_dist[i] = find_expected_score.remote(self.p_matrix[i], self.prob_dist[i], self.n_items)
            self.prob_dist[i] = ray.get(self.prob_dist[i])
            self.lo_prob_des[i] = self.prob_dist
            self.lo_rank_scores[i] = [self.expected_value(range(1,self.n_items+1), self.prob_dist[i][key]) 
                                    for key in self.prob_dist[i].keys()]
            
        self.weighted_ensemble_dist = self.weighted_ensemble(self.p_matrix, self.weights)

    def weighted_ensemble(
        self,
        p_mat, 
        weights
    ):
        @ray.remote
        def _find_expected_score_thread(
            prob_matrix, 
            each_item, 
            sample_range
        ):
            options = list(range(sample_range))
            checking = each_item
            exp_result = []
            for i in range(1, sample_range+1):
                rank_position = i
                exp_result.append(find_position(options, rank_position,
                                                checking, prob_matrix))

            return each_item, exp_result
        
        @ray.remote
        def find_expected_score(
            prob_matrix, 
            prob_dist, 
            sample_range
        ):
            # expected_item_score = []
            # values = list(range(1, sample_range+1))
            # if len(prob_dist[a_b[0]]) == 0:
            futures = [_find_expected_score_thread.remote(prob_matrix, each_item, 
                                                        sample_range)
                    for each_item in range(0, sample_range)]
            results = ray.get(futures)
            for result in results:
                prob_dist[result[0]] = result[1]

            return prob_dist
        
        def find_position(
            items_ops, 
            n, 
            check_item, 
            data
        ):
            items = items_ops.copy()
            number_of_items = len(items)
            items.remove(check_item)

            # Generate all combinations of winning items
            winning_items = it.combinations(items, n-1)

            each_prod_combination_results = []
            for each_combination in winning_items:
                # Get indices of losing items
                losing_items = np.array(list(set(range(number_of_items)) - \
                                            set(each_combination) - {check_item}))

                # Compute probabilities of winning and losing items
                prob_win = 1 - np.array([data[check_item][i] 
                                            for i in each_combination])
                prob_lose = np.array([data[check_item][i] 
                                        for i in losing_items])

                # Compute product of probabilities
                prod_win = np.multiply.reduce(prob_win)
                prod_lose = np.multiply.reduce(prob_lose)

                # Append product of probabilities to list
                each_prod_combination_results.append(prod_win * prod_lose)

            # Compute total result using numpy's einsum() function
            total_results = np.einsum('i->', each_prod_combination_results)  # equivalent to np.sum(each_prod_combination_results)

            return total_results

        sample_size = len(p_mat[0][0])
        n_los = len(p_mat)
        WE_prob_dist_combined = {k:[] for k in range(sample_size)}
        WE_p_matrix = [[-1 if i >= j else [] for j in range(sample_size)] for i in range(sample_size)]

        for row in range(len(p_mat[0])):
            for col in range(len(p_mat[0][row])):
                if p_mat[0][row][col] != -1:
                    prob = self.combine_weighted_ensemble(n_los, p_mat, weights, row, col)
                    WE_p_matrix[row][col] = prob
                    WE_p_matrix[col][row] = 1 - prob
        
        WE_prob_dist_combined = find_expected_score.remote(WE_p_matrix, WE_prob_dist_combined, sample_size)
        WE_prob_dist_combined = ray.get(WE_prob_dist_combined)
        WE_rank_scores = [self.expected_value(range(1,sample_size+1), WE_prob_dist_combined[key]) for key in WE_prob_dist_combined.keys()]
        self.WE_res         = np.argsort(np.array(WE_rank_scores))
        
        # print(f"Combined beta WCDF rank: {WE_res}")
        # print(f"Tau WCDF score: {normalised_kendall_tau_distance(WE_res, rank)}")
        # WE_tau = normalised_kendall_tau_distance(WE_res, rank)

        return WE_prob_dist_combined
    
    def expected_value(
            self,
        values, 
        weights
    ):
        """_summary_

        Args:
            values (_type_): _description_
            weights (_type_): _description_

        Returns:
            _type_: _description_
        """
        values = np.asarray(values)
        weights = np.asarray(weights)

        return (values * weights).sum() / weights.sum()
    
    def combine_weighted_ensemble(
            self,
        n_lo: int, 
        cdf_matrix: list, 
        weights: list, 
        row: int, 
        col: int
    ):
        samples = []
        for i in range(n_lo):
            samples.append(cdf_matrix[i][row][col] * weights[i])
        
        weighted_ensemble_res = np.sum(samples)/np.sum(weights)

        return weighted_ensemble_res

    def check(self):
        print("Multi-Criterion BayesianCJMC")

    def multiple_LO_comparisons_wd(
            self,
        n_rounds: int, 
        n_lo: int, 
        sample_size: int,
        results 
    ):
        
        comparison_results = self.create_half_matrix(sample_size, n_lo)
        entropy_results    = self.create_half_matrix(sample_size, n_lo)
        total_entropy      = [[-1 if i >= j else [] for j in range(sample_size)] for i in range(sample_size)]
        for rounds in range(n_rounds):
            
            for lo in range(n_lo):
                # s_lo = lo
                a = results[rounds][0]
                b = results[rounds][1]
                
                winner = results[rounds][lo+2]

                if winner == a:
                    comparison_results[lo][a][b].append(1)
                elif winner == b:
                    comparison_results[lo][a][b].append(0)
                
                if rounds == 0:
                    p_matrix = self.create_cdf_matrix(comparison_results, 
                                                sample_size, n_lo)
                else:
                    p_matrix = self.update_cdf_matrix(comparison_results, p_matrix, 
                                                a, b, lo)

        return comparison_results, p_matrix
    
    def create_half_matrix(self, sample_size, lo_n):
        half_a = []
        for i in range(lo_n):
            half_a.append([[-1 if i >= j else [] for j in range(sample_size)] for i in range(sample_size)])

        return half_a
    
    def create_cdf_matrix(
            self,
        data, 
        sample_size, 
        n_lo
    ):
        """_summary_

        Args:
            data (_type_): _description_
            sample_size (_type_): _description_

        Returns:
            _type_: _description_
        """
        full_matrix = []
        for n in range(n_lo):
            full_matrix.append([[-1 if i >= j else [] for j in range(sample_size)]
                                    for i in range(sample_size)])

        for lo in range(n_lo):
            for i in range(len(data[lo])):
                for j in range(len(data[lo][i])):
                    if data[lo][i][j] != -1:
                        a_prob, b_prob = self.get_CDF(data[lo][i][j])
                        full_matrix[lo][i][j] = a_prob
                        full_matrix[lo][j][i] = b_prob

        return full_matrix
    
    def update_cdf_matrix(
            self,
        data, 
        full_matrix, 
        a, 
        b, 
        lo
    ):
        """_summary_

        Args:
            data (_type_): _description_
            sample_size (_type_): _description_

        Returns:
            _type_: _description_
        """
        # full_matrix = [[-1 if i >= j else [] for j in range(sample_size)] for i in range(sample_size)] 
        # for i in range(len(data)):
        #     for j in range(len(data[i])):
        #         if data[i][j] != -1:
        a_prob, b_prob = self.get_CDF(data[lo][a][b])
        full_matrix[lo][a][b] = a_prob
        full_matrix[lo][b][a] = b_prob

        return full_matrix
    
    def get_CDF(self, data):
        """
            r heads in n tosses
            See: https://en.wikipedia.org/wiki/Conjugate_prior#Table_of_conjugate_distributions
        """
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
        p_a_wins = beta.cdf(1, a=a_post, b=b_post) \
            - beta.cdf(0.5, a=a_post, b=b_post)
        p_b_wins = 1 - p_a_wins

        return p_a_wins, p_b_wins
    
    def calculate_lo_Er(
            self,
        comparison_results, 
        p_matrix, 
        prob_dist, 
        lo_prob_des, 
        lo_rank_scores, 
        sample_size
    ):
        @ray.remote
        def _find_expected_score_thread(
            prob_matrix, 
            each_item, 
            sample_range
        ):
            options = list(range(sample_range))
            checking = each_item
            exp_result = []
            for i in range(1, sample_range+1):
                rank_position = i
                exp_result.append(find_position(options, rank_position,
                                                checking, prob_matrix))

            return each_item, exp_result
        
        @ray.remote
        def find_expected_score(
            prob_matrix, 
            prob_dist, 
            sample_range
        ):
            # expected_item_score = []
            # values = list(range(1, sample_range+1))
            # if len(prob_dist[a_b[0]]) == 0:
            futures = [_find_expected_score_thread.remote(prob_matrix, each_item, 
                                                        sample_range)
                    for each_item in range(0, sample_range)]
            results = ray.get(futures)
            for result in results:
                prob_dist[result[0]] = result[1]

            return prob_dist
        
        def find_position(
            items_ops, 
            n, 
            check_item, 
            data
        ):
            items = items_ops.copy()
            number_of_items = len(items)
            items.remove(check_item)

            # Generate all combinations of winning items
            winning_items = it.combinations(items, n-1)

            each_prod_combination_results = []
            for each_combination in winning_items:
                # Get indices of losing items
                losing_items = np.array(list(set(range(number_of_items)) - \
                                            set(each_combination) - {check_item}))

                # Compute probabilities of winning and losing items
                prob_win = 1 - np.array([data[check_item][i] 
                                            for i in each_combination])
                prob_lose = np.array([data[check_item][i] 
                                        for i in losing_items])

                # Compute product of probabilities
                prod_win = np.multiply.reduce(prob_win)
                prod_lose = np.multiply.reduce(prob_lose)

                # Append product of probabilities to list
                each_prod_combination_results.append(prod_win * prod_lose)

            # Compute total result using numpy's einsum() function
            total_results = np.einsum('i->', each_prod_combination_results)  # equivalent to np.sum(each_prod_combination_results)

            return total_results
        
        for i in range(len(comparison_results)):
            prob_dist[i] = find_expected_score.remote(p_matrix[i], prob_dist[i], 
                                                    sample_size)
            prob_dist[i] = ray.get(prob_dist[i])
            lo_prob_des[i] = prob_dist
            lo_rank_scores[i] = [self.expected_value(range(1,sample_size+1), prob_dist[i][key])
                                    for key in prob_dist[i].keys()]

            return lo_prob_des, lo_rank_scores