import numpy as np
from scipy.optimize import minimize

class BTMCJ:
    def __init__(self, n_items):
        self.n_items = n_items

    def run(self, X):
        self.m = np.asarray([[0 if i!=j else -1 
              for j in range(self.n_items)] 
                for i in range(self.n_items)])

        number_of_rounds = len(X)
        for _ in range(number_of_rounds):
            a = X[_][0]
            b = X[_][1]
            winner = X[_][2]

            if winner == a:
                self.m[a][b] += 1
            elif winner == b:
                self.m[b][a] += 1

        self.results = self.btm_model(self.m, fix_theta=None, max_iter=100, conv=0.0001, eps=0.3)

        self.scores = []
        for i in range(self.n_items):
            self.scores.append(self.results[i]['theta']) 
        
        self.rank = np.argsort(self.scores)[::-1]

        self.ssr = self.calculate_ssr(self.results)

        # Assuming 'out' is your list of results from the model
        self.rank_order = self.create_rank_order(self.results)

        self.sorted_results = sorted(self.results, key=lambda x: x['theta'], reverse=True)


    def uniq_teams(self, dat):
        chosen_teams = [d['chosen'] for d in dat]
        not_chosen_teams = [d['notChosen'] for d in dat]
        all_teams = list(range(self.n_items))
        return sorted(all_teams)

    def team_index(self, teams, col_data):
        return [teams.index(team) if team in teams else -1 for team in col_data]

    def calc_scores(self, dat, n_teams):
        scores = [0] * n_teams
        for num in dat:
            scores[num] += 1
        return scores

    def epsilon_adjustment(self, scores, max_scores, eps):
        return [eps + (max_scores[i] - 2 * eps) * scores[i] / max_scores[i] for i in range(len(scores))]

    def prop_score(self, scores, max_scores):
        return [scores[i] / max_scores[i] for i in range(len(scores))]

    def qlogis(self, propscore):
        return [np.log(p / (1 - p)) for p in propscore]

    def match_to_theta(self, matches, theta):
        return [theta[matches[i]] for i in range(len(matches))]

    def calc_m13(self, M11, M12, delta):
        return [delta + (M11[i] + M12[i]) / 2 for i in range(len(M11))]

    def exp_vec(self, vec):
        return [np.exp(v) for v in vec]

    def row_sums(self, expM11, expM12, expM13):
        return [expM11[i] + expM12[i] + expM13[i] for i in range(len(expM11))]

    def div_vecs(self, dat1, dat2):
        return [dat1[i] / dat2[i] for i in range(len(dat1))]

    def add_vecs(self, dat1, dat2):
        return [dat1[i] + dat2[i] for i in range(len(dat1))]

    def theta_change(self, theta, theta0):
        return max([abs(theta[i] - theta0[i]) for i in range(len(theta))])

    def fac(self, M11, M13):
        return [(M11[i] + M13[i]) / 2 for i in range(len(M11))]

    def group_sum(self, vals, grp, TP):
        out = [0] * TP
        for i in range(len(vals)):
            out[grp[i]] += vals[i]
        return out

    def calc_d(self, h1, h2, score):
        return [score[i] - (h1[i] + h2[i]) for i in range(len(h1))]

    def calc_d2(self, h1, h2):
        return [h1[i] + h2[i] + 1e-21 for i in range(len(h1))]

    def se_theta(self, d2):
        return [np.sqrt(1 / d2[i]) for i in range(len(d2))]

    def second_deriv(self, col1, col2):
        return [col1[i] * (1 - col1[i] - col2[i] / 2) + col2[i] / 2 * (0.5 - col1[i] - col2[i] / 2) for i in range(len(col1))]

    def change_inc(self, incr, maxincr):
        return [maxincr * self.sign(incr[i]) if abs(incr[i]) > maxincr else incr[i] for i in range(len(incr))]
    
    def sign(self, val):
        if val > 0:
            return 1
        elif val < 0:
            return -1
        elif val == 0:
            return 0


    def cent_theta(self, theta):
        avg = sum(theta) / len(theta)
        return [theta[i] - avg for i in range(len(theta))]

    def fixed_theta_index(self, fixed, teams):
        out = [None] * len(teams)
        for f in fixed:
            indx = teams.index(f['team'])
            out[indx] = f['theta']
        return out

    def matrix_to_dat(self, matrix):
        dat = []
        n = matrix.shape[0]
        for i in range(n):
            for j in range(n):
                if matrix[i, j] > matrix[j, i]:
                    dat.append({'chosen': i, 'notChosen': j})
        return dat
    
    def calculate_ssr(self, results):
        """
        Calculate the Scale Separation Reliability (SSR) metric.
        SSR is defined as the ratio of the variance of the thetas to the sum of the variance of the thetas and the average squared standard error.
        """
        thetas = [result['theta'] for result in results]
        se_thetas = [result['seTheta'] for result in results]
        
        variance_theta = np.var(thetas, ddof=1)
        mean_se_theta_squared = np.mean([se**2 for se in se_thetas])
        
        ssr = variance_theta / (variance_theta + mean_se_theta_squared)
        
        return ssr
    
    def create_rank_order(self, results):
        # Sort the results based on theta values in descending order
        sorted_results = sorted(results, key=lambda x: x['theta'], reverse=True)
        # Create the rank order
        rank_order = [{'team': result['team'], 'rank': index + 1} for index, result in enumerate(sorted_results)]
        return rank_order

    

    def btm_model(self, matrix, fix_theta=None, max_iter=100, conv=0.0001, eps=0.3, callback=None):
        dat = self.matrix_to_dat(matrix)
        # start = time.time()
        delta = -99
        center_theta = True
        teams = self.uniq_teams(dat)
        anchor_in = None
        if fix_theta:
            center_theta = False
            anchor_in = self.fixed_theta_index(fix_theta, teams)
        TP = len(teams)
        chosen_teams = [d['chosen'] for d in dat]
        dat01 = self.team_index(teams, chosen_teams)
        wins = self.calc_scores(dat01, TP)
        not_chosen_teams = [d['notChosen'] for d in dat]
        dat02 = self.team_index(teams, not_chosen_teams)
        losses = self.calc_scores(dat02, TP)
        maxscore = self.add_vecs(wins, losses)
        score = self.epsilon_adjustment(wins, maxscore, eps)
        prop_scores = self.prop_score(score, maxscore)
        theta = self.qlogis(prop_scores)
        max_change = 1e5
        iter = 0
        incrfac = 0.98
        maxincr = 1
        se_th = None

        while iter < max_iter and max_change > conv:
            theta0 = theta.copy()
            M11 = self.match_to_theta(dat01, theta)
            M12 = self.match_to_theta(dat02, theta)
            M13 = self.calc_m13(M11, M12, delta)
            expM11 = self.exp_vec(M11)
            expM12 = self.exp_vec(M12)
            expM13 = self.exp_vec(M13)
            rowsums = self.row_sums(expM11, expM12, expM13)
            dexpM11 = self.div_vecs(expM11, rowsums)
            dexpM12 = self.div_vecs(expM12, rowsums)
            dexpM13 = self.div_vecs(expM13, rowsums)
            maxincr *= incrfac
            fac1 = self.fac(dexpM11, dexpM13)
            fac2 = self.fac(dexpM12, dexpM13)
            h1 = self.group_sum(fac1, dat01, TP)
            h2 = self.group_sum(fac2, dat02, TP)
            d1 = self.calc_d(h1, h2, score)
            d2a = self.second_deriv(dexpM11, dexpM13)
            d2b = self.second_deriv(dexpM12, dexpM13)
            h21 = self.group_sum(d2a, dat01, TP)
            h22 = self.group_sum(d2b, dat02, TP)
            d2 = self.calc_d2(h21, h22)
            incr = self.div_vecs(d1, d2)
            incr = self.change_inc(incr, maxincr)
            theta = self.add_vecs(theta, incr)
            se_th = self.se_theta(d2)
            if center_theta:
                theta = self.cent_theta(theta)
            if fix_theta:
                for j in range(len(theta)):
                    if anchor_in[j] is not None:
                        theta[j] = anchor_in[j]
                        se_th[j] = 0
            iter += 1
            max_change = self.theta_change(theta, theta0)

        # end = time.time()
        # elapsed_time = end - start
        out = [{
            'team': teams[i],
            'theta': theta[i],
            'seTheta': se_th[i],
            'wins': wins[i],
            'losses': losses[i],
            'matches': maxscore[i],
            'score': score[i],
            'propScore': prop_scores[i]
        } for i in range(len(theta))]

        if callback:
            return callback(None, out)
        else:
            return out
        

class BradleyTerryModelOG:
    def __init__(self, n_items):
        self.n_items = n_items

    def run(self, results):
        number_of_rounds = len(results)
        m = np.zeros((self.n_items, self.n_items))

        for _ in range(number_of_rounds):
            a = results[_][0]
            b = results[_][1]
            winner = results[_][2]

            # Update comparison results
            if winner == a:
                m[a][b] += 1
            elif winner == b:
                m[b][a] += 1

        p = np.ones(self.n_items)
        for _ in range(1000):
            p_prime = np.zeros_like(p)
            for i in range(self.n_items):
                denominator_sum = 0
                w_sum = np.sum(m[i, :])  # Total wins for item i
                for j in range(self.n_items):
                    if i != j:
                        r = (m[i, j] + m[j, i]) / (p[i] + p[j])
                        denominator_sum += r

                if denominator_sum > 0:
                    p_prime[i] = w_sum / denominator_sum

            p_norm = np.sum(p_prime)
            if p_norm > 0:
                p = p_prime / p_norm

        p_scaled = p * 100
        self.rank = np.argsort(-p_scaled)
        self.p = p