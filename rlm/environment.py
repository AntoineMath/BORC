#An environment contains all the necessary functionnality to run and allow it to learn
import gym
import json


class TradingEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(TradingEnvironment, self).__init__()
        self.df = df
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)

        #Actions Buy x%, Sell x%, Hold
        self.action_space = spaces.Box(low=np.array([0, 0]),
                                       high=np.array([3, 1]),
                                       dtype=np.float16)

        #Prices contains the OHLCVQNTT values for the last 5 prices
        self.observation_space = spaces.Box(low=0,
                                            high=1,
                                            shape=(6, 6),
                                            dtype=np.float16)

    def reset(self):
        #Reset the state of the environment to an initial state
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.max_net_worth = INITIAL_ACCOUNT_BALANCE
        self.shares_held = 0
        self.cost_basis = 0
        self.total_shares_sold = 0
        self.total_sales_value = 0

        #Set the cuurent step to a random point within the data frame
        self.current_step = random.randint(
            0,
            len(self.df.loc[:, 'open'].values) - 6)

        return self._next_observation()

    def _next_observation(self):
        #Get the data points for the last 5 days and scale to 0-1
        self.df.loc[self.current_step:self.current_step + 5, 'open' /
                    MAX_SHARE_PRICE]
        self.df.loc[self.current_step:self.current_step + 5, 'high' /
                    MAX_SHARE_PRICE]
        self.df.loc[self.current_step:self.current_step + 5, 'low' /
                    MAX_SHARE_PRICE]
        self.df.loc[self.current_step:self.current_step + 5, 'close' /
                    MAX_SHARE_PRICE]
        self.df.loc[self.current_step:self.current_step + 5, 'volume' /
                    MAX_SHARE_PRICE]
        self.df.loc[self.current_step:self.current_step +
                    5, 'quote_asset_volume' / MAX_SHARE_PRICE]
        self.df.loc[self.current_step:self.current_step +
                    5, 'number_of_trades' / MAX_SHARE_PRICE]
        self.df.loc[self.current_step:self.current_step +
                    5, 'optaker_buy_base_asset_volumeen' / MAX_SHARE_PRICE]
        self.df.loc[self.current_step:self.current_step +
                    5, 'taker_buy_quote_asset_volume' / MAX_SHARE_PRICE]

        #Append additional data and scale each value to 0-1
        obs = np.append(frame, [[
            self.balance / MAX_ACCOUNT_BALANCE, self.max_net_worth /
            MAX_ACCOUNT_BALANCE, self.shares_held / MAX_NUM_SHARES,
            self.cost_basis / MAX_SHARE_PRICE,
            self.total_shares_sold / MAX_NUM_SHARES, self.total_sales_value /
            (MAX_NUM_SHARES * MAX_SHARE_PRICE)
        ]])

        return obs

    def step(self, action):
        #Execute one time step within the environment
        self._take_action(action)

        self.current_step += 1

        if self.current_step > len(self.df.loc[:'open'].values) - 6:
            self.current_step = 0

        delay_modifier = (self.current_step / MAX_STEPS)

        reward = self.balance * delay_modifier
        done = self.net_worth  <= 0

        obs = self._next_observation()

        return obs, reward, done, {}

    def _take_action(self, action):
        #Set the current price to a random price within the time step
        current_price = random.uniform(
            self.df.loc[self.current_step, 'open'],
            self.df.loc[self.current_step, 'close']
        )

        action_type = action[0]
        amount = action[1]

        if action_type < 1:
            #Buy amount % of balance in shares
            total_possible = self.balance / current_price
            shares_bought = total_possible * amount
            prev_cost = self = self.cost_basis * self.shares_held
            additional_cost = shares_bought * current_price

            self.balance -= additional_cost
            self.cost_basis = (prev_cost + additional_cost) / (self.shares_held + shares_bought)
            self.shares_held += shares_bought

        elif action_type < 2:
            #Sell amount % of shares held
            shares_sold = self.shares_held * amount
            self.balance += shares_sold * current_price
            self.shares_held -= shares_sold
            self.total_shares_sold += shares_sold
            self.total_sales_value += shares_sold * current_price

        self.netWorth = self.balance + self.shares_held * current_price

        if self.net_worth > self.max_net_worth:
            self.max_net_worth = net_worth

        if self.shares_held == 0:
            self.cost_basis = 0


    def render(self, mode='human', close=False):
        # Render the environment to the screen
        profit = self.net_worth - INITIAL_ACCOUNT_BALANCE

        print(f'Step: {self.current_step}')
        print(f'Balance: {self.balance}')
        print(
            f'Shares held: {self.shares_held} (Total sold: {self.total_shares_sold})'
        )
        print(
            f'Avg cost for held shares: {self.cost_basis} (Total sales value: {self.total_sales_value})'
        )
        print(f'Net worth: {self.net_worth} (Max net worth: {self.max_net_worth})')
        print(f'Profit: {profit}')
