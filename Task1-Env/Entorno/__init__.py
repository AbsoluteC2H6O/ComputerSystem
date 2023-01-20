from gym.envs.registration import register

register(
    id='TwoArmedBandit-v1',
    entry_point='Agente.Actividad1.Entorno.bandits:TwoArmedBanditEnv',
)