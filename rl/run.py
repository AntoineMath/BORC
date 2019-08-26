import pickle
import time
import numpy as np
import argparse
import re


from bt_sea_env import TradingEnv
from borc_agent import BorcAgent
from utils import get_data, get_scaler, maybe_make_dir


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--episode', type=int, default=100,
                        help='number of episode to run')
    parser.add_argument('-b', '--batch_size', type=int, default=32,
                        help='batch size for experience replay')
    parser.add_argument('-i', '--initial_invest', type=int, default=20000,
                        help='initial investment amount')
    parser.add_argument('-m', '--mode', type=str, required=True,
                        help='either "train" or "test"')
    parser.add_argument('-w', '--weights', type=str, help='a trained model weights')
    args = parser.parse_args()

    maybe_make_dir('weights')
    maybe_make_dir('portfolio_val')

    timestamp = time.strftime('%Y%m%d%H%M')

    data = np.around(get_data())
    train_data = data[:, :50]
    test_data = data[:, 3526:]

    env = TradingEnv(train_data, args.initial_invest)
    state_size = np.prod(env.observation_space.shape)
    action_size = env.action_space.n
    agent = BorcAgent(state_size, action_size)
    scaler = get_scaler(env)

    history = {"balance": [],
               "actions": [],
               "reward": []}

    if args.mode == 'test':
        # remake the env with test data
        env = TradingEnv(test_data, args.initial_invest)
        # load trained weights
        agent.load(args.weights)
        # when test, the timestamp is same as time when weights was trained
        timestamp = re.findall(r'\d{12}', args.weights)[0]

    for e in range(args.episode):
        balance_history = []
        actions_history = []
        rewards_history = []

        state = env.reset()
        state = scaler.transform([state])
        for time in range(env.n_step):
            action = agent.act(state)
            next_state, reward, done, info = env.step(action)
            next_state = scaler.transform([next_state])

            # add training log to history dict
            balance_history.append(info['cur_val'])
            actions_history.append(action)
            rewards_history.append(reward)

            if args.mode == 'train':
                agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print("episode: {}/{}, episode end value: {}".format(
                    e + 1, args.episode, info['cur_val']))
                break
            if args.mode == 'train' and len(agent.memory) > args.batch_size:
                agent.replay(args.batch_size)
        if args.mode == 'train' and (e + 1) % 10 == 0:  # checkpoint weights
            agent.save('weights/{}-dqn.h5'.format(timestamp))

            # save portfolio value history to disk
        history["balance"].append(balance_history)
        history["actions"].append(actions_history)
        history["reward"].append(rewards_history)
        with open('portfolio_val/{}-{}.p'.format(timestamp, args.mode), 'wb') as fp:
            pickle.dump(history, fp)

