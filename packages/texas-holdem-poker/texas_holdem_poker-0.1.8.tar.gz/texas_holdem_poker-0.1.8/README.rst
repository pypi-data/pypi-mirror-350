========================
Texas Holdem Poker
========================
This is a package including a command-line-interacted simulated texas holdem poker game, and a winning-rate calculator

In this game, you will play holdem and compete with AI which is based on Monte Carlo method and Kelly formula

If you are interested in poker game like this, try and enjoy!


德州扑克模拟器

这个包包含了一个命令行交互形式的德州扑克游戏，以及包含一个实时胜率计算器

在该游戏中，你将与其他基于蒙特卡洛算法与凯利公式设计的AI玩家进行对抗

如果你也对德州扑克感兴趣，不妨一起来试一试吧！


========================
1.How to install
========================

::

    pip install texas_holdem_poker

========================
2.How to play
========================
------------------------
HoldemGame
------------------------
class HoldemGame is a simulator of texas holdem poker game

to start the game, just import this class and call 'run' method

::

    from texas_holdem_poker import HoldemGame

    HoldemGame().run()

And it will work like this

::

                Texas Holdem Poker Simulator


    Your money: 1000
    Player1 money: 1000
    Player2 money: 1000
    Player3 money: 1000
    Player4 money: 1000
    Player5 money: 1000

    Round: 0
    now your turn, your cards: [♦K, ♠K]
    remaining money: 5000, already bet: 0
    input your bet:

And then, input your bet(bet should be an integer) to action!
    fold if input < 0

    check if input == 0 == bottom

    call if input <= bottom

    raise if input > bottom


------------------------
Calculator
------------------------
class Calculator is designed for winning-rate calculation

::

        from texas_holdem_poker import Calculator

        Calculator(simulate_times=1500).run()

And it will work like this

::

    Input your hand cards, for examples: "SJ S10", S=Spade♠, C=Club♣, H=Heart♥, D=Diamond♦
    SJ S10
    Input community cards, can be empty

    Input total players and total remaining players(include yourself), for examples:"6 2"
    6 2
    Win Rate: 0.6093

through pip and pypi, you can easily use it anywhere and on any devices which can run python